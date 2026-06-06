#!/usr/bin/env python3
"""
Auto-build the generated indexes from the real skill files:
  1) the CATALOG block inside prompts/triage.md  (routing)
  2) skills/INDEX.md                              (live raw-URL manifest = auto-sync)

Both must stay in sync with skills/ so the triage router and the "load live" links
never go stale. Deterministic (no judgment) → safe to run in CI and auto-commit,
unlike STANDARDS.md (edition bumps need human judgment).

Usage:  python scripts/build_triage.py
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
INDEX = SKILLS / "INDEX.md"
RAW = "https://raw.githubusercontent.com/areliw/mt-score-up-skill/main/skills/"
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
        clean = re.sub(r"\*\*(.+?)\*\*", r"\1", line)
        return clean[:MAXLEN] + ("…" if len(clean) > MAXLEN else "")
    return ""


def load_skills() -> list[tuple[str, str, str]]:
    """Return sorted (name, intro, last_edited) for every skill file."""
    rows = []
    for f in sorted(SKILLS.glob("*.md")):
        if f.name in ("README.md", "INDEX.md"):
            continue
        t = f.read_text(encoding="utf-8")
        name = frontmatter_value(t, "skill") or f.stem
        rows.append((name, intro_line(t), frontmatter_value(t, "last_edited") or "—"))
    rows.sort(key=lambda r: r[0])
    return rows


def write_triage_catalog(rows) -> bool:
    if not TRIAGE.exists():
        print(f"WARN: {TRIAGE} not found — skip triage")
        return False
    catalog = "\n".join(f"- `{n}` — {d}" if d else f"- `{n}`" for n, d, _ in rows)
    doc = TRIAGE.read_text(encoding="utf-8")
    if START not in doc or END not in doc:
        print("WARN: markers not found in triage.md — skip")
        return False
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), f"{START}\n{catalog}\n{END}", doc, flags=re.S)
    if new != doc:
        TRIAGE.write_text(new, encoding="utf-8")
        return True
    return False


def write_index(rows) -> bool:
    lines = [
        "# Skill Index — live links (auto-generated · อย่าแก้มือ)",
        "",
        "**โหลดสด (auto-sync):** บอก AI ที่ต่อเน็ตได้ว่า *“ดึง skill จาก URL นี้มาใช้”* → ได้เวอร์ชัน",
        "ล่าสุดบน `main` ทุกครั้ง (ไม่ต้องก๊อปใหม่). **ก๊อปเนื้อไฟล์** = snapshot แช่แข็ง (เสถียร/cite ได้).",
        "เลือกตามงาน — งานคลินิกที่ต้อง cite audit → freeze; อยากตามอัปเดตเสมอ → live link.",
        "",
        "| skill | live URL (raw) | updated |",
        "|---|---|---|",
    ]
    for n, _d, edited in rows:
        lines.append(f"| `{n}` | {RAW}{n}.md | {edited} |")
    lines.append("")
    content = "\n".join(lines)
    if not INDEX.exists() or INDEX.read_text(encoding="utf-8") != content:
        INDEX.write_text(content, encoding="utf-8")
        return True
    return False


def main() -> int:
    rows = load_skills()
    t = write_triage_catalog(rows)
    i = write_index(rows)
    print(f"{len(rows)} skills · triage {'updated' if t else 'in-sync'} · INDEX {'updated' if i else 'in-sync'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
