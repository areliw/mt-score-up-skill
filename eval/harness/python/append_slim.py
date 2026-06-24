"""Append harness rows to eval/_ab_slim.json."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SLIM = ROOT / "eval" / "_ab_slim.json"


def load_slim(path: Path | None = None) -> list[dict[str, Any]]:
    p = path or DEFAULT_SLIM
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return data if isinstance(data, list) else []


def append_rows(
    rows: list[dict[str, Any]],
    *,
    path: Path | None = None,
    dry_run: bool = False,
) -> int:
    """Append slim rows; returns count appended."""
    if not rows:
        return 0
    p = path or DEFAULT_SLIM
    existing = load_slim(p)
    if dry_run:
        return len(rows)
    existing.extend(rows)
    p.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(rows)
