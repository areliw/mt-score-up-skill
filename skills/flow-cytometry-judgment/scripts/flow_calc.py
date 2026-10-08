#!/usr/bin/env python3
"""flow_calc - absolute counts (CD4 / lymphocyte subsets) and MRD limit of detection.

Black-box tool for flow-cytometry-judgment Fork 4 (CD4 monitoring, lymphocyte subsets, MRD). Run --help.
ADVISORY ONLY: counts and sensitivities depend on a clean gate (run gating_check.py first), the lab's
validated method, and physician interpretation.

  abs-dual   dual-platform: absolute = WBC x lymph% / 100 x subset% / 100
             (subset% = % of LYMPHOCYTES from flow; WBC + lymph% from the hematology analyzer)
             absolute count = %diff x WBC / 100 (501 digest §2); dual- vs single-platform (immunodiagnostic digest §5.5)
  abs-bead   single-platform beads: absolute = (cell events / bead events) x (beads per tube / sample volume uL)
             (immunodiagnostic digest §5.5 "beads count absolute in one instrument";
              formula: standard bead-based absolute counting as in bead-tube package inserts)
             optional --threshold: e.g. 200 cells/uL for CD4 (immunodiagnostic digest §5.5: CD4 < 200 defines AIDS)
  mrd-lod    limit of detection = minimum cluster events / evaluable events
             events needed for a claimed sensitivity = minimum cluster / claimed fraction
             card Fork 4: "MRD must acquire many events, else a small clone is falsely negative".
             --min-cluster has NO default: it is the cluster size your lab validated.
             Evaluable events = viable nucleated singlets in the analysed gate, NOT raw acquired events.

Examples
  python flow_calc.py abs-dual --wbc 6000 --lymph-pct 30 --subset-pct 25 --threshold 200
  python flow_calc.py abs-bead --cell-events 5000 --bead-events 10000 --beads-per-tube 50000 --volume-ul 50
  python flow_calc.py mrd-lod --events 100000 --min-cluster 20 --claim 1e-4
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

ADVISORY = ("ADVISORY: decision support only - confirm with the lab's validated method/SOP; interpretation "
            "and diagnosis belong to the physician.")


def _threshold(res, value, threshold):
    if threshold is not None:
        res["threshold"] = threshold
        res["below_threshold"] = value < threshold
    return res


def abs_dual(wbc, lymph_pct, subset_pct, threshold=None):
    for name, v in (("lymph_pct", lymph_pct), ("subset_pct", subset_pct)):
        if not 0 <= v <= 100:
            raise ValueError("%s must be 0-100" % name)
    alc = wbc * lymph_pct / 100
    absolute = alc * subset_pct / 100
    res = {"inputs": {"wbc_per_ul": wbc, "lymph_pct": lymph_pct, "subset_pct_of_lymph": subset_pct},
           "abs_lymphocytes_per_ul": alc, "abs_subset_per_ul": absolute,
           "formula": "WBC x lymph%/100 x subset%/100",
           "note": "dual-platform: errors of both instruments add up; WBC and flow tube must be the same sample"}
    return _threshold(res, absolute, threshold)


def abs_bead(cell_events, bead_events, beads_per_tube, volume_ul, threshold=None):
    if bead_events <= 0 or volume_ul <= 0:
        raise ValueError("bead events and volume must be > 0")
    absolute = cell_events / bead_events * beads_per_tube / volume_ul
    res = {"inputs": {"cell_events": cell_events, "bead_events": bead_events,
                      "beads_per_tube": beads_per_tube, "volume_ul": volume_ul},
           "abs_per_ul": absolute,
           "formula": "(cell events / bead events) x (beads per tube / volume uL)",
           "note": "beads per tube comes from the lot's certificate; pipette volume errors scale the result 1:1"}
    return _threshold(res, absolute, threshold)


def mrd_lod(events, min_cluster, claim=None):
    if events <= 0 or min_cluster <= 0:
        raise ValueError("events and --min-cluster must be > 0")
    lod = min_cluster / events
    res = {"inputs": {"evaluable_events": events, "min_cluster": min_cluster},
           "lod_fraction": lod, "lod_percent": lod * 100,
           "lod_one_in": events / min_cluster}
    if claim is not None:
        if not 0 < claim < 1:
            raise ValueError("--claim is a fraction, e.g. 1e-4 for 0.01%")
        needed = math.ceil(min_cluster / claim - 1e-9)
        res["claim_fraction"] = claim
        res["events_needed_for_claim"] = needed
        res["claim_supported"] = lod <= claim
        res["verdict"] = ("SUPPORTED: a negative result can be reported at %g" % claim if lod <= claim else
                          "NOT SUPPORTED: only %d evaluable events; need >= %d for %g -> report the achieved "
                          "LOD (%.2g), not 'MRD negative at %g' (false-negative risk)"
                          % (events, needed, claim, lod, claim))
    return res


def _print(res):
    for k, v in res.items():
        print("%-26s %s" % (k, ("%.6g" % v) if isinstance(v, float) else v))
    print(ADVISORY)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("abs-dual", help="dual-platform absolute count")
    p.add_argument("--wbc", type=float, required=True, help="WBC per uL from the hematology analyzer")
    p.add_argument("--lymph-pct", type=float, required=True, help="lymphocyte %% of WBC")
    p.add_argument("--subset-pct", type=float, required=True, help="subset %% of lymphocytes (flow)")
    p.add_argument("--threshold", type=float, help="flag if below, e.g. 200 for CD4")
    p = sub.add_parser("abs-bead", help="single-platform bead absolute count")
    p.add_argument("--cell-events", type=float, required=True)
    p.add_argument("--bead-events", type=float, required=True)
    p.add_argument("--beads-per-tube", type=float, required=True, help="from the bead lot certificate")
    p.add_argument("--volume-ul", type=float, required=True, help="sample volume pipetted into the tube")
    p.add_argument("--threshold", type=float, help="flag if below, e.g. 200 for CD4")
    p = sub.add_parser("mrd-lod", help="MRD limit of detection / events needed")
    p.add_argument("--events", type=float, required=True, help="evaluable (viable nucleated singlet) events")
    p.add_argument("--min-cluster", type=float, required=True, help="lab-validated minimum cluster size")
    p.add_argument("--claim", type=float, help="sensitivity to be reported, as a fraction (1e-4 = 0.01%%)")
    for _sp in sub.choices.values():  # also accept --json after the subcommand, as the examples show
        _sp.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="print JSON")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "abs-dual":
            res = abs_dual(a.wbc, a.lymph_pct, a.subset_pct, a.threshold)
        elif a.cmd == "abs-bead":
            res = abs_bead(a.cell_events, a.bead_events, a.beads_per_tube, a.volume_ul, a.threshold)
        else:
            res = mrd_lod(a.events, a.min_cluster, a.claim)
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
