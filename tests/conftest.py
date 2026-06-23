from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterable
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return ROOT


def run_script(repo_root: Path, script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(repo_root / "scripts" / script), *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def run_validate_in_temp_repo(
    repo_root: Path,
    skill_fixtures: Iterable[str],
) -> subprocess.CompletedProcess[str]:
    """Copy validate_repo.py + fixture skills into a temp mini-repo and run it."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        scripts_dir = tmp_root / "scripts"
        skills_dir = tmp_root / "skills"
        scripts_dir.mkdir()
        skills_dir.mkdir()
        shutil.copy(repo_root / "scripts" / "validate_repo.py", scripts_dir / "validate_repo.py")
        for fixture_name in skill_fixtures:
            shutil.copy(FIXTURES / fixture_name, skills_dir / fixture_name)
        return subprocess.run(
            [sys.executable, str(scripts_dir / "validate_repo.py")],
            cwd=tmp_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )


def run_maturity_gate_on_fixture(
    repo_root: Path,
    fixture_name: str,
) -> subprocess.CompletedProcess[str]:
    """Run check_maturity_gate.py against a single fixture skill in a temp skills/ dir."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        scripts_dir = tmp_root / "scripts"
        skills_dir = tmp_root / "skills"
        eval_dir = tmp_root / "eval"
        scripts_dir.mkdir()
        skills_dir.mkdir()
        eval_dir.mkdir()
        shutil.copy(repo_root / "scripts" / "check_maturity_gate.py", scripts_dir / "check_maturity_gate.py")
        shutil.copy(repo_root / "scripts" / "ab_tier.py", scripts_dir / "ab_tier.py")
        shutil.copy(FIXTURES / fixture_name, skills_dir / fixture_name)
        (eval_dir / "_ab_slim.json").write_text("[]", encoding="utf-8")
        (eval_dir / "ab-coverage.json").write_text("{}", encoding="utf-8")
        skill_path = skills_dir / fixture_name
        return subprocess.run(
            [sys.executable, str(scripts_dir / "check_maturity_gate.py"), str(skill_path)],
            cwd=tmp_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
