#!/usr/bin/env python3
"""method_compare — "can the new method replace the old one?" Paired method comparison done the way the
card says: agreement (Bland-Altman bias + limits of agreement) and errors-in-both-axes regression
(Passing-Bablok, Deming) - never correlation r or a paired t-test as the agreement verdict.

Black-box tool for method-validation-stats. Run --help first; read the source only if a number looks wrong.
Sources:
  - method-validation-stats card rule #1 / trap #1 (r high != agreement; paired-t gives significance not
    clinical size of bias), Fork 1 (Bland-Altman: bias = mean difference, LoA = bias +/- 1.96 SD;
    Passing-Bablok / Deming because x also has error; intercept = constant bias, slope = proportional bias),
    trap #2 (OLS instead of Deming/PB), trap #7 (p-value instead of clinical acceptability), Fork 5 (n ~40-100+)
  - 510403 Clinical Laboratory Practice digest §2.4 (comparison >= 40 specimens; r >= 0.99 -> estimate bias at
    the medical decision level from regression; r < 0.99 -> range too narrow, use mean bias)
Method formulas are the published ones (Bland & Altman 1986; Passing & Bablok 1983 with shifted median and
rank-based CI; Deming with error-variance ratio lambda = var(error y) / var(error x), jackknife SE).
CIs use the normal quantile (z) - fine for n >= 40, approximate below that.
Allowable bias is a LAB choice -> pass it in. ADVISORY ONLY: acceptance is the lab's documented criterion,
signed off by the responsible MT; publication-grade work -> a statistician.

Input CSV: header with columns x (comparative / old method) and y (candidate / new method).

Examples
  python method_compare.py ../data/method_pairs_example.csv
  python method_compare.py ../data/method_pairs_example.csv --xc 126 --xc 200 --allowable-bias-pct 5
  python method_compare.py ../data/method_pairs_example.csv --percent --json
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

Z = statistics.NormalDist().inv_cdf(0.975)   # 1.959964


def load(path, xcol="x", ycol="y"):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = [{k.strip().lower(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(ln for ln in f if not ln.lstrip().startswith("#"))]
    pairs = [(float(r[xcol]), float(r[ycol])) for r in rows if r.get(xcol) and r.get(ycol)]
    if len(pairs) < 3:
        sys.exit("need at least 3 complete x,y pairs")
    return [p[0] for p in pairs], [p[1] for p in pairs]


# ---------------------------------------------------------------- agreement
def bland_altman(x, y, percent=False):
    if percent:
        d = [(b - a) / ((a + b) / 2) * 100 for a, b in zip(x, y)]
    else:
        d = [b - a for a, b in zip(x, y)]
    n = len(d)
    bias = statistics.fmean(d)
    sd = statistics.stdev(d)   # n-1
    half = Z * sd / math.sqrt(n)
    return {"unit": "%" if percent else "abs", "n": n, "bias": bias, "sd_diff": sd,
            "loa_low": bias - Z * sd, "loa_high": bias + Z * sd, "bias_ci": (bias - half, bias + half)}


def pearson_r(x, y):
    return statistics.correlation(x, y)


# ---------------------------------------------------------------- regressions (errors in x and y)
def deming(x, y, lam=1.0):
    """lam = var(error in y) / var(error in x); lam = 1 -> orthogonal regression."""
    mx, my = statistics.fmean(x), statistics.fmean(y)
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    if sxy == 0:
        raise ValueError("Sxy = 0: no linear relationship to fit")
    b = ((syy - lam * sxx) + math.sqrt((syy - lam * sxx) ** 2 + 4 * lam * sxy ** 2)) / (2 * sxy)
    return {"slope": b, "intercept": my - b * mx}


def deming_ci(x, y, lam=1.0):
    n = len(x)
    full = deming(x, y, lam)
    ps, pa = [], []
    for i in range(n):
        xi, yi = x[:i] + x[i + 1:], y[:i] + y[i + 1:]
        f = deming(xi, yi, lam)
        ps.append(n * full["slope"] - (n - 1) * f["slope"])
        pa.append(n * full["intercept"] - (n - 1) * f["intercept"])
    se_b = statistics.stdev(ps) / math.sqrt(n)
    se_a = statistics.stdev(pa) / math.sqrt(n)
    return dict(full, slope_ci=(full["slope"] - Z * se_b, full["slope"] + Z * se_b),
                intercept_ci=(full["intercept"] - Z * se_a, full["intercept"] + Z * se_a))


def passing_bablok(x, y):
    n = len(x)
    s = []
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy = x[j] - x[i], y[j] - y[i]
            if dx == 0:
                if dy == 0:
                    continue                      # identical points carry no slope
                s.append(math.copysign(math.inf, dy))
                continue
            sl = dy / dx
            if sl == -1:
                continue                          # PB excludes slopes of exactly -1
            s.append(sl)
    s.sort()
    N = len(s)
    if N == 0:
        raise ValueError("no usable pairwise slopes")
    K = sum(1 for v in s if v < -1)

    def at(k1):                                   # 1-based index into s
        return s[min(max(k1, 1), N) - 1]

    if N % 2:
        b = at((N + 1) // 2 + K)
    else:
        b = 0.5 * (at(N // 2 + K) + at(N // 2 + 1 + K))
    C = Z * math.sqrt(n * (n - 1) * (2 * n + 5) / 18.0)
    M1 = int(round((N - C) / 2.0))
    M2 = N - M1 + 1
    b_lo, b_hi = at(M1 + K), at(M2 + K)
    a = statistics.median([yi - b * xi for xi, yi in zip(x, y)])
    a_lo = statistics.median([yi - b_hi * xi for xi, yi in zip(x, y)])
    a_hi = statistics.median([yi - b_lo * xi for xi, yi in zip(x, y)])
    return {"slope": b, "intercept": a, "slope_ci": (b_lo, b_hi), "intercept_ci": (a_lo, a_hi),
            "n_slopes": N, "K": K}


def ols(x, y):
    """Shown only to make trap #2 visible; never used for a verdict."""
    mx, my = statistics.fmean(x), statistics.fmean(y)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    return {"slope": b, "intercept": my - b * mx}


# ---------------------------------------------------------------- verdict
def bias_type(reg):
    lo, hi = reg["intercept_ci"]
    slo, shi = reg["slope_ci"]
    return {"constant_bias": not (lo <= 0 <= hi), "proportional_bias": not (slo <= 1 <= shi)}


def agreement_verdict(ba, at_levels, allowable_abs=None, allowable_pct=None, r=None):
    """Clinical acceptability from bias size vs the lab's allowable bias - never from r or a p-value."""
    if allowable_abs is None and allowable_pct is None:
        return "NO VERDICT: give --allowable-bias / --allowable-bias-pct (lab criterion) to judge acceptability"
    fails = []
    for lv in at_levels:
        if allowable_abs is not None and abs(lv["bias"]) > allowable_abs:
            fails.append("bias %.4g at Xc=%g > %g" % (lv["bias"], lv["xc"], allowable_abs))
        if allowable_pct is not None and lv["bias_pct"] is not None and abs(lv["bias_pct"]) > allowable_pct:
            fails.append("bias %.2f%% at Xc=%g > %g%%" % (lv["bias_pct"], lv["xc"], allowable_pct))
    if not at_levels:
        if ba["unit"] == "abs" and allowable_abs is not None and abs(ba["bias"]) > allowable_abs:
            fails.append("mean bias %.4g > %g" % (ba["bias"], allowable_abs))
        if ba["unit"] == "%" and allowable_pct is not None and abs(ba["bias"]) > allowable_pct:
            fails.append("mean bias %.2f%% > %g%%" % (ba["bias"], allowable_pct))
    return ("NOT ACCEPTABLE: " + "; ".join(fails)) if fails else "bias within the allowable limit given"


def analyse(x, y, xc=(), lam=1.0, percent=False, allowable_abs=None, allowable_pct=None, use="pb"):
    ba = bland_altman(x, y, percent)
    r = pearson_r(x, y)
    pb = passing_bablok(x, y)
    dm = deming_ci(x, y, lam)
    reg = pb if use == "pb" else dm
    levels = []
    for c in xc:
        yc = reg["intercept"] + reg["slope"] * c
        levels.append({"xc": c, "yc": yc, "bias": yc - c, "bias_pct": (yc - c) / c * 100 if c else None})
    warn = []
    if len(x) < 40:
        warn.append("n = %d < 40: below the minimum taught for method comparison (510403 §2.4; card Fork 5)" % len(x))
    if r < 0.99:
        warn.append("r = %.4f < 0.99: data range narrow for regression estimates -> rely on mean bias "
                    "(510403 §2.4); widen the range if you can" % r)
    return {"n": len(x), "x_range": (min(x), max(x)), "bland_altman": ba, "passing_bablok": pb, "deming": dm,
            "deming_lambda": lam, "ols_for_contrast_only": ols(x, y), "r_range_check_only": r,
            "bias_type_from": use, "bias_type": bias_type(reg), "decision_levels": levels,
            "verdict": agreement_verdict(ba, levels, allowable_abs, allowable_pct, r), "warnings": warn}


def fmt_ci(ci):
    return "[%.4g, %.4g]" % ci


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
    try:  # never crash a non-UTF-8 console (e.g. Thai cp874) on the section sign / Thai text
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--x", default="x", help="column of the comparative/old method (default x)")
    ap.add_argument("--y", default="y", help="column of the candidate/new method (default y)")
    ap.add_argument("--xc", type=float, action="append", default=[], help="medical decision level (repeatable)")
    ap.add_argument("--allowable-bias", type=float, help="lab's allowable bias, measurement units")
    ap.add_argument("--allowable-bias-pct", type=float, help="lab's allowable bias, %%")
    ap.add_argument("--lambda", dest="lam", type=float, default=1.0, help="Deming error-variance ratio y/x (default 1)")
    ap.add_argument("--use", choices=["pb", "deming"], default="pb", help="regression for decision-level bias")
    ap.add_argument("--percent", action="store_true", help="Bland-Altman on %% differences (proportional scatter)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    x, y = load(a.csv, a.x.lower(), a.y.lower())
    try:
        res = analyse(x, y, a.xc, a.lam, a.percent, a.allowable_bias, a.allowable_bias_pct, a.use)
    except ValueError as e:
        sys.exit(str(e))
    if a.json:
        print(json.dumps(json_safe(res), ensure_ascii=False, indent=1, allow_nan=False))
        return 0
    ba, pb, dm = res["bland_altman"], res["passing_bablok"], res["deming"]
    u = "%" if ba["unit"] == "%" else ""
    print("n = %d   x range %.4g - %.4g" % (res["n"], *res["x_range"]))
    print("BLAND-ALTMAN (y - x%s)" % (", as %% of pair mean" if u else ""))
    print("  bias (mean diff)   %.4g%s   95%% CI %s" % (ba["bias"], u, fmt_ci(ba["bias_ci"])))
    print("  SD of differences  %.4g%s" % (ba["sd_diff"], u))
    print("  limits of agreement %.4g%s to %.4g%s   (bias +/- 1.96 SD)" % (ba["loa_low"], u, ba["loa_high"], u))
    print("PASSING-BABLOK   slope %.4g %s   intercept %.4g %s" % (pb["slope"], fmt_ci(pb["slope_ci"]),
                                                               pb["intercept"], fmt_ci(pb["intercept_ci"])))
    print("DEMING (lambda=%g) slope %.4g %s   intercept %.4g %s" % (res["deming_lambda"], dm["slope"], fmt_ci(dm["slope_ci"]),
                                                                 dm["intercept"], fmt_ci(dm["intercept_ci"])))
    o = res["ols_for_contrast_only"]
    print("  (OLS shown only for contrast - biased when x has error: slope %.4g intercept %.4g)" % (o["slope"], o["intercept"]))
    bt = res["bias_type"]
    print("BIAS TYPE (%s CIs): constant bias %s (intercept CI %s 0) · proportional bias %s (slope CI %s 1)" % (
        res["bias_type_from"], "YES" if bt["constant_bias"] else "no", "excludes" if bt["constant_bias"] else "includes",
        "YES" if bt["proportional_bias"] else "no", "excludes" if bt["proportional_bias"] else "includes"))
    for lv in res["decision_levels"]:
        print("  at Xc=%g: Yc=%.4g  bias %.4g (%.2f%%)" % (lv["xc"], lv["yc"], lv["bias"], lv["bias_pct"] or 0))
    print("r = %.4f  -> range-adequacy check ONLY (510403 §2.4). r is NOT agreement (card trap #1)." % res["r_range_check_only"])
    for w in res["warnings"]:
        print("WARN: " + w)
    print("VERDICT: " + res["verdict"])
    print("ADVISORY: decision support only - acceptance per the lab's documented criterion + responsible MT sign-off.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
