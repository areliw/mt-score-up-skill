#!/usr/bin/env python3
"""qc_setup_check — before you draw a Levey-Jennings chart: is this control data good enough to set the
lab's OWN mean/SD and limits? Checks points, distinct days and lot, then computes the limits.

Black-box tool for lab-management-judgment. Run --help first; read the source only if a check fails.
Rules come from:
  - lab-management-judgment card rule #1 + the harder trap under it: set QC limits from the lab's own
    mean/SD, never the package insert (that is a peer range -> loose limits that hide error); >= 20 points
    on >= 20 different days (20 points in one day = within-run SD only -> limits too narrow -> false
    rejects); a new control/reagent lot gets its own mean/SD - never carry the old lot's values
  - LAB-MANAGEMENT digest §2 (lab mean/SD from >= 20 runs; %CV = SD/mean x 100)
  - 505402 Clinical Chemistry digest §1.4 (OCV = 20 repeats in one run vs RCV = control daily for 20 days)
    and §2.1 (SD with n-1)
Statistics are plain mean / SD (n-1) / %CV (stdlib); the Westgard evaluation itself is clinchem-judgment
`scripts/westgard.py` - not repeated here. ADVISORY ONLY: the QC policy of the lab decides.

Input CSV header: date,value[,lot][,level]   (date as YYYY-MM-DD; one row per control result)

Examples
  python qc_setup_check.py ../data/qc_setup_example.csv
  python qc_setup_check.py ../data/qc_setup_example.csv --insert-low 90 --insert-high 110 --json
"""
import argparse
import csv
import json
import statistics
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

MIN_POINTS = 20   # card rule #1
MIN_DAYS = 20     # card rule #1 (the harder trap)


def distinct_days(rows):
    return len({r["date"] for r in rows})


def evaluate_group(rows, lot_recorded, insert=None):
    vals = [r["value"] for r in rows]
    n, days = len(vals), distinct_days(rows)
    out = {"n": n, "days": days, "problems": []}
    if n >= 2:
        mean = statistics.fmean(vals)
        sd = statistics.stdev(vals)
        out.update(mean=mean, sd=sd, cv_pct=sd / mean * 100 if mean else None,
                   limits={k: (mean - m * sd, mean + m * sd) for k, m in (("1SD", 1), ("2SD", 2), ("3SD", 3))})
    if n < MIN_POINTS:
        out["problems"].append("only %d points (< %d)" % (n, MIN_POINTS))
    if days < MIN_DAYS:
        msg = "only %d distinct day(s) (< %d)" % (days, MIN_DAYS)
        if n >= MIN_POINTS:
            msg += " -> this SD is mostly within-run (OCV-like): limits too narrow -> false rejects"
        out["problems"].append(msg)
    if not lot_recorded:
        out["problems"].append("lot not recorded -> cannot confirm the data come from ONE lot")
    if insert and "limits" in out:
        lo, hi = out["limits"]["2SD"]
        width_lab = hi - lo
        width_ins = insert[1] - insert[0]
        out["insert_vs_lab_2sd_width"] = width_ins / width_lab if width_lab else None
    out["verdict"] = "READY: set limits from these data" if not out["problems"] else "NOT READY"
    return out


def check(rows, insert=None):
    lot_recorded = all(r.get("lot") for r in rows)
    groups = {}
    for r in rows:
        groups.setdefault((r.get("level") or "-", r.get("lot") or "?"), []).append(r)
    res = {"groups": [], "notes": []}
    levels = {}
    for (lv, lot), rs in sorted(groups.items()):
        levels.setdefault(lv, []).append(lot)
        g = evaluate_group(rs, lot_recorded, insert)
        g.update(level=lv, lot=lot)
        res["groups"].append(g)
    for lv, lots in levels.items():
        if len(lots) > 1:
            res["notes"].append("level %s has %d lots (%s): each lot needs its own mean/SD - do not carry or pool "
                                "across lots" % (lv, len(lots), ", ".join(lots)))
    if insert:
        res["notes"].append("package-insert range %g-%g is a peer/manufacturer range, not this analyser's "
                            "performance -> use the lab-derived limits (card rule #1)" % insert)
    return res


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = [{k.strip().lower(): (v or "").strip() for k, v in r.items()}
                for r in csv.DictReader(ln for ln in f if not ln.lstrip().startswith("#"))]
    out = []
    for r in rows:
        if r.get("value"):
            out.append({"date": r["date"], "value": float(r["value"]), "lot": r.get("lot", ""), "level": r.get("level", "")})
    return out


def main(argv=None):
    try:  # never crash a non-UTF-8 console (e.g. Thai cp874) on the section sign / Thai text
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--insert-low", type=float, help="package insert / manufacturer range low (for contrast)")
    ap.add_argument("--insert-high", type=float)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    insert = (a.insert_low, a.insert_high) if a.insert_low is not None and a.insert_high is not None else None
    res = check(load(a.csv), insert)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("%-6s %-10s %-4s %-5s %-9s %-8s %-7s %s" % ("level", "lot", "n", "days", "mean", "SD", "CV%", "+/-2SD"))
    for g in res["groups"]:
        if "mean" in g:
            lo, hi = g["limits"]["2SD"]
            print("%-6s %-10s %-4d %-5d %-9.4g %-8.4g %-7.3g %.4g-%.4g" % (g["level"], g["lot"], g["n"], g["days"],
                                                                         g["mean"], g["sd"], g["cv_pct"], lo, hi))
        else:
            print("%-6s %-10s %-4d %-5d (too few points)" % (g["level"], g["lot"], g["n"], g["days"]))
        for p in g["problems"]:
            print("%8s- %s" % ("", p))
        if g.get("insert_vs_lab_2sd_width"):
            print("%8s- insert range is %.1fx the width of the lab +/-2SD" % ("", g["insert_vs_lab_2sd_width"]))
        print("%8s=> %s" % ("", g["verdict"]))
    for n in res["notes"]:
        print("NOTE: " + n)
    print("ADVISORY: decision support only - QC limits per the lab QC policy; Westgard evaluation: "
          "clinchem-judgment scripts/westgard.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
