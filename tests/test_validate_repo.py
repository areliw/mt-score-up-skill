from __future__ import annotations

from pathlib import Path

from conftest import run_script


def test_validate_repo_passes_on_current_library(repo_root: Path) -> None:
    proc = run_script(repo_root, "validate_repo.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "94 skill files scanned" in proc.stdout
