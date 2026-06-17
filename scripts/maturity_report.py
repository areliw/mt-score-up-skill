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
    try:
        rows = json.loads((EVAL / "_ab_slim.json").read_text(encoding="utf-8"))
    except Exception:
        return {}
    out = {}
    for r in rows:  # later entries (this-session x3/x5) overwrite legacy -> best current read
        name = str(r.get("skill", "")).strip()
        if name.endswith(".md"):
            name = name[:-3]
        if name:
            out[name] = {"delta": r.get("delta"), "kind": r.get("effect") or r.get("kind"), "method": r.get("method", "legacy")}
    return out


def screen_corpus() -> str:
    parts = []
    for f in ("round4-new-skills.md", "round5-remaining.md"):
        p = EVAL / f
        if p.exists():
            parts.append(p.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts)


def main() -> int:
    fab = full_ab()
    screen = screen_corpus()
    skills = sorted(p for p in SKILLS.glob("*.md") if p.stem not in SKIP)

    rows, overclaim = [], []
    n_full = n_screen = n_none = 0
    for p in skills:
        slug = p.stem
        text = p.read_text(encoding="utf-8", errors="ignore")
        status = frontmatter_status(text)
        has_full = slug in fab
        has_screen = slug in screen
        if has_full: n_full += 1
        elif has_screen: n_screen += 1
        else: n_none += 1
        ev = "full-A/B" if has_full else ("screen-A/B" if has_screen else "NONE")
        rows.append((slug, status, ev, fab.get(slug, {})))
        # over-claim: semi-stable (old: "codex + A/B") with no A/B evidence of any kind
        if status == "semi-stable" and not has_full and not has_screen:
            overclaim.append(slug)

    print(f"maturity report — {len(skills)} skills")
    print(f"  evidence:  full-A/B {n_full} · screen-A/B {n_screen} · NONE {n_none}")
    semi = [r for r in rows if r[1] == "semi-stable"]
    semi_full = sum(1 for r in semi if r[2] == "full-A/B")
    semi_screen = sum(1 for r in semi if r[2] == "screen-A/B")
    semi_none = sum(1 for r in semi if r[2] == "NONE")
    print(f"  semi-stable ({len(semi)}):  full-A/B {semi_full} · screen-A/B {semi_screen} · NONE {semi_none}")
    if overclaim:
        print(f"\n  OVER-CLAIM — status=semi-stable but NO A/B evidence ({len(overclaim)}):")
        for s in overclaim:
            print(f"    - {s}")
        print("\n  -> re-baseline these toward L2 `reviewed` (codex) until re-A/B, per maturity-ladder.md")
    else:
        print("  no over-claims found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
