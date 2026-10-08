"""Oracle tests for infection-control-judgment tool precaution_check.py.

Expected outcomes come from the RULES WRITTEN IN THE CARD (skills/infection-control-judgment.md),
not from the code. There is no course digest behind this card: its forks were checked against
CDC/HICPAC by codex review (see CHANGELOG, Fork 4 fix). 510408 digest only mentions "PPE don/doff"
as a field activity without an order. Each assertion names the card fork it comes from.
Must-fail controls inject the card's #1 trap (surgical mask / positive pressure for airborne) and
require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import json
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import precaution_check as pk  # noqa: E402


def amap():
    with open(os.path.join(SKILL, "data", "agent_routes_teaching.json"), encoding="utf-8") as f:
        return json.load(f)


def status(res, item):
    return next(r["status"] for r in res["rows"] if r["item"] == item)


def plan(**kw):
    base = {"mask": "none", "room": "standard", "gloves": False, "gown": False, "hand": "alcohol", "soiled": False}
    base.update(kw)
    return base


# ---------------------------------------------------------------- airborne (VERDICT box, Fork 2-4)
def test_tb_needs_n95_and_negative_pressure():
    routes, soap = pk.routes_for(["tuberculosis"], amap())
    good = pk.check_plan(routes, plan(mask="n95", room="negative"), soap=soap)
    assert good["verdict"] == "PASS"
    bad = pk.check_plan(routes, plan(mask="surgical", room="positive"), soap=soap)
    assert status(bad, "mask") == "FAIL"           # trap #1: surgical mask for airborne
    assert status(bad, "room") == "FAIL"           # Fork 4: positive pressure + airborne = swapped
    assert bad["verdict"] == "FAIL"


def test_must_fail_control_surgical_mask_accepted_for_airborne(monkeypatch):
    """Inject card trap #1: treat airborne like droplet (surgical mask is 'enough')."""
    monkeypatch.setattr(pk, "required_mask", lambda routes, agp: "surgical" if routes else "none")
    with pytest.raises(AssertionError):
        test_tb_needs_n95_and_negative_pressure()


def test_must_fail_control_positive_pressure_accepted(monkeypatch):
    """Inject the room-swap trap: any isolation room accepted for airborne."""
    monkeypatch.setattr(pk, "room_check", lambda routes, host, room: ("PASS", "any room"))
    with pytest.raises(AssertionError):
        test_tb_needs_n95_and_negative_pressure()


def test_varicella_is_airborne_plus_contact():
    # Fork 4: varicella / disseminated zoster = airborne + contact (not airborne alone)
    routes, _ = pk.routes_for(["varicella"], amap())
    assert routes == {"airborne", "contact"}
    res = pk.check_plan(routes, plan(mask="n95", room="negative"))
    assert status(res, "gloves") == "FAIL" and status(res, "gown") == "FAIL"


def test_droplet_with_aerosol_procedure_needs_n95():
    # Fork 2: aerosol-generating procedure -> N95 even for a droplet disease
    routes, _ = pk.routes_for(["influenza"], amap())
    assert status(pk.check_plan(routes, plan(mask="surgical")), "mask") == "PASS"
    assert status(pk.check_plan(routes, plan(mask="surgical"), agp=True), "mask") == "FAIL"


# ---------------------------------------------------------------- contact + room (Fork 3, Fork 4)
def test_contact_only_in_aiir_is_a_waste_warning_not_a_pass():
    # Fork 4: drainage/incontinence = contact -> single room/cohort; AIIR reserved for airborne
    routes, _ = pk.routes_for(["MRSA"], amap())
    res = pk.check_plan(routes, plan(gloves=True, gown=True, room="negative"))
    assert status(res, "room") == "WARN"
    assert status(pk.check_plan(routes, plan(gloves=True, gown=True, room="single")), "room") == "PASS"


def test_contact_without_gloves_gown_fails():
    routes, _ = pk.routes_for(["VRE"], amap())
    res = pk.check_plan(routes, plan(room="single"))
    assert status(res, "gloves") == "FAIL" and status(res, "gown") == "FAIL"


def test_immunocompromised_host_needs_positive_pressure():
    # Fork 4: positive pressure = protect immunocompromised (BMT/neutropenia); negative = swapped
    assert status(pk.check_plan(set(), plan(room="positive"), protective_host=True), "room") == "PASS"
    assert status(pk.check_plan(set(), plan(room="negative"), protective_host=True), "room") == "FAIL"


def test_airborne_in_immunocompromised_host_is_flagged_conflict():
    # not covered by the card -> the tool must not invent an answer
    res = pk.check_plan({"airborne"}, plan(mask="n95", room="negative"), protective_host=True)
    assert status(res, "room") == "CONFLICT"


# ---------------------------------------------------------------- hand hygiene (Fork 1)
def test_c_difficile_needs_soap_and_water():
    routes, soap = pk.routes_for(["C. difficile"], amap())
    assert soap is True
    assert status(pk.check_plan(routes, plan(gloves=True, gown=True, room="single", hand="alcohol"), soap=soap),
                  "hand hygiene") == "FAIL"
    assert status(pk.check_plan(routes, plan(gloves=True, gown=True, room="single", hand="soap"), soap=soap),
                  "hand hygiene") == "PASS"


def test_norovirus_soap_rule_without_route():
    routes, soap = pk.routes_for(["norovirus"], amap())
    assert routes == set() and soap is True


# ---------------------------------------------------------------- don/doff order (Fork 2, Fork 1)
def test_sequence_card_order_passes():
    assert pk.check_sequence(["gown", "mask", "gloves"], ["gloves", "gown", "mask", "hand-hygiene"])["verdict"] == "PASS"


def test_sequence_errors_caught():
    res = pk.check_sequence(["gown", "gloves", "mask"], ["gown", "gloves", "mask"])
    assert res["verdict"] == "FAIL"
    joined = " ".join(res["problems"])
    assert "gloves must go on LAST" in joined
    assert "gloves must come off FIRST" in joined
    assert "END with hand hygiene" in joined


def test_cli_smoke(capsys):
    assert pk.main(["plan", "--map", os.path.join(SKILL, "data", "agent_routes_teaching.json"),
                    "--agent", "tuberculosis", "--mask", "surgical", "--room", "positive"]) == 0
    out = capsys.readouterr().out
    assert "PLAN FAIL" in out and "ADVISORY" in out
