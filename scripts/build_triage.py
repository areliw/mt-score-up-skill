#!/usr/bin/env python3
"""
Auto-build the skill CATALOG inside prompts/triage.md from the real skill files.

The triage prompt routes a user's problem to the right skill — so its catalog must
stay in sync with skills/ automatically. This regenerates the block between the
<!-- CATALOG:START --> / <!-- CATALOG:END --> markers from each skill's frontmatter
`skill:` name + its one-line intro (the first description line under the # heading).

Deterministic (no judgment) → safe to run in CI and auto-commit, unlike STANDARDS.md
(which stays human-reviewed because edition bumps need judgment).

Usage:  python scripts/build_triage.py
Exit 0 if it ran; the file is rewritten in place only if the catalog changed.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
TRIAGE = ROOT / "prompts" / "triage.md"
START, END = "<!-- CATALOG:START -->", "<!-- CATALOG:END -->"
MAXLEN = 150


def frontmatter_value(text: str, key: str) -> str | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    for line in text[3:end].splitlines():
        m = re.match(rf"^{key}\s*:\s*(.+)$", line)
        if m:
            return m.group(1).strip().strip("\"'")
    return None


def intro_line(text: str) -> str:
    """First descriptive line after the `# Heading` (skips blanks/blockquotes/headings)."""
    body_start = text.find("\n---", 3)
    body = text[body_start + 4 :] if body_start != -1 else text
    seen_h1 = False
    for raw in body.splitlines():
        line = raw.strip()
        if not seen_h1:
            if line.startswith("# "):
                seen_h1 = True
            continue
        if not line or line.startswith(("#", ">", "<", "|", "-", "*")):
            continue
        # strip markdown emphasis for a clean one-liner
        clean = re.sub(r"\*\*(.+?)\*\*", r"\1", line)
        return clean[:MAXLEN] + ("…" if len(clean) > MAXLEN else "")
    return ""


def build_catalog() -> tuple[str, int]:
    rows = []
    for f in sorted(SKILLS.glob("*.md")):
        if f.name == "README.md":
            continue
        t = f.read_text(encoding="utf-8")
        name = frontmatter_value(t, "skill") or f.stem
        rows.append((name, intro_line(t)))
    rows.sort(key=lambda r: r[0])
    lines = [f"- `{name}` — {desc}" if desc else f"- `{name}`" for name, desc in rows]
    return "\n".join(lines), len(rows)


def main() -> int:
    if not TRIAGE.exists():
        print(f"ERROR: {TRIAGE} not found")
        return 1
    catalog, n = build_catalog()
    doc = TRIAGE.read_text(encoding="utf-8")
    if START not in doc or END not in doc:
        print(f"ERROR: markers {START}/{END} not found in triage.md")
        return 1
    new_block = f"{START}\n{catalog}\n{END}"
    updated = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: new_block, doc, flags=re.S)
    if updated != doc:
        TRIAGE.write_text(updated, encoding="utf-8")
        print(f"triage catalog updated — {n} skills")
    else:
        print(f"triage catalog already in sync — {n} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
