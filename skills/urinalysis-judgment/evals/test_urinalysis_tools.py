"""Oracle tests for urinalysis-judgment tools.

The owner has no dedicated urinalysis digest, so urine rules are oracled against the card's own
fork text (the spec), cross-checked where possible with owner digests: 505402-DIGEST-2026-05-31.md
section 5.4 (nephritic = RBC + RBC casts), 510416-DIGEST-2026-05-31.md Case 7 (red cell casts =
glomerular damage). Body-fluid rules: 503402-DIGEST-2026-05-31.md section 8 (Light's criteria list,
CSF tubes, synovial MSU/CPPD) + Light 1972 for the "any one criterion" rule. Arithmetic by hand.
Must-fail controls inject the traps the card warns about and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import fluid_calc  # noqa: E402
import ua_reconcile as ua  # noqa: E402


def findings(**s):
    return ua.evaluate(s)


def has(res, level, text):
    return any(f["level"] == level and text in (f["finding"] + " " + f["action"]) for f in res["findings"])


# ---------------------------------------------------------------- card trap #1 / #2: nitrite
def test_nitrite_negative_with_pyuria_is_not_cleared():
    # Card box "กับดัก #1" + Fork 1: nitrite negative does NOT exclude UTI -> microscopy + culture.
    r = findings(nitrite="neg", le="1+", wbc=25, wbc_max=5, bacteria="many")
    assert has(r, "FLAG", "culture")
    assert not any("excluded" in f["action"] or "unlikely" in f["action"] for f in r["findings"])


def test_nitrite_negative_alone_still_carries_caveat():
    r = findings(nitrite="neg", le="neg", wbc=1, wbc_max=5)
    assert has(r, "CAUTION", "does not exclude UTI")


def test_must_fail_control_nitrite_negative_rules_out_uti(monkeypatch):
    """Trap #2: 'nitrite/LE negative = no UTI'."""
    monkeypatch.setattr(ua, "nitrite_rule",
                        lambda nitrite, uti_signal: ("INFO", "Fork 1", "nitrite negative", "UTI unlikely")
                        if nitrite == "neg" else None)
    with pytest.raises(AssertionError):
        test_nitrite_negative_with_pyuria_is_not_cleared()


# ---------------------------------------------------------------- Fork 1 strip <-> sediment
def test_blood_positive_no_rbc_is_hemoglobin_or_myoglobin():
    # Card Fork 1 + trap #6: blood strip + with no RBC = hemoglobinuria / myoglobinuria, resolve first
    r = findings(blood="2+", rbc=0, rbc_max=2)
    assert has(r, "HOLD", "myoglobinuria")
    assert r["status"].startswith("DO NOT RELEASE")


def test_le_and_wbc_discordance_holds():
    # Card rule #1: strip and microscope must agree before report
    assert has(findings(le="neg", wbc=30, wbc_max=5), "HOLD", "leukocyte esterase negative")
    assert has(findings(le="2+", wbc=0, wbc_max=5), "HOLD", "WBC not seen")


def test_myeloma_needs_ssa_even_if_strip_protein_negative():
    # Card Fork 1 + trap #7: strip reads albumin, misses Bence-Jones
    assert has(findings(protein="neg", suspect_myeloma=True), "FLAG", "SSA")


def test_ph_over_8_and_stale_specimen():
    # Card "ก่อนแปลผล" 2 h rule + trap #1; Fork 1: pH > 8 -> stale / Proteus
    r = findings(age_h=4, ph=8.5, bacteria="many")
    assert has(r, "RECOLLECT", "not refrigerated")
    assert has(r, "CAUTION", "pH 8.5")
    assert has(r, "CAUTION", "in-vitro growth")
    # refrigerated 4 h -> no stale finding
    assert not has(findings(age_h=4, refrigerated=True), "RECOLLECT", "not refrigerated")


# ---------------------------------------------------------------- Fork 2 cells
def test_squamous_many_and_menstruation_recollect():
    # Card Fork 2 + trap #3: many squamous = contamination; RBC during menses = contamination
    assert has(findings(squamous="many"), "RECOLLECT", "squamous")
    assert has(findings(rbc=20, rbc_max=2, menstruating=True), "RECOLLECT", "menstruation")


def test_rte_and_dysmorphic_rbc_flagged():
    assert has(findings(rte=True), "FLAG", "renal tubular")
    assert has(findings(rbc=20, rbc_max=2, rbc_morph="dysmorphic"), "FLAG", "glomerular")


def test_sterile_pyuria():
    assert has(findings(wbc=20, wbc_max=5, culture="negative"), "FLAG", "TB")


# ---------------------------------------------------------------- Fork 3 casts
def test_rbc_cast_flags_glomerulonephritis():
    # Card Fork 3; 505402 section 5.4 nephritic = RBC + RBC casts; 510416 Case 7 red cell casts = glomerular
    r = findings(casts=["RBC"])
    assert has(r, "FLAG", "glomerulonephritis") and r["status"].startswith("RELEASE WITH FLAG")
    assert has(findings(casts=["muddy brown"]), "FLAG", "ATN")
    assert has(findings(casts=["hyaline"]), "INFO", "benign")


# ---------------------------------------------------------------- Fork 4 crystals
def test_calcium_oxalate_with_aki_is_emergency():
    # Card Fork 4 + trap #5: calcium oxalate + AKI -> ethylene glycol
    assert has(findings(crystals=["calcium oxalate"], aki=True, ph=6.0), "FLAG", "ethylene glycol")
    assert not has(findings(crystals=["calcium oxalate"], ph=6.0), "FLAG", "ethylene glycol")


def test_crystal_ph_consistency():
    # Card Fork 4: uric acid = acid urine; triple phosphate = alkaline urine
    assert has(findings(crystals=["uric-acid"], ph=7.8), "CAUTION", "re-identify")
    assert not has(findings(crystals=["uric-acid"], ph=5.5), "CAUTION", "re-identify")
    assert has(findings(crystals=["triple-phosphate"], ph=5.5), "CAUTION", "re-identify")


def test_pathologic_and_artifact_crystals():
    assert has(findings(crystals=["cystine"]), "FLAG", "cystinuria")
    assert has(findings(crystals=["talc"]), "INFO", "artifact")


def test_clean_ua_has_no_hold():
    r = findings(blood="neg", rbc=1, rbc_max=2, le="neg", wbc=2, wbc_max=5, nitrite="pos", ph=6.0, age_h=1)
    assert not any(f["level"] in ("HOLD", "RECOLLECT", "FLAG") for f in r["findings"])


# ---------------------------------------------------------------- Fork 5 body fluids
def test_lights_exudate_on_protein_only():
    # 3.5 / 6.5 = 0.538 > 0.5 (met); LDH 150 / 300 = 0.50 <= 0.6; 150 <= 2/3 x 250 = 166.7
    r = fluid_calc.lights(3.5, 6.5, 150, 300, 250)
    assert r["criteria"][0]["value"] == pytest.approx(0.5385, abs=1e-4)
    assert r["n_met"] == 1 and r["result"].startswith("EXUDATE")


def test_lights_transudate():
    # 1.5 / 6.5 = 0.23 ; 80 / 200 = 0.40 ; 80 <= 166.7 -> none met
    r = fluid_calc.lights(1.5, 6.5, 80, 200, 250)
    assert r["n_met"] == 0 and r["result"].startswith("TRANSUDATE")
    assert "note" in fluid_calc.lights(1.5, 6.5, 80, 200, 250, fluid_type="peritoneal")


def test_must_fail_control_lights_requires_all_three(monkeypatch):
    """Misuse: demanding ALL criteria instead of ANY one (Light 1972) turns the exudate into a transudate."""
    real = fluid_calc.lights

    def all_three(*args, **kw):
        r = real(*args, **kw)
        r["result"] = "EXUDATE" if r["n_met"] == 3 else "TRANSUDATE"
        return r

    monkeypatch.setattr(fluid_calc, "lights", all_three)
    with pytest.raises(AssertionError):
        test_lights_exudate_on_protein_only()


def test_csf_tube_clearing_is_not_decisive():
    # (12000 - 800) / 12000 = 11200 / 12000 = 93.33 % fall -> supports traumatic tap, never excludes SAH
    r = fluid_calc.csf(12000, 800, minutes_to_count=90)
    assert r["fall_pct"] == pytest.approx(93.333, abs=1e-3)
    assert "does not exclude SAH" in r["reading"]
    assert "unreliable" in r["timing"]                 # 503402 section 8: count within 1 h
    assert "SAH stays" in fluid_calc.csf(800, 900)["reading"]


def test_synovial_crystals():
    # 503402 section 8 / card Fork 5: MSU needle negative = gout; CPPD rhomboid positive = pseudogout
    assert fluid_calc.synovial("needle", "negative")["meaning"] == "gout"
    assert fluid_calc.synovial("rhomboid", "positive")["meaning"] == "pseudogout"
    assert fluid_calc.synovial("needle", "positive")["crystal"] == "INCONSISTENT"


@pytest.mark.parametrize("mod,argv", [
    (ua, ["--blood", "2+", "--rbc", "0", "--nitrite", "neg", "--le", "1+", "--wbc", "25", "--wbc-max", "5"]),
    (fluid_calc, ["lights", "--fluid-protein", "3.5", "--serum-protein", "6.5", "--fluid-ldh", "150",
                  "--serum-ldh", "300", "--ldh-uln", "250"]),
])
def test_cli_prints_advisory(mod, argv, capsys):
    assert mod.main(argv) == 0
    assert "ADVISORY" in capsys.readouterr().out


# ---------------------------------------------------------------- EQA 2569 count traps (tnc / eqa-check / pd)
# Sources: EQA round-review failure causes for body-fluid counts (DF / units / swapped IDs / analyzer background);
# PD rule WBC > 100/uL AND PMN >= 50%, ISPD 2022 peritonitis recommendations (> 50% after a dwell >= 2 h;
# short-dwell PMN fraction; diagnosis = 2 of 3). Assigned ranges below are MADE-UP teaching values:
# A1 1,800-2,400 · A2 80-120 · B1 0 · B2 700-1,000 cells/cu.mm.
# Arithmetic by hand: one large Neubauer square = 1 mm2 x 0.1 mm = 0.1 uL.
def test_tnc_undiluted_four_squares():
    r = fluid_calc.tnc(52, 4)  # 52 / 0.4 uL
    assert r["TNC_per_uL"] == pytest.approx(130.0)
    assert r["volume_counted_uL"] == pytest.approx(0.4)


def test_tnc_with_dilution_from_volumes_lands_in_a1():
    df = fluid_calc.dilution_factor(sample_ul=20, diluent_ul=80)  # 100 / 20 = 5
    assert df == pytest.approx(5.0)
    r = fluid_calc.tnc(389, 9, df)  # 389 x 5 / 0.9 = 2161.1
    assert r["TNC_per_uL"] == pytest.approx(2161.11, abs=0.01)
    assert 1800 <= r["TNC_per_uL"] <= 2400


def test_dilution_factor_rejects_fraction_and_half_volumes():
    with pytest.raises(ValueError):
        fluid_calc.dilution_factor(df=0.2)  # someone typed 1/5 as 0.2
    with pytest.raises(ValueError):
        fluid_calc.dilution_factor(sample_ul=20)  # diluent missing


def test_must_fail_control_tnc_forgets_dilution(monkeypatch):
    """EQA trap: DF dropped from the formula."""
    monkeypatch.setattr(fluid_calc, "tnc",
                        lambda cells, squares, dfactor=1.0, square_mm2=1.0, depth_mm=0.1:
                        {"TNC_per_uL": cells / (squares * square_mm2 * depth_mm), "volume_counted_uL": squares * 0.1})
    with pytest.raises(AssertionError):
        test_tnc_with_dilution_from_volumes_lands_in_a1()


def test_eqa_check_in_range():
    assert fluid_calc.eqa_check(2161, 1800, 2400)["verdict"] == "IN RANGE"


def test_eqa_check_names_the_forgotten_dilution():
    r = fluid_calc.eqa_check(432, 1800, 2400, dfactor=5)  # 432 x 5 = 2160
    assert r["verdict"] == "OUT OF RANGE"
    assert any("DF slip" in c and "too low" in c for c in r["likely_causes"])


def test_eqa_check_names_x10_and_x1000_slips():
    assert any("x10 chamber" in c for c in fluid_calc.eqa_check(21611, 1800, 2400)["likely_causes"])
    assert any("x1000 unit" in c for c in fluid_calc.eqa_check(2.16, 1800, 2400)["likely_causes"])


def test_eqa_check_catches_swapped_sample_numbers():
    r = fluid_calc.eqa_check(98, 1800, 2400, others={"A2": (80, 120)})
    assert any("swapped" in c and "A2" in c for c in r["likely_causes"])


def test_must_fail_control_swap_check_removed(monkeypatch):
    real = fluid_calc.eqa_check
    monkeypatch.setattr(fluid_calc, "eqa_check",
                        lambda reported, low, high, dfactor=None, others=None, background_limit=None:
                        real(reported, low, high, dfactor, None, background_limit))
    with pytest.raises(AssertionError):
        test_eqa_check_catches_swapped_sample_numbers()


def test_eqa_check_zero_cell_sample_points_at_background():
    r = fluid_calc.eqa_check(6, 0, 0, background_limit=10)  # sample B1 assigned 0
    assert any("background" in c for c in r["likely_causes"])
    assert any("<= your background limit" in c for c in r["likely_causes"])


def test_eqa_check_zero_cell_sample_far_above_background_is_not_background():
    r = fluid_calc.eqa_check(500, 0, 0, background_limit=10)  # 50x the limit: not background
    assert any("NOT explained by background" in c for c in r["likely_causes"])
    assert not any("-> report < LoQ" in c for c in r["likely_causes"])


def test_pd_rule_needs_both_criteria():
    assert fluid_calc.pd(240, 62)["result"].startswith("PERITONITIS SUSPECTED")
    high_mono = fluid_calc.pd(240, 30)
    assert high_mono["result"].startswith("effluent criterion not met") and "NOT exclude" in high_mono["result"]
    assert "mononuclear" in high_mono["note"]
    low = fluid_calc.pd(80, 70)  # short-dwell APD: PMN fraction counts -> never a plain "not met"
    assert low["result"].startswith("INDETERMINATE") and "dwell" in low["result"]
    assert "boundary" in fluid_calc.pd(150, 50)


def test_must_fail_control_pd_or_instead_of_and(monkeypatch):
    monkeypatch.setattr(fluid_calc, "pd", lambda wbc, neut_pct: {
        "result": "PERITONITIS SUSPECTED" if (wbc > 100 or neut_pct >= 50) else "effluent criterion not met",
        "note": "mononuclear"})
    with pytest.raises(AssertionError):
        test_pd_rule_needs_both_criteria()


@pytest.mark.parametrize("argv", [
    ["tnc", "--cells", "389", "--squares", "9", "--sample-ul", "20", "--diluent-ul", "80"],
    ["eqa-check", "--reported", "432", "--low", "1800", "--high", "2400", "--df", "5", "--other", "A2=80-120"],
    ["pd", "--wbc", "240", "--neut-pct", "62"],
])
def test_new_cli_runs_and_prints_advisory(argv, capsys):
    assert fluid_calc.main(argv) == 0
    out = capsys.readouterr().out
    assert "ADVISORY" in out


def test_cli_bad_other_exits_cleanly():
    with pytest.raises(SystemExit):
        fluid_calc.main(["eqa-check", "--reported", "5", "--low", "1", "--high", "2", "--other", "A2"])


@pytest.mark.parametrize("call", [
    lambda: fluid_calc.tnc(-5, 4),                                  # negative count
    lambda: fluid_calc.pd(240, 130),                                # PMN above 100%
    lambda: fluid_calc.eqa_check(10, 2400, 1800),                   # low > high
    lambda: fluid_calc.dilution_factor(sample_ul=20, diluent_ul=80, df=10),  # DF and volumes disagree
])
def test_malformed_input_is_rejected(call):
    with pytest.raises(ValueError):
        call()
