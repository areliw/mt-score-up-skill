#!/usr/bin/env python3
"""Maturity gate — a skill's frontmatter `status:` must not out-rank its evidence.

Hard-gate version of scripts/maturity_report.py (which only reports). Implements the
"status ≤ evidence" rule of docs/design/maturity-ladder.md, mapped onto the live 3-tier
vocab (draft / semi-stable / stable):

  - draft        → no requirement
  - semi-stable  → MUST have empirical A/B evidence: a record in eval/_ab_slim.json (full
                   blind-judge) OR a light screen in eval/round4-new-skills.md / round5-remaining.md
  - stable       → MUST have a signed MT peer-review in eval/peer-review/<slug>-*.md

This matches the 2026-06-18 re-baseline (only skills with NO A/B of any kind were demoted;
screen-only skills stayed semi-stable = ladder L4 `screened`).

Exit 1 if any skill out-ranks its evidence (or carries an unknown status); else 0.
Deterministic, no AI / no API key. Run on all skills, or pass specific files (CI passes the
changed ones). Hash-currency (evidence-stale-after-edit) is a later add — see maturity-ladder.md.
"""
import sys
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
EVAL = ROOT / "eval"
SCOREBOARD = EVAL / "_ab_slim.json"
SCREEN_FILES = ["round4-new-skills.md", "round5-remaining.md"]
PEER_DIR = EVAL / "peer-review"
SKIP = {"README", "INDEX"}
VALID = {"draft", "semi-stable", "stable"}

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def status_of(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "?"


def ab_scored() -> set[str]:
    try:
        rows = json.loads(SCOREBOARD.read_text(encoding="utf-8"))
    except Exception:
        return set()
    out = set()
    for r in rows if isinstance(rows, list) else []:
        name = str(r.get("skill", "")).strip()
        out.add(name[:-3] if name.endswith(".md") else name)
    return out


def screen_corpus() -> str:
    parts = []
    for f in SCREEN_FILES:
        p = EVAL / f
        if p.exists():
            parts.append(p.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts)


def peer_signed() -> set[str]:
    """Skills with at least one peer-review file that records a SIGN verdict."""
    out = set()
    if not PEER_DIR.exists():
        return out
    for p in PEER_DIR.glob("*.md"):
        if p.stem.upper() == "TEMPLATE":
            continue
        try:
            body = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if "SIGN" not in body:
            continue
        stem = p.stem  # convention: <skill-slug>-YYYY-MM-DD.md
        slug = stem.rsplit("-", 3)[0] if stem.count("-") >= 3 else stem
        out.add(slug)
    return out


def main(argv: list[str]) -> int:
    scored = ab_scored()
    screen = screen_corpus()
    signed = peer_signed()
    targets = sorted(SKILLS.glob("*.md")) if (not argv or argv == ["--all"]) else [pathlib.Path(a) for a in argv]

    checked, viol = [], []
    for t in targets:
        slug = t.stem
        if slug in SKIP or not t.name.endswith(".md") or t.parent.name != "skills":
            continue
        st = status_of(t.read_text(encoding="utf-8", errors="ignore"))
        checked.append(slug)
        has_ab = slug in scored or slug in screen  # full OR light screen
        if st not in VALID:
            viol.append((slug, st, f"unknown status (allowed: {', '.join(sorted(VALID))})"))
        elif st == "semi-stable" and not has_ab:
            viol.append((slug, st, "semi-stable but no A/B evidence (neither _ab_slim.json nor a screen round)"))
        elif st == "stable" and slug not in signed:
            viol.append((slug, st, "stable but no signed MT peer-review in eval/peer-review/"))

    if not checked:
        print("maturity-gate: no skill files to check — OK")
        return 0
    print(f"maturity-gate: checked {len(checked)} skill(s) — status ≤ evidence")
    if viol:
        print(f"\n  OVER-CLAIM ({len(viol)}):")
        for slug, st, why in viol:
            print(f"    - {slug} [{st}] — {why}")
        print("\n  -> earn the status (run eval/harness/ab-x3.js / record a peer-review) or lower it.\n")
        return 1
    print("  all checked skills are within their evidence — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
