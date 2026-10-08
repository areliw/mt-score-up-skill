#!/usr/bin/env python3
"""platelet_check - "is this low platelet count real or pseudo?" arithmetic (hematology-judgment Fork 4).

Black-box tool: run --help, not the source. ADVISORY ONLY: never auto-report a low platelet count
from the analyzer without looking at the smear (card Fork 4); critical lows go to the physician per SOP.

  estimate  smear estimate = mean platelets per oil-immersion field (monolayer) x lab-validated factor
            (card Fork 4 step 2: "x factor ที่แล็บ validate, ทั่วไป ~15-20k" -> --factor is REQUIRED, no default)
            per-field band: <5 decreased · 5-25 adequate · >25 increased   (501 digest §2, teaching values)
            optional cross-check against the analyzer count with a lab tolerance (--tolerance-pct, from SOP)
            analyzer << smear -> suspect clump / partial clot (card Fork 4 steps 0-1)
            analyzer >> smear -> suspect fragments / microcytes counted as platelets (501 digest judgment fork 7)
  citrate   count from a re-collected citrate tube x dilution factor (blood + anticoagulant) / blood
            teaching default 9 parts blood : 1 part 3.2% citrate -> x 10/9   (503402 digest §6, §10; card Fork 4 step 3)

Examples
  python platelet_check.py estimate --fields 9 11 10 8 12 10 9 11 10 10 --factor 15000
  python platelet_check.py estimate --fields 9 11 10 8 12 10 9 11 10 10 --factor 15000 --analyzer 42000 --tolerance-pct 25
  python platelet_check.py citrate --count 90000
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

ADVISORY = ("ADVISORY: decision support only - look at the smear (feather edge for clumps), check QC/clot/"
            "delta, and confirm with the lab SOP and the responsible MT before reporting.")


def estimate(fields, factor, analyzer=None, tolerance_pct=None, low_band=5.0, high_band=25.0):
    if not fields:
        raise ValueError("give the platelet count of each oil-immersion field")
    if factor <= 0:
        raise ValueError("--factor must be > 0 (use the factor your lab validated)")
    mean = sum(fields) / len(fields)
    est = mean * factor
    if mean < low_band:
        band = "decreased (< %g / field)" % low_band
    elif mean > high_band:
        band = "increased (> %g / field)" % high_band
    else:
        band = "adequate (%g-%g / field)" % (low_band, high_band)
    res = {"inputs": {"fields": fields, "n_fields": len(fields), "factor": factor},
           "mean_per_field": mean, "smear_band": band, "smear_estimate": est}
    if analyzer is not None:
        diff_pct = (analyzer - est) / est * 100 if est else float("inf")
        res["analyzer"] = analyzer
        res["analyzer_vs_smear_pct"] = diff_pct
        if tolerance_pct is None:
            res["agreement"] = "no --tolerance-pct given (take it from the lab SOP) -> no call"
        elif abs(diff_pct) <= tolerance_pct:
            res["agreement"] = "CONCORDANT within %g%%" % tolerance_pct
        elif diff_pct < 0:
            res["agreement"] = ("DISCORDANT: analyzer %.0f%% below the smear estimate -> suspect platelet clumps "
                                "(EDTA pseudothrombocytopenia) / partial clot. Do not report the analyzer value; "
                                "check feather edge, re-collect in citrate (see `citrate`)" % -diff_pct)
        else:
            res["agreement"] = ("DISCORDANT: analyzer %.0f%% above the smear estimate -> suspect fragments / "
                                "microcytes counted as platelets; review RBC morphology" % diff_pct)
    return res


def citrate(count, blood_parts=9.0, anticoag_parts=1.0):
    if blood_parts <= 0 or anticoag_parts < 0:
        raise ValueError("blood parts must be > 0 and anticoagulant parts >= 0")
    factor = (blood_parts + anticoag_parts) / blood_parts
    return {"inputs": {"citrate_count": count, "blood_parts": blood_parts, "anticoag_parts": anticoag_parts},
            "dilution_factor": factor, "corrected_count": count * factor,
            "formula": "count x (blood + anticoagulant) / blood"}


def _print(res):
    for k, v in res.items():
        print("%-24s %s" % (k, ("%.4f" % v) if isinstance(v, float) else v))
    print(ADVISORY)


def json_safe(o):
    """JSON has no Infinity/NaN: an unbounded value (e.g. a ratio with a zero denominator) is written as null."""
    if isinstance(o, float) and not math.isfinite(o):
        return None
    if isinstance(o, dict):
        return {k: json_safe(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [json_safe(v) for v in o]
    return o


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("estimate", help="smear platelet estimate (+ analyzer cross-check)")
    p.add_argument("--fields", type=float, nargs="+", required=True, help="platelets in each oil-immersion field")
    p.add_argument("--factor", type=float, required=True, help="lab-validated multiplication factor (per uL)")
    p.add_argument("--analyzer", type=float, help="analyzer platelet count (same unit as the estimate)")
    p.add_argument("--tolerance-pct", type=float, help="allowed analyzer-vs-smear difference, from the lab SOP")
    p = sub.add_parser("citrate", help="correct a citrate-tube count for the anticoagulant dilution")
    p.add_argument("--count", type=float, required=True)
    p.add_argument("--blood-parts", type=float, default=9.0, help="teaching default 9 (3.2%% citrate 1:9, 503402 §6)")
    p.add_argument("--anticoag-parts", type=float, default=1.0, help="teaching default 1")
    for _sp in sub.choices.values():  # also accept --json after the subcommand, as the examples show
        _sp.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="print JSON")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "estimate":
            res = estimate(a.fields, a.factor, a.analyzer, a.tolerance_pct)
        else:
            res = citrate(a.count, a.blood_parts, a.anticoag_parts)
    except ValueError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        res["advisory"] = ADVISORY
        print(json.dumps(json_safe(res), ensure_ascii=False, indent=1, allow_nan=False))
    else:
        _print(res)
    return 0


if __name__ == "__main__":
    sys.exit(main())
