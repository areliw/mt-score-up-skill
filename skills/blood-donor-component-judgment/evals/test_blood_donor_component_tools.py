"""Oracle tests for blood-donor-component-judgment tools (donor_eligibility, component_qc, unit_return).

Expected values come from the owner's course digests and the card, NOT from the code under test:
  512303 = 06_Background_MedTech/512303-TRANSFUSION-SCIENCE-1/512303-DIGEST-2026-05-31.md
           §10.1 donor criteria (teaching values), §10.6 transport temperatures
  512304 = 06_Background_MedTech/512304-TRANSFUSION-SCIENCE-2/512304-DIGEST-2026-06-01.md
           §9 component QC: volume = (bag weight - empty bag)/SG; QC >= 1% of each component
  card   = skills/blood-donor-component-judgment.md Fork 1 (defer protects both), Fork 5 (QC escalation),
           Fork 6 (return to stock needs time AND temperature)
Hand arithmetic is in the comments. Must-fail controls inject the card's traps and must go red.

Run from the skill folder:  python -m pytest evals -q
"""
import csv
import json
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import component_qc  # noqa: E402
import donor_eligibility  # noqa: E402
import unit_return  # noqa: E402

CRITERIA_PATH = os.path.join(SKILL, "data", "criteria_teaching_512303_whole_blood.json")
QC_CSV = os.path.join(SKILL, "data", "platelet_qc_teaching.csv")
with open(CRITERIA_PATH, encoding="utf-8") as _f:
    CRITERIA = json.load(_f)


def donor(**kw):
    base = {"sex": "F", "age": 22, "weight_kg": 48, "hb": 12.9, "hct": None, "temp_c": 36.8, "sbp": 118,
            "dbp": 76, "pulse": 72, "days_since_last": 120, "first_time": False}
    base.update(kw)
    return donor_eligibility.evaluate(base, CRITERIA)


def result_of(res, prefix):
    return next(r["result"] for r in res["rows"] if r["criterion"].startswith(prefix))


# ================================================================ donor_eligibility (512303 §10.1, card Fork 1)
def test_teaching_criteria_file_matches_digest():
    # 512303 §10.1: age 17-70, first-time <=60, weight >45, temp <37.5, BP <160/<100, pulse 50-100,
    # Hb F 12.5-16.5 / M 13.0-18.5, Hct F 37-49 / M 39-55
    c = CRITERIA
    assert c["age_years"] == {"min": 17, "max": 70} and c["first_time_age_max"] == 60
    assert c["weight_kg"] == {"min": 45} and c["temp_c"] == {"max_exclusive": 37.5}  # TRC: 45 kg and above
    assert c["sbp_mmhg"] == {"max_exclusive": 160} and c["dbp_mmhg"] == {"max_exclusive": 100}
    assert c["hb_g_dl"]["F"] == {"min": 12.5, "max": 16.5} and c["hb_g_dl"]["M"] == {"min": 13.0, "max": 18.5}
    assert "NOT an SOP" in c["_label"]


def test_female_48kg_all_in_range_350ml():
    # 512303 §10.1: 45-50 kg -> 350 mL bag
    r = donor()
    assert r["overall"] == "MEASURED CRITERIA MET" and r["collection_volume_ml"] == 350


def test_male_hb_12_8_is_deferred():
    # M Hb lower limit 13.0 -> 12.8 defers (the F limit 12.5 would wrongly accept)
    r = donor(sex="M", hb=12.8, weight_kg=70)
    assert result_of(r, "Hb") == "DEFER (temporary)" and r["overall"] == "DEFER"


def test_female_hb_12_8_passes():
    assert result_of(donor(hb=12.8), "Hb") == "PASS"


def test_hb_upper_limit_defers():
    # F upper limit 16.5 -> 16.8 defers (polycythaemia side of the range)
    assert result_of(donor(hb=16.8), "Hb") == "DEFER (temporary)"


@pytest.mark.parametrize("w,overall,vol", [(44.9, "DEFER", None), (45, "MEASURED CRITERIA MET", 350),
                                           (49.9, "MEASURED CRITERIA MET", 350), (50, "MEASURED CRITERIA MET", 450)])
def test_weight_boundaries(w, overall, vol):
    # Thai Red Cross: "น้ำหนัก 45 กิโลกรัมขึ้นไป" (45 inclusive); owner 2026-10-08: 45 to <50 kg -> 350 mL, >=50 -> 450 mL
    r = donor(weight_kg=w)
    assert r["overall"] == overall and r["collection_volume_ml"] == vol


def test_temperature_37_5_defers():
    assert result_of(donor(temp_c=37.5), "temperature") == "DEFER (temporary)"


def test_first_time_age_limit():
    assert donor(age=61, first_time=True)["overall"] == "DEFER"          # first-time <= 60
    assert donor(age=61, first_time=False)["overall"] == "MEASURED CRITERIA MET"


def test_age_17_needs_consent():
    assert any("consent" in n for n in donor(age=17)["notes"])


def test_interval_too_short_defers():
    assert result_of(donor(days_since_last=60), "days since") == "DEFER (temporary)"


def test_missing_hb_is_incomplete_not_pass():
    r = donor(hb=None)
    assert r["overall"].startswith("INCOMPLETE")


def test_missing_bp_is_incomplete_not_pass():
    assert donor(sbp=None)["overall"].startswith("INCOMPLETE")


def test_hb_without_sex_is_not_assessed():
    assert donor(sex=None)["overall"].startswith("INCOMPLETE")


def test_empty_criteria_never_passes():
    r = donor_eligibility.evaluate({"sex": "F", "hb": 13}, {})
    assert r["overall"].startswith("INCOMPLETE")


def test_must_fail_control_sex_agnostic_hb(monkeypatch):
    """Trap: one Hb cut-off for everyone (the loosest), so a male at 12.8 is accepted."""
    def loosest(criteria, key, sex):
        block = criteria.get(key) or {}
        return {"min": min(v["min"] for v in block.values())} if block else None

    monkeypatch.setattr(donor_eligibility, "sex_spec", loosest)
    with pytest.raises(AssertionError):
        test_male_hb_12_8_is_deferred()


def test_must_fail_control_missing_counts_as_pass(monkeypatch):
    """Trap: soft-fail - a value nobody measured is treated as within range."""
    original = donor_eligibility.judge
    monkeypatch.setattr(donor_eligibility, "judge", lambda v, s: "PASS" if v is None else original(v, s))
    with pytest.raises(AssertionError):
        test_missing_hb_is_incomplete_not_pass()
    with pytest.raises(AssertionError):
        test_missing_bp_is_incomplete_not_pass()


# ================================================================ component_qc (512304 §9, card Fork 5)
def test_volume_from_weight():
    # (312 - 52) / 1.03 = 260 / 1.03 = 252.427
    assert component_qc.volume_ml(312, 52, 1.03)["volume_ml"] == pytest.approx(252.427, abs=1e-3)


@pytest.mark.parametrize("produced,expected", [(850, 9), (100, 1), (1000, 10), (1, 1)])
def test_sample_size_one_percent(produced, expected):
    # 512304 §9: >= 1% -> ceil(850 x 0.01 = 8.5) = 9; 100 -> 1; 1000 -> 10; 1 -> ceil(0.01) = 1
    assert component_qc.sample_size(produced)["units_to_qc"] == expected


def test_sample_size_sop_minimum():
    assert component_qc.sample_size(100, 1, min_units=4)["units_to_qc"] == 4


def rows(*vals, cols=("unit", "a")):
    return [dict(zip(cols, v)) for v in vals]


def test_teaching_csv_isolated_failure():
    # data/platelet_qc_teaching.csv: plt_e11 limit 2.4 (placeholder) -> T03 (2.2) fails; 7/8 = 0.875 >= 0.75
    with open(QC_CSV, encoding="utf-8", newline="") as f:
        data = list(csv.DictReader(f))
    specs = component_qc.parse_specs(["plt_e11:2.4::0.75"], ["culture=neg"], 0.9)
    r = component_qc.evaluate_batch(data, specs, ["culture"])
    assert r["failed_units"] == ["T03"] and r["verdict"] == "PASS WITH ISOLATED FAILURES"


def test_batch_fail_when_proportion_below_required():
    # 2 of 4 pass = 0.50 < required 0.75 -> lot-level action (card Fork 5)
    specs = component_qc.parse_specs(["a:10::0.75"], [], None)
    r = component_qc.evaluate_batch(rows(("u1", "12"), ("u2", "8"), ("u3", "11"), ("u4", "9")), specs)
    assert r["per_param"]["a"]["proportion"] == pytest.approx(0.5)
    assert r["verdict"] == "BATCH FAIL"


def test_critical_failure_is_red_flag_even_if_rate_met():
    specs = component_qc.parse_specs([], ["culture=neg:0.5"], None)
    data = rows(("u1", "neg"), ("u2", "pos"), ("u3", "neg"), ("u4", "neg"), cols=("unit", "culture"))
    assert component_qc.evaluate_batch(data, specs, ["culture"])["verdict"] == "RED FLAG"


def test_untested_value_is_incomplete():
    specs = component_qc.parse_specs(["a:10::0.5"], [], None)
    r = component_qc.evaluate_batch(rows(("u1", "12"), ("u2", ""), ("u3", "11")), specs)
    assert r["verdict"] == "INCOMPLETE"


def test_pass_rate_has_no_default():
    with pytest.raises(ValueError):
        component_qc.parse_specs(["a:10:"], [], None)


def test_must_fail_control_discard_and_walk_on(monkeypatch):
    """Trap (card Fork 5): drop the failed units and carry on, never looking at the lot."""
    monkeypatch.setattr(component_qc, "batch_verdict",
                        lambda per_param, failed, critical: ("PASS WITH ISOLATED FAILURES", "discard failed units")
                        if failed else ("PASS", ""))
    with pytest.raises(AssertionError):
        test_batch_fail_when_proportion_below_required()


# ================================================================ unit_return (card Fork 6; 512303 §10.6)
# limits used here: 30 min (the card's "30-min rule" example) and RBC transport 1-10 C (512303 §10.6)
def test_within_time_and_temperature_returns():
    assert unit_return.decide(20, 30, 6, 1, 10)["decision"] == "RETURN TO STOCK"


def test_time_ok_but_temperature_out_is_quarantined():
    assert unit_return.decide(20, 30, 12, 1, 10)["decision"].startswith("QUARANTINE")


def test_temperature_not_measured_is_quarantined():
    assert unit_return.decide(20, 30, None, 1, 10)["decision"].startswith("QUARANTINE")


def test_time_exceeded_is_quarantined():
    assert unit_return.decide(45, 30, 6, 1, 10)["decision"].startswith("QUARANTINE")


def test_integrity_compromised_is_quarantined():
    assert unit_return.decide(10, 30, 5, 1, 10, "compromised")["decision"].startswith("QUARANTINE")


def test_must_fail_control_time_only(monkeypatch):
    """Trap (card Fork 6): judging the return on time alone when the cold chain broke."""
    def time_only(minutes_out, max_minutes, temp_c, lo, hi, integrity="not recorded"):
        ok = minutes_out is not None and minutes_out <= max_minutes
        return {"decision": "RETURN TO STOCK" if ok else "QUARANTINE"}

    monkeypatch.setattr(unit_return, "decide", time_only)
    with pytest.raises(AssertionError):
        test_time_ok_but_temperature_out_is_quarantined()


def test_unit_return_limits_are_required():
    with pytest.raises(SystemExit):
        unit_return.main(["--minutes-out", "20", "--temp-c", "5", "--temp-range", "1:10"])


# ================================================================ every CLI output is advisory
@pytest.mark.parametrize("mod,args", [
    (donor_eligibility, ["--criteria", CRITERIA_PATH, "--sex", "F", "--age", "22", "--weight-kg", "48",
                         "--hb", "12.9", "--temp-c", "36.8", "--sbp", "118", "--dbp", "76", "--pulse", "72",
                         "--days-since-last", "120"]),
    (component_qc, ["volume", "--gross-g", "312", "--tare-g", "52", "--sg", "1.03"]),
    (component_qc, ["batch", QC_CSV, "--spec", "plt_e11:2.4::0.75", "--expect", "culture=neg", "--pass-rate", "0.9",
                    "--critical", "culture"]),
    (unit_return, ["--minutes-out", "20", "--max-minutes", "30", "--temp-c", "6", "--temp-range", "1:10"]),
])
def test_cli_prints_advisory(mod, args, capsys):
    assert mod.main(args) == 0
    assert "ADVISORY:" in capsys.readouterr().out


def test_must_fail_control_weight_45_exclusive(monkeypatch):
    """Inject the old OCR reading '>45 kg' (exclusive). The 45-kg boundary case must go red."""
    monkeypatch.setitem(CRITERIA, "weight_kg", {"min_exclusive": 45})
    with pytest.raises(AssertionError):
        test_weight_boundaries(45, "MEASURED CRITERIA MET", 350)
