#!/usr/bin/env python3
"""cbc_calc - checkable CBC arithmetic for hematology-judgment.

Black-box tool: run --help, not the source. ADVISORY ONLY. A normal number is not a normal smear
(card trap #1): every result that changes treatment still needs a smear review and an MT/physician sign-off.

Subcommands and where each formula / cut-off comes from (owner's course digests):
  indices   MCV = Hct% x 10 / RBC   MCH = Hb x 10 / RBC   MCHC = Hb x 100 / Hct%   (503402 digest §1 formula table)
            MCV class <80 micro / 80-100 normo / >100 macro    (503402 §2, 501 digest §4, card Fork 2)
            thal screen: MCV <80 fL or MCH <27 pg               (503402 §4A(2), automated values only)
            MCHC flag: > 36 g/dL -> review smear (artifact vs spherocytosis)   (card Fork 1 ">36-37"; 503402 §1)
            Mentzer index = MCV / RBC: <13 thal-like, >13 IDA-like. A CLUE, not a diagnosis (503402 §2, card Fork 5)
  retic     corrected retic = %retic x Hct / 45
            RPI = corrected retic / maturation days; days from Hct (503402 §1):
              (35,45] -> 1.5   (25,35] -> 2.0   (15,25] -> 2.5   <=15 -> 3.0
              (digest bands 36-45 / 26-35 / 16-25 / <15 read as half-open intervals;
               Hct > 45 is outside the digest table -> pass --maturation-days yourself)
            RPI >= 2 hyperproliferative, < 2 hypoproliferative  (503402 §1, card Fork 2)
  nrbc-wbc  corrected WBC = WBC x 100 / (100 + NRBC per 100 WBC)
            (503402 §3 "NRBC high -> WBC falsely high, must correct"; formula: standard hematology texts, e.g. Rodak's)
  lap       Kaplow LAP score = sum(grade x cells) over 100 neutrophils, grades 0-4
            <20 low (CML-like) · 20-100 normal · >100 high (leukemoid-like)   (503402 §5, 510403 §3.9, card Fork 3)

All cut-offs above are TEACHING defaults from the digests and can be overridden by flags.
Units: Hb g/dL, Hct %, RBC x10^6/uL, WBC any count unit (output keeps the unit).

Examples
  python cbc_calc.py indices --hb 11.2 --hct 35 --rbc 5.6
  python cbc_calc.py retic --retic-pct 6 --hct 25
  python cbc_calc.py nrbc-wbc --wbc 15000 --nrbc 25
  python cbc_calc.py lap --counts 90 8 2 0 0
  python cbc_calc.py --json indices --hb 11.2 --hct 35 --rbc 5.6
"""
import argparse
import json
import sys

ADVISORY = ("ADVISORY: decision support only - review the smear and confirm with the lab SOP "
            "and the responsible MT/physician before reporting.")


# ---------------------------------------------------------------- indices (503402 §1-§2, §4A)
def indices(hb, hct, rbc, mcv_low=80.0, mcv_high=100.0, mch_screen=27.0, mchc_flag=36.0, mentzer_cut=13.0):
    if hct <= 1.5:
        raise ValueError("Hct must be in %% (e.g. 35), not a fraction (%.3f)" % hct)
    if rbc <= 0 or hb <= 0:
        raise ValueError("Hb and RBC must be > 0")
    mcv = hct * 10 / rbc
    mch = hb * 10 / rbc
    mchc = hb * 100 / hct
    if mcv < mcv_low:
        mcv_class = "microcytic (MCV < %g): IDA / thal / chronic dz / sideroblastic -> ferritin; OFT/DCIP -> Hb typing" % mcv_low
    elif mcv > mcv_high:
        mcv_class = "macrocytic (MCV > %g): check retic FIRST (retic high = pseudo-macro from hemolysis), then B12/folate + smear" % mcv_high
    else:
        mcv_class = "normocytic (%g-%g): check retic / RPI first" % (mcv_low, mcv_high)
    thal_screen = (mcv < mcv_low) or (mch < mch_screen)
    mentzer = mcv / rbc
    if mentzer < mentzer_cut:
        mentzer_read = "< %g -> thal-like (high RBC count)" % mentzer_cut
    elif mentzer > mentzer_cut:
        mentzer_read = "> %g -> IDA-like" % mentzer_cut
    else:
        mentzer_read = "= %g -> borderline, no lean" % mentzer_cut
    flags = []
    if mchc > mchc_flag:
        flags.append("MCHC %.1f > %g -> review smear: artifact (cold agglutinin -> warm 37C 30 min and rerun; "
                     "lipemia; hyperbilirubinemia; paraprotein) vs TRUE high MCHC (hereditary spherocytosis)"
                     % (mchc, mchc_flag))
    if mcv < mcv_low:
        flags.append("Mentzer is a clue only: confirm with ferritin / HbA2. IDA lowers HbA2 -> correct iron first "
                     "or a beta-thal trait can be missed (card Fork 5)")
    return {"inputs": {"hb_g_dl": hb, "hct_pct": hct, "rbc_1e6_ul": rbc},
            "mcv_fl": mcv, "mch_pg": mch, "mchc_g_dl": mchc,
            "mcv_class": mcv_class,
            "thal_screen_positive": thal_screen,
            "thal_screen_rule": "MCV < %g or MCH < %g" % (mcv_low, mch_screen),
            "mentzer": mentzer, "mentzer_read": mentzer_read,
            "flags": flags}


# ---------------------------------------------------------------- retic / RPI (503402 §1)
def maturation_days(hct):
    """503402 digest §1 table, read as half-open intervals. Hct > 45 is outside the table."""
    if hct > 45:
        raise ValueError("Hct %.1f > 45 is outside the digest maturation table; pass --maturation-days" % hct)
    if hct > 35:
        return 1.5
    if hct > 25:
        return 2.0
    if hct > 15:
        return 2.5
    return 3.0


def retic(retic_pct, hct, normal_hct=45.0, rpi_cut=2.0, mat_days=None):
    if hct <= 1.5:
        raise ValueError("Hct must be in % (e.g. 25), not a fraction")
    corrected = retic_pct * hct / normal_hct
    days = mat_days if mat_days is not None else maturation_days(hct)
    rpi = corrected / days
    if rpi >= rpi_cut:
        verdict = ("RPI %.2f >= %g -> hyperproliferative (hemolysis / acute blood loss / treated deficiency) "
                   "-> reflex hemolysis panel: LDH, bilirubin, haptoglobin, DAT" % (rpi, rpi_cut))
    else:
        verdict = ("RPI %.2f < %g -> hypoproliferative (chronic dz / CKD / aplastic / early IDA / B12-folate)"
                   % (rpi, rpi_cut))
    note = ""
    if retic_pct >= rpi_cut and rpi < rpi_cut:
        note = ("raw retic %g%% looks high, but after the anemia (Hct) and shift (maturation) corrections "
                "the marrow response is NOT adequate - do not call hemolysis from the raw %%" % retic_pct)
    return {"inputs": {"retic_pct": retic_pct, "hct_pct": hct, "normal_hct": normal_hct},
            "corrected_retic_pct": corrected, "maturation_days": days,
            "maturation_source": "--maturation-days" if mat_days is not None else "503402 digest §1 table",
            "rpi": rpi, "verdict": verdict, "note": note}


# ---------------------------------------------------------------- NRBC-corrected WBC (503402 §3)
def nrbc_wbc(wbc, nrbc_per_100):
    if nrbc_per_100 < 0 or wbc < 0:
        raise ValueError("WBC and NRBC must be >= 0")
    corrected = wbc * 100 / (100 + nrbc_per_100)
    return {"inputs": {"wbc_uncorrected": wbc, "nrbc_per_100_wbc": nrbc_per_100},
            "wbc_corrected": corrected,
            "formula": "WBC x 100 / (100 + NRBC)",
            "note": "report the corrected WBC and the NRBC/100 WBC; check the smear (cryoglobulin also inflates WBC)"}


# ---------------------------------------------------------------- LAP score (503402 §5, 510403 §3.9)
def lap(counts, low=20.0, high=100.0):
    if len(counts) != 5 or any(c < 0 for c in counts):
        raise ValueError("give 5 non-negative counts: neutrophils graded 0, 1, 2, 3, 4")
    total = sum(counts)
    if total == 0:
        raise ValueError("no cells counted")
    raw = sum(g * n for g, n in enumerate(counts))
    score = raw * 100 / total
    note = "" if total == 100 else ("counted %d cells, not 100: score scaled to per-100 (Kaplow counts 100)" % total)
    if score < low:
        read = "LOW (< %g): favours CML over leukemoid reaction - confirm BCR-ABL1 (t(9;22))" % low
    elif score > high:
        read = "HIGH (> %g): favours leukemoid reaction (toxic granules, left shift) over CML" % high
    else:
        read = "NORMAL (%g-%g): does not separate CML from leukemoid on its own" % (low, high)
    return {"inputs": {"counts_grade0_to_4": counts, "cells": total},
            "score": score, "read": read, "note": note}


# ---------------------------------------------------------------- CLI
def _print(res):
    for k, v in res.items():
        if isinstance(v, float):
            v = "%.4f" % v
        elif isinstance(v, list):
            if not v:
                continue
            v = "\n" + "\n".join("    - " + str(x) for x in v)
        elif v == "":
            continue
        print("%-22s %s" % (k, v))
    print(ADVISORY)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("indices", help="MCV/MCH/MCHC + class + thal screen + Mentzer")
    p.add_argument("--hb", type=float, required=True, help="g/dL")
    p.add_argument("--hct", type=float, required=True, help="%%")
    p.add_argument("--rbc", type=float, required=True, help="x10^6/uL")
    p.add_argument("--mcv-low", type=float, default=80.0, help="teaching default 80 (503402 §2)")
    p.add_argument("--mcv-high", type=float, default=100.0, help="teaching default 100 (503402 §2)")
    p.add_argument("--mch-screen", type=float, default=27.0, help="teaching default 27 (503402 §4A)")
    p.add_argument("--mchc-flag", type=float, default=36.0, help="teaching default 36 (card Fork 1)")

    p = sub.add_parser("retic", help="corrected retic + RPI")
    p.add_argument("--retic-pct", type=float, required=True)
    p.add_argument("--hct", type=float, required=True, help="%%")
    p.add_argument("--normal-hct", type=float, default=45.0, help="teaching default 45 (503402 §1)")
    p.add_argument("--rpi-cut", type=float, default=2.0, help="teaching default 2 (503402 §1)")
    p.add_argument("--maturation-days", type=float, help="override the digest table (required if Hct > 45)")

    p = sub.add_parser("nrbc-wbc", help="WBC corrected for NRBC")
    p.add_argument("--wbc", type=float, required=True)
    p.add_argument("--nrbc", type=float, required=True, help="NRBC per 100 WBC counted")

    p = sub.add_parser("lap", help="Kaplow LAP score")
    p.add_argument("--counts", type=int, nargs=5, required=True, metavar="N",
                   help="neutrophils graded 0 1 2 3 4 (usually totalling 100)")
    p.add_argument("--low", type=float, default=20.0, help="teaching default 20 (503402 §5)")
    p.add_argument("--high", type=float, default=100.0, help="teaching default 100 (503402 §5)")

    a = ap.parse_args(argv)
    try:
        if a.cmd == "indices":
            res = indices(a.hb, a.hct, a.rbc, a.mcv_low, a.mcv_high, a.mch_screen, a.mchc_flag)
        elif a.cmd == "retic":
            res = retic(a.retic_pct, a.hct, a.normal_hct, a.rpi_cut, a.maturation_days)
        elif a.cmd == "nrbc-wbc":
            res = nrbc_wbc(a.wbc, a.nrbc)
        else:
            res = lap(a.counts, a.low, a.high)
    except ValueError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        res["advisory"] = ADVISORY
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        _print(res)
    return 0


if __name__ == "__main__":
    sys.exit(main())
