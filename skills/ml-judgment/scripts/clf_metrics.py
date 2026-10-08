#!/usr/bin/env python3
"""clf_metrics - classification metrics that show when accuracy lies (imbalance trap).

Black-box tool for ml-judgment (Fork 4 + the "accuracy on imbalanced data" trap). Run a subcommand
first; do not read the source unless a run fails. Formulas follow the CMU 961701 / 229711 digests:
Accuracy = (TP+TN)/all, Precision = TP/(TP+FP), Recall = TP/(TP+FN), F1 = 2PR/(P+R); specificity = TN/(TN+FP).
Every output also prints the MAJORITY-CLASS BASELINE accuracy: an accuracy that does not beat it is worthless.

Subcommands (all accept --json)
  confusion  --tp --fp --fn --tn [--prevalence P]   metrics from counts; --prevalence re-expresses PPV/NPV at that prevalence
  from-csv   FILE --true COL --pred COL [--positive V]   counts from two label columns, then the same table
  ppv        --sens S --spec S --prevalence P [P ...]   PPV/NPV by Bayes at each prevalence (the AUC-vs-precision trap)
  auc        FILE --label COL --score COL [--positive V]   ROC-AUC (rank/Mann-Whitney) and average precision (PR-AUC)

Examples
  python clf_metrics.py confusion --tp 0 --fp 0 --fn 2 --tn 98
  python clf_metrics.py ppv --sens 0.95 --spec 0.95 --prevalence 0.5 0.1 0.02
  python clf_metrics.py auc scores.csv --label y --score p
ADVISORY: decision support only - judge the metric against the cost of a miss vs a false alarm in your use case.
"""
import argparse
import csv
import json
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ADVISORY = "ADVISORY: decision support only - judge the metric against the cost of a miss vs a false alarm in your use case."


def safe_div(a, b):
    """None (not 0) when the ratio is undefined, so 'no predicted positives' is never read as 'precision 0'."""
    return None if b == 0 else a / b


def baseline_accuracy(tp, fp, fn, tn):
    """Accuracy of always predicting the majority class: max(actual positives, actual negatives) / n."""
    n = tp + fp + fn + tn
    return safe_div(max(tp + fn, tn + fp), n)


def confusion_metrics(tp, fp, fn, tn, prevalence=None):
    n = tp + fp + fn + tn
    if n == 0 or min(tp, fp, fn, tn) < 0:
        raise ValueError("counts must be non-negative and not all zero")
    acc = (tp + tn) / n
    prec = safe_div(tp, tp + fp)
    rec = safe_div(tp, tp + fn)  # sensitivity
    spec = safe_div(tn, tn + fp)
    f1 = 0.0 if tp == 0 else 2 * prec * rec / (prec + rec)
    base = baseline_accuracy(tp, fp, fn, tn)
    pos, neg = tp + fn, tn + fp
    res = {"n": n, "tp": tp, "fp": fp, "fn": fn, "tn": tn,
           "actual_positive_share": pos / n,
           "imbalance_ratio_majority_over_minority": safe_div(max(pos, neg), min(pos, neg)),
           "accuracy": acc, "precision": prec, "recall": rec, "specificity": spec, "f1": f1,
           "balanced_accuracy": None if rec is None or spec is None else (rec + spec) / 2,
           "majority_baseline_accuracy": base, "accuracy_minus_baseline": acc - base, "flags": []}
    if acc <= base + 1e-12:
        res["flags"].append("ACCURACY-TRAP: accuracy does not beat the majority baseline (%.4f <= %.4f) - the model adds nothing; "
                            "read precision / recall / PR-AUC" % (acc, base))
    if rec == 0:
        res["flags"].append("RECALL=0: not one actual positive was found")
    if prec is None:
        res["flags"].append("PRECISION undefined: the model never predicted positive")
    if prevalence is not None and rec is not None and spec is not None:
        res["at_prevalence"] = ppv_npv(rec, spec, prevalence)
    return res


def ppv_npv(sens, spec, prevalence):
    """Bayes: PPV = sens*prev / (sens*prev + (1-spec)*(1-prev)); NPV likewise. PPV falls with prevalence."""
    if not 0 < prevalence < 1:
        raise ValueError("prevalence must be in (0,1)")
    tp = sens * prevalence
    fp = (1 - spec) * (1 - prevalence)
    tn = spec * (1 - prevalence)
    fn = (1 - sens) * prevalence
    return {"prevalence": prevalence, "sens": sens, "spec": spec,
            "ppv": safe_div(tp, tp + fp), "npv": safe_div(tn, tn + fn)}


def counts_from_labels(y_true, y_pred, positive):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == positive and p == positive)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t != positive and p == positive)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == positive and p != positive)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t != positive and p != positive)
    return tp, fp, fn, tn


def ranks_average(values):
    """1-based average ranks (ties share the mean rank) - the Mann-Whitney convention."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def roc_auc(labels, scores):
    """AUC = P(score of a random positive > score of a random negative), ties count 1/2. labels are 1/0."""
    p = sum(labels)
    n = len(labels) - p
    if p == 0 or n == 0:
        raise ValueError("need both classes")
    r = ranks_average(scores)
    return (sum(rk for rk, y in zip(r, labels) if y == 1) - p * (p + 1) / 2) / (p * n)


def average_precision(labels, scores):
    """AP = sum_n (R_n - R_{n-1}) P_n over thresholds (scikit-learn definition; ties grouped)."""
    p = sum(labels)
    if p == 0:
        raise ValueError("no positives")
    pairs = sorted(zip(scores, labels), key=lambda t: -t[0])
    tp = fp = 0
    prev_recall = 0.0
    ap = 0.0
    i = 0
    while i < len(pairs):
        j = i
        while j < len(pairs) and pairs[j][0] == pairs[i][0]:
            tp += pairs[j][1]
            fp += 1 - pairs[j][1]
            j += 1
        recall = tp / p
        ap += (recall - prev_recall) * (tp / (tp + fp))
        prev_recall = recall
        i = j
    return ap


def read_columns(path, cols):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        missing = [c for c in cols if c not in (rd.fieldnames or [])]
        if missing:
            raise SystemExit("column(s) not found: %s; have %s" % (missing, rd.fieldnames))
        return [[row[c] for c in cols] for row in rd]


def render(res):
    lines = []
    for k, v in res.items():
        if k in ("flags", "at_prevalence"):
            continue
        lines.append("%-40s %s" % (k, ("%.4f" % v) if isinstance(v, float) else v))
    if "at_prevalence" in res:
        a = res["at_prevalence"]
        lines.append("at prevalence %.4g: PPV %.4f  NPV %.4f  (same sens/spec)" % (a["prevalence"], a["ppv"], a["npv"]))
    for fl in res["flags"]:
        lines.append("FLAG: " + fl)
    lines.append(ADVISORY)
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", dest="json_main")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("confusion")
    for k in ("tp", "fp", "fn", "tn"):
        p.add_argument("--" + k, type=int, required=True)
    p.add_argument("--prevalence", type=float, default=None)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("from-csv")
    p.add_argument("file")
    p.add_argument("--true", required=True, dest="true_col")
    p.add_argument("--pred", required=True, dest="pred_col")
    p.add_argument("--positive", default="1")
    p.add_argument("--prevalence", type=float, default=None)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("ppv")
    p.add_argument("--sens", type=float, required=True)
    p.add_argument("--spec", type=float, required=True)
    p.add_argument("--prevalence", type=float, nargs="+", required=True)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("auc")
    p.add_argument("file")
    p.add_argument("--label", required=True)
    p.add_argument("--score", required=True)
    p.add_argument("--positive", default="1")
    p.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    want_json = a.json_main or a.json
    if a.cmd == "confusion":
        res = confusion_metrics(a.tp, a.fp, a.fn, a.tn, a.prevalence)
    elif a.cmd == "from-csv":
        rows = read_columns(a.file, [a.true_col, a.pred_col])
        res = confusion_metrics(*counts_from_labels([r[0] for r in rows], [r[1] for r in rows], a.positive), a.prevalence)
    elif a.cmd == "ppv":
        res = {"rows": [ppv_npv(a.sens, a.spec, pv) for pv in a.prevalence]}
    else:
        rows = read_columns(a.file, [a.label, a.score])
        y = [1 if r[0] == a.positive else 0 for r in rows]
        s = [float(r[1]) for r in rows]
        res = {"n": len(y), "positives": sum(y), "roc_auc": roc_auc(y, s), "average_precision": average_precision(y, s),
               "average_precision_if_random": sum(y) / len(y),
               "note": "AP of a random scorer equals the prevalence; compare AP with that, not with 0.5"}
    if want_json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    elif a.cmd == "confusion" or a.cmd == "from-csv":
        print(render(res))
    elif a.cmd == "ppv":
        for r in res["rows"]:
            print("prevalence %-8g sens %.3f spec %.3f -> PPV %.4f  NPV %.4f" % (r["prevalence"], r["sens"], r["spec"], r["ppv"], r["npv"]))
        print(ADVISORY)
    else:
        for k, v in res.items():
            print("%-28s %s" % (k, ("%.4f" % v) if isinstance(v, float) else v))
        print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
