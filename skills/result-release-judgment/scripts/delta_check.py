#!/usr/bin/env python3
"""delta_check — compare a patient's current result with the previous one against the LAB'S delta
limits (absolute and/or percent) and say what to do when it fires.

Black-box tool for result-release-judgment. Run --help first; read the source only if a check fails.
Logic comes from the result-release-judgment card:
  rule #1 / Fork 2  a delta flag means "do not believe the change yet": rule out specimen mix-up /
                    mislabel FIRST (most dangerous), then pre-analytical/analytical artifact, then real
                    change (treatment / transfusion / timing). Follow the analyte-specific SOP.
  Fork 2            "the new value looks plausible" is NOT a reason to release (plausible != right patient);
                    several analytes shifting together raises suspicion of a mix-up (not proof).
Formulas: delta = current - previous; percent delta = (current - previous) / previous x 100.
Delta limits are lab- and analyte-specific -> always passed in; nothing is built in.
ADVISORY ONLY: release/hold follows the lab SOP and an authorised MT.

Single analyte
  python delta_check.py --prev 4.0 --cur 6.1 --pct-limit 20
  python delta_check.py --prev 4.0 --cur 6.1 --abs-limit 1.0 --ref-low 3.5 --ref-high 5.0
Panel (CSV header: analyte,prev,cur,abs_limit,pct_limit[,ref_low,ref_high])
  python delta_check.py --panel ../data/delta_panel_example.csv
  python delta_check.py --panel ../data/delta_panel_example.csv --json
"""
import argparse
import csv
import json
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

INVESTIGATE = ["1 specimen identity / mix-up / mislabel (check ID, collection time) - most dangerous",
               "2 pre-analytical / analytical artifact (wrong tube, order of draw, IV contamination, carryover, drift)",
               "3 real change (treatment, transfusion, clinical course, timing) - with clinical context per SOP"]


def num(x):
    return None if x in (None, "") else float(x)


def decide(flagged, in_ref):
    """Card Fork 2: a fired delta is HOLD whatever the reference range says."""
    return "HOLD - investigate before release" if flagged else "delta OK - continue the other release checks"


def delta(prev, cur, abs_limit=None, pct_limit=None, ref_low=None, ref_high=None, analyte=""):
    if abs_limit is None and pct_limit is None:
        raise ValueError("delta limits are lab-specific: give abs_limit and/or pct_limit for %s" % (analyte or "the analyte"))
    d_abs = cur - prev
    d_pct = None if prev == 0 else d_abs / prev * 100.0
    reasons = []
    if abs_limit is not None and abs(d_abs) > abs_limit:
        reasons.append("|delta| %.4g > abs limit %.4g" % (abs(d_abs), abs_limit))
    if pct_limit is not None:
        if d_pct is None:
            reasons.append("previous value is 0 -> percent delta undefined; use an absolute limit")
        elif abs(d_pct) > pct_limit:
            reasons.append("|delta%%| %.1f > pct limit %.4g" % (abs(d_pct), pct_limit))
    flagged = bool(reasons)
    in_ref = None
    if ref_low is not None and ref_high is not None:
        in_ref = ref_low <= cur <= ref_high
    return {"analyte": analyte, "prev": prev, "cur": cur, "delta_abs": d_abs, "delta_pct": d_pct,
            "abs_limit": abs_limit, "pct_limit": pct_limit, "flagged": flagged, "reasons": reasons,
            "current_in_ref_range": in_ref, "decision": decide(flagged, in_ref),
            "investigate": INVESTIGATE if flagged else []}


def panel(rows):
    res = [delta(num(r["prev"]), num(r["cur"]), num(r.get("abs_limit")), num(r.get("pct_limit")),
                 num(r.get("ref_low")), num(r.get("ref_high")), r.get("analyte", "")) for r in rows]
    k = sum(r["flagged"] for r in res)
    note = ""
    if k >= 2:
        note = ("%d of %d analytes shifted together -> raises suspicion of specimen mix-up (card Fork 2); "
                "not proof - some conditions move many analytes" % (k, len(res)))
    return {"results": res, "flagged": k, "n": len(res), "panel_note": note,
            "decision": "HOLD - investigate before release" if k else "delta OK for all analytes"}


def show(r):
    pct = "n/a" if r["delta_pct"] is None else "%+.1f%%" % r["delta_pct"]
    print("%-10s prev=%-8g cur=%-8g delta=%+-9.4g delta%%=%-8s %s" % (
        r["analyte"] or "-", r["prev"], r["cur"], r["delta_abs"], pct, "FLAG" if r["flagged"] else "ok"))
    for why in r["reasons"]:
        print("%12s %s" % ("", why))
    if r["flagged"] and r["current_in_ref_range"]:
        print("%12s current value is inside the reference range - that does NOT clear the flag "
              "(plausible != right patient)" % "")


def main(argv=None):
    try:  # never crash a non-UTF-8 console (e.g. Thai cp874) on the section sign / Thai text
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prev", type=float)
    ap.add_argument("--cur", type=float)
    ap.add_argument("--abs-limit", type=float, help="lab delta limit, absolute units")
    ap.add_argument("--pct-limit", type=float, help="lab delta limit, percent of the previous value")
    ap.add_argument("--ref-low", type=float)
    ap.add_argument("--ref-high", type=float)
    ap.add_argument("--analyte", default="")
    ap.add_argument("--panel", help="CSV: analyte,prev,cur,abs_limit,pct_limit[,ref_low,ref_high]")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.panel:
            with open(a.panel, encoding="utf-8-sig", newline="") as f:
                res = panel([{k.strip().lower(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(ln for ln in f if not ln.lstrip().startswith("#"))])
            items = res["results"]
        else:
            if a.prev is None or a.cur is None:
                ap.error("give --prev and --cur, or --panel")
            res = delta(a.prev, a.cur, a.abs_limit, a.pct_limit, a.ref_low, a.ref_high, a.analyte)
            items = [res]
    except ValueError as e:
        sys.exit(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("formula: delta = cur - prev ; delta% = (cur - prev) / prev x 100 ; limits = lab SOP")
    for r in items:
        show(r)
    print("-" * 70)
    if res.get("panel_note"):
        print("PANEL: " + res["panel_note"])
    print("DECISION: " + res["decision"])
    if any(r["flagged"] for r in items):
        print("INVESTIGATE (in this order):")
        for step in INVESTIGATE:
            print("  " + step)
    print("ADVISORY: decision support only - follow the lab delta-check SOP; confirm with an authorised MT.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
