"""Oracle tests for lab-management-judgment tools.

Expected values come from OUTSIDE the code:
  - lab-management-judgment card rule #1 + its harder trap (>= 20 points on >= 20 days, own lot), Fork 2
    (EQA bias formula), Fork 8 (TAT KPI), Fork 9 (investigation order, single miss vs pattern)
  - LAB-MANAGEMENT digest §2 (bias = (mean lab - mean peer)/mean peer x 100; %CV = SD/mean x 100)
  - 505402 Clinical Chemistry digest §2.1 (SD with n-1); 510403 digest §2.7 (SDI formula + bands)
  - RESEARCH-METHOD digest §5.1 (skewed data -> median/percentiles, not mean)
  - hand arithmetic in the comments
Must-fail controls inject the traps the card warns about and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import math
import os
import statistics
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import eqa_eval as eq  # noqa: E402
import qc_setup_check as qs  # noqa: E402
import tat_stats as ts  # noqa: E402

BLOCK = [100, 102, 98, 101, 99]


def rows(values, days, lot="A", level="L1"):
    return [{"date": "2026-09-%02d" % (1 + (i % days)), "value": v, "lot": lot, "level": level}
            for i, v in enumerate(values)]


# ---------------------------------------------------------------- qc_setup_check (card rule #1)
def test_twenty_points_on_twenty_days_is_ready_and_stats_are_right():
    # BLOCK x4 = 20 values on 20 days: mean 100; SS = (0+4+4+1+1) x 4 = 40; SD = sqrt(40/19) = 1.450953
    r = qs.check(rows(BLOCK * 4, 20))
    g = r["groups"][0]
    assert g["verdict"].startswith("READY")
    assert g["mean"] == pytest.approx(100)
    assert g["sd"] == pytest.approx(math.sqrt(40 / 19))
    assert g["limits"]["2SD"][0] == pytest.approx(100 - 2 * math.sqrt(40 / 19))


def test_twenty_points_in_one_day_is_not_ready():
    # the harder trap under rule #1: 20 points, 1 day = within-run SD -> limits too narrow
    g = qs.check(rows(BLOCK * 4, 1))["groups"][0]
    assert g["verdict"] == "NOT READY"
    assert any("within-run" in p for p in g["problems"])


def test_too_few_points_is_not_ready():
    assert qs.check(rows(BLOCK * 3, 15))["groups"][0]["verdict"] == "NOT READY"


def test_lots_are_never_pooled():
    # 20 days of lot A + 20 days of lot B: each lot judged on its own; a note forbids carrying across lots
    r = qs.check(rows(BLOCK * 4, 20, lot="A") + rows(BLOCK * 4, 20, lot="B"))
    assert [g["lot"] for g in r["groups"]] == ["A", "B"]
    assert all(g["n"] == 20 for g in r["groups"])
    assert any("do not carry or pool" in n for n in r["notes"])


def test_missing_lot_is_not_a_pass():
    g = qs.check(rows(BLOCK * 4, 20, lot=""))["groups"][0]
    assert g["verdict"] == "NOT READY" and any("lot not recorded" in p for p in g["problems"])


def test_must_fail_control_points_counted_as_days(monkeypatch):
    """Inject the harder trap: 'I have 20 points' treated as '20 days'. The oracle must go red."""
    monkeypatch.setattr(qs, "distinct_days", lambda rs: len(rs))
    with pytest.raises(AssertionError):
        test_twenty_points_in_one_day_is_not_ready()


# ---------------------------------------------------------------- tat_stats (card Fork 8; research digest §5.1)
def tat_rows(durations, priority="routine"):
    out = []
    for i, d in enumerate(durations):
        out.append({"priority": priority, "received": "2026-10-01 08:00",
                    "reported": "2026-10-01 %02d:%02d" % (8 + (d // 60), d % 60)})
    return out


def test_percentiles_hand_example():
    # durations 10..100: inclusive rank 1+(n-1)p -> P50 = 55, P90 = rank 9.1 -> 90 + 0.1*10 = 91
    r = ts.analyse(tat_rows(list(range(10, 101, 10))), pcts=(50, 90), target=60)["overall"]
    assert r["percentiles"]["P50"] == pytest.approx(55)
    assert r["percentiles"]["P90"] == pytest.approx(91)
    assert r["pct_within_target"] == pytest.approx(60.0)          # 10..60 -> 6 of 10
    # cross-check against the stdlib definition
    q = statistics.quantiles(list(range(10, 101, 10)), n=10, method="inclusive")
    assert r["percentiles"]["P90"] == pytest.approx(q[8])


def test_skewed_tat_median_is_not_the_mean():
    # nine tests at 10 min + one lost sample at 300 min: median 10, mean 39
    r = ts.analyse(tat_rows([10] * 9 + [300]), pcts=(50,))["overall"]
    assert r["median"] == pytest.approx(10) and r["percentiles"]["P50"] == pytest.approx(10)
    assert r["mean_contrast_only"] == pytest.approx(39)


def test_bad_rows_are_counted_not_silently_dropped():
    rs = tat_rows([20, 30]) + [{"priority": "routine", "received": "2026-10-01 09:00", "reported": ""},
                               {"priority": "routine", "received": "2026-10-01 09:00", "reported": "2026-10-01 08:30"}]
    r = ts.analyse(rs)
    assert r["rows"] == 4 and r["overall"]["n"] == 2 and len(r["excluded"]) == 2
    assert "end before start" in r["excluded"][1]["why"]


def test_split_by_priority():
    r = ts.analyse(tat_rows([20, 30], "STAT") + tat_rows([60, 90], "routine"), by="priority", pcts=(50,))
    assert r["by_group"]["STAT"]["median"] == pytest.approx(25)
    assert r["by_group"]["routine"]["median"] == pytest.approx(75)


def test_must_fail_control_mean_as_tat_kpi(monkeypatch):
    """Inject the skewed-data trap: report the mean as the 'typical' TAT. The oracle must go red."""
    monkeypatch.setattr(ts, "pctile", lambda s, p: statistics.fmean(s))
    with pytest.raises(AssertionError):
        test_skewed_tat_median_is_not_the_mean()


# ---------------------------------------------------------------- eqa_eval (card Fork 2/9; 510403 §2.7)
def eqa(*specs):
    return [{"analyte": a, "round": rd, "result": str(r), "peer_mean": str(m), "peer_sd": str(s)}
            for a, rd, r, m, s in specs]


def test_bias_and_sdi_hand_example():
    # bias = (105 - 100)/100 x 100 = 5% (denominator = PEER mean) ; SDI = (105 - 100)/2.5 = 2.0
    x = eq.evaluate(eqa(("Glucose", "R1", 105, 100, 2.5)), fail_sdi=2)["rows"][0]
    assert x["bias_pct"] == pytest.approx(5.0)
    assert x["sdi"] == pytest.approx(2.0)
    assert x["status"] == "ok"                                     # |2.0| is not > 2
    assert x["sdi_band"].startswith("satisfactory")


def test_sdi_bands_from_digest():
    assert eq.sdi_band(0.4).startswith("excellent")
    assert eq.sdi_band(-1.9).startswith("satisfactory")
    assert eq.sdi_band(3.2).startswith("serious")
    assert "not banded" in eq.sdi_band(2.5)                        # 510403 §2.7 leaves 2.0-3.0 unnamed


def test_no_scheme_criterion_no_verdict():
    assert eq.evaluate(eqa(("K", "R1", 4.5, 4.0, 0.1)))["rows"][0]["status"] == "NO CRITERION"


def test_single_miss_vs_pattern():
    single = eq.evaluate(eqa(("ALT", "R1", 48, 40, 3), ("K", "R1", 4.0, 4.0, 0.1)), fail_sdi=2)
    assert single["summary"].startswith("single miss")
    two = eq.evaluate(eqa(("ALT", "R1", 48, 40, 3), ("Chol", "R1", 212, 200, 5)), fail_sdi=2)
    assert two["summary"].startswith("PATTERN") and "same direction" in two["summary"]
    repeat = eq.evaluate(eqa(("ALT", "R1", 48, 40, 3), ("ALT", "R2", 49, 41, 3)), fail_sdi=2)
    assert "2 rounds" in repeat["summary"]


def test_investigation_starts_with_clerical_not_the_instrument():
    r = eq.evaluate(eqa(("ALT", "R1", 48, 40, 3)), fail_sdi=2)
    assert r["investigation"][0].startswith("1 clerical")
    assert r["investigation"][1].startswith("2 IQC")
    assert any("PT referral" in n for n in r["never"])


def test_must_fail_control_blame_the_instrument_first(monkeypatch):
    """Inject the trap 'EQA fail = blame the analyser': investigation starts with recalibration."""
    monkeypatch.setattr(eq, "INVESTIGATION", ["1 recalibrate / call service"] + eq.INVESTIGATION)
    with pytest.raises(AssertionError):
        test_investigation_starts_with_clerical_not_the_instrument()


def test_must_fail_control_bias_over_lab_value(monkeypatch):
    """Inject a formula slip: bias divided by the lab result instead of the peer mean (5% -> 4.76%)."""
    monkeypatch.setattr(eq, "bias_pct", lambda result, peer_mean: (result - peer_mean) / result * 100.0)
    with pytest.raises(AssertionError):
        test_bias_and_sdi_hand_example()
