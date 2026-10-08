#!/usr/bin/env python3
"""validation_calc — small, checkable method-verification calculations: precision split into
repeatability vs between-day (within-lab), total error vs TEa, and reference-interval verify / estimate.

Black-box tool for method-validation-stats. Run --help first; read the source only if a number looks wrong.
Sources:
  - method-validation-stats card Fork 4 / trap #5 (repeatability = within-run vs reproducibility =
    between-run/day are different numbers), Fork 2 / trap #3 (reference interval: nonparametric 2.5/97.5
    percentile, n >= 120 per partition; transference verify with n = 20, <= 2 outside = pass; never
    mean +/- 2SD on non-Gaussian data)
  - 510403 Clinical Laboratory Practice digest §2.4 (replication: within-run SD < 0.25 TEa, between-run
    < 0.33 TEa; reference interval verify 20, pass if <= 2 outside; TEcalc = bias + 3 SD, worked example
    glucose 0.58 + 3(1.75) = 5.83 <= TEa 10% -> acceptable)
  - 505402 Clinical Chemistry digest §1.2 (repeatability vs reproducibility definitions)
Precision uses one-way ANOVA variance components (day = group); percentile rank = p(n+1) with linear
interpolation. Sigma metric is NOT here - use clinchem-judgment `scripts/qc_calc.py sigma` (same TEa/bias/CV).
TEa and the reference limits are lab choices -> pass them in. ADVISORY ONLY.

Examples
  python validation_calc.py precision ../data/precision_example.csv --tea 10
  python validation_calc.py te --bias 0.58 --sd 1.75 --tea 10
  python validation_calc.py refint-verify --low 3.5 --high 5.1 4.0 4.2 ... (20 values)
  python validation_calc.py refint-estimate ../data/refint_example.csv
"""
import argparse
import csv
import json
import math
import statistics
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


# ---------------------------------------------------------------- precision (card Fork 4; 510403 §2.4)
def precision(groups, tea=None):
    """groups: {day: [values]} -> repeatability, between-day and within-lab SD/CV (one-way ANOVA)."""
    days = [g for g in groups.values() if g]
    k = len(days)
    N = sum(len(g) for g in days)
    if k < 2 or N - k < 1:
        raise ValueError("need >= 2 days and replicates within days")
    grand = statistics.fmean([v for g in days for v in g])
    ss_w = sum(sum((v - statistics.fmean(g)) ** 2 for v in g) for g in days)
    ss_b = sum(len(g) * (statistics.fmean(g) - grand) ** 2 for g in days)
    ms_w = ss_w / (N - k)
    ms_b = ss_b / (k - 1)
    n0 = (N - sum(len(g) ** 2 for g in days) / N) / (k - 1)
    var_b = max(0.0, (ms_b - ms_w) / n0)
    s_r = math.sqrt(ms_w)
    s_b = math.sqrt(var_b)
    s_wl = math.sqrt(ms_w + var_b)
    out = {"days": k, "n": N, "grand_mean": grand, "ms_within": ms_w, "ms_between": ms_b, "n0": n0,
           "repeatability_sd": s_r, "repeatability_cv": s_r / grand * 100,
           "between_day_sd": s_b, "within_lab_sd": s_wl, "within_lab_cv": s_wl / grand * 100,
           "lumped_sd_do_not_use": statistics.stdev([v for g in days for v in g])}
    if tea is not None:
        out["tea_pct"] = tea
        out["repeatability_ok"] = out["repeatability_cv"] < 0.25 * tea
        out["within_lab_ok"] = out["within_lab_cv"] < 0.33 * tea
    return out


def load_groups(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = [{k.strip().lower(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(ln for ln in f if not ln.lstrip().startswith("#"))]
    groups = {}
    for r in rows:
        if r.get("value"):
            groups.setdefault(r["day"], []).append(float(r["value"]))
    return groups


# ---------------------------------------------------------------- total error (510403 §2.4)
def total_error(bias, sd, tea, k=3.0):
    te = abs(bias) + k * sd
    return {"bias": bias, "sd": sd, "k": k, "te_calc": te, "tea": tea, "acceptable": te <= tea,
            "formula": "TEcalc = |bias| + %g x SD" % k}


# ---------------------------------------------------------------- reference interval (card Fork 2)
def refint_verify(values, low, high):
    out = [v for v in values if v < low or v > high]
    n = len(values)
    res = {"n": n, "outside": len(out), "outside_values": out, "low": low, "high": high}
    if n == 20:
        res["verdict"] = "PASS: <= 2 of 20 outside -> transference verified" if len(out) <= 2 else \
            "FAIL: > 2 of 20 outside -> interval not verified for this population"
    else:
        res["verdict"] = "NO VERDICT: the taught rule is <= 2 of 20 (n = 20); you gave n = %d -> apply your SOP" % n
    return res


def percentile(sorted_vals, p):
    n = len(sorted_vals)
    r = p * (n + 1)
    if r <= 1:
        return sorted_vals[0]
    if r >= n:
        return sorted_vals[-1]
    lo = int(math.floor(r))
    return sorted_vals[lo - 1] + (r - lo) * (sorted_vals[lo] - sorted_vals[lo - 1])


def refint_estimate(values):
    s = sorted(values)
    n = len(s)
    lo, hi = percentile(s, 0.025), percentile(s, 0.975)
    mean, sd = statistics.fmean(s), statistics.stdev(s)
    skew = sum(((v - mean) / sd) ** 3 for v in s) / n
    return {"n": n, "low_2.5": lo, "high_97.5": hi, "valid_n": n >= 120,
            "verdict": "nonparametric 2.5-97.5 percentile interval" if n >= 120 else
            "NOT VALID: n = %d < 120 per partition -> collect more or use transference (verify 20)" % n,
            "skewness": skew, "mean_pm_2sd_contrast_only": (mean - 2 * sd, mean + 2 * sd)}


def main(argv=None):
    try:  # never crash a non-UTF-8 console (e.g. Thai cp874) on the section sign / Thai text
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("precision", help="CSV with columns day,value (replicates per day)")
    p.add_argument("csv")
    p.add_argument("--tea", type=float, help="%% TEa chosen by the lab -> checks 0.25 / 0.33 TEa")
    p = sub.add_parser("te", help="total error vs TEa")
    p.add_argument("--bias", type=float, required=True)
    p.add_argument("--sd", type=float, required=True)
    p.add_argument("--tea", type=float, required=True)
    p.add_argument("--k", type=float, default=3.0, help="SD multiplier (510403 §2.4 uses 3)")
    p = sub.add_parser("refint-verify", help="transference check, n = 20")
    p.add_argument("--low", type=float, required=True)
    p.add_argument("--high", type=float, required=True)
    p.add_argument("values", nargs="+", type=float)
    p = sub.add_parser("refint-estimate", help="CSV with a column 'value'")
    p.add_argument("csv")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "precision":
            res = precision(load_groups(a.csv), a.tea)
        elif a.cmd == "te":
            res = total_error(a.bias, a.sd, a.tea, a.k)
        elif a.cmd == "refint-verify":
            res = refint_verify(a.values, a.low, a.high)
        else:
            with open(a.csv, encoding="utf-8-sig", newline="") as f:
                vals = [float(r["value"]) for r in csv.DictReader(ln for ln in f if not ln.lstrip().startswith("#")) if (r.get("value") or "").strip()]
            res = refint_estimate(vals)
    except ValueError as e:
        sys.exit(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "precision":
        print("days %d  n %d  grand mean %.4g   (one-way ANOVA, day = group)" % (res["days"], res["n"], res["grand_mean"]))
        print("  MS within %.4g   MS between %.4g   n0 %.4g" % (res["ms_within"], res["ms_between"], res["n0"]))
        print("  repeatability (within-run) SD %.4g  CV %.3f%%" % (res["repeatability_sd"], res["repeatability_cv"]))
        print("  between-day SD               %.4g" % res["between_day_sd"])
        print("  within-lab (total) SD        %.4g  CV %.3f%%" % (res["within_lab_sd"], res["within_lab_cv"]))
        print("  lumped SD of all values      %.4g   <- neither of the above; do not report as precision"
              % res["lumped_sd_do_not_use"])
        if "tea_pct" in res:
            print("  repeatability CV < 0.25 TEa (%.3g%%): %s" % (0.25 * res["tea_pct"], "PASS" if res["repeatability_ok"] else "FAIL"))
            print("  within-lab CV   < 0.33 TEa (%.3g%%): %s" % (0.33 * res["tea_pct"], "PASS" if res["within_lab_ok"] else "FAIL"))
    elif a.cmd == "te":
        print("%s = |%g| + %g x %g = %.4g  vs TEa %g -> %s" % (res["formula"], res["bias"], res["k"], res["sd"],
                                                            res["te_calc"], res["tea"],
                                                            "ACCEPTABLE" if res["acceptable"] else "NOT ACCEPTABLE"))
        print("  units: bias, SD and TEa must be in the same units (all % or all concentration)")
    elif a.cmd == "refint-verify":
        print("n %d · outside [%g, %g]: %d %s" % (res["n"], res["low"], res["high"], res["outside"], res["outside_values"]))
        print("VERDICT: " + res["verdict"])
    else:
        print("n %d · 2.5th %.4g · 97.5th %.4g   (rank = p(n+1), interpolated)" % (res["n"], res["low_2.5"], res["high_97.5"]))
        print("  skewness %.3f · mean +/- 2SD %.4g to %.4g  <- contrast only; wrong when skewed (card trap #3)"
              % (res["skewness"], *res["mean_pm_2sd_contrast_only"]))
        print("VERDICT: " + res["verdict"])
    print("ADVISORY: decision support only - acceptance criteria per the lab SOP + responsible MT sign-off.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
