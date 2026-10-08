"""Oracle tests for parasitology-judgment tools (parasite_calc.py, negative_ruleout.py).

Expected values come from the owner's digest / the card + hand arithmetic, NOT from the code:
  317331 = 06_Background_MedTech/317331-PARASITOLOGY-FOR-MED-TECH-64-65/317331-DIGEST-2026-05-31.md
           Part 2 Lab Dx (parasites/200 WBC x 8,000; >40,000/uL count WBC per 500 parasites;
           negative set -> repeat 12-24 h) · §5.1 (stool routine 1, confirm 3 alternate days,
           E. histolytica 6) · §5.2 (Kato EPG) · §5.3 micrometry (stage micrometer 0.01 mm/div;
           example 10x -> 9.9 um/div, 40x -> 2.56 um/div; measure at THAT objective) ·
           EXAM-LIKELY #8 (Cryptosporidium 4-6 um vs Cyclospora 8-10 um)
  card   = skills/parasitology-judgment.md rule #1, FORK 1, FORK 3, traps
Must-fail controls inject the traps the card warns about and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import datetime as dt
import json
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import negative_ruleout as nr  # noqa: E402
import parasite_calc as pc  # noqa: E402


def rules():
    with open(os.path.join(SKILL, "data", "ruleout_rules_teaching.json"), encoding="utf-8") as f:
        return json.load(f)


def candidates():
    with open(os.path.join(SKILL, "data", "oocyst_sizes_teaching.json"), encoding="utf-8") as f:
        return json.load(f)["candidates"]


# ================================================================ parasite_calc
def test_density_digest_formula():
    # 317331 Lab Dx: parasites/200 WBC x 8,000. 50 parasites / 200 x 8,000 = 2,000 /uL
    assert pc.density(50, 200, 8000)["density_per_ul"] == pytest.approx(2000)
    # patient WBC 5,000 instead of the assumed 8,000: 50 / 200 x 5,000 = 1,250 /uL
    assert pc.density(50, 200, 5000)["density_per_ul"] == pytest.approx(1250)


def test_density_high_count_switch_flag():
    # 1,200 / 200 x 8,000 = 48,000 > 40,000 -> digest: count WBC per 500 parasites instead
    res = pc.density(1200, 200, 8000, switch_above=40000)
    assert res["density_per_ul"] == pytest.approx(48000) and res["flags"]
    # counted the other way: 500 parasites against 83 WBC -> 500 x 8,000 / 83 = 48,192.8
    assert pc.density(500, 83, 8000)["density_per_ul"] == pytest.approx(500 * 8000 / 83)


def test_epg_kato():
    # EPG = eggs x 1000 / mg. 10 eggs on a 41.7 mg template -> 10 x 23.98 = 239.8 EPG
    assert pc.epg(10, 41.7)["epg"] == pytest.approx(10 * 1000 / 41.7)
    # two smears, 18 eggs total -> 18 x 1000 / (41.7 x 2) = 215.8
    assert pc.epg(18, 41.7, smears=2)["epg"] == pytest.approx(18 * 1000 / 83.4)


def test_calibration_317331_example():
    # 317331 §5.3: stage micrometer 10 um/div; 10 stage div = 39 ocular div -> 100/39 = 2.564 um/div (~2.56 at 40x)
    assert pc.calibrate(10, 39) == pytest.approx(100 / 39)
    # 99 stage div = 100 ocular div -> 9.9 um/div (the digest's 10x example)
    assert pc.calibrate(99, 100) == pytest.approx(9.9)


def test_measure_uses_the_objective_factor():
    cal = {"10x": 9.9, "40x": 2.56}
    # 2 ocular div at 40x = 5.12 um -> inside Cryptosporidium 4-6 um, not Cyclospora 8-10 um
    r = pc.measure(2, "40x", cal, candidates())
    assert r["size_um"] == pytest.approx(5.12)
    assert r["fits"] == ["Cryptosporidium oocyst"]
    # 3.5 div at 40x = 8.96 um -> Cyclospora
    assert pc.measure(3.5, "40x", cal, candidates())["fits"] == ["Cyclospora oocyst"]


def test_measure_refuses_uncalibrated_objective():
    with pytest.raises(KeyError):
        pc.measure(2, "100x", {"40x": 2.56})


def test_must_fail_control_reuse_10x_factor_at_40x(monkeypatch):
    """Inject the trap: one calibration factor for every objective (10x factor used at 40x -> 19.8 um)."""
    monkeypatch.setattr(pc, "um_per_div", lambda cal, objective: cal["10x"])
    with pytest.raises(AssertionError):
        test_measure_uses_the_objective_factor()


# ================================================================ negative_ruleout
T = dt.datetime.fromisoformat


def films(*specs):
    return [{"time": T(t), "fields": f} for t, f in specs]


def test_malaria_three_films_12_to_24h_apart_meets_rule():
    # card rule #1 + FORK 3: >= 3 films, 12-24 h apart, >= 100 thick fields each
    res = nr.malaria(films(("2026-10-01T08:00", 100), ("2026-10-01T20:30", 100), ("2026-10-02T09:00", 120)),
                     rules()["malaria"])
    assert res["counted"] == 3 and res["ruled_out_by_rule"] is True


def test_malaria_three_films_same_morning_is_one_repeat():
    # 3 films within 2 h = one time point -> not ruled out; next due 12 h after the counted film
    res = nr.malaria(films(("2026-10-01T08:00", 100), ("2026-10-01T09:00", 100), ("2026-10-01T10:00", 100)),
                     rules()["malaria"])
    assert res["counted"] == 1 and res["ruled_out_by_rule"] is False
    assert res["next_due"] == "2026-10-01 20:00:00"


def test_malaria_film_with_too_few_fields_does_not_count():
    # card FORK 3: negative only after >= 100 thick fields; an 80-field film is not a valid negative
    res = nr.malaria(films(("2026-10-01T08:00", 100), ("2026-10-01T20:30", 80), ("2026-10-02T09:00", 120)),
                     rules()["malaria"])
    assert res["counted"] == 2 and res["ruled_out_by_rule"] is False


def test_must_fail_control_count_films_without_spacing(monkeypatch):
    """Inject card rule #1 trap: three films drawn together counted as three repeats."""
    monkeypatch.setattr(nr, "chain", lambda items, key, min_gap: (sorted(items, key=key), []))
    with pytest.raises(AssertionError):
        test_malaria_three_films_same_morning_is_one_repeat()


def test_must_fail_control_ignore_field_count(monkeypatch):
    """Inject card trap: report negative after a short read (fields not checked)."""
    r = rules()
    r["malaria"]["min_thick_fields"] = 0
    monkeypatch.setattr(nr, "malaria", lambda fl, rule, _real=nr.malaria: _real(fl, r["malaria"]))
    with pytest.raises(AssertionError):
        test_malaria_film_with_too_few_fields_does_not_count()


D = dt.date.fromisoformat


def test_stool_ruleout_three_alternate_days():
    # 317331 §5.1: confirm = 3 specimens, alternate days. 1, 3, 5 Oct -> meets; 1, 2, 3 Oct -> only 1 and 3 count
    r = rules()["stool_ruleout"]
    assert nr.stool([D("2026-10-01"), D("2026-10-03"), D("2026-10-05")], r)["ruled_out_by_rule"] is True
    res = nr.stool([D("2026-10-01"), D("2026-10-02"), D("2026-10-03")], r)
    assert res["counted"] == 2 and res["ruled_out_by_rule"] is False and res["next_due"] == "2026-10-05"


def test_single_routine_stool_is_not_a_ruleout():
    # card trap: single stool = false negative. Routine (n=1) passes its own rule, rule-out (n=3) does not.
    one = [D("2026-10-01")]
    assert nr.stool(one, rules()["stool_routine"])["ruled_out_by_rule"] is True
    assert nr.stool(one, rules()["stool_ruleout"])["ruled_out_by_rule"] is False


def test_e_histolytica_needs_six_and_no_spacing_claim():
    # 317331 §5.1: E. histolytica = 6; source gives no spacing -> the tool must say spacing is unchecked
    res = nr.stool([D("2026-10-0%d" % i) for i in range(1, 6)], rules()["e_histolytica"])
    assert res["counted"] == 5 and res["ruled_out_by_rule"] is False
    assert any("spacing NOT checked" in f for f in res["flags"])


def test_cli_smoke(capsys):
    assert nr.main(["malaria", "--rules", os.path.join(SKILL, "data", "ruleout_rules_teaching.json"),
                    "--film", "2026-10-01T08:00:100"]) == 0
    assert "NOT RULED OUT" in capsys.readouterr().out
    assert pc.main(["density", "--parasites", "50", "--wbc-counted", "200", "--wbc-per-ul", "8000"]) == 0
    assert "ADVISORY" in capsys.readouterr().out
