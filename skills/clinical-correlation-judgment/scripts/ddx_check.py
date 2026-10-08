#!/usr/bin/env python3
"""ddx_check — check a case-correlation worksheet against the card's definition of done before anyone
"locks" an answer: the 4 iron rules, >= 3 DDx each with a test that could refute it, screens confirmed,
exclusion only after the treatable/dangerous options are ruled out with evidence, and MT-scope wording.

Black-box tool for clinical-correlation-judgment. Run --help first; read the source only if a check fails.
Every rule is from the clinical-correlation-judgment card:
  "กฎเหล็ก" 4 checks: clinical context · pre-analytical · pivotal value(s) · drug/interference
  rule #1 / trap #1 anchoring: keep >= 3 DDx + order tests that REFUTE the others, not only confirm one
  Fork 2: do not declare a diagnosis of exclusion until the treatable / more dangerous options are ruled out
  Fork 3: a positive screen is not the end -> confirm
  Fork 5: write the cause -> effect chain (recommended; missing chain is a warning)
  scope: MT does not diagnose - correlate, flag, suggest reflex tests, refer
ADVISORY ONLY: this checks the reasoning record is complete; it does not judge the medicine.

Worksheet JSON keys:
  context, preanalytical, pivotal [..], interference           (strings / list; must be non-empty)
  ddx: [{"name", "status": "open"|"leading"|"ruled-out", "discriminating_test", "evidence"}]
  screens: [{"screen", "confirm"}]                              (confirm empty -> FAIL)
  chain: "trigger -> mechanism -> lab -> sign"                  (optional -> WARN)
  conclusion: free text                                          (diagnostic wording -> WARN)

Examples
  python ddx_check.py ../data/worksheet_example.json
  python ddx_check.py ../data/worksheet_example.json --json
"""
import argparse
import json
import re
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

MIN_DDX = 3
IRON_RULES = ("context", "preanalytical", "pivotal", "interference")
DIAG_WORDS = re.compile(r"\b(diagnosed|diagnosis is|confirms? the diagnosis|definitely)\b|วินิจฉัยว่า|เป็นโรค", re.I)


def finding(level, msg):
    return {"level": level, "msg": msg}


def check(ws):
    out = []
    for k in IRON_RULES:
        v = ws.get(k)
        if not v:
            out.append(finding("FAIL", "iron rule missing: %s (card 'กฎเหล็ก' 4 checks)" % k))
    ddx = ws.get("ddx") or []
    if len(ddx) < MIN_DDX:
        out.append(finding("FAIL", "only %d DDx (< %d) -> anchoring risk (card trap #1)" % (len(ddx), MIN_DDX)))
    for d in ddx:
        name = d.get("name") or "(unnamed)"
        if not d.get("discriminating_test"):
            out.append(finding("FAIL", "DDx '%s' has no test that could refute/confirm it" % name))
        if d.get("status") == "ruled-out" and not d.get("evidence"):
            out.append(finding("FAIL", "DDx '%s' marked ruled-out without evidence" % name))
    concl = ws.get("conclusion") or ""
    if "exclusion" in concl.lower() or "ตัดออก" in concl:
        still_open = [d.get("name") for d in ddx if d.get("status") == "open"]
        if still_open:
            out.append(finding("FAIL", "diagnosis of exclusion claimed while still open: %s (card Fork 2)"
                               % ", ".join(still_open)))
    for s in ws.get("screens") or []:
        if not s.get("confirm"):
            out.append(finding("FAIL", "screen '%s' positive without a confirmatory test (card Fork 3)" % s.get("screen")))
    if not ws.get("chain"):
        out.append(finding("WARN", "no cause -> effect chain (card Fork 5)"))
    if DIAG_WORDS.search(concl):
        out.append(finding("WARN", "conclusion reads like a diagnosis - MT phrasing: 'suggests / consistent with ... "
                                   "recommend <reflex test>; refer to physician'"))
    if not concl:
        out.append(finding("WARN", "no conclusion / referral sentence"))
    fails = [f for f in out if f["level"] == "FAIL"]
    return {"findings": out, "ddx_count": len(ddx), "done": not fails,
            "verdict": "DONE (no FAIL)" if not fails else "NOT DONE: %d FAIL" % len(fails)}


def main(argv=None):
    try:  # never crash a non-UTF-8 console (e.g. Thai cp874) on the section sign / Thai text
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("worksheet_json")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    with open(a.worksheet_json, encoding="utf-8") as f:
        ws = json.load(f)
    res = check(ws)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("DDx listed: %d (min %d)" % (res["ddx_count"], MIN_DDX))
    for d in ws.get("ddx") or []:
        print("  %-28s %-10s test: %s" % (d.get("name", ""), d.get("status", "-"), d.get("discriminating_test") or "-"))
    for f in res["findings"]:
        print("%-5s %s" % (f["level"], f["msg"]))
    print("VERDICT: " + res["verdict"])
    print("ADVISORY: completeness check of the reasoning record only - diagnosis belongs to the physician.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
