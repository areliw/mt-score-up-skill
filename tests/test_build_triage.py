from __future__ import annotations

import re
from pathlib import Path

from conftest import run_script

CATALOG_START = "<!-- CATALOG:START -->"
CATALOG_END = "<!-- CATALOG:END -->"


def _skill_slugs(skills_dir: Path) -> set[str]:
    skip = {"README.md", "INDEX.md"}
    return {p.stem for p in skills_dir.glob("*.md") if p.name not in skip}


def test_build_triage_regenerates_catalog_in_sync(repo_root: Path) -> None:
    proc = run_script(repo_root, "build_triage.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "triage updated" in proc.stdout or "triage in-sync" in proc.stdout

    triage = (repo_root / "prompts" / "triage.md").read_text(encoding="utf-8")
    assert CATALOG_START in triage and CATALOG_END in triage
    block = triage.split(CATALOG_START, 1)[1].split(CATALOG_END, 1)[0]
    slugs = _skill_slugs(repo_root / "skills")
    assert len(slugs) == 94
    for slug in slugs:
        assert f"`{slug}`" in block, f"missing catalog entry for {slug}"
