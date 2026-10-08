"""Oracle tests for flow-cytometry-judgment tools (gating_check, flow_calc).

Expected values are hand arithmetic on synthetic teaching hierarchies/counts (written in the comments),
using rules from the card and the owner's digests:
  card flow-cytometry-judgment: rule #1 / trap #1 (gate viability + singlet + scatter before reading a marker),
      Fork 1 order (time -> scatter -> singlet -> viable/dump -> CD45/SSC -> marker), Fork 4 (CD4, MRD events).
  501 Hematology Lecture digest §2: absolute count = %diff x WBC / 100.
  Immunodiagnostic digest §5.5: dual- vs single-platform (bead) CD4 counting; CD4 < 200 = AIDS-defining.
Must-fail controls inject the card's traps (dirty denominator, unchecked hierarchy, CD4 from WBC without
the lymphocyte %, MRD sensitivity that ignores the cluster size); the oracle must go red.

Run from the repo root:  python -m pytest skills/flow-cytometry-judgment/evals -q
"""
import json
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import flow_calc  # noqa: E402
import gating_check  # noqa: E402

CLEAN = os.path.join(SKILL, "data", "gating_example.csv")
DIRTY = os.path.join(SKILL, "data", "gating_no_singlet_viable.csv")


def rows_by_gate(res):
    return {r["gate"]: r for r in res["rows"]}


# ---------------------------------------------------------------- gating_check (card Fork 1, trap #1)
def test_clean_hierarchy_percentages():
    # data/gating_example.csv: Live 63,000 / Singlets 70,000 = 90 % ; Lymph 18,000 / 63,000 = 28.571 %
    # CD3+ 13,500 / 18,000 = 75 % ; CD4+ 6,750 / 13,500 = 50 % ; CD8+ 5,400 / 13,500 = 40 % ; CD4 of total 6.75 %
    res = gating_check.evaluate(gating_check.load(CLEAN))
    r = rows_by_gate(res)
    assert r["Live"]["pct_parent"] == pytest.approx(90.0)
    assert r["Lymph CD45br"]["pct_parent"] == pytest.approx(1800 / 63)
    assert r["CD3+"]["pct_parent"] == pytest.approx(75.0)
    assert r["CD4+"]["pct_parent"] == pytest.approx(50.0)
    assert r["CD8+"]["pct_parent"] == pytest.approx(40.0)
    assert r["CD4+"]["pct_total"] == pytest.approx(6.75)
    assert res["overall"] == "PASS"


def test_dirty_hierarchy_fails_on_missing_singlet_and_viable():
    # data/gating_no_singlet_viable.csv: markers gated straight from an FSC/SSC lymph gate
    res = gating_check.evaluate(gating_check.load(DIRTY))
    c = res["checks"]["CD4+"]
    assert c["status"] == "FAIL" and res["overall"] == "FAIL"
    joined = " ".join(c["missing"])
    assert "singlet" in joined and "viability" in joined
    assert not any("scatter" in m for m in c["missing"])  # it has a scatter gate
    assert c["warn"]  # and no time gate -> warning


def test_order_note_when_singlet_below_viable_and_cd45():
    rows = [
        {"gate": "All", "parent": "", "events": "1000", "kind": "all"},
        {"gate": "Time", "parent": "All", "events": "990", "kind": "time"},
        {"gate": "Cells", "parent": "Time", "events": "900", "kind": "scatter"},
        {"gate": "Live", "parent": "Cells", "events": "800", "kind": "viable"},
        {"gate": "CD45", "parent": "Live", "events": "700", "kind": "cd45"},
        {"gate": "Single", "parent": "CD45", "events": "650", "kind": "singlet"},
        {"gate": "CD19+", "parent": "Single", "events": "100", "kind": "marker"},
    ]
    c = gating_check.evaluate(gating_check.parse(rows))["checks"]["CD19+"]
    assert c["status"] == "WARN" and c["order_notes"] and not c["missing"]


@pytest.mark.parametrize("bad", [
    [{"gate": "All", "parent": "", "events": "100", "kind": "all"},
     {"gate": "X", "parent": "All", "events": "150", "kind": "marker"}],          # child > parent
    [{"gate": "All", "parent": "", "events": "100", "kind": "all"},
     {"gate": "X", "parent": "Nope", "events": "10", "kind": "marker"}],          # unknown parent
    [{"gate": "All", "parent": "", "events": "100", "kind": "all"},
     {"gate": "X", "parent": "All", "events": "10", "kind": "gate"}],             # bad kind
])
def test_sanity_errors(bad):
    with pytest.raises(gating_check.GatingError):
        gating_check.parse(bad)


def test_must_fail_control_denominator_is_all_events(monkeypatch):
    """Inject trap #1: % computed against all acquired events (debris + doublets + dead in the denominator)."""
    monkeypatch.setattr(gating_check, "pct_of_parent",
                        lambda nodes, g: nodes[g]["events"] / nodes[gating_check.root_of(nodes)]["events"] * 100)
    with pytest.raises(AssertionError):
        test_clean_hierarchy_percentages()


def test_must_fail_control_hierarchy_not_checked(monkeypatch):
    """Inject the trap of trusting the hierarchy: no upstream requirement is enforced."""
    monkeypatch.setattr(gating_check, "REQUIRED_UPSTREAM", {})
    with pytest.raises(AssertionError):
        test_dirty_hierarchy_fails_on_missing_singlet_and_viable()


# ---------------------------------------------------------------- absolute counts (501 §2; immunodiag §5.5)
def test_cd4_dual_platform():
    # WBC 6,000/uL x lymph 30 % = 1,800 lymphocytes/uL ; CD4 25 % of lymphocytes -> 1,800 x 0.25 = 450/uL
    r = flow_calc.abs_dual(6000, 30, 25, threshold=200)
    assert r["abs_lymphocytes_per_ul"] == pytest.approx(1800)
    assert r["abs_subset_per_ul"] == pytest.approx(450)
    assert r["below_threshold"] is False
    # WBC 3,000 x 20 % = 600 ; x 15 % = 90/uL -> below 200
    assert flow_calc.abs_dual(3000, 20, 15, threshold=200)["below_threshold"] is True


def test_cd4_bead_single_platform():
    # (5,000 / 10,000) x (50,000 beads / 50 uL) = 0.5 x 1,000 = 500 cells/uL
    assert flow_calc.abs_bead(5000, 10000, 50000, 50)["abs_per_ul"] == pytest.approx(500)
    # (1,500 / 10,000) x 1,000 = 150/uL -> below 200
    assert flow_calc.abs_bead(1500, 10000, 50000, 50, threshold=200)["below_threshold"] is True


def test_must_fail_control_cd4_without_lymph_pct(monkeypatch):
    """Inject the trap: absolute CD4 = WBC x CD4% (forgets that CD4% is a % of LYMPHOCYTES): 6,000 x 0.25 = 1,500."""
    monkeypatch.setattr(flow_calc, "abs_dual",
                        lambda wbc, lymph, sub, threshold=None: {
                            "abs_lymphocytes_per_ul": wbc * lymph / 100,
                            "abs_subset_per_ul": wbc * sub / 100,
                            "below_threshold": threshold is not None and wbc * sub / 100 < threshold})
    with pytest.raises(AssertionError):
        test_cd4_dual_platform()


# ---------------------------------------------------------------- MRD events (card Fork 4)
def test_mrd_lod_and_claim():
    # 100,000 evaluable events, minimum cluster 20 -> LOD = 20/100,000 = 2e-4 (0.02 %) = 1 in 5,000
    # claim 1e-4 (0.01 %) -> 2e-4 > 1e-4 -> NOT supported ; events needed = 20 / 1e-4 = 200,000
    r = flow_calc.mrd_lod(100000, 20, claim=1e-4)
    assert r["lod_fraction"] == pytest.approx(2e-4)
    assert r["lod_one_in"] == pytest.approx(5000)
    assert r["claim_supported"] is False
    assert r["events_needed_for_claim"] == 200000
    # 500,000 events -> LOD 4e-5 <= 1e-4 -> supported
    assert flow_calc.mrd_lod(500000, 20, claim=1e-4)["claim_supported"] is True
    # exactly 200,000 events -> LOD = 1e-4 -> supported (boundary)
    assert flow_calc.mrd_lod(200000, 20, claim=1e-4)["claim_supported"] is True


def test_mrd_min_cluster_has_no_default():
    with pytest.raises(SystemExit):
        flow_calc.main(["mrd-lod", "--events", "100000"])


def test_must_fail_control_mrd_one_event_lod(monkeypatch):
    """Inject the trap: sensitivity = 1/events (a 'clone' of one event) -> claims 1e-5, says supported."""
    def naive(events, min_cluster, claim=None):
        lod = 1 / events
        return {"lod_fraction": lod, "lod_one_in": events, "claim_supported": claim is not None and lod <= claim,
                "events_needed_for_claim": int(1 / claim) if claim else None}

    monkeypatch.setattr(flow_calc, "mrd_lod", naive)
    with pytest.raises(AssertionError):
        test_mrd_lod_and_claim()


# ---------------------------------------------------------------- CLI contract
def test_gating_cli(capsys):
    assert gating_check.main([DIRTY]) == 0
    out = capsys.readouterr().out
    assert "OVERALL FAIL" in out and "ADVISORY" in out
    assert gating_check.main([CLEAN, "--target", "CD4+", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["overall"] == "PASS" and list(data["checks"]) == ["CD4+"]


def test_flow_calc_cli(capsys):
    assert flow_calc.main(["mrd-lod", "--events", "100000", "--min-cluster", "20", "--claim", "1e-4"]) == 0
    out = capsys.readouterr().out
    assert "NOT SUPPORTED" in out and "ADVISORY" in out
    assert flow_calc.main(["--json", "abs-bead", "--cell-events", "5000", "--bead-events", "10000",
                           "--beads-per-tube", "50000", "--volume-ul", "50"]) == 0
    assert json.loads(capsys.readouterr().out)["abs_per_ul"] == pytest.approx(500)
