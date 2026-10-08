"""Oracle tests for receiving-review-judgment tools.

There is no course digest for this skill; expected outcomes come from the rules written in the
receiving-review-judgment card itself (rule #1, trap #1, Fork 1-4, trap list), applied by hand to
constructed comment rows. Must-fail controls inject the traps the card warns about.

Run from the skill folder:  python -m pytest evals -q
"""
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import triage_check as tc  # noqa: E402


def row(**kw):
    d = {"id": "C", "source": "human", "category": "correctness", "verdict": "TAKE", "reason": "real bug",
         "root_intent": "unclear bound", "alternative": "", "verified": "", "owner": "", "log_ref": "", "escalated": ""}
    d.update(kw)
    return d


def status(**kw):
    return tc.check_row(row(**kw))["status"]


def test_clean_take_passes():
    assert status() == "PASS"


def test_every_verdict_needs_a_reason():
    assert status(reason="") == "FAIL"


def test_unknown_verdict_fails():
    assert status(verdict="MAYBE") == "FAIL"


def test_push_back_needs_an_alternative():
    # Fork 1/2: push-back = reason + alternative, not just "no"
    assert status(category="style", verdict="PUSH-BACK") == "FAIL"
    assert status(category="style", verdict="PUSH-BACK", alternative="keep + docstring") == "PASS"


def test_defer_must_be_logged():
    assert status(category="scope", verdict="DEFER") == "FAIL"
    assert status(category="scope", verdict="DEFER", log_ref="ISSUE-1") == "PASS"


@pytest.mark.parametrize("cat", ["correctness", "security", "legal", "ethics"])
def test_high_stakes_never_dropped_or_committed_silently(cat):
    # Fork 1 warning: correctness/security/legal/ethics -> escalate or write the risk down
    assert status(category=cat, verdict="COMMIT", owner="lead") == "FAIL"
    assert status(category=cat, verdict="DROP") == "FAIL"
    assert status(category=cat, verdict="DROP", escalated="risk log R-7") == "PASS"


def test_taste_commit_needs_owner():
    assert status(category="taste", verdict="COMMIT") == "FAIL"
    assert status(category="taste", verdict="COMMIT", owner="maintainer") == "PASS"


def test_automated_flag_applied_only_after_verification():
    # Fork 4: verify before apply - tools produce false positives
    assert status(source="automated", category="style", verdict="TAKE") == "FAIL"
    assert status(source="automated", category="style", verdict="TAKE", verified="Y") == "PASS"


def test_high_severity_automated_flag_checked_before_dismissing():
    assert status(source="automated", category="security", verdict="PUSH-BACK", alternative="x",
                  verified="N") == "FAIL"


def test_take_without_intent_is_a_warning():
    assert status(root_intent="") == "WARN"


def test_caved_and_ego_notes():
    caved = tc.check([row(id="1"), row(id="2", category="taste", root_intent="x")])
    assert any("caved" in n for n in caved["notes"])
    ego = tc.check([row(id="1", category="style", verdict="PUSH-BACK", alternative="a"),
                    row(id="2", category="style", verdict="DROP")])
    assert any("ego" in n for n in ego["notes"])


def test_shared_root_is_flagged_as_pattern():
    r = tc.check([row(id="1", root_intent="Naming unclear"), row(id="2", root_intent="naming unclear ")])
    assert any(n.startswith("pattern: comments 1, 2") for n in r["notes"])


def test_definition_of_done():
    assert tc.check([row(id="1"), row(id="2", category="scope", verdict="DEFER", log_ref="I-2")])["done"] is True
    assert tc.check([row(id="1", reason="")])["done"] is False
    assert tc.check([])["done"] is False


def test_must_fail_control_trust_automated_raw(monkeypatch):
    """Inject the trap 'apply automated review raw': verification is no longer required. Oracle must go red."""
    real = tc.check_row

    def raw(r):
        r = dict(r)
        if (r.get("source") or "").lower() == "automated":
            r["verified"] = "Y"
        return real(r)

    monkeypatch.setattr(tc, "check_row", raw)
    with pytest.raises(AssertionError):
        test_automated_flag_applied_only_after_verification()


def test_must_fail_control_silent_commit_on_correctness(monkeypatch):
    """Inject the trap 'disagree-and-commit on a correctness issue'. Oracle must go red."""
    monkeypatch.setattr(tc, "HIGH_STAKES", set())
    with pytest.raises(AssertionError):
        test_high_stakes_never_dropped_or_committed_silently("correctness")
