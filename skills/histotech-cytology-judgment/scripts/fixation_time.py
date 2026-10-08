#!/usr/bin/env python3
"""fixation_time - cold-ischemia and fixation durations from timestamps, checked against YOUR limits.

Black-box tool for histotech-cytology-judgment Fork 2 ("fixation = the step you cannot redo on the same
tissue"). Run --help, not the source. ADVISORY ONLY: a breached limit is a FLAG to document and pass to
the pathologist; whether IHC/molecular is still interpretable depends on assay/marker/validation.

  cold ischemia  = time into fixative - time of collection/excision            (minutes)
  fixation time  = time out of fixative (processing start) - time into fixative (hours)
  window         = earliest / latest processing time from --min-fix-h / --max-fix-h
Real dates are used, so overnight and weekend fixation are counted correctly (the clock-only
"16:00 - 15:00 = 1 h" error hides a Friday-to-Monday 73 h fixation).

Limits are guideline/SOP/assay specific (card: verify the edition) -> NO defaults:
  --max-cold-min   longest acceptable cold ischemia, minutes
  --min-fix-h      shortest acceptable fixation, hours
  --max-fix-h      longest acceptable fixation, hours
  (example only: ASCO/CAP breast-biomarker guidance has used <= 60 min cold ischemia and 6-72 h in 10% NBF
   - verify the edition your lab follows before using these numbers)
Without limits the tool prints durations and the window only.

Input: one specimen via flags, or --csv with columns specimen,collected,into_fixative,out_of_fixative
(out_of_fixative may be empty = still in fixative -> elapsed is measured to --now). Times: YYYY-MM-DD HH:MM.

Examples
  python fixation_time.py --collected "2026-10-09 14:30" --into-fixative "2026-10-09 15:00" --out "2026-10-12 16:00" --max-cold-min 60 --min-fix-h 6 --max-fix-h 72
  python fixation_time.py --csv data/fixation_log.csv --max-cold-min 60 --min-fix-h 6 --max-fix-h 72 --now "2026-10-08 12:15"
"""
import argparse
import csv
import json
import sys
from datetime import datetime, timedelta

ADVISORY = ("ADVISORY: decision support only - document, flag to the pathologist and follow the lab SOP / "
            "guideline edition; fixation cannot be redone on the same tissue.")
ACTION = ("document + flag to the pathologist: morphology / IHC (e.g. ER/PR/HER2) / molecular MAY be "
          "uninterpretable depending on assay, marker and validation - the lab/pathologist decides repeat or "
          "new specimen (card Fork 2)")


def parse_time(s, field):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        raise ValueError("%s: cannot read time %r (use YYYY-MM-DD HH:MM)" % (field, s))


def hours_between(start, end):
    return (end - start).total_seconds() / 3600


def check(specimen, collected, into, out=None, now=None, max_cold_min=None, min_fix_h=None, max_fix_h=None):
    if collected is None or into is None:
        raise ValueError("%s: collected and into_fixative times are required" % specimen)
    if into < collected:
        raise ValueError("%s: into-fixative is BEFORE collection - check the log" % specimen)
    if out is not None and out < into:
        raise ValueError("%s: out-of-fixative is BEFORE into-fixative - check the log" % specimen)
    res = {"specimen": specimen, "cold_ischemia_min": hours_between(collected, into) * 60}
    still_in = out is None
    if still_in:
        if now is None:
            now = datetime.now().replace(second=0, microsecond=0)
        res["fixation_h"] = hours_between(into, now)
        res["fixation_status"] = "still in fixative (elapsed to %s)" % now.strftime("%Y-%m-%d %H:%M")
    else:
        res["fixation_h"] = hours_between(into, out)
        res["fixation_status"] = "completed"
    window = {}
    if min_fix_h is not None:
        window["earliest_processing"] = (into + timedelta(hours=min_fix_h)).strftime("%Y-%m-%d %H:%M")
    if max_fix_h is not None:
        window["latest_processing"] = (into + timedelta(hours=max_fix_h)).strftime("%Y-%m-%d %H:%M")
    res["window"] = window
    flags = []
    if max_cold_min is not None and res["cold_ischemia_min"] > max_cold_min:
        flags.append("COLD ISCHEMIA %.0f min > %g min" % (res["cold_ischemia_min"], max_cold_min))
    if max_fix_h is not None and res["fixation_h"] > max_fix_h:
        flags.append("OVER-FIXED %.1f h > %g h%s" % (res["fixation_h"], max_fix_h, " (still in fixative!)" if still_in else ""))
    if min_fix_h is not None and res["fixation_h"] < min_fix_h:
        if still_in:
            flags.append("NOT YET %.1f h < %g h - do not process before %s"
                         % (res["fixation_h"], min_fix_h, window["earliest_processing"]))
        else:
            flags.append("UNDER-FIXED %.1f h < %g h" % (res["fixation_h"], min_fix_h))
    res["flags"] = flags
    limits_set = any(x is not None for x in (max_cold_min, min_fix_h, max_fix_h))
    if not limits_set:
        res["verdict"] = "NO LIMITS SET - durations only (pass the lab/guideline limits)"
    elif any(not f.startswith("NOT YET") for f in flags):
        res["verdict"] = "FLAG -> " + ACTION
    elif flags:
        res["verdict"] = "WAIT - keep in fixative until the earliest processing time"
    else:
        res["verdict"] = "WITHIN LIMITS"
    return res


def load_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        r = {(k or "").strip().lower(): (v or "").strip() for k, v in r.items()}
        sp = r.get("specimen") or "?"
        out.append((sp, parse_time(r.get("collected"), sp + " collected"),
                    parse_time(r.get("into_fixative"), sp + " into_fixative"),
                    parse_time(r.get("out_of_fixative"), sp + " out_of_fixative")))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", help="batch log: specimen,collected,into_fixative,out_of_fixative")
    ap.add_argument("--specimen", default="specimen")
    ap.add_argument("--collected", help="collection / excision time")
    ap.add_argument("--into-fixative", help="time the tissue went into fixative")
    ap.add_argument("--out", help="time out of fixative / processing start (omit if still in fixative)")
    ap.add_argument("--now", help="reference time for specimens still in fixative (default: now)")
    ap.add_argument("--max-cold-min", type=float, help="lab/guideline limit, minutes")
    ap.add_argument("--min-fix-h", type=float, help="lab/guideline limit, hours")
    ap.add_argument("--max-fix-h", type=float, help="lab/guideline limit, hours")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        now = parse_time(a.now, "--now") if a.now else None
        if a.csv:
            specs = load_csv(a.csv)
        else:
            specs = [(a.specimen, parse_time(a.collected, "--collected"),
                      parse_time(a.into_fixative, "--into-fixative"), parse_time(a.out, "--out"))]
        results = [check(sp, c, i, o, now, a.max_cold_min, a.min_fix_h, a.max_fix_h) for sp, c, i, o in specs]
    except ValueError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps({"results": results, "advisory": ADVISORY}, ensure_ascii=False, indent=1))
        return 0
    lim = lambda v: "not set" if v is None else "%g" % v  # noqa: E731
    print("limits: cold <= %s min | fixation %s to %s h" % (lim(a.max_cold_min), lim(a.min_fix_h), lim(a.max_fix_h)))
    print("%-10s %10s %10s  %-36s %s" % ("specimen", "cold(min)", "fix(h)", "processing window", "verdict"))
    for r in results:
        w = r["window"]
        win = "%s .. %s" % (w.get("earliest_processing", "?"), w.get("latest_processing", "?")) if w else "-"
        print("%-10s %10.0f %10.1f  %-36s %s" % (r["specimen"], r["cold_ischemia_min"], r["fixation_h"], win,
                                                  r["verdict"].split(" -> ")[0]))
        for f in r["flags"]:
            print("%12s %s" % ("", f))
    if any(r["verdict"].startswith("FLAG") for r in results):
        print("FLAG action: " + ACTION)
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
