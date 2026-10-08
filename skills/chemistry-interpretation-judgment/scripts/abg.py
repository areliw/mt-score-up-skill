#!/usr/bin/env python3
"""abg - read an arterial blood gas in the card's 5 steps, plus anion gap.

Black-box tool for chemistry-interpretation-judgment (Fork 5). Run --help first; read the source
only if a result looks wrong. Source: owner digest CLINCHEM2-DIGEST-2026-06-01.md section 6:
  5 steps   pH -> PCO2 -> HCO3 -> the value that moves WITH the pH is the cause
            (CO2 = respiratory, HCO3 = metabolic) -> compensation: uncompensated (only one abnormal) /
            partially (both abnormal, pH still abnormal) / fully (pH normal, side judged against 7.40)
  refs      teaching reference values pH 7.35-7.45, PCO2 35-45 mmHg, HCO3 22-26 mmol/L (defaults below;
            pass your lab's with --ph-ref / --pco2-ref / --hco3-ref)
  HH        pH = 6.1 + log10(HCO3 / (0.03 x PCO2))  -> internal-consistency check only
  AG        AG = (Na + K) - (Cl + HCO3); high AG = DKA / lactic / renal failure / toxin
            (methanol, ethylene glycol, salicylate); normal AG = diarrhea / RTA / CA inhibitor
  urine Cl  metabolic alkalosis: urine Cl < 10 saline-responsive, > 20 saline-resistant
The AG reference interval depends on the analyzer AND on whether K is in the formula -> pass --ag-ref.
Without it the tool prints the AG but does not call it high or normal. ADVISORY ONLY.

Examples
  python abg.py --ph 7.31 --pco2 33 --hco3 16
  python abg.py --ph 7.31 --pco2 33 --hco3 16 --na 138 --k 3.9 --cl 113 --ag-ref 10-20
  python abg.py --ph 7.50 --pco2 46 --hco3 34 --urine-cl 6 --json
"""
import argparse
import json
import math
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

TEACHING_PH = (7.35, 7.45)
TEACHING_PCO2 = (35.0, 45.0)
TEACHING_HCO3 = (22.0, 26.0)
PH_MID = 7.40

HIGH_AG = "DKA/ketoacidosis, lactic acidosis, renal failure, toxin (methanol / ethylene glycol / salicylate)"
NORMAL_AG = "diarrhea (GI loss), RTA, carbonic-anhydrase inhibitor (acetazolamide)"


def parse_range(text):
    lo, hi = (float(x) for x in text.replace(" ", "").split("-", 1))
    if lo >= hi:
        raise argparse.ArgumentTypeError("range must be LOW-HIGH with LOW < HIGH")
    return (lo, hi)


def _dir(value, ref, high, low):
    if value > ref[1]:
        return high
    if value < ref[0]:
        return low
    return "normal"


def primary_disorders(side, resp_dir, met_dir):
    """Step 4: the component(s) whose direction matches the pH side ('acid'/'base') is the cause."""
    out = []
    if resp_dir == side:
        out.append("respiratory")
    if met_dir == side:
        out.append("metabolic")
    return out


def classify(ph, pco2, hco3, ph_ref=TEACHING_PH, pco2_ref=TEACHING_PCO2, hco3_ref=TEACHING_HCO3,
             ph_mid=PH_MID):
    if ph < ph_ref[0]:
        ph_state, side = "acidemia", "acid"
    elif ph > ph_ref[1]:
        ph_state, side = "alkalemia", "base"
    else:
        ph_state = "normal"
        side = "acid" if ph < ph_mid else ("base" if ph > ph_mid else None)
    resp = _dir(pco2, pco2_ref, high="acid", low="base")   # PCO2 up = acid direction
    met = _dir(hco3, hco3_ref, high="base", low="acid")    # HCO3 down = acid direction
    res = {"ph": ph, "pco2": pco2, "hco3": hco3, "ph_state": ph_state, "side": side,
           "pco2_direction": resp, "hco3_direction": met, "primary": [], "compensation": None,
           "result": "", "check": ""}
    noun = {"acid": "acidosis", "base": "alkalosis"}
    if ph_state == "normal":
        if resp == "normal" and met == "normal":
            res["result"] = "normal acid-base (pH, PCO2, HCO3 all within reference)"
            return res
        if "normal" in (resp, met):
            res["result"] = "not classifiable by the 5 steps"
            res["check"] = ("pH normal with ONE abnormal component: consider a mixed disorder or an "
                            "entry/pre-analytical error; recheck")
            return res
        if resp == met:
            res["result"] = "inconsistent values"
            res["check"] = "both components push the same way but pH is normal: recheck sample / entry"
            return res
        if side is None:
            res["result"] = "fully compensated, primary not assignable (pH exactly %.2f)" % ph_mid
            return res
        res["primary"] = primary_disorders(side, resp, met)
        res["compensation"] = "fully compensated"
    else:
        res["primary"] = primary_disorders(side, resp, met)
        if not res["primary"]:
            res["result"] = "no component explains the pH"
            res["check"] = "neither PCO2 nor HCO3 moves with the pH: recheck sample / entry (pre-analytical)"
            return res
        if len(res["primary"]) == 2:
            res["result"] = "mixed respiratory + metabolic %s" % noun[side]
            res["compensation"] = "not applicable (both components push pH the same way)"
            return res
        other = met if res["primary"] == ["respiratory"] else resp
        res["compensation"] = "uncompensated" if other == "normal" else "partially compensated"
    res["result"] = "%s %s, %s" % (res["primary"][0], noun[side], res["compensation"])
    return res


def anion_gap(na, cl, hco3, k=None):
    if k is None:
        return {"ag": na - (cl + hco3), "formula": "Na - (Cl + HCO3)  [without K]"}
    return {"ag": (na + k) - (cl + hco3), "formula": "(Na + K) - (Cl + HCO3)"}


def classify_ag(ag, ref):
    if ref is None:
        return None
    if ag > ref[1]:
        return "high"
    if ag < ref[0]:
        return "low"
    return "normal"


def hh_ph(hco3, pco2):
    return 6.1 + math.log10(hco3 / (0.03 * pco2))


def urine_cl_reading(ucl):
    if ucl < 10:
        return "saline-responsive (vomiting, NG suction, diuretic)"
    if ucl > 20:
        return "saline-resistant (mineralocorticoid excess)"
    return "between the card bands (<10 responsive, >20 resistant): not classified"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ph", type=float, required=True)
    ap.add_argument("--pco2", type=float, required=True, help="mmHg")
    ap.add_argument("--hco3", type=float, required=True, help="mmol/L")
    ap.add_argument("--na", type=float)
    ap.add_argument("--k", type=float)
    ap.add_argument("--cl", type=float)
    ap.add_argument("--no-k", action="store_true", help="compute AG as Na - (Cl + HCO3) even if K is given")
    ap.add_argument("--ag-ref", type=parse_range, help="your lab's AG reference LOW-HIGH for the SAME formula")
    ap.add_argument("--urine-cl", type=float, help="urine chloride mmol/L (metabolic alkalosis)")
    ap.add_argument("--ph-ref", type=parse_range, default=TEACHING_PH, help="default 7.35-7.45 (teaching)")
    ap.add_argument("--pco2-ref", type=parse_range, default=TEACHING_PCO2, help="default 35-45 (teaching)")
    ap.add_argument("--hco3-ref", type=parse_range, default=TEACHING_HCO3, help="default 22-26 (teaching)")
    ap.add_argument("--hh-tol", type=float, help="flag if |reported pH - HH pH| exceeds this (optional)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    res = classify(a.ph, a.pco2, a.hco3, a.ph_ref, a.pco2_ref, a.hco3_ref)
    res["refs"] = {"ph": a.ph_ref, "pco2": a.pco2_ref, "hco3": a.hco3_ref}
    hh = hh_ph(a.hco3, a.pco2)
    res["hh"] = {"ph_from_hco3_pco2": hh, "diff": a.ph - hh,
                 "flag": (abs(a.ph - hh) > a.hh_tol) if a.hh_tol is not None else None}
    if a.na is not None and a.cl is not None:
        ag = anion_gap(a.na, a.cl, a.hco3, None if a.no_k else a.k)
        ag["ref"] = a.ag_ref
        ag["class"] = classify_ag(ag["ag"], a.ag_ref)
        if ag["class"] == "high":
            ag["reading"] = "high-AG group: " + HIGH_AG
        elif ag["class"] == "normal":
            ag["reading"] = "normal-AG (hyperchloremic) group: " + NORMAL_AG
        elif ag["class"] == "low":
            ag["reading"] = "below your reference: not covered by the card; recheck values"
        else:
            ag["reading"] = "no --ag-ref given: AG not classified (interval is analyzer + formula specific)"
        if "metabolic" not in res["primary"] or res["side"] != "acid":
            ag["note"] = "card uses AG to split METABOLIC ACIDOSIS; primary here is not metabolic acidosis"
        res["anion_gap"] = ag
    if a.urine_cl is not None:
        res["urine_cl"] = {"value": a.urine_cl, "reading": urine_cl_reading(a.urine_cl)}
        if not ("metabolic" in res["primary"] and res["side"] == "base"):
            res["urine_cl"]["note"] = "card uses urine Cl for METABOLIC ALKALOSIS; primary here is not that"

    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    r = res
    print("%-5s %-13s %-8s %-12s %s" % ("step", "item", "value", "reference", "reading"))
    print("%-5s %-13s %-8s %-12s %s" % ("1", "pH", a.ph, "%g-%g" % a.ph_ref, r["ph_state"]))
    print("%-5s %-13s %-8s %-12s %s" % ("2", "PCO2", a.pco2, "%g-%g" % a.pco2_ref,
                                         "%s direction" % r["pco2_direction"] if r["pco2_direction"] != "normal" else "normal"))
    print("%-5s %-13s %-8s %-12s %s" % ("3", "HCO3", a.hco3, "%g-%g" % a.hco3_ref,
                                         "%s direction" % r["hco3_direction"] if r["hco3_direction"] != "normal" else "normal"))
    print("%-5s %-13s %s" % ("4", "primary", ", ".join(r["primary"]) or "-"))
    print("%-5s %-13s %s" % ("5", "compensation", r["compensation"] or "-"))
    print("RESULT: %s" % r["result"])
    if r["check"]:
        print("CHECK: %s" % r["check"])
    if "anion_gap" in r:
        g = r["anion_gap"]
        print("AG = %s = %.1f  %s" % (g["formula"], g["ag"],
                                      ("vs ref %g-%g -> %s" % (g["ref"][0], g["ref"][1], g["class"])) if g["ref"] else ""))
        print("     %s" % g["reading"])
        if g.get("note"):
            print("     NOTE: %s" % g["note"])
    if "urine_cl" in r:
        print("urine Cl %.0f -> %s%s" % (a.urine_cl, r["urine_cl"]["reading"],
                                        ("  (NOTE: %s)" % r["urine_cl"]["note"]) if r["urine_cl"].get("note") else ""))
    print("HH check: pH from HCO3/PCO2 = %.3f (reported %.2f, diff %+.3f)%s" % (
        hh, a.ph, a.ph - hh, "  -> CHECK: values not internally consistent (entry / pre-analytical: "
        "air bubble pO2 up pCO2 down pH up; delay pO2 down pCO2 up pH down)" if r["hh"]["flag"] else ""))
    print("ADVISORY: decision support only - confirm with the lab SOP/reference ranges; diagnosis is the physician's.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
