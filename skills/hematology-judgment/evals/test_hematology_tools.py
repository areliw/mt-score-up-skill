"""Oracle tests for hematology-judgment tools (cbc_calc, platelet_check, coag).

Expected values come from the formulas and tables in the owner's digests, applied BY HAND to small
teaching inputs (arithmetic written in each comment), not from running the code:
  503402 Clinical Hematology Lab digest: §1 RBC-index formulas + retic/RPI table, §2 MCV classes + Mentzer,
      §3 NRBC inflates WBC, §4A(2) MCV<80 / MCH<27 screen, §5 + 510403 §3.9 LAP bands, §6 coag patterns,
      mixing test, citrate 1:9 and the Hct>55 citrate formula.
  501 Hematology Lecture digest: §2 platelet estimate band 5-25 / field.
  Card hematology-judgment: Fork 1 (MCHC >36-37), Fork 4 (estimate x lab factor, citrate x dilution),
      Fork 6 + trap #9 (normal screen but bleeding), trap #10 (Hct > 55).
Must-fail controls inject the traps the card warns about; the oracle must go red.

Run from the repo root:  python -m pytest skills/hematology-judgment/evals -q
"""
import json
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import cbc_calc  # noqa: E402
import coag  # noqa: E402
import platelet_check  # noqa: E402


# ---------------------------------------------------------------- RBC indices (503402 §1, §2, §4A)
def test_indices_formulas_and_mentzer():
    # Hb 11.2, Hct 35, RBC 5.6: MCV = 35*10/5.6 = 62.5 ; MCH = 11.2*10/5.6 = 20.0 ; MCHC = 11.2*100/35 = 32.0
    # Mentzer = 62.5/5.6 = 11.1607 (< 13 -> thal-like) ; MCV < 80 -> thal screen positive
    r = cbc_calc.indices(11.2, 35, 5.6)
    assert r["mcv_fl"] == pytest.approx(62.5)
    assert r["mch_pg"] == pytest.approx(20.0)
    assert r["mchc_g_dl"] == pytest.approx(32.0)
    assert r["mentzer"] == pytest.approx(11.160714, abs=1e-5)
    assert r["mentzer_read"].startswith("< 13")
    assert r["thal_screen_positive"] is True
    assert r["mcv_class"].startswith("microcytic")


def test_mcv_class_boundaries_follow_digest_80_100():
    # Hct 40 / RBC 5.0 -> MCV 80.0 (digest: normocytic 80-100, so 80 is normo)
    assert cbc_calc.indices(13.0, 40, 5.0)["mcv_class"].startswith("normocytic")
    # Hct 45 / RBC 4.5 -> MCV 100.0 -> still normo ; Hct 45.05 / 4.5 -> 100.11 -> macro
    assert cbc_calc.indices(15.0, 45, 4.5)["mcv_class"].startswith("normocytic")
    assert cbc_calc.indices(15.0, 45.05, 4.5)["mcv_class"].startswith("macrocytic")


def test_thal_screen_fires_on_mch_alone():
    # Hb 10.4, Hct 32, RBC 4.0: MCV = 80 (not < 80) but MCH = 10.4*10/4 = 26 < 27 -> screen positive
    r = cbc_calc.indices(10.4, 32, 4.0)
    assert r["mcv_fl"] == pytest.approx(80.0) and r["mch_pg"] == pytest.approx(26.0)
    assert r["thal_screen_positive"] is True


def test_mchc_flag_names_artifact_and_spherocytosis():
    # Hb 14, Hct 37 -> MCHC = 1400/37 = 37.84 > 36 -> flag must offer BOTH readings (card Fork 1)
    r = cbc_calc.indices(14.0, 37, 4.6)
    assert r["mchc_g_dl"] == pytest.approx(37.8378, abs=1e-4)
    flag = " ".join(r["flags"])
    assert "cold agglutinin" in flag and "spherocytosis" in flag


def test_mentzer_exactly_13_is_borderline():
    # Hct 32.5, RBC 5 -> MCV 65 -> Mentzer 65/5 = 13.0 exactly -> no lean
    assert cbc_calc.indices(10.0, 32.5, 5.0)["mentzer_read"].startswith("= 13")


def test_hct_as_fraction_is_rejected():
    with pytest.raises(ValueError):
        cbc_calc.indices(11.0, 0.35, 4.5)


# ---------------------------------------------------------------- reticulocyte / RPI (503402 §1)
def test_rpi_worked_example_raw_retic_misleads():
    # retic 6 %, Hct 25: corrected = 6 * 25/45 = 3.3333 ; Hct 25 is in band 16-25 -> 2.5 days
    # RPI = 3.3333 / 2.5 = 1.3333 < 2 -> HYPOproliferative, although the raw 6 % "looks high"
    r = cbc_calc.retic(6, 25)
    assert r["corrected_retic_pct"] == pytest.approx(10 / 3)
    assert r["maturation_days"] == 2.5
    assert r["rpi"] == pytest.approx(4 / 3)
    assert "hypoproliferative" in r["verdict"]
    assert r["note"]  # the tool must say the raw % would mislead


def test_rpi_hyperproliferative():
    # retic 10 %, Hct 30: corrected = 10*30/45 = 6.6667 ; band 26-35 -> 2.0 ; RPI = 3.3333 >= 2
    r = cbc_calc.retic(10, 30)
    assert r["rpi"] == pytest.approx(10 / 3)
    assert "hyperproliferative" in r["verdict"]


@pytest.mark.parametrize("hct,days", [(45, 1.5), (36, 1.5), (35, 2.0), (26, 2.0), (25, 2.5),
                                      (16, 2.5), (15, 3.0), (10, 3.0)])
def test_maturation_table_matches_digest(hct, days):
    # 503402 §1: Hct 36-45 -> 1.5 ; 26-35 -> 2.0 ; 16-25 -> 2.5 ; <15 -> 3.0 (15 itself put in the 3.0 band)
    assert cbc_calc.maturation_days(hct) == days


def test_hct_above_table_needs_explicit_days():
    with pytest.raises(ValueError):
        cbc_calc.maturation_days(48)
    # with an explicit value the user owns the choice: 2 * 48/45 / 1.0 = 2.1333
    assert cbc_calc.retic(2, 48, mat_days=1.0)["rpi"] == pytest.approx(2 * 48 / 45)


def test_must_fail_control_rpi_without_hct_correction(monkeypatch):
    """Inject the trap: RPI from the raw retic % (no anemia correction). Oracle must go red."""
    real = cbc_calc.retic

    def raw_rpi(retic_pct, hct, *a, **k):
        r = real(retic_pct, hct, *a, **k)
        r["rpi"] = retic_pct / r["maturation_days"]           # 6 / 2.5 = 2.4 -> "hyper"
        r["corrected_retic_pct"] = retic_pct
        r["verdict"] = "hyperproliferative" if r["rpi"] >= 2 else "hypoproliferative"
        return r

    monkeypatch.setattr(cbc_calc, "retic", raw_rpi)
    with pytest.raises(AssertionError):
        test_rpi_worked_example_raw_retic_misleads()


# ---------------------------------------------------------------- NRBC-corrected WBC (503402 §3)
def test_nrbc_corrected_wbc():
    # 15,000 x 100 / (100 + 25) = 12,000
    assert cbc_calc.nrbc_wbc(15000, 25)["wbc_corrected"] == pytest.approx(12000)
    assert cbc_calc.nrbc_wbc(8000, 0)["wbc_corrected"] == pytest.approx(8000)


def test_must_fail_control_nrbc_subtracted_as_percent(monkeypatch):
    """Inject the trap: treat NRBC/100 WBC as a % of WBC and subtract it (15,000 x 0.75 = 11,250)."""
    monkeypatch.setattr(cbc_calc, "nrbc_wbc",
                        lambda wbc, n: {"wbc_corrected": wbc * (1 - n / 100)})
    with pytest.raises(AssertionError):
        test_nrbc_corrected_wbc()


# ---------------------------------------------------------------- LAP score (503402 §5, 510403 §3.9)
def test_lap_score_bands():
    # grades 0..4 counts [90,8,2,0,0]: 1*8 + 2*2 = 12 -> < 20 LOW (CML-like)
    assert cbc_calc.lap([90, 8, 2, 0, 0])["score"] == pytest.approx(12)
    assert cbc_calc.lap([90, 8, 2, 0, 0])["read"].startswith("LOW")
    # [5,20,30,30,15]: 20 + 60 + 90 + 60 = 230 -> > 100 HIGH (leukemoid-like)
    assert cbc_calc.lap([5, 20, 30, 30, 15])["score"] == pytest.approx(230)
    assert cbc_calc.lap([5, 20, 30, 30, 15])["read"].startswith("HIGH")
    # [60,30,8,2,0]: 30 + 16 + 6 = 52 -> NORMAL ; boundaries 20 and 100 are normal (digest "20-100")
    assert cbc_calc.lap([60, 30, 8, 2, 0])["read"].startswith("NORMAL")
    assert cbc_calc.lap([80, 20, 0, 0, 0])["read"].startswith("NORMAL")      # score 20
    assert cbc_calc.lap([50, 0, 50, 0, 0])["read"].startswith("NORMAL")      # score 100


def test_lap_scales_when_not_100_cells():
    # 50 cells [45,4,1,0,0]: raw 4 + 2 = 6 -> per 100 = 12, and a note is printed
    r = cbc_calc.lap([45, 4, 1, 0, 0])
    assert r["score"] == pytest.approx(12) and r["note"]


def test_must_fail_control_lap_mean_grade(monkeypatch):
    """Inject the trap: report the MEAN grade (2.3) instead of the summed score (230)."""
    real = cbc_calc.lap

    def mean_grade(counts, *a, **k):
        r = real(counts, *a, **k)
        r["score"] = r["score"] / 100
        r["read"] = "LOW" if r["score"] < 20 else ("HIGH" if r["score"] > 100 else "NORMAL")
        return r

    monkeypatch.setattr(cbc_calc, "lap", mean_grade)
    with pytest.raises(AssertionError):
        test_lap_score_bands()


# ---------------------------------------------------------------- platelets (card Fork 4; 501 §2)
FIELDS = [9, 11, 10, 8, 12, 10, 9, 11, 10, 10]  # mean = 100/10 = 10 per field


def test_platelet_estimate_and_discordance():
    # 10 / field x factor 15,000 = 150,000 ; band 5-25 -> adequate
    r = platelet_check.estimate(FIELDS, 15000)
    assert r["smear_estimate"] == pytest.approx(150000)
    assert r["smear_band"].startswith("adequate")
    # analyzer 42,000: (42,000 - 150,000)/150,000 = -72 % -> beyond 25 % -> DISCORDANT, clump direction
    r = platelet_check.estimate(FIELDS, 15000, analyzer=42000, tolerance_pct=25)
    assert r["analyzer_vs_smear_pct"] == pytest.approx(-72)
    assert r["agreement"].startswith("DISCORDANT") and "clump" in r["agreement"]
    # analyzer 140,000: -6.67 % -> concordant ; 220,000: +46.7 % -> discordant, fragment direction
    assert platelet_check.estimate(FIELDS, 15000, 140000, 25)["agreement"].startswith("CONCORDANT")
    assert "fragments" in platelet_check.estimate(FIELDS, 15000, 220000, 25)["agreement"]
    # no tolerance from SOP -> no call
    assert "no call" in platelet_check.estimate(FIELDS, 15000, 42000)["agreement"]


def test_platelet_factor_has_no_default():
    with pytest.raises(SystemExit):
        platelet_check.main(["estimate", "--fields", "10", "10"])


def test_citrate_dilution_factor():
    # 3.2 % citrate 1:9 -> factor (9+1)/9 = 1.1111 ; 90,000 x 10/9 = 100,000
    r = platelet_check.citrate(90000)
    assert r["dilution_factor"] == pytest.approx(10 / 9)
    assert r["corrected_count"] == pytest.approx(100000)


def test_must_fail_control_citrate_not_multiplied(monkeypatch):
    """Inject the trap: report the citrate-tube count without the dilution factor."""
    monkeypatch.setattr(platelet_check, "citrate",
                        lambda count, *a, **k: {"dilution_factor": 1.0, "corrected_count": count})
    with pytest.raises(AssertionError):
        test_citrate_dilution_factor()


# ---------------------------------------------------------------- coagulation (card Fork 6; 503402 §6)
def test_pattern_table_rows():
    assert "FVII" in coag.pattern("18.2", "31", "normal", pt_uln=14.5, aptt_uln=35)["pattern"]
    r = coag.pattern("normal", "48", aptt_uln=35)
    assert "hemophilia" in r["pattern"] and "lupus anticoagulant" in r["pattern"]
    assert "FX / FV / FII" in coag.pattern("long", "long", "normal")["pattern"]
    assert "DIC" in coag.pattern("long", "long", "long")["pattern"]
    assert "TT not done" in coag.pattern("long", "long")["pattern"]
    assert "no screening-test pattern" in coag.pattern("normal", "normal")["pattern"]


def test_prolonged_screen_asks_for_mixing():
    assert any("mixing" in n for n in coag.pattern("long", "normal")["next"])
    assert not coag.pattern("normal", "normal")["next"]


def test_numeric_value_requires_lab_uln():
    with pytest.raises(ValueError):
        coag.pattern("18", "normal")


def test_normal_screen_with_bleeding_does_not_stop():
    # card trap #9: PT/aPTT normal but the patient bleeds -> FXIII / mild factor / fibrinolysis
    r = coag.pattern("normal", "normal", bleeding=True)
    assert "FXIII" in r["pattern"] and "do NOT stop" in r["pattern"]


def test_must_fail_control_bleeding_branch_dropped(monkeypatch):
    """Inject trap #9: ignore bleeding when the screen is normal ("reported normal, done")."""
    real = coag.pattern
    monkeypatch.setattr(coag, "pattern", lambda pt, aptt, tt=None, bleeding=False, **k: real(pt, aptt, tt, False, **k))
    with pytest.raises(AssertionError):
        test_normal_screen_with_bleeding_does_not_stop()


def test_mixing_criteria():
    # within reference: mix 34.1 <= ULN 35 -> corrected -> deficiency
    assert coag.mixing(34.1, uln=35)["verdict"].startswith("CORRECTED")
    # Rosner: (52 - 30)/68 x 100 = 32.35 > 15 -> not corrected -> inhibitor
    r = coag.mixing(52, patient=68, npp=30, rosner_cutoff=15)
    assert r["criteria"]["rosner"]["index"] == pytest.approx(2200 / 68)
    assert r["verdict"].startswith("NOT CORRECTED")
    # the two criteria disagree (52 <= 55 but index 32.35 > 15) -> DISCORDANT, not a silent pick
    assert coag.mixing(52, uln=55, patient=68, npp=30, rosner_cutoff=15)["verdict"].startswith("DISCORDANT")
    with pytest.raises(ValueError):
        coag.mixing(40)


def test_citrate_for_high_hct():
    # digest: 0.5 x (100 - 65)/55 = 17.5/55 = 0.318182 mL ; Hct 60 -> 20/55 = 0.363636 mL
    assert coag.citrate_hct(65, formula="digest")["citrate_ml"] == pytest.approx(0.318182, abs=1e-6)
    assert coag.citrate_hct(60, formula="digest")["citrate_ml"] == pytest.approx(0.363636, abs=1e-6)
    # CLSI form (default): 0.00185 x 35 x 4.5 = 0.291375 mL
    assert coag.citrate_hct(65)["citrate_ml"] == pytest.approx(0.291375)
    # Hct 55 is not > 55 -> no adjustment
    assert coag.citrate_hct(55)["adjust"] is False


def test_must_fail_control_citrate_not_adjusted(monkeypatch):
    """Inject trap #10: keep the standard 0.5 mL citrate at Hct 65."""
    monkeypatch.setattr(coag, "citrate_hct", lambda hct, *a, **k: {"adjust": False, "citrate_ml": 0.5})
    with pytest.raises(AssertionError):
        test_citrate_for_high_hct()


# ---------------------------------------------------------------- CLI contract (spec: --json + ADVISORY)
@pytest.mark.parametrize("mod,args", [
    (cbc_calc, ["retic", "--retic-pct", "6", "--hct", "25"]),
    (platelet_check, ["citrate", "--count", "90000"]),
    (coag, ["pattern", "--pt", "long", "--aptt", "normal"]),
])
def test_cli_prints_advisory_and_json(mod, args, capsys):
    assert mod.main(args) == 0
    assert "ADVISORY" in capsys.readouterr().out
    assert mod.main(["--json"] + args) == 0
    assert "ADVISORY" in json.loads(capsys.readouterr().out)["advisory"]


def test_citrate_clsi_matches_arup_worked_example():
    # ARUP worked example (CLSI H21 form): Hct 60 %, 2.7 mL tube -> blood 2.43 mL, citrate 0.27 mL;
    # C = 0.00185 x 40 x 2.43 = 0.17982 ~ 0.18 mL -> remove 0.27 - 0.18 = 0.09 mL
    r = coag.citrate_hct(60, blood_ml=2.43)
    assert r["citrate_ml"] == pytest.approx(0.17982, abs=1e-5)
    assert r["remove_from_standard_ml"] == pytest.approx(0.09, abs=0.001)


def test_must_fail_control_digest_form_as_default(monkeypatch):
    """Inject the old default (digest form). The ARUP/CLSI oracle must go red."""
    real = coag.citrate_hct
    monkeypatch.setattr(coag, "citrate_hct", lambda hct, formula="digest", **k: real(hct, formula, **k))
    with pytest.raises(AssertionError):
        test_citrate_clsi_matches_arup_worked_example()
