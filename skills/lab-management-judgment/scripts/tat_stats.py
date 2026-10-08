#!/usr/bin/env python3
"""tat_stats — turnaround time (TAT) as a KPI: median and percentiles from timestamps, % within the lab's
target, split by priority (STAT / routine), with the measured interval stated and bad rows counted.

Black-box tool for lab-management-judgment. Run --help first; read the source only if a number looks wrong.
Sources:
  - lab-management-judgment card Fork 8 (TAT = the KPI wards/doctors press hardest; STAT pathway) and
    Fork 4 (post-analytical errors include late reports / TAT over target)
  - RESEARCH-METHOD digest §5.1 (skewed data -> report median + IQR / percentiles, not mean +/- SD)
TAT is right-skewed (a few very late tests) -> the KPI is a percentile ("90% reported within X min"), the
mean is printed only for contrast. Percentiles use linear interpolation between order statistics
(rank = 1 + (n-1)p, same as statistics.quantiles(method="inclusive")). The target is lab policy -> argument.
Rows with a missing / unparsable / negative interval are EXCLUDED AND COUNTED, never silently dropped.
ADVISORY ONLY: KPI definitions (which timestamps, which tests) belong to the lab.

Input CSV: one row per test with two timestamp columns (default names: received, reported; ISO format
YYYY-MM-DD HH:MM[:SS]) and optionally a priority column.

Examples
  python tat_stats.py ../data/tat_example.csv --target 60
  python tat_stats.py ../data/tat_example.csv --start collected --end reported --by priority --pct 50 90 95
"""
import argparse
import csv
import json
import math
import statistics
import sys
from datetime import datetime

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def pctile(sorted_vals, p):
    """Linear interpolation, rank = 1 + (n-1)p (p in 0..1)."""
    n = len(sorted_vals)
    if n == 1:
        return sorted_vals[0]
    r = (n - 1) * p
    lo = int(math.floor(r))
    hi = min(lo + 1, n - 1)
    return sorted_vals[lo] + (r - lo) * (sorted_vals[hi] - sorted_vals[lo])


def minutes(row, start, end):
    try:
        a = datetime.fromisoformat(row[start].strip())
        b = datetime.fromisoformat(row[end].strip())
    except (KeyError, ValueError, AttributeError):
        return None, "missing/unparsable timestamp"
    m = (b - a).total_seconds() / 60.0
    if m < 0:
        return None, "end before start (%.0f min)" % m
    return m, ""


def summarise(mins, pcts, target=None):
    s = sorted(mins)
    out = {"n": len(s)}
    if not s:
        return out
    out["percentiles"] = {"P%g" % p: pctile(s, p / 100.0) for p in pcts}
    out["median"] = pctile(s, 0.5)
    out["iqr"] = (pctile(s, 0.25), pctile(s, 0.75))
    out["mean_contrast_only"] = statistics.fmean(s)
    out["max"] = s[-1]
    if target is not None:
        within = sum(1 for m in s if m <= target)
        out["target"] = target
        out["within_target"] = within
        out["pct_within_target"] = 100.0 * within / len(s)
    return out


def analyse(rows, start="received", end="reported", by=None, pcts=(50, 90), target=None):
    good, bad = [], []
    for i, r in enumerate(rows, 1):
        m, why = minutes(r, start, end)
        if m is None:
            bad.append({"row": i, "why": why})
        else:
            good.append((r.get(by, "") if by else "all", m))
    groups = {}
    for g, m in good:
        groups.setdefault(g or "(blank)", []).append(m)
    return {"interval": "%s -> %s" % (start, end), "rows": len(rows), "excluded": bad,
            "overall": summarise([m for _, m in good], pcts, target),
            "by_group": {g: summarise(ms, pcts, target) for g, ms in sorted(groups.items())} if by else {}}


def main(argv=None):
    try:  # never crash a non-UTF-8 console (e.g. Thai cp874) on the section sign / Thai text
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--start", default="received", help="start timestamp column (default received)")
    ap.add_argument("--end", default="reported", help="end timestamp column (default reported)")
    ap.add_argument("--by", help="column to split by, e.g. priority")
    ap.add_argument("--pct", type=float, nargs="+", default=[50, 90], help="percentiles (default 50 90)")
    ap.add_argument("--target", type=float, help="lab TAT target in minutes")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        rows = [{k.strip().lower(): (v or "").strip() for k, v in r.items()}
                for r in csv.DictReader(ln for ln in f if not ln.lstrip().startswith("#"))]
    res = analyse(rows, a.start.lower(), a.end.lower(), a.by.lower() if a.by else None, a.pct, a.target)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("interval measured: %s · rows %d · excluded %d" % (res["interval"], res["rows"], len(res["excluded"])))
    for b in res["excluded"]:
        print("  excluded row %d: %s" % (b["row"], b["why"]))
    blocks = [("ALL", res["overall"])] + list(res["by_group"].items())
    for name, s in blocks:
        if not s.get("n"):
            print("%-10s n 0" % name)
            continue
        ps = "  ".join("%s %.0f" % (k, v) for k, v in s["percentiles"].items())
        line = "%-10s n %-5d median %.0f  IQR %.0f-%.0f  %s  max %.0f min" % (name, s["n"], s["median"], s["iqr"][0],
                                                                          s["iqr"][1], ps, s["max"])
        if "target" in s:
            line += "  within %g min: %.1f%% (%d/%d)" % (s["target"], s["pct_within_target"], s["within_target"], s["n"])
        print(line)
        print("%-10s mean %.0f min <- contrast only; TAT is skewed, report percentiles" % ("", s["mean_contrast_only"]))
    print("ADVISORY: decision support only - KPI definition and target are the lab's.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
