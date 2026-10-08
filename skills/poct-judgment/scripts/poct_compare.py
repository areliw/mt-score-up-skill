#!/usr/bin/env python3
"""poct_compare - periodic POCT vs central-lab comparison: per-pair difference, bias, agreement, drift.

Black-box tool for poct-judgment (Fork 3 "correlate POCT with the central lab periodically"; trap 7
"no periodic correlation -> drift goes unnoticed"). Run --help first.

Input CSV columns (header required): date, poct, lab   - one paired sample per row, time order.
Per pair:  diff = poct - lab ; pct = (poct - lab) / lab x 100   (the central lab is the comparator)
Summary:   mean diff, mean % diff, share of pairs inside YOUR acceptance limit, and drift = mean % diff of
           the later half minus the earlier half. Acceptance limits are YOUR policy (no default):
             --limit-pct P                  every pair judged by |pct| <= P
             --limit-abs A --switch-at X    |diff| <= A when lab < X, |pct| <= P when lab >= X
Matrix note (owner digest 504202-CLINCHEM-LECTURE-DIGEST section 1 + judgment fork 10): plasma glucose
runs ~12-15 % above whole blood; with a whole-blood-calibrated meter a difference of that size is matrix,
not error - do not "correct" values to match. ADVISORY ONLY.

Examples
  python poct_compare.py ../data/poct_pairs_teaching_example.csv --limit-pct 15   (teaching values)
  python poct_compare.py pairs.csv --limit-abs 15 --limit-pct 15 --switch-at 100 --json
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


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    pairs = []
    for i, r in enumerate(rows):
        r = {k.strip().lower(): (v or "").strip() for k, v in r.items()}
        lab = float(r["lab"])
        if lab <= 0:
            raise ValueError("row %d: lab value must be > 0" % (i + 2))
        pairs.append({"date": r.get("date", str(i + 1)), "poct": float(r["poct"]), "lab": lab})
    return pairs


def pair_stats(p):
    diff = p["poct"] - p["lab"]
    return dict(p, diff=diff, pct=diff / p["lab"] * 100)


def within(p, limit_pct, limit_abs=None, switch_at=None):
    if limit_abs is not None and switch_at is not None and p["lab"] < switch_at:
        return abs(p["diff"]) <= limit_abs
    return abs(p["pct"]) <= limit_pct


def compare(pairs, limit_pct, limit_abs=None, switch_at=None, drift_pct=None):
    if len(pairs) < 2:
        raise ValueError("need at least 2 pairs")
    rows = [pair_stats(p) for p in pairs]
    for r in rows:
        r["within"] = within(r, limit_pct, limit_abs, switch_at)
    n = len(rows)
    half = n // 2
    early, late = rows[:half], rows[n - half:]
    early_pct = sum(r["pct"] for r in early) / len(early)
    late_pct = sum(r["pct"] for r in late) / len(late)
    res = {"n": n, "rows": rows,
           "mean_diff": sum(r["diff"] for r in rows) / n,
           "mean_pct": sum(r["pct"] for r in rows) / n,
           "n_within": sum(r["within"] for r in rows),
           "share_within": sum(r["within"] for r in rows) / n,
           "drift": {"early_mean_pct": early_pct, "late_mean_pct": late_pct, "change_pct_points": late_pct - early_pct}}
    if drift_pct is not None:
        res["drift"]["flag"] = abs(late_pct - early_pct) > drift_pct
    res["limits"] = {"limit_pct": limit_pct, "limit_abs": limit_abs, "switch_at": switch_at}
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--limit-pct", type=float, required=True, help="your acceptance limit, percent")
    ap.add_argument("--limit-abs", type=float, help="absolute limit used below --switch-at")
    ap.add_argument("--switch-at", type=float, help="lab value below which --limit-abs applies")
    ap.add_argument("--drift-pct", type=float, help="flag if late-minus-early mean bias exceeds this (optional)")
    ap.add_argument("--meter-cal", choices=["plasma", "whole-blood"], help="meter calibration (matrix note)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if (a.limit_abs is None) != (a.switch_at is None):
        ap.error("--limit-abs and --switch-at go together")
    res = compare(load(a.csv), a.limit_pct, a.limit_abs, a.switch_at, a.drift_pct)
    if a.meter_cal == "whole-blood":
        res["matrix_note"] = ("whole-blood-calibrated meter: plasma runs ~12-15 % higher (504202 digest); "
                              "understand the matrix, do not 'correct' values")
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("%-12s %8s %8s %8s %8s %s" % ("date", "poct", "lab", "diff", "pct", "within"))
    for r in res["rows"]:
        print("%-12s %8g %8g %+8.1f %+7.1f%% %s" % (r["date"], r["poct"], r["lab"], r["diff"], r["pct"], r["within"]))
    print("-" * 60)
    print("n=%d  mean diff %+.2f  mean %%diff %+.2f%%  within limits %d/%d (%.0f%%)"
          % (res["n"], res["mean_diff"], res["mean_pct"], res["n_within"], res["n"], 100 * res["share_within"]))
    d = res["drift"]
    print("drift: early mean %+.2f%% -> late mean %+.2f%% (change %+.2f points)%s"
          % (d["early_mean_pct"], d["late_mean_pct"], d["change_pct_points"],
             ("  -> DRIFT FLAG" if d.get("flag") else "")))
    if res.get("matrix_note"):
        print("NOTE: " + res["matrix_note"])
    print("ADVISORY: decision support only - acceptance limits and actions follow your POCT policy/SOP.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
