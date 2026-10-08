"""Oracle tests for clinchem-judgment tools.

Expected outcomes come from rule DEFINITIONS in the 505402 Clinical Chemistry Lab digest
(§2.3 Westgard table, classic vs modified algorithm; §3.1 sigma rules; §2.1 SD n-1; §1.4 OCV/RCV;
§5 Friedewald), applied by hand to small constructed series. Hand arithmetic is in the comments.
Must-fail controls inject the traps the skill warns about and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import csv
import math
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import qc_calc  # noqa: E402
import westgard  # noqa: E402


def series(points):
    """points: list of (run, level, z) with mean 100, sd 2 -> value = 100 + 2z."""
    return [{"i": i, "run": str(r), "level": lv, "value": 100 + 2 * z, "mean": 100.0, "sd": 2.0, "z": z}
            for i, (r, lv, z) in enumerate(points)]


def last(obs, **kw):
    return westgard.evaluate(obs, **kw)["runs"][-1]


# ---------------------------------------------------------------- Westgard oracle (§2.3)
def test_1_2s_alone_is_warning_not_reject():
    r = last(series([(1, "L1", 2.5), (1, "L2", 0.3)]))
    assert r["decision"] == "WARNING" and r["warning_rules"] == ["1-2s"]


def test_1_3s_rejects_random():
    r = last(series([(1, "L1", 3.2), (1, "L2", 0.1)]))
    assert "1-3s" in r["reject_rules"] and r["error_type"] == ["random"]


def test_2_2s_within_run_across_levels():
    r = last(series([(1, "L1", 2.3), (1, "L2", 2.4)]))
    assert "2-2s" in r["reject_rules"] and "systematic" in r["error_type"]


def test_2_2s_across_runs_same_level():
    r = last(series([(1, "L1", 2.2), (1, "L2", 0.0), (2, "L1", 2.1), (2, "L2", 0.4)]))
    assert "2-2s" in r["reject_rules"]


def test_r4s_within_run():
    r = last(series([(1, "L1", 2.5), (1, "L2", -2.2)]))
    assert "R-4s" in r["reject_rules"] and "random" in r["error_type"]


def test_r4s_never_across_runs():
    # run1 L1 +2.5, run2 L1 -2.5: range 5SD but in DIFFERENT runs -> not R-4s; 1-2s warning only
    r = last(series([(1, "L1", 2.5), (1, "L2", 0.0), (2, "L1", -2.5), (2, "L2", 0.2)]))
    assert "R-4s" not in r["reject_rules"]
    assert r["decision"] == "WARNING"


def test_4_1s_within_level_and_classic_gate_difference():
    pts = [(1, "L1", 1.2), (2, "L1", 1.5), (3, "L1", 1.1), (4, "L1", 1.3)]  # 4 in a row > +1SD, none > 2SD
    assert "4-1s" in last(series(pts))["reject_rules"]
    classic = last(series(pts), mode="classic")
    assert classic["decision"] == "ACCEPT" and "4-1s" in classic["note"]  # gate hides it -> note says so


def test_10x_reject_in_all_mode_warning_in_modified():
    pts = [(i, "L1", 0.3 + 0.05 * i) for i in range(1, 11)]  # 10 on the same side of the mean
    assert "10x" in last(series(pts))["reject_rules"]
    mod = last(series(pts), mode="modified")
    assert mod["decision"] == "WARNING" and "10x" in mod["warning_rules"]


def test_sigma_6_uses_1_3s_only():
    pts = [(1, "L1", 2.3), (1, "L2", 2.4)]  # 2-2s pattern
    r = last(series(pts), mode="sigma", sigma=6.2)
    assert r["reject_rules"] == [] and r["decision"] == "WARNING"
    assert last(series(pts), mode="sigma", sigma=5.1)["reject_rules"] == ["2-2s"]


def test_clean_run_accepts():
    assert last(series([(1, "L1", 0.5), (1, "L2", -1.1)]))["decision"] == "ACCEPT"


def test_csv_loader_roundtrip(tmp_path):
    p = tmp_path / "qc.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["run", "level", "value", "mean", "sd"])
        w.writerow(["2026-10-01", "L1", "106.4", "100", "2"])  # z = +3.2
        w.writerow(["2026-10-01", "L2", "200", "200", "4"])
    obs = westgard.load(str(p))
    assert obs[0]["z"] == pytest.approx(3.2)
    assert last(obs)["decision"] == "REJECT"


def test_must_fail_control_r4s_across_runs(monkeypatch):
    """Inject the trap: R-4s looking across runs. The oracle test must go red."""
    history = []

    def r4s_across(run_obs):
        history.extend(run_obs)
        hi = [o for o in history if o["z"] > 2]
        lo = [o for o in history if o["z"] < -2]
        return (hi[:1] + lo[:1]) if hi and lo else []

    monkeypatch.setattr(westgard, "rule_r4s", r4s_across)
    with pytest.raises(AssertionError):
        test_r4s_never_across_runs()


# ---------------------------------------------------------------- qc_calc oracle (§2.1 §1.4 §3 §5)
def test_stats_uses_n_minus_1():
    # [100,102,98,101,99]: mean 100, squared deviations 0+4+4+1+1 = 10, SD = sqrt(10/4) = 1.581139
    s = qc_calc.stats([100, 102, 98, 101, 99])
    assert s["mean"] == pytest.approx(100)
    assert s["sd"] == pytest.approx(math.sqrt(2.5), abs=1e-6)
    assert s["cv_pct"] == pytest.approx(1.581139, abs=1e-6)


def test_ocv_rcv_two_times_rule():
    assert qc_calc.ocv_rcv(1.5, 3.0)["pass"] is True    # exactly 2x is allowed
    assert qc_calc.ocv_rcv(1.5, 3.2)["pass"] is False


def test_sigma_metric_and_bands():
    assert qc_calc.sigma(10, 2, 1.5)["sigma"] == pytest.approx(16 / 3)   # (10-2)/1.5 = 5.333
    assert qc_calc.sigma(10, -2, 1.5)["sigma"] == pytest.approx(16 / 3)  # |bias|
    assert qc_calc.sigma(10, 1, 1.4)["band"].startswith("world class")  # 9/1.4 = 6.43
    assert qc_calc.sigma(10, 4, 2.5)["band"].startswith("poor")         # 6/2.5 = 2.4


def test_friedewald_and_tg_guard():
    assert qc_calc.ldl_friedewald(200, 50, 150)["ldl"] == pytest.approx(120)  # 200-50-30
    assert qc_calc.ldl_friedewald(200, 50, 450)["valid"] is False


def test_must_fail_control_population_sd(monkeypatch):
    """Inject the trap: SD with n instead of n-1. The oracle must go red."""
    def pop_stats(values):
        n = len(values)
        mean = sum(values) / n
        sd = math.sqrt(sum((x - mean) ** 2 for x in values) / n)
        return {"n": n, "mean": mean, "sd": sd, "cv_pct": sd / mean * 100}

    monkeypatch.setattr(qc_calc, "stats", pop_stats)
    with pytest.raises(AssertionError):
        test_stats_uses_n_minus_1()
