"""Oracle tests for preanalytical-judgment tools.

Expected outcomes come from rules written OUTSIDE the code:
  - order of draw: 510403 Clinical Laboratory Practice digest §2.8 table (culture -> citrate(blue) ->
    red -> green -> lavender -> gray) and preanalytical-judgment card Fork 1/2
  - tube/test pairs: card Fork 1/2, 505402 Clinical Chemistry digest §5.4/§7 (no fluoride for urease BUN),
    clinical-correlation card Fork 4 + 510416 digest Case 11 (no heparin tube for RT-PCR)
  - specimen rejection: card Fork 2/3/4/5/6 and trap #1/#2/#8
Specimens are constructed teaching values. Must-fail controls inject the traps the card warns about.

Run from the skill folder:  python -m pytest evals -q
"""
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import order_of_draw as od  # noqa: E402
import specimen_check as sc  # noqa: E402


def run(*items, winged=False):
    return od.check(od.parse(list(items)), winged=winged)


# ---------------------------------------------------------------- order of draw (510403 §2.8)
def test_canonical_order_passes():
    r = run("culture", "citrate", "serum", "heparin", "edta", "fluoride")
    assert r["order_violations"] == [] and r["verdict"] == "OK"


def test_thai_colour_aliases_follow_the_same_table():
    # 510403 §2.8 colours: ฟ้า citrate, แดง clot, เขียว heparin, ม่วง EDTA, เทา NaF
    r = run("ฟ้า", "แดง", "เขียว", "ม่วง", "เทา")
    assert r["order_violations"] == []


def test_edta_before_serum_flags_k_ca_carryover():
    r = run("edta", "serum")
    assert len(r["order_violations"]) == 1
    why = r["order_violations"][0]["why"]
    assert "K up" in why and "Ca" in why                       # card Fork 1 mechanism


def test_heparin_before_citrate_flags_coag():
    r = run("heparin", "citrate")
    assert "coag" in r["order_violations"][0]["why"]


def test_discard_tube_is_allowed_anywhere():
    assert run("discard", "citrate", "serum")["order_violations"] == []


def test_winged_set_needs_discard_before_citrate():
    assert run("citrate", "serum", winged=True)["verdict"] == "FIX ORDER/TUBES"
    assert run("discard", "citrate", "serum", winged=True)["verdict"] == "OK"
    assert run("citrate", "serum", winged=False)["verdict"] == "OK"   # straight needle: no rule


@pytest.mark.parametrize("item,status", [
    ("citrate:PT", "OK"), ("serum:PT", "FAIL"),           # coag = citrate (card Fork 2)
    ("edta:CBC", "OK"), ("heparin:CBC", "FAIL"),          # CBC = EDTA (510403 §2.8)
    ("edta:K", "FAIL"), ("serum:K", "OK"),                # K from EDTA = false (card Fork 1)
    ("gray:BUN", "FAIL"),                                  # urease BUN not fluoride (505402 §5.4)
    ("heparin:PCR", "FAIL"), ("edta:PCR", "OK"),          # heparin inhibits PCR (510416 Case 11)
    ("serum:glucose", "WARN"), ("gray:glucose", "OK"),    # glycolysis (card Fork 2)
    ("serum:Na", "NO-RULE"),                               # unknown test is never a silent OK
])
def test_tube_test_pairs(item, status):
    r = run(item)
    assert r["test_checks"][0]["status"] == status


def test_unknown_tube_is_an_error_not_a_guess():
    with pytest.raises(ValueError):
        od.parse(["pink"])


def test_must_fail_control_wrong_order_table(monkeypatch):
    """Inject the trap 'ignore order of draw': EDTA ranked before serum. The oracle must go red."""
    monkeypatch.setitem(od.RANK, "edta", 2.5)
    with pytest.raises(AssertionError):
        test_canonical_order_passes()


# ---------------------------------------------------------------- specimen rejection (card Forks 2-6)
BASE = {"id_match": True, "identifiers": 2, "labeled_at": "bedside"}


def spec(**kw):
    d = dict(BASE)
    d.update(kw)
    return d


def test_hemolyzed_k_is_not_reportable():
    # card Fork 3 + trap #2: hemolysis -> K/LDH/AST falsely high -> recollect, not hyperkalemia
    r = sc.check(spec(tests=["K", "Na", "AST"], hemolysis_index=120), hi_limit=50)
    assert r["verdict"] == "RECOLLECT"
    assert set(r["do_not_report"]) == {"K", "AST"}
    assert r["reportable"] == ["Na"]
    assert "will not fix" in [c for c in r["checks"] if c["criterion"] == "hemolysis"][0]["msg"]  # trap #1


def test_hemolysis_index_needs_a_lab_limit():
    r = sc.check(spec(tests=["K"], hemolysis_index=120))       # no --hi-limit given
    hem = [c for c in r["checks"] if c["criterion"] == "hemolysis"][0]
    assert hem["status"] == "NOT CHECKED"                       # never a hard-coded cut-off


def test_hemolysis_without_affected_tests_is_comment_only():
    r = sc.check(spec(tests=["Na"], hemolyzed=True))
    assert r["verdict"] == "ACCEPT WITH COMMENT" and r["reportable"] == ["Na"]


def test_identity_mismatch_rejects_everything():
    # card Fork 5: wrong-blood-in-tube -> recollect, never relabel, whatever the quality
    r = sc.check(spec(id_match=False, tests=["CBC"], hemolyzed=False))
    assert r["verdict"] == "REJECT" and r["reportable"] == []


def test_unknown_identity_is_hold_not_accept():
    r = sc.check({"tests": ["CBC"], "labeled_at": "bedside", "hemolyzed": False})
    assert r["verdict"] == "HOLD" and r["reportable"] == []


def test_counter_labelling_rejects():
    assert sc.check(spec(labeled_at="counter", tests=["CBC"]))["verdict"] == "REJECT"    # trap #8


def test_citrate_underfill_and_high_hct():
    # card Fork 2: 1:9 exact; underfill -> PT/aPTT falsely long; Hct > 55% -> adjust citrate
    under = sc.check(spec(tube="citrate", tests=["PT", "aPTT"], fill_pct=70), min_fill=90)
    assert under["verdict"] == "REJECT" and set(under["do_not_report"]) == {"PT", "aPTT"}
    hct = sc.check(spec(tube="citrate", tests=["PT"], fill_pct=100, hct=58), min_fill=90)
    assert hct["verdict"] == "HOLD"
    ok = sc.check(spec(tube="citrate", tests=["PT"], fill_pct=100, hct=45, hemolyzed=False), min_fill=90)
    assert ok["verdict"] == "ACCEPT"


def test_iv_line_above_site_recollects():
    assert sc.check(spec(tests=["glucose"], iv_line="above"))["verdict"] == "RECOLLECT"   # card Fork 4


def test_ammonia_not_on_ice_recollects():
    assert sc.check(spec(tests=["ammonia"], transport="room"))["verdict"] == "RECOLLECT"   # card Fork 6


def test_stability_limit_is_an_argument():
    late = spec(tests=["K"], hemolyzed=False, hours_since_collection=6)
    assert sc.check(late, max_hours=4)["verdict"] == "REJECT"
    assert [c for c in sc.check(late)["checks"] if c["criterion"] == "stability"][0]["status"] == "NOT CHECKED"


def test_must_fail_control_hemolysis_list_without_k(monkeypatch):
    """Inject trap #2: K dropped from the hemolysis list -> hemolyzed K gets reported. Oracle must go red."""
    monkeypatch.setattr(sc, "HEMOLYSIS_AFFECTED", {"ldh", "ast"})
    with pytest.raises(AssertionError):
        test_hemolyzed_k_is_not_reportable()


def test_must_fail_control_unknown_treated_as_pass(monkeypatch):
    """Inject soft-fail laundering: missing identity data counted as PASS. Oracle must go red."""
    real = sc.check

    def laundering(sp, *a, **k):
        sp = dict(sp)
        sp.setdefault("id_match", True)
        sp.setdefault("identifiers", 2)
        return real(sp, *a, **k)

    monkeypatch.setattr(sc, "check", laundering)
    with pytest.raises(AssertionError):
        test_unknown_identity_is_hold_not_accept()
