from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import ab_tier  # noqa: E402


def test_slug_of_strips_md_suffix() -> None:
    assert ab_tier.slug_of("flow-cytometry-judgment.md") == "flow-cytometry-judgment"
    assert ab_tier.slug_of("poct-judgment") == "poct-judgment"


@pytest.mark.parametrize(
    ("row", "expected"),
    [
        ({"tier": "full"}, "full"),
        ({"tier": "manual"}, "manual"),
        ({"tier": "screen"}, "screen"),
        ({"method": "manual-screen"}, "manual"),
        ({"method": "screen"}, "screen"),
        ({"method": "x3"}, "full"),
        ({}, "full"),
    ],
)
def test_infer_tier(row: dict, expected: str) -> None:
    assert ab_tier.infer_tier(row) == expected


def test_index_by_slug_prefers_full_over_manual() -> None:
    rows = [
        {"skill": "demo-skill.md", "tier": "manual", "method": "manual-screen", "delta": 1.0},
        {"skill": "demo-skill.md", "tier": "full", "method": "x3", "delta": 2.5},
    ]
    idx = ab_tier.index_by_slug(rows)
    assert idx["demo-skill"]["tier"] == "full"
    assert idx["demo-skill"]["delta"] == 2.5


def test_full_slugs_only_includes_full_tier() -> None:
    rows = [
        {"skill": "a.md", "tier": "full"},
        {"skill": "b.md", "tier": "manual"},
        {"skill": "c.md", "method": "x5"},
    ]
    assert ab_tier.full_slugs(rows) == {"a", "c"}


def test_manual_only_slugs_excludes_full() -> None:
    rows = [
        {"skill": "a.md", "tier": "full"},
        {"skill": "b.md", "tier": "manual"},
        {"skill": "c.md", "tier": "screen"},
    ]
    assert ab_tier.manual_only_slugs(rows) == {"b", "c"}


def test_promotion_entry_is_full_tier_only() -> None:
    rows = [
        {"skill": "a.md", "tier": "manual", "delta": 4.0},
        {"skill": "a.md", "tier": "full", "delta": 1.5},
        {"skill": "b.md", "tier": "manual", "delta": 2.0},
    ]
    promo = ab_tier.promotion_entry(rows)
    assert set(promo) == {"a"}
    assert promo["a"]["delta"] == 1.5


def test_any_slugs_collects_all_recorded_skills() -> None:
    rows = [
        {"skill": "x.md", "tier": "manual"},
        {"skill": "y.md", "tier": "full"},
    ]
    assert ab_tier.any_slugs(rows) == {"x", "y"}
