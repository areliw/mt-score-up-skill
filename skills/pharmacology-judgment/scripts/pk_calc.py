#!/usr/bin/env python3
"""pk_calc — first-order pharmacokinetic arithmetic behind TDM timing (no dosing).

Black-box tool for pharmacology-judgment. Run --help first; read the source only if a number looks wrong.
Formulas from the PHARMACOLOGY digest §2 "Kinetics & เวลา":
  t½ = 0.7 x Vd / CL      (digest uses 0.7; the exact constant ln 2 = 0.693 is shown alongside)
  steady state is reached at ~4-5 t½  (also card Fork 7)
  fraction of steady state after n half-lives = 1 - 0.5^n   [hand arithmetic of first-order accumulation]
Valid for FIRST-ORDER drugs only. Zero-order / saturable drugs (phenytoin, ethanol, high-dose aspirin;
digest §2, card Fork 7) have no constant t½ -> the tool refuses with --kinetics zero.
MT does not prescribe: this tool deliberately has no loading/maintenance-dose command.
ADVISORY ONLY.

Subcommands
  halflife      --vd L --cl L/h            -> t½ (h) and elimination constant k
  steady-state  --half-life h [--hours h]  -> % of steady state by half-lives (and at the time given)

Examples
  python pk_calc.py halflife --vd 641 --cl 7.5
  python pk_calc.py steady-state --half-life 40 --hours 72
  python pk_calc.py steady-state --half-life 24 --kinetics zero
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

DIGEST_CONSTANT = 0.7          # PHARMACOLOGY digest §2
LN2 = math.log(2)


def halflife(vd, cl):
    if vd <= 0 or cl <= 0:
        raise ValueError("Vd and CL must be > 0")
    return {"vd_L": vd, "cl_L_per_h": cl, "t_half_h_digest_0.7": DIGEST_CONSTANT * vd / cl,
            "t_half_h_ln2": LN2 * vd / cl, "k_per_h": cl / vd}


def fraction_of_steady_state(n_half_lives):
    if n_half_lives < 0:
        raise ValueError("time on regimen must be >= 0")
    return 1 - 0.5 ** n_half_lives


def steady_state(t_half, hours=None, kinetics="first"):
    if kinetics == "zero":
        raise ValueError("zero-order (saturable) kinetics: t½ is not constant, so steady-state timing "
                         "cannot be computed from t½ (card Fork 7 trap) - follow the drug's TDM protocol")
    if t_half <= 0:
        raise ValueError("half-life must be > 0")
    table = [{"half_lives": n, "hours": n * t_half, "pct_of_ss": fraction_of_steady_state(n) * 100}
             for n in range(1, 7)]
    res = {"t_half_h": t_half, "table": table, "ss_rule": "~4-5 t½ (card Fork 7; digest §2)"}
    if hours is not None:
        n = hours / t_half
        res["at_hours"] = {"hours": hours, "half_lives": n, "pct_of_ss": fraction_of_steady_state(n) * 100}
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("halflife")
    p.add_argument("--vd", type=float, required=True, help="volume of distribution, L")
    p.add_argument("--cl", type=float, required=True, help="clearance, L/h")
    p = sub.add_parser("steady-state")
    p.add_argument("--half-life", type=float, required=True, help="hours")
    p.add_argument("--hours", type=float, help="hours since start or last dose change")
    p.add_argument("--kinetics", choices=["first", "zero"], default="first")
    for _sp in sub.choices.values():  # also accept --json after the subcommand, as the examples show
        _sp.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="print JSON")
    a = ap.parse_args(argv)
    try:
        res = halflife(a.vd, a.cl) if a.cmd == "halflife" else steady_state(a.half_life, a.hours, a.kinetics)
    except ValueError as e:
        ap.error(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "halflife":
        for k, v in res.items():
            print("%-22s %.4g" % (k, v))
    else:
        print("t½ %.4g h   steady state rule: %s" % (res["t_half_h"], res["ss_rule"]))
        print("%-12s %-10s %s" % ("half-lives", "hours", "% of steady state"))
        for r in res["table"]:
            print("%-12d %-10.4g %.2f" % (r["half_lives"], r["hours"], r["pct_of_ss"]))
        if "at_hours" in res:
            h = res["at_hours"]
            print("-" * 50)
            print("at %.4g h = %.2f half-lives -> %.1f%% of steady state" % (h["hours"], h["half_lives"],
                                                                             h["pct_of_ss"]))
    print("ADVISORY: teaching arithmetic only - dosing and TDM decisions belong to the physician/pharmacist.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
