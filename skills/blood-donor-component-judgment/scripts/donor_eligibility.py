#!/usr/bin/env python3
"""donor_eligibility - check a donor's MEASURED values against a criteria file YOU supply.

Black-box tool for blood-donor-component-judgment. Run --help first; read the source only if needed.
Logic follows the card's Fork 1 (identity/interval -> measured Hb/Hct, BP, pulse, temperature,
weight -> questionnaire -> permanent-deferral list) and its rule that every number is a teaching
illustration: there are NO built-in limits - pass --criteria. A teaching file built from the 512303
digest §10.1 (age 17-70, first-time <=60, weight >45 kg with 350/450 mL by weight band, temp <37.5 C,
BP <160/<100, pulse 50-100, Hb F 12.5-16.5 / M 13.0-18.5 g/dL, Hct F 37-49 / M 39-55 %, interval)
is in ../data/criteria_teaching_512303_whole_blood.json - it is NOT an SOP.
Rules the tool enforces:
  * a criterion that is in the file but not measured = NOT ASSESSED -> overall INCOMPLETE, never a pass
  * Hb/Hct limits are sex-specific (needs --sex)
  * out-of-range measured value = DEFER (temporary, card Fork 1 step 2); age outside range = NOT ELIGIBLE
  * the questionnaire / risk history / medication / travel / permanent-deferral list is NOT assessed
    here - judgment + SOP (card Fork 1 steps 3-4). So the best verdict is "MEASURED CRITERIA MET",
    never "accept".
ADVISORY ONLY. Acceptance belongs to the donor-unit SOP and the responsible MT/physician.

Criteria file: JSON; each limit is {"min"|"max"|"min_exclusive"|"max_exclusive": number}.
  keys used: age_years, first_time_age_max, consent_required_below_age, weight_kg, temp_c, sbp_mmhg,
  dbp_mmhg, pulse_bpm, hb_g_dl{F,M}, hct_pct{F,M}, min_interval_days, volume_by_weight[]

Examples
  python donor_eligibility.py --criteria ../data/criteria_teaching_512303_whole_blood.json \\
      --sex F --age 22 --weight-kg 48 --hb 12.9 --temp-c 36.8 --sbp 118 --dbp 76 --pulse 72 --days-since-last 120
  python donor_eligibility.py --criteria my_sop.json --sex M --age 30 --weight-kg 70 --hb 12.8 --first-time --json
"""
import argparse
import json
import sys

ADVISORY = "ADVISORY: decision support only - confirm with the donor-unit SOP and the responsible MT/physician."

MEASURED = [  # (criteria key, donor field, label)
    ("weight_kg", "weight_kg", "weight (kg)"),
    ("temp_c", "temp_c", "temperature (C)"),
    ("sbp_mmhg", "sbp", "systolic BP (mmHg)"),
    ("dbp_mmhg", "dbp", "diastolic BP (mmHg)"),
    ("pulse_bpm", "pulse", "pulse (/min)"),
]


def limit_text(spec):
    parts = []
    for k, sym in (("min", ">="), ("min_exclusive", ">"), ("max", "<="), ("max_exclusive", "<")):
        if k in spec:
            parts.append("%s %g" % (sym, spec[k]))
    return " and ".join(parts) or "(no limit)"


def judge(value, spec):
    """PASS / FAIL / MISSING. A missing value is never a pass."""
    if value is None:
        return "MISSING"
    if "min" in spec and value < spec["min"]:
        return "FAIL"
    if "min_exclusive" in spec and value <= spec["min_exclusive"]:
        return "FAIL"
    if "max" in spec and value > spec["max"]:
        return "FAIL"
    if "max_exclusive" in spec and value >= spec["max_exclusive"]:
        return "FAIL"
    return "PASS"


def sex_spec(criteria, key, sex):
    """Sex-specific Hb/Hct limits (512303 §10.1 gives separate F and M ranges)."""
    block = criteria.get(key)
    if not block or sex is None:
        return None
    return block.get(sex)


def evaluate(donor, criteria):
    rows = []

    def add(name, value, spec, fail_result="DEFER (temporary)"):
        j = judge(value, spec)
        res = {"PASS": "PASS", "FAIL": fail_result, "MISSING": "NOT ASSESSED"}[j]
        rows.append({"criterion": name, "value": value, "limit": limit_text(spec), "result": res})

    age = donor.get("age")
    if "age_years" in criteria:
        add("age (years)", age, criteria["age_years"], "NOT ELIGIBLE (age)")
    if donor.get("first_time") and "first_time_age_max" in criteria:
        add("first-time donor age", age, {"max": criteria["first_time_age_max"]}, "NOT ELIGIBLE (first-time age)")
    for key, field, label in MEASURED:
        if key in criteria:
            add(label, donor.get(field), criteria[key])

    # anaemia screen: sex-specific Hb and/or Hct; at least one must be measured
    sex = donor.get("sex")
    anaemia_keys = [(k, f, lab) for k, f, lab in (("hb_g_dl", "hb", "Hb (g/dL)"), ("hct_pct", "hct", "Hct (%)"))
                    if k in criteria]
    measured_any = False
    for key, field, label in anaemia_keys:
        val = donor.get(field)
        if val is None:
            continue
        measured_any = True
        spec = sex_spec(criteria, key, sex)
        if spec is None:
            rows.append({"criterion": label, "value": val, "limit": "needs --sex (F/M limits differ)",
                         "result": "NOT ASSESSED"})
        else:
            add("%s [%s]" % (label, sex), val, spec)
    if anaemia_keys and not measured_any:  # nothing measured: goes through judge() like every other value
        add("Hb or Hct", None, sex_spec(criteria, anaemia_keys[0][0], sex) or {})

    if "min_interval_days" in criteria:
        if donor.get("first_time"):
            rows.append({"criterion": "interval since last donation", "value": "first time", "limit": "-",
                         "result": "PASS"})
        else:
            add("days since last donation", donor.get("days_since_last"), {"min": criteria["min_interval_days"]})

    notes = []
    if age is not None and "consent_required_below_age" in criteria and age < criteria["consent_required_below_age"]:
        notes.append("age %s: written guardian consent required (512303 §10.1)" % age)
    volume = None
    w = donor.get("weight_kg")
    for band in criteria.get("volume_by_weight", []):
        if w is not None and judge(w, band["weight_kg"]) == "PASS":
            volume = band["volume_ml"]
            break
    results = [r["result"] for r in rows]
    if not rows:
        overall = "INCOMPLETE - criteria file has no limits this tool can check"
    elif any(r.startswith(("DEFER", "NOT ELIGIBLE")) for r in results):
        overall = "DEFER"
    elif "NOT ASSESSED" in results:
        overall = "INCOMPLETE - cannot accept on missing measurements"
    else:
        overall = "MEASURED CRITERIA MET"
    return {"criteria_label": criteria.get("_label", "(no label in criteria file)"), "rows": rows,
            "overall": overall, "collection_volume_ml": volume if overall == "MEASURED CRITERIA MET" else None,
            "notes": notes,
            "not_assessed_by_tool": "health questionnaire, risk behaviour, medication, travel, recent "
                                    "procedures, permanent-deferral list -> judgment + SOP (card Fork 1 steps 3-4)"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--criteria", required=True, help="JSON criteria file from YOUR SOP (no built-in limits)")
    ap.add_argument("--sex", choices=["F", "M"])
    ap.add_argument("--age", type=float)
    ap.add_argument("--weight-kg", type=float)
    ap.add_argument("--hb", type=float, help="g/dL")
    ap.add_argument("--hct", type=float, help="%%")
    ap.add_argument("--temp-c", type=float)
    ap.add_argument("--sbp", type=float)
    ap.add_argument("--dbp", type=float)
    ap.add_argument("--pulse", type=float)
    ap.add_argument("--days-since-last", type=float)
    ap.add_argument("--first-time", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        with open(a.criteria, encoding="utf-8") as f:
            criteria = json.load(f)
    except (OSError, ValueError) as e:
        ap.error("cannot read criteria file: %s" % e)
    donor = {"sex": a.sex, "age": a.age, "weight_kg": a.weight_kg, "hb": a.hb, "hct": a.hct, "temp_c": a.temp_c,
             "sbp": a.sbp, "dbp": a.dbp, "pulse": a.pulse, "days_since_last": a.days_since_last,
             "first_time": a.first_time}
    res = evaluate(donor, criteria)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("criteria: %s" % res["criteria_label"])
    print("%-32s %-12s %-22s %s" % ("criterion", "value", "limit", "result"))
    for r in res["rows"]:
        v = "-" if r["value"] is None else ("%g" % r["value"] if isinstance(r["value"], (int, float)) else r["value"])
        print("%-32s %-12s %-22s %s" % (r["criterion"], v, r["limit"], r["result"]))
    print("-" * 78)
    print("OVERALL (measured criteria only): %s" % res["overall"])
    if res["collection_volume_ml"]:
        print("collection volume by weight band : %d mL" % res["collection_volume_ml"])
    for n in res["notes"]:
        print("note: %s" % n)
    print("not assessed by this tool: %s" % res["not_assessed_by_tool"])
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
