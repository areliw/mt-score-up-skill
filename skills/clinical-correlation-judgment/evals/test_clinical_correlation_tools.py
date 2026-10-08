"""Oracle tests for clinical-correlation-judgment tools.

Expected outcomes come from OUTSIDE the code:
  - clinical-correlation-judgment card Fork 1 (MCV branch; iron pattern; ferritin normal -> do not stop at IDA),
    Fork 2 (exclusion only after ruling out), Fork 3 (confirm screens; KLF1), trap #1 anchoring (>= 3 DDx),
    and the DB/TB heuristic marked "not a fixed cut-off"
  - 510416 Clinical Correlation digest §2 (DB/TB bands; microcytic DDx list), Case 8 (DB/TB 0.58 with a
    hepatocellular final diagnosis), Case 5 (KLF1 mimics beta-thal trait)
  - 505402 Clinical Chemistry digest §5.3 (DB/TB bands); 510403 digest §3.8 (HbA2 >= 3.5% = beta-thal trait)
Inputs are constructed teaching values; only single published teaching-case numbers are reused.
Must-fail controls inject the traps the card warns about and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import copy
import json
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import ddx_check as dx  # noqa: E402
import pivot_check as pc  # noqa: E402


# ---------------------------------------------------------------- anemia branch (card Fork 1)
@pytest.mark.parametrize("mcv,branch", [(66, "microcytic"), (79.9, "microcytic"), (80, "normocytic"),
                                        (100, "normocytic"), (108, "macrocytic")])
def test_mcv_branch(mcv, branch):
    assert pc.anemia(mcv)["branch"] == branch


def test_classic_ida_pattern_points_to_blood_loss_source():
    # card Fork 1 / 510416 Case 1 pattern: ferritin L, TIBC H, %sat L -> IDA -> look for the bleeding source
    r = pc.anemia(48, ferritin="L", tibc="H", sat="L")
    assert any("IDA pattern" in s and "blood loss" in s for s in r["steps"])
    assert len(r["keep_open_ddx"]) >= 3                     # still not anchored


def test_normal_ferritin_does_not_stop_at_ida():
    # card Fork 1: ferritin normal in a microcytic patient -> reflex Hb typing / DNA
    r = pc.anemia(66, ferritin="N")
    assert any("do NOT stop at IDA" in s and "Hb typing" in s for s in r["steps"])
    assert "iron deficiency anemia" not in r["keep_open_ddx"]


def test_hba2_high_is_a_pattern_with_klf1_caveat():
    # 510403 §3.8: HbA2 >= 3.5% = beta-thal trait ; 510416 Case 5: KLF1 can mimic it
    r = pc.anemia(70, ferritin="N", hba2=5.2)
    assert any("beta-thal trait PATTERN" in s for s in r["steps"])
    assert any("KLF1" in c for c in r["caveats"])


def test_incomplete_iron_study_gives_no_label():
    r = pc.anemia(66, ferritin="L")                          # TIBC and %sat missing
    assert any("mixed/incomplete" in s for s in r["steps"])
    assert not any("IDA pattern" in s for s in r["steps"])


# ---------------------------------------------------------------- jaundice DB/TB (card + 3 digests)
def test_case8_ratio_shows_source_disagreement():
    # 510416 Case 8: DB/TB 0.58, final answer hepatocellular (DILI).
    # card heuristic: > 0.50 -> post-hepatic ; 505402: 0.30-0.60 -> mixed ; 510416: 0.5-0.6 is in BOTH intra and post
    r = pc.jaundice(ratio=0.58)
    assert r["sources_agree"] is False and "enzyme pattern" in r["verdict"]
    assert r["readings"]["card (heuristic)"]["category"] == "post"
    assert r["readings"]["505402 §5.3"]["category"] == "hepatic"
    assert r["readings"]["510416 §2"]["category"] == "unclear"


def test_clear_low_ratio_all_sources_agree():
    r = pc.jaundice(db=0.1, tb=1.0)                          # 0.10
    assert r["sources_agree"] is True and r["verdict"].endswith("pre")


def test_clear_high_ratio_all_sources_agree():
    assert pc.jaundice(ratio=0.85)["verdict"].endswith("post")


def test_direct_above_total_is_an_error():
    with pytest.raises(ValueError):
        pc.jaundice(db=3.0, tb=2.0)


def test_must_fail_control_single_fixed_cutoff(monkeypatch):
    """Inject the trap 'treat the DB/TB heuristic as a fixed cut-off' (one source only). Oracle must go red."""
    monkeypatch.setattr(pc, "BANDS", {"card (heuristic)": pc.BANDS["card (heuristic)"]})
    with pytest.raises(AssertionError):
        test_case8_ratio_shows_source_disagreement()


# ---------------------------------------------------------------- ddx_check (trap #1, Fork 2/3/5, scope)
with open(os.path.join(SKILL, "data", "worksheet_example.json"), encoding="utf-8") as _f:
    GOOD = json.load(_f)


def ws(**kw):
    d = copy.deepcopy(GOOD)
    d.update(kw)
    return d


def test_example_worksheet_is_done():
    assert dx.check(GOOD)["done"] is True


def test_single_ddx_is_anchoring():
    one = ws(ddx=[GOOD["ddx"][0]])
    r = dx.check(one)
    assert r["done"] is False and any("anchoring" in f["msg"] for f in r["findings"])


def test_each_ddx_needs_a_test():
    bad = ws()
    bad["ddx"][1]["discriminating_test"] = ""
    assert dx.check(bad)["done"] is False


def test_ruled_out_needs_evidence():
    bad = ws()
    bad["ddx"][2]["evidence"] = ""
    assert dx.check(bad)["done"] is False


def test_exclusion_claim_with_open_ddx_fails():
    r = dx.check(ws(conclusion="Diagnosis of exclusion: supplement toxicity."))
    assert r["done"] is False and any("Fork 2" in f["msg"] for f in r["findings"])


def test_unconfirmed_screen_fails():
    assert dx.check(ws(screens=[{"screen": "NS1 positive", "confirm": ""}]))["done"] is False


def test_missing_iron_rule_fails():
    assert dx.check(ws(preanalytical=""))["done"] is False


def test_diagnostic_wording_is_a_warning_not_a_fail():
    r = dx.check(ws(conclusion="Patient is diagnosed with beta-thalassemia trait."))
    assert r["done"] is True and any(f["level"] == "WARN" and "diagnosis" in f["msg"] for f in r["findings"])


def test_must_fail_control_anchoring_allowed(monkeypatch):
    """Inject trap #1: one DDx is enough. The oracle must go red."""
    monkeypatch.setattr(dx, "MIN_DDX", 1)
    with pytest.raises(AssertionError):
        test_single_ddx_is_anchoring()


# ================================================================ R ratio (added 2026-10-08)
# Convention: ACG 2014 DILI guideline / LiverTox RUCAM manual (NBK548272): R = (ALT/ULN)/(ALP/ULN);
# >= 5 hepatocellular, <= 2 cholestatic, between = mixed; shortcuts ALT>2xULN & ALP normal ->
# hepatocellular, ALP>2xULN & ALT normal -> cholestatic. ULNs below (ALT 40, ALP 120 U/L) are
# TEACHING values, not from a source - the tool always takes the lab's own limits.
import pivot_check as pc  # noqa: E402


def test_case8_dili_is_hepatocellular_by_enzymes():
    # 510416 Case 8: ALT 1220, AST 577, ALP 111 (normal), DB/TB 0.58 -> hepatocellular DILI.
    r = pc.liver_pattern(1220, 40, 111, 120)
    assert r["pattern"] == "hepatocellular" and r["r"] is None      # shortcut: ALT 30.5x, ALP normal
    # the card's DB/TB band alone would have said post-hepatic -> the jaundice read points to `liver`
    assert pc.jaundice(ratio=0.58)["readings"]["card (heuristic)"]["category"] == "post"
    assert "liver" in pc.jaundice(ratio=0.58)["next"]


def test_r_ratio_bands_by_hand():
    # ALT 200/40 = 5.0x, ALP 180/120 = 1.5x -> R = 3.33 -> mixed
    assert pc.liver_pattern(200, 40, 180, 120)["pattern"] == "mixed"
    # ALT 400/40 = 10x, ALP 240/120 = 2x -> R = 5.0 exactly -> hepatocellular, flagged as boundary
    r = pc.liver_pattern(400, 40, 240, 120)
    assert r["pattern"] == "hepatocellular" and r["boundary"] is True
    # ALT 90/40 = 2.25x, ALP 360/120 = 3x -> R = 0.75 -> cholestatic
    assert pc.liver_pattern(90, 40, 360, 120)["pattern"] == "cholestatic"
    # shortcut the other way: ALP 400/120 = 3.3x, ALT 30/40 normal -> cholestatic
    assert pc.liver_pattern(30, 40, 400, 120)["pattern"] == "cholestatic"


def test_liver_pattern_rejects_missing_uln():
    with pytest.raises(ValueError):
        pc.liver_pattern(100, 0, 120, 120)


def test_must_fail_control_ratio_without_uln(monkeypatch):
    """Inject the trap: raw ALT/ALP without dividing by each ULN. The hand-worked bands must go red."""
    def raw_ratio(alt, alt_uln, alp, alp_uln):
        r = alt / alp
        return {"alt_x_uln": alt, "alp_x_uln": alp, "r": r, "boundary": False,
                "pattern": "hepatocellular" if r >= 5 else ("cholestatic" if r <= 2 else "mixed")}
    monkeypatch.setattr(pc, "liver_pattern", raw_ratio)
    with pytest.raises(AssertionError):
        test_r_ratio_bands_by_hand()
