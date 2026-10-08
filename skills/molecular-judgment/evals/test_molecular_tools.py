"""Oracle tests for molecular-judgment tools (pcr_call, qpcr_calc).

Where the expected values come from (never from the code under test):
  - Well/run calls: card "ก่อนรัน/แปลผลเสมอ — 3 ด่าน", Fork 4 (no amplification + no IC = INVALID,
    NTC signal = whole run void, SYBR melt), Fork 5 (internal control mandatory), Fork 6 (contamination),
    trap list (heparin tube); 510415 Molecular Biology digest §9 (controls, heparin, internal control
    "กัน false-negative") and §8 (SYBR needs melt curve).
  - Curve acceptance: card Fork 5 "efficiency 90–110%, R²>0.98".
  - Efficiency arithmetic [ทั่วไป]: E = 10^(-1/slope) - 1, hand values in comments
    (slope -3.321928 -> 100.0 %; -3.6 -> 89.6 %; -3.1 -> 110.2 %; -2.8 -> 127.6 %).
  - Doubling per cycle: 510415 digest §4 "2ⁿ copies"; 510201 digest §9 "30 cycle -> ~1 พันล้าน copy"
    (2^30 = 1,073,741,824).
Must-fail controls inject the traps the card warns about and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import pcr_call  # noqa: E402
import qpcr_calc  # noqa: E402

RUN_CSV = os.path.join(SKILL, "data", "qpcr_run_teaching.csv")


def well(name, role, target, ic="absent", tube="", melt_tm=None, melt_peaks=None):
    return {"well": name, "role": role, "target_ct": target, "ic_ct": ic, "tube": tube,
            "melt_tm": melt_tm, "melt_peaks": melt_peaks}


CONTROLS = [well("PC", "pos", 28.0, 30.0), well("NTC", "ntc", None, None)]


def calls(wells, **kw):
    res = pcr_call.evaluate(wells, kw.pop("ct_cutoff", 38), **kw)
    return res, {s["well"]: s["call"] for s in res["samples"]}


# ---------------------------------------------------------------- sample-level calls (card Fork 4/5)
def test_ic_failure_is_invalid_never_negative():
    # card Fork 4: "ไม่ขึ้น amplification + internal control ก็ไม่ขึ้น = INVALID ไม่ใช่ negative"
    _, c = calls(CONTROLS + [well("S", "sample", None, None)])
    assert c["S"] == "INVALID"
    _, c = calls(CONTROLS + [well("S", "sample", None, 30.2)])
    assert c["S"] == "NEGATIVE"


def test_no_internal_control_means_no_negative_call():
    # card iron rule #1: no internal control -> may not read "negative"
    _, c = calls(CONTROLS + [well("S", "sample", None)])
    assert c["S"] == "NO-CALL"


def test_teaching_run_calls():
    # data/qpcr_run_teaching.csv, cut-off 38: S1 24.6 -> POS; S2 IC ok -> NEG; S3 no IC -> INVALID;
    # S4 39.5 > 38 -> not detected, IC ok -> NEG; S5 heparin -> REJECT (card ด่าน #1)
    res, c = calls(pcr_call.load(RUN_CSV))
    assert res["run_valid"] is True
    assert c == {"S1": "POSITIVE", "S2": "NEGATIVE", "S3": "INVALID", "S4": "NEGATIVE",
                 "S5": "REJECT SPECIMEN"}
    assert "late amplification" in [s for s in res["samples"] if s["well"] == "S4"][0]["reason"]


# ---------------------------------------------------------------- run-level gate (card Fork 4/6, ด่าน #2)
def test_ntc_signal_voids_the_whole_run():
    res, c = calls([well("PC", "pos", 28.0, 30.0), well("NTC", "ntc", 36.5, None),
                    well("S", "sample", 25.0, 30.0)])
    assert res["run_valid"] is False and c["S"] == "RUN INVALID"
    assert not any(s["reportable"] for s in res["samples"])


def test_missing_controls_or_failed_positive_control_void_the_run():
    assert calls([well("S", "sample", 25.0, 30.0)])[0]["run_valid"] is False                 # no controls
    assert calls([well("PC", "pos", None, 30.0), well("NTC", "ntc", None, None),
                  well("S", "sample", None, 30.0)])[0]["run_valid"] is False                   # PC failed


def test_cutoff_is_an_argument():
    # Ct 39.5 is POSITIVE at a cut-off of 40 and not detected at 38 -> the lab value decides
    w = CONTROLS + [well("S", "sample", 39.5, 30.0)]
    assert calls(w, ct_cutoff=40)[1]["S"] == "POSITIVE"
    assert calls(w, ct_cutoff=38)[1]["S"] == "NEGATIVE"


def test_sybr_positive_needs_a_clean_melt():
    # card Fork 3/4: SYBR binds any dsDNA -> melt must show one peak at the expected Tm
    base = [well("PC", "pos", 28.0, 30.0, melt_tm=82.4, melt_peaks=1), well("NTC", "ntc", None, None)]
    kw = dict(chemistry="sybr", melt_tm=82.5, melt_tol=1.0)
    assert calls(base + [well("S", "sample", 26.0, 30.0, melt_tm=82.3, melt_peaks=1)], **kw)[1]["S"] == "POSITIVE"
    assert calls(base + [well("S", "sample", 33.0, 30.0, melt_tm=76.0, melt_peaks=1)], **kw)[1]["S"] == "REVIEW"
    assert calls(base + [well("S", "sample", 33.0, 30.0, melt_tm=82.3, melt_peaks=2)], **kw)[1]["S"] == "REVIEW"
    assert calls(base + [well("S", "sample", 26.0, 30.0)], chemistry="sybr")[1]["S"] == "REVIEW"


def test_must_fail_control_failed_reaction_read_as_negative(monkeypatch):
    """Inject trap #1 of the card: no target + no internal control reported as NEGATIVE."""
    real = pcr_call.call_sample

    def trusting(w, *a, **k):
        if w["target_ct"] is None:
            return "NEGATIVE", "no target"
        return real(w, *a, **k)

    monkeypatch.setattr(pcr_call, "call_sample", trusting)
    with pytest.raises(AssertionError):
        test_ic_failure_is_invalid_never_negative()


def test_must_fail_control_ntc_ignored(monkeypatch):
    """Inject the contamination trap: ignore NTC amplification."""
    monkeypatch.setattr(pcr_call, "run_gate", lambda wells: [])
    with pytest.raises(AssertionError):
        test_ntc_signal_voids_the_whole_run()


# ---------------------------------------------------------------- standard curve (card Fork 5)
def test_curve_slope_efficiency_and_quantity():
    # standards from data/qpcr_standards_teaching.csv were built as Ct = 40 - 3.321928*log10(Q), rounded
    # to 2 dp -> slope ~ -3.322, efficiency ~ 100 %, R² ~ 1.
    # Unknown Ct 25.0 -> Q = 10^((25-40)/-3.321928) = 2^15 = 32,768 (each cycle earlier = 2x template)
    res = qpcr_calc.curve(qpcr_calc.load_csv(os.path.join(SKILL, "data", "qpcr_standards_teaching.csv")),
                          unknowns=[25.0, 37.2])
    assert res["slope"] == pytest.approx(-3.322, abs=0.005)
    assert res["efficiency_pct"] == pytest.approx(100.0, abs=0.5)
    assert res["acceptance"]["pass"] is True
    assert res["unknowns"][0]["quantity"] == pytest.approx(32768, rel=0.01)
    assert res["unknowns"][1]["status"].startswith("EXTRAPOLATED")   # 37.2 -> ~7 copies < lowest std 100


@pytest.mark.parametrize("slope, eff", [(-3.321928, 100.0), (-3.6, 89.574), (-3.1, 110.175), (-2.8, 127.585)])
def test_efficiency_from_slope(slope, eff):
    assert qpcr_calc.efficiency_pct(slope) == pytest.approx(eff, abs=0.01)


def test_curve_outside_card_limits_is_not_reportable():
    # slope -2.8 -> 127.6 % (> 110 %): quantities must not be reportable
    pts = [(10 ** k, 40 - 2.8 * k) for k in range(2, 7)]
    res = qpcr_calc.curve(pts, unknowns=[26.0])
    assert res["acceptance"]["pass"] is False
    assert res["unknowns"][0]["status"].startswith("NOT REPORTABLE")
    # slope -3.6 -> 89.6 % (< 90 %) also fails
    assert qpcr_calc.curve([(10 ** k, 40 - 3.6 * k) for k in range(2, 7)])["acceptance"]["pass"] is False


def test_must_fail_control_quantify_without_acceptance(monkeypatch):
    """Inject the card trap 'quantify when efficiency is poor': acceptance always passes."""
    monkeypatch.setattr(qpcr_calc, "acceptance", lambda *a, **k: {"pass": True, "problems": []})
    with pytest.raises(AssertionError):
        test_curve_outside_card_limits_is_not_reportable()


def test_curve_needs_three_levels():
    with pytest.raises(ValueError):
        qpcr_calc.curve([(1e3, 30.0), (1e5, 23.4)])


# ---------------------------------------------------------------- relative quantification + doubling
def test_ddct_hand_example():
    # dCt sample = 24-18 = 6 ; dCt calibrator = 27-18 = 9 ; ddCt = -3 ; fold = 2^3 = 8 (target 8x higher)
    r = qpcr_calc.ddct(24, 18, 27, 18)
    assert r["ddCt"] == pytest.approx(-3) and r["fold_2^-ddCt"] == pytest.approx(8)
    # with both efficiencies 100 % the corrected ratio equals 2^-ddCt
    assert qpcr_calc.ddct(24, 18, 27, 18, 100, 100)["fold_efficiency_corrected"] == pytest.approx(8)
    # target efficiency 90 %: 1.9^3 / 2^0 = 6.859 -> the 2^-ddCt shortcut overstates
    assert qpcr_calc.ddct(24, 18, 27, 18, 90, 100)["fold_efficiency_corrected"] == pytest.approx(6.859)


def test_must_fail_control_ddct_sign_flip(monkeypatch):
    """Inject the arithmetic trap 2^(+ddCt): an up-regulated target would read as 1/8."""
    real = qpcr_calc.ddct

    def flipped(*a, **k):
        r = real(*a, **k)
        r["fold_2^-ddCt"] = 2 ** r["ddCt"]
        return r

    monkeypatch.setattr(qpcr_calc, "ddct", flipped)
    with pytest.raises(AssertionError):
        test_ddct_hand_example()


def test_doubling_per_cycle_matches_digest():
    # 510201 digest §9: 30 cycles -> ~1 billion copies = 2^30 ; 510415 §4: 2^n
    assert qpcr_calc.fold(30)["template_ratio"] == 2 ** 30
    # dCt of log2(10) = 3.3219 cycles = 10-fold template difference (Ct low = more template, card Fork 4)
    assert qpcr_calc.fold(3.321928)["template_ratio"] == pytest.approx(10, rel=1e-5)
