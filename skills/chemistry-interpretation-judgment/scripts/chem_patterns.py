#!/usr/bin/env python3
"""chem_patterns - the card's ratio reads: LFT (AST:ALT, DB/TB), cardiac (CK-MB index, troponin delta), LDL.

Black-box tool for chemistry-interpretation-judgment (Forks 3, 4, 7). Run --help first. Units mg/dL, U/L.
Sources (owner digests; the card's own bands win where they are stated):
  lft      AST:ALT >= 2 = alcoholic pattern; AST > 500 in a drinker = look for another cause
           (alcoholic usually < 300); ALT > AST = usual liver injury; AST/ALT > 2000 = think
           ischemic hepatitis (falls within ~1 week)                        - CLINCHEM2 section 4, card Fork 3
           DB/TB % : < 20 prehepatic (hemolysis/Gilbert) | 30-60 mixed hepatic (hepatitis/cirrhosis) |
           > 70 conjugated (cholestasis/obstruction). 20-30 and 60-70 are gaps between the card's bands:
           reported as "between bands", never guessed                    - card Fork 3, 505402 section 5.3
  cardiac  CK-MB relative index = CK-MB mass x 100 / total CK              - CLINCHEM2 section 5
           bands from the card (lab-dependent): < 2.5 % skeletal, > 5 % cardiac, 2.5-5 borderline
           troponin: delta = later - earlier; significance needs YOUR assay's delta cutoff (--delta-cutoff)
  ldl      Friedewald LDL-C = TC - HDL-C - TG/5; not valid when TG >= 400 or non-fasting
           (505402 section 5.2; card Fork 7 says "> 400" - the stricter >= is used); card: underestimates
           from TG ~150, so a caution prints for TG 150-399.
ADVISORY ONLY.

Examples
  python chem_patterns.py lft --ast 577 --alt 1220 --dbil 5.8 --tbil 10
  python chem_patterns.py cardiac --ckmb 12 --ck 150 --ctn0 10 --ctn1 35 --delta-cutoff 5
  python chem_patterns.py ldl --tc 200 --hdl 50 --tg 150
"""
import argparse
import json
import sys


def lft(ast, alt, dbil=None, tbil=None, tb_uln=None):
    out = {"ast": ast, "alt": alt, "ast_alt_ratio": ast / alt, "notes": []}
    r = out["ast_alt_ratio"]
    if r >= 2:
        out["ratio_reading"] = "AST:ALT >= 2 -> alcoholic pattern (look for GGT/ALP support)"
        if ast > 500:
            out["notes"].append("AST > 500 is atypical for alcoholic injury (usually < 300) -> look for another cause")
    elif r < 1:
        out["ratio_reading"] = "ALT > AST -> usual hepatocellular injury pattern"
    else:
        out["ratio_reading"] = "AST >= ALT but < 2x -> no card pattern; read with GGT/ALP/history (non-hepatic AST: "\
                               "hemolysis, muscle, exercise)"
    if max(ast, alt) > 2000:
        out["notes"].append("> 2000: consider ischemic hepatitis ('shock liver') - self-limited if it falls within "
                            "~1 week; check the trend before alarm")
    if dbil is not None and tbil is not None:
        out.update(bilirubin_fraction(dbil, tbil, tb_uln))
    out["notes"] = out.pop("notes")  # print notes after the readings
    return out


def bilirubin_fraction(dbil, tbil, tb_uln=None):
    if dbil > tbil:
        raise ValueError("direct bilirubin cannot exceed total")
    pct = dbil / tbil * 100
    if pct < 20:
        band = "< 20 % -> mostly unconjugated: prehepatic (hemolysis, Gilbert)"
    elif pct < 30:
        band = "20-30 % -> between card bands (card: < 20 prehepatic; digest: < 20-30 unconjugated) - not classified"
    elif pct <= 60:
        band = "30-60 % -> mixed: hepatic (hepatitis, cirrhosis)"
    elif pct <= 70:
        band = "60-70 % -> between card bands (30-60 mixed / > 70 conjugated) - not classified"
    else:
        band = "> 70 % -> conjugated: cholestasis / obstruction"
    res = {"db_tb_pct": pct, "db_tb_reading": band}
    if tb_uln is not None and tbil <= tb_uln:
        res["db_tb_note"] = "total bilirubin within ULN: the fraction is less informative"
    return res


def ckmb_index(ckmb_mass, ck_total, skeletal_below=2.5, cardiac_above=5.0):
    idx = ckmb_mass * 100 / ck_total
    if idx < skeletal_below:
        band = "skeletal muscle source more likely"
    elif idx > cardiac_above:
        band = "cardiac source more likely"
    else:
        band = "borderline"
    return {"ckmb_index_pct": idx, "band": band,
            "bands_used": "< %g skeletal / > %g cardiac (card teaching, lab-dependent)" % (skeletal_below, cardiac_above),
            "note": "CK-MB is secondary to troponin; use CK-MB MASS (not activity)"}


def troponin_delta(c0, c1, cutoff=None):
    d = c1 - c0
    res = {"ctn_first": c0, "ctn_second": c1, "delta": d, "abs_delta": abs(d),
           "rule": "single troponin never = MI: rise/fall + clinical + EKG (card Fork 4); "
                   "renal failure / sepsis / PE / HF / exercise also raise it"}
    if cutoff is None:
        res["reading"] = "no --delta-cutoff: change not judged (cutoff is assay- and algorithm-specific)"
    else:
        res["reading"] = ("|delta| %g >= your cutoff %g -> significant change by your algorithm" % (abs(d), cutoff)
                          if abs(d) >= cutoff else "|delta| %g < your cutoff %g -> no significant change" % (abs(d), cutoff))
    return res


def friedewald(tc, hdl, tg, fasting=True):
    if not fasting:
        return {"ldl": None, "valid": False, "verdict": "NOT VALID: non-fasting sample -> direct LDL-C"}
    if tg >= 400:
        return {"ldl": None, "valid": False, "verdict": "NOT VALID: TG >= 400 mg/dL -> direct LDL-C"}
    res = {"ldl": tc - hdl - tg / 5, "valid": True, "verdict": "LDL-C = TC - HDL-C - TG/5 (fasting)"}
    if tg >= 150:
        res["caution"] = "TG >= 150: Friedewald starts to UNDER-estimate LDL-C (card Fork 7) - consider direct LDL-C"
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("lft")
    p.add_argument("--ast", type=float, required=True)
    p.add_argument("--alt", type=float, required=True)
    p.add_argument("--dbil", type=float, help="direct bilirubin mg/dL")
    p.add_argument("--tbil", type=float, help="total bilirubin mg/dL")
    p.add_argument("--tb-uln", type=float, help="your lab's total bilirubin ULN (optional)")
    p = sub.add_parser("cardiac")
    p.add_argument("--ckmb", type=float, help="CK-MB mass (ng/mL)")
    p.add_argument("--ck", type=float, help="total CK (U/L)")
    p.add_argument("--skeletal-below", type=float, default=2.5)
    p.add_argument("--cardiac-above", type=float, default=5.0)
    p.add_argument("--ctn0", type=float, help="first troponin (same assay, same units)")
    p.add_argument("--ctn1", type=float, help="second troponin")
    p.add_argument("--delta-cutoff", type=float, help="your assay/algorithm delta cutoff (same units)")
    p = sub.add_parser("ldl")
    p.add_argument("--tc", type=float, required=True)
    p.add_argument("--hdl", type=float, required=True)
    p.add_argument("--tg", type=float, required=True)
    p.add_argument("--non-fasting", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "lft":
        res = lft(a.ast, a.alt, a.dbil, a.tbil, a.tb_uln)
    elif a.cmd == "cardiac":
        res = {}
        if a.ckmb is not None and a.ck is not None:
            res["ckmb"] = ckmb_index(a.ckmb, a.ck, a.skeletal_below, a.cardiac_above)
        if a.ctn0 is not None and a.ctn1 is not None:
            res["troponin"] = troponin_delta(a.ctn0, a.ctn1, a.delta_cutoff)
        if not res:
            ap.error("cardiac needs --ckmb + --ck and/or --ctn0 + --ctn1")
    else:
        res = friedewald(a.tc, a.hdl, a.tg, not a.non_fasting)

    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        def show(d, pad=""):
            for k, v in d.items():
                if isinstance(v, dict):
                    print("%s%s:" % (pad, k))
                    show(v, pad + "  ")
                elif isinstance(v, list):
                    for item in v:
                        print("%s%-18s %s" % (pad, "note", item))
                else:
                    print("%s%-18s %s" % (pad, k, ("%.3f" % v) if isinstance(v, float) else v))
        show(res)
        print("ADVISORY: decision support only - confirm with the lab SOP/reference ranges; diagnosis is the physician's.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
