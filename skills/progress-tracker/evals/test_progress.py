"""Oracle tests for progress-tracker tool progress.py.

Expected values come from the card (skills/progress-tracker.md), NOT from the code:
  rule #1   : ✅ only for steps done AND seen; "started / ordered" != done -> ▶️ (กับดักเนียน)
  step 1    : status set ✅ ▶️ ⬜ ⏭️ ; ⏭️ = not relevant + say why ; "ตอนนี้อยู่ขั้น X / Y"
  example   : the card's own panel - 2 ✅, 1 ▶️, 2 ⬜ is printed as "(3/5)"
  traps     : 5-7 steps is enough; do not slice into 30
Slip numbers are hand date arithmetic in the comments.
Must-fail controls inject the "theatre" traps and require the oracle tests to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import datetime as dt
import os
import subprocess
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import progress as pg  # noqa: E402

SCRIPT = os.path.join(SKILL, "scripts", "progress.py")
EXAMPLE = os.path.join(SKILL, "data", "steps_example.csv")
TODAY = dt.date(2026, 10, 8)


def rows(*specs):
    """specs: (step, status, evidence, reason[, due, finished])"""
    out = []
    for i, s in enumerate(specs, 1):
        s = list(s) + [""] * (6 - len(s))
        out.append({"row": i, "step": s[0], "status": s[1], "evidence": s[2], "reason": s[3],
                    "due": s[4], "finished": s[5]})
    return out


def kinds(res):
    return [f["kind"] for f in res["findings"]]


def test_card_example_is_3_of_5():
    # card example: ✅ ✅ ▶️ ⬜ ⬜ -> "📊 ความคืบหน้า (3/5)"; % done = 2/5 = 40
    res = pg.evaluate(pg.load(EXAMPLE), TODAY)
    s = res["summary"]
    assert (s["position"], s["total"], s["done"]) == (3, 5, 2)
    assert s["percent_done"] == pytest.approx(40.0)
    assert [p["shown"] for p in res["panel"]] == ["done", "done", "doing", "todo", "todo"]


def test_done_without_evidence_is_shown_as_doing():
    # rule #1: no seen result = ▶️ not ✅. 1 real ✅ + 1 claimed ✅ (no evidence) + 1 ⬜ -> 1 done of 3
    res = pg.evaluate(rows(("a", "done", "pytest 12 passed", ""), ("b", "done", "", ""), ("c", "todo", "", "")), TODAY)
    assert [p["shown"] for p in res["panel"]] == ["done", "doing", "todo"]
    assert res["summary"]["done"] == 1 and res["summary"]["position"] == 2
    assert "DONE_WITHOUT_EVIDENCE" in kinds(res)


def test_started_is_not_evidence():
    # กับดักเนียน: "สั่งแล้ว" / "started" means the step was requested, not that a result was seen
    for ev in ("สั่งแล้ว", "started", "รอผล"):
        res = pg.evaluate(rows(("run tests", "done", ev, "")), TODAY)
        assert res["panel"][0]["shown"] == "doing", ev
        assert res["summary"]["done"] == 0


def test_skip_needs_a_reason_and_leaves_the_denominator():
    # step 1: ⏭️ = not relevant + reason. Skipped steps are not work left: 1 ✅ of 2 active = 50%
    res = pg.evaluate(rows(("a", "done", "file saved: out.csv", ""), ("b", "skip", "", ""),
                           ("c", "skip", "", "ไม่เกี่ยวกับโจทย์"), ("d", "todo", "", "")), TODAY)
    assert res["summary"]["total"] == 2 and res["summary"]["percent_done"] == pytest.approx(50.0)
    assert kinds(res).count("SKIP_WITHOUT_REASON") == 1


def test_more_than_seven_steps_warns():
    many = rows(*[("s%d" % i, "todo", "", "") for i in range(8)])
    assert "TOO_MANY_STEPS" in kinds(pg.evaluate(many, TODAY))
    seven = rows(*[("s%d" % i, "todo", "", "") for i in range(7)])
    assert "TOO_MANY_STEPS" not in kinds(pg.evaluate(seven, TODAY))


def test_slip_late_and_overdue():
    # done: due 2026-10-01, finished 2026-10-04 -> +3 late
    # open: due 2026-10-05, today 2026-10-08 -> +3 overdue ; open, due 2026-10-10 -> not slipped
    res = pg.evaluate(rows(("a", "done", "report sent, read-back OK", "", "2026-10-01", "2026-10-04"),
                           ("b", "doing", "", "", "2026-10-05"),
                           ("c", "todo", "", "", "2026-10-10")), TODAY)
    assert [p["slip_days"] for p in res["panel"]] == [3, 3, None]
    assert res["summary"]["max_slip_days"] == 3


def test_early_finish_is_not_slip():
    res = pg.evaluate(rows(("a", "done", "ok", "", "2026-10-05", "2026-10-03")), TODAY)
    assert "SLIP" not in kinds(res)


def test_cli_strict_under_cp874():
    env = dict(os.environ, PYTHONIOENCODING="cp874")
    csv_text = "step,status,evidence,reason\nรัน test,✅,สั่งแล้ว,\n"
    p = subprocess.run([sys.executable, SCRIPT, "-", "--strict"], input=csv_text, capture_output=True,
                       text=True, encoding="utf-8", env=env)
    assert p.returncode == 1 and "DONE_WITHOUT_EVIDENCE" in p.stdout


# ---------------------------------------------------------------- must-fail controls
def test_must_fail_control_tick_on_status_alone(monkeypatch):
    """Theatre trap: count ✅ because the status column says done, without a seen result."""
    monkeypatch.setattr(pg, "is_verified_done", lambda row: row["status"] == "done")
    with pytest.raises(AssertionError):
        test_done_without_evidence_is_shown_as_doing()


def test_must_fail_control_started_counts_as_done(monkeypatch):
    """กับดักเนียน: any non-empty evidence (even 'สั่งแล้ว') accepted as proof."""
    monkeypatch.setattr(pg, "NOT_EVIDENCE", pg.re.compile(r"(?!x)x"))
    with pytest.raises(AssertionError):
        test_started_is_not_evidence()
