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
  tnc       hemocytometer total nucleated cell count (improved Neubauer: one large square = 1 mm2 x 0.1 mm
            = 0.1 uL):  cells/uL = cells counted x DF / (squares x area_mm2 x depth_mm).  cells/uL = cells/cu.mm
            = x10^6/L. DF comes from volumes (DF = (sample + diluent) / sample) because ratio strings are
            ambiguous ("1:9" = 1 in 9 total, or 1 + 9?). EQA round reviews rank dilution-factor / unit
            slips and swapped sample numbers among the top count failures.
  eqa-check a reported count vs the EQA assigned range; when it misses, tests which classic slip lands it in
            range (forgot DF / applied DF twice / x10 chamber slip / x1000 unit slip / swapped sample number)
            and, on a 0-cell sample, separates "within your background/LoQ limit" from "above it -> investigate".
  pd        peritoneal dialysate: peritonitis suspected when WBC > 100/uL AND neutrophils > 50% of TNCC
            (ISPD 2022, after a dwell of >= 2 h). Exactly 50% = INDETERMINATE boundary: some teaching material
            writes >= 50%, so the lab SOP decides.
            Not met != no peritonitis (ISPD = 2 of 3: clinical, effluent, culture); PMN >= 50% with a low count
            after a short dwell = INDETERMINATE, not negative.
ADVISORY ONLY.

Examples
  python fluid_calc.py lights --fluid-protein 3.5 --serum-protein 6.5 --fluid-ldh 150 --serum-ldh 300 --ldh-uln 250
  python fluid_calc.py csf --tube1-rbc 12000 --tube3-rbc 800 --minutes-to-count 30
  python fluid_calc.py synovial --shape needle --birefringence negative
  python fluid_calc.py tnc --cells 389 --squares 9 --sample-ul 20 --diluent-ul 80
  python fluid_calc.py eqa-check --reported 432 --low 1800 --high 2400 --df 5 --other A2=80-120 --other B2=700-1000
  python fluid_calc.py pd --wbc 240 --neut-pct 62
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


def dilution_factor(sample_ul=None, diluent_ul=None, df=None):
    """DF = total volume / sample volume. Volumes beat ratio strings ("1:9" is read two ways)."""
    if sample_ul is not None or diluent_ul is not None:
        if df is not None:
            raise ValueError("give --df OR --sample-ul/--diluent-ul, not both")
        if sample_ul is None or diluent_ul is None or sample_ul <= 0 or diluent_ul < 0:
            raise ValueError("give both --sample-ul (> 0) and --diluent-ul (>= 0)")
        return (sample_ul + diluent_ul) / sample_ul
    if df is None:
        return 1.0
    if df < 1:
        raise ValueError("DF must be >= 1 (undiluted = 1); %g looks like a fraction - use 1/%g" % (df, df))
    return float(df)


def tnc(cells, squares, dfactor=1.0, square_mm2=1.0, depth_mm=0.1):
    if cells < 0 or squares <= 0 or square_mm2 <= 0 or depth_mm <= 0:
        raise ValueError("cells must be >= 0; squares, area and depth must be > 0")
    volume_ul = squares * square_mm2 * depth_mm  # 1 mm3 = 1 uL
    per_ul = cells * dfactor / volume_ul
    return {"cells_counted": cells, "squares": squares, "volume_counted_uL": volume_ul, "DF": dfactor,
            "TNC_per_uL": per_ul,
            "formula": "%g cells x DF %g / (%g squares x %g mm2 x %g mm) = %g /uL"
                       % (cells, dfactor, squares, square_mm2, depth_mm, per_ul),
            "units": "cells/uL = cells/cu.mm = x10^6/L  (x10^9/L = /nL: divide by 1000)",
            "check": "write the number on the right sample ID before you report (swapped IDs: a top EQA failure)"}


# A miss is explained by a slip only when the slip lands it inside the assigned range.
def _slips(dfactor):
    s = [("x10 chamber slip (used 1 uL or 0.01 uL per square instead of 0.1 uL)", 10.0),
         ("x1000 unit slip (per mL vs per uL, or x10^9/L vs x10^6/L)", 1000.0)]
    if dfactor and dfactor > 1:
        s.insert(0, ("DF slip (forgot DF %g, or applied it twice)" % dfactor, dfactor))
    return s


def eqa_check(reported, low, high, dfactor=None, others=None, background_limit=None):
    if reported < 0 or low < 0 or low > high:
        raise ValueError("need reported >= 0 and 0 <= low <= high")
    res = {"reported": reported, "assigned": "%g - %g" % (low, high)}
    if low <= reported <= high:
        res["verdict"] = "IN RANGE"
        return res
    res["verdict"] = "OUT OF RANGE"
    causes = []
    if high == 0 and reported > 0:
        if background_limit is None:
            causes.append("assigned value is 0 cells: run the analyzer background first - a count within your "
                          "background/LoQ limit is background or carry-over (report < LoQ per SOP); above it, treat "
                          "it as real cells, contamination or a swapped tube (give --background-limit)")
        elif reported <= background_limit:
            causes.append("reported %g <= your background limit %g -> consistent with background / carry-over; "
                          "a count below LoQ cannot prove zero cells -> report < LoQ per SOP"
                          % (reported, background_limit))
        else:
            causes.append("reported %g > your background limit %g -> NOT explained by background: contamination, "
                          "carry-over from a high sample, or a swapped tube -> investigate before reporting"
                          % (reported, background_limit))
    for name, f in _slips(dfactor):
        for direction, val in (("too high", reported / f), ("too low", reported * f)):
            if low <= val <= high:
                causes.append("%s by x%g -> %s (corrected %g)" % (direction, f, name, val))
    for label, (olow, ohigh) in (others or {}).items():
        if olow <= reported <= ohigh:
            causes.append("fits sample %s's range %g - %g -> swapped sample numbers?" % (label, olow, ohigh))
    res["likely_causes"] = causes or ["no single classic slip explains it -> recount, recheck chamber fill, "
                                      "mixing, specimen age"]
    return res


def pd(wbc, neut_pct):
    if wbc < 0 or not 0 <= neut_pct <= 100:
        raise ValueError("need WBC >= 0 and neutrophils between 0 and 100%")
    high_wbc, high_neut = wbc > 100, neut_pct > 50
    if neut_pct == 50:
        result = ("INDETERMINATE - exactly 50% neutrophils is the boundary: ISPD 2022 requires > 50%, some SOPs "
                  "use >= 50% -> follow your SOP; Gram + culture if in doubt")
    elif high_wbc and high_neut:
        result = "PERITONITIS SUSPECTED (WBC > 100/uL AND neutrophils > 50%) -> Gram stain + culture now"
    elif high_neut:
        result = ("INDETERMINATE - neutrophils > 50% with WBC <= 100/uL: after a short dwell (APD) ISPD counts "
                  "PMN > 50% as strong evidence of peritonitis -> ask the dwell time, Gram + culture per SOP")
    else:
        result = ("effluent criterion not met - does NOT exclude peritonitis (ISPD: 2 of 3 = clinical features, "
                  "effluent count, positive culture)")
    res = {"wbc_per_uL": wbc, "neut_pct": neut_pct, "wbc_gt_100": high_wbc, "neut_gt_50": high_neut,
           "result": result}
    if neut_pct == 50:
        res["boundary"] = "exactly 50%: teaching material often writes >= 50%, ISPD 2022 uses > 50% -> follow your SOP"
    if high_wbc and neut_pct < 50:
        res["note"] = ("WBC > 100/uL with mononuclear predominance: think TB / fungal / non-infectious causes "
                       "-> culture per SOP")
    return res


def _parse_other(items):
    out = {}
    for it in items or []:
        label, _, rng = it.partition("=")
        lo, _, hi = rng.partition("-")
        if not label or not lo or not hi:
            raise ValueError("--other takes LABEL=LOW-HIGH, e.g. A2=80-120")
        out[label.strip()] = (float(lo), float(hi))
    return out


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
    p = sub.add_parser("tnc")
    p.add_argument("--cells", type=float, required=True, help="nucleated cells counted")
    p.add_argument("--squares", type=float, required=True, help="large squares counted (1 mm2 each)")
    p.add_argument("--sample-ul", type=float, help="sample volume in the dilution")
    p.add_argument("--diluent-ul", type=float, help="diluent volume added")
    p.add_argument("--df", type=float, help="dilution factor if you already know it (undiluted = 1)")
    p.add_argument("--square-mm2", type=float, default=1.0)
    p.add_argument("--depth-mm", type=float, default=0.1)
    p = sub.add_parser("eqa-check")
    p.add_argument("--reported", type=float, required=True)
    p.add_argument("--low", type=float, required=True, help="assigned range low")
    p.add_argument("--high", type=float, required=True, help="assigned range high")
    p.add_argument("--df", type=float, help="the DF you used (lets it test a DF slip)")
    p.add_argument("--other", action="append", help="other sample in the round: LABEL=LOW-HIGH (repeatable)")
    p.add_argument("--background-limit", type=float, help="your analyzer's background / LoQ limit")
    p = sub.add_parser("pd")
    p.add_argument("--wbc", type=float, required=True, help="effluent WBC /uL")
    p.add_argument("--neut-pct", type=float, required=True, help="neutrophils %% of TNCC")
    for _sp in sub.choices.values():  # also accept --json after the subcommand, as the examples show
        _sp.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="print JSON")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "lights":
            res = lights(a.fluid_protein, a.serum_protein, a.fluid_ldh, a.serum_ldh, a.ldh_uln, a.fluid)
        elif a.cmd == "csf":
            res = csf(a.tube1_rbc, a.tube3_rbc, a.minutes_to_count, a.csf_glucose, a.serum_glucose, a.ratio_low)
        elif a.cmd == "synovial":
            res = synovial(a.shape, a.birefringence)
        elif a.cmd == "tnc":
            res = tnc(a.cells, a.squares, dilution_factor(a.sample_ul, a.diluent_ul, a.df), a.square_mm2, a.depth_mm)
        elif a.cmd == "eqa-check":
            res = eqa_check(a.reported, a.low, a.high, a.df, _parse_other(a.other), a.background_limit)
        else:
            res = pd(a.wbc, a.neut_pct)
    except ValueError as e:
        ap.error(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        for k, v in res.items():
            if k == "criteria":
                print("%-34s %-9s %-9s %s" % ("criterion", "value", "limit", "met"))
                for c in v:
                    print("%-34s %-9.3f %-9.3f %s" % (c["criterion"], c["value"], c["limit"], c["met"]))
            elif isinstance(v, list):
                print(k)
                for item in v:
                    print("  - %s" % item)
            else:
                print("%-16s %s" % (k, ("%.3f" % v) if isinstance(v, float) else v))
        print("ADVISORY: decision support only - correlate clinically; confirm with the lab SOP and MT/physician.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
