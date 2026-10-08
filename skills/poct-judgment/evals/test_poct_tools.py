"""Oracle tests for poct-judgment tools.

The owner has no dedicated POCT digest, so gate outcomes are oracled against the card's own rule
text (rule #1 / trap #1 QC + competency, Fork 3 interference directions, traps 3/4/5/8), and the
matrix note against 504202-CLINCHEM-LECTURE-DIGEST-2026-06-01.md section 1 (plasma > whole blood
~12-15 %). Comparison statistics are hand arithmetic written in the comments.
Must-fail controls inject the traps the card warns about and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import datetime as dt
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import poct_compare  # noqa: E402
import poct_gate  # noqa: E402

GOOD = {"analyte": "glucose", "qc": "pass", "operator_competent": True, "lot_verified": True,
        "range": (20, 600), "today": dt.date(2026, 10, 8)}


def gate(**kw):
    s = dict(GOOD)
    s.update(kw)
    return poct_gate.evaluate(s)


def has(res, level, text):
    return any(f["level"] == level and text in (f["finding"] + " " + f["action"]) for f in res["findings"])


# ---------------------------------------------------------------- rule #1 / trap #1: QC + competency
def test_clean_result_is_usable():
    assert gate(value=120)["status"] == "USABLE (gates passed)"


def test_qc_fail_blocks():
    # Card rule #1 + trap #1: a POCT result without passed QC is not usable
    r = gate(value=120, qc="fail")
    assert r["status"].startswith("BLOCKED") and has(r, "BLOCK", "QC fail")


def test_operator_and_lot_gates():
    assert gate(value=120, operator_competent=False)["status"].startswith("BLOCKED")
    assert gate(value=120, lot_verified=False)["status"].startswith("BLOCKED")          # trap 8
    # last assessment 2025-01-01 + 365 days = due 2026-01-01 < today 2026-10-08 -> expired
    r = gate(value=120, competency_date=dt.date(2025, 1, 1), competency_interval_days=365)
    assert has(r, "BLOCK", "competency expired on 2026-01-01")
    # 2026-03-01 + 365 = 2027-03-01 > today -> still valid
    assert gate(value=120, competency_date=dt.date(2026, 3, 1), competency_interval_days=365)["status"].startswith("USABLE")


def test_must_fail_control_qc_ignored(monkeypatch):
    """Trap #1: treating POCT as 'no QC needed' - a gate that never looks at QC."""
    real = poct_gate.evaluate

    def no_qc(s):
        s = dict(s)
        s["qc"] = "pass"
        return real(s)

    monkeypatch.setattr(poct_gate, "evaluate", no_qc)
    with pytest.raises(AssertionError):
        test_qc_fail_blocks()


# ---------------------------------------------------------------- Fork 3 interference (glucose)
def test_hct_direction():
    # Card Fork 3: high Hct -> glucose falsely LOW; low Hct (neonate/anaemia/dialysis) -> falsely HIGH
    assert poct_gate.hct_bias(65, (20, 60)) == "falsely LOW"
    assert poct_gate.hct_bias(15, (20, 60)) == "falsely HIGH"
    assert poct_gate.hct_bias(40, (20, 60)) is None
    assert has(gate(value=120, hct=65, hct_range=(20, 60)), "BLOCK", "falsely LOW")


def test_must_fail_control_hct_direction_swapped(monkeypatch):
    """Trap #2: getting the Hct direction backwards."""
    monkeypatch.setattr(poct_gate, "hct_bias",
                        lambda hct, rng: "falsely HIGH" if hct > rng[1] else ("falsely LOW" if hct < rng[0] else None))
    with pytest.raises(AssertionError):
        test_hct_direction()


def test_gdh_pqq_maltose_icodextrin_blocks():
    # Card Fork 3: GDH-PQQ + maltose / icodextrin (PD fluid) / galactose -> falsely high
    r = gate(value=180, method="gdh-pqq", interferents=["icodextrin"])
    assert has(r, "BLOCK", "falsely HIGH")
    assert not has(gate(value=180, method="gdh-fad", interferents=["icodextrin"]), "BLOCK", "GDH-PQQ")


def test_gox_oxygen_and_amperometric_confirm():
    # Card Fork 3: O2 interferes only with glucose oxidase (arterial / high O2 -> falsely low)
    assert has(gate(value=90, method="gox", sample="arterial"), "CONFIRM", "falsely LOW")
    assert not has(gate(value=90, method="gdh-fad", sample="arterial"), "CONFIRM", "O2")
    assert gate(value=90, interferents=["acetaminophen"])["status"].startswith("CONFIRM")


def test_capillary_in_shock_blocked():
    # Card Fork 3: capillary glucose unreliable in shock / hypotension / oedema / vasopressor
    assert has(gate(value=90, perfusion="shock"), "BLOCK", "capillary")
    assert not has(gate(value=90, perfusion="shock", sample="venous"), "BLOCK", "capillary")


# ---------------------------------------------------------------- traps 3 / 4 / 5
def test_out_of_range_critical_and_manual_entry():
    assert has(gate(value=650), "BLOCK", "outside measuring range")                       # trap 3
    r = gate(value=35, critical=(40, 400))                                                # trap 5
    assert r["status"].startswith("USABLE + CRITICAL") and has(r, "NOTIFY", "critical value 35")
    assert has(gate(value=120, connectivity="manual"), "CAUTION", "not traceable")       # trap 4


# ---------------------------------------------------------------- POCT vs central lab (Fork 3, trap 7)
PAIRS = [{"date": "d1", "poct": 110, "lab": 100}, {"date": "d2", "poct": 190, "lab": 200},
         {"date": "d3", "poct": 165, "lab": 150}]


def test_compare_bias_and_agreement():
    # diffs +10, -10, +15 -> mean diff 15/3 = 5 ; pct +10, -5, +10 -> mean 15/3 = 5 %
    r = poct_compare.compare(PAIRS, limit_pct=12)
    assert r["mean_diff"] == pytest.approx(5)
    assert r["mean_pct"] == pytest.approx(5)
    assert r["n_within"] == 3                                   # all |pct| <= 12
    assert poct_compare.compare(PAIRS, limit_pct=8)["n_within"] == 1   # only -5 %


def test_compare_abs_limit_below_switch():
    # lab 80 < switch 100 -> judged by |diff| 10 <= 15 (pct 12.5 % would fail a 10 % limit)
    r = poct_compare.compare([{"date": "a", "poct": 90, "lab": 80}, {"date": "b", "poct": 220, "lab": 200}],
                             limit_pct=10, limit_abs=15, switch_at=100)
    assert [row["within"] for row in r["rows"]] == [True, True]          # 220 vs 200 = 10 % <= 10


def test_compare_drift():
    # early half pct 0, 0 -> mean 0 ; late half +10, +12 -> mean 11 ; change 11 points > 5 -> flag
    pairs = [{"date": str(i), "poct": p, "lab": 100} for i, p in enumerate([100, 100, 110, 112])]
    d = poct_compare.compare(pairs, limit_pct=15, drift_pct=5)["drift"]
    assert d["change_pct_points"] == pytest.approx(11) and d["flag"] is True


def test_example_csv_loads_and_shows_drift():
    # teaching file: early half mean pct (-2.0 + 1.333 + 2.5 - 1.25) / 4 = 0.146 ;
    # late half (6.667 + 8.387 + 7.619 + 8.889) / 4 = 7.890 ; change 7.74 points
    pairs = poct_compare.load(os.path.join(SKILL, "data", "poct_pairs_teaching_example.csv"))
    d = poct_compare.compare(pairs, limit_pct=15)["drift"]
    assert d["early_mean_pct"] == pytest.approx(0.146, abs=1e-3)
    assert d["change_pct_points"] == pytest.approx(7.744, abs=1e-3)


@pytest.mark.parametrize("mod,argv", [
    (poct_gate, ["--value", "120", "--qc", "fail", "--operator-competent", "--lot-verified"]),
    (poct_compare, [os.path.join(SKILL, "data", "poct_pairs_teaching_example.csv"), "--limit-pct", "15",
                    "--meter-cal", "whole-blood"]),
])
def test_cli_prints_advisory(mod, argv, capsys):
    assert mod.main(argv) == 0
    assert "ADVISORY" in capsys.readouterr().out
