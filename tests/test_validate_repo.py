from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from conftest import run_validate_in_temp_repo, run_script


def test_validate_repo_passes_on_current_library(repo_root: Path) -> None:
    proc = run_script(repo_root, "validate_repo.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "96 skill files scanned" in proc.stdout


def test_validate_repo_accepts_minimal_valid_fixture(repo_root: Path) -> None:
    proc = run_validate_in_temp_repo(repo_root, ["minimal_valid_skill.md"])
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1 skill files scanned" in proc.stdout


def test_validate_repo_rejects_missing_trap_section(repo_root: Path) -> None:
    proc = run_validate_in_temp_repo(repo_root, ["bad_skill_missing_section.md"])
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "missing canonical section 'กับดัก'" in proc.stdout


def test_validate_repo_rejects_invalid_type(repo_root: Path) -> None:
    base = (Path(__file__).parent / "fixtures" / "minimal_valid_skill.md").read_text(encoding="utf-8")
    bad = base.replace("type: ADVISE", "type: INVALID")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        scripts_dir = tmp_root / "scripts"
        skills_dir = tmp_root / "skills"
        scripts_dir.mkdir()
        skills_dir.mkdir()
        shutil.copy(repo_root / "scripts" / "validate_repo.py", scripts_dir / "validate_repo.py")
        (skills_dir / "bad-type.md").write_text(bad, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(scripts_dir / "validate_repo.py")],
            cwd=tmp_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    assert proc.returncode == 1
    assert "type 'INVALID' not in" in proc.stdout
