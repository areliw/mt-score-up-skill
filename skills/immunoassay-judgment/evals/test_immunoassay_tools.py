"""Oracle tests for immunoassay-judgment tools (hbv_panel, titer, serology_algo).

Where the expected values come from (never from the code under test):
  - HBV patterns: the card's FORK 2 HBV table (5 rows) + "ตัวชี้ขาด vaccinated vs recovered = anti-HBc"
    + trap #5 (reading HBV markers one at a time); 506202 Immunology digest §14.
  - Titer: 506202 digest §15 "titer = ส่วนกลับของ dilution สูงสุดที่ยังให้ผลบวก (1:128 -> 128)";
    IMMUNODIAGNOSTIC digest §3.1 (prozone = Ab excess -> false negative -> dilute) and trap #1 (hook).
  - Fourfold rule + congenital ">= 4x flags, < 4x does NOT exclude": card FORK 2 syphilis line.
  - Syphilis traditional/reverse steps: card FORK 2 + 506202 digest §14.
  - HIV serial algorithm, < 24 months -> NAT: card FORK 2/trap #3 + IMMUNODIAGNOSTIC digest §5.4.
  - PPV worked example: IMMUNODIAGNOSTIC digest §5.4 — prevalence 0.05 %, sens 99.5 %, spec 99 %
    -> PPV 1 test ~4.7 %, 2 tests ~83 %, 3 tests ~99.8 %.
Must-fail controls inject the traps the card warns about and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import hbv_panel  # noqa: E402
import serology_algo  # noqa: E402
import titer  # noqa: E402


def hbv(hbsag, anti_hbc, anti_hbs, igm="na", months=None):
    return hbv_panel.interpret(hbsag, anti_hbc, anti_hbs, igm, months)["status"]


# ---------------------------------------------------------------- HBV panel (card FORK 2 table)
@pytest.mark.parametrize("panel, expected", [
    (("pos", "pos", "neg", "pos"), "ACUTE"),          # row 1: + / +(IgM) / -
    (("pos", "pos", "neg", "neg"), "CHRONIC"),        # row 2: + / +(IgG) / -
    (("neg", "pos", "pos"), "RECOVERED"),             # row 3: - / + / +
    (("neg", "neg", "pos"), "VACCINATED"),            # row 4: - / - / +
    (("neg", "pos", "neg", "neg"), "ISOLATED anti-HBc"),  # row 5: core-only -> follow-up
])
def test_hbv_card_table_rows(panel, expected):
    assert hbv(*panel).startswith(expected)


def test_hbv_recovered_vs_vaccinated_is_decided_by_anti_hbc():
    # card: "ตัวชี้ขาด vaccinated vs recovered = anti-HBc"
    assert hbv("neg", "pos", "pos").startswith("RECOVERED")
    assert hbv("neg", "neg", "pos").startswith("VACCINATED")
    assert hbv("neg", "na", "pos").startswith("UNDETERMINED")  # anti-HBs+ alone -> cannot tell


def test_hbv_hbsag_alone_is_not_acute_or_chronic():
    # trap #5: HBsAg+ alone does not tell acute vs chronic
    assert hbv("pos", "na", "neg").startswith("UNDETERMINED")
    assert hbv("pos", "pos", "neg").startswith("UNDETERMINED")  # IgM and duration both unknown


def test_hbv_core_window_and_duration_rule():
    # card viral-serology line: HBsAg-/anti-HBs- is not "not infected" -> IgM anti-HBc
    assert hbv("neg", "pos", "neg", "pos").startswith("CORE WINDOW")
    assert hbv("neg", "na", "neg").startswith("UNDETERMINED")
    # card row 2: chronic = HBsAg+ > 6 months (7 > 6; exactly 6 is not "> 6")
    assert hbv("pos", "pos", "neg", "na", 7).startswith("CHRONIC")
    assert hbv("pos", "pos", "neg", "na", 6).startswith("UNDETERMINED")


def test_hbv_teaching_csv_roundtrip():
    cases = hbv_panel.load_csv(os.path.join(SKILL, "data", "hbv_teaching_cases.csv"))
    got = {c[0]: hbv_panel.interpret(*c[1:])["status"].split(" ")[0] for c in cases}
    assert got["T1-acute"] == "ACUTE" and got["T3-recovered"] == "RECOVERED"
    assert got["T4-vaccinated"] == "VACCINATED" and got["T7-antiHBs-only-no-core"] == "UNDETERMINED:"


def test_must_fail_control_anti_hbs_read_alone(monkeypatch):
    """Inject trap #5: call any anti-HBs+ / HBsAg- panel 'vaccinated' without looking at anti-HBc."""
    real = hbv_panel.interpret

    def marker_by_marker(hbsag, anti_hbc, anti_hbs, igm=None, months=None):
        if hbsag == "neg" and anti_hbs == "pos":
            return {"status": "VACCINATED", "pattern": "", "provenance": "", "next_step": "", "notes": []}
        return real(hbsag, anti_hbc, anti_hbs, igm, months)

    monkeypatch.setattr(hbv_panel, "interpret", marker_by_marker)
    with pytest.raises(AssertionError):
        test_hbv_recovered_vs_vaccinated_is_decided_by_anti_hbc()


# ---------------------------------------------------------------- titer series (506202 §15, IMMUNODIAG §3.1)
def test_titer_is_reciprocal_of_highest_positive_dilution():
    # 1:2 +, 1:4 +, ..., 1:128 +, 1:256 neg -> titer 128 (digest example "1:128 -> titer 128")
    pts = [(2 ** k, 1) for k in range(1, 8)] + [(256, 0)]
    r = titer.series(pts)
    assert r["titer"] == 128 and r["endpoint_reached"] and not r["prozone"]


def test_prozone_pattern_from_teaching_csv():
    # data/rpr_prozone_series.csv: neat and 1:2 negative, 1:4..1:64 positive, 1:128 negative
    # -> negative at low dilution then positive when diluted = prozone; titer = 64
    r = titer.series(titer.load_series_csv(os.path.join(SKILL, "data", "rpr_prozone_series.csv")))
    assert r["prozone"] is True and r["titer"] == 64


def test_endpoint_not_reached_is_flagged():
    r = titer.series([(1, 2), (2, 2), (4, 1)])  # last well still positive
    assert r["endpoint_reached"] is False and r["verdict"].startswith("TITER >= 4")


# ---------------------------------------------------------------- fourfold rule (card FORK 2)
def test_fourfold_rule():
    # 1:8 -> 1:32 = 32/8 = 4x -> significant; 1:8 -> 1:16 = 2x (one 2-fold step) -> not significant
    assert titer.compare(8, 32, same_test=True)["verdict"].startswith("SIGNIFICANT RISE")
    assert titer.compare(8, 16, same_test=True)["verdict"].startswith("NOT SIGNIFICANT")
    assert titer.compare(64, 16, same_test=True)["verdict"].startswith("SIGNIFICANT FALL")  # 16/64 = 1/4


def test_congenital_less_than_4x_does_not_exclude():
    r = titer.compare(16, 32, mode="infant-vs-mother", same_test=True)   # infant 2x maternal
    assert "does NOT exclude" in r["verdict"]
    assert "meets" in titer.compare(16, 64, mode="infant-vs-mother", same_test=True)["verdict"]  # 4x


def test_cross_test_titer_comparison_warns():
    assert "warning" in titer.compare(8, 32)          # same test not confirmed
    assert "warning" not in titer.compare(8, 32, same_test=True)


def test_must_fail_control_twofold_counted_significant(monkeypatch):
    """Inject the trap: treat a 2-fold (one dilution step) change as significant."""
    real = titer.compare

    def lax_compare(t1, t2, mode="paired", same_test=False):
        res = real(t1, t2, mode, same_test)
        if mode == "paired" and t2 / t1 >= 2:
            res["verdict"] = "SIGNIFICANT RISE (>= 2x)"
        return res

    monkeypatch.setattr(titer, "compare", lax_compare)
    with pytest.raises(AssertionError):
        test_fourfold_rule()


# ---------------------------------------------------------------- hook check (IMMUNODIAG trap #1)
def test_hook_detected_when_diluted_result_exceeds_neat():
    # neat 180; 1:10 reads 95 -> 950 (+428 %) ; tolerance 20 % -> hook suspected
    assert titer.hook(180, [(10, 95)], 20)["hook_suspected"] is True
    # neat 180; 1:2 reads 92 -> 184 (+2.2 %) -> within 20 % -> no hook
    assert titer.hook(180, [(2, 92)], 20)["hook_suspected"] is False


# ---------------------------------------------------------------- syphilis algorithm (card FORK 2)
def test_syphilis_reverse_discordant_needs_second_tt():
    r = serology_algo.syphilis("reverse", ntt="NR", tt="R")
    assert r["status"].startswith("DISCORDANT") and "SECOND" in r["next_step"]
    assert r["reportable_as_positive"] is False
    assert serology_algo.syphilis("reverse", ntt="NR", tt="R", tt2="R")["status"].startswith("TT+ / NTT- / TT2+")


def test_syphilis_traditional_steps():
    assert "TT" in serology_algo.syphilis("traditional", ntt="R")["next_step"]           # NTT+ -> confirm TT
    assert serology_algo.syphilis("traditional", ntt="R")["reportable_as_positive"] is False
    assert "false-positive" in serology_algo.syphilis("traditional", ntt="R", tt="NR")["status"]  # BFP
    high = serology_algo.syphilis("traditional", ntt="NR", suspicion="high")
    assert "prozone" in high["next_step"]                                                 # trap #1


# ---------------------------------------------------------------- HIV algorithm (card FORK 2, trap #3)
def test_hiv_never_reportable_from_one_screen():
    assert serology_algo.hiv(["R"], 3)["reportable_as_positive"] is False
    assert serology_algo.hiv(["R", "R"], 3)["reportable_as_positive"] is False
    assert serology_algo.hiv(["R", "R", "R"], 3)["reportable_as_positive"] is True
    assert serology_algo.hiv(["R", "NR"], 3)["status"].startswith("DISCORDANT")
    with pytest.raises(ValueError):
        serology_algo.hiv(["R"], 1)


def test_hiv_infant_uses_nat():
    assert "NAT" in serology_algo.hiv(["R"], 3, age_months=9)["next_step"]


def test_must_fail_control_single_screen_reported(monkeypatch):
    """Inject iron rule #1's trap: report positive from one reactive screen."""
    real = serology_algo.hiv

    def screen_only(results, n_tests, age_months=None):
        if results and results[0] == "R":
            return serology_algo.step("REACTIVE", "report", reportable=True)
        return real(results, n_tests, age_months)

    monkeypatch.setattr(serology_algo, "hiv", screen_only)
    with pytest.raises(AssertionError):
        test_hiv_never_reportable_from_one_screen()


# ---------------------------------------------------------------- PPV (IMMUNODIAG §5.4 worked example)
def test_ppv_serial_matches_digest_worked_example():
    # hand check, test 1: TP = 0.995*0.0005 = 0.0004975; FP = 0.01*0.9995 = 0.009995
    #   PPV = 0.0004975 / 0.0104925 = 0.04741 (~4.7 %)
    rows = serology_algo.ppv_serial(0.0005, [(0.995, 0.99)] * 3)["rows"]
    assert rows[0]["ppv"] == pytest.approx(0.0474, abs=5e-4)
    assert rows[1]["ppv"] == pytest.approx(0.83, abs=5e-3)
    assert rows[2]["ppv"] == pytest.approx(0.998, abs=5e-4)


def test_must_fail_control_spec_taken_as_ppv(monkeypatch):
    """Inject the trap 'spec 99 % = believe the positive': PPV reported as specificity."""
    monkeypatch.setattr(serology_algo, "ppv_after_positive", lambda prior, sens, spec: spec)
    with pytest.raises(AssertionError):
        test_ppv_serial_matches_digest_worked_example()
