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
