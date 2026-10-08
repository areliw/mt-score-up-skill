#!/usr/bin/env python3
"""diag_accuracy — 2x2 diagnostic accuracy, PPV/NPV at YOUR population's prevalence (taught with a
"per 1,000 people" table), and Cohen's kappa for categorical agreement.

Black-box tool for method-validation-stats. Run --help first; read the source only if a number looks wrong.
Sources:
  - 510403 Clinical Laboratory Practice digest §1.2: Sensitivity = a/(a+c), Specificity = d/(d+b),
    PPV = a/(a+b), NPV = d/(d+c)  with a = TP, b = FP, c = FN, d = TN
  - method-validation-stats card Fork 3 (PPV/NPV depend on prevalence - state the population; sens/spec only
    mean something against the named reference standard; imperfect gold standard bias), Fork 6 / trap #6
    (Cohen's kappa, not % agreement), trap #4 (PPV without prevalence), trap #8 (accuracy misleads at low
    prevalence)
PPV at prevalence p (Bayes) = sens*p / (sens*p + (1-spec)*(1-p)); NPV = spec*(1-p) / (spec*(1-p) + (1-sens)*p).
Kappa = (po - pe) / (1 - pe). CIs for proportions are Wilson 95%.
ADVISORY ONLY: interpretation for a real test needs the study design, the reference standard and the lab SOP.

Examples
  python diag_accuracy.py table --tp 90 --fp 10 --fn 10 --tn 890 --reference "culture"
  python diag_accuracy.py ppv --sens 0.95 --spec 0.95 --prevalence 0.01
  python diag_accuracy.py kappa --matrix "40,10;5,45"
"""
import argparse
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

Z = statistics.NormalDist().inv_cdf(0.975)
SWEEP = (0.001, 0.01, 0.05, 0.10, 0.20, 0.50)   # illustration only


def wilson(k, n):
    if n == 0:
        return (None, None)
    p = k / n
    den = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / den
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / den
    return (c - h, c + h)


def ppv_at(sens, spec, prev):
    tp, fp = sens * prev, (1 - spec) * (1 - prev)
    tn, fn = spec * (1 - prev), (1 - sens) * prev
    return {"ppv": tp / (tp + fp) if tp + fp else None, "npv": tn / (tn + fn) if tn + fn else None}


def per_population(sens, spec, prev, per=1000):
    sick = prev * per
    well = per - sick
    tp, fn = sens * sick, (1 - sens) * sick
    fp, tn = (1 - spec) * well, spec * well
    lr_pos = sens / (1 - spec) if spec < 1 else math.inf
    pre_odds = prev / (1 - prev)
    post_odds = pre_odds * lr_pos
    return {"per": per, "sick": sick, "well": well, "tp": tp, "fn": fn, "fp": fp, "tn": tn,
            "ppv": tp / (tp + fp) if tp + fp else None, "npv": tn / (tn + fn) if tn + fn else None,
            "check_ppv_via_lr": post_odds / (1 + post_odds) if math.isfinite(post_odds) else 1.0}


def table(tp, fp, fn, tn, prevalence=None):
    n = tp + fp + fn + tn
    sens = tp / (tp + fn)
    spec = tn / (tn + fp)
    res = {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "n": n,
           "sensitivity": sens, "sens_ci": wilson(tp, tp + fn),
           "specificity": spec, "spec_ci": wilson(tn, tn + fp),
           "ppv_at_study_prevalence": tp / (tp + fp) if tp + fp else None,
           "npv_at_study_prevalence": tn / (tn + fn) if tn + fn else None,
           "lr_pos": sens / (1 - spec) if spec < 1 else math.inf,
           "lr_neg": (1 - sens) / spec if spec > 0 else math.inf,
           "accuracy": (tp + tn) / n, "study_prevalence": (tp + fn) / n}
    if prevalence is not None:
        res["at_your_prevalence"] = dict(ppv_at(sens, spec, prevalence), prevalence=prevalence)
    return res


def kappa(matrix):
    k = len(matrix)
    if any(len(r) != k for r in matrix):
        raise ValueError("matrix must be square (same categories for both raters/methods)")
    n = sum(sum(r) for r in matrix)
    po = sum(matrix[i][i] for i in range(k)) / n
    rows = [sum(r) for r in matrix]
    cols = [sum(matrix[i][j] for i in range(k)) for j in range(k)]
    pe = sum(rows[i] * cols[i] for i in range(k)) / (n * n)
    return {"n": n, "percent_agreement": po * 100, "po": po, "pe": pe,
            "kappa": (po - pe) / (1 - pe) if pe < 1 else None}


def pct(v):
    return "-" if v is None else "%.2f%%" % (v * 100)


def main(argv=None):
    try:  # never crash a non-UTF-8 console (e.g. Thai cp874) on the section sign / Thai text
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("table", help="2x2 counts against a named reference standard")
    for k in ("tp", "fp", "fn", "tn"):
        p.add_argument("--" + k, type=int, required=True)
    p.add_argument("--reference", help="the reference standard the 2x2 was built against")
    p.add_argument("--prevalence", type=float, help="prevalence (0-1) in YOUR population")
    p = sub.add_parser("ppv", help="PPV/NPV at a prevalence, taught per 1,000 people")
    p.add_argument("--sens", type=float, required=True)
    p.add_argument("--spec", type=float, required=True)
    p.add_argument("--prevalence", type=float, required=True, help="0-1")
    p.add_argument("--per", type=int, default=1000)
    p = sub.add_parser("kappa", help="Cohen's kappa from an agreement matrix")
    p.add_argument("--matrix", required=True, help='rows ";" cols "," e.g. "40,10;5,45" (method A rows, method B cols)')
    a = ap.parse_args(argv)
    try:
        if a.cmd == "table":
            res = table(a.tp, a.fp, a.fn, a.tn, a.prevalence)
            res["reference"] = a.reference
        elif a.cmd == "ppv":
            if not 0 < a.prevalence < 1:
                raise ValueError("prevalence must be between 0 and 1 (e.g. 0.01 for 1%)")
            res = per_population(a.sens, a.spec, a.prevalence, a.per)
            res.update(sens=a.sens, spec=a.spec, prevalence=a.prevalence,
                       sweep=[dict(ppv_at(a.sens, a.spec, q), prevalence=q) for q in SWEEP])
        else:
            res = kappa([[float(v) for v in r.split(",")] for r in a.matrix.split(";")])
    except (ValueError, ZeroDivisionError) as e:
        sys.exit(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1, default=str))
        return 0
    if a.cmd == "table":
        print("              reference +   reference -")
        print("test +        a=TP %-7d  b=FP %d" % (res["tp"], res["fp"]))
        print("test -        c=FN %-7d  d=TN %d" % (res["fn"], res["tn"]))
        print("sensitivity a/(a+c) %s  95%%CI %s-%s" % (pct(res["sensitivity"]), pct(res["sens_ci"][0]), pct(res["sens_ci"][1])))
        print("specificity d/(d+b) %s  95%%CI %s-%s" % (pct(res["specificity"]), pct(res["spec_ci"][0]), pct(res["spec_ci"][1])))
        print("LR+ %.3g   LR- %.3g" % (res["lr_pos"], res["lr_neg"]))
        print("PPV a/(a+b) %s · NPV d/(d+c) %s   <- valid ONLY at the study prevalence %s" % (
            pct(res["ppv_at_study_prevalence"]), pct(res["npv_at_study_prevalence"]), pct(res["study_prevalence"])))
        print("accuracy %s   <- misleading when prevalence is low (card trap #8); use sens/spec/LR" % pct(res["accuracy"]))
        if "at_your_prevalence" in res:
            y = res["at_your_prevalence"]
            print("AT YOUR PREVALENCE %s: PPV %s · NPV %s" % (pct(y["prevalence"]), pct(y["ppv"]), pct(y["npv"])))
        else:
            print("NOTE: give --prevalence for your population, or run `ppv` - study PPV does not transfer")
        print("REFERENCE STANDARD: %s" % (res["reference"] or
                                          "NOT STATED - sens/spec mean nothing until you name it (card Fork 3)"))
    elif a.cmd == "ppv":
        print("Out of %d people at prevalence %s:" % (res["per"], pct(res["prevalence"])))
        print("  have the disease   %8.1f -> test + %8.1f (TP = sens x sick)    test - %8.1f (FN)" % (res["sick"], res["tp"], res["fn"]))
        print("  do not have it     %8.1f -> test + %8.1f (FP = (1-spec) x well) test - %8.1f (TN)" % (res["well"], res["fp"], res["tn"]))
        print("  PPV = TP / (TP + FP) = %.1f / %.1f = %s" % (res["tp"], res["tp"] + res["fp"], pct(res["ppv"])))
        print("  NPV = TN / (TN + FN) = %.1f / %.1f = %s" % (res["tn"], res["tn"] + res["fn"], pct(res["npv"])))
        print("  check via odds: pre-odds x LR+ -> PPV %s" % pct(res["check_ppv_via_lr"]))
        print("Same test, other prevalences (illustration):")
        for s in res["sweep"]:
            print("  prevalence %-8s PPV %-8s NPV %s" % (pct(s["prevalence"]), pct(s["ppv"]), pct(s["npv"])))
        print("LESSON: rare disease -> most positives are false even with a good test; PPV belongs to a population.")
    else:
        print("n %g · %% agreement %.2f%% · chance agreement pe %.4f · kappa %s" % (
            res["n"], res["percent_agreement"], res["pe"], "-" if res["kappa"] is None else "%.4f" % res["kappa"]))
        print("  kappa = (po - pe) / (1 - pe); % agreement includes chance agreement (card trap #6)")
    print("ADVISORY: decision support only - interpret with the study design, reference standard and lab SOP.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
