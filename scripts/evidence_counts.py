#!/usr/bin/env python3
"""Evidence counts — the numbers quoted in EVIDENCE.md, recomputed from the repo's own files.

Read-only. Sources (deterministic, no AI):
  - status         : `status:` in each skills/*.md frontmatter
  - A/B result     : best row per skill in eval/_ab_slim.json (same rule as ab_tier.index_by_slug)
  - lab-bench cards: links under the README section "### 🩸 งานแล็บ"

If a number here and in EVIDENCE.md disagree, this script wins — update EVIDENCE.md.

Usage: python scripts/evidence_counts.py
"""
import re
import sys
import pathlib
from collections import Counter

from ab_tier import index_by_slug, load_rows

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
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


def method_group(row: dict) -> str:
    if row["tier"] != "full":
        return "manual (does not count)"
    return "repeated x3/x5" if str(row.get("method", "")).startswith(("x3", "x5")) else "early rounds"


def main() -> int:
    status = {p.stem: frontmatter_status(p.read_text(encoding="utf-8"))
              for p in sorted(SKILLS.glob("*.md")) if p.stem not in SKIP}
    best = index_by_slug(load_rows())
    untested = sorted(s for s in status if s not in best)

    print(f"guides: {len(status)}")
    print(f"status: {dict(Counter(status.values()))}")
    print(f"with an A/B record: {len(status) - len(untested)}  (untested: {untested or 'none'})")
    print(f"A/B method: {dict(Counter(method_group(best[s]) for s in status if s in best))}")
    for st in sorted(set(status.values())):
        eff = Counter(best[s].get("effect") for s in status if status[s] == st and s in best)
        print(f"A/B effect, {st}: {dict(eff)}")
    semi = [s for s in status if status[s] == "semi-stable" and s in best]
    print(f"semi-stable by method: {dict(Counter(method_group(best[s]) for s in semi))}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    lab_sec = readme.split("### 🩸 งานแล็บ", 1)[1].split("\n## ", 1)[0]
    lab = sorted(set(re.findall(r"\./skills/([a-z0-9-]+)\.md", lab_sec)))
    print(f"lab-bench cards: {len(lab)}  status: {dict(Counter(status.get(s, '?') for s in lab))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
