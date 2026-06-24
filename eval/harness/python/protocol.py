"""Portable A/B protocol — config parsing, scoring, kind classification.

Scoring rules mirror eval/harness/ab-x3.js (L86–101). Unit-tested against golden
vectors derived from round6 probe rows.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HARNESS_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = HARNESS_DIR / "prompts"


@dataclass(frozen=True)
class Target:
    skill: str
    file: str
    focus: str


@dataclass(frozen=True)
class HarnessConfig:
    targets: list[Target]
    reps: int


@dataclass(frozen=True)
class RepScores:
    """Per-rep with-skill / without-skill scores after blind unswap."""

    ws: float
    wos: float


@dataclass(frozen=True)
class ScoreRow:
    skill: str
    reps: int
    mean_without: float
    mean_with: float
    delta: float
    se: float
    sigma: float | None
    threshold: float
    kind: str


def parse_config(raw: Any) -> HarnessConfig:
    """Parse harness args — same shapes as ab-x3.js parseConfig."""
    data = raw
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            data = []
    if isinstance(data, list):
        targets_raw, reps = data, 3
    elif isinstance(data, dict) and isinstance(data.get("targets"), list):
        targets_raw = data["targets"]
        reps = int(data.get("reps") or 0)
        reps = reps if reps > 0 else 3
    else:
        targets_raw, reps = [], 3

    targets: list[Target] = []
    for item in targets_raw:
        if not isinstance(item, dict):
            continue
        skill = str(item.get("skill", "")).strip()
        file = str(item.get("file", "")).strip()
        focus = str(item.get("focus", "")).strip()
        if skill and file and focus:
            targets.append(Target(skill=skill, file=file, focus=focus))
    return HarnessConfig(targets=targets, reps=reps)


def load_prompt(name: str, **kwargs: str) -> str:
    path = PROMPTS_DIR / name
    text = path.read_text(encoding="utf-8")
    return text.format(**kwargs)


def _sd(values: list[float], mean: float, n: int) -> float:
    if n <= 1:
        return 0.0
    var = sum((x - mean) ** 2 for x in values) / max(1, n - 1)
    return math.sqrt(var)


def classify_kind(
    delta: float,
    threshold: float,
    mean_with: float,
    mean_without: float,
    se: float,
) -> str:
    """Kind taxonomy — must match ab-x3.js L95–100."""
    if delta >= threshold and mean_without <= 2.5 and mean_with >= 3:
        return "rescued"
    if delta >= threshold:
        return "better"
    if delta <= -threshold and mean_with <= 2.5:
        return "regression"
    if delta <= -max(se, 0.5):
        return "style-cost"
    if mean_with <= 2.5 and mean_without <= 2.5:
        return "no-rescue"
    return "tie"


def score_reps(skill: str, reps: list[RepScores]) -> ScoreRow | None:
    """Aggregate rep scores into one row (ab-x3.js L85–101)."""
    ok = [r for r in reps if r is not None]
    if not ok:
        return None
    n = len(ok)
    m_with = sum(r.ws for r in ok) / n
    m_without = sum(r.wos for r in ok) / n
    delta = round(m_with - m_without, 2)

    sd_with = _sd([r.ws for r in ok], m_with, n)
    sd_without = _sd([r.wos for r in ok], m_without, n)
    se = round(math.sqrt(sd_with**2 / n + sd_without**2 / n), 3)
    threshold = round(max(2 * se, 0.8), 2)
    sigma = round(delta / se, 2) if se > 0 else None
    kind = classify_kind(delta, threshold, m_with, m_without, se)

    return ScoreRow(
        skill=skill,
        reps=n,
        mean_without=round(m_without, 2),
        mean_with=round(m_with, 2),
        delta=delta,
        se=se,
        sigma=sigma,
        threshold=threshold,
        kind=kind,
    )


def unswap_verdict(
    score1: float,
    score2: float,
    *,
    even: bool,
) -> RepScores:
    """Map blind judge scores back to with/without (ab-x3.js L79)."""
    if even:
        return RepScores(ws=score2, wos=score1)
    return RepScores(ws=score1, wos=score2)


def score_row_to_dict(row: ScoreRow) -> dict[str, Any]:
    return {
        "skill": row.skill,
        "reps": row.reps,
        "meanWithout": row.mean_without,
        "meanWith": row.mean_with,
        "delta": row.delta,
        "se": row.se,
        "sigma": row.sigma,
        "threshold": row.threshold,
        "kind": row.kind,
    }


def infer_effect(kind: str, delta: float) -> str:
    if kind in ("rescued", "better"):
        return "lift"
    if kind == "regression":
        return "backfire"
    if abs(delta) < 0.5:
        return "neutral"
    return "lift" if delta > 0 else "neutral"


def infer_trap_avoid(kind: str, mean_with: float, mean_without: float) -> str:
    if kind == "rescued" and mean_without <= 2.5 and mean_with >= 3:
        return "with-only"
    return "both"


def slim_row_from_score(
    row: ScoreRow,
    *,
    run_id: str,
    method: str = "x3",
    note: str = "Haiku+Opus blind harness (python)",
) -> dict[str, Any]:
    """Build a full-tier _ab_slim.json row from a harness score row."""
    effect = infer_effect(row.kind, row.delta)
    trap = infer_trap_avoid(row.kind, row.mean_with, row.mean_without)
    skill_name = row.skill if row.skill.endswith(".md") else f"{row.skill}.md"
    return {
        "skill": skill_name,
        "effect": effect,
        "withScore": row.mean_with,
        "withoutScore": row.mean_without,
        "delta": row.delta,
        "trapAvoid": trap,
        "method": method,
        "tier": "full",
        "run": run_id,
        "note": note,
    }


def resolve_target_by_skill(skill_slug: str, skills_dir: Path | None = None) -> Target:
    """Build a single target from a skill slug (for --skill CLI)."""
    root = Path(__file__).resolve().parents[3]
    sdir = skills_dir or (root / "skills")
    slug = skill_slug.removesuffix(".md")
    path = sdir / f"{slug}.md"
    if not path.is_file():
        raise FileNotFoundError(f"skill not found: {path}")
    return Target(
        skill=slug,
        file=f"skills/{slug}.md",
        focus="the skill's own #1 anti-pattern",
    )
