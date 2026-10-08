#!/usr/bin/env python3
"""power_calc - a priori sample-size arithmetic for sample-size-power (normal approximation).

Black-box tool: run `--help` / a subcommand first, do not read the source unless a run fails.
Formulas are the ones printed in the card (sections A-F, step 5); z values come from the exact
normal quantile (statistics.NormalDist), not the rounded 1.96 / 0.84 table values, so results can
differ by 1 from hand arithmetic with rounded z. The tool prints the formula, the z values, the raw
(unrounded) n and the rounded-up n so every number is checkable.

Subcommands (all accept --json; estimators accept --dropout RATE)
  prop-ci    one proportion, margin E          n = z^2 p(1-p) / E^2          (p defaults to 0.5)
  mean-ci    one mean, margin E                n = (z * sd / E)^2
  two-means  two independent means (per group) n = 2 (za+zb)^2 sd^2 / delta^2  (+ Guenther t-adjust, Lehr 16/d^2)
  paired     paired means                      n = (za+zb)^2 sd_diff^2 / delta^2  (sd_diff = SD of the DIFFERENCES)
  two-props  two proportions (per group)       pooled score-test form
  corr       Pearson r                         n = ((za+zb)/C)^2 + 3, C = 0.5 ln((1+r)/(1-r))
  dropout    enrolled N                        N = ceil(n / (1 - rate))
  se2sd      convert a standard error to SD    sd = se * sqrt(n)             (guards the SE-for-SD trap)
  posthoc    REFUSES: post-hoc / observed power (use the CI of the effect instead)

Examples
  python power_calc.py prop-ci --p 0.2 --margin 0.05
  python power_calc.py two-means --delta 5 --sd 10 --dropout 0.15
  python power_calc.py corr --r 0.3 --json
ADVISORY: confirm with G*Power / R pwr and a statistician before an EC or protocol submission.
"""
import argparse
import json
import math
import sys
from statistics import NormalDist

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ND = NormalDist()
ADVISORY = "ADVISORY: confirm with G*Power / R pwr and a statistician before an EC or protocol submission."


def ceil_n(x):
    """Round UP to a whole subject; the 1e-9 guard stops 64.0000000001 from becoming 65."""
    return int(math.ceil(x - 1e-9))


def z_alpha(alpha, two_sided=True):
    """Critical z for the type-I error: 0.05 two-sided -> 1.96, one-sided -> 1.645."""
    return ND.inv_cdf(1 - alpha / 2) if two_sided else ND.inv_cdf(1 - alpha)


def z_power(power):
    """z for power = 1 - beta: 0.80 -> 0.8416, 0.90 -> 1.2816."""
    return ND.inv_cdf(power)


def inflate_dropout(n, rate):
    """Enrol N so that n remain after dropout: N = n / (1 - rate), NOT n * (1 + rate)."""
    if not 0 <= rate < 1:
        raise ValueError("dropout rate must be in [0, 1)")
    return ceil_n(n / (1 - rate))


def se_to_sd(se, n):
    """SD = SE * sqrt(n). Putting an SE in a sigma slot makes N far too small."""
    return se * math.sqrt(n)


def n_prop_ci(p, margin, conf=0.95):
    z = z_alpha(1 - conf)
    raw = z * z * p * (1 - p) / margin ** 2
    return {"design": "one proportion (estimate)", "formula": "n = z^2 p(1-p) / E^2",
            "inputs": {"p": p, "margin": margin, "conf": conf}, "z": {"z_alpha": z}, "n_raw": raw, "n": ceil_n(raw),
            "unit": "subjects"}


def n_mean_ci(sd, margin, conf=0.95):
    z = z_alpha(1 - conf)
    raw = (z * sd / margin) ** 2
    return {"design": "one mean (estimate)", "formula": "n = (z * sd / E)^2",
            "inputs": {"sd": sd, "margin": margin, "conf": conf}, "z": {"z_alpha": z}, "n_raw": raw, "n": ceil_n(raw),
            "unit": "subjects"}


def n_two_means(delta, sd, alpha=0.05, power=0.80, two_sided=True):
    za, zb = z_alpha(alpha, two_sided), z_power(power)
    raw = 2 * (za + zb) ** 2 * sd ** 2 / delta ** 2
    d = delta / sd
    res = {"design": "two independent means", "formula": "n/group = 2 (za+zb)^2 sd^2 / delta^2",
           "inputs": {"delta": delta, "sd": sd, "d": d, "alpha": alpha, "power": power, "two_sided": two_sided},
           "z": {"z_alpha": za, "z_power": zb}, "n_raw": raw, "n": ceil_n(raw), "unit": "per group",
           "t_adjusted_raw": raw + za * za / 4, "t_adjusted_n": ceil_n(raw + za * za / 4)}
    if abs(alpha - 0.05) < 1e-12 and abs(power - 0.80) < 1e-12 and two_sided:
        res["lehr_16_over_d2"] = ceil_n(16 / d ** 2)
    return res


def n_paired(delta, sd_diff, alpha=0.05, power=0.80, two_sided=True):
    za, zb = z_alpha(alpha, two_sided), z_power(power)
    raw = (za + zb) ** 2 * sd_diff ** 2 / delta ** 2
    return {"design": "paired means", "formula": "n = (za+zb)^2 sd_diff^2 / delta^2",
            "inputs": {"delta": delta, "sd_diff": sd_diff, "alpha": alpha, "power": power, "two_sided": two_sided},
            "z": {"z_alpha": za, "z_power": zb}, "n_raw": raw, "n": ceil_n(raw), "unit": "pairs",
            "t_adjusted_raw": raw + za * za / 2, "t_adjusted_n": ceil_n(raw + za * za / 2)}


def n_two_props(p1, p2, alpha=0.05, power=0.80, two_sided=True):
    if p1 == p2:
        raise ValueError("p1 == p2: no effect to detect")
    za, zb = z_alpha(alpha, two_sided), z_power(power)
    pbar = (p1 + p2) / 2
    num = (za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    raw = num / (p1 - p2) ** 2
    return {"design": "two proportions", "formula": "n/group = [za sqrt(2 pbar(1-pbar)) + zb sqrt(p1q1+p2q2)]^2 / (p1-p2)^2",
            "inputs": {"p1": p1, "p2": p2, "pbar": pbar, "alpha": alpha, "power": power, "two_sided": two_sided},
            "z": {"z_alpha": za, "z_power": zb}, "n_raw": raw, "n": ceil_n(raw), "unit": "per group"}


def n_corr(r, alpha=0.05, power=0.80, two_sided=True):
    if not 0 < abs(r) < 1:
        raise ValueError("r must be in (0,1) in absolute value")
    za, zb = z_alpha(alpha, two_sided), z_power(power)
    c = 0.5 * math.log((1 + r) / (1 - r))
    raw = ((za + zb) / c) ** 2 + 3
    return {"design": "correlation", "formula": "n = ((za+zb)/C)^2 + 3, C = 0.5 ln((1+r)/(1-r))",
            "inputs": {"r": r, "C": c, "alpha": alpha, "power": power, "two_sided": two_sided},
            "z": {"z_alpha": za, "z_power": zb}, "n_raw": raw, "n": ceil_n(raw), "unit": "subjects"}


def add_dropout(res, rate):
    if rate:
        res["dropout_rate"] = rate
        res["n_enrol"] = inflate_dropout(res["n"], rate)
        res["n_enrol_unit"] = res["unit"]
    return res


def render(res):
    lines = ["design        %s" % res["design"], "formula       %s" % res["formula"]]
    for k, v in res["inputs"].items():
        lines.append("  input %-8s %s" % (k, ("%.6g" % v) if isinstance(v, float) else v))
    for k, v in res["z"].items():
        lines.append("  %-14s %.6f" % (k, v))
    lines.append("n_raw         %.4f" % res["n_raw"])
    lines.append("n (round up)  %d %s" % (res["n"], res["unit"]))
    if "t_adjusted_n" in res:
        lines.append("t-adjusted    %.2f -> %d  (Guenther: normal-approx + za^2/4 or /2; closer to G*Power's noncentral t)"
                     % (res["t_adjusted_raw"], res["t_adjusted_n"]))
    if "lehr_16_over_d2" in res:
        lines.append("Lehr 16/d^2   %d  (only valid for alpha 0.05 two-sided, power 0.80)" % res["lehr_16_over_d2"])
    if "n_enrol" in res:
        lines.append("dropout %.0f%%   enrol %d %s  (= n / (1 - rate), not n x (1 + rate))"
                     % (res["dropout_rate"] * 100, res["n_enrol"], res["n_enrol_unit"]))
    for note in res.get("notes", []):
        lines.append("NOTE: " + note)
    lines.append(ADVISORY)
    return "\n".join(lines)


def build_parser():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", dest="json_main")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, power=True):
        p.add_argument("--json", action="store_true")
        p.add_argument("--dropout", type=float, default=0.0, help="expected dropout rate, e.g. 0.15")
        if power:
            p.add_argument("--alpha", type=float, default=0.05)
            p.add_argument("--power", type=float, default=0.80)
            p.add_argument("--one-sided", action="store_true",
                           help="one-sided alpha (needs a direction fixed BEFORE the data; default is two-sided)")

    p = sub.add_parser("prop-ci", help="one proportion")
    p.add_argument("--p", type=float, default=None, help="expected proportion; omit -> 0.5 (largest n, safest)")
    p.add_argument("--margin", type=float, required=True)
    p.add_argument("--conf", type=float, default=0.95)
    common(p, power=False)
    p = sub.add_parser("mean-ci", help="one mean")
    p.add_argument("--sd", type=float, required=True, help="SD (NOT the standard error)")
    p.add_argument("--margin", type=float, required=True)
    p.add_argument("--conf", type=float, default=0.95)
    common(p, power=False)
    p = sub.add_parser("two-means", help="two independent means, per group")
    p.add_argument("--delta", type=float, required=True, help="smallest difference worth detecting")
    p.add_argument("--sd", type=float, required=True, help="common SD (NOT the standard error)")
    common(p)
    p = sub.add_parser("paired", help="paired means")
    p.add_argument("--delta", type=float, required=True)
    p.add_argument("--sd-diff", type=float, required=True, help="SD of the paired DIFFERENCES")
    common(p)
    p = sub.add_parser("two-props", help="two proportions, per group")
    p.add_argument("--p1", type=float, required=True)
    p.add_argument("--p2", type=float, required=True)
    common(p)
    p = sub.add_parser("corr", help="Pearson correlation")
    p.add_argument("--r", type=float, required=True)
    common(p)
    p = sub.add_parser("dropout", help="inflate n for dropout")
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--rate", type=float, required=True)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("se2sd", help="standard error -> SD")
    p.add_argument("--se", type=float, required=True)
    p.add_argument("--n", type=int, required=True, help="sample size the SE came from")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("posthoc", help="refused: observed/post-hoc power")
    p.add_argument("--json", action="store_true")
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    want_json = a.json_main or getattr(a, "json", False)
    if a.cmd == "posthoc":
        msg = ("REFUSED: post-hoc (observed) power is a one-to-one function of the p-value (Hoenig & Heisey 2001), "
               "so it explains nothing. Report the CI of the effect; if you need a plan, compute n a priori.")
        print(json.dumps({"refused": True, "reason": msg}, ensure_ascii=False) if want_json else msg)
        return 2
    if a.cmd == "dropout":
        res = {"n": a.n, "dropout_rate": a.rate, "n_enrol": inflate_dropout(a.n, a.rate),
               "wrong_formula_n_x_(1+rate)": ceil_n(a.n * (1 + a.rate))}
    elif a.cmd == "se2sd":
        res = {"se": a.se, "n": a.n, "sd": se_to_sd(a.se, a.n), "formula": "sd = se * sqrt(n)"}
    else:
        two_sided = not getattr(a, "one_sided", False)
        if a.cmd == "prop-ci":
            res = n_prop_ci(0.5 if a.p is None else a.p, a.margin, a.conf)
        elif a.cmd == "mean-ci":
            res = n_mean_ci(a.sd, a.margin, a.conf)
        elif a.cmd == "two-means":
            res = n_two_means(a.delta, a.sd, a.alpha, a.power, two_sided)
        elif a.cmd == "paired":
            res = n_paired(a.delta, a.sd_diff, a.alpha, a.power, two_sided)
        elif a.cmd == "two-props":
            res = n_two_props(a.p1, a.p2, a.alpha, a.power, two_sided)
        else:
            res = n_corr(a.r, a.alpha, a.power, two_sided)
        res["notes"] = []
        if not two_sided:
            res["notes"].append("one-sided alpha: only defensible when the direction was fixed before data; "
                                "otherwise it is p-hacking by design")
        if a.cmd == "prop-ci" and a.p is None:
            res["notes"].append("p not given -> 0.5 (largest n, safest)")
        add_dropout(res, a.dropout)
    if want_json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    elif a.cmd in ("dropout", "se2sd"):
        for k, v in res.items():
            print("%-26s %s" % (k, ("%.4f" % v) if isinstance(v, float) else v))
        print(ADVISORY)
    else:
        print(render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
