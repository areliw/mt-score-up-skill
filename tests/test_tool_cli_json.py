"""Every skill tool with subcommands accepts --json on both sides of the subcommand.

PR #125 review: `bb_calc.py rhig --fmh-rbc-ml 20 --json` (the documented example) failed with
"unrecognized arguments: --json" because the flag lived only on the parent parser.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _tools() -> list[Path]:
    out = []
    for p in sorted(ROOT.glob("skills/*/scripts/*.py")):
        s = p.read_text(encoding="utf-8")
        if "add_subparsers" in s and '"--json"' in s:
            out.append(p)
    return out


def _run(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(path), *args], cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=False)


TOOLS = _tools()


def test_tool_list_is_not_empty():
    assert len(TOOLS) >= 20


@pytest.mark.parametrize("tool", TOOLS, ids=lambda p: f"{p.parent.parent.name}/{p.name}")
def test_every_subcommand_accepts_json(tool: Path):
    top = _run(tool, "--help")
    assert top.returncode == 0, top.stderr
    m = re.search(r"\{([\w,-]+)\}", top.stdout)
    assert m, "no subcommand list in --help"
    for cmd in m.group(1).split(","):
        h = _run(tool, cmd, "--help")
        assert h.returncode == 0, h.stderr
        assert "--json" in h.stdout, f"{tool.name} {cmd}: --json missing after the subcommand"


BB = ROOT / "skills" / "bloodbank-judgment" / "scripts" / "bb_calc.py"


@pytest.mark.parametrize("args", [
    ("rhig", "--fmh-rbc-ml", "20", "--json"),   # documented example
    ("--json", "rhig", "--fmh-rbc-ml", "20"),   # flag before the subcommand must keep working
])
def test_bb_calc_json_either_position(args):
    r = _run(BB, *args)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["vials"] == 2      # 40 mL WB / 30 -> 1.33 -> 1 + 1 safety vial


def test_text_output_unchanged_without_json():
    r = _run(BB, "rhig", "--fmh-rbc-ml", "20")
    assert r.returncode == 0 and r.stdout.lstrip().startswith("fetal bleed")
