"""Oracle tests for ml-judgment tools (clf_metrics.py, cv_check.py).

Expected numbers come from places other than this code:
  961701 = CMU 961701 digest, "Confusion Matrix Metrics": Acc=(TP+TN)/all, P=TP/(TP+FP), R=TP/(TP+FN), F1=2PR/(P+R)
  HKP    = Han, Kamber & Pei, Data Mining: Concepts and Techniques, the cancer example in the classifier-evaluation
           section (300 positives / 9,700 negatives; TP 90, FN 210, FP 140, TN 9,560 -> accuracy 96.50%,
           sensitivity 30.00%, specificity 98.56%).  Every figure is re-derived by hand below.
  SKL    = scikit-learn documentation examples: roc_auc_score([0,0,1,1],[.1,.4,.35,.8]) = 0.75,
           average_precision_score(same) = 0.8333
  ESL    = Hastie, Tibshirani, Friedman, Elements of Statistical Learning 2nd ed. s7.10.2 (null predictors:
           screening on all rows then CV looks excellent; screening inside folds gives about chance)
  CARD   = the 2%-prevalence "predict everyone healthy" example printed in the ml-judgment card
  HAND   = arithmetic in the comment next to each assertion
Must-fail controls inject the traps the card warns about (accuracy without a baseline, PPV that ignores prevalence,
no stratification, feature selection outside the CV fold) and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import csv
import json
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import clf_metrics  # noqa: E402
import cv_check  # noqa: E402

EXAMPLE = os.path.join(SKILL, "data", "audit_example.csv")


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    return str(path)


def checks(findings, name):
    return [f for f in findings if f["check"] == name]


# ================================================================ clf_metrics
def test_accuracy_paradox_two_percent_prevalence():
    # CARD: 2% disease, model says "healthy" for everybody. HAND: 100 people, TP 0 FP 0 FN 2 TN 98
    r = clf_metrics.confusion_metrics(0, 0, 2, 98)
    assert r["accuracy"] == pytest.approx(0.98)            # 98/100
    assert r["recall"] == 0.0                              # 0/2
    assert r["precision"] is None                          # 0/0 is undefined, NOT 0
    assert r["f1"] == 0.0
    assert r["majority_baseline_accuracy"] == pytest.approx(0.98)  # max(2, 98)/100
    assert any(f.startswith("ACCURACY-TRAP") for f in r["flags"])


def test_han_kamber_cancer_example():
    r = clf_metrics.confusion_metrics(tp=90, fp=140, fn=210, tn=9560)
    assert r["accuracy"] == pytest.approx(0.9650)          # HAND: (90+9560)/10000
    assert r["recall"] == pytest.approx(0.30)              # 90/300
    assert r["specificity"] == pytest.approx(0.98557, abs=1e-5)  # 9560/9700
    assert r["precision"] == pytest.approx(0.39130, abs=1e-5)    # 90/230
    assert r["f1"] == pytest.approx(0.33962, abs=1e-5)     # 2*0.39130*0.30/(0.39130+0.30) = 0.23478/0.69130
    # the textbook's own point: 96.5% accuracy is BELOW the 97% you get by saying "no cancer" every time
    assert r["majority_baseline_accuracy"] == pytest.approx(0.97)
    assert r["accuracy_minus_baseline"] < 0
    assert any(f.startswith("ACCURACY-TRAP") for f in r["flags"])


def test_balanced_case_is_not_flagged():
    # HAND: TP 40 FP 10 FN 10 TN 40 -> acc 80/100, P = R = 40/50 = 0.8, F1 = 0.8, baseline 0.5
    r = clf_metrics.confusion_metrics(40, 10, 10, 40)
    assert (r["accuracy"], r["precision"], r["recall"], r["f1"]) == pytest.approx((0.8, 0.8, 0.8, 0.8))
    assert r["majority_baseline_accuracy"] == pytest.approx(0.5)
    assert r["flags"] == []


def test_ppv_falls_with_prevalence_at_fixed_sens_spec():
    # HAND: PPV = sens*prev / (sens*prev + (1-spec)(1-prev)),  sens = spec = 0.95
    #   prev 0.50 -> .475 / (.475 + .025)  = 0.9500
    #   prev 0.10 -> .095 / (.095 + .045)  = 0.678571
    #   prev 0.02 -> .019 / (.019 + .049)  = 0.279412
    for prev, want in ((0.5, 0.95), (0.1, 0.678571), (0.02, 0.279412)):
        assert clf_metrics.ppv_npv(0.95, 0.95, prev)["ppv"] == pytest.approx(want, abs=1e-6)


def test_roc_auc_and_average_precision_sklearn_example():
    y, s = [0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]
    assert clf_metrics.roc_auc(y, s) == pytest.approx(0.75)  # SKL; HAND: 3 of 4 positive-negative pairs ordered correctly
    # SKL; HAND: by score desc 0.8(+) 0.4(-) 0.35(+) 0.1(-): recall .5 at precision 1, recall 1 at precision 2/3
    #            AP = .5*1 + .5*(2/3) = 0.8333
    assert clf_metrics.average_precision(y, s) == pytest.approx(0.833333, abs=1e-6)


def test_ties_in_auc_count_half():
    # HAND: every score equal -> each pos/neg pair is a tie -> AUC = 0.5
    assert clf_metrics.roc_auc([1, 0, 1, 0], [0.5, 0.5, 0.5, 0.5]) == pytest.approx(0.5)


def test_high_roc_auc_but_low_average_precision_at_2pct_prevalence():
    # 20 positives (scores .80-.99) vs 980 negatives: 882 clearly low, 98 overlapping the positives (.85-.99)
    pos = [0.80 + 0.01 * i for i in range(20)]
    neg = [0.5 * i / 882 for i in range(882)] + [0.85 + 0.14 * i / 97 for i in range(98)]
    y, s = [1] * 20 + [0] * 980, pos + neg
    brute = sum((p > q) + 0.5 * (p == q) for p in pos for q in neg) / (20 * 980)  # independent pairwise definition
    assert clf_metrics.roc_auc(y, s) == pytest.approx(brute, abs=1e-12)
    assert brute > 0.93                                   # "excellent" ROC-AUC ...
    assert clf_metrics.average_precision(y, s) < 0.2      # ... while precision at useful recall is poor (prevalence is 0.02)


def test_from_csv_counts_and_cli_json(tmp_path, capsys):
    p = write_csv(tmp_path / "pred.csv", ["truth", "pred"],
                  [[1, 1], [1, 0], [0, 0], [0, 0], [0, 1], [0, 0], [0, 0], [1, 1], [0, 0], [0, 0]])
    # HAND: positives = rows 1,2,8 -> TP 2 (rows 1,8), FN 1 (row 2); FP 1 (row 5); TN 6
    assert clf_metrics.main(["--json", "from-csv", p, "--true", "truth", "--pred", "pred"]) == 0
    res = json.loads(capsys.readouterr().out)
    assert (res["tp"], res["fp"], res["fn"], res["tn"]) == (2, 1, 1, 6)
    assert res["accuracy"] == pytest.approx(0.8)          # 8/10
    assert res["majority_baseline_accuracy"] == pytest.approx(0.7)


def test_help_runs():
    for mod in (clf_metrics, cv_check):
        with pytest.raises(SystemExit) as e:
            mod.main(["--help"])
        assert e.value.code == 0


# ================================================================ cv_check
def test_stratified_folds_spread_minority_evenly():
    # HAND: 90 negatives + 10 positives, k = 5 -> every fold gets 90/5 = 18 negatives and 10/5 = 2 positives
    y = [0] * 90 + [1] * 10
    tab = cv_check.fold_table(y, cv_check.stratified_folds(y, 5), 5)
    assert all(tab[f] == {0: 18, 1: 2} for f in range(5))


def test_unshuffled_file_sorted_by_class_gives_empty_folds():
    # HAND: 100 rows sorted (90 neg then 10 pos), contiguous blocks of 20 -> folds 0-3 hold only negatives,
    #       fold 4 holds 10 negatives + 10 positives
    y = [0] * 90 + [1] * 10
    tab = cv_check.fold_table(y, cv_check.plain_folds(100, 5), 5)
    assert [tab[f][1] for f in range(5)] == [0, 0, 0, 0, 10]


def test_audit_example_file_flags_the_planted_problems():
    header, rows = cv_check.load_csv(EXAMPLE)
    f5 = cv_check.audit(header, rows, "outcome", folds=5)
    # 30 rows, 27 negative / 3 positive: 3 minority rows < 5 folds -> ERROR; 3 folds is feasible
    assert checks(f5, "fold-feasibility") and checks(f5, "fold-feasibility")[0]["severity"] == "ERROR"
    assert not checks(cv_check.audit(header, rows, "outcome", folds=3), "fold-feasibility")
    # HAND: file sorted by outcome, 6-row blocks: rows 0-23 (folds 0-3) are all negative
    assert "[0, 1, 2, 3]" in checks(f5, "no-shuffle-no-stratify")[0]["detail"]
    # sample_id is unique text -> ID-like; age is unique integers but a real measurement -> NOT ID-like
    idl = " ".join(f["detail"] for f in checks(f5, "id-like"))
    assert "'sample_id'" in idl and "'age'" not in idl
    # post_treatment_flag equals the outcome (yes iff outcome 1) -> purity 1.0 -> leak suspect
    assert any("post_treatment_flag" in f["detail"] for f in checks(f5, "target-leak-suspect"))
    # baseline accuracy = 27/30 = 0.9
    assert "0.9000" in checks(f5, "balance")[0]["detail"]


def test_numeric_leak_suspect_via_auc(tmp_path):
    # column "lab_after" separates perfectly: outcome = 1 iff i >= 10 -> AUC 1.0; column "noise" cycles 10..14 unrelated to y
    rows = [[f"r{i}", 10 + (i * 7) % 5, 100 + i if i >= 10 else 5 + i, 1 if i >= 10 else 0] for i in range(20)]
    p = write_csv(tmp_path / "d.csv", ["rid", "noise", "lab_after", "y"], rows)
    header, data = cv_check.load_csv(p)
    f = cv_check.audit(header, data, "y", folds=5)
    flagged = " ".join(x["detail"] for x in checks(f, "target-leak-suspect"))
    assert "'lab_after'" in flagged and "'noise'" not in flagged


def test_train_test_overlap_is_an_error(tmp_path):
    rows = [["a", 1, "train"], ["b", 0, "train"], ["c", 1, "train"], ["d", 0, "train"],
            ["a", 1, "test"], ["c", 1, "test"], ["e", 0, "test"]]
    p = write_csv(tmp_path / "s.csv", ["x", "y", "split"], rows)
    header, data = cv_check.load_csv(p)
    f = cv_check.audit(header, data, "y", split_col="split", folds=2)
    ov = checks(f, "train-test-overlap")[0]
    assert ov["severity"] == "ERROR" and "2 of 3 test row(s)" in ov["detail"]  # test rows a and c repeat train rows


def test_p_greater_than_n_warns(tmp_path):
    header = ["f%d" % j for j in range(6)] + ["y"]
    rows = [[(i * (j + 3)) % 11 for j in range(6)] + [i % 2] for i in range(5)]
    p = write_csv(tmp_path / "w.csv", header, rows)
    h, data = cv_check.load_csv(p)
    f = cv_check.audit(h, data, "y", folds=2)
    assert checks(f, "p-greater-than-n")  # 6 features > 5 rows


def test_roc_auc_helper_matches_sklearn_doc():
    assert cv_check.roc_auc([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]) == pytest.approx(0.75)


def test_selection_leak_demo_wrong_way_looks_great_right_way_is_chance():
    for seed in (0, 1):
        d = cv_check.demo(seed=seed)
        # ESL s7.10.2: the labels are independent of every predictor, so any honest estimate is ~0.5
        assert d["wrong_way_cv_accuracy"] >= 0.85
        assert d["right_way_cv_accuracy"] <= 0.75
        assert d["gap"] >= 0.2


# ================================================================ must-fail controls (trap injected -> oracle must go red)
def test_must_fail_control_accuracy_without_baseline(monkeypatch):
    """Trap: judge by accuracy alone (no majority baseline). The accuracy-paradox oracle must go red."""
    monkeypatch.setattr(clf_metrics, "baseline_accuracy", lambda tp, fp, fn, tn: 0.0)
    with pytest.raises(AssertionError):
        test_accuracy_paradox_two_percent_prevalence()


def test_must_fail_control_ppv_ignores_prevalence(monkeypatch):
    """Trap: quote PPV = sensitivity (as if prevalence were 50%). The prevalence oracle must go red."""
    monkeypatch.setattr(clf_metrics, "ppv_npv", lambda sens, spec, prev: {"ppv": sens, "npv": spec})
    with pytest.raises(AssertionError):
        test_ppv_falls_with_prevalence_at_fixed_sens_spec()


def test_must_fail_control_no_stratification(monkeypatch):
    """Trap: split in file order without stratifying. The even-minority-spread oracle must go red."""
    monkeypatch.setattr(cv_check, "stratified_folds", lambda labels, k: cv_check.plain_folds(len(labels), k))
    with pytest.raises(AssertionError):
        test_stratified_folds_spread_minority_evenly()


def test_must_fail_control_selection_outside_the_fold(monkeypatch):
    """Trap: pick features on ALL rows even inside the 'right way' loop. The chance-level oracle must go red."""
    real = cv_check.select_features
    monkeypatch.setattr(cv_check, "select_features", lambda X, y, idx, top: real(X, y, range(len(y)), top))
    with pytest.raises(AssertionError):
        test_selection_leak_demo_wrong_way_looks_great_right_way_is_chance()
