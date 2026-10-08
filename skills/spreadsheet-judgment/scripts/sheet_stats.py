#!/usr/bin/env python3
"""sheet_stats - Excel/Sheets statistics with the exact Excel definitions, so you can check a workbook's numbers.

Black-box tool for spreadsheet-judgment (Fork 3: STDEV.S vs STDEV.P, median + P90/P95 for skewed TAT).
Run a subcommand first; do not read the source unless a run fails.

  stdev VALUES...                 STDEV.S (divides by n-1, a SAMPLE) and STDEV.P (divides by n, a whole POPULATION),
                                  mean, %CV and the Levey-Jennings lines mean +/- 1/2/3 SD (from STDEV.S)
  percentile --p P [--exc] VALUES...   PERCENTILE.INC (rank = P*(n-1)+1) or --exc PERCENTILE.EXC (rank = P*(n+1); #NUM! outside [1/(n+1), n/(n+1)])
  summary FILE --col COL          n, mean, median, P90, P95 (PERCENTILE.INC), min/max, STDEV.S/.P and a skew hint for a CSV column;
                                  text cells in the column are listed (Excel's AVERAGE/STDEV skip them silently)
All accept --json.

Examples
  python sheet_stats.py stdev 1345 1301 1368 1322 1310 1370 1318 1350 1303 1299
  python sheet_stats.py percentile --p 0.9 1 2 3 4 5 6 7 8 9 10
  python sheet_stats.py summary tat.csv --col tat_min
ADVISORY: check the workbook's own formula range and whether it holds a sample (STDEV.S) or a population (STDEV.P) before comparing numbers.
"""
import argparse
import csv
import json
import math
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ADVISORY = "ADVISORY: check the workbook's own formula range and whether it holds a sample (STDEV.S) or a population (STDEV.P) before comparing numbers."


def mean(xs):
    return sum(xs) / len(xs)


def stdev_s(xs):
    """Excel STDEV.S: sample SD, divides by n-1."""
    if len(xs) < 2:
        raise ValueError("STDEV.S needs at least 2 values (Excel returns #DIV/0!)")
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def stdev_p(xs):
    """Excel STDEV.P: population SD, divides by n."""
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def percentile_inc(xs, p):
    """Excel PERCENTILE.INC: linear interpolation at rank p*(n-1)+1 (p in [0,1])."""
    if not 0 <= p <= 1:
        raise ValueError("PERCENTILE.INC needs 0 <= p <= 1 (Excel #NUM!)")
    s = sorted(xs)
    r = p * (len(s) - 1)
    lo = int(math.floor(r))
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (r - lo)


def percentile_exc(xs, p):
    """Excel PERCENTILE.EXC: rank p*(n+1); undefined (#NUM!) when p < 1/(n+1) or p > n/(n+1)."""
    n = len(xs)
    if not 1 / (n + 1) <= p <= n / (n + 1):
        raise ValueError("PERCENTILE.EXC is #NUM! for p=%g with n=%d (valid %.4f..%.4f)" % (p, n, 1 / (n + 1), n / (n + 1)))
    s = sorted(xs)
    r = p * (n + 1)
    lo = int(math.floor(r))
    if lo >= n:
        return s[-1]
    return s[lo - 1] + (s[lo] - s[lo - 1]) * (r - lo)


def describe_stdev(xs):
    m, ss, sp = mean(xs), stdev_s(xs), stdev_p(xs)
    return {"n": len(xs), "mean": m, "stdev_s": ss, "stdev_p": sp, "ratio_s_over_p": ss / sp if sp else None,
            "cv_pct_s": ss / m * 100 if m else None,
            "lj_lines": {"-3SD": m - 3 * ss, "-2SD": m - 2 * ss, "-1SD": m - ss, "mean": m, "+1SD": m + ss, "+2SD": m + 2 * ss, "+3SD": m + 3 * ss},
            "note": "use STDEV.S for a run of QC values or any sample (n-1); STDEV.P only when the cells are the WHOLE population"}


def read_column(path, col):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        if col not in (rd.fieldnames or []):
            raise SystemExit("column %r not found; have %s" % (col, rd.fieldnames))
        nums, text, blank = [], [], 0
        for i, row in enumerate(rd, start=2):
            v = (row[col] or "").strip()
            if not v:
                blank += 1
                continue
            try:
                nums.append(float(v))
            except ValueError:
                text.append((i, v))
    return nums, text, blank


def summarize(nums, text=(), blank=0, gap=0.10):
    if len(nums) < 2:
        raise ValueError("need at least 2 numeric cells")
    med = percentile_inc(nums, 0.5)
    res = {"n": len(nums), "mean": mean(nums), "median": med, "p90": percentile_inc(nums, 0.90), "p95": percentile_inc(nums, 0.95),
           "min": min(nums), "max": max(nums), "stdev_s": stdev_s(nums), "stdev_p": stdev_p(nums),
           "text_cells_skipped": [{"row": r, "value": v} for r, v in text], "blank_cells": blank, "hints": []}
    if text:
        res["hints"].append("%d non-numeric cell(s) in the column (rows %s): AVERAGE/STDEV/PERCENTILE in Excel skip them silently - "
                            "numbers stored as text? clean them first" % (len(text), ", ".join(str(r) for r, _ in text[:5])))
    if med and res["mean"] > med * (1 + gap):
        res["hints"].append("mean %.2f is %.0f%% above the median %.2f (> %.0f%% gap): right-skewed - quote median and P90/P95, "
                            "not the mean (typical for turnaround time)" % (res["mean"], (res["mean"] / med - 1) * 100, med, gap * 100))
    return res


def show(res):
    for k, v in res.items():
        if k == "lj_lines":
            print("Levey-Jennings lines (STDEV.S): " + "  ".join("%s %.4f" % (a, b) for a, b in v.items()))
        elif k == "hints":
            for h in v:
                print("HINT: " + h)
        elif k == "text_cells_skipped":
            if v:
                print("text cells skipped: " + ", ".join("row %s %r" % (d["row"], d["value"]) for d in v))
        else:
            print("%-16s %s" % (k, ("%.6f" % v) if isinstance(v, float) else v))
    print(ADVISORY)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", dest="json_main")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("stdev")
    p.add_argument("values", nargs="+", type=float)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("percentile")
    p.add_argument("--p", type=float, required=True)
    p.add_argument("--exc", action="store_true", help="PERCENTILE.EXC instead of PERCENTILE.INC")
    p.add_argument("values", nargs="+", type=float)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("summary")
    p.add_argument("file")
    p.add_argument("--col", required=True)
    p.add_argument("--gap", type=float, default=0.10, help="skew hint when mean exceeds median by this fraction (screening heuristic)")
    p.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    want_json = a.json_main or a.json
    try:
        if a.cmd == "stdev":
            res = describe_stdev(a.values)
        elif a.cmd == "percentile":
            f = percentile_exc if a.exc else percentile_inc
            res = {"function": "PERCENTILE.EXC" if a.exc else "PERCENTILE.INC", "p": a.p, "n": len(a.values), "value": f(a.values, a.p)}
        else:
            nums, text, blank = read_column(a.file, a.col)
            res = summarize(nums, text, blank, a.gap)
    except ValueError as e:
        print("ERROR (Excel would show #NUM! / #DIV/0!): %s" % e)
        return 2
    if want_json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        show(res)
    return 0


if __name__ == "__main__":
    sys.exit(main())
