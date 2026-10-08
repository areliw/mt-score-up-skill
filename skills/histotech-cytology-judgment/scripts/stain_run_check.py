#!/usr/bin/env python3
"""stain_run_check - is each IHC / special-stain result releasable, given its controls?

Black-box tool for histotech-cytology-judgment Fork 5. Run --help, not the source.
ADVISORY ONLY: it checks control validity; reading the stain and the diagnosis belong to the pathologist.

Rules (card Fork 5 and its anti-pattern "IHC/special-stain control fail then report negative"):
  - controls are judged per RUN + MARKER: a failed control invalidates THAT marker only, not the other
    antibodies/stains in the same run
  - positive control must stain (pos). Not stained -> every patient result for that marker is INVALID:
    a patient "negative" there is NOT a true negative -> re-stain
  - negative reagent control (if run) must not stain (neg). Stained -> INVALID (non-specific staining)
  - no positive control for a marker -> INVALID (cannot be verified)
  - negative reagent control is required only by lab policy / CAP / validated protocol:
    pass --require-neg-control to enforce it (card: "not every set-up")
  - internal control (on the patient's own slide, e.g. normal ducts for ER) must stain; not stained ->
    that SLIDE's result is INVALID
  - control read as "weak" -> HOLD for review per SOP (the card does not set a rule for weak controls)
Same principle as "control line absent = invalid, not negative" (immunodiagnostic digest §4 / trap 9) and
"no ACTB control band = invalid" (503402 digest §4B).

Input CSV (header required): run,marker,slide,role,result
  role   = patient | pos_control | neg_control | internal_control
  result = pos | neg | weak | equivocal      Example: data/ihc_run_example.csv

Examples
  python stain_run_check.py data/ihc_run_example.csv
  python stain_run_check.py data/ihc_run_example.csv --require-neg-control --json
"""
import argparse
import csv
import json
import sys

ROLES = {"patient", "pos_control", "neg_control", "internal_control"}
RESULTS = {"pos": "pos", "positive": "pos", "+": "pos", "neg": "neg", "negative": "neg", "-": "neg",
           "weak": "weak", "equivocal": "equivocal"}
EXPECT = {"pos_control": "pos", "neg_control": "neg", "internal_control": "pos"}
ADVISORY = ("ADVISORY: decision support only - the pathologist reads and signs out; re-stain / release "
            "follows the lab SOP and validated protocol.")


def parse(rows):
    out = []
    for i, r in enumerate(rows):
        r = {(k or "").strip().lower(): (v or "").strip() for k, v in r.items()}
        role = r.get("role", "").lower()
        res = RESULTS.get(r.get("result", "").lower())
        if role not in ROLES:
            raise ValueError("row %d: role %r not in %s" % (i + 2, r.get("role"), sorted(ROLES)))
        if res is None:
            raise ValueError("row %d: result %r not one of pos/neg/weak/equivocal" % (i + 2, r.get("result")))
        if not r.get("marker"):
            raise ValueError("row %d: empty marker" % (i + 2))
        out.append({"run": r.get("run", ""), "marker": r["marker"], "slide": r.get("slide", ""),
                    "role": role, "result": res})
    return out


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return parse(list(csv.DictReader(f)))


def group_key(row):
    """Controls apply within one run AND one marker (card Fork 5)."""
    return (row["run"], row["marker"])


def control_status(role, result):
    if result == EXPECT[role]:
        return "PASS"
    if result == "weak" and role in ("pos_control", "internal_control"):
        return "REVIEW"
    return "FAIL"


def evaluate(rows, require_neg_control=False):
    groups = {}
    for r in rows:
        groups.setdefault(group_key(r), []).append(r)
    decisions, summary = [], {}
    for key, grp in groups.items():
        pos = [control_status("pos_control", c["result"]) for c in grp if c["role"] == "pos_control"]
        negc = [control_status("neg_control", c["result"]) for c in grp if c["role"] == "neg_control"]
        reasons, level = [], "PASS"
        if not pos:
            reasons.append("no positive control for this marker in this run")
            level = "FAIL"
        elif "FAIL" in pos:
            reasons.append("positive control did not stain")
            level = "FAIL"
        elif "REVIEW" in pos:
            reasons.append("positive control weak - review per SOP")
            level = "REVIEW"
        if negc and "FAIL" in negc:
            reasons.append("negative reagent control stained (non-specific)")
            level = "FAIL"
        elif not negc and require_neg_control:
            reasons.append("no negative reagent control (required by --require-neg-control)")
            level = "FAIL"
        summary["/".join(k for k in key if k)] = {"control": level, "reasons": reasons}
        internal = {}
        for c in grp:
            if c["role"] == "internal_control":
                internal.setdefault(c["slide"], []).append(control_status("internal_control", c["result"]))
        for p in (x for x in grp if x["role"] == "patient"):
            why, lvl = list(reasons), level
            ic = internal.get(p["slide"], [])
            if "FAIL" in ic:
                why.append("internal control on this slide did not stain")
                lvl = "FAIL"
            elif "REVIEW" in ic and lvl == "PASS":
                why.append("internal control weak - review per SOP")
                lvl = "REVIEW"
            if lvl == "FAIL":
                decision = "INVALID - re-stain"
                if p["result"] == "neg":
                    decision += " (NOT a true negative)"
            elif lvl == "REVIEW":
                decision = "HOLD - review controls per SOP"
            else:
                decision = "VALID - %s" % p["result"]
            decisions.append({"run": p["run"], "marker": p["marker"], "slide": p["slide"], "reported": p["result"],
                              "decision": decision, "reasons": why})
    restain = {}
    for d in decisions:
        if d["decision"].startswith("INVALID"):
            restain.setdefault(d["marker"], []).append(d["slide"])
    return {"decisions": decisions, "controls": summary, "restain": restain}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--require-neg-control", action="store_true", help="lab policy: negative reagent control mandatory")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        res = evaluate(load(a.csv), a.require_neg_control)
    except ValueError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        res["advisory"] = ADVISORY
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("%-6s %-8s %-8s %-9s %s" % ("run", "marker", "slide", "reported", "decision"))
    for d in res["decisions"]:
        print("%-6s %-8s %-8s %-9s %s" % (d["run"], d["marker"], d["slide"], d["reported"], d["decision"]))
        for w in d["reasons"]:
            print("%35s - %s" % ("", w))
    print("-" * 70)
    print("RE-STAIN: %s" % ("; ".join("%s %s" % (m, ", ".join(s)) for m, s in sorted(res["restain"].items()))
                              or "none"))
    print("(other markers in the same run are unaffected - card Fork 5)")
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
