#!/usr/bin/env python3
"""parasite_calc - checkable parasitology arithmetic: malaria density, Kato EPG, micrometry.

Black-box tool for parasitology-judgment. Run --help first; read the source only if a result looks
wrong. Source = 317331 Parasitology digest (owner's course notes). ADVISORY ONLY.

Subcommands
  density     thick-film parasite density /uL = parasites counted x WBC per uL / WBC counted
              (317331 digest Part 2 Lab Dx: "parasites/200 WBC x 8,000 = /uL; above 40,000/uL
              count WBC per 500 parasites"; card FORK 3). WBC/uL is an INPUT: 8,000 is the
              digest's assumed value - the tool labels which one you used. --switch-above makes
              it remind you of the high-density counting rule.
  epg         Kato thick smear eggs per gram = eggs x 1000 / stool mass on the smear (mg)
              (317331 §5.2: Kato = quantitative EPG survey; card FORK 1: counts, cannot speciate).
              Template mass is an input (it differs by template).
  calibrate   ocular-micrometer factor: um per ocular division = stage divisions x um per stage
              division / ocular divisions (317331 §5.3: stage micrometer 0.01 mm = 10 um/div)
  measure     object size = ocular divisions x um/div AT THAT OBJECTIVE (317331 §5.3), then
              which candidate size ranges fit (data/oocyst_sizes_teaching.json: Crypto 4-6 um vs
              Cyclospora 8-10 um, 317331 high-yield #8). No fit -> think artifact (card trap).

Examples (run from the skill folder)
  python scripts/parasite_calc.py density --parasites 50 --wbc-counted 200 --wbc-per-ul 8000 --switch-above 40000
  python scripts/parasite_calc.py epg --eggs 10 --smear-mg 41.7
  python scripts/parasite_calc.py calibrate --stage-div 10 --ocular-div 39
  python scripts/parasite_calc.py measure --ocular-div 2 --objective 40x --cal 40x=2.56 --cal 10x=9.9 --candidates data/oocyst_sizes_teaching.json
"""
import argparse
import json
import sys

ADVISORY = "ADVISORY: decision support only - confirm with the lab SOP and the responsible MT before reporting."


def density(parasites, wbc_counted, wbc_per_ul, switch_above=None):
    """parasites/uL = parasites x WBC/uL / WBC counted (317331 digest, Lab Dx)."""
    if wbc_counted <= 0 or wbc_per_ul <= 0 or parasites < 0:
        raise ValueError("need parasites >= 0, wbc_counted > 0, wbc_per_ul > 0")
    d = parasites * wbc_per_ul / wbc_counted
    flags = []
    if switch_above is not None and d > switch_above:
        flags.append("density %.0f/uL > %g: the digest switches to counting WBC per 500 parasites "
                     "(count parasites to 500, then put the WBC tally in --wbc-counted)" % (d, switch_above))
    return {"parasites": parasites, "wbc_counted": wbc_counted, "wbc_per_ul": wbc_per_ul,
            "density_per_ul": d, "flags": flags}


def epg(eggs, smear_mg, smears=1):
    """eggs per gram = eggs x 1000 / (mg per smear x smears)."""
    if smear_mg <= 0 or smears < 1 or eggs < 0:
        raise ValueError("need eggs >= 0, smear_mg > 0, smears >= 1")
    return {"eggs": eggs, "smear_mg": smear_mg, "smears": smears, "factor": 1000.0 / smear_mg,
            "epg": eggs * 1000.0 / (smear_mg * smears)}


def calibrate(stage_div, ocular_div, um_per_stage_div=10.0):
    """um per ocular division = stage divisions x um/stage division / ocular divisions."""
    if stage_div <= 0 or ocular_div <= 0:
        raise ValueError("divisions must be > 0")
    return stage_div * um_per_stage_div / ocular_div


def um_per_div(cal, objective):
    """The factor must belong to the objective used for the measurement (317331 §5.3)."""
    if objective not in cal:
        raise KeyError("no calibration for objective %r (have: %s) - calibrate it; never reuse another "
                       "objective's factor" % (objective, ", ".join(sorted(cal))))
    return cal[objective]


def measure(ocular_div, objective, cal, candidates=None):
    f = um_per_div(cal, objective)
    size = ocular_div * f
    fits = [c["name"] for c in (candidates or []) if c["min_um"] <= size <= c["max_um"]]
    return {"ocular_div": ocular_div, "objective": objective, "um_per_div": f, "size_um": size, "fits": fits}


def parse_cal(specs):
    cal = {}
    for s in specs or []:
        if "=" not in s:
            raise ValueError("--cal must be OBJECTIVE=UM_PER_DIV, got %r" % s)
        k, v = s.split("=", 1)
        cal[k.strip()] = float(v)
    return cal


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("density", help="thick-film malaria parasite density")
    p.add_argument("--parasites", type=float, required=True)
    p.add_argument("--wbc-counted", type=float, required=True, help="WBC tallied alongside (digest: 200)")
    p.add_argument("--wbc-per-ul", type=float, required=True, help="WBC/uL used (digest assumes 8000)")
    p.add_argument("--switch-above", type=float, help="density above which your SOP changes counting method")
    p = sub.add_parser("epg", help="Kato thick smear eggs per gram")
    p.add_argument("--eggs", type=float, required=True)
    p.add_argument("--smear-mg", type=float, required=True, help="stool mass per smear (template), mg")
    p.add_argument("--smears", type=int, default=1, help="number of smears the eggs were counted on")
    p = sub.add_parser("calibrate", help="ocular micrometer factor from a stage micrometer")
    p.add_argument("--stage-div", type=float, required=True)
    p.add_argument("--ocular-div", type=float, required=True)
    p.add_argument("--um-per-stage-div", type=float, default=10.0, help="stage micrometer: 0.01 mm = 10 um/div")
    p = sub.add_parser("measure", help="size an object and match candidate ranges")
    p.add_argument("--ocular-div", type=float, required=True)
    p.add_argument("--objective", required=True, help="objective used for THIS measurement, e.g. 40x")
    p.add_argument("--cal", action="append", required=True, help="OBJECTIVE=UM_PER_DIV, repeat per objective")
    p.add_argument("--candidates", help="JSON list of {name, min_um, max_um}")
    a = ap.parse_args(argv)

    if a.cmd == "density":
        res = density(a.parasites, a.wbc_counted, a.wbc_per_ul, a.switch_above)
        lines = ["parasites %g / WBC %g x WBC/uL %g = %.1f parasites/uL" % (a.parasites, a.wbc_counted,
                                                                            a.wbc_per_ul, res["density_per_ul"]),
                 "WBC/uL used: %g%s" % (a.wbc_per_ul, " (the digest's assumed 8,000 - state it on the report)"
                                        if a.wbc_per_ul == 8000 else " (supplied)")] + ["FLAG: " + f for f in res["flags"]]
    elif a.cmd == "epg":
        res = epg(a.eggs, a.smear_mg, a.smears)
        lines = ["eggs %g x 1000 / (%g mg x %d smear) = %.1f EPG  (factor %.2f per smear)"
                 % (a.eggs, a.smear_mg, a.smears, res["epg"], res["factor"]),
                 "NOTE: Kato counts eggs; it cannot tell species apart (card FORK 1)."]
    elif a.cmd == "calibrate":
        f = calibrate(a.stage_div, a.ocular_div, a.um_per_stage_div)
        res = {"um_per_ocular_div": f}
        lines = ["%g stage div x %g um / %g ocular div = %.3f um per ocular division (valid ONLY for the objective "
                 "it was measured on)" % (a.stage_div, a.um_per_stage_div, a.ocular_div, f)]
    else:
        cands = []
        if a.candidates:
            with open(a.candidates, encoding="utf-8") as fh:
                cands = json.load(fh)["candidates"]
        try:
            res = measure(a.ocular_div, a.objective, parse_cal(a.cal), cands)
        except KeyError as e:
            raise SystemExit("ERROR: %s" % e.args[0])
        lines = ["%g ocular div x %.3f um/div (%s) = %.2f um" % (a.ocular_div, res["um_per_div"], a.objective,
                                                                 res["size_um"])]
        if cands:
            lines.append("fits: %s" % (", ".join(res["fits"]) if res["fits"] else
                                       "NONE -> re-measure, check stain/structure; consider artifact (card trap)"))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    for ln in lines:
        print(ln)
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
