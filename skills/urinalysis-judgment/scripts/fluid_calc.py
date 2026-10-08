#!/usr/bin/env python3
"""fluid_calc - body-fluid reads from the card's Fork 5: Light's criteria, CSF tube 1->3 RBC, synovial crystals.

Black-box tool for urinalysis-judgment (Fork 5). Run --help first. Sources:
  lights    exudate if ANY one is met (Light RW et al. Ann Intern Med 1972;77:507-13):
              fluid/serum protein > 0.5 ; fluid/serum LDH > 0.6 ; fluid LDH > 2/3 x serum LDH ULN
            criteria listed in owner digest 503402-DIGEST-2026-05-31.md section 8 (serous fluid).
            The serum LDH upper limit is YOUR lab's (--ldh-uln, required). Light's criteria were derived
            for PLEURAL fluid; for ascites many labs use the serum-ascites albumin gradient instead -> SOP.
  csf       RBC falling from tube 1 to tube 3 supports a traumatic tap but is NOT decisive: clearing
            does not exclude SAH (card Fork 5). Xanthochromia only from a promptly spun supernatant.
            Count cells within 1 h (503402 section 8; card: count immediately). Optional CSF/serum glucose
            ratio, judged only against YOUR cutoff (--ratio-low).
  synovial  MSU = needle, NEGATIVE birefringence = gout; CPPD = rhomboid, POSITIVE birefringence =
            pseudogout (card Fork 5; 503402 section 8). Other combinations -> re-check compensator /
            identity. Always correlate cell count + Gram (septic joint = emergency).
ADVISORY ONLY.

Examples
  python fluid_calc.py lights --fluid-protein 3.5 --serum-protein 6.5 --fluid-ldh 150 --serum-ldh 300 --ldh-uln 250
  python fluid_calc.py csf --tube1-rbc 12000 --tube3-rbc 800 --minutes-to-count 30
  python fluid_calc.py synovial --shape needle --birefringence negative
"""
import argparse
import json
import sys


def lights(fluid_protein, serum_protein, fluid_ldh, serum_ldh, ldh_uln, fluid_type="pleural"):
    crit = [
        {"criterion": "fluid/serum protein > 0.5", "value": fluid_protein / serum_protein, "limit": 0.5},
        {"criterion": "fluid/serum LDH > 0.6", "value": fluid_ldh / serum_ldh, "limit": 0.6},
        {"criterion": "fluid LDH > 2/3 x serum LDH ULN", "value": fluid_ldh, "limit": 2 / 3 * ldh_uln},
    ]
    for c in crit:
        c["met"] = c["value"] > c["limit"]
    exudate = any(c["met"] for c in crit)
    res = {"criteria": crit, "n_met": sum(c["met"] for c in crit),
           "result": "EXUDATE (>= 1 criterion met)" if exudate else "TRANSUDATE (no criterion met)",
           "meaning": ("inflammation / malignancy / infection" if exudate else
                       "CHF / cirrhosis / hypoproteinemia (hydrostatic up / oncotic down)")}
    if fluid_type != "pleural":
        res["note"] = ("Light's criteria were derived for pleural fluid; for %s fluid follow your SOP "
                       "(ascites: serum-ascites albumin gradient is common)" % fluid_type)
    return res


def csf(tube1_rbc, tube3_rbc, minutes_to_count=None, csf_glucose=None, serum_glucose=None, ratio_low=None):
    res = {"tube1_rbc": tube1_rbc, "tube3_rbc": tube3_rbc}
    if tube1_rbc > 0:
        res["fall_pct"] = (tube1_rbc - tube3_rbc) / tube1_rbc * 100
    if tube3_rbc < tube1_rbc:
        res["reading"] = ("RBC falls tube 1 -> 3: SUPPORTS traumatic tap, NOT decisive - clearing does not exclude "
                          "SAH (a real SAH can carry a traumatic tap on top)")
    else:
        res["reading"] = "no clearing tube 1 -> 3: does not support traumatic tap; SAH stays on the table"
    res["xanthochromia"] = "judge only on a supernatant spun promptly (standing whole CSF -> in-vitro lysis -> false xanthochromia)"
    if minutes_to_count is not None and minutes_to_count > 60:
        res["timing"] = "counted %g min after collection (> 1 h): cells lyse -> count is unreliable" % minutes_to_count
    if csf_glucose is not None and serum_glucose:
        ratio = csf_glucose / serum_glucose
        res["glucose_ratio"] = ratio
        if ratio_low is not None:
            res["glucose_reading"] = ("ratio %.2f < your cutoff %g -> low CSF glucose" % (ratio, ratio_low)
                                      if ratio < ratio_low else "ratio %.2f >= your cutoff %g" % (ratio, ratio_low))
        else:
            res["glucose_reading"] = "no --ratio-low: ratio not judged (cutoff per SOP)"
    return res


def synovial(shape, birefringence):
    shape, bi = shape.lower(), birefringence.lower()
    if shape == "needle" and bi == "negative":
        crystal, meaning = "MSU (monosodium urate)", "gout"
    elif shape == "rhomboid" and bi == "positive":
        crystal, meaning = "CPPD (calcium pyrophosphate)", "pseudogout"
    else:
        crystal, meaning = "INCONSISTENT", ("shape + sign do not match MSU (needle, negative) or CPPD (rhomboid, "
                                            "positive) -> re-check compensator orientation / identity")
    return {"shape": shape, "birefringence": bi, "crystal": crystal, "meaning": meaning,
            "always": "correlate cell count + Gram stain: septic joint = emergency"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("lights")
    p.add_argument("--fluid-protein", type=float, required=True)
    p.add_argument("--serum-protein", type=float, required=True)
    p.add_argument("--fluid-ldh", type=float, required=True)
    p.add_argument("--serum-ldh", type=float, required=True)
    p.add_argument("--ldh-uln", type=float, required=True, help="your lab's serum LDH upper reference limit")
    p.add_argument("--fluid", choices=["pleural", "peritoneal", "pericardial"], default="pleural")
    p = sub.add_parser("csf")
    p.add_argument("--tube1-rbc", type=float, required=True)
    p.add_argument("--tube3-rbc", type=float, required=True)
    p.add_argument("--minutes-to-count", type=float)
    p.add_argument("--csf-glucose", type=float)
    p.add_argument("--serum-glucose", type=float)
    p.add_argument("--ratio-low", type=float, help="your SOP's low CSF/serum glucose ratio cutoff")
    p = sub.add_parser("synovial")
    p.add_argument("--shape", required=True, choices=["needle", "rhomboid", "other"])
    p.add_argument("--birefringence", required=True, choices=["negative", "positive", "none"])
    a = ap.parse_args(argv)
    if a.cmd == "lights":
        res = lights(a.fluid_protein, a.serum_protein, a.fluid_ldh, a.serum_ldh, a.ldh_uln, a.fluid)
    elif a.cmd == "csf":
        res = csf(a.tube1_rbc, a.tube3_rbc, a.minutes_to_count, a.csf_glucose, a.serum_glucose, a.ratio_low)
    else:
        res = synovial(a.shape, a.birefringence)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        for k, v in res.items():
            if k == "criteria":
                print("%-34s %-9s %-9s %s" % ("criterion", "value", "limit", "met"))
                for c in v:
                    print("%-34s %-9.3f %-9.3f %s" % (c["criterion"], c["value"], c["limit"], c["met"]))
            else:
                print("%-16s %s" % (k, ("%.3f" % v) if isinstance(v, float) else v))
        print("ADVISORY: decision support only - correlate clinically; confirm with the lab SOP and MT/physician.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
