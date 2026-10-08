"""Oracle tests for scripts/power_calc.py.

Expected numbers come from places other than this code:
  CARD  = worked examples printed in the sample-size-power card (each re-derived by hand below)
  COHEN = Cohen (1988) Statistical Power Analysis, 2nd ed.: Table 2.4.1 (d = .50, alpha .05 two-tailed,
          power .80 -> n = 64 per group) and Table 3.4.1 (r = .30, same alpha/power -> n = 85)
  GPOWER= G*Power 3 gives the same 64 per group (independent t test) and 34 pairs (paired t test, d = .5)
  229711= z values in the CMU 229711 digest: 1.645 (5% one-sided), 1.96, 2.576
  HAND  = arithmetic written in the comment next to each assertion (exact z: 1.959964, 0.841621)
Must-fail controls inject the traps the card warns about and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import json
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import power_calc  # noqa: E402


# ---------------------------------------------------------------- estimation (card A, B)
def test_prevalence_n_card_example():
    # CARD A: p=0.2, E=0.05, 95%.  HAND: 1.959964^2 = 3.841459; x 0.2 x 0.8 = 0.614633; / 0.0025 = 245.85 -> 246
    r = power_calc.n_prop_ci(0.2, 0.05)
    assert r["n_raw"] == pytest.approx(245.85, abs=0.01)
    assert r["n"] == 246


def test_prevalence_unknown_p_uses_half():
    # HAND: 3.841459 x 0.25 / 0.0025 = 384.146 -> 385 (the textbook "384.16 -> 385")
    r = power_calc.n_prop_ci(0.5, 0.05)
    assert r["n_raw"] == pytest.approx(384.146, abs=0.01)
    assert r["n"] == 385


def test_mean_ci_n_card_example():
    # CARD B: sd=10, E=2.  HAND: (1.959964 x 10 / 2)^2 = 9.79982^2 = 96.04 -> 97
    r = power_calc.n_mean_ci(10, 2)
    assert r["n_raw"] == pytest.approx(96.036, abs=0.01)
    assert r["n"] == 97


# ---------------------------------------------------------------- comparison (card C-F)
def test_two_means_cohen_d_half():
    # HAND: (1.959964 + 0.841621)^2 = 2.801585^2 = 7.84888; x 2 = 15.6978; / d^2 (0.25) = 62.79 -> 63
    r = power_calc.n_two_means(5, 10)
    assert r["inputs"]["d"] == pytest.approx(0.5)
    assert r["n_raw"] == pytest.approx(62.79, abs=0.01)
    assert r["n"] == 63
    # COHEN Table 2.4.1 / GPOWER say 64: the Guenther t-adjustment (+ za^2/4 = 0.96) and Lehr's 16/d^2 both reach it
    assert r["t_adjusted_n"] == 64
    assert r["lehr_16_over_d2"] == 64  # CARD C shortcut: 16 / 0.25


def test_paired_uses_sd_of_differences():
    # HAND: 7.84888 x 10^2 / 5^2 = 31.40 -> 32 (normal); + za^2/2 = 1.92 -> 33.32 -> 34 = GPOWER paired t, d = .5
    r = power_calc.n_paired(5, 10)
    assert r["n_raw"] == pytest.approx(31.40, abs=0.01)
    assert r["t_adjusted_n"] == 34


def test_two_proportions_card_example():
    # CARD E: p1=.3, p2=.5 -> about 93/group.
    # HAND: pbar=.4; za sqrt(2 x .4 x .6)=1.959964 x .692820=1.35790; zb sqrt(.21+.25)=.841621 x .678233=.57082;
    #       (1.35790+.57082)^2 = 3.7199; / (.2)^2 = 92.998 -> 93
    r = power_calc.n_two_props(0.3, 0.5)
    assert r["n_raw"] == pytest.approx(93.0, abs=0.05)
    assert r["n"] == 93


def test_correlation_cohen_table():
    # HAND: C = 0.5 ln(1.3/0.7) = 0.5 x 0.619039 = 0.309520; ((2.801585)/0.309520)^2 + 3 = 81.93 + 3 = 84.93 -> 85
    r = power_calc.n_corr(0.3)
    assert r["inputs"]["C"] == pytest.approx(0.30952, abs=1e-4)
    assert r["n_raw"] == pytest.approx(84.93, abs=0.01)
    assert r["n"] == 85  # COHEN Table 3.4.1


def test_power_090_uses_z_128():
    # HAND: power .90 -> z = 1.281552; (1.959964 + 1.281552)^2 x 2 / 0.25 = 10.5074 x 8 = 84.06 -> 85
    r = power_calc.n_two_means(5, 10, power=0.90)
    assert r["z"]["z_power"] == pytest.approx(1.2816, abs=1e-4)
    assert r["n"] == 85


def test_z_table_matches_229711_digest():
    assert power_calc.z_alpha(0.05) == pytest.approx(1.96, abs=1e-3)
    assert power_calc.z_alpha(0.05, two_sided=False) == pytest.approx(1.645, abs=1e-3)
    assert power_calc.z_alpha(0.01) == pytest.approx(2.576, abs=1e-3)


# ---------------------------------------------------------------- dropout, SE vs SD, post-hoc refusal
def test_dropout_card_example():
    # CARD step 5: n=64, dropout 15% -> 64 / 0.85 = 75.29 -> 76  (NOT 64 x 1.15 = 73.6 -> 74)
    assert power_calc.inflate_dropout(64, 0.15) == 76


def test_se_to_sd_card_trap():
    # HAND: SE = sd / sqrt(n)  =>  sd = 2 x sqrt(25) = 10; feeding SE=2 as sd gives n = (1.96 x 2 / 2)^2 = 3.84 -> 4 (wrong)
    assert power_calc.se_to_sd(2, 25) == pytest.approx(10)
    right = power_calc.n_mean_ci(power_calc.se_to_sd(2, 25), 2)["n"]
    wrong = power_calc.n_mean_ci(2, 2)["n"]
    assert right == 97 and wrong == 4


def test_posthoc_is_refused_with_exit_2(capsys):
    assert power_calc.main(["posthoc"]) == 2
    assert "REFUSED" in capsys.readouterr().out


def test_cli_json_and_dropout_flag(capsys):
    assert power_calc.main(["two-means", "--delta", "5", "--sd", "10", "--dropout", "0.15", "--json"]) == 0
    res = json.loads(capsys.readouterr().out)
    assert res["n"] == 63 and res["n_enrol"] == 75  # 63 / 0.85 = 74.12 -> 75


def test_one_sided_needs_a_warning(capsys):
    power_calc.main(["two-means", "--delta", "5", "--sd", "10", "--one-sided"])
    out = capsys.readouterr().out
    assert "one-sided alpha" in out and "p-hacking" in out


def test_help_runs(capsys):
    with pytest.raises(SystemExit) as e:
        power_calc.main(["--help"])
    assert e.value.code == 0


# ---------------------------------------------------------------- must-fail controls (trap injected -> oracle must go red)
def test_must_fail_control_dropout_multiplied(monkeypatch):
    """Trap: inflate by n x (1 + rate) instead of n / (1 - rate). The dropout oracle must go red."""
    monkeypatch.setattr(power_calc, "inflate_dropout", lambda n, rate: power_calc.ceil_n(n * (1 + rate)))
    with pytest.raises(AssertionError):
        test_dropout_card_example()


def test_must_fail_control_se_used_as_sd(monkeypatch):
    """Trap: put the standard error in the sigma slot. The SE/SD oracle must go red."""
    monkeypatch.setattr(power_calc, "se_to_sd", lambda se, n: se)
    with pytest.raises(AssertionError):
        test_se_to_sd_card_trap()


def test_must_fail_control_one_sided_z_for_two_sided(monkeypatch):
    """Trap: use the one-sided z (1.645) while claiming alpha 0.05 two-sided. Prevalence oracle must go red."""
    real = power_calc.ND.inv_cdf
    monkeypatch.setattr(power_calc, "z_alpha", lambda alpha, two_sided=True: real(1 - alpha))
    with pytest.raises(AssertionError):
        test_prevalence_n_card_example()
