from __future__ import annotations

import json
from pathlib import Path

from conftest import run_maturity_gate_on_fixture, run_script


def test_maturity_gate_all_skills_pass(repo_root: Path) -> None:
    proc = run_script(repo_root, "check_maturity_gate.py", "--all")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "within their evidence" in proc.stdout


def test_manual_ab_six_skills_tiered_and_full_restored(repo_root: Path) -> None:
    rows = json.loads((repo_root / "eval" / "_ab_slim.json").read_text(encoding="utf-8"))
    by_skill: dict[str, list[dict]] = {}
    for r in rows:
        slug = r["skill"].removesuffix(".md")
        by_skill.setdefault(slug, []).append(r)
    manual = [
        "preanalytical-judgment",
        "urinalysis-judgment",
        "poct-judgment",
        "flow-cytometry-judgment",
        "incident-postmortem-judgment",
        "market-research-judgment",
    ]
    for slug in manual:
        assert slug in by_skill, slug
        tiers = {r.get("tier") or ("manual" if "manual" in str(r.get("method", "")) else "full") for r in by_skill[slug]}
        assert "manual" in tiers, slug
        assert "full" in tiers, slug
        manual_rows = [r for r in by_skill[slug] if r.get("tier") == "manual"]
        assert manual_rows[0].get("method") == "manual-screen"
        assert manual_rows[0].get("run") == "manual-2026-06-24"
        full_rows = [r for r in by_skill[slug] if r.get("tier") == "full"]
        assert full_rows[0].get("run") == "round6-probe"
        assert full_rows[0].get("method") == "x3"
    proc = run_script(repo_root, "ab_gate_check.py", *[f"skills/{s}.md" for s in manual])
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARNING" not in proc.stdout


def test_ab_tier_promotion_prefers_full_over_manual(repo_root: Path) -> None:
    proc = run_script(repo_root, "build_ab_coverage.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    reg = json.loads((repo_root / "eval" / "ab-coverage.json").read_text(encoding="utf-8"))
    assert reg["flow-cytometry-judgment"]["ab_full"] is True
    assert reg["flow-cytometry-judgment"]["ab_tier"] == "full"
    assert reg["flow-cytometry-judgment"]["ab_delta"] == 3.67
    assert reg["poct-judgment"]["ab_delta"] == -0.67


def test_maturity_gate_semi_stable_without_ab_fails(repo_root: Path) -> None:
    proc = run_maturity_gate_on_fixture(repo_root, "semi_stable_no_ab.md")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "semi-stable but no full-tier A/B" in proc.stdout


def test_maturity_gate_draft_fixture_passes(repo_root: Path) -> None:
    proc = run_maturity_gate_on_fixture(repo_root, "minimal_valid_skill.md")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "within their evidence" in proc.stdout
