#!/usr/bin/env python3
"""lights_criteria - exudate vs transudate by Light's criteria (pathology-judgment Fork 8).

Black-box tool: run --help, not the source. ADVISORY ONLY: the call guides work-up; diagnosis belongs to
the physician/pathologist.

Light's criteria (503402 Clinical Hematology Lab digest §8; card Fork 8). ANY ONE met = exudate:
  1. fluid protein / serum protein   > 0.5
  2. fluid LDH / serum LDH           > 0.6
  3. fluid LDH > 2/3 x the UPPER LIMIT OF NORMAL for serum LDH  (the lab's ULN -> --ldh-uln, no default)
None met = transudate - but only when all three could be evaluated; with a missing value and nothing met
the answer is INDETERMINATE, never "transudate".
Thresholds are strict ">" as written in the digest and the card.

Card Fork 8 caveats printed with the result:
  - SG / total protein are only a rough estimate -> --sg is accepted for the record but NOT used
    (the 318322 digest's "SG > 1.020" shortcut is what the card corrects)
  - Light's itself calls ~15-20% of transudates exudates -> an exudate still needs its cause found
  - exudate -> look for malignancy / infection and send cytology

Units: protein g/dL (both the same unit), LDH U/L (all three the same unit).

Examples
  python lights_criteria.py --fluid-protein 2.0 --serum-protein 7.0 --fluid-ldh 90 --serum-ldh 250 --ldh-uln 250
  python lights_criteria.py --fluid-protein 2.5 --serum-protein 7.0 --fluid-ldh 180 --serum-ldh 400 --ldh-uln 250
  python lights_criteria.py --fluid-protein 2.0 --serum-protein 7.0 --json
"""
import argparse
import json
import sys

PROTEIN_RATIO = 0.5
LDH_RATIO = 0.6
LDH_ULN_FRACTION = 2 / 3
ADVISORY = ("ADVISORY: decision support only - interpret with the clinical picture; diagnosis and further "
            "work-up are decided by the physician/pathologist per SOP.")


def _ratio(a, b):
    if a is None or b is None:
        return None
    if b <= 0:
        raise ValueError("serum value must be > 0")
    return a / b


def criteria(fluid_protein=None, serum_protein=None, fluid_ldh=None, serum_ldh=None, ldh_uln=None):
    pr = _ratio(fluid_protein, serum_protein)
    lr = _ratio(fluid_ldh, serum_ldh)
    lim = ldh_uln * LDH_ULN_FRACTION if ldh_uln is not None else None
    rows = [
        {"criterion": "fluid/serum protein > %g" % PROTEIN_RATIO, "value": pr, "threshold": PROTEIN_RATIO,
         "met": None if pr is None else pr > PROTEIN_RATIO},
        {"criterion": "fluid/serum LDH > %g" % LDH_RATIO, "value": lr, "threshold": LDH_RATIO,
         "met": None if lr is None else lr > LDH_RATIO},
        {"criterion": "fluid LDH > 2/3 x serum LDH ULN", "value": fluid_ldh, "threshold": lim,
         "met": None if (fluid_ldh is None or lim is None) else fluid_ldh > lim},
    ]
    return rows


def classify(rows):
    met = [r for r in rows if r["met"] is True]
    missing = [r for r in rows if r["met"] is None]
    if met:
        return "EXUDATE"
    if missing:
        return "INDETERMINATE"
    return "TRANSUDATE"


def evaluate(fluid_protein=None, serum_protein=None, fluid_ldh=None, serum_ldh=None, ldh_uln=None, sg=None):
    rows = criteria(fluid_protein, serum_protein, fluid_ldh, serum_ldh, ldh_uln)
    call = classify(rows)
    notes = []
    if call == "EXUDATE":
        notes.append("exudate -> look for malignancy / infection / inflammation and send cytology (card Fork 8)")
        notes.append("Light's labels ~15-20% of transudates as exudates (card Fork 8) - correlate clinically")
    elif call == "TRANSUDATE":
        notes.append("transudate -> think hydrostatic / oncotic causes (CHF, cirrhosis, nephrotic)")
    else:
        notes.append("not every criterion could be evaluated and none met -> cannot call transudate; "
                     "supply the missing values (protein pair, LDH pair, serum LDH ULN)")
    if sg is not None:
        notes.append("SG %.3f recorded but NOT used: SG/protein are a rough estimate only (card Fork 8)" % sg)
    return {"inputs": {"fluid_protein": fluid_protein, "serum_protein": serum_protein, "fluid_ldh": fluid_ldh,
                       "serum_ldh": serum_ldh, "ldh_uln": ldh_uln, "sg": sg},
            "criteria": rows, "met_count": sum(1 for r in rows if r["met"] is True),
            "call": call, "notes": notes}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fluid-protein", type=float)
    ap.add_argument("--serum-protein", type=float)
    ap.add_argument("--fluid-ldh", type=float)
    ap.add_argument("--serum-ldh", type=float)
    ap.add_argument("--ldh-uln", type=float, help="the lab's upper limit of normal for SERUM LDH (no default)")
    ap.add_argument("--sg", type=float, help="specific gravity (recorded, not used)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        res = evaluate(a.fluid_protein, a.serum_protein, a.fluid_ldh, a.serum_ldh, a.ldh_uln, a.sg)
    except ValueError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        res["advisory"] = ADVISORY
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("%-34s %10s %10s  %s" % ("criterion", "value", "threshold", "met"))
    for r in res["criteria"]:
        v = "-" if r["value"] is None else "%.3f" % r["value"]
        t = "-" if r["threshold"] is None else "%.3f" % r["threshold"]
        m = {True: "YES", False: "no", None: "n/a (missing input)"}[r["met"]]
        print("%-34s %10s %10s  %s" % (r["criterion"], v, t, m))
    print("-" * 70)
    print("CALL: %s  (%d of 3 met; any one = exudate)" % (res["call"], res["met_count"]))
    for n in res["notes"]:
        print("  - " + n)
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
