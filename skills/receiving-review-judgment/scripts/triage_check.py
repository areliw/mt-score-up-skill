#!/usr/bin/env python3
"""triage_check — check a review-comment triage table against the card's rules before you reply:
every comment has a verdict and a reason, push-backs carry an alternative, deferrals are logged,
automated flags are verified before they are applied, and correctness/security/legal/ethics comments are
never dropped or committed-to silently.

Black-box tool for receiving-review-judgment. Run --help first; read the source only if a check fails.
Every rule is from the receiving-review-judgment card:
  rule #1   correctness/security first; style/taste is judgment
  trap #1   applying literally without the intent -> TAKE rows should record the root/intent (warning)
  Fork 1    verdicts TAKE / PUSH-BACK / DROP-or-DEFER (+ disagree-and-commit); push-back = reason + alternative;
            worth-doing-later = log it; disagree-and-commit is for TASTE only - correctness/security/legal/ethics
            must be escalated or the risk written down, never committed to silently
  Fork 2    push-back everything = reviewers stop reviewing (warning when every comment is pushed back/dropped)
  Fork 3    several comments with the same root = a pattern -> consider one structural fix (note)
  Fork 4    automated (codex/linter/CI) flags: verify before applying; high-severity flags are checked first
  traps     caved (take everything incl. taste) · ego (push back everything) · un-logged drops
This checks the triage record, not whether the code/paper change is right.

CSV header: id,source,category,verdict,reason,root_intent,alternative,verified,owner,log_ref,escalated
  source: human|automated · category: correctness|security|legal|ethics|style|taste|scope|clarity|other
  verdict: TAKE|PUSH-BACK|DROP|DEFER|COMMIT (COMMIT = disagree-and-commit) · verified: Y|N

Examples
  python triage_check.py ../data/triage_example.csv
  python triage_check.py ../data/triage_example.csv --json
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

VERDICTS = {"TAKE", "PUSH-BACK", "DROP", "DEFER", "COMMIT"}
HIGH_STAKES = {"correctness", "security", "legal", "ethics"}
TASTE = {"style", "taste"}


def yes(x):
    return (x or "").strip().upper() in ("Y", "YES", "TRUE", "1")


def check_row(r):
    v = (r.get("verdict") or "").strip().upper()
    cat = (r.get("category") or "").strip().lower()
    auto = (r.get("source") or "").strip().lower() == "automated"
    fails, warns = [], []
    if v not in VERDICTS:
        fails.append("verdict %r not one of %s" % (r.get("verdict"), "/".join(sorted(VERDICTS))))
    if not r.get("reason"):
        fails.append("no reason (every verdict needs one)")
    if v == "PUSH-BACK" and not r.get("alternative"):
        fails.append("push-back without an alternative (Fork 1/2: reason + alternative)")
    if v == "DEFER" and not r.get("log_ref"):
        fails.append("deferred but not logged (issue/TODO ref)")
    if cat in HIGH_STAKES and v in ("DROP", "DEFER", "COMMIT") and not r.get("escalated"):
        fails.append("%s comment %s without escalation / written risk (Fork 1)" % (cat, v.lower()))
    if v == "COMMIT" and cat not in TASTE and cat not in HIGH_STAKES:
        warns.append("disagree-and-commit is meant for taste; category is %r" % cat)
    if v == "COMMIT" and not r.get("owner"):
        fails.append("disagree-and-commit needs the decision owner named")
    if auto and v == "TAKE" and not yes(r.get("verified")):
        fails.append("automated flag applied without verification (Fork 4)")
    if auto and cat in HIGH_STAKES and not yes(r.get("verified")):
        fails.append("high-severity automated flag not verified yet - check it first (Fork 4)")
    if v == "TAKE" and not r.get("root_intent"):
        warns.append("TAKE without the reviewer's intent/root -> risk of a literal fix (trap #1)")
    if not cat:
        warns.append("no category -> cannot weigh correctness vs taste (rule #1)")
    return {"id": r.get("id"), "verdict": v, "category": cat, "fails": fails, "warns": warns,
            "status": "FAIL" if fails else ("WARN" if warns else "PASS")}


def check(rows):
    res = [check_row(r) for r in rows]
    notes = []
    vs = [x["verdict"] for x in res]
    if res and all(v == "TAKE" for v in vs) and any(x["category"] in TASTE for x in res):
        notes.append("every comment taken, including style/taste ones -> caved? (card trap: caved)")
    if res and all(v in ("PUSH-BACK", "DROP") for v in vs):
        notes.append("every comment pushed back or dropped -> ego? reviewers stop reviewing (Fork 2)")
    roots = {}
    for r in rows:
        key = (r.get("root_intent") or "").strip().lower()
        if key:
            roots.setdefault(key, []).append(r.get("id"))
    for key, ids in roots.items():
        if len(ids) >= 2:
            notes.append("pattern: comments %s share the root '%s' -> consider one structural fix, only if it is "
                         "truly one root (Fork 3)" % (", ".join(ids), key))
    return {"rows": res, "notes": notes, "done": bool(res) and all(x["status"] != "FAIL" for x in res),
            "counts": {v: vs.count(v) for v in sorted(set(vs))}}


def main(argv=None):
    try:  # never crash a non-UTF-8 console (e.g. Thai cp874) on the section sign / Thai text
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        rows = [{k.strip().lower(): (v or "").strip() for k, v in r.items()}
                for r in csv.DictReader(ln for ln in f if not ln.lstrip().startswith("#"))]
    res = check(rows)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("%-5s %-10s %-12s %-6s %s" % ("id", "verdict", "category", "status", "detail"))
    for x in res["rows"]:
        detail = "; ".join(x["fails"] + ["(warn) " + w for w in x["warns"]]) or "-"
        print("%-5s %-10s %-12s %-6s %s" % (x["id"], x["verdict"], x["category"], x["status"], detail))
    print("-" * 70)
    print("counts: " + ", ".join("%s %d" % kv for kv in res["counts"].items()))
    for n in res["notes"]:
        print("NOTE: " + n)
    print("DEFINITION OF DONE: %s" % ("MET (no FAIL rows)" if res["done"] else "NOT MET - fix the FAIL rows"))
    print("ADVISORY: checks the triage record only - the decision owner makes the final call.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
