#!/usr/bin/env python3
"""qc_calc — small, checkable clinical-chemistry QC calculations.

Black-box tool for clinchem-judgment. Formulas follow the 505402 Clinical Chemistry Lab digest:
  §2.1 mean / SD (n-1) / %CV · §1.4 OCV vs RCV (RCV %CV must not exceed 2x OCV %CV)
  §3   sigma metric = (TEa - |bias|) / CV, all in %, and its interpretation · §3.1 rule choice
  §5   Friedewald LDL-C = TC - HDL-C - TG/5 (mg/dL; not valid when TG >= 400; fasting only)
TEa is a lab choice (CLIA / Ricos / RCPA ...) -> always pass it in. ADVISORY ONLY.

Examples
  python qc_calc.py stats 100 102 98 101 99
  python qc_calc.py ocv-rcv --ocv-cv 1.5 --rcv-cv 3.2
  python qc_calc.py sigma --tea 10 --bias 2 --cv 1.5
  python qc_calc.py ldl --tc 200 --hdl 50 --tg 150
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


def stats(values):
    n = len(values)
    if n < 2:
        raise ValueError("need at least 2 values")
    mean = sum(values) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in values) / (n - 1))  # sample SD, n-1 (§2.1)
    return {"n": n, "mean": mean, "sd": sd, "cv_pct": sd / mean * 100,
            "limits": {k: (mean - m * sd, mean + m * sd) for k, m in (("1SD", 1), ("2SD", 2), ("3SD", 3))}}


def ocv_rcv(ocv_cv, rcv_cv):
    ok = rcv_cv <= 2 * ocv_cv
    return {"ocv_cv": ocv_cv, "rcv_cv": rcv_cv, "ratio": rcv_cv / ocv_cv, "pass": ok,
            "verdict": "PASS: RCV %CV <= 2x OCV %CV" if ok else "FAIL: RCV %CV > 2x OCV %CV -> find the between-run cause"}


def sigma(tea, bias, cv):
    if cv <= 0:
        raise ValueError("cv must be > 0")
    s = (tea - abs(bias)) / cv
    if s >= 6:
        band, rules = "world class (>=6)", "1-3s, N=2, R=1"
    elif s >= 5:
        band, rules = "excellent (5)", "1-3s/2-2s/R-4s, N=2, R=1"
    elif s >= 4:
        band, rules = "good (4)", "1-3s/2-2s/R-4s/4-1s, N=4 R=1 or N=2 R=2"
    elif s >= 3:
        band, rules = "marginal (3): correct the method", "full multirule + 8x, N=8 or N=4 R=2"
    elif s >= 2:
        band, rules = "poor (2): correct or change the method", "QC cannot rescue this method"
    else:
        band, rules = "unacceptable (<2): change technology/analyzer", "QC cannot rescue this method"
    return {"tea_pct": tea, "bias_pct": bias, "cv_pct": cv, "sigma": s, "band": band, "suggested_qc": rules}


def ldl_friedewald(tc, hdl, tg):
    if tg >= 400:
        return {"ldl": None, "valid": False,
                "verdict": "NOT VALID: TG >= 400 mg/dL -> measure direct LDL-C"}
    ldl = tc - hdl - tg / 5
    return {"ldl": ldl, "valid": True, "verdict": "LDL-C = TC - HDL-C - TG/5 (fasting sample only)"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("stats")
    p.add_argument("values", nargs="+", type=float)
    p = sub.add_parser("ocv-rcv")
    p.add_argument("--ocv-cv", type=float, required=True)
    p.add_argument("--rcv-cv", type=float, required=True)
    p = sub.add_parser("sigma")
    p.add_argument("--tea", type=float, required=True, help="%% total allowable error chosen by the lab")
    p.add_argument("--bias", type=float, required=True, help="%% bias")
    p.add_argument("--cv", type=float, required=True, help="%% CV")
    p = sub.add_parser("ldl")
    p.add_argument("--tc", type=float, required=True)
    p.add_argument("--hdl", type=float, required=True)
    p.add_argument("--tg", type=float, required=True)
    a = ap.parse_args(argv)
    if a.cmd == "stats":
        res = stats(a.values)
    elif a.cmd == "ocv-rcv":
        res = ocv_rcv(a.ocv_cv, a.rcv_cv)
    elif a.cmd == "sigma":
        res = sigma(a.tea, a.bias, a.cv)
    else:
        res = ldl_friedewald(a.tc, a.hdl, a.tg)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        for k, v in res.items():
            print("%-14s %s" % (k, ("%.4f" % v) if isinstance(v, float) else v))
        print("ADVISORY: decision support only - confirm with the lab SOP and an authorised signatory.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
