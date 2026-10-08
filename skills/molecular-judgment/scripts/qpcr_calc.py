#!/usr/bin/env python3
"""qpcr_calc — checkable qPCR arithmetic: standard curve, Ct -> quantity, delta-delta-Ct, Ct fold.

Black-box tool for molecular-judgment. Run --help first; read the source only if a number looks wrong.
Card/digest anchors:
  - quantify only through a standard curve that passes acceptance; card Fork 5 teaching limits
    efficiency 90-110 %, R^2 > 0.98 (defaults below; replace with the lab's validated limits)
  - Ct low = more starting template; relative quantification needs a housekeeping/reference gene
    (card Fork 4; 510415 digest §8-§9)
  - PCR doubles per cycle at 100 % efficiency: 2^n copies; 30 cycles ~ 1 billion copies
    (510415 digest §4; 510201 digest §9)
Formulas [ทั่วไป — standard qPCR arithmetic, not printed in our digests]:
  Ct = slope * log10(quantity) + intercept (least squares) · efficiency E = 10^(-1/slope) - 1
  ddCt = (Ct_target - Ct_ref)_sample - (Ct_target - Ct_ref)_calibrator ; fold = 2^(-ddCt)
  with measured efficiencies (Pfaffl): (1+E_t)^(Ct_t,cal - Ct_t,s) / (1+E_r)^(Ct_r,cal - Ct_r,s)
ADVISORY ONLY: a reported quantity needs the lab's validated assay and an authorised signatory.

Subcommands
  curve  --std QTY:CT (>= 3 levels) or --csv quantity,ct ; optional --unknown CT (repeatable)
  ddct   --t-s --r-s --t-c --r-c  [--eff-t PCT --eff-r PCT]
  fold   --dct N [--eff PCT]   template ratio for a Ct difference N (sample B Ct - sample A Ct)

Examples
  python qpcr_calc.py curve --csv ../data/qpcr_standards_teaching.csv --unknown 25.0 --unknown 37.2
  python qpcr_calc.py curve --std 1e2:33.36 --std 1e4:26.71 --std 1e6:20.07 --eff-min 90 --eff-max 110 --r2-min 0.98
  python qpcr_calc.py ddct --t-s 24 --r-s 18 --t-c 27 --r-c 18
  python qpcr_calc.py fold --dct 3.32
"""
import argparse
import csv
import json
import math
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

CARD_DEFAULTS = {"eff_min": 90.0, "eff_max": 110.0, "r2_min": 0.98}  # card Fork 5 teaching values


def fit(points):
    """points: list of (quantity, ct). Least-squares Ct on log10(quantity)."""
    if len({q for q, _ in points}) < 3:
        raise ValueError("need at least 3 distinct standard levels")
    if any(q <= 0 for q, _ in points):
        raise ValueError("standard quantities must be > 0")
    xs = [math.log10(q) for q, _ in points]
    ys = [c for _, c in points]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx
    intercept = my - slope * mx
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    r2 = 1 - ss_res / ss_tot if ss_tot else 1.0
    return {"n": n, "slope": slope, "intercept": intercept, "r2": r2}


def efficiency_pct(slope):
    if slope >= 0:
        raise ValueError("slope must be negative (Ct falls as quantity rises)")
    return (10 ** (-1 / slope) - 1) * 100


def acceptance(eff, r2, eff_min, eff_max, r2_min):
    problems = []
    if not eff_min <= eff <= eff_max:
        problems.append("efficiency %.1f%% outside %.0f-%.0f%%" % (eff, eff_min, eff_max))
    if r2 <= r2_min:
        problems.append("R^2 %.4f not > %.2f" % (r2, r2_min))
    return {"pass": not problems, "problems": problems}


def quantify(ct, slope, intercept):
    return 10 ** ((ct - intercept) / slope)


def curve(points, unknowns=(), eff_min=90.0, eff_max=110.0, r2_min=0.98):
    f = fit(points)
    eff = efficiency_pct(f["slope"])
    acc = acceptance(eff, f["r2"], eff_min, eff_max, r2_min)
    qmin, qmax = min(q for q, _ in points), max(q for q, _ in points)
    rows = []
    for ct in unknowns:
        q = quantify(ct, f["slope"], f["intercept"])
        inside = qmin <= q <= qmax
        status = ("REPORTABLE (curve passes, inside standard range)" if acc["pass"] and inside else
                  "NOT REPORTABLE: curve fails acceptance" if not acc["pass"] else
                  "EXTRAPOLATED: outside the standard range -> dilute/re-run or report per SOP as < / >")
        rows.append({"ct": ct, "quantity": q, "inside_range": inside, "status": status})
    limits = {"eff_min": eff_min, "eff_max": eff_max, "r2_min": r2_min,
              "source": "card Fork 5 teaching default" if (eff_min, eff_max, r2_min) == tuple(CARD_DEFAULTS.values())
              else "user/lab supplied"}
    return dict(f, efficiency_pct=eff, acceptance=acc, limits=limits, standard_range=(qmin, qmax), unknowns=rows)


def ddct(t_s, r_s, t_c, r_c, eff_t=None, eff_r=None):
    d_s = t_s - r_s
    d_c = t_c - r_c
    dd = d_s - d_c
    res = {"dCt_sample": d_s, "dCt_calibrator": d_c, "ddCt": dd, "fold_2^-ddCt": 2 ** (-dd)}
    if eff_t is not None and eff_r is not None:
        et, er = 1 + eff_t / 100, 1 + eff_r / 100
        res["fold_efficiency_corrected"] = et ** (t_c - t_s) / er ** (r_c - r_s)
        res["note"] = "efficiency-corrected ratio uses the measured efficiencies of both genes"
    else:
        res["note"] = ("2^-ddCt assumes ~100 % efficiency for BOTH target and reference - "
                       "pass --eff-t/--eff-r from validated curves to check")
    return res


def fold(dct, eff_pct=100.0):
    return {"dCt": dct, "efficiency_pct": eff_pct, "template_ratio": (1 + eff_pct / 100) ** dct}


def load_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    return [(float(r["quantity"]), float(r["ct"])) for r in rows]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("curve")
    p.add_argument("--std", action="append", default=[], help="QTY:CT, e.g. 1e4:26.7")
    p.add_argument("--csv", help="columns quantity,ct")
    p.add_argument("--unknown", action="append", type=float, default=[])
    p.add_argument("--eff-min", type=float, default=CARD_DEFAULTS["eff_min"])
    p.add_argument("--eff-max", type=float, default=CARD_DEFAULTS["eff_max"])
    p.add_argument("--r2-min", type=float, default=CARD_DEFAULTS["r2_min"])
    p = sub.add_parser("ddct")
    for flag, h in (("--t-s", "target Ct, sample"), ("--r-s", "reference Ct, sample"),
                    ("--t-c", "target Ct, calibrator"), ("--r-c", "reference Ct, calibrator")):
        p.add_argument(flag, type=float, required=True, help=h)
    p.add_argument("--eff-t", type=float, help="target efficiency %%")
    p.add_argument("--eff-r", type=float, help="reference efficiency %%")
    p = sub.add_parser("fold")
    p.add_argument("--dct", type=float, required=True)
    p.add_argument("--eff", type=float, default=100.0)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "curve":
            pts = load_csv(a.csv) if a.csv else []
            pts += [(float(s.split(":")[0]), float(s.split(":")[1])) for s in a.std]
            res = curve(pts, a.unknown, a.eff_min, a.eff_max, a.r2_min)
        elif a.cmd == "ddct":
            res = ddct(a.t_s, a.r_s, a.t_c, a.r_c, a.eff_t, a.eff_r)
        else:
            res = fold(a.dct, a.eff)
    except ValueError as e:
        ap.error(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "curve":
        print("standards n=%d  slope %.4f  intercept %.4f  R^2 %.5f  efficiency %.1f%%" % (
            res["n"], res["slope"], res["intercept"], res["r2"], res["efficiency_pct"]))
        lim = res["limits"]
        print("acceptance: eff %.0f-%.0f%%, R^2 > %.2f  (%s) -> %s" % (
            lim["eff_min"], lim["eff_max"], lim["r2_min"], lim["source"],
            "PASS" if res["acceptance"]["pass"] else "FAIL: " + "; ".join(res["acceptance"]["problems"])))
        print("standard range %.4g .. %.4g" % res["standard_range"])
        for u in res["unknowns"]:
            print("  Ct %-7.2f -> %-12.4g %s" % (u["ct"], u["quantity"], u["status"]))
    else:
        for k, v in res.items():
            print("%-26s %s" % (k, ("%.4f" % v) if isinstance(v, float) else v))
    print("ADVISORY: decision support only - confirm with the validated assay, lab SOP and an authorised signatory.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
