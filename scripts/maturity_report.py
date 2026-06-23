#!/usr/bin/env python3
"""Maturity report — claimed status vs actual evidence (advisory, honest).

Implements the *measurement* half of docs/design/maturity-ladder.md: for each skill,
show the evidence we actually have and the honest max level it supports, then flag where
the frontmatter `status:` claims more than the evidence backs. Does NOT mutate anything —
it surfaces the re-baseline gap as data for the maintainer to decide.

Evidence sources (deterministic, no AI):
  - L1 structured : validate_repo gates this in CI -> assumed for all present skills
  - full A/B      : eval/_ab_slim.json (Δ/kind)            -> toward L5 `proven`
  - screen A/B    : eval/round4-new-skills.md, round5-remaining.md -> toward L4 `screened`
Hash-currency for legacy A/B can't be auto-verified (no stored test-time hash), so a full-A/B
record only *suggests* L5; it is reported, not auto-granted.

Usage: python scripts/maturity_report.py
"""
import sys, json, pathlib, hashlib

from ab_tier import full_slugs, index_by_slug, infer_tier, load_rows, manual_only_slugs

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
EVAL = ROOT / "eval"
SKIP = {"README", "INDEX"}

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def frontmatter_status(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "?"


def full_ab() -> dict:
    return {s: {"delta": r.get("delta"), "kind": r.get("effect") or r.get("kind"), "method": r.get("method", "legacy"), "tier": infer_tier(r)}
            for s, r in index_by_slug(load_rows()).items() if infer_tier(r) == "full"}


def screen_corpus() -> str:
    parts = []
    for f in ("round4-new-skills.md", "round5-remaining.md"):
        p = EVAL / f
        if p.exists():
            parts.append(p.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts)


def main() -> int:
    fab = full_ab()
    manual_only = manual_only_slugs() - full_slugs()
    screen = screen_corpus()
    skills = sorted(p for p in SKILLS.glob("*.md") if p.stem not in SKIP)

    rows, overclaim = [], []
    n_full = n_manual = n_screen = n_none = 0
    for p in skills:
        slug = p.stem
        text = p.read_text(encoding="utf-8", errors="ignore")
        status = frontmatter_status(text)
        has_full = slug in fab
        has_manual = slug in manual_only
        has_screen = slug in screen
        if has_full: n_full += 1
        elif has_manual: n_manual += 1
        elif has_screen: n_screen += 1
        else: n_none += 1
        if has_full:
            ev = "full-A/B"
        elif has_manual:
            ev = "manual-A/B"
        elif has_screen:
            ev = "screen-A/B"
        else:
            ev = "NONE"
        rows.append((slug, status, ev, fab.get(slug, {})))
        if status == "semi-stable" and not has_full and not has_screen:
            overclaim.append(slug)
        elif status == "semi-stable" and has_manual and not has_full and not has_screen:
            overclaim.append(slug)

    print(f"maturity report — {len(skills)} skills")
    print(f"  evidence:  full-tier {n_full} · manual-tier {n_manual} · screen-A/B {n_screen} · NONE {n_none}")
    semi = [r for r in rows if r[1] == "semi-stable"]
    semi_full = sum(1 for r in semi if r[2] == "full-A/B")
    semi_manual = sum(1 for r in semi if r[2] == "manual-A/B")
    semi_screen = sum(1 for r in semi if r[2] == "screen-A/B")
    semi_none = sum(1 for r in semi if r[2] == "NONE")
    print(f"  semi-stable ({len(semi)}):  full-tier {semi_full} · manual-tier {semi_manual} · screen-A/B {semi_screen} · NONE {semi_none}")
    if overclaim:
        print(f"\n  OVER-CLAIM — status=semi-stable but no full-tier A/B nor screen ({len(overclaim)}):")
        for s in overclaim:
            print(f"    - {s}")
        print("\n  -> re-baseline these toward L2 `reviewed` (codex) until re-A/B, per maturity-ladder.md")
    else:
        print("  no over-claims found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
