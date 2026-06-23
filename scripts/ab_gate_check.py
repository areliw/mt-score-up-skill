#!/usr/bin/env python3
"""A/B coverage gate — every skill must have an A/B record in eval/ before it lands.

This is the *deterministic* half of P4 (no AI / no API key needed):
it does NOT run the A/B itself — it enforces that each changed (or all) skill has
a recorded Δ somewhere under eval/. The AI half (actually running the ×3 blind-judge)
runs via Claude Code Workflow: eval/harness/ab-x3.js  (see eval/AB-GATE.md).

Usage:
    python scripts/ab_gate_check.py skills/foo-judgment.md skills/bar.md   # check these
    python scripts/ab_gate_check.py --all                                  # audit whole library

Exit 1 if any checked skill has no A/B record under eval/; else 0.
"""
import sys
import pathlib

import json

from ab_tier import any_slugs, manual_only_slugs, full_slugs

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
SCOREBOARD = ROOT / "eval" / "_ab_slim.json"  # canonical structured A/B record
SKIP = {"README", "INDEX"}  # not skills

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def scored_slugs() -> set[str]:
    """Skill slugs that have any Δ entry in the structured scoreboard."""
    return any_slugs()


def main(argv: list[str]) -> int:
    scored = scored_slugs()
    manual_only = manual_only_slugs() - full_slugs()
    if argv == ["--all"]:
        targets = sorted(SKILLS.glob("*.md"))
    else:
        targets = [pathlib.Path(a) for a in argv]

    checked, missing = [], []
    for t in targets:
        stem = t.stem
        if stem in SKIP or not t.name.endswith(".md"):
            continue
        if t.parent.name != "skills":
            continue
        checked.append(stem)
        if stem not in scored:
            missing.append(stem)

    if not checked:
        print("ab-gate: no skill files to check — OK")
        return 0

    print(f"ab-gate: checked {len(checked)} skill(s) against eval/_ab_slim.json")
    if missing:
        print(f"\n  MISSING A/B record ({len(missing)}):")
        for m in missing:
            print(f"    - {m}")
        print(
            "\n  -> run the x3 A/B harness on these and record the result:\n"
            "       Workflow({scriptPath: 'eval/harness/ab-x3.js', args: [{skill, file, focus}, ...]})\n"
            "     then append the delta entry to eval/_ab_slim.json. See eval/AB-GATE.md.\n"
        )
        return 1
    print("  all checked skills have an A/B record - OK")
    warned = [s for s in checked if s in manual_only]
    if warned:
        print(f"\n  WARNING — manual-tier only (NOT valid for semi-stable promotion) ({len(warned)}):")
        for w in warned:
            print(f"    - {w}")
        print("     -> re-run eval/harness/ab-x3.js per eval/ANTI-BIAS-PROTOCOL.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
