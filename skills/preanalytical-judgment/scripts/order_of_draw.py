#!/usr/bin/env python3
"""order_of_draw — check a list of tubes (in the order they were / will be drawn) against the
order of draw, and optionally check which test was put in which tube.

Black-box tool for preanalytical-judgment. Run --help first; read the source only if a check fails.
Sources (rules are copied from these, nothing else):
  - preanalytical-judgment card Fork 1 (order + why: EDTA carryover -> K up, Ca/Mg/ALP down falsely;
    heparin -> coag invalid; winged set -> discard tube before citrate) and Fork 2 (coag = citrate,
    CBC = EDTA, glucose/lactate = fluoride; glucose falls if not fluoride / not separated)
  - 510403 Clinical Laboratory Practice digest §2.8 (order table: culture -> citrate(blue) ->
    clot activator(red) -> Li-heparin(green) -> K2EDTA(lavender) -> NaF/K-oxalate(gray);
    EDTA = CBC/Hb typing/HbA1c/flow/PCR; gray = glucose/alcohol)
  - 505402 Clinical Chemistry Lab digest §5.4/§7 (no fluoride tube for urease BUN)
  - clinical-correlation-judgment card Fork 4 + 510416 Case 11 (heparin tube must not go to RT-PCR)
ADVISORY ONLY: the lab's own collection SOP wins over this script.

Tubes (aliases, case-insensitive; Thai colour words accepted):
  culture  (blood-culture, bc, bottle)          citrate  (blue, light-blue, ฟ้า)
  serum    (red, sst, gold, yellow, clot, แดง, เหลือง) heparin  (green, li-heparin, เขียว)
  edta     (lavender, purple, ม่วง)             fluoride (naf, gray, grey, เทา)
  discard  (plain discard tube, no additive)

Optional test placement: write tube:test+test, e.g.  citrate:PT+aPTT  edta:CBC  serum:K+Na  gray:glucose

Examples
  python order_of_draw.py culture citrate serum heparin edta fluoride
  python order_of_draw.py serum edta citrate --winged
  python order_of_draw.py citrate:PT serum:K+Na edta:CBC gray:glucose
  python order_of_draw.py --file ../data/tubes_example.txt --json
"""
import argparse
import json
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ALIASES = {
    "culture": "culture", "blood-culture": "culture", "bc": "culture", "bottle": "culture",
    "citrate": "citrate", "blue": "citrate", "light-blue": "citrate", "ฟ้า": "citrate",
    "serum": "serum", "red": "serum", "sst": "serum", "gold": "serum", "yellow": "serum",
    "clot": "serum", "แดง": "serum", "เหลือง": "serum",
    "heparin": "heparin", "green": "heparin", "li-heparin": "heparin", "เขียว": "heparin",
    "edta": "edta", "lavender": "edta", "purple": "edta", "ม่วง": "edta",
    "fluoride": "fluoride", "naf": "fluoride", "gray": "fluoride", "grey": "fluoride", "เทา": "fluoride",
    "discard": "discard",
}
# card Fork 1 + 510403 §2.8. discard has no additive -> no rank (allowed anywhere).
RANK = {"culture": 1, "citrate": 2, "serum": 3, "heparin": 4, "edta": 5, "fluoride": 6}
ADDITIVE = {"culture": "broth", "citrate": "sodium citrate", "serum": "clot activator / gel",
            "heparin": "lithium heparin", "edta": "K2EDTA", "fluoride": "NaF / K-oxalate",
            "discard": "none"}
# consequences stated in the sources; any other inversion is reported generically.
CARRYOVER = {
    ("edta", "serum"): "EDTA carryover -> K up, Ca/Mg down, ALP down FALSELY (card Fork 1)",
    ("edta", "heparin"): "EDTA carryover -> K up, Ca/Mg down, ALP down FALSELY (card Fork 1)",
    ("heparin", "citrate"): "heparin carryover -> coag results invalid (card Fork 1)",
}

TEST_ALIASES = {
    "pt": "coag", "aptt": "coag", "ptt": "coag", "tt": "coag", "inr": "coag", "coag": "coag",
    "cbc": "edta_test", "hba1c": "edta_test", "hb-typing": "edta_test", "hbtyping": "edta_test",
    "flow": "edta_test",
    "glucose": "glycolysis", "lactate": "glycolysis",
    "k": "cation", "ca": "cation", "mg": "cation", "alp": "cation",
    "bun": "urease", "urea": "urease",
    "pcr": "pcr", "rt-pcr": "pcr",
}


def norm_tube(name):
    key = name.strip().lower()
    if key not in ALIASES:
        raise ValueError("unknown tube %r - use one of: %s" % (name, ", ".join(sorted(set(ALIASES.values())))))
    return ALIASES[key]


def parse(items):
    """items like 'edta' or 'edta:CBC+HbA1c' -> list of (tube, [tests])."""
    out = []
    for it in items:
        tube, _, tests = it.partition(":")
        out.append((norm_tube(tube), [t.strip() for t in tests.split("+") if t.strip()]))
    return out


def test_rules(tube, test):
    """Return (status, message) for one test in one tube. status in OK / FAIL / WARN / NO-RULE."""
    kind = TEST_ALIASES.get(test.strip().lower())
    if kind is None:
        return "NO-RULE", "no rule for %r in this script - not checked (check your SOP)" % test
    if kind == "coag":
        return ("OK", "coag in citrate") if tube == "citrate" else (
            "FAIL", "%s must be drawn in citrate (card Fork 2; 510403 §2.8)" % test)
    if kind == "edta_test":
        return ("OK", "EDTA test in EDTA") if tube == "edta" else (
            "FAIL", "%s belongs in EDTA (card Fork 2; 510403 §2.8)" % test)
    if kind == "glycolysis":
        return ("OK", "fluoride inhibits glycolysis") if tube == "fluoride" else (
            "WARN", "%s not in fluoride -> falls with time unless separated fast (card Fork 2)" % test)
    if kind == "cation":
        return ("FAIL", "%s from an EDTA tube is falsely changed (card Fork 1)" % test) if tube == "edta" else (
            "OK", "not an EDTA tube")
    if kind == "urease":
        return ("FAIL", "no fluoride tube for urease BUN (505402 §5.4/§7)") if tube == "fluoride" else (
            "OK", "not a fluoride tube")
    if kind == "pcr":
        return ("FAIL", "heparin tube must not go to (RT-)PCR (clinical-correlation Fork 4)") if tube == "heparin" else (
            "OK", "not a heparin tube")
    return "NO-RULE", "not checked"


def check(entries, winged=False):
    rows, violations, test_findings = [], [], []
    ranked = [(i, t) for i, (t, _) in enumerate(entries) if t in RANK]
    for i, (tube, tests) in enumerate(entries):
        rows.append({"pos": i + 1, "tube": tube, "additive": ADDITIVE[tube], "rank": RANK.get(tube), "tests": tests})
    for a in range(len(ranked)):
        for b in range(a + 1, len(ranked)):
            ia, ta = ranked[a]
            ib, tb = ranked[b]
            if RANK[ta] > RANK[tb]:
                why = CARRYOVER.get((ta, tb), "%s additive can carry over into the %s tube (order rule, "
                                              "card Fork 1 / 510403 §2.8)" % (ADDITIVE[ta], tb))
                violations.append({"earlier": ia + 1, "earlier_tube": ta, "later": ib + 1, "later_tube": tb,
                                   "why": why})
    first_additive = next((t for t, _ in entries if t != "discard"), None)
    discard_before = bool(entries) and entries[0][0] == "discard"
    if winged and first_additive == "citrate" and not discard_before:
        violations.append({"earlier": None, "earlier_tube": None, "later": 1, "later_tube": "citrate",
                           "why": "winged set + citrate first -> draw a discard tube first (air in tubing -> "
                                  "underfill -> PT/aPTT falsely long) (card Fork 1/2)"})
    for i, (tube, tests) in enumerate(entries):
        for t in tests:
            status, msg = test_rules(tube, t)
            test_findings.append({"pos": i + 1, "tube": tube, "test": t, "status": status, "msg": msg})
    fails = [f for f in test_findings if f["status"] == "FAIL"]
    verdict = "FIX ORDER/TUBES" if (violations or fails) else "OK"
    return {"tubes": rows, "order_violations": violations, "test_checks": test_findings, "verdict": verdict,
            "expected_order": sorted(RANK, key=RANK.get)}


def main(argv=None):
    try:  # never crash a non-UTF-8 console (e.g. Thai cp874) on the section sign / Thai text
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tubes", nargs="*", help="tubes in draw order, optionally tube:test+test")
    ap.add_argument("--file", help="text file: one tube (or tube:tests) per line; # comments allowed")
    ap.add_argument("--winged", action="store_true", help="winged (butterfly) set used")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    items = list(a.tubes)
    if a.file:
        with open(a.file, encoding="utf-8") as f:
            items += [ln.split("#")[0].strip() for ln in f if ln.split("#")[0].strip()]
    if not items:
        ap.error("give tubes on the command line or with --file")
    try:
        res = check(parse(items), winged=a.winged)
    except ValueError as e:
        sys.exit(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("expected order: " + " -> ".join(res["expected_order"]) + "   (discard tube: no additive, allowed)")
    print("%-4s %-9s %-22s %-5s %s" % ("pos", "tube", "additive", "rank", "tests"))
    for r in res["tubes"]:
        print("%-4s %-9s %-22s %-5s %s" % (r["pos"], r["tube"], r["additive"], r["rank"] or "-", "+".join(r["tests"])))
    print("-" * 70)
    if res["order_violations"]:
        for v in res["order_violations"]:
            if v["earlier"]:
                print("ORDER  #%s %s drawn before #%s %s: %s" % (v["earlier"], v["earlier_tube"], v["later"],
                                                               v["later_tube"], v["why"]))
            else:
                print("ORDER  %s" % v["why"])
    else:
        print("ORDER  no inversions")
    for t in res["test_checks"]:
        print("%-6s #%s %s in %s: %s" % (t["status"], t["pos"], t["test"], t["tube"], t["msg"]))
    print("VERDICT: %s" % res["verdict"])
    print("ADVISORY: decision support only - follow the lab collection SOP; confirm with the responsible MT.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
