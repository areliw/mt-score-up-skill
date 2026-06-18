#!/usr/bin/env python3
"""Maturity gate — a skill's `status:` must not out-rank its evidence, and the evidence
must still cover the current content (hash-currency).

Hard-gate version of scripts/maturity_report.py. Implements "status ≤ evidence" + hash-currency
from docs/design/maturity-ladder.md, on the live 3-tier vocab (draft / semi-stable / stable):

  - draft        → no requirement
  - semi-stable  → MUST have empirical A/B: a record in eval/_ab_slim.json (full blind-judge)
                   OR a light screen in eval/round4-new-skills.md / round5-remaining.md
  - semi-stable/stable → its WINNING A/B delta (eval/ab-coverage.json) must NOT be negative
                   (a "backfire" result cannot back a "proven helpful" claim).
  - stable       → MUST have a signed MT peer-review in eval/peer-review/<slug>-*.md
  - semi-stable/stable → its BODY hash must match eval/ab-coverage.json (else the judgment was
                   edited since it was tested → evidence stale → re-test + rebuild the registry).

BODY hash = sha256 of content after the frontmatter, so editing status/last_edited does NOT
trip staleness — only a real judgment change does. Exit 1 on any violation; else 0.
Deterministic, no AI / no key. Run on all skills, or pass changed files (CI passes them).
"""
import sys
import json
import hashlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
EVAL = ROOT / "eval"
SCOREBOARD = EVAL / "_ab_slim.json"
REGISTRY = EVAL / "ab-coverage.json"
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


def split_body(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            nl = text.find("\n", end + 1)
            return text[nl + 1:] if nl != -1 else ""
    return text


def body_hash(text: str) -> str:
    return hashlib.sha256(split_body(text).strip().encode("utf-8")).hexdigest()[:12]


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
    out = set()
    if not PEER_DIR.exists():
        return out
    for p in PEER_DIR.glob("*.md"):
        if p.stem.upper() == "TEMPLATE":
            continue
        if "SIGN" in p.read_text(encoding="utf-8", errors="ignore"):
            stem = p.stem
            out.add(stem.rsplit("-", 3)[0] if stem.count("-") >= 3 else stem)
    return out


def registry() -> dict:
    try:
        return json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception:
        return {}


def main(argv: list[str]) -> int:
    scored = ab_scored()
    screen = screen_corpus()
    signed = peer_signed()
    reg = registry()
    targets = sorted(SKILLS.glob("*.md")) if (not argv or argv == ["--all"]) else [pathlib.Path(a) for a in argv]

    checked, viol = [], []
    for t in targets:
        slug = t.stem
        if slug in SKIP or not t.name.endswith(".md") or t.parent.name != "skills":
            continue
        text = t.read_text(encoding="utf-8", errors="ignore")
        st = status_of(text)
        checked.append(slug)
        has_ab = slug in scored or slug in screen
        if st not in VALID:
            viol.append((slug, st, f"unknown status (allowed: {', '.join(sorted(VALID))})"))
            continue
        if st == "semi-stable" and not has_ab:
            viol.append((slug, st, "semi-stable but no A/B evidence (neither _ab_slim.json nor a screen round)"))
            continue
        if st == "stable" and slug not in signed:
            viol.append((slug, st, "stable but no signed MT peer-review in eval/peer-review/"))
            continue
        # negative-evidence: a tested skill whose WINNING A/B delta is negative (backfire) is
        # over-claimed — "proven helpful" cannot rest on a negative result. (gate hole, fixed 2026-06-19)
        if st in ("semi-stable", "stable") and slug in reg:
            d = reg[slug].get("ab_delta")
            if isinstance(d, (int, float)) and d < 0:
                viol.append((slug, st, f"A/B winning delta is NEGATIVE ({d}) — over-claim; re-test (x5, need delta>=2*SE) or demote to draft"))
                continue
        # hash-currency: a tested skill whose body changed since the registry was built = stale
        if st in ("semi-stable", "stable") and slug in reg:
            if reg[slug].get("body_hash") and reg[slug]["body_hash"] != body_hash(text):
                viol.append((slug, st, "evidence STALE — body changed since last A/B; re-test (eval/harness/ab-x3.js) + rebuild ab-coverage.json"))

    if not checked:
        print("maturity-gate: no skill files to check — OK")
        return 0
    print(f"maturity-gate: checked {len(checked)} skill(s) — status ≤ evidence + hash-currency")
    if viol:
        print(f"\n  VIOLATION ({len(viol)}):")
        for slug, st, why in viol:
            print(f"    - {slug} [{st}] — {why}")
        print("\n  -> earn the status / re-test the edited skill, or lower the status.\n")
        return 1
    print("  all checked skills are within their evidence (class + hash-current) — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
