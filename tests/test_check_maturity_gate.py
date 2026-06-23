from __future__ import annotations

import json
from pathlib import Path

from conftest import run_script


def test_maturity_gate_all_skills_pass(repo_root: Path) -> None:
    proc = run_script(repo_root, "check_maturity_gate.py", "--all")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "within their evidence" in proc.stdout


def test_manual_ab_six_skills_have_fresh_records(repo_root: Path) -> None:
    rows = json.loads((repo_root / "eval" / "_ab_slim.json").read_text(encoding="utf-8"))
    by_skill = {r["skill"].removesuffix(".md"): r for r in rows}
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
        assert by_skill[slug].get("method") == "manual-x3"
        assert by_skill[slug].get("run") == "manual-2026-06-24"
        assert by_skill[slug].get("delta", 0) > 0
    proc = run_script(repo_root, "ab_gate_check.py", *[f"skills/{s}.md" for s in manual])
    assert proc.returncode == 0, proc.stdout + proc.stderr
