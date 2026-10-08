"""Oracle tests for bloodbank-judgment tools (abo_rh, panel_ruleout, bb_calc).

Expected values come from the owner's course digests, NOT from the code under test:
  512303 = 06_Background_MedTech/512303-TRANSFUSION-SCIENCE-1/512303-DIGEST-2026-05-31.md
  512304 = 06_Background_MedTech/512304-TRANSFUSION-SCIENCE-2/512304-DIGEST-2026-06-01.md
  510403 = 06_Background_MedTech/510403-CLINICAL-LABORATORY-PRACTICE-66/510403-DIGEST-2026-05-31.md
Where a digest gives a rule but no number, the hand reasoning is written in the comment.
Must-fail controls inject the traps the card warns about and require the oracle test to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import csv
import json
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import abo_rh  # noqa: E402
import bb_calc  # noqa: E402
import panel_ruleout  # noqa: E402

PANEL = os.path.join(SKILL, "data", "panel_teaching_anti-E_anti-Jka.csv")

# 512303 §2.6 ABO compatibility table, transcribed independently of the code
DIGEST_RBC = {"A": {"A", "O"}, "B": {"B", "O"}, "AB": {"AB", "A", "B", "O"}, "O": {"O"}}
DIGEST_PLASMA = {"A": {"A", "AB"}, "B": {"B", "AB"}, "AB": {"AB"}, "O": {"O", "A", "B", "AB"}}


# ================================================================ abo_rh: ABO typing
@pytest.mark.parametrize("fa,fb,ra,rb,group", [
    ("4+", "0", "0", "4+", "A"),    # Landsteiner (512303 §2.1): A has anti-B
    ("0", "4+", "4+", "0", "B"),
    ("4+", "4+", "0", "0", "AB"),
    ("0", "0", "4+", "4+", "O"),
])
def test_concordant_groups(fa, fb, ra, rb, group):
    r = abo_rh.interpret_type(fa, fb, ra, rb)
    assert r["status"] == "CONCORDANT" and r["forward_group"] == group == r["reverse_group"]


def test_acquired_b_pattern_512304_case1():
    # 512304 §4 Case 1: anti-A 4+, anti-B 1+ (abnormally weak), serum = group A pattern -> acquired B,
    # transfuse group A once resolved; until then group O RBC / AB plasma (card Fork 1, Fork 7)
    r = abo_rh.interpret_type("4+", "1+", "0", "3+", auto="0")
    assert r["status"] == "DISCREPANCY"
    assert (r["forward_group"], r["reverse_group"]) == ("AB", "A")
    assert any("acquired B" in c for c in r["candidate_causes"])
    assert "group O" in r["issue_while_unresolved"] and "AB" in r["issue_while_unresolved"]


def test_a2_with_anti_a1_512304_case2():
    # 512304 §4 Case 2: cells group A, serum reacts with A1 cells (looks like O) -> Dolichos lectin
    r = abo_rh.interpret_type("4+", "0", "2+", "4+")
    assert r["status"] == "DISCREPANCY" and r["reverse_group"] == "O"
    assert any("anti-A1" in c and "Dolichos" in c for c in r["candidate_causes"])


def test_bombay_is_never_issued_group_o():
    # 512303 §2.5 / §8.2: Bombay types as O, anti-H reacts with O cells, auto-; giving O = acute
    # intravascular hemolysis (card trap #2) -> the tool must refuse group O
    r = abo_rh.interpret_type("0", "0", "4+", "4+", o_cells="3+", auto="0")
    assert r["bombay_suspect"] is True
    assert r["issue_while_unresolved"].startswith("DO NOT issue group O")


def test_cold_auto_is_not_called_bombay():
    # 512303 §8.2: cold autoantibody = screen+ AND auto+ -> prewarm; not anti-H
    r = abo_rh.interpret_type("0", "0", "4+", "4+", o_cells="2+", auto="2+")
    assert r["bombay_suspect"] is False
    assert any("cold autoantibody" in c for c in r["candidate_causes"])


def test_missing_antigen_or_antibody_gap():
    # 510403 §3.1: serologic O that was really A-weak -> forward O but serum lacks anti-A
    r = abo_rh.interpret_type("0", "0", "0", "4+")
    assert r["status"] == "DISCREPANCY" and r["reverse_group"] == "A"
    joined = " ".join(r["candidate_causes"])
    assert "RBC missing/weak A" in joined and "serum missing/weak anti-A" in joined


def test_mixed_field_forward():
    # 512303 §8.1: mixed-field = recent O transfusion / post-HSCT / A3
    r = abo_rh.interpret_type("mf", "0", "0", "4+")
    assert r["status"] == "DISCREPANCY"
    assert any("mixed-field" in c for c in r["candidate_causes"])


def test_neonate_forward_only():
    # 512303 §2.4: serum grouping only from ~3-6 months
    r = abo_rh.interpret_type("4+", "0", neonate=True)
    assert r["status"] == "FORWARD-ONLY" and r["reverse_group"] is None


def test_reverse_required_for_patient():
    assert abo_rh.interpret_type("4+", "0")["status"] == "INCOMPLETE"


# ================================================================ abo_rh: RhD (512303 §3.2, card Fork 9)
def test_patient_weak_d_transfused_d_negative():
    r = abo_rh.interpret_rh("0", d_ahg="2+", role="patient")
    assert r["transfuse_as"] == "D-negative"


def test_donor_weak_d_labelled_d_positive():
    r = abo_rh.interpret_rh("0", d_ahg="2+", role="donor")
    assert r["label_as"] == "D-positive"


def test_donor_is_negative_needs_weak_d_test():
    assert abo_rh.interpret_rh("0", role="donor")["d_status"] == "INCOMPLETE"


def test_patient_is_negative_no_weak_d_needed():
    r = abo_rh.interpret_rh("0", role="patient")
    assert r["d_status"] == "D-NEGATIVE" and r["transfuse_as"] == "D-negative"


def test_must_fail_control_weak_d_reported_positive_for_patient(monkeypatch):
    """Trap: one-line rule 'weak D = Rh positive' applied to a PATIENT (partial D -> anti-D)."""
    def naive(anti_d, d_ahg=None, role="patient", forward_min=2, auto=None):
        positive = abo_rh.pos(abo_rh.parse_grade(anti_d)) or abo_rh.pos(abo_rh.parse_grade(d_ahg))
        status = "D-positive" if positive else "D-negative"
        return {"d_status": status, "label_as": status, "transfuse_as": status, "notes": []}

    monkeypatch.setattr(abo_rh, "interpret_rh", naive)
    with pytest.raises(AssertionError):
        test_patient_weak_d_transfused_d_negative()


def test_must_fail_control_bombay_given_group_o(monkeypatch):
    """Trap: 'unresolved discrepancy -> give O' applied blindly, so Bombay is issued group O."""
    original = abo_rh.interpret_type

    def blind_o(*a, **k):
        r = original(*a, **k)
        r["bombay_suspect"] = False
        r["issue_while_unresolved"] = "RBC group O, plasma group AB"
        return r

    monkeypatch.setattr(abo_rh, "interpret_type", blind_o)
    with pytest.raises(AssertionError):
        test_bombay_is_never_issued_group_o()


# ================================================================ abo_rh: compatibility (512303 §2.6)
@pytest.mark.parametrize("recipient", ["O", "A", "B", "AB"])
def test_rbc_compat_matches_digest_table(recipient):
    assert set(abo_rh.compat(recipient, "rbc")["acceptable"]) == DIGEST_RBC[recipient]


@pytest.mark.parametrize("recipient", ["O", "A", "B", "AB"])
def test_plasma_compat_matches_digest_table(recipient):
    assert set(abo_rh.compat(recipient, "plasma")["acceptable"]) == DIGEST_PLASMA[recipient]


def test_platelet_risk_is_donor_plasma():
    # card Fork 5 + 512303 §2.6: identical first, then plasma-compatible; O platelets to A = plasma-incompatible
    p = abo_rh.compat("A", "platelet")
    assert p["preferred"] == ["A"] and set(p["acceptable"]) == {"A", "AB"}
    assert "O" in p["plasma_incompatible"]


def test_cryo_any_group_and_whole_blood_identical():
    assert set(abo_rh.compat("O", "cryo")["acceptable"]) == {"O", "A", "B", "AB"}
    assert abo_rh.compat("B", "wb")["acceptable"] == ["B"]


def test_unknown_recipient_universal_donors():
    # 512303 §2.6: O = universal RBC donor, AB = universal plasma donor; card Fork 7: D-negative if unknown
    rbc = abo_rh.compat("unknown", "rbc", rh="unknown")
    assert rbc["acceptable"] == ["O"] and rbc["rh_rbc"]["acceptable"] == ["D-negative"]
    assert abo_rh.compat("unknown", "plasma")["acceptable"] == ["AB"]


def test_must_fail_control_group_o_plasma_to_group_a(monkeypatch):
    """Trap: treating O as 'universal' for plasma too -> anti-A in O plasma given to an A recipient."""
    bad = dict(abo_rh.PLASMA_COMPAT)
    bad["A"] = ["A", "AB", "O"]
    monkeypatch.setattr(abo_rh, "PLASMA_COMPAT", bad)
    with pytest.raises(AssertionError):
        test_plasma_compat_matches_digest_table("A")


# ================================================================ panel_ruleout (512304 §3, 510403 §3.3)
def teaching_panel(**kw):
    antigens, cells = panel_ruleout.load(PANEL)
    return panel_ruleout.analyse(antigens, cells, auto="0", **kw)


def test_teaching_panel_crossout():
    # Hand cross-out of data/panel_teaching_anti-E_anti-Jka.csv: non-reactive cells 3,5,6,7,10.
    # Homozygous non-reactive cells exclude C(10) c(5,6) e(3,5,6,7,10) M(10) N(5,7) S(7) s(6,10)
    # k(5,7,10) Fya(6) Fyb(5,7) Jkb(3,5,7,10); D/P1/Lea/Leb have no dosage partner -> any cell.
    # Jka+ non-reactive cell 6 is Jk(a+b+) and K+ cells 3,6 are K+k+ -> NOT excluded (dosage rule).
    r = teaching_panel()
    assert set(r["candidates"]) == {"E", "Jka", "K"}
    assert set(r["explaining"]) == {"E", "Jka"}


def test_jka_not_ruled_out_by_heterozygous_cell():
    # 512304 §3: rule out dosage antibodies only with homozygous cells
    r = teaching_panel()
    assert "Jka" not in r["excluded"] and r["candidates"]["Jka"]["excluded_only_by_dosage_rule"]


def test_case4_needs_one_more_e_pos_jka_neg_cell():
    # 512304 §4 Case 4 (anti-E + anti-Jka): "3-cell not enough -> need 1 more E+/Jka- cell".
    # Hand count: E+ reactive cells negative for Jka = 2, 11 -> 2 of 3 -> need 1.
    # Jka+ reactive cells negative for E = 1, 8, 9 -> 3 -> met.
    r = teaching_panel(confirm=["E", "Jka"])
    assert r["candidates"]["E"]["strict_pos_reactive"] == ["2", "11"]
    assert r["candidates"]["Jka"]["rule_of_three"] is True
    assert any("need 1 more reactive E+ Jka- cell" in x for x in r["reasons"])
    assert r["verdict"] == "NOT CONCLUSIVE"


def test_any_mode_shows_the_dosage_trap():
    r = teaching_panel(mode="any")
    assert "Jka" in r["excluded"]                     # crossing out on cell 6 (het) hides anti-Jka
    assert r["unexplained_reactive"] == ["1", "8", "9"]


def test_single_antibody_rule_of_three_met(tmp_path):
    # Hand-built: E+ cells 1-3 react, E- cells 4-6 do not; homozygous e/Jka/Jkb cells exclude the rest
    p = tmp_path / "p.csv"
    rows = [["cell", "E", "e", "Jk(a)", "Jk(b)", "result"],
            ["1", "+", "0", "+", "+", "3+"], ["2", "+", "+", "0", "+", "2+"], ["3", "+", "0", "0", "+", "3+"],
            ["4", "0", "+", "+", "0", "0"], ["5", "0", "+", "0", "+", "0"], ["6", "0", "+", "+", "+", "0"]]
    with open(p, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    antigens, cells = panel_ruleout.load(str(p))
    assert antigens == ["E", "e", "Jka", "Jkb"]       # Jk(a) normalised
    r = panel_ruleout.analyse(antigens, cells, auto="0", patient=["E-"])
    assert list(r["candidates"]) == ["E"]
    assert r["verdict"].startswith("CONSISTENT WITH anti-E")


def test_patient_antigen_positive_blocks_conclusion():
    # 510403 §3.3 confirmation: the patient must lack the antigen
    r = teaching_panel(confirm=["E", "Jka"], patient=["E+", "Jka-"])
    assert any("own RBC are E+" in x for x in r["reasons"])


def test_pan_reactive_auto_negative_flags_high_incidence(tmp_path):
    # 510403 §3.3: all cells positive + auto negative = antibody to a high-incidence antigen
    p = tmp_path / "pan.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([["cell", "K", "k", "result"], ["1", "0", "+", "2+"], ["2", "+", "+", "2+"],
                                 ["3", "0", "+", "2+"]])
    antigens, cells = panel_ruleout.load(str(p))
    r = panel_ruleout.analyse(antigens, cells, auto="0")
    assert any("high-incidence" in n for n in r["notes"])


def test_must_fail_control_rule_out_on_heterozygous(monkeypatch):
    """Trap: crossing out on heterozygous cells (every Ag+ cell treated as homozygous)."""
    monkeypatch.setattr(panel_ruleout, "is_homozygous", lambda cell, ag: cell["ag"].get(ag) is True)
    with pytest.raises(AssertionError):
        test_jka_not_ruled_out_by_heterozygous_cell()


def test_must_fail_control_loose_rule_of_three(monkeypatch):
    """Trap: counting E+ cells that also carry Jka as evidence for anti-E (512304 Case 4)."""
    def loose(cells, x, others):
        return [c["id"] for c in cells if c["reactive"] and c["ag"].get(x) is True]

    monkeypatch.setattr(panel_ruleout, "strict_positive", loose)
    with pytest.raises(AssertionError):
        test_case4_needs_one_more_e_pos_jka_neg_cell()


# ================================================================ bb_calc
def test_units_512304_worked_example():
    # 512304 §3: 3 / (0.7 x 0.25) = 17.14 ("17 units"; card Fork 2 "~17") -> screen at least 18
    r = bb_calc.units_to_screen(3, {"E": 0.70, "Jka": 0.25})
    assert r["compatible_fraction"] == pytest.approx(0.175)
    assert r["units_expected"] == pytest.approx(17.142857, abs=1e-5)
    assert r["units_to_screen"] == 18


def test_units_512303_worked_example():
    # 512303 §1.4: 0.32 x 0.26 x 0.91 = 0.0757 (~8%); digest rounds to 8% -> (100/8) x 2 = 25.
    # Exact arithmetic gives 26.4 (screen 27); rounding the frequency first reproduces the digest's 25.
    r = bb_calc.units_to_screen(2, {"Fya": 0.32, "Jkb": 0.26, "K": 0.91})
    assert r["compatible_fraction"] == pytest.approx(0.075712)
    assert r["units_expected"] == pytest.approx(26.4159, abs=1e-3)
    assert bb_calc.units_to_screen(2, {"rounded": 0.08})["units_expected"] == pytest.approx(25)


def test_units_rejects_percent_instead_of_fraction():
    with pytest.raises(ValueError):
        bb_calc.units_to_screen(3, {"E": 70})


def test_rhig_kb_hand_example():
    # 512303 §3.3 rule (30 mL whole blood / vial, round .5 up, +1 vial), hand arithmetic:
    # KB 1.5% x 5000 mL = 75 mL -> 75/30 = 2.5 -> 3 -> +1 = 4 vials
    fmh = bb_calc.fmh_from_kb(1.5, 5000)
    assert fmh == pytest.approx(75)
    assert bb_calc.rhig_vials(fmh)["vials"] == 4


@pytest.mark.parametrize("ml,vials", [(10, 1), (15, 2), (30, 2), (44, 2), (45, 3)])
def test_rhig_rounding(ml, vials):
    # 10/30=0.33->0+1 · 15/30=0.5->1+1 · 30/30=1->1+1 · 44/30=1.47->1+1 · 45/30=1.5->2+1
    assert bb_calc.rhig_vials(ml)["vials"] == vials


def test_rhig_cli_rbc_volume_and_no_default_blood_volume(capsys):
    # card Fork 8: 30 mL whole blood = 15 mL RBC -> 20 mL RBC = 40 mL WB -> 1.33 -> 1 + 1 = 2
    assert bb_calc.main(["--json", "rhig", "--fmh-rbc-ml", "20"]) == 0
    assert json.loads(capsys.readouterr().out)["vials"] == 2
    with pytest.raises(SystemExit):
        bb_calc.main(["rhig", "--kb-pct", "1.5"])      # maternal blood volume must be given


def test_must_fail_control_standard_dose_regardless_of_bleed(monkeypatch):
    """Trap (card Fork 8): giving the standard 300 ug dose without calculating a large FMH."""
    monkeypatch.setattr(bb_calc, "rhig_vials", lambda fmh, ml_per_vial=30.0, extra_vials=1: {"vials": 1})
    with pytest.raises(AssertionError):
        test_rhig_kb_hand_example()


# ================================================================ every patient-facing CLI output is advisory
@pytest.mark.parametrize("mod,args", [
    (abo_rh, ["type", "--anti-a", "4+", "--anti-b", "0", "--a1-cells", "0", "--b-cells", "4+", "--anti-d", "3+"]),
    (abo_rh, ["compat", "--recipient", "A"]),
    (panel_ruleout, [PANEL, "--auto", "0"]),
    (bb_calc, ["units", "--requested", "3", "--neg-freq", "E=0.7"]),
    (bb_calc, ["rhig", "--fmh-ml", "75"]),
])
def test_cli_prints_advisory(mod, args, capsys):
    assert mod.main(args) == 0
    assert "ADVISORY:" in capsys.readouterr().out
