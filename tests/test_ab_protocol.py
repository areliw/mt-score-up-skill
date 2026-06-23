"""Golden-vector tests for eval/harness/python/protocol.py — no API calls."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "eval" / "harness" / "python"))

from protocol import (  # noqa: E402
    HarnessConfig,
    RepScores,
    classify_kind,
    load_prompt,
    parse_config,
    score_reps,
    score_row_to_dict,
    slim_row_from_score,
    unswap_verdict,
)


# Round6-derived rep vectors (per-run ws/wos after blind unswap)
GIT_WORKFLOW_REPS = [
    RepScores(ws=5, wos=1),
    RepScores(ws=4, wos=3),
    RepScores(ws=4, wos=3),
]

DEEP_RESEARCH_REPS = [
    RepScores(ws=1, wos=4),
    RepScores(ws=1, wos=4),
    RepScores(ws=2, wos=4),
]

INTERPROFESSIONAL_REPS = [
    RepScores(ws=5, wos=2),
    RepScores(ws=5, wos=2),
    RepScores(ws=5, wos=2),
]

TIE_BOTH_SAFE_REPS = [
    RepScores(ws=4, wos=4),
    RepScores(ws=4, wos=4),
    RepScores(ws=4, wos=4),
]

STYLE_COST_REPS = [
    RepScores(ws=3, wos=4),
    RepScores(ws=3, wos=4),
    RepScores(ws=3, wos=4),
]


def test_parse_config_array_default_reps() -> None:
    cfg = parse_config([{"skill": "a", "file": "skills/a.md", "focus": "trap"}])
    assert isinstance(cfg, HarnessConfig)
    assert cfg.reps == 3
    assert cfg.targets[0].skill == "a"


def test_parse_config_object_reps() -> None:
    raw = {"targets": [{"skill": "b", "file": "skills/b.md", "focus": "x"}], "reps": 5}
    cfg = parse_config(raw)
    assert cfg.reps == 5
    assert len(cfg.targets) == 1


def test_parse_config_json_string() -> None:
    cfg = parse_config(json.dumps([{"skill": "c", "file": "skills/c.md", "focus": "y"}]))
    assert cfg.targets[0].skill == "c"


def test_unswap_even_and_odd() -> None:
    assert unswap_verdict(2, 5, even=True) == RepScores(ws=5, wos=2)
    assert unswap_verdict(2, 5, even=False) == RepScores(ws=2, wos=5)


@pytest.mark.parametrize(
    ("reps", "skill", "expected"),
    [
        (
            GIT_WORKFLOW_REPS,
            "git-workflow-judgment",
            {
                "meanWithout": 2.33,
                "meanWith": 4.33,
                "delta": 2.0,
                "se": 0.745,
                "threshold": 1.49,
                "kind": "rescued",
            },
        ),
        (
            INTERPROFESSIONAL_REPS,
            "interprofessional-communication-judgment",
            {
                "meanWithout": 2.0,
                "meanWith": 5.0,
                "delta": 3.0,
                "se": 0.0,
                "threshold": 0.8,
                "kind": "rescued",
            },
        ),
        (
            DEEP_RESEARCH_REPS,
            "deep-research",
            {
                "meanWithout": 4.0,
                "meanWith": 1.33,
                "delta": -2.67,
                "se": 0.333,
                "threshold": 0.8,
                "kind": "regression",
            },
        ),
        (
            TIE_BOTH_SAFE_REPS,
            "crm-judgment",
            {
                "meanWithout": 4.0,
                "meanWith": 4.0,
                "delta": 0.0,
                "se": 0.0,
                "threshold": 0.8,
                "kind": "tie",
            },
        ),
        (
            STYLE_COST_REPS,
            "urinalysis-judgment",
            {
                "meanWithout": 4.0,
                "meanWith": 3.0,
                "delta": -1.0,
                "se": 0.0,
                "threshold": 0.8,
                "kind": "style-cost",
            },
        ),
    ],
)
def test_score_reps_golden_vectors(
    reps: list[RepScores],
    skill: str,
    expected: dict,
) -> None:
    row = score_reps(skill, reps)
    assert row is not None
    d = score_row_to_dict(row)
    for key, val in expected.items():
        assert d[key] == val, f"{skill}.{key}: got {d[key]!r}, want {val!r}"


def test_classify_kind_boundaries() -> None:
    assert classify_kind(2.0, 1.0, 4.0, 2.0, 0.5) == "rescued"
    assert classify_kind(1.5, 1.0, 4.0, 3.5, 0.5) == "better"
    assert classify_kind(-2.0, 1.5, 2.0, 4.0, 0.75) == "regression"
    assert classify_kind(-0.6, 0.8, 3.5, 4.0, 0.5) == "style-cost"
    assert classify_kind(0.2, 0.8, 2.0, 2.0, 0.4) == "no-rescue"
    assert classify_kind(0.3, 0.8, 3.5, 3.5, 0.4) == "tie"


def test_slim_row_full_tier() -> None:
    row = score_reps("git-workflow-judgment", GIT_WORKFLOW_REPS)
    assert row is not None
    slim = slim_row_from_score(row, run_id="test-run")
    assert slim["tier"] == "full"
    assert slim["method"] == "x3"
    assert slim["run"] == "test-run"
    assert slim["skill"] == "git-workflow-judgment.md"
    assert slim["effect"] == "lift"
    assert slim["trapAvoid"] == "with-only"


def test_load_prompt_templates() -> None:
    text = load_prompt("judge.txt", scenario="S", answer1="A1", answer2="A2", focus="F")
    assert "{scenario}" not in text
    assert "S" in text and "A1" in text
