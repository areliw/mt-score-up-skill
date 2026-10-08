#!/usr/bin/env python3
"""bb_calc - blood bank arithmetic: antigen-negative units to screen, and RhIG vials from a fetal bleed.

Black-box tool for bloodbank-judgment. Run --help first; read the source only if a result looks wrong.
Formulas come from the owner's course digests:
  units  512304 Transfusion Science 2 digest §3: units to crossmatch = units requested /
         product(frequency of each antigen-negative phenotype); worked example 3/(0.7 x 0.25) = 17.
         512303 Transfusion Science 1 digest §1.4: Fy(a-) 0.32 x Jk(b-) 0.26 x K- 0.91 = 0.076 ~ 8%
         -> (100/8) x 2 ~ 25 units (the digest rounds 7.6% to 8% first; exact = 26.4).
         Frequencies depend on the population (512303 §1.4 has Thai columns) -> you must pass them.
  rhig   512303 digest §3.3: Kleihauer-Betke quantifies the fetal bleed; 1 vial = 300 ug = 1,500 IU
         covers ~30 mL fetal whole blood; round the vial count (>= .5 up) and add 1 vial.
         card bloodbank-judgment Fork 8: standard 300 ug covers only ~30 mL whole blood / 15 mL RBC -
         a large FMH needs KB/flow and a calculated dose.
         % fetal cells -> mL needs the maternal blood volume your protocol uses: pass it, there is no default.
ADVISORY ONLY. Dose and unit selection are decided per SOP by an authorised signatory / physician.

Examples
  python bb_calc.py units --requested 3 --neg-freq E=0.70 --neg-freq Jka=0.25
  python bb_calc.py rhig --kb-pct 1.5 --maternal-bv-ml 5000
  python bb_calc.py rhig --fmh-ml 75
  python bb_calc.py rhig --fmh-rbc-ml 20 --json
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

ADVISORY = "ADVISORY: decision support only - confirm with the blood bank SOP and an authorised signatory/physician."


def units_to_screen(requested, neg_freqs):
    """neg_freqs: {antigen: frequency of the antigen-NEGATIVE phenotype, 0 < f <= 1}."""
    if requested <= 0:
        raise ValueError("requested units must be > 0")
    if not neg_freqs:
        raise ValueError("give at least one --neg-freq ANTIGEN=fraction")
    p = 1.0
    for ag, f in neg_freqs.items():
        if not 0 < f <= 1:
            raise ValueError("frequency for %s must be a fraction in (0, 1], got %s" % (ag, f))
        p *= f
    expected = requested / p
    return {"requested": requested, "neg_freqs": neg_freqs, "compatible_fraction": p,
            "compatible_pct": p * 100, "units_expected": expected, "units_to_screen": math.ceil(expected - 1e-9),
            "formula": "units = requested / product(antigen-negative frequency)  (512304 §3)",
            "note": "an average, not a guarantee; real stock may be short -> rare antigen / not enough units = "
                    "ref lab / rare donor registry (card Fork 2)"}


def round_half_up(x):
    return int(math.floor(x + 0.5))


def rhig_vials(fmh_ml, ml_per_vial=30.0, extra_vials=1):
    """fmh_ml = fetal WHOLE BLOOD volume. 512303 §3.3: vials = round(fmh/30, .5 up) + 1."""
    if fmh_ml < 0:
        raise ValueError("fetal bleed volume cannot be negative")
    if ml_per_vial <= 0:
        raise ValueError("--ml-per-vial must be > 0")
    raw = fmh_ml / ml_per_vial
    rounded = round_half_up(raw)
    return {"fmh_whole_blood_ml": fmh_ml, "ml_per_vial": ml_per_vial, "raw_vials": raw,
            "rounded_vials": rounded, "extra_vials": extra_vials, "vials": rounded + extra_vials,
            "formula": "vials = round(FMH mL whole blood / %g, .5 up) + %d  (512303 §3.3)" % (ml_per_vial, extra_vials)}


def fmh_from_kb(kb_pct, maternal_bv_ml):
    if not 0 <= kb_pct <= 100:
        raise ValueError("--kb-pct is a percentage of fetal cells (0-100)")
    if maternal_bv_ml <= 0:
        raise ValueError("--maternal-bv-ml must be > 0")
    return kb_pct / 100.0 * maternal_bv_ml


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    u = sub.add_parser("units", help="antigen-negative units to screen")
    u.add_argument("--requested", type=float, required=True)
    u.add_argument("--neg-freq", action="append", default=[], metavar="ANTIGEN=FRACTION",
                   help="frequency of the antigen-NEGATIVE phenotype in YOUR donor population, e.g. Jka=0.25")
    r = sub.add_parser("rhig", help="RhIG vials from a quantified fetal bleed")
    g = r.add_mutually_exclusive_group(required=True)
    g.add_argument("--fmh-ml", type=float, help="fetal bleed as mL of fetal WHOLE BLOOD")
    g.add_argument("--fmh-rbc-ml", type=float, help="fetal bleed as mL of fetal RED CELLS (x2 -> whole blood; card Fork 8: 30 mL WB = 15 mL RBC)")
    g.add_argument("--kb-pct", type=float, help="Kleihauer-Betke %% fetal cells (needs --maternal-bv-ml)")
    r.add_argument("--maternal-bv-ml", type=float, help="maternal blood volume your protocol uses (no default)")
    r.add_argument("--ml-per-vial", type=float, default=30.0,
                   help="mL fetal whole blood covered by one vial (default 30 for 300 ug, 512303 §3.3; check product insert)")
    r.add_argument("--extra-vials", type=int, default=1, help="safety vials added after rounding (default 1, 512303 §3.3)")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "units":
            freqs = {}
            for item in a.neg_freq:
                if "=" not in item:
                    raise ValueError("--neg-freq needs ANTIGEN=FRACTION, got %r" % item)
                k, v = item.split("=", 1)
                freqs[k.strip()] = float(v)
            res = units_to_screen(a.requested, freqs)
        else:
            if a.kb_pct is not None:
                if a.maternal_bv_ml is None:
                    raise ValueError("--kb-pct needs --maternal-bv-ml (the blood volume your protocol uses)")
                fmh, src = fmh_from_kb(a.kb_pct, a.maternal_bv_ml), "KB %g%% x %g mL" % (a.kb_pct, a.maternal_bv_ml)
            elif a.fmh_rbc_ml is not None:
                fmh, src = a.fmh_rbc_ml * 2, "%g mL fetal RBC x 2" % a.fmh_rbc_ml
            else:
                fmh, src = a.fmh_ml, "given"
            res = rhig_vials(fmh, a.ml_per_vial, a.extra_vials)
            res["fmh_source"] = src
    except ValueError as e:
        ap.error(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "units":
        print("antigen-negative frequencies : %s" % ", ".join("%s-neg %.3f" % kv for kv in res["neg_freqs"].items()))
        print("compatible fraction          : %.4f (%.2f%%)" % (res["compatible_fraction"], res["compatible_pct"]))
        print("units expected to screen     : %.2f  -> screen at least %d for %g compatible unit(s)" %
              (res["units_expected"], res["units_to_screen"], res["requested"]))
        print("formula                      : %s" % res["formula"])
        print("note                         : %s" % res["note"])
    else:
        print("fetal bleed (whole blood)    : %.1f mL  [%s]" % (res["fmh_whole_blood_ml"], res["fmh_source"]))
        print("raw vials (/ %g mL)          : %.3f" % (res["ml_per_vial"], res["raw_vials"]))
        print("rounded (.5 up)              : %d" % res["rounded_vials"])
        print("+ safety vial(s)             : %d" % res["extra_vials"])
        print("VIALS                        : %d" % res["vials"])
        print("formula                      : %s" % res["formula"])
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
