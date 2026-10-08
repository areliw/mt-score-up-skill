"""Oracle tests for applied-microbiology-judgment tool plate_count.py.

Expected values come from the owner's digests + hand arithmetic, NOT from the code:
  AM     = 06_Background_MedTech/APPLIED-MICROBIOLOGY/APPLIED-MICRO-DIGEST-2026-06-01.md §2
           ("CFU/mL = avg colony x dilution factor / mL; count 30-300 only, outside = discard")
  508304 = 06_Background_MedTech/508304-CLINICAL-MICROBIOLOGY-2-LECTURE/508304-LECTURE-DIGEST-2026-06-01.md §3
           (APC: count 25-250; N = sum(C) / [(1 x n1) + (0.1 x n2)] x d)
  card   = skills/applied-microbiology-judgment.md (rule #1 deeper trap: not detected != absent)
Must-fail controls inject the traps and require the oracle tests to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import plate_count as pc  # noqa: E402


def plates(*specs):
    return [pc.parse_plate(s) for s in specs]


def test_single_dilution_avg_times_df():
    # AM §2: CFU/mL = avg x DF / mL. 150 and 170 at 1e-2, 1 mL: avg 160 x 100 = 16,000 CFU/mL
    res = pc.plate_count(plates("1e-2:150", "1e-2:170"), 30, 300, 1)
    assert res["valid"] and res["n"] == pytest.approx(16000)


def test_two_dilution_formula_508304():
    # 508304 §3: N = sum(C) / ((n1 + 0.1 n2) x d1). 1e-2: 232, 244; 1e-3: 33, 28 (all in 25-250)
    # sum(C) = 537; n1 = 2, n2 = 2 -> 537 / (2.2 x 0.01) = 537 / 0.022 = 24,409.09
    res = pc.plate_count(plates("1e-2:232", "1e-2:244", "1e-3:33", "1e-3:28"), 25, 250, 1)
    assert res["n"] == pytest.approx(537 / 0.022)


def test_out_of_range_plates_are_discarded():
    # same series + TNTC at 1e-1 and 2, 4 at 1e-4: those plates sit outside 25-250 and must not move N
    res = pc.plate_count(plates("1e-1:TNTC", "1e-1:300", "1e-2:232", "1e-2:244", "1e-3:33", "1e-3:28",
                                "1e-4:2", "1e-4:4"), 25, 250, 1)
    assert res["n"] == pytest.approx(537 / 0.022)
    assert [p["counted"] for p in res["plates"]] == [False, False, True, True, True, True, False, False]


def test_range_choice_changes_which_plates_count():
    # 30-300 (AM §2) drops the 28-colony plate: (232 + 244 + 33) / (0.01 + 0.01 + 0.001) = 509 / 0.021
    res = pc.plate_count(plates("1e-2:232", "1e-2:244", "1e-3:33", "1e-3:28"), 30, 300, 1)
    assert res["n"] == pytest.approx(509 / 0.021)


def test_volume_plated_divides():
    # spread plate 0.1 mL: 150, 170 at 1e-2 -> 160 x 100 / 0.1 = 160,000 CFU/mL
    assert pc.plate_count(plates("1e-2:150", "1e-2:170"), 30, 300, 0.1)["n"] == pytest.approx(160000)


def test_must_fail_control_count_every_plate(monkeypatch):
    """Inject the card's counting trap: no countable-range filter (TNTC-ish 300 + 2/4-colony plates counted)."""
    monkeypatch.setattr(pc, "in_range", lambda count, low, high: count is not None)
    with pytest.raises(AssertionError):
        test_out_of_range_plates_are_discarded()


def test_all_zero_is_below_detection_limit_not_zero():
    # card rule #1 deeper trap: 'not detected' != 'absent'. 0, 0 at 1e-1, 1 mL -> LOD = 1 / (0.1 x 1) = 10
    res = pc.plate_count(plates("1e-1:0", "1e-1:0"), 30, 300, 1)
    assert res["n"] is None
    assert res["detection_limit"] == pytest.approx(10)
    assert res["report"].startswith("< 10")


def test_must_fail_control_zero_reported_as_zero(monkeypatch):
    """Inject the trap: pool zero plates as a real count (reports 0 = 'absent')."""
    real = pc.plate_count

    def zero_as_count(pl, low, high, volume, limit=None):
        if all(p["count"] == 0 for p in pl):
            return {"valid": True, "n": 0.0, "report": "0", "plates": pl}
        return real(pl, low, high, volume, limit)
    monkeypatch.setattr(pc, "plate_count", zero_as_count)
    with pytest.raises(AssertionError):
        test_all_zero_is_below_detection_limit_not_zero()


def test_below_range_is_not_a_valid_count():
    # AM §2: outside 30-300 = discard. 12, 15 at 1e-1 -> no valid count; EST only = 13.5 x 10 = 135
    res = pc.plate_count(plates("1e-1:12", "1e-1:15"), 30, 300, 1)
    assert res["valid"] is False and res["n"] is None
    assert res["estimate"] == pytest.approx(135)
    assert "NOT a valid count" in res["report"]


def test_above_range_is_not_a_valid_count():
    res = pc.plate_count(plates("1e-1:TNTC", "1e-2:400"), 30, 300, 1)
    assert res["valid"] is False and "re-plate" in res["report"]


def test_limit_comparison_uses_user_limit():
    # 508304 §3 teaching line: SPC >= 1e6 CFU/g = spoiled. 120, 110 at 1e-4 -> 115 x 10,000 = 1.15e6 >= 1e6
    res = pc.plate_count(plates("1e-4:120", "1e-4:110"), 30, 300, 1, limit=1e6)
    assert res["n"] == pytest.approx(1.15e6) and res["vs_limit"].startswith("AT/ABOVE")
    # detection limit above the limit -> cannot judge (absence not shown)
    res0 = pc.plate_count(plates("1e-1:0"), 30, 300, 1, limit=5)
    assert res0["vs_limit"].startswith("CANNOT JUDGE")


def test_cli_teaching_input(capsys):
    assert pc.main(["--input", os.path.join(SKILL, "data", "apc_two_dilutions_teaching.json")]) == 0
    out = capsys.readouterr().out
    assert "2.441e+04" in out and "ADVISORY" in out


def test_cli_requires_range():
    with pytest.raises(SystemExit):
        pc.main(["--volume", "1", "--plate", "1e-2:100"])
