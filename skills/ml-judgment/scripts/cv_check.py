#!/usr/bin/env python3
"""cv_check - leakage and validation sanity checks on a CSV dataset (before you trust a metric).

Black-box tool for ml-judgment (rule #1 leakage, traps: target leakage, no stratify, p>>n, tuning on test).
Run `--help` / a subcommand first; do not read the source unless a run fails.

  audit FILE --target COL [--id-cols a,b] [--split-col COL] [--folds 5] [--positive V]
      class balance + majority baseline, stratified fold layout (and what an UNshuffled split does to a file sorted
      by class), ID-like columns, single features that (almost) determine the target, duplicate rows (and rows
      duplicated across a train/test split column), p > n warning.
  demo [--n 50 --p 5000 --top 100 --folds 5 --seed 0]
      the textbook null experiment (Hastie-Tibshirani-Friedman, Elements of Statistical Learning 2nd ed. s7.10.2):
      labels independent of 5000 noise predictors; screening the top predictors on ALL rows and then cross-validating
      ("wrong way") looks excellent, screening inside each training fold ("right way") sits near 50%.

Thresholds --auc-flag / --purity-flag are screening heuristics, not verdicts: a flagged column means "check the
timeline - was this value known at prediction time?", not "this is leakage".

Examples
  python cv_check.py audit data.csv --target outcome --id-cols patient_id --folds 5
  python cv_check.py audit data.csv --target outcome --split-col split     # split column holds train / test
  python cv_check.py demo --seed 1
ADVISORY: a clean audit does not prove there is no leakage; it only removes the cheap, checkable causes.
"""
import argparse
import csv
import json
import random
import re
import sys
from collections import Counter, defaultdict

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ADVISORY = "ADVISORY: a clean audit does not prove there is no leakage; it only removes the cheap, checkable causes."
MISSING = {"", "na", "n/a", "nan", "null", "none", "?"}
ID_NAME = re.compile(r"(^|[_\W])(id|rid|hn|mrn|uuid|guid|index|barcode|accession)($|[_\W])", re.I)


# ---------------------------------------------------------------- helpers
def is_missing(v):
    return v is None or str(v).strip().lower() in MISSING


def to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def load_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        rows = [dict(r) for r in rd]
        return list(rd.fieldnames or []), rows


def ranks_average(values):
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
    """P(random positive scores above random negative), ties = 1/2 (Mann-Whitney U / (P*N)). labels are 1/0."""
    p = sum(labels)
    n = len(labels) - p
    if p == 0 or n == 0:
        return None
    r = ranks_average(scores)
    return (sum(rk for rk, y in zip(r, labels) if y == 1) - p * (p + 1) / 2) / (p * n)


def stratified_folds(labels, k):
    """Fold id per row; each class is dealt round-robin so every class is spread over the k folds as evenly as possible."""
    folds = [0] * len(labels)
    offset = 0
    for cls in sorted(set(labels), key=str):
        idx = [i for i, y in enumerate(labels) if y == cls]
        for j, i in enumerate(idx):
            folds[i] = (j + offset) % k
        offset = (offset + len(idx)) % k
    return folds


def plain_folds(n, k):
    """Contiguous blocks in file order = unshuffled K-fold (first n%k folds get one extra row)."""
    sizes = [n // k + (1 if i < n % k else 0) for i in range(k)]
    out = []
    for fid, s in enumerate(sizes):
        out += [fid] * s
    return out


def fold_table(labels, folds, k):
    classes = sorted(set(labels), key=str)
    return {f: {c: sum(1 for y, g in zip(labels, folds) if g == f and y == c) for c in classes} for f in range(k)}


# ---------------------------------------------------------------- audit
def column_kind(vals):
    present = [v for v in vals if not is_missing(v)]
    return "numeric" if present and all(to_float(v) is not None for v in present) else "categorical"


def audit(header, rows, target, id_cols=(), split_col=None, folds=5, auc_flag=0.95, purity_flag=0.99, positive=None):
    findings = []

    def add(sev, check, detail):
        findings.append({"severity": sev, "check": check, "detail": detail})

    if target not in header:
        raise SystemExit("target column %r not found; have %s" % (target, header))
    n_all = len(rows)
    rows_t = [r for r in rows if not is_missing(r[target])]
    if len(rows_t) < n_all:
        add("ERROR", "target-missing", "%d row(s) have no target value; drop or fix them before any split" % (n_all - len(rows_t)))
    y = [r[target] for r in rows_t]
    feats = [h for h in header if h != target and h not in id_cols and h != split_col]
    n = len(rows_t)
    cnt = Counter(y)
    classes = sorted(cnt, key=lambda c: (-cnt[c], str(c)))
    majority, minority = classes[0], classes[-1]
    base = cnt[majority] / n if n else 0.0
    add("INFO", "balance", "n=%d, classes=%s; majority baseline accuracy=%.4f (any model accuracy must beat this); "
        "imbalance ratio majority/minority=%.2f" % (n, dict(cnt), base, cnt[majority] / cnt[minority]))
    # ---- fold feasibility
    if len(classes) >= 2:
        if cnt[minority] < folds:
            add("ERROR", "fold-feasibility", "minority class %r has %d rows < %d folds: at least one fold has NO minority row even "
                "when stratified - use fewer folds, repeated stratified CV, or collect more data" % (minority, cnt[minority], folds))
        sf = fold_table(y, stratified_folds(y, folds), folds)
        add("INFO", "stratified-layout", "stratified %d-fold rows per class: %s" % (folds, {f: sf[f] for f in sf}))
        pf = fold_table(y, plain_folds(n, folds), folds)
        empty = [f for f in pf if any(v == 0 for v in pf[f].values())]
        if empty:
            add("WARN", "no-shuffle-no-stratify", "in FILE ORDER (unshuffled K-fold) fold(s) %s lack at least one class: %s - "
                "the file looks sorted/blocked by target; shuffle + StratifiedKFold" % (empty, {f: pf[f] for f in empty}))
    # ---- ID-like columns
    id_like = set()
    for h in feats:
        vals = [r[h] for r in rows_t if not is_missing(r[h])]
        if len(vals) == n and n > 2 and len(set(vals)) == n:
            floats = [to_float(v) for v in vals]
            all_int = all(f is not None and f == int(f) for f in floats)
            all_str = all(f is None for f in floats)
            consecutive = all_int and max(floats) - min(floats) + 1 == n  # 1..n style counter
            # unique integers such as ages are legitimate measurements; call it an ID only on strong evidence
            if all_str or consecutive or ID_NAME.search(h):
                id_like.add(h)
                add("WARN", "id-like", "column %r has a unique value in every row: an identifier, not a feature - drop it "
                    "(a tree/KNN can memorise rows with it; information gain is maximal for it)" % h)
    # ---- single-feature leakage
    pos_label = positive if positive is not None else minority
    binary = len(classes) == 2
    ybin = [1 if v == str(pos_label) or v == pos_label else 0 for v in y]
    for h in feats:
        if h in id_like:
            continue
        pairs = [(r[h], yy, lab) for r, yy, lab in zip(rows_t, ybin, y) if not is_missing(r[h])]
        if len(pairs) < 4:
            continue
        kind = column_kind([p[0] for p in pairs])
        if kind == "numeric" and binary:
            a = roc_auc([p[1] for p in pairs], [to_float(p[0]) for p in pairs])
            if a is not None and max(a, 1 - a) >= auc_flag:
                add("WARN", "target-leak-suspect", "numeric %r alone separates the target (AUC=%.3f >= %.2f): confirm the value existed "
                    "BEFORE prediction time; if it is a consequence of the outcome (treatment, status, result), drop it" % (h, a, auc_flag))
        elif kind == "categorical":
            groups = defaultdict(Counter)
            for val, _, lab in pairs:
                groups[val][lab] += 1
            if 2 <= len(groups) < len(pairs) / 2:
                purity = sum(max(c.values()) for c in groups.values()) / len(pairs)
                if purity >= purity_flag:
                    add("WARN", "target-leak-suspect", "categorical %r determines the target (purity=%.3f >= %.2f over %d levels): "
                        "confirm it was known before prediction time" % (h, purity, purity_flag, len(groups)))
    # ---- duplicates
    sig = lambda r: tuple((h, r[h]) for h in feats)  # noqa: E731
    seen = Counter(sig(r) + (("__y__", r[target]),) for r in rows_t)
    dups = sum(c - 1 for c in seen.values() if c > 1)
    if dups:
        add("WARN", "duplicates", "%d duplicate row(s) (same features and target): they leak across folds unless grouped" % dups)
    if split_col:
        if split_col not in header:
            raise SystemExit("split column %r not found" % split_col)
        train = {sig(r) + (("__y__", r[target]),) for r in rows_t if str(r[split_col]).strip().lower() in ("train", "training", "0")}
        test = [r for r in rows_t if str(r[split_col]).strip().lower() in ("test", "testing", "valid", "validation", "1")]
        shared = sum(1 for r in test if sig(r) + (("__y__", r[target]),) in train)
        if shared:
            add("ERROR", "train-test-overlap", "%d of %d test row(s) are identical to a training row: the test score is inflated" % (shared, len(test)))
        else:
            add("INFO", "train-test-overlap", "no test row is identical to a training row (%d test rows checked)" % len(test))
    # ---- p vs n
    p = len(feats)
    if p > n:
        add("WARN", "p-greater-than-n", "%d features > %d rows: feature selection MUST sit inside each CV fold, use regularisation "
            "(Lasso/Elastic Net), expect batch effects, and apply FDR/Bonferroni if testing features one by one" % (p, n))
    else:
        add("INFO", "p-vs-n", "%d features, %d rows (p/n=%.2f)" % (p, n, p / n if n else 0))
    return findings


# ---------------------------------------------------------------- selection-leak demo (ESL s7.10.2)
def select_features(X, y, idx, top):
    """Indices of the `top` columns with the largest |Pearson r| to the 0/1 label, computed on rows `idx` only."""
    idx = list(idx)
    m = len(idx)
    ys = [y[i] for i in idx]
    ybar = sum(ys) / m
    syy = sum((v - ybar) ** 2 for v in ys)
    scores = []
    for j in range(len(X[0])):
        col = [X[i][j] for i in idx]
        xbar = sum(col) / m
        sxx = sum((v - xbar) ** 2 for v in col)
        sxy = sum((c - xbar) * (v - ybar) for c, v in zip(col, ys))
        scores.append((abs(sxy) / ((sxx * syy) ** 0.5 or 1.0), j))
    scores.sort(reverse=True)
    return [j for _, j in scores[:top]]


def one_nn_accuracy(X, y, train, test, cols):
    correct = 0
    for t in test:
        best, lab = None, None
        for r in train:
            d = sum((X[t][j] - X[r][j]) ** 2 for j in cols)
            if best is None or d < best:
                best, lab = d, y[r]
        correct += lab == y[t]
    return correct / len(test)


def demo(n=50, p=5000, top=100, folds=5, seed=0):
    rnd = random.Random(seed)
    y = [0] * (n // 2) + [1] * (n - n // 2)
    rnd.shuffle(y)
    X = [[rnd.gauss(0, 1) for _ in range(p)] for _ in range(n)]
    fid = stratified_folds(y, folds)
    all_idx = list(range(n))
    cols_all = select_features(X, y, all_idx, top)
    wrong = right = 0.0
    for f in range(folds):
        test = [i for i in all_idx if fid[i] == f]
        train = [i for i in all_idx if fid[i] != f]
        wrong += one_nn_accuracy(X, y, train, test, cols_all) * len(test)  # screened on ALL rows (leak)
        right += one_nn_accuracy(X, y, train, test, select_features(X, y, train, top)) * len(test)  # screened in-fold
    return {"n": n, "p": p, "top": top, "folds": folds, "seed": seed, "true_signal": "none (labels independent of predictors)",
            "wrong_way_cv_accuracy": wrong / n, "right_way_cv_accuracy": right / n,
            "gap": wrong / n - right / n,
            "reading": "the 'wrong way' number is the leak; with no real signal an honest estimate sits near 0.5"}


def render(findings):
    lines = []
    for fd in findings:
        lines.append("[%-5s] %-22s %s" % (fd["severity"], fd["check"], fd["detail"]))
    n_err = sum(1 for f in findings if f["severity"] == "ERROR")
    n_warn = sum(1 for f in findings if f["severity"] == "WARN")
    lines.append("summary: %d ERROR, %d WARN" % (n_err, n_warn))
    lines.append(ADVISORY)
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", dest="json_main")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("audit")
    p.add_argument("file")
    p.add_argument("--target", required=True)
    p.add_argument("--id-cols", default="")
    p.add_argument("--split-col", default=None)
    p.add_argument("--folds", type=int, default=5)
    p.add_argument("--positive", default=None, help="positive class label for AUC checks (default: the minority class)")
    p.add_argument("--auc-flag", type=float, default=0.95)
    p.add_argument("--purity-flag", type=float, default=0.99)
    p.add_argument("--strict", action="store_true", help="exit 1 when any ERROR is found")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("demo")
    p.add_argument("--n", type=int, default=50)
    p.add_argument("--p", type=int, default=5000)
    p.add_argument("--top", type=int, default=100)
    p.add_argument("--folds", type=int, default=5)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    want_json = a.json_main or a.json
    if a.cmd == "demo":
        res = demo(a.n, a.p, a.top, a.folds, a.seed)
        if want_json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
        else:
            for k, v in res.items():
                print("%-24s %s" % (k, ("%.4f" % v) if isinstance(v, float) else v))
            print(ADVISORY)
        return 0
    header, rows = load_csv(a.file)
    ids = tuple(c for c in a.id_cols.split(",") if c)
    findings = audit(header, rows, a.target, ids, a.split_col, a.folds, a.auc_flag, a.purity_flag, a.positive)
    if want_json:
        print(json.dumps(findings, ensure_ascii=False, indent=1))
    else:
        print(render(findings))
    return 1 if a.strict and any(f["severity"] == "ERROR" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
