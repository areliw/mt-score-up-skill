"""Oracle tests for method-validation-stats tools.

Expected values come from OUTSIDE the code:
  - 510403 Clinical Laboratory Practice digest §1.2 (2x2 formulas) and §2.4 (TEcalc = bias + 3SD worked
    example: glucose 0.58 + 3(1.75) = 5.83 <= TEa 10%; reference-interval verify <= 2 of 20)
  - the method-validation-stats card (trap #1 r != agreement, #2 OLS vs Deming/PB, #3 mean +/- 2SD,
    #4 PPV without prevalence, #5 repeatability vs reproducibility, #6 % agreement vs kappa)
  - hand arithmetic written in each comment on small constructed data sets
Must-fail controls inject those traps and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import math
import os
import statistics
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import diag_accuracy as da  # noqa: E402
import method_compare as mc  # noqa: E402
import validation_calc as vc  # noqa: E402


# ---------------------------------------------------------------- method_compare
def test_bland_altman_hand_example():
    # x=[10,20,30,40], y=[11,19,33,41] -> d=[1,-1,3,1]; mean 1; SS=(0+4+4+0)=8, SD=sqrt(8/3)=1.632993
    # LoA = 1 +/- 1.959964*1.632993 = 1 +/- 3.200608
    ba = mc.bland_altman([10, 20, 30, 40], [11, 19, 33, 41])
    assert ba["bias"] == pytest.approx(1.0)
    assert ba["sd_diff"] == pytest.approx(math.sqrt(8 / 3))
    assert ba["loa_low"] == pytest.approx(-2.200608, abs=1e-5)
    assert ba["loa_high"] == pytest.approx(4.200608, abs=1e-5)


def test_passing_bablok_hand_example():
    # x=[1,2,3,4], y=[1,3,3,5]: pairwise slopes 2,1,4/3,0,1,2 -> sorted [0,1,1,1.333,2,2], K=0, N=6 even
    # slope = (S3 + S4)/2 = (1 + 1.3333)/2 = 1.166667
    # intercept = median(y - b x) = median(-0.1667, 0.6667, -0.5, 0.3333) = (-0.1667 + 0.3333)/2 = 0.083333
    pb = mc.passing_bablok([1, 2, 3, 4], [1, 3, 3, 5])
    assert pb["slope"] == pytest.approx(7 / 6)
    assert pb["intercept"] == pytest.approx(1 / 12)


def test_deming_hand_example_and_ols_attenuation():
    # x=[1,2,3], y=[1,3,2]: Sxx=2, Syy=2, Sxy=1
    # lambda=1: b = ((2-2) + sqrt(0 + 4*1*1)) / (2*1) = 1 ; a = 2 - 1*2 = 0
    # lambda=4: b = ((2-8) + sqrt(36 + 16)) / 2 = (-6 + 7.211103) / 2 = 0.605551
    # OLS b = Sxy/Sxx = 0.5 (attenuated because x also carries error - card trap #2)
    d1 = mc.deming([1, 2, 3], [1, 3, 2], 1.0)
    assert d1["slope"] == pytest.approx(1.0) and d1["intercept"] == pytest.approx(0.0)
    assert mc.deming([1, 2, 3], [1, 3, 2], 4.0)["slope"] == pytest.approx(0.605551, abs=1e-6)
    assert mc.ols([1, 2, 3], [1, 3, 2])["slope"] == pytest.approx(0.5)


def test_perfect_r_with_constant_bias_is_not_acceptable():
    # card trap #1: y = x + 5 on x = 1..40 -> r = 1.000 exactly, yet every result is 5 units high.
    x = [float(i) for i in range(1, 41)]
    y = [v + 5 for v in x]
    res = mc.analyse(x, y, allowable_abs=2.0)
    assert res["r_range_check_only"] == pytest.approx(1.0)
    assert res["bland_altman"]["bias"] == pytest.approx(5.0)
    assert res["verdict"].startswith("NOT ACCEPTABLE")
    assert res["bias_type"] == {"constant_bias": True, "proportional_bias": False}  # PB: slope 1, intercept 5


def test_proportional_bias_detected():
    x = [float(i) for i in range(1, 41)]
    res = mc.analyse(x, [2 * v for v in x], allowable_pct=5)
    assert res["passing_bablok"]["slope"] == pytest.approx(2.0)
    assert res["bias_type"] == {"constant_bias": False, "proportional_bias": True}


def test_decision_level_bias_and_small_n_warning():
    x = [float(i) for i in range(10, 30)]                    # n = 20
    res = mc.analyse(x, [v * 1.05 for v in x], xc=[20.0], allowable_pct=10)
    lv = res["decision_levels"][0]
    assert lv["yc"] == pytest.approx(21.0) and lv["bias_pct"] == pytest.approx(5.0)   # 1.05*20 = 21
    assert any("n = 20 < 40" in w for w in res["warnings"])
    assert res["verdict"] == "bias within the allowable limit given"


def test_no_allowable_bias_gives_no_verdict():
    x = [float(i) for i in range(1, 41)]
    assert mc.analyse(x, x)["verdict"].startswith("NO VERDICT")


def test_must_fail_control_r_as_agreement(monkeypatch):
    """Inject trap #1: 'r >= 0.99 so the methods agree'. The oracle must go red."""
    def by_r(ba, levels, allowable_abs=None, allowable_pct=None, r=None):
        return "bias within the allowable limit given" if r is not None and r >= 0.99 else "NOT ACCEPTABLE"

    monkeypatch.setattr(mc, "agreement_verdict", by_r)
    with pytest.raises(AssertionError):
        test_perfect_r_with_constant_bias_is_not_acceptable()


def test_must_fail_control_ols_instead_of_deming(monkeypatch):
    """Inject trap #2: OLS used where Deming belongs. The oracle must go red."""
    monkeypatch.setattr(mc, "deming", lambda x, y, lam=1.0: mc.ols(x, y))
    with pytest.raises(AssertionError):
        test_deming_hand_example_and_ols_attenuation()


# ---------------------------------------------------------------- validation_calc
def test_precision_components_hand_example():
    # day1 [10,12], day2 [14,16]; grand mean 13; day means 11, 15
    # SS_within = 1+1+1+1 = 4, df 2 -> MS_w = 2 -> repeatability SD = sqrt(2) = 1.414214
    # SS_between = 2*(4+4) = 16, df 1 -> MS_b = 16 ; n0 = 2 -> var_between = (16-2)/2 = 7
    # within-lab SD = sqrt(2 + 7) = 3.0 ; lumped SD of all 4 values = sqrt(20/3) = 2.581989 (neither)
    p = vc.precision({"D1": [10, 12], "D2": [14, 16]})
    assert p["repeatability_sd"] == pytest.approx(math.sqrt(2))
    assert p["between_day_sd"] == pytest.approx(math.sqrt(7))
    assert p["within_lab_sd"] == pytest.approx(3.0)
    assert p["lumped_sd_do_not_use"] == pytest.approx(math.sqrt(20 / 3))


def test_precision_tea_fractions():
    # 510403 §2.4: within-run < 0.25 TEa, between-run (within-lab) < 0.33 TEa.
    # grand mean 13: repeatability CV = 1.414/13 = 10.88%, within-lab CV = 3/13 = 23.08%
    p = vc.precision({"D1": [10, 12], "D2": [14, 16]}, tea=50)       # limits 12.5% and 16.5%
    assert p["repeatability_ok"] is True and p["within_lab_ok"] is False


def test_total_error_digest_worked_example():
    # 510403 §2.4: glucose 0.58 + 3(1.75) = 5.83 <= TEa 10% -> acceptable
    te = vc.total_error(0.58, 1.75, 10)
    assert te["te_calc"] == pytest.approx(5.83) and te["acceptable"] is True
    assert vc.total_error(-0.58, 1.75, 10)["te_calc"] == pytest.approx(5.83)   # |bias|


def test_refint_verify_two_of_twenty():
    inside = [4.0] * 18
    assert vc.refint_verify(inside + [3.0, 6.0], 3.5, 5.1)["verdict"].startswith("PASS")   # 2 outside
    assert vc.refint_verify(inside[:17] + [3.0, 6.0, 7.0], 3.5, 5.1)["verdict"].startswith("FAIL")  # 3
    assert vc.refint_verify(inside[:19], 3.5, 5.1)["verdict"].startswith("NO VERDICT")    # n = 19


def test_refint_estimate_nonparametric_ranks():
    # values 1..120: rank 0.025*121 = 3.025 -> 3.025 ; rank 0.975*121 = 117.975 -> 117.975
    r = vc.refint_estimate([float(i) for i in range(1, 121)])
    assert r["low_2.5"] == pytest.approx(3.025) and r["high_97.5"] == pytest.approx(117.975)
    assert r["valid_n"] is True
    assert vc.refint_estimate([float(i) for i in range(1, 120)])["valid_n"] is False   # n = 119


def test_must_fail_control_lumped_sd_as_repeatability(monkeypatch):
    """Inject trap #5: one SD of everything reported as repeatability. The oracle must go red."""
    real = vc.precision

    def lumped(groups, tea=None):
        out = real(groups, tea)
        out["repeatability_sd"] = statistics.stdev([v for g in groups.values() for v in g])
        return out

    monkeypatch.setattr(vc, "precision", lumped)
    with pytest.raises(AssertionError):
        test_precision_components_hand_example()


def test_must_fail_control_mean_2sd_interval(monkeypatch):
    """Inject trap #3: reference interval = mean +/- 2SD. The oracle must go red."""
    def parametric(values):
        m, s = statistics.fmean(values), statistics.stdev(values)
        return {"low_2.5": m - 2 * s, "high_97.5": m + 2 * s, "valid_n": len(values) >= 120}

    monkeypatch.setattr(vc, "refint_estimate", parametric)
    with pytest.raises(AssertionError):
        test_refint_estimate_nonparametric_ranks()


# ---------------------------------------------------------------- diag_accuracy
def test_two_by_two_digest_formulas():
    # 510403 §1.2 with a=90 b=10 c=10 d=890: sens 90/100, spec 890/900, PPV 90/100, NPV 890/900
    # LR+ = 0.9 / (10/900) = 81 ; LR- = 0.1 / (890/900) = 0.101124 ; study prevalence 100/1000
    t = da.table(90, 10, 10, 890)
    assert t["sensitivity"] == pytest.approx(0.9)
    assert t["specificity"] == pytest.approx(890 / 900)
    assert t["ppv_at_study_prevalence"] == pytest.approx(0.9)
    assert t["npv_at_study_prevalence"] == pytest.approx(890 / 900)
    assert t["lr_pos"] == pytest.approx(81)
    assert t["lr_neg"] == pytest.approx(0.101124, abs=1e-6)
    assert t["study_prevalence"] == pytest.approx(0.1)
    lo, hi = t["sens_ci"]                                  # Wilson 90/100 -> 0.8256 - 0.9448
    assert lo == pytest.approx(0.8256, abs=1e-3) and hi == pytest.approx(0.9448, abs=1e-3)


def test_ppv_depends_on_prevalence_teaching_table():
    # per 1,000 at 1%: sick 10 -> TP 9.5, FN 0.5 ; well 990 -> FP 49.5, TN 940.5
    # PPV = 9.5 / 59 = 0.161017 ; NPV = 940.5 / 941 = 0.999469
    r = da.per_population(0.95, 0.95, 0.01)
    assert (r["tp"], r["fp"]) == (pytest.approx(9.5), pytest.approx(49.5))
    assert r["ppv"] == pytest.approx(9.5 / 59)
    assert r["npv"] == pytest.approx(940.5 / 941)
    assert r["check_ppv_via_lr"] == pytest.approx(r["ppv"])          # odds route agrees


def test_study_ppv_does_not_transfer():
    # same 2x2 (sens 0.9, spec 0.98889) at 1% prevalence: 0.009 / (0.009 + 0.011111*0.99) = 0.009/0.02 = 0.45
    t = da.table(90, 10, 10, 890, prevalence=0.01)
    assert t["ppv_at_study_prevalence"] == pytest.approx(0.9)
    assert t["at_your_prevalence"]["ppv"] == pytest.approx(0.45)


def test_kappa_hand_examples():
    # [[40,10],[5,45]]: po .85 ; pe = (50*45 + 50*55)/100^2 = .5 ; kappa = .35/.5 = .70
    assert da.kappa([[40, 10], [5, 45]])["kappa"] == pytest.approx(0.70)
    # [[90,5],[5,0]]: 90% agreement but pe = (95*95 + 5*5)/10000 = .905 -> kappa = -.005/.095 = -0.052632
    k = da.kappa([[90, 5], [5, 0]])
    assert k["percent_agreement"] == pytest.approx(90.0)
    assert k["kappa"] == pytest.approx(-0.005 / 0.095)


def test_must_fail_control_ppv_ignores_prevalence(monkeypatch):
    """Inject trap #4: PPV quoted without prevalence (study/50% value reused). The oracle must go red."""
    monkeypatch.setattr(da, "ppv_at", lambda sens, spec, prev: {"ppv": sens * 0.5 / (sens * 0.5 + (1 - spec) * 0.5),
                                                                "npv": None})
    with pytest.raises(AssertionError):
        test_study_ppv_does_not_transfer()


def test_must_fail_control_percent_agreement_as_kappa(monkeypatch):
    """Inject trap #6: % agreement reported as kappa. The oracle must go red."""
    real = da.kappa
    monkeypatch.setattr(da, "kappa", lambda m: dict(real(m), kappa=real(m)["po"]))
    with pytest.raises(AssertionError):
        test_kappa_hand_examples()
