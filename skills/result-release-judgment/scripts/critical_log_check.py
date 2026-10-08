#!/usr/bin/env python3
"""critical_log_check — check a critical-value call log against the card's definition of done:
who/when/what, patient identity, read-back for verbal calls, escalation when nobody was reached, and
minutes from result to notification versus the LAB'S limit.

Black-box tool for result-release-judgment. Run --help first; read the source only if a check fails.
Requirements come from the result-release-judgment card Fork 4 (+ trap list):
  notify the responsible person IMMEDIATELY within the SOP turnaround; confirm receipt AND patient identity
  with the identifiers the SOP requires; read-back for verbal notification; log time / who called / who
  received; escalate if nobody can be reached. Repeat-before-notify is not routine and must not push the
  call past the turnaround.
The notification time limit is lab policy -> --max-minutes is required. Identifier count defaults to 2
(preanalytical-judgment card Fork 5 uses 2 identifiers; this card says "the identifiers the SOP requires")
- override with --min-ids.
ADVISORY ONLY: the log format and limits are the lab's; this checks completeness, it does not certify.

CSV header (one row per critical call):
  id1,id2,analyte,value,unit,result_time,call_time,caller,receiver,receiver_role,method,read_back,reached,
  escalated_to,escalation_time
  times: YYYY-MM-DD HH:MM ; method: verbal|electronic ; read_back/reached: Y|N

Examples
  python critical_log_check.py ../data/critical_log_example.csv --max-minutes 30
  python critical_log_check.py ../data/critical_log_example.csv --max-minutes 30 --json
"""
import argparse
import csv
import json
import statistics
import sys
from datetime import datetime

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

FMT = "%Y-%m-%d %H:%M"
REQUIRED = ("analyte", "value", "unit", "result_time", "caller")


def t(x):
    return datetime.strptime(x.strip(), FMT)


def yes(x):
    return (x or "").strip().upper() in ("Y", "YES", "TRUE", "1")


def check_row(r, max_minutes, min_ids=2):
    problems = []
    for k in REQUIRED:
        if not r.get(k):
            problems.append("missing %s" % k)
    ids = [r.get(k) for k in ("id1", "id2", "id3") if r.get(k)]
    if len(ids) < min_ids:
        problems.append("%d patient identifier(s) < %d" % (len(ids), min_ids))
    minutes = None
    reached = yes(r.get("reached")) if r.get("reached") else bool(r.get("receiver"))
    if reached:
        for k in ("receiver", "receiver_role", "call_time"):
            if not r.get(k):
                problems.append("missing %s" % k)
        if (r.get("method") or "").strip().lower() == "verbal" and not yes(r.get("read_back")):
            problems.append("verbal call without read-back")
        if not r.get("method"):
            problems.append("missing method (verbal/electronic)")
    else:
        if not r.get("escalated_to") or not r.get("escalation_time"):
            problems.append("nobody reached and no escalation recorded")
    stamp = r.get("call_time") if reached else r.get("escalation_time")
    if r.get("result_time") and stamp:
        try:
            minutes = (t(stamp) - t(r["result_time"])).total_seconds() / 60.0
        except ValueError:
            problems.append("time not in format %s" % FMT.replace("%", ""))
        else:
            if minutes < 0:
                problems.append("notification time before result time (%.0f min)" % minutes)
            elif minutes > max_minutes:
                problems.append("notified after %.0f min > %g min limit" % (minutes, max_minutes))
    return {"row": r, "minutes": minutes, "problems": problems, "status": "FAIL" if problems else "PASS"}


def check(rows, max_minutes, min_ids=2):
    res = [check_row(r, max_minutes, min_ids) for r in rows]
    mins = [x["minutes"] for x in res if x["minutes"] is not None and x["minutes"] >= 0]
    within = [m for m in mins if m <= max_minutes]
    return {"rows": res, "n": len(res), "pass": sum(x["status"] == "PASS" for x in res),
            "median_minutes": statistics.median(mins) if mins else None,
            "pct_within_limit": (100.0 * len(within) / len(mins)) if mins else None,
            "max_minutes": max_minutes, "done": all(x["status"] == "PASS" for x in res) and bool(res)}


def main(argv=None):
    try:  # never crash a non-UTF-8 console (e.g. Thai cp874) on the section sign / Thai text
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--max-minutes", type=float, required=True, help="lab limit: result -> notification")
    ap.add_argument("--min-ids", type=int, default=2, help="patient identifiers the SOP requires (default 2)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        rows = [{k.strip().lower(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(ln for ln in f if not ln.lstrip().startswith("#"))]
    res = check(rows, a.max_minutes, a.min_ids)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1, default=str))
        return 0
    print("%-4s %-10s %-10s %-8s %-6s %s" % ("#", "analyte", "value", "minutes", "status", "problems"))
    for i, x in enumerate(res["rows"], 1):
        r = x["row"]
        m = "-" if x["minutes"] is None else "%.0f" % x["minutes"]
        print("%-4s %-10s %-10s %-8s %-6s %s" % (i, r.get("analyte", ""), (r.get("value", "") + " " + r.get("unit", "")).strip(),
                                                  m, x["status"], "; ".join(x["problems"]) or "-"))
    print("-" * 70)
    med = "-" if res["median_minutes"] is None else "%.0f" % res["median_minutes"]
    pct = "-" if res["pct_within_limit"] is None else "%.0f%%" % res["pct_within_limit"]
    print("rows %d · complete %d · median %s min · within %g min: %s" % (res["n"], res["pass"], med, a.max_minutes, pct))
    print("DEFINITION OF DONE: %s" % ("MET" if res["done"] else "NOT MET - fix the FAIL rows"))
    print("ADVISORY: completeness check only - the critical-value policy and log format are the lab's.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
