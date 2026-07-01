"""Evidence tiers for eval/_ab_slim.json — shared by gate/coverage/report scripts.

Tiers (strongest → weakest for promotion):
  full   — harness blind-judge (Haiku answerer, Opus judge, order swap): x3/x5/legacy
  screen — structured screen row in _ab_slim (rare; round4/5 prose stays in markdown)
  manual — same-session / same-model manual runs; exploratory only

Legacy rows without `tier` infer from `method`:
  manual* → manual · x3/x5/legacy/absent → full
"""
from __future__ import annotations

import json
import pathlib
import re
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCOREBOARD = ROOT / "eval" / "_ab_slim.json"
PEER_DIR = ROOT / "eval" / "peer-review"

TIER_RANK = {"full": 3, "screen": 2, "manual": 1}

# A peer-review file names its skill in a `**skill:** `<slug>`` line and is SIGNED only when
# the `## Verdict` SIGN checkbox is ticked `[x]` (DRAFT/TEMPLATE leave it `[ ]`).
_PEER_SKILL_RE = re.compile(r"\*\*skill:\*\*\s*`?([a-z0-9][a-z0-9-]*)`?")
_PEER_SIGN_RE = re.compile(r"(?m)^\s*-?\s*\[[xX]\]\s*\*\*SIGN\*\*")


def slug_of(name: str) -> str:
    name = str(name).strip()
    return name[:-3] if name.endswith(".md") else name


def infer_tier(row: dict[str, Any]) -> str:
    explicit = str(row.get("tier", "")).strip().lower()
    if explicit in TIER_RANK:
        return explicit
    method = str(row.get("method", "")).strip().lower()
    if "manual" in method:
        return "manual"
    if method == "screen":
        return "screen"
    return "full"


def load_rows(path: pathlib.Path | None = None) -> list[dict[str, Any]]:
    p = path or SCOREBOARD
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []
    return [r for r in data if isinstance(r, dict)] if isinstance(data, list) else []


def index_by_slug(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Best row per slug — full tier beats manual/screen; later row wins on tie."""
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        slug = slug_of(row.get("skill", ""))
        if not slug:
            continue
        tier = infer_tier(row)
        enriched = {**row, "tier": tier}
        prev = out.get(slug)
        if prev is None:
            out[slug] = enriched
            continue
        if TIER_RANK[tier] > TIER_RANK[infer_tier(prev)]:
            out[slug] = enriched
        elif TIER_RANK[tier] == TIER_RANK[infer_tier(prev)]:
            out[slug] = enriched
    return out


def full_slugs(rows: list[dict[str, Any]] | None = None) -> set[str]:
    rows = rows if rows is not None else load_rows()
    return {s for s, r in index_by_slug(rows).items() if infer_tier(r) == "full"}


def any_slugs(rows: list[dict[str, Any]] | None = None) -> set[str]:
    rows = rows if rows is not None else load_rows()
    return {slug_of(r.get("skill", "")) for r in rows if slug_of(r.get("skill", ""))}


def manual_only_slugs(rows: list[dict[str, Any]] | None = None) -> set[str]:
    """Slugs with _ab_slim record but no full-tier row (manual and/or screen tier only)."""
    rows = rows if rows is not None else load_rows()
    idx = index_by_slug(rows)
    return {s for s, r in idx.items() if infer_tier(r) != "full"}


def promotion_entry(rows: list[dict[str, Any]] | None = None) -> dict[str, dict[str, Any]]:
    """Entry used for semi-stable promotion / winning delta — full tier only."""
    rows = rows if rows is not None else load_rows()
    return {s: r for s, r in index_by_slug(rows).items() if infer_tier(r) == "full"}


def peer_signed(peer_dir: pathlib.Path | None = None) -> set[str]:
    """Slugs with a SIGNED MT peer-review in eval/peer-review/.

    "Signed" = the `## Verdict` SIGN checkbox is ticked `[x]`; DRAFT and TEMPLATE files
    (unchecked `[ ]`) are excluded. The skill slug is read from the `**skill:**` line,
    never guessed from the filename (a `<slug>-<reviewer>-<date>.md` name would mis-split).
    """
    d = peer_dir or PEER_DIR
    out: set[str] = set()
    if not d.exists():
        return out
    for p in d.glob("*.md"):
        if p.stem.upper() == "TEMPLATE":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if not _PEER_SIGN_RE.search(text):
            continue
        m = _PEER_SKILL_RE.search(text)
        if m:
            out.add(m.group(1))
    return out
