#!/usr/bin/env python3
"""titer — titer endpoint, prozone pattern, fourfold comparison and high-dose hook check.

Black-box tool for immunoassay-judgment. Run --help first; read the source only if a result looks wrong.
Sources:
  titer = reciprocal of the highest dilution still positive (1:128 -> 128), serial 2-fold
          (506202 Immunology digest §15; IMMUNODIAGNOSTIC digest §3.4)
  prozone = antibody excess -> no lattice -> false negative at low dilution; fix = dilute and retest
          (IMMUNODIAGNOSTIC digest §3.1 + interpretation trap #1; 506202 §12; card FORK 4, trap #1)
  hook = very high analyte in a sandwich assay -> falsely low signal; fix = dilute and retest
          (IMMUNODIAGNOSTIC trap #1; card trap #2)
  fourfold rule = a titer change counts only at >= 4x, same test + same lab; congenital syphilis:
          infant >= 4x maternal flags, < 4x does NOT exclude (card FORK 2 syphilis line; Widal FORK 7)
ADVISORY ONLY. Lab-specific limits (hook tolerance) are arguments, never built in.

Subcommands
  series   dilution series -> titer, prozone flag, endpoint-not-reached flag
           results: neg/pos, 0/w/1+..4+ (0 = negative; any other grade counts as positive)
  compare  two titers -> fold change and the fourfold verdict (--mode paired | infant-vs-mother)
  hook     neat result + diluted results -> dilution-corrected values, hook suspected or not

Examples
  python titer.py series 1:1=0 1:2=0 1:4=2+ 1:8=3+ 1:16=2+ 1:32=1+ 1:64=0
  python titer.py series --csv ../data/rpr_prozone_series.csv
  python titer.py compare 1:8 1:32 --same-test
  python titer.py compare 1:16 1:64 --mode infant-vs-mother --same-test
  python titer.py hook --neat 180 --diluted 10:95 --diluted 100:12 --tolerance 20
"""
import argparse
import csv
import json
import math
import sys

GRADES = {"0": 0, "neg": 0, "-": 0, "nr": 0, "negative": 0,
          "w": 0.5, "w+": 0.5, "weak": 0.5, "+/-": 0.5, "±": 0.5,
          "pos": 1, "+": 1, "r": 1, "positive": 1, "1+": 1, "2+": 2, "3+": 3, "4+": 4}


def parse_dilution(text):
    """'1:32' or '32' -> 32.0 (the reciprocal)."""
    t = text.strip()
    if ":" in t:
        a, b = t.split(":", 1)
        return float(b) / float(a)
    return float(t)


def parse_grade(text):
    key = text.strip().lower()
    if key not in GRADES:
        raise ValueError("result %r: use neg/pos or 0, w, 1+..4+" % text)
    return GRADES[key]


def series(points):
    """points: list of (reciprocal_dilution, grade). Returns titer + flags."""
    pts = sorted(points)
    if len(pts) < 2:
        raise ValueError("need at least 2 dilutions")
    recips = [p[0] for p in pts]
    if len(set(recips)) != len(recips):
        raise ValueError("duplicate dilution in series")
    positive = [p for p in pts if p[1] > 0]
    label = lambda g: "0" if g == 0 else ("w" if g == 0.5 else "%g+" % g)  # noqa: E731
    out = {"points": [{"dilution": "1:%g" % d, "grade": label(g)} for d, g in pts]}
    if not positive:
        out.update(titer=None, verdict="NON-REACTIVE at every dilution tested",
                   prozone=False, endpoint_reached=True)
        return out
    highest = max(p[0] for p in positive)
    first_pos_index = next(i for i, p in enumerate(pts) if p[1] > 0)
    # prozone: a negative well at a LOWER dilution than a positive well
    prozone = any(p[1] == 0 for p in pts[:first_pos_index])
    # possible partial prozone: grade at the lowest dilution is weaker than the peak grade
    peak = max(p[1] for p in pts)
    partial = (not prozone) and pts[0][1] > 0 and pts[0][1] < peak
    endpoint_reached = pts[-1][1] == 0
    ratios = [recips[i + 1] / recips[i] for i in range(len(recips) - 1)]
    out.update(titer=highest, titer_text="1:%g" % highest, prozone=prozone, partial_prozone=partial,
               endpoint_reached=endpoint_reached,
               twofold=all(abs(r - 2) < 1e-9 for r in ratios))
    if not endpoint_reached:
        out["verdict"] = ("TITER >= %g: endpoint NOT reached (last well still positive) -> extend the series"
                          % highest)
    else:
        out["verdict"] = "TITER %g (1:%g)" % (highest, highest)
    if prozone:
        out["verdict"] += " | PROZONE pattern: negative at low dilution, positive when diluted"
    elif partial:
        out["verdict"] += " | possible partial prozone: weaker at the lowest dilution than when diluted"
    return out


def fold_change(earlier, later):
    return later / earlier


def compare(t1, t2, mode="paired", same_test=False):
    """t1 = earlier titer (or maternal), t2 = later titer (or infant). Reciprocal values."""
    fold = fold_change(t1, t2)
    steps = math.log2(fold)
    res = {"first": t1, "second": t2, "fold": fold, "twofold_steps": steps, "mode": mode,
           "same_test": same_test}
    if mode == "infant-vs-mother":
        if fold >= 4:
            res["verdict"] = "INFANT >= 4x MATERNAL: meets the congenital-syphilis flag -> flag clinician"
        else:
            res["verdict"] = ("INFANT < 4x MATERNAL: does NOT exclude congenital infection "
                              "(limited sensitivity) -> clinical follow-up")
    else:
        if fold >= 4:
            res["verdict"] = "SIGNIFICANT RISE (>= 4x)"
        elif fold <= 0.25:
            res["verdict"] = "SIGNIFICANT FALL (>= 4x)"
        else:
            res["verdict"] = "NOT SIGNIFICANT (< 4x change)"
    if not same_test:
        res["warning"] = ("titers are comparable only on the same test and same lab "
                          "(e.g. RPR vs VDRL titers are not interchangeable) - pass --same-test to confirm")
    return res


def hook(neat, diluted, tolerance_pct):
    """diluted: list of (dilution_factor, measured). Hook suspected when a dilution-corrected value
    exceeds the neat value by more than tolerance_pct."""
    rows = [{"dilution_factor": 1.0, "measured": neat, "corrected": neat}]
    for df, m in sorted(diluted):
        rows.append({"dilution_factor": df, "measured": m, "corrected": m * df})
    for r in rows:
        r["vs_neat_pct"] = (r["corrected"] / neat - 1) * 100 if neat else float("inf")
    suspected = any(r["vs_neat_pct"] > tolerance_pct for r in rows[1:])
    best = max(rows, key=lambda r: r["corrected"])
    res = {"rows": rows, "tolerance_pct": tolerance_pct, "hook_suspected": suspected}
    if suspected:
        res["verdict"] = ("HOOK SUSPECTED: diluted x factor exceeds neat by > %g%% -> do not report the neat "
                          "value; dilute further until two dilutions agree within tolerance (highest corrected "
                          "so far %.4g at 1:%g)" % (tolerance_pct, best["corrected"], best["dilution_factor"]))
    else:
        res["verdict"] = "NO HOOK SIGNAL: corrected values do not exceed neat beyond tolerance"
    return res


def load_series_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    return [(parse_dilution(r["dilution"]), parse_grade(r["result"])) for r in rows]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("series", help="dilution=result pairs, e.g. 1:4=2+")
    p.add_argument("pairs", nargs="*")
    p.add_argument("--csv", help="columns dilution,result")
    p = sub.add_parser("compare")
    p.add_argument("first", help="earlier (or maternal) titer, e.g. 1:8")
    p.add_argument("second", help="later (or infant) titer, e.g. 1:32")
    p.add_argument("--mode", choices=["paired", "infant-vs-mother"], default="paired")
    p.add_argument("--same-test", action="store_true", help="both titers from the same test and lab")
    p = sub.add_parser("hook")
    p.add_argument("--neat", type=float, required=True, help="result on the undiluted sample")
    p.add_argument("--diluted", action="append", required=True, help="FACTOR:MEASURED, e.g. 10:95")
    p.add_argument("--tolerance", type=float, required=True,
                   help="%% the lab accepts between dilutions (lab SOP value, no default)")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "series":
            pts = load_series_csv(a.csv) if a.csv else []
            for pair in a.pairs:
                d, r = pair.split("=", 1)
                pts.append((parse_dilution(d), parse_grade(r)))
            res = series(pts)
        elif a.cmd == "compare":
            res = compare(parse_dilution(a.first), parse_dilution(a.second), a.mode, a.same_test)
        else:
            dil = []
            for item in a.diluted:
                f_, m = item.split(":", 1)
                dil.append((float(f_), float(m)))
            res = hook(a.neat, dil, a.tolerance)
    except ValueError as e:
        ap.error(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "series":
        print("%-10s %s" % ("dilution", "grade"))
        for p_ in res["points"]:
            print("%-10s %s" % (p_["dilution"], p_["grade"]))
    elif a.cmd == "compare":
        print("first 1:%g  second 1:%g  fold %.3g  (2-fold steps %+.2f)" % (
            res["first"], res["second"], res["fold"], res["twofold_steps"]))
        if res.get("warning"):
            print("WARNING:", res["warning"])
    else:
        print("%-8s %-10s %-10s %s" % ("factor", "measured", "corrected", "vs neat"))
        for r in res["rows"]:
            print("%-8g %-10.4g %-10.4g %+.1f%%" % (r["dilution_factor"], r["measured"], r["corrected"],
                                                   r["vs_neat_pct"]))
    print("-" * 70)
    print("VERDICT:", res["verdict"])
    print("ADVISORY: decision support only - confirm with the lab SOP and an authorised signatory.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
