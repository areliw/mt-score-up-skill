"""Oracle tests for offload-to-automation tool roi.py.

Expected verdicts come from the card's table (skills/offload-to-automation.md, "ทำเอง vs โยน automation"):
  row A: ทำครั้งเดียว / กฎเปลี่ยนตลอด / ปริมาณน้อย -> ทำมือ (เวลาที่เสียเขียน+ดูแล > เวลาที่ประหยัด)
  row B: ซ้ำ + กฎนิ่ง + ทำบ่อย + ใช้ไปอีกนาน -> automation (คุ้ม ROI)
  ⛔ box: พลาดแล้วมีผล = ใช้ tool (accuracy is its own reason)
  step 4: verify always -> checking output is a per-run cost
Numbers are hand arithmetic in the comments, not read from the code.
Must-fail controls inject the two ROI traps (ignore frequency; ignore upkeep) and require red.

Run from the skill folder:  python -m pytest evals -q
"""
import math
import os
import subprocess
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import roi  # noqa: E402

SCRIPT = os.path.join(SKILL, "scripts", "roi.py")


def test_repeated_stable_task_automates():
    # row B. 20 min by hand, 2 min to launch+check, 8x/month, 4 h build, 0.5 h/month upkeep, 12 months
    # saved = 18 x 8 / 60 = 2.4 h/mo · net = 2.4 - 0.5 = 1.9 · break-even = 4 / 1.9 = 2.105 mo
    # net@12 = 1.9 x 12 - 4 = 18.8 h
    r = roi.roi(20, 2, 8, 4, maintain_hours_per_month=0.5, horizon_months=12)
    assert r["saved_hours_per_month"] == pytest.approx(2.4)
    assert r["net_hours_per_month"] == pytest.approx(1.9)
    assert r["breakeven_months"] == pytest.approx(4 / 1.9)
    assert r["net_hours_at_horizon"] == pytest.approx(18.8)
    assert r["verdict"] == "AUTOMATE"


def test_one_off_is_manual():
    # row A "ทำครั้งเดียว": 1 run of 30 min over 12 months = 1/12 run/mo, build 2 h
    # saved = 30 x (1/12) / 60 = 0.041667 h/mo -> break-even 48 months > 12 -> MANUAL
    r = roi.roi(30, 0, 1 / 12, 2, horizon_months=12)
    assert r["breakeven_months"] == pytest.approx(48)
    assert r["verdict"] == "MANUAL"


def test_one_off_but_error_costly_is_script_once():
    # ⛔ box: mistakes cost something -> still compute with a tool, but do not build a system
    r = roi.roi(30, 0, 1 / 12, 2, horizon_months=12, error_costly=True)
    assert r["verdict"] == "SCRIPT-ONCE"


def test_rules_keep_changing_never_breaks_even():
    # row A "กฎเปลี่ยนตลอด": 10 min -> 1 min, 4x/mo: saved = 9 x 4 / 60 = 0.6 h/mo
    # rules change monthly (12/yr) x 1 h rework = 1.0 h/mo upkeep -> net = -0.4 -> never
    r = roi.roi(10, 1, 4, 3, rule_changes_per_year=12, rework_hours=1, horizon_months=24)
    assert r["upkeep_hours_per_month"] == pytest.approx(1.0)
    assert r["net_hours_per_month"] == pytest.approx(-0.4)
    assert r["breakeven_months"] == math.inf
    assert r["verdict"] == "MANUAL"


def test_short_horizon_turns_a_good_automation_manual():
    # row B needs "ใช้ไปอีกนาน": 15 -> 3 min, 5x/mo: saved = 12 x 5 / 60 = 1.0 h/mo, build 10 h
    # break-even 10 months: horizon 6 -> MANUAL, horizon 18 -> AUTOMATE
    assert roi.roi(15, 3, 5, 10, horizon_months=6)["verdict"] == "MANUAL"
    assert roi.roi(15, 3, 5, 10, horizon_months=18)["verdict"] == "AUTOMATE"


def test_zero_check_time_is_warned():
    # step 4: verifying output is never free
    assert any("auto_min = 0" in n for n in roi.roi(20, 0, 8, 4)["notes"])


def test_cli_runs_total_and_json_under_cp874():
    env = dict(os.environ, PYTHONIOENCODING="cp874")
    p = subprocess.run([sys.executable, SCRIPT, "--manual-min", "30", "--runs-total", "1", "--build-hours", "2",
                        "--json"], capture_output=True, text=True, encoding="utf-8", env=env)
    assert p.returncode == 0, p.stderr
    assert '"verdict": "MANUAL"' in p.stdout


# ---------------------------------------------------------------- must-fail controls
def test_must_fail_control_ignore_frequency(monkeypatch):
    """Trap: 'automation is faster per run, so it pays' - per-run saving without x runs/month."""
    monkeypatch.setattr(roi, "monthly_saving_hours", lambda manual, auto, runs: (manual - auto) / 60.0)
    with pytest.raises(AssertionError):
        test_repeated_stable_task_automates()


def test_must_fail_control_ignore_upkeep(monkeypatch):
    """Trap: 'build once and forget' - rule changes and maintenance left out of the cost."""
    monkeypatch.setattr(roi, "monthly_upkeep_hours", lambda m, n, h: 0.0)
    with pytest.raises(AssertionError):
        test_rules_keep_changing_never_breaks_even()
