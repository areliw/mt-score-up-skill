#!/usr/bin/env python3
"""renal - eGFR / 24-h creatinine clearance / BUN:Cr ratio, with the card's renal traps printed.

Black-box tool for chemistry-interpretation-judgment (Fork 2). Run --help first. All inputs mg/dL
unless stated. Sources:
  egfr   CKD-EPI 2021 race-free creatinine equation (card: default for every GFR range) -
         Inker LA et al. N Engl J Med 2021;385:1737-49:
           eGFR = 142 x min(Scr/k,1)^a x max(Scr/k,1)^-1.200 x 0.9938^age x 1.012 [female]
           k = 0.7 (F) / 0.9 (M), a = -0.241 (F) / -0.302 (M); adults (>= 18 y) only
         Cockcroft-Gault (drug dosing) - owner digest CLINCHEM2 section 3:
           CrCl = (140 - age) x weight / (72 x Scr), x 0.85 if female   [mL/min, not per 1.73 m2]
  crcl   CrCl = (Ucr x V) / (Pcr x minutes). Completeness check from total urine creatinine
         excretion (mg/kg/day): card Fork 2 teaching ~20-25 (M) / 15-20 (F), "much below ~15 =
         under-collection" -> default floor 15. NOTE: CLINCHEM2 section 3 uses a lower floor
         (8.5 mg/kg/day) - sources disagree, set --min-mgkg from your SOP.
  bun-cr ratio > 20 = prerenal / GI bleed (card Fork 2; owner digest 505402 section 5.4).
         --urea converts urea mg/dL to BUN with BUN = urea / 2.14 (505402 section 5.4).
Creatinine SI input: mg/dL = umol/L / 88.4 (creatinine MW 113.1). ADVISORY ONLY.

Examples
  python renal.py egfr --cr 1.0 --age 50 --sex M --weight 70
  python renal.py crcl --ucr 100 --volume 1440 --hours 24 --pcr 1.0 --weight 70 --sex M
  python renal.py bun-cr --bun 37 --cr 1.5
"""
import argparse
import json
import sys

CAVEATS = [
    "Cr normal != kidney normal: <25% glomerular loss keeps Cr normal; elderly (low muscle) and cirrhosis "
    "(low creatine) -> Cr falsely reassuring -> consider cystatin C (card Fork 2)",
    "Jaffe Cr: glucose/protein/vit C/ASA/cephalosporin/ketone raise Cr (GFR UNDER-estimated); bilirubin lowers "
    "Cr (GFR OVER-estimated) -> compute GFR from enzymatic Cr (card Fork 2)",
]


def to_mgdl(cr=None, cr_umol=None):
    if (cr is None) == (cr_umol is None):
        raise ValueError("give exactly one of --cr (mg/dL) or --cr-umol (umol/L)")
    return cr if cr is not None else cr_umol / 88.4


def ckd_epi_2021(scr, age, female):
    if age < 18:
        raise ValueError("CKD-EPI 2021 is for adults (>= 18 y); use a paediatric equation per SOP")
    if scr <= 0:
        raise ValueError("creatinine must be > 0")
    k, a = (0.7, -0.241) if female else (0.9, -0.302)
    r = scr / k
    egfr = 142 * min(r, 1.0) ** a * max(r, 1.0) ** -1.200 * 0.9938 ** age
    return egfr * 1.012 if female else egfr


def cockcroft_gault(age, weight, scr, female):
    crcl = (140 - age) * weight / (72 * scr)
    return crcl * 0.85 if female else crcl


def crcl_24h(ucr, volume_ml, hours, pcr):
    return ucr * volume_ml / (pcr * hours * 60)


def excretion_mg_day(ucr, volume_ml, hours):
    """Ucr mg/dL x V mL / 100 (mL -> dL) scaled to 24 h."""
    return ucr * volume_ml / 100 * 24 / hours


def collection_check(mg_per_kg_day, min_mgkg=15.0):
    if mg_per_kg_day < min_mgkg:
        return {"complete": False,
                "verdict": "UNDER-COLLECTION suspected: urine Cr %.1f mg/kg/day < %.1f -> CrCl unreliable, re-collect"
                           % (mg_per_kg_day, min_mgkg)}
    return {"complete": True, "verdict": "collection plausible (%.1f mg/kg/day >= %.1f)" % (mg_per_kg_day, min_mgkg)}


def bun_cr(bun, cr):
    ratio = bun / cr
    if ratio > 20:
        reading = "> 20 -> prerenal / GI bleed pattern (dehydration, high protein, steroid)"
    else:
        reading = "<= 20 -> no prerenal signal from the ratio alone; read BUN and Cr together, follow the trend"
    return {"bun": bun, "cr": cr, "ratio": ratio, "reading": reading}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("egfr")
    p.add_argument("--cr", type=float, help="serum creatinine mg/dL (IDMS-traceable, enzymatic preferred)")
    p.add_argument("--cr-umol", type=float, help="serum creatinine umol/L")
    p.add_argument("--age", type=float, required=True)
    p.add_argument("--sex", choices=["M", "F"], required=True)
    p.add_argument("--weight", type=float, help="kg, actual body weight -> adds Cockcroft-Gault")
    p = sub.add_parser("crcl")
    p.add_argument("--ucr", type=float, required=True, help="urine creatinine mg/dL")
    p.add_argument("--volume", type=float, required=True, help="urine volume mL")
    p.add_argument("--hours", type=float, default=24.0)
    p.add_argument("--pcr", type=float, required=True, help="plasma creatinine mg/dL")
    p.add_argument("--weight", type=float, help="kg -> completeness check")
    p.add_argument("--sex", choices=["M", "F"])
    p.add_argument("--min-mgkg", type=float, default=15.0,
                   help="under-collection floor mg/kg/day (default 15 = card teaching value)")
    p = sub.add_parser("bun-cr")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--bun", type=float, help="BUN mg/dL")
    g.add_argument("--urea", type=float, help="urea mg/dL (BUN = urea / 2.14)")
    p.add_argument("--cr", type=float, required=True, help="creatinine mg/dL")
    a = ap.parse_args(argv)

    if a.cmd == "egfr":
        scr = to_mgdl(a.cr, a.cr_umol)
        female = a.sex == "F"
        res = {"scr_mgdl": scr, "age": a.age, "sex": a.sex,
               "ckd_epi_2021": ckd_epi_2021(scr, a.age, female), "unit": "mL/min/1.73m2"}
        if a.weight is not None:
            res["cockcroft_gault_ml_min"] = cockcroft_gault(a.age, a.weight, scr, female)
        res["caveats"] = CAVEATS
    elif a.cmd == "crcl":
        res = {"crcl_ml_min": crcl_24h(a.ucr, a.volume, a.hours, a.pcr),
               "urine_cr_mg_day": excretion_mg_day(a.ucr, a.volume, a.hours)}
        if a.weight:
            res["urine_cr_mg_kg_day"] = res["urine_cr_mg_day"] / a.weight
            res["collection"] = collection_check(res["urine_cr_mg_kg_day"], a.min_mgkg)
            res["expected_card_teaching"] = "M 20-25, F 15-20 mg/kg/day"
        else:
            res["collection"] = {"complete": None, "verdict": "no --weight: completeness NOT checked"}
        res["caveats"] = ["very low GFR: tubular Cr secretion rises -> CrCl OVER-estimates GFR (card Fork 2)"]
    else:
        bun = a.bun if a.bun is not None else a.urea / 2.14
        res = bun_cr(bun, a.cr)
        if a.urea is not None:
            res["note"] = "BUN derived from urea %.1f / 2.14" % a.urea
        res["caveats"] = ["BUN moves with diet / liver / GI bleed: never read one BUN alone (card Fork 2)",
                          "ratio assumes conventional mg/dL units; SI urea:creatinine ratios are on another scale"]

    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        for k, v in res.items():
            if k == "caveats":
                for c in v:
                    print("%-22s %s" % ("caveat", c))
            elif isinstance(v, dict):
                print("%-22s %s" % (k, v.get("verdict", v)))
            else:
                print("%-22s %s" % (k, ("%.2f" % v) if isinstance(v, float) else v))
        print("ADVISORY: decision support only - confirm with the lab SOP/reference ranges; diagnosis is the physician's.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
