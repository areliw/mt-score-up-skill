"""Oracle tests for clinmicro-judgment tools (culture_screen.py, ast_read.py).

Expected values come from the owner's digests / the card, NOT from the code:
  509402 = 06_Background_MedTech/509402-CLINICAL-MICROBIOLOGY-LAB-64-65/509402-DIGEST-2026-05-31.md
  508304 = 06_Background_MedTech/508304-CLINICAL-MICROBIOLOGY-2-LECTURE/508304-LECTURE-DIGEST-2026-06-01.md
  CM1    = 06_Background_MedTech/CLINICAL-MICROBIOLOGY-1-LECTURE/CLINMICRO1-DIGEST-2026-06-01.md
  MQC    = 06_Background_MedTech/MICROBIOLOGY-QC-LAB/MICRO-QC-DIGEST-2026-06-01.md
  card   = skills/clinmicro-judgment.md
Hand arithmetic is written next to each assertion. Must-fail controls inject the exact traps the
card warns about and require the oracle test to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import json
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import ast_read  # noqa: E402
import culture_screen as cs  # noqa: E402


def teaching(name):
    with open(os.path.join(SKILL, "data", name), encoding="utf-8") as f:
        return json.load(f)


def profile(name):
    return cs.load_profile(os.path.join(SKILL, "data", "micro_cutoffs_teaching.json"), name,
                           teaching("micro_cutoffs_teaching.json")["profiles"][name]["kind"])


# ================================================================ sputum (card FORK 5; 508304 §2)
def test_sputum_accept_reject_borderline_card_profile():
    # card FORK 5: accept SEC<10 + PMN>25; reject SEC>25; 10-25 borderline
    assert cs.sputum(8, 30, 10, 25, 25)["verdict"] == "ACCEPT"
    assert cs.sputum(30, 40, 10, 25, 25)["verdict"] == "REJECT"
    assert cs.sputum(15, 30, 10, 25, 25)["verdict"] == "BORDERLINE"
    assert cs.sputum(8, 20, 10, 25, 25)["verdict"] == "BORDERLINE"  # SEC fine but PMN not > 25


def test_sputum_sources_disagree_at_15_per_lpf():
    # 508304 §2 rejects SEC>10/LPF; the card only rejects SEC>25 -> SEC 15 flips verdict by profile
    card = profile("sputum-card-fork5")
    lect = profile("sputum-508304")
    args = lambda p: (p["sec_accept_below"], p["sec_reject_above"], p["pmn_above"])  # noqa: E731
    assert cs.sputum(15, 30, *args(card))["verdict"] == "BORDERLINE"
    assert cs.sputum(15, 30, *args(lect))["verdict"] == "REJECT"


# ================================================================ colony count (509402 §4; 508304 §2)
def test_urine_loop_0001_bands_509402():
    p = profile("urine-509402")
    # 509402 §4: loop 0.001 mL -> colonies x 1,000. 150 col = 150,000 = 1.5e5 -> '>100 colony' row = indicated
    r = cs.count([("E. coli", 150)], 0.001, p, symptoms="no")["rows"][0]
    assert r["cfu_ml"] == pytest.approx(1.5e5) and r["band"] == ">=1e5"
    # 50 col = 5e4 -> '10-100 colony' row = suspected pathogen
    assert cs.count([("E. coli", 50)], 0.001, p, symptoms="no")["rows"][0]["band"] == "1e4-1e5"
    # 5 col = 5e3 -> '<10 colony' row = 1e3-1e4
    assert cs.count([("E. coli", 5)], 0.001, p, symptoms="no")["rows"][0]["band"] == "1e3-1e4"


def test_zero_colonies_reported_below_detection_limit_not_zero():
    # 509402 §4: no colony -> '<10^3'. 1 colony on a 0.001 mL loop = 1,000 CFU/mL -> report '< 1000'
    res = cs.count([("none", 0)], 0.001, profile("urine-509402"), symptoms="no")
    assert res["verdict"] == "NO GROWTH"
    assert res["detection_limit_cfu_ml"] == pytest.approx(1000)
    assert res["rows"][0]["report"].startswith("< 1000")


def test_bal_loop_001_worked_example_508304():
    # 508304 §2 BAL: calibrated 0.01 mL loop, '100 colonies = 10^4 CFU/ml'; VAP threshold >= 1e4
    r = cs.count([("P. aeruginosa", 100)], 0.01, profile("bal-508304"))["rows"][0]
    assert r["cfu_ml"] == pytest.approx(1e4)
    assert r["band"] == ">=1e4"


def test_mixed_growth_three_species():
    # card iron rule #1 / trap 1: urine >=3 species -> mixed growth, new specimen (teaching mixed_min_species = 3)
    res = cs.count([("a", 40), ("b", 35), ("c", 30)], 0.001, profile("urine-509402"), symptoms="no")
    assert res["verdict"] == "MIXED GROWTH"


def test_symptom_status_changes_significance():
    # card FORK 3: symptomatic single uropathogen significant below 1e5. 2 col x 1,000 = 2,000 >= 1,000 (teaching)
    p = profile("urine-509402")
    assert cs.count([("E. coli", 2)], 0.001, p, symptoms="yes")["verdict"] == "SIGNIFICANT (symptomatic)"
    assert cs.count([("E. coli", 2)], 0.001, p, symptoms="no")["verdict"] != "SIGNIFICANT (symptomatic)"
    unknown = cs.count([("E. coli", 2)], 0.001, p, symptoms="unknown")
    assert any("symptom status unknown" in f for f in unknown["flags"])


def test_must_fail_control_fixed_x1000_multiplier(monkeypatch):
    """Inject the trap: 'colonies x 1,000' applied whatever the loop volume. BAL oracle must go red."""
    monkeypatch.setattr(cs, "cfu_per_ml", lambda colonies, loop_ml, dilution_factor=1.0: colonies * 1000.0)
    with pytest.raises(AssertionError):
        test_bal_loop_001_worked_example_508304()


# ================================================================ blood culture (card FORK 3; CM1 §1 §4)
def test_blood_cons_one_of_two_is_likely_contaminant():
    flora = teaching("blood_culture_flora_teaching.json")
    cls, _ = cs.classify("Staphylococcus epidermidis", flora)
    assert cls == "skin-flora"
    assert cs.blood(cls, 1, 2)["verdict"] == "LIKELY CONTAMINANT"   # CM1 §4: CoNS 1 bottle = suspect contaminant


def test_blood_cons_two_of_two_with_line_needs_correlation():
    # CM1 §4: >=2 bottles + catheter/prosthesis -> may be a real pathogen; card FORK 3 same
    assert cs.blood("skin-flora", 2, 2, line=True)["verdict"].startswith("CORRELATE")


def test_blood_single_set_cannot_judge_skin_flora():
    # card FORK 3 frames the rule as '1 bottle out of 2+'; with 1 drawn the rule cannot be applied
    assert cs.blood("skin-flora", 1, 1)["verdict"] == "INDETERMINATE"


def test_blood_non_flora_and_classical_are_significant():
    flora = teaching("blood_culture_flora_teaching.json")
    # CM1 trap #7: E. coli in blood = pathogen always; CM1 §1: Salmonella = classical, report at once
    assert cs.blood(cs.classify("Escherichia coli", flora)[0], 1, 2)["verdict"] == "SIGNIFICANT"
    assert cs.classify("Salmonella Typhi", flora)[0] == "classical"
    assert cs.classify("Bacillus anthracis", flora)[0] == "classical"   # override beats 'Bacillus'
    assert cs.classify("Bacillus cereus", flora)[0] == "skin-flora"


def test_whole_word_match_does_not_misclass():
    # 'CoNS' must not match inside 'constellatus'
    assert cs.classify("Streptococcus constellatus", teaching("blood_culture_flora_teaching.json"))[0] == "other"


def test_must_fail_control_report_skin_flora_as_pathogen(monkeypatch):
    """Inject card trap #1: report every blood isolate as significant regardless of class/sets."""
    monkeypatch.setattr(cs, "blood", lambda *a, **k: {"verdict": "SIGNIFICANT", "why": "trap"})
    with pytest.raises(AssertionError):
        test_blood_cons_one_of_two_is_likely_contaminant()


# ================================================================ AST (509402 §3; card FORK 4; MQC §B11)
RULES = None


def rules():
    global RULES
    if RULES is None:
        RULES = teaching("ast_rules_teaching.json")
    return RULES


def panel(organism, group, results, **extra):
    iso = {"organism": organism, "group": group, "results": results}
    iso.update(extra)
    return ast_read.read_panel(iso, rules())


def row(res, drug):
    return next(r for r in res["rows"] if r["drug"] == drug)


def test_disk_and_mic_directions_509402():
    # 509402 §3.3 cefoxitin S. aureus: <=21 R, >=22 S
    assert ast_read.interpret(22, "disk", 22, 21) == "S"
    assert ast_read.interpret(21, "disk", 22, 21) == "R"
    # 509402 §3.3 oxacillin MIC S. aureus: S <=2, R >=4 -> 2 S, 4 R, 3 I (between)
    assert ast_read.interpret(2, "mic", 2, 4) == "S"
    assert ast_read.interpret(4, "mic", 2, 4) == "R"
    assert ast_read.interpret(3, "mic", 2, 4) == "I"


def test_cefoxitin_23mm_cons_is_resistant_but_s_aureus_is_susceptible():
    # card FORK 4: CoNS cefoxitin <=24 mm = R (MR-CoNS); S. aureus <=21 = R, 23 >= 22 -> S
    cons = panel("Staphylococcus epidermidis", "CoNS", [{"drug": "cefoxitin", "method": "disk", "value": 23}])
    assert row(cons, "cefoxitin")["final"] == "R"
    assert row(cons, "cefoxitin")["reported_as"] == "oxacillin"
    assert any("methicillin resistance" in a for a in cons["alerts"])
    sa = panel("Staphylococcus aureus", "S. aureus", [{"drug": "cefoxitin", "method": "disk", "value": 23}])
    assert row(sa, "cefoxitin")["final"] == "S"


def test_no_breakpoint_means_not_interpreted():
    res = panel("Enterococcus faecalis", "Enterococcus", [{"drug": "cefoxitin", "method": "disk", "value": 30}])
    assert row(res, "cefoxitin")["raw"] == "NI"


def test_must_fail_control_borrow_s_aureus_breakpoint_for_cons(monkeypatch):
    """Inject card FORK 4 trap: fall back to any group's breakpoint (S. aureus 21 mm used for CoNS)."""
    def borrowing(rules_, group, drug, method):
        return next((bp for bp in rules_["breakpoints"] if bp["drug"] == drug and bp["method"] == method), None)
    monkeypatch.setattr(ast_read, "find_breakpoint", borrowing)
    with pytest.raises(AssertionError):
        test_cefoxitin_23mm_cons_is_resistant_but_s_aureus_is_susceptible()


def test_d_test_positive_reports_clindamycin_r():
    # 509402 §3.3: erythro R + clinda S -> D-test; D shape (+) -> report clindamycin resistant
    res = panel("Staphylococcus aureus", "S. aureus", [{"drug": "erythromycin", "sir": "R"},
                                                       {"drug": "clindamycin", "sir": "S"}], d_test="positive")
    assert row(res, "clindamycin")["final"] == "R"


def test_d_test_missing_holds_clindamycin():
    res = panel("Staphylococcus aureus", "S. aureus", [{"drug": "erythromycin", "sir": "R"},
                                                       {"drug": "clindamycin", "sir": "S"}])
    assert row(res, "clindamycin")["final"] == "HOLD"


def test_must_fail_control_ignore_d_test(monkeypatch):
    """Inject card trap 3: misread inducible clindamycin (skip the D-test)."""
    monkeypatch.setattr(ast_read, "apply_d_test", lambda rows, d_test, alerts: None)
    with pytest.raises(AssertionError):
        test_d_test_positive_reports_clindamycin_r()


def test_esbl_combination_disk_5mm():
    # 509402 §3.3: zone (drug + clav) larger by >= 5 mm -> ESBL+. 14->21 = +7 yes; 17->20 = +3 no; 14->19 = +5 yes
    out = ast_read.esbl_screen([{"drug": "ceftazidime", "alone": 14, "with_clav": 21},
                                {"drug": "cefotaxime", "alone": 17, "with_clav": 20},
                                {"drug": "cefpodoxime", "alone": 14, "with_clav": 19}], 5)
    assert [e["esbl"] for e in out] == [True, False, True]


def test_qc_out_of_range_holds_that_drug_only():
    # MQC §B11: gentamicin S. aureus ATCC 25923 range 19-27 -> 28 is out -> gentamicin HOLD (card trap #8)
    res = panel("Staphylococcus aureus", "S. aureus",
                [{"drug": "gentamicin", "sir": "S"}, {"drug": "erythromycin", "sir": "S"}],
                qc=[{"strain": "S. aureus ATCC 25923", "drug": "gentamicin", "value": 28}])
    assert row(res, "gentamicin")["final"] == "HOLD"
    assert row(res, "erythromycin")["final"] == "S"
    ok = panel("Staphylococcus aureus", "S. aureus", [{"drug": "gentamicin", "sir": "S"}],
               qc=[{"strain": "S. aureus ATCC 25923", "drug": "gentamicin", "value": 22}])
    assert row(ok, "gentamicin")["final"] == "S"


def test_penicillin_sharp_edge_is_resistant():
    # 509402 §3.1 exception 3: beta-lactamase+ staph vs penicillin, sharp 'cliff' edge -> R whatever the zone
    res = panel("Staphylococcus aureus", "S. aureus",
                [{"drug": "penicillin", "method": "disk", "value": 35, "edge": "sharp"}])
    assert row(res, "penicillin")["final"] == "R"


def test_intrinsic_resistance_overrides_a_reported_s():
    # card trap 10 / 509402 §3.4: P. aeruginosa intrinsically R to ampicillin
    res = panel("Pseudomonas aeruginosa", "Pseudomonas", [{"drug": "ampicillin", "sir": "S"}])
    assert row(res, "ampicillin")["final"] == "R"


def test_ampc_core_three_flagged_but_hafnia_not():
    # card trap 10b: E. cloacae / K. aerogenes / C. freundii -> flag 3rd-gen ceph 'S'; Hafnia = treat per AST
    ecl = panel("Enterobacter cloacae", "Enterobacterales", [{"drug": "ceftriaxone", "sir": "S"}])
    assert any("AmpC" in f for f in row(ecl, "ceftriaxone")["flags"])
    haf = panel("Hafnia alvei", "Enterobacterales", [{"drug": "ceftriaxone", "sir": "S"}])
    assert not any("AmpC" in f for f in row(haf, "ceftriaxone")["flags"])


def test_cli_runs_on_teaching_data(capsys):
    d = os.path.join(SKILL, "data")
    assert ast_read.main([os.path.join(d, "isolate_cons_teaching.json"), "--rules",
                          os.path.join(d, "ast_rules_teaching.json")]) == 0
    out = capsys.readouterr().out
    assert "ADVISORY" in out and "HOLD" in out
    assert cs.main(["sputum", "--sec", "8", "--pmn", "30", "--sec-accept-below", "10",
                    "--sec-reject-above", "25", "--pmn-above", "25"]) == 0
    assert "ADVISORY" in capsys.readouterr().out


def test_cli_refuses_without_cutoffs():
    with pytest.raises(SystemExit):
        cs.main(["sputum", "--sec", "8", "--pmn", "30"])
