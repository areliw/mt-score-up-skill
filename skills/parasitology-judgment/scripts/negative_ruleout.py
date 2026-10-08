#!/usr/bin/env python3
"""negative_ruleout - may a series of NEGATIVE films/stools be reported as "not found / ruled out"?

Black-box tool for parasitology-judgment. Run --help first; read the source only if a result looks
wrong. It encodes the card's rule #1: one negative stool or film does not rule the disease out.
How many repeats, how far apart and how many fields are SOP numbers -> they come from a rules JSON
(data/ruleout_rules_teaching.json = teaching values from the card + 317331 digest). ADVISORY ONLY.

Logic
  malaria  films given as TIME:FIELDS (ISO time, thick-film fields read). A film read on fewer than
           min_thick_fields fields is not a valid negative (card FORK 3: >= 100 thick fields).
           Valid films are chained in time order; a film counts as a new repeat only if it is at
           least min_interval_h after the last counted one (3 films drawn together = 1 repeat).
           Gaps longer than max_interval_h are flagged. Need >= min_films counted.
           Sources: card rule #1 + FORK 3 ("repeat every 12-24 h x >= 3"); 317331 digest Lab Dx.
  stool    specimen dates (YYYY-MM-DD) for a target in the rules file (stool_routine,
           stool_ruleout, e_histolytica). Chained with min_gap_days when the source gives one;
           when it does not (null) spacing is NOT checked and the tool says so.
           Sources: card rule #1; 317331 digest §5.1 ("routine = 1, confirm = 3 alternate days,
           E. histolytica = 6").

Examples (run from the skill folder)
  python scripts/negative_ruleout.py malaria --rules data/ruleout_rules_teaching.json --film 2026-10-01T08:00:100 --film 2026-10-01T20:30:100 --film 2026-10-02T09:00:120
  python scripts/negative_ruleout.py stool --rules data/ruleout_rules_teaching.json --target stool_ruleout --specimen 2026-10-01 --specimen 2026-10-03 --specimen 2026-10-05
"""
import argparse
import datetime as dt
import json
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ADVISORY = ("ADVISORY: decision support only - the negative report follows the lab SOP, the clinical picture "
            "and the responsible MT/physician.")


def parse_film(spec):
    t, f = spec.rsplit(":", 1)
    return {"time": dt.datetime.fromisoformat(t), "fields": float(f)}


def chain(items, key, min_gap):
    """Greedy: count an item only if it is >= min_gap after the last counted item."""
    counted, skipped = [], []
    for it in sorted(items, key=key):
        if not counted or key(it) - key(counted[-1]) >= min_gap:
            counted.append(it)
        else:
            skipped.append(it)
    return counted, skipped


def malaria(films, rule):
    min_f, min_n = rule["min_thick_fields"], rule["min_films"]
    lo, hi = dt.timedelta(hours=rule["min_interval_h"]), dt.timedelta(hours=rule["max_interval_h"])
    short = [f for f in films if f["fields"] < min_f]
    valid = [f for f in films if f["fields"] >= min_f]
    counted, too_close = chain(valid, lambda f: f["time"], lo)
    flags = ["film %s read on %g fields < %g -> not a valid negative film" % (f["time"].isoformat(" "), f["fields"], min_f)
             for f in short]
    for f in too_close:
        prev = max(c["time"] for c in counted if c["time"] <= f["time"])
        flags.append("film %s only %.1f h after %s (< %g h) -> not an independent repeat"
                     % (f["time"].isoformat(" "), (f["time"] - prev).total_seconds() / 3600, prev.isoformat(" "),
                        rule["min_interval_h"]))
    for a, b in zip(counted, counted[1:]):
        if b["time"] - a["time"] > hi:
            flags.append("gap %.1f h between %s and %s > %g h (repeat was late)"
                         % ((b["time"] - a["time"]).total_seconds() / 3600, a["time"].isoformat(" "),
                            b["time"].isoformat(" "), rule["max_interval_h"]))
    ok = len(counted) >= min_n
    nxt = None if ok or not counted else (counted[-1]["time"] + lo)
    return {"counted": len(counted), "needed": min_n, "ruled_out_by_rule": ok, "flags": flags,
            "next_due": nxt.isoformat(" ") if nxt else None}


def stool(dates, rule):
    min_n, gap = rule["min_specimens"], rule.get("min_gap_days")
    flags = []
    if gap is None:
        counted, skipped = sorted(dates), []
        if min_n > 1:
            flags.append("source gives no spacing for this target -> spacing NOT checked; follow your SOP")
    else:
        counted, skipped = chain(dates, lambda d: d, dt.timedelta(days=gap))
        for d in skipped:
            flags.append("specimen %s is < %g day(s) after the previous counted one -> not counted" % (d, gap))
    ok = len(counted) >= min_n
    nxt = None
    if not ok:
        if not counted:
            nxt = "now"
        elif gap is None:
            nxt = "per SOP (source gives no spacing)"
        else:
            nxt = (counted[-1] + dt.timedelta(days=gap)).isoformat()
    return {"counted": len(counted), "needed": min_n, "ruled_out_by_rule": ok, "flags": flags, "next_due": nxt}


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("malaria")
    p.add_argument("--rules", required=True)
    p.add_argument("--film", action="append", required=True, help="ISO_TIME:FIELDS_READ, e.g. 2026-10-01T08:00:100")
    p = sub.add_parser("stool")
    p.add_argument("--rules", required=True)
    p.add_argument("--target", required=True, help="key in the rules file, e.g. stool_ruleout / e_histolytica")
    p.add_argument("--specimen", action="append", required=True, help="collection date YYYY-MM-DD")
    for _sp in sub.choices.values():  # also accept --json after the subcommand, as the examples show
        _sp.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="print JSON")
    a = ap.parse_args(argv)
    with open(a.rules, encoding="utf-8") as f:
        rules = json.load(f)
    if a.cmd == "malaria":
        rule = rules["malaria"]
        res = malaria([parse_film(s) for s in a.film], rule)
    else:
        if a.target not in rules:
            raise SystemExit("target %r not in %s" % (a.target, a.rules))
        rule = rules[a.target]
        res = stool([dt.date.fromisoformat(s) for s in a.specimen], rule)
    res["rule"] = {k: v for k, v in rule.items() if not k.startswith("_")}
    res["rule_src"] = rule.get("_src", "")
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("rule: %s" % res["rule"])
    print("rule source: %s" % res["rule_src"])
    print("valid repeats counted: %d of %d needed" % (res["counted"], res["needed"]))
    for f in res["flags"]:
        print("FLAG: " + f)
    if res["ruled_out_by_rule"]:
        print("-> SERIES MEETS THE RULE: a 'not found' report is allowed by the rule (still correlate clinically)")
    else:
        print("-> NOT RULED OUT: report only 'not found in this specimen'; next repeat due %s" % res["next_due"])
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
