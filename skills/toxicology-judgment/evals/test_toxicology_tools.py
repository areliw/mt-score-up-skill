"""Oracle tests for toxicology-judgment tools.

Expected outcomes come from OUTSIDE the code: the owner digest 510414-DIGEST-2026-05-31.md
("510414": section 3 TDM, 4 opioids, 5 chelator table, 6 pesticides/ChE, 8 methanol, 10 corrosives),
510403-DIGEST-2026-05-31.md section 2.8 (grey NaF tube for alcohol), the card's Forks 3-6 and
anti-pattern list, and hand arithmetic in the comments.
Must-fail controls inject the traps the card warns about and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import antidote_check as ac  # noqa: E402
import tox_calc  # noqa: E402


def status(agent, give, **kw):
    return ac.check(agent, [give], **kw)["rows"][0]["status"]


# ---------------------------------------------------------------- chelators (510414 section 5, card Fork 4)
def test_lead_ca_edta_ok_na_edta_forbidden():
    # 510414 section 5: "EDTA (Ca-EDTA) | Pb | ห้ามใช้เกลือ Na (hypocalcemic tetany)"
    assert status("lead", "Ca-EDTA") == ac.FIRST
    assert status("Pb", "Na-EDTA") == ac.FORBID
    assert ac.check("lead", ["Na-EDTA"])["verdict"].startswith("STOP")


def test_plain_edta_is_ambiguous():
    # the salt IS the trap -> a bare "EDTA" must not pass silently
    assert status("lead", "EDTA") == ac.AMBIG


def test_cadmium_bal_forbidden_arsenic_mercury_bal_ok():
    # 510414 section 5: "BAL | As, Hg, Pb | ห้ามใช้กับ Cd (เพิ่มพิษไต)"
    assert status("cadmium", "BAL") == ac.FORBID
    assert status("arsenic", "dimercaprol") == ac.FIRST
    assert status("Hg", "BAL") == ac.FIRST


def test_other_chelators_from_digest_table():
    # 510414 section 5: penicillamine -> Cu/Wilson; desferrioxamine -> Fe; dithiocarb -> nickel carbonyl
    assert status("wilson", "penicillamine") == ac.FIRST
    assert status("iron", "deferoxamine") == ac.FIRST
    assert status("nickel-carbonyl", "DDC") == ac.FIRST


def test_must_fail_control_na_edta_allowed(monkeypatch):
    """Trap (card Fork 4 + anti-pattern 'Na-EDTA กับ Pb'): treating the Na salt as interchangeable."""
    pairs = dict(ac.TABLE["lead"]["pairs"])
    pairs["na-edta"] = (ac.FIRST, "EDTA is EDTA")
    monkeypatch.setitem(ac.TABLE["lead"], "pairs", pairs)
    with pytest.raises(AssertionError):
        test_lead_ca_edta_ok_na_edta_forbidden()


# ---------------------------------------------------------------- antidotes (510414 sections 4, 6, 8, 10; card Fork 3)
def test_op_needs_atropine_with_2pam():
    # 510414 section 6: OP -> Atropine + 2-PAM. Card: always give 2-PAM WITH atropine.
    both = ac.check("op", ["atropine", "2-PAM"])
    assert both["warnings"] == [] and both["verdict"].startswith("consistent")
    alone = ac.check("organophosphate", ["pralidoxime"])
    assert any("WITHOUT atropine" in w for w in alone["warnings"])
    assert alone["verdict"].startswith("CHECK")


def test_unknown_cholinergic_flags_missing_2pam():
    # Card Fork 3: OP vs carbamate not distinguished -> flag 2-PAM until OP ruled out.
    r = ac.check("cholinergic-unknown", ["atropine"])
    assert any("pralidoxime" in w for w in r["warnings"])


def test_confirmed_carbamate_2pam_conditional():
    # 510414 section 6: carbamate uses atropine, "2-PAM ไม่จำเป็น/ระวัง"
    assert status("carbamate", "atropine") == ac.FIRST
    assert status("carbamate", "pralidoxime") == ac.COND


def test_naloxone_is_opioid_not_op():
    # 510414 section 4: opioid antidote = naloxone; card anti-pattern: "naloxone ใน OP"
    assert status("heroin", "naloxone") == ac.FIRST
    assert status("op", "naloxone") == ac.WRONG


def test_paraquat_organochlorine_corrosive_forbidden_moves():
    # 510414 section 6: paraquat no antidote (Fuller's earth, hemoperfusion); card: no high O2.
    assert status("paraquat", "high-O2") == ac.FORBID
    assert status("paraquat", "hemoperfusion") == ac.ADJ
    # 510414 section 6: organochlorine -> diazepam/phenobarbital, "ห้าม epinephrine"
    assert status("DDT", "adrenaline") == ac.FORBID
    # 510414 section 10: corrosive -> no emesis, no neutralising
    assert status("corrosive", "induce vomiting") == ac.FORBID
    assert status("corrosive", "neutralise") == ac.FORBID


def test_methanol_warfarin_cyanide():
    # 510414 section 8: methanol -> NaHCO3 + ethanol; card adds fomepizole first-line
    assert status("methanol", "fomepizole") == ac.FIRST
    assert status("methanol", "ethanol") == ac.ADJ
    assert status("methanol", "NaHCO3") == ac.ADJ
    # 510414 section 6: warfarin rodenticide -> vitamin K
    assert status("coumarin", "vitamin K") == ac.FIRST
    # card Fork 3: hydroxocobalamin first; nitrite adds metHb -> avoid with CO / smoke
    assert status("cyanide", "hydroxocobalamin") == ac.FIRST
    assert status("cyanide", "nitrite") == ac.COND
    assert status("cyanide", "nitrite", co_suspected=True) == ac.FORBID


def test_unknown_pair_is_never_ok():
    assert status("mercury", "penicillamine") == ac.UNKNOWN          # not in the card's Hg row
    assert ac.check("snake", ["antivenom"])["known_agent"] is False
    assert ac.check("lead", ["vitamin-k"])["verdict"].startswith("CHECK")


# ---------------------------------------------------------------- ChE (510414 section 6, card Fork 5)
def test_che_depression_from_baseline():
    # baseline 6000, now 2500: (6000 - 2500) / 6000 = 3500 / 6000 = 58.33 % fall -> > 50 % -> OP-level
    r = tox_calc.che(2500, baseline=6000, che_type="plasma")
    assert r["depression_pct"] == pytest.approx(58.333, abs=1e-3)
    assert r["exceeds"] is True
    # baseline 6000, now 4000: 2000 / 6000 = 33.3 % -> below threshold
    assert tox_calc.che(4000, baseline=6000)["exceeds"] is False
    # exactly 50 % (3000 of 6000) is not "> 50 %"
    assert tox_calc.che(3000, baseline=6000)["exceeds"] is False


def test_che_plasma_note_and_no_builtin_reference():
    assert "liver failure" in tox_calc.che(2500, baseline=6000, che_type="plasma")["type_note"]
    with pytest.raises(ValueError):            # no baseline and no lab reference -> refuses to judge
        tox_calc.che(2500)
    assert tox_calc.che(2500, ref_low=3000)["reading"].startswith("below")


def test_must_fail_control_percent_remaining_as_inhibition(monkeypatch):
    """Trap: reading '% of baseline remaining' (2500/6000 = 41.7 %) as '% depression'."""
    monkeypatch.setattr(tox_calc, "percent_depression", lambda current, baseline: current / baseline * 100)
    with pytest.raises(AssertionError):
        test_che_depression_from_baseline()


# ---------------------------------------------------------------- TDM timing (510414 section 3, card Fork 6)
def test_steady_state_fraction_hand_values():
    # t_half 6 h: after 30 h = 5 half-lives: 1 - 0.5^5 = 1 - 1/32 = 0.96875 -> reached (5-half-life rule)
    r = tox_calc.tdm(6, 30)
    assert r["fraction_of_steady_state"] == pytest.approx(0.96875)
    assert r["steady_state"] is True
    # after 12 h = 2 half-lives: 1 - 0.25 = 0.75 -> NOT at steady state (card trap)
    r = tox_calc.tdm(6, 12)
    assert r["fraction_of_steady_state"] == pytest.approx(0.75)
    assert r["steady_state"] is False and "NOT at steady state" in r["steady_state_reading"]


def test_trough_timing():
    # interval 12 h, drawn 11.75 h after the last dose -> 0.25 h before next <= 0.5 h window -> trough
    ok = tox_calc.tdm(6, 30, interval=12, since_last=11.75, trough_window=0.5, order="trough")
    assert ok["is_trough"] is True and ok["order_check"].startswith("timing consistent")
    # drawn 2 h after the dose -> 10 h before next -> trough order at the wrong time
    bad = tox_calc.tdm(6, 30, interval=12, since_last=2, trough_window=0.5, order="trough")
    assert bad["is_trough"] is False and bad["order_check"].startswith("WRONG TIME")


# ---------------------------------------------------------------- specimen (510414 sections 2-3, card Fork 2/6)
def test_specimen_rules():
    # 510414 section 3: gel separator absorbs phenytoin -> plain tube
    assert tox_calc.specimen("phenytoin", "gel")["ok"] is False
    assert tox_calc.specimen("phenytoin", "plain")["ok"] is True
    # 510414 section 3: tacrolimus + cyclosporine -> whole blood
    assert tox_calc.specimen("tacrolimus", "plain")["ok"] is False
    assert tox_calc.specimen("ciclosporin", "edta")["ok"] is True
    # alcohol: whole blood, sealed; grey NaF tube is the usual alcohol tube (510403 section 2.8)
    assert tox_calc.specimen("alcohol", "fluoride")["ok"] is True
    assert tox_calc.specimen("alcohol", "fluoride", sealed=False)["ok"] is False
    assert tox_calc.specimen("cyanide", "gel")["ok"] is False


@pytest.mark.parametrize("mod,argv", [
    (ac, ["--agent", "lead", "--give", "Na-EDTA"]),
    (tox_calc, ["che", "--current", "2500", "--baseline", "6000", "--type", "plasma"]),
    (tox_calc, ["tdm", "--half-life", "6", "--since-start", "12"]),
])
def test_cli_prints_advisory(mod, argv, capsys):
    assert mod.main(argv) == 0
    assert "ADVISORY" in capsys.readouterr().out
