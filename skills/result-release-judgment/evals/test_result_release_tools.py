"""Oracle tests for result-release-judgment tools.

Expected outcomes come from the result-release-judgment card (Fork 1 layer order, Fork 2 delta
investigation + "plausible != right patient", Fork 3 auto-release stop-conditions, Fork 4 critical
notification requirements) applied by hand to constructed teaching values. Arithmetic is in the comments.
Must-fail controls inject the traps the card lists and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import critical_log_check as clc  # noqa: E402
import delta_check as dc  # noqa: E402
import release_gate as rg  # noqa: E402


# ---------------------------------------------------------------- delta_check (card Fork 2)
def test_delta_arithmetic_uses_previous_as_denominator():
    # prev 4.0 -> cur 6.0: delta = +2.0 ; delta% = 2.0 / 4.0 x 100 = +50%  (not 2.0/6.0 = 33%)
    r = dc.delta(4.0, 6.0, pct_limit=40)
    assert r["delta_abs"] == pytest.approx(2.0)
    assert r["delta_pct"] == pytest.approx(50.0)
    assert r["flagged"] is True
    # prev 5 -> cur 4: -1/5 = -20% (a current-value denominator would give -25%)
    assert dc.delta(5.0, 4.0, pct_limit=30)["delta_pct"] == pytest.approx(-20.0)


def test_delta_within_limit_passes():
    # Cr 1.0 -> 1.1: +10% <= 20% limit
    assert dc.delta(1.0, 1.1, pct_limit=20)["flagged"] is False


def test_abs_limit_is_two_sided():
    assert dc.delta(4.0, 2.9, abs_limit=1.0)["flagged"] is True     # |-1.1| > 1.0


def test_limits_are_required():
    with pytest.raises(ValueError):
        dc.delta(4.0, 6.0)


def test_flag_inside_reference_range_is_still_hold():
    # card Fork 2: "do not release because the new value looks plausible" - K 3.6 -> 4.9 (ref 3.5-5.0)
    r = dc.delta(3.6, 4.9, abs_limit=1.0, ref_low=3.5, ref_high=5.0)
    assert r["flagged"] and r["current_in_ref_range"] is True
    assert r["decision"].startswith("HOLD")
    assert r["investigate"][0].startswith("1 specimen identity")   # mix-up first


def test_panel_wide_shift_raises_mix_up_note():
    rows = [{"analyte": "K", "prev": "4.0", "cur": "6.1", "abs_limit": "1.0"},
            {"analyte": "Hb", "prev": "13", "cur": "8.1", "pct_limit": "20"},
            {"analyte": "Cr", "prev": "1.0", "cur": "1.1", "pct_limit": "20"}]
    r = dc.panel(rows)
    assert r["flagged"] == 2 and "mix-up" in r["panel_note"] and "not proof" in r["panel_note"]


def test_must_fail_control_release_because_plausible(monkeypatch):
    """Inject the trap 'release because the new value looks plausible'. The oracle must go red."""
    def plausible_release(flagged, in_ref):
        return "RELEASE" if (not flagged or in_ref) else "HOLD - investigate before release"

    monkeypatch.setattr(dc, "decide", plausible_release)
    with pytest.raises(AssertionError):
        test_flag_inside_reference_range_is_still_hold()


# ---------------------------------------------------------------- release_gate (card Fork 1/3/4)
LIM = {"amr_low": 1.0, "amr_high": 10.0, "crit_low": 2.5, "crit_high": 6.5, "delta_abs": 1.0, "delta_pct": None}


def res(**kw):
    d = {"id": "x", "analyte": "K", "value": 4.4, "qc": "pass", "integrity": "ok", "instrument_flag": False}
    d.update(kw)
    return d


def test_clean_result_is_auto_release_eligible():
    r = rg.evaluate(res(prev=4.1), LIM)
    assert r["auto_release"] is True and r["action"] == "AUTO-RELEASE eligible"


def test_qc_fail_stops_first_even_if_everything_else_is_fine():
    r = rg.evaluate(res(qc="fail"), LIM)
    assert r["action"].startswith("STOP at 1 QC") and r["auto_release"] is False


def test_unknown_qc_is_a_stop_not_a_pass():
    r = rg.evaluate(res(qc=None), LIM)
    assert r["action"].startswith("STOP at 1 QC")


def test_hemolyzed_stops_at_integrity():
    assert rg.evaluate(res(integrity="hemolyzed"), LIM)["action"].startswith("STOP at 2 integrity")


def test_above_amr_offers_dilution_or_greater_than_not_always_dilute():
    r = rg.evaluate(res(value=12.0), LIM)
    amr = [x for x in r["layers"] if x["layer"] == "3 flag/AMR"][0]["msg"]
    assert "validated dilution" in amr and "'>10'" in amr


def test_critical_is_notify_never_auto_release():
    # K 7.0 > crit_high 6.5, everything else clean -> release + notify, not auto (card Fork 3/4)
    r = rg.evaluate(res(value=7.0), LIM)
    assert r["auto_release"] is False and "NOTIFY CRITICAL" in r["action"]


def test_delta_fire_stops_auto_release():
    r = rg.evaluate(res(value=5.6, prev=4.1), LIM)             # |1.5| > 1.0
    assert r["action"].startswith("STOP at 4 delta")


def test_missing_critical_limits_cannot_auto_release():
    lim = dict(LIM, crit_low=None, crit_high=None)
    assert rg.evaluate(res(), lim)["auto_release"] is False


def test_must_fail_control_autoverify_without_critical_stop(monkeypatch):
    """Inject the trap 'auto-verify with no critical stop-rule' -> criticals leak out silently."""
    monkeypatch.setattr(rg, "AUTO_CONDITIONS", ("qc", "integrity", "amr_flag", "delta"))
    with pytest.raises(AssertionError):
        test_critical_is_notify_never_auto_release()


# ---------------------------------------------------------------- critical_log_check (card Fork 4)
GOOD = {"id1": "HN-T1", "id2": "DOB-T1", "analyte": "K", "value": "7.0", "unit": "mmol/L",
        "result_time": "2026-10-08 09:00", "call_time": "2026-10-08 09:12", "caller": "MT-A",
        "receiver": "RN-B", "receiver_role": "nurse", "method": "verbal", "read_back": "Y", "reached": "Y"}


def row(**kw):
    d = dict(GOOD)
    d.update(kw)
    return d


def test_complete_call_passes_and_minutes_are_right():
    r = clc.check_row(GOOD, 30)
    assert r["status"] == "PASS" and r["minutes"] == pytest.approx(12)   # 09:00 -> 09:12


def test_verbal_without_read_back_fails():
    assert "verbal call without read-back" in clc.check_row(row(read_back="N"), 30)["problems"]


def test_electronic_call_does_not_need_read_back():
    assert clc.check_row(row(method="electronic", read_back=""), 30)["status"] == "PASS"


def test_late_call_fails_against_lab_limit():
    r = clc.check_row(row(call_time="2026-10-08 10:10"), 30)   # 70 min > 30
    assert r["status"] == "FAIL" and r["minutes"] == pytest.approx(70)


def test_one_identifier_fails():
    assert clc.check_row(row(id2=""), 30)["status"] == "FAIL"


def test_unreached_needs_escalation():
    bad = row(reached="N", receiver="", receiver_role="", call_time="", method="", read_back="")
    assert "nobody reached and no escalation recorded" in clc.check_row(bad, 30)["problems"]
    ok = dict(bad, escalated_to="charge nurse", escalation_time="2026-10-08 09:20")
    assert clc.check_row(ok, 30)["status"] == "PASS"                     # 20 min to escalation


def test_summary_counts():
    s = clc.check([GOOD, row(read_back="N")], 30)
    assert s["n"] == 2 and s["pass"] == 1 and s["done"] is False and s["median_minutes"] == pytest.approx(12)


def test_must_fail_control_no_read_back_check(monkeypatch):
    """Inject the trap 'critical called but no read-back': strip the read-back rule. Oracle must go red."""
    real = clc.check_row

    def lax(r, max_minutes, min_ids=2):
        out = real(r, max_minutes, min_ids)
        out["problems"] = [p for p in out["problems"] if "read-back" not in p]
        out["status"] = "FAIL" if out["problems"] else "PASS"
        return out

    monkeypatch.setattr(clc, "check_row", lax)
    with pytest.raises(AssertionError):
        test_verbal_without_read_back_fails()
