"""Oracle tests for pathology-judgment tool (lights_criteria).

Rule source: Light's criteria as written in the 503402 Clinical Hematology Lab digest §8 (protein ratio > 0.5,
LDH ratio > 0.6, fluid LDH > 2/3 of the serum ULN; any one = exudate) and card Fork 8 (Light's first; SG is
only a rough estimate; exudate -> cytology). Inputs are teaching values; arithmetic is in the comments.
Must-fail controls inject three traps: requiring ALL criteria, comparing with 2/3 of the patient's serum LDH
instead of the ULN, and treating a missing value as "not met"; the oracle must go red.

Run from the repo root:  python -m pytest skills/pathology-judgment/evals -q
"""
import json
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import lights_criteria as lc  # noqa: E402


def test_transudate_none_met():
    # protein 2.0/7.0 = 0.286 ; LDH 90/250 = 0.36 ; 2/3 x ULN 250 = 166.67, fluid LDH 90 -> none met
    r = lc.evaluate(2.0, 7.0, 90, 250, 250)
    assert [c["met"] for c in r["criteria"]] == [False, False, False]
    assert r["criteria"][0]["value"] == pytest.approx(2 / 7)
    assert r["call"] == "TRANSUDATE"


def test_exudate_on_a_single_criterion():
    # protein 2.5/7.0 = 0.357 (no) ; LDH 180/400 = 0.45 (no) ; 180 > 2/3 x 250 = 166.67 (YES) -> EXUDATE
    r = lc.evaluate(2.5, 7.0, 180, 400, 250)
    assert [c["met"] for c in r["criteria"]] == [False, False, True]
    assert r["criteria"][2]["threshold"] == pytest.approx(500 / 3)
    assert r["call"] == "EXUDATE"
    assert any("cytology" in n for n in r["notes"])


def test_thresholds_are_strict():
    # protein 3.0/6.0 = 0.5 exactly -> NOT > 0.5 ; LDH 120/200 = 0.6 exactly -> NOT > 0.6 ;
    # ULN 300 -> 2/3 = 200 ; fluid LDH 120 -> no  => TRANSUDATE
    r = lc.evaluate(3.0, 6.0, 120, 200, 300)
    assert r["call"] == "TRANSUDATE"
    # one step over: 3.1/6.0 = 0.517 -> exudate
    assert lc.evaluate(3.1, 6.0, 120, 200, 300)["call"] == "EXUDATE"


def test_missing_values_never_give_transudate():
    # only the protein pair (0.286, not met) -> INDETERMINATE, not transudate
    assert lc.evaluate(2.0, 7.0)["call"] == "INDETERMINATE"
    # but one met criterion is enough even with gaps: 4.0/6.0 = 0.667 > 0.5 -> EXUDATE
    assert lc.evaluate(4.0, 6.0)["call"] == "EXUDATE"


def test_sg_is_recorded_not_used():
    # SG 1.025 would "look exudative" on the old SG shortcut; the call stays with Light's
    r = lc.evaluate(2.0, 7.0, 90, 250, 250, sg=1.025)
    assert r["call"] == "TRANSUDATE"
    assert any("NOT used" in n for n in r["notes"])


def test_must_fail_control_all_three_required(monkeypatch):
    """Inject the trap: exudate only when ALL criteria are met (AND instead of OR)."""
    def and_rule(rows):
        if all(r["met"] is True for r in rows):
            return "EXUDATE"
        return "INDETERMINATE" if any(r["met"] is None for r in rows) else "TRANSUDATE"

    monkeypatch.setattr(lc, "classify", and_rule)
    with pytest.raises(AssertionError):
        test_exudate_on_a_single_criterion()


def test_must_fail_control_two_thirds_of_patient_serum(monkeypatch):
    """Inject the trap: 2/3 of the patient's serum LDH (400 -> 266.7) instead of 2/3 of the ULN."""
    real = lc.criteria

    def wrong(fp=None, sp=None, fl=None, sl=None, uln=None):
        return real(fp, sp, fl, sl, sl)

    monkeypatch.setattr(lc, "criteria", wrong)
    with pytest.raises(AssertionError):
        test_exudate_on_a_single_criterion()


def test_must_fail_control_missing_counts_as_not_met(monkeypatch):
    """Inject the trap: a missing value is silently 'not met' -> transudate from incomplete data."""
    monkeypatch.setattr(lc, "classify", lambda rows: "EXUDATE" if any(r["met"] for r in rows) else "TRANSUDATE")
    with pytest.raises(AssertionError):
        test_missing_values_never_give_transudate()


def test_cli(capsys):
    assert lc.main(["--fluid-protein", "2.5", "--serum-protein", "7.0", "--fluid-ldh", "180",
                    "--serum-ldh", "400", "--ldh-uln", "250"]) == 0
    out = capsys.readouterr().out
    assert "CALL: EXUDATE" in out and "ADVISORY" in out
    assert lc.main(["--fluid-protein", "2.0", "--serum-protein", "7.0", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["call"] == "INDETERMINATE" and "ADVISORY" in data["advisory"]
