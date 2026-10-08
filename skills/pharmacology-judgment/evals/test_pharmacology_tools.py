"""Oracle tests for pharmacology-judgment tools (pk_calc, tdm_timing).

Where the expected values come from (never from the code under test):
  - PHARMACOLOGY digest §2: t½ = 0.7 x Vd / CL; steady state at ~4-5 t½; digoxin Vd ~641 L;
    zero-order drugs (phenytoin/ethanol/high-dose aspirin) -> conc rises steeply.
  - PHARMACOLOGY digest §10 + card Fork 7: sample at steady state; efficacy -> trough, toxicity -> peak;
    aminoglycoside -> both peak and trough; vancomycin -> AUC/MIC 400-600, not the peak/trough rule;
    digoxin + hypokalemia -> more toxic (read K+ together; digest §8c).
  - Accumulation arithmetic (hand): fraction of steady state after n t½ = 1 - 0.5^n
    -> 1: 50 %, 2: 75 %, 3: 87.5 %, 4: 93.75 %, 5: 96.875 %.
Must-fail controls inject the traps the card warns about ("เจาะผิดจังหวะ (ไม่ steady state, peak↔trough
สลับ)", vancomycin forced into the aminoglycoside rule) and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import pk_calc  # noqa: E402
import tdm_timing  # noqa: E402


def tdm(**kw):
    base = dict(drug_class="other", half_life=10.0, hours_on_regimen=60.0, sample="trough", purpose="efficacy")
    base.update(kw)
    return tdm_timing.assess(**base)


# ---------------------------------------------------------------- pk_calc (digest §2)
def test_halflife_digest_formula():
    # digoxin Vd 641 L (digest §2), CL 7.5 L/h (teaching value): t½ = 0.7*641/7.5 = 448.7/7.5 = 59.83 h
    r = pk_calc.halflife(641, 7.5)
    assert r["t_half_h_digest_0.7"] == pytest.approx(59.8267, abs=1e-3)
    assert r["t_half_h_ln2"] == pytest.approx(59.24, abs=0.01)    # 0.693147*641/7.5


@pytest.mark.parametrize("n, pct", [(1, 50.0), (2, 75.0), (3, 87.5), (4, 93.75), (5, 96.875)])
def test_fraction_of_steady_state(n, pct):
    assert pk_calc.fraction_of_steady_state(n) * 100 == pytest.approx(pct)


def test_steady_state_at_given_time():
    # t½ 40 h, 72 h on regimen -> 1.8 t½ -> 1 - 0.5^1.8 = 0.7128 (71.3 %)
    r = pk_calc.steady_state(40, hours=72)
    assert r["at_hours"]["half_lives"] == pytest.approx(1.8)
    assert r["at_hours"]["pct_of_ss"] == pytest.approx(71.28, abs=0.01)


def test_zero_order_refuses_t_half_timing():
    with pytest.raises(ValueError):
        pk_calc.steady_state(24, kinetics="zero")


# ---------------------------------------------------------------- tdm_timing: steady state (card Fork 7)
def test_sample_before_steady_state_is_not_interpretable():
    # t½ 40 h: 72 h = 1.8 t½ -> NOT at steady state ; 160 h = 4 t½ -> approaching ; 200 h = 5 t½ -> SS
    assert tdm(half_life=40, hours_on_regimen=72)["steady_state"] == "NOT AT STEADY STATE"
    assert tdm(half_life=40, hours_on_regimen=72)["verdict"] == "NOT INTERPRETABLE AS REQUESTED"
    assert tdm(half_life=40, hours_on_regimen=160)["steady_state"].startswith("APPROACHING")
    assert tdm(half_life=40, hours_on_regimen=200)["steady_state"] == "STEADY STATE"
    assert tdm(half_life=40, hours_on_regimen=200)["verdict"] == "INTERPRETABLE"


def test_must_fail_control_steady_state_after_one_half_life(monkeypatch):
    """Inject the trap 'เจาะไม่ steady state': treat 1 t½ as steady state."""
    monkeypatch.setattr(tdm_timing, "steady_state_status",
                        lambda n: "STEADY STATE" if n >= 1 else "NOT AT STEADY STATE")
    with pytest.raises(AssertionError):
        test_sample_before_steady_state_is_not_interpretable()


# ---------------------------------------------------------------- tdm_timing: which sample (card Fork 7)
def test_efficacy_trough_toxicity_peak():
    assert tdm(sample="trough", purpose="efficacy")["verdict"] == "INTERPRETABLE"
    assert tdm(sample="peak", purpose="toxicity")["verdict"] == "INTERPRETABLE"
    assert tdm(sample="peak", purpose="efficacy")["verdict"] == "NOT INTERPRETABLE AS REQUESTED"
    assert tdm(sample="trough", purpose="toxicity")["verdict"] == "NOT INTERPRETABLE AS REQUESTED"
    assert tdm(sample="random")["verdict"] == "NOT INTERPRETABLE AS REQUESTED"


def test_must_fail_control_peak_trough_swapped(monkeypatch):
    """Inject the trap 'peak↔trough สลับ'."""
    real = tdm_timing.expected_sample

    def swapped(drug_class, purpose):
        if drug_class in ("aminoglycoside", "vancomycin"):
            return real(drug_class, purpose)
        return {"peak"} if purpose == "efficacy" else {"trough"}

    monkeypatch.setattr(tdm_timing, "expected_sample", swapped)
    with pytest.raises(AssertionError):
        test_efficacy_trough_toxicity_peak()


def test_aminoglycoside_needs_peak_and_trough():
    # t½ 2.5 h x 24 h = 9.6 t½ -> steady state; one level alone is not enough
    one = tdm(drug_class="aminoglycoside", half_life=2.5, hours_on_regimen=24, sample="trough", purpose="toxicity")
    assert one["verdict"] == "NOT INTERPRETABLE AS REQUESTED"
    assert any("peak" in p for p in one["problems"])
    pair = tdm(drug_class="aminoglycoside", half_life=2.5, hours_on_regimen=24, sample="peak",
               purpose="efficacy", paired_sample="trough")
    assert pair["verdict"] == "INTERPRETABLE"


def test_vancomycin_is_auc_not_peak_trough():
    r = tdm(drug_class="vancomycin", half_life=6, hours_on_regimen=48, sample="trough")
    assert r["verdict"] == "NOT INTERPRETABLE AS REQUESTED"
    assert any("AUC" in p for p in r["problems"])


def test_must_fail_control_vancomycin_read_like_aminoglycoside(monkeypatch):
    """Inject the card trap: read vancomycin with the generic trough/peak rule (no AUC)."""
    real_assess = tdm_timing.assess

    def no_vanco_rule(**kw):
        if kw.get("drug_class") == "vancomycin":
            kw = dict(kw, drug_class="other")
        return real_assess(**kw)

    monkeypatch.setattr(tdm_timing, "assess", no_vanco_rule)
    with pytest.raises(AssertionError):
        test_vancomycin_is_auc_not_peak_trough()


# ---------------------------------------------------------------- digoxin + K+ (digest §8c, card Fork 7)
def test_digoxin_needs_k_and_flags_hypokalemia():
    base = dict(drug_class="digoxin", half_life=40, hours_on_regimen=220, sample="trough", purpose="efficacy",
                level=1.6, range_low=1, range_high=2)
    assert tdm(**base)["verdict"] == "NOT INTERPRETABLE AS REQUESTED"            # no K+
    low = tdm(k=3.1, k_low=3.5, **base)                                          # K 3.1 < lab limit 3.5
    assert low["verdict"] == "INTERPRETABLE WITH CAUTION"
    assert any("HYPOKALEMIA" in c for c in low["cautions"])
    assert low["level_vs_range"].startswith("within")
    assert tdm(k=4.0, k_low=3.5, **base)["verdict"] == "INTERPRETABLE"


def test_zero_order_is_never_plain_interpretable():
    r = tdm(drug_class="zero-order", half_life=None, hours_on_regimen=96)
    assert r["verdict"] == "INTERPRETABLE WITH CAUTION" and r["steady_state"].startswith("UNKNOWN")


def test_teaching_csv_batch():
    cases = tdm_timing.load_csv(os.path.join(SKILL, "data", "tdm_teaching_requests.csv"))
    got = {cid: tdm_timing.assess(**kw)["verdict"] for cid, kw in cases}
    assert got["R1-dig-early"] == "NOT INTERPRETABLE AS REQUESTED"      # 72/40 = 1.8 t½
    assert got["R2-dig-lowK"] == "INTERPRETABLE WITH CAUTION"
    assert got["R3-genta-1lvl"] == "NOT INTERPRETABLE AS REQUESTED"
    assert got["R4-genta-pair"] == "INTERPRETABLE"
    assert got["R7-wrong-type"] == "NOT INTERPRETABLE AS REQUESTED"
