"""Oracle tests for histotech-cytology-judgment tools (fixation_time, stain_run_check).

No digest of ours gives fixation-time numbers, and the card refuses universal cut-offs ("verify the
edition"), so the limits here are TEST INPUTS, not claims; the oracle is calendar arithmetic done by hand
(2026-10-09 is a Friday, 2026-10-12 a Monday) and the decision rules written in the card:
  Fork 2: cold ischemia + under/over-fixation are flagged; fixation cannot be redone.
  Fork 5 + anti-pattern: a control that fails invalidates THAT assay; "negative" with a failed control is
      invalid, not negative; other antibodies in the same run are not affected; negative reagent control
      only per CAP/SOP. Same principle as immunodiagnostic digest §4 (control line absent = invalid) and
      503402 digest §4B (no ACTB control band = invalid).
Must-fail controls inject the traps; the oracle must go red.

Run from the repo root:  python -m pytest skills/histotech-cytology-judgment/evals -q
"""
import json
import os
import sys
from datetime import datetime

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import fixation_time  # noqa: E402
import stain_run_check  # noqa: E402

LOG = os.path.join(SKILL, "data", "fixation_log.csv")
RUN = os.path.join(SKILL, "data", "ihc_run_example.csv")
LIMITS = dict(max_cold_min=60, min_fix_h=6, max_fix_h=72)   # test inputs (example values, see module doc)
NOW = datetime(2026, 10, 8, 12, 15)


def by_specimen():
    return {sp: fixation_time.check(sp, c, i, o, NOW, **LIMITS) for sp, c, i, o in fixation_time.load_csv(LOG)}


# ---------------------------------------------------------------- fixation_time (card Fork 2)
def test_fixation_durations_by_hand():
    r = by_specimen()
    # S-01: 09:00 -> 09:30 = 30 min ; 09:30 -> 20:30 = 11 h -> within
    assert r["S-01"]["cold_ischemia_min"] == pytest.approx(30)
    assert r["S-01"]["fixation_h"] == pytest.approx(11)
    assert r["S-01"]["verdict"] == "WITHIN LIMITS"
    # S-02: 10:00 -> 11:45 = 105 min > 60 -> FLAG ; 11:45 -> next day 08:00 = 20.25 h
    assert r["S-02"]["cold_ischemia_min"] == pytest.approx(105)
    assert r["S-02"]["fixation_h"] == pytest.approx(20.25)
    assert r["S-02"]["verdict"].startswith("FLAG")
    # S-04: 16:20 -> 19:00 = 2 h 40 min = 2.6667 h < 6 -> under-fixed
    assert r["S-04"]["fixation_h"] == pytest.approx(8 / 3)
    assert any(f.startswith("UNDER-FIXED") for f in r["S-04"]["flags"])


def test_weekend_overfixation_counts_real_dates():
    # S-03: Fri 2026-10-09 15:00 -> Mon 2026-10-12 16:00 = 3 x 24 + 1 = 73 h > 72 -> OVER-FIXED
    r = by_specimen()["S-03"]
    assert r["fixation_h"] == pytest.approx(73)
    assert any(f.startswith("OVER-FIXED") for f in r["flags"])
    assert r["verdict"].startswith("FLAG")


def test_still_in_fixative_gives_window():
    # S-05: into 08:15, now 12:15 -> 4 h < 6 -> WAIT ; earliest 08:15 + 6 h = 14:15 ; latest + 72 h = 10-11 08:15
    r = by_specimen()["S-05"]
    assert r["fixation_h"] == pytest.approx(4)
    assert r["verdict"].startswith("WAIT")
    assert r["window"] == {"earliest_processing": "2026-10-08 14:15", "latest_processing": "2026-10-11 08:15"}


def test_no_limits_no_verdict_and_bad_order_rejected():
    c, i, o = datetime(2026, 10, 9, 14, 30), datetime(2026, 10, 9, 15, 0), datetime(2026, 10, 12, 16, 0)
    assert fixation_time.check("x", c, i, o)["verdict"].startswith("NO LIMITS SET")
    with pytest.raises(ValueError):
        fixation_time.check("x", i, c, o)          # into fixative before collection
    with pytest.raises(ValueError):
        fixation_time.check("x", c, o, i)          # out before into


def test_must_fail_control_clock_only_arithmetic(monkeypatch):
    """Inject the trap: subtract clock times and ignore the date (Fri 15:00 -> Mon 16:00 = '1 h')."""
    def clock_only(start, end):
        mins = (end.hour * 60 + end.minute) - (start.hour * 60 + start.minute)
        return (mins % (24 * 60)) / 60

    monkeypatch.setattr(fixation_time, "hours_between", clock_only)
    with pytest.raises(AssertionError):
        test_weekend_overfixation_counts_real_dates()


# ---------------------------------------------------------------- stain_run_check (card Fork 5)
def decisions(**kw):
    res = stain_run_check.evaluate(stain_run_check.load(RUN), **kw)
    return {(d["marker"], d["slide"]): d["decision"] for d in res["decisions"]}, res


def test_failed_positive_control_makes_negative_invalid_not_negative():
    d, _ = decisions()
    # HER2 positive control did not stain -> both patient "negatives" are INVALID, explicitly not true negatives
    assert d[("HER2", "S1")].startswith("INVALID") and "NOT a true negative" in d[("HER2", "S1")]
    assert d[("HER2", "S2")].startswith("INVALID")


def test_failure_is_per_marker_not_per_run():
    d, res = decisions()
    # ER controls passed in the same run -> ER S1 / S2 releasable
    assert d[("ER", "S1")] == "VALID - pos"
    assert d[("ER", "S2")] == "VALID - neg"
    assert res["restain"] == {"ER": ["S3"], "HER2": ["S1", "S2"], "PR": ["S1"], "Ki67": ["S1"]}


def test_slide_internal_neg_reagent_and_missing_controls():
    d, _ = decisions()
    assert d[("ER", "S3")].startswith("INVALID")       # internal control on S3 did not stain
    assert d[("PR", "S1")].startswith("INVALID")       # negative reagent control stained
    assert d[("Ki67", "S1")].startswith("INVALID")     # no positive control at all


def test_negative_reagent_control_only_when_policy_requires():
    d, _ = decisions(require_neg_control=True)
    assert d[("ER", "S1")].startswith("INVALID")       # ER had no negative reagent control


def test_weak_positive_control_is_held_not_decided():
    rows = [{"run": "R2", "marker": "PAS", "slide": "C", "role": "pos_control", "result": "weak"},
            {"run": "R2", "marker": "PAS", "slide": "S9", "role": "patient", "result": "neg"}]
    res = stain_run_check.evaluate(stain_run_check.parse(rows))
    assert res["decisions"][0]["decision"].startswith("HOLD")


def test_must_fail_control_control_ignored(monkeypatch):
    """Inject the anti-pattern: report the IHC result without honouring the control (failed control -> 'negative')."""
    monkeypatch.setattr(stain_run_check, "control_status", lambda role, result: "PASS")
    with pytest.raises(AssertionError):
        test_failed_positive_control_makes_negative_invalid_not_negative()


def test_must_fail_control_whole_run_invalidated(monkeypatch):
    """Inject the over-correction: one failed control voids every antibody in the run."""
    monkeypatch.setattr(stain_run_check, "group_key", lambda row: (row["run"],))
    with pytest.raises(AssertionError):
        test_failure_is_per_marker_not_per_run()


# ---------------------------------------------------------------- CLI contract
def test_cli_outputs(capsys):
    assert fixation_time.main(["--csv", LOG, "--max-cold-min", "60", "--min-fix-h", "6", "--max-fix-h", "72",
                               "--now", "2026-10-08 12:15"]) == 0
    out = capsys.readouterr().out
    assert "OVER-FIXED 73.0 h" in out and "ADVISORY" in out
    assert stain_run_check.main([RUN, "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert "ADVISORY" in data["advisory"] and data["restain"]["HER2"] == ["S1", "S2"]
