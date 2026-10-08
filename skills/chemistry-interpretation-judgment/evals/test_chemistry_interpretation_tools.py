"""Oracle tests for chemistry-interpretation-judgment tools.

Expected values come from OUTSIDE the code: worked cases in the owner's digests
(CLINCHEM2-DIGEST-2026-06-01.md = "CLINCHEM2", 505402-DIGEST-2026-05-31.md = "505402",
510416-DIGEST-2026-05-31.md = "510416"), the card's own fork rules, the published CKD-EPI 2021
equation (Inker 2021 NEJM), and hand arithmetic written in each comment.
Must-fail controls inject the traps the card warns about and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import abg  # noqa: E402
import chem_patterns  # noqa: E402
import renal  # noqa: E402


# ---------------------------------------------------------------- ABG 5 steps (CLINCHEM2 section 6)
def test_abg_diarrhea_case_metabolic_acidosis_partial():
    # CLINCHEM2 section 6 case: diarrhea 2 days, pH 7.31 / PCO2 33 / HCO3 16 -> metabolic acidosis,
    # partially compensated (pH low; HCO3 16 < 22 moves with pH; PCO2 33 < 35 moved the other way).
    r = abg.classify(7.31, 33, 16)
    assert r["primary"] == ["metabolic"]
    assert r["result"] == "metabolic acidosis, partially compensated"


def test_abg_diarrhea_case_anion_gap_normal():
    # Digest gives AG 12.9 (normal) for this case. Electrolytes chosen by hand to reproduce it:
    # (138 + 3.9) - (113 + 16) = 141.9 - 129 = 12.9. The --ag-ref used here is test input only.
    g = abg.anion_gap(138, 113, 16, k=3.9)
    assert g["ag"] == pytest.approx(12.9)
    assert abg.classify_ag(g["ag"], (10, 20)) == "normal"


def test_abg_dka_case_high_anion_gap():
    # CLINCHEM2 section 6 DKA case: pH 7.27, HCO3 10, AG 34 (high). PCO2 not given -> 23 chosen (low).
    # Electrolytes by hand: (135 + 5) - (96 + 10) = 140 - 106 = 34.
    r = abg.classify(7.27, 23, 10)
    assert r["result"] == "metabolic acidosis, partially compensated"
    g = abg.anion_gap(135, 96, 10, k=5)
    assert g["ag"] == pytest.approx(34)
    assert abg.classify_ag(g["ag"], (10, 20)) == "high"


def test_abg_chf_case_respiratory_acidosis():
    # CLINCHEM2 section 6 case: CHF, pH 7.24 / PCO2 60 / HCO3 27 -> respiratory acidosis.
    r = abg.classify(7.24, 60, 27)
    assert r["primary"] == ["respiratory"]
    assert r["result"].startswith("respiratory acidosis")


def test_abg_fully_compensated_uses_7_40_side():
    # Step 5 definition: pH normal, both abnormal -> fully compensated; side judged against 7.40.
    # pH 7.38 (< 7.40 -> acid side), PCO2 30 (base direction), HCO3 18 (acid direction) -> metabolic.
    r = abg.classify(7.38, 30, 18)
    assert r["result"] == "metabolic acidosis, fully compensated"


def test_abg_uncompensated_and_mixed():
    # pH 7.30, PCO2 55 (acid), HCO3 24 (normal) -> respiratory acidosis, uncompensated (only one abnormal).
    assert abg.classify(7.30, 55, 24)["result"] == "respiratory acidosis, uncompensated"
    # pH 7.20, PCO2 50 (acid) and HCO3 18 (acid): both move with pH -> mixed.
    assert abg.classify(7.20, 50, 18)["result"] == "mixed respiratory + metabolic acidosis"


def test_abg_metabolic_alkalosis_urine_cl():
    # pH 7.50 high; HCO3 34 > 26 (base, moves with pH); PCO2 46 > 45 (acid, compensating).
    r = abg.classify(7.50, 46, 34)
    assert r["result"] == "metabolic alkalosis, partially compensated"
    # Card Fork 5 / CLINCHEM2 section 6: urine Cl < 10 saline-responsive, > 20 saline-resistant.
    assert abg.urine_cl_reading(6).startswith("saline-responsive")
    assert abg.urine_cl_reading(35).startswith("saline-resistant")
    assert abg.urine_cl_reading(15).startswith("between")


def test_abg_henderson_hasselbalch_check():
    # pH = 6.1 + log10(16 / (0.03 x 33)) = 6.1 + log10(16.1616) = 6.1 + 1.20848 = 7.30848
    assert abg.hh_ph(16, 33) == pytest.approx(7.30848, abs=1e-4)


def test_must_fail_control_primary_from_first_abnormal(monkeypatch):
    """Trap (card Fork 5 step 4): naming the primary from 'whichever value is abnormal' instead of
    'whichever moves WITH the pH'. In the diarrhea case PCO2 is abnormal too -> wrong answer."""
    def naive(side, resp_dir, met_dir):
        if resp_dir != "normal":
            return ["respiratory"]
        return ["metabolic"] if met_dir != "normal" else []

    monkeypatch.setattr(abg, "primary_disorders", naive)
    with pytest.raises(AssertionError):
        test_abg_diarrhea_case_metabolic_acidosis_partial()


# ---------------------------------------------------------------- renal (card Fork 2)
def test_ckd_epi_2021_hand_values():
    # Male 50 y, Scr 1.0: 142 x (1.0/0.9)^-1.200 x 0.9938^50
    #   (1.1111)^-1.2 = exp(-1.2 x 0.105361) = 0.881237 ; 0.9938^50 = exp(50 x -0.0062193) = 0.732740
    #   142 x 0.881237 x 0.732740 = 91.69  (NKF calculator shows 92 for this input)
    assert renal.ckd_epi_2021(1.0, 50, female=False) == pytest.approx(91.69, abs=0.05)
    # Female 50 y, Scr 0.7 = kappa -> both ratio terms are 1: 142 x 0.732740 x 1.012 = 105.30
    assert renal.ckd_epi_2021(0.7, 50, female=True) == pytest.approx(105.30, abs=0.05)
    # Female 40 y, Scr 0.5 < kappa: (0.5/0.7)^-0.241 = exp(0.241 x 0.336472) = 1.084469;
    #   0.9938^40 = 0.779758 ; 142 x 1.084469 x 0.779758 x 1.012 = 121.52
    assert renal.ckd_epi_2021(0.5, 40, female=True) == pytest.approx(121.52, abs=0.05)


def test_ckd_epi_refuses_children_and_umol_conversion():
    with pytest.raises(ValueError):
        renal.ckd_epi_2021(0.5, 12, female=False)
    # 88.4 umol/L = 1.0 mg/dL
    assert renal.to_mgdl(cr_umol=88.4) == pytest.approx(1.0)


def test_cockcroft_gault_formula():
    # CLINCHEM2 section 3: (140 - age) x weight / (Cr x 72), female x 0.85
    # 60 y, 72 kg, Cr 1.0: 80 x 72 / 72 = 80 mL/min ; female 80 x 0.85 = 68
    assert renal.cockcroft_gault(60, 72, 1.0, female=False) == pytest.approx(80)
    assert renal.cockcroft_gault(60, 72, 1.0, female=True) == pytest.approx(68)


def test_crcl_24h_and_complete_collection():
    # Ucr 100 mg/dL, V 1440 mL, 24 h (1440 min), Pcr 1.0: 100 x 1440 / (1.0 x 1440) = 100 mL/min
    assert renal.crcl_24h(100, 1440, 24, 1.0) == pytest.approx(100)
    # excretion = 100 mg/dL x 14.4 dL = 1440 mg/day; / 70 kg = 20.57 mg/kg/day >= 15 -> plausible
    per_kg = renal.excretion_mg_day(100, 1440, 24) / 70
    assert per_kg == pytest.approx(20.571, abs=1e-3)
    assert renal.collection_check(per_kg)["complete"] is True


def test_crcl_under_collection_flagged():
    # Card Fork 2 trap: only 720 mL saved: 100 x 7.2 = 720 mg/day / 70 = 10.29 mg/kg/day < 15 -> flag
    per_kg = renal.excretion_mg_day(100, 720, 24) / 70
    assert per_kg == pytest.approx(10.286, abs=1e-3)
    assert renal.collection_check(per_kg)["complete"] is False


def test_must_fail_control_skip_collection_check(monkeypatch):
    """Trap (card Fork 2): trusting a 24-h CrCl without checking that the collection is complete."""
    monkeypatch.setattr(renal, "collection_check", lambda per_kg, min_mgkg=15.0: {"complete": True, "verdict": ""})
    with pytest.raises(AssertionError):
        test_crcl_under_collection_flagged()


def test_bun_cr_ratio_case7():
    # 510416 Case 7: BUN 37 / Cr 1.5 = 24.7 ("25:1 = pre-renal component") -> > 20 prerenal pattern
    r = renal.bun_cr(37, 1.5)
    assert r["ratio"] == pytest.approx(24.667, abs=1e-3)
    assert r["reading"].startswith("> 20")
    assert renal.bun_cr(15, 1.0)["reading"].startswith("<= 20")   # 15:1


# ---------------------------------------------------------------- LFT / cardiac / LDL
def test_lft_case8_dili_hepatocellular_mixed_bilirubin():
    # 510416 Case 8: ALT 1220, AST 577 (ratio 0.47 -> ALT > AST hepatocellular), DB/TB 0.58 = intra-hepatic
    r = chem_patterns.lft(577, 1220, dbil=5.8, tbil=10.0)
    assert r["ast_alt_ratio"] == pytest.approx(0.473, abs=1e-3)
    assert r["ratio_reading"].startswith("ALT > AST")
    assert r["db_tb_pct"] == pytest.approx(58)
    assert r["db_tb_reading"].startswith("30-60")


def test_lft_alcoholic_ratio_and_ast_over_500():
    # CLINCHEM2 section 4: AST:ALT >= 2 alcoholic; AST > 500 -> think of another cause.
    assert chem_patterns.lft(240, 100)["ratio_reading"].startswith("AST:ALT >= 2")      # 2.4
    r = chem_patterns.lft(600, 250)                                                      # 2.4, AST > 500
    assert any("AST > 500" in n for n in r["notes"])


def test_bilirubin_bands_and_gaps():
    # CLINCHEM2 section 4 Case 2 extrahepatic obstruction: bili 25, DB 76 % -> conjugated
    assert chem_patterns.bilirubin_fraction(19, 25)["db_tb_reading"].startswith("> 70")
    # 3 / 20 = 15 % -> prehepatic (hemolysis/Gilbert)
    assert chem_patterns.bilirubin_fraction(3, 20)["db_tb_reading"].startswith("< 20")
    # 5 / 20 = 25 % and 13 / 20 = 65 % fall in the card's gaps -> not classified
    assert "not classified" in chem_patterns.bilirubin_fraction(5, 20)["db_tb_reading"]
    assert "not classified" in chem_patterns.bilirubin_fraction(13, 20)["db_tb_reading"]


def test_ckmb_index():
    # CLINCHEM2 section 5: index = CK-MB mass x 100 / total CK
    # 12 x 100 / 150 = 8 % -> cardiac band ; 20 x 100 / 2000 = 1 % -> skeletal band
    assert chem_patterns.ckmb_index(12, 150)["ckmb_index_pct"] == pytest.approx(8)
    assert chem_patterns.ckmb_index(12, 150)["band"].startswith("cardiac")
    assert chem_patterns.ckmb_index(20, 2000)["band"].startswith("skeletal")


def test_troponin_delta_case14():
    # 510416 Case 14: hs-cTnT 0 h = 10 -> 1 h = 35 ng/L, delta = 25. Cutoff below is arbitrary test input.
    r = chem_patterns.troponin_delta(10, 35, cutoff=5)
    assert r["delta"] == 25 and "significant" in r["reading"]
    assert "not judged" in chem_patterns.troponin_delta(10, 35)["reading"]


def test_friedewald_and_guards():
    # 505402 section 5.2: 200 - 50 - 150/5 = 120 ; TG >= 400 or non-fasting -> not valid
    assert chem_patterns.friedewald(200, 50, 150)["ldl"] == pytest.approx(120)
    assert "caution" in chem_patterns.friedewald(200, 50, 150)      # card Fork 7: TG >= 150 underestimates
    assert "caution" not in chem_patterns.friedewald(200, 50, 100)
    assert chem_patterns.friedewald(200, 50, 400)["valid"] is False
    assert chem_patterns.friedewald(200, 50, 450)["valid"] is False
    assert chem_patterns.friedewald(200, 50, 100, fasting=False)["valid"] is False


def test_must_fail_control_friedewald_without_tg_guard(monkeypatch):
    """Trap (card Fork 7 + anti-pattern list): using Friedewald when TG > 400."""
    monkeypatch.setattr(chem_patterns, "friedewald",
                        lambda tc, hdl, tg, fasting=True: {"ldl": tc - hdl - tg / 5, "valid": True})
    with pytest.raises(AssertionError):
        test_friedewald_and_guards()


# ---------------------------------------------------------------- CLI smoke (ADVISORY line present)
@pytest.mark.parametrize("mod,argv", [
    (abg, ["--ph", "7.31", "--pco2", "33", "--hco3", "16", "--na", "138", "--k", "3.9", "--cl", "113"]),
    (renal, ["egfr", "--cr", "1.0", "--age", "50", "--sex", "M", "--weight", "70"]),
    (chem_patterns, ["ldl", "--tc", "200", "--hdl", "50", "--tg", "150"]),
])
def test_cli_prints_advisory(mod, argv, capsys):
    assert mod.main(argv) == 0
    assert "ADVISORY" in capsys.readouterr().out
