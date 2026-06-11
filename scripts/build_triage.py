#!/usr/bin/env python3
"""
Auto-build the generated artifacts from the real skill files:
  1) the CATALOG block inside prompts/triage.md   (routing)
  2) skills/INDEX.md                               (live raw-URL manifest = auto-sync)
  3) dist/all-skills.md                            (ALL skills bundle, AI self-routes)

All must stay in sync with skills/ so the router, the live links, and the bundle
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
BUNDLE = ROOT / "dist" / "all-skills.md"
RAW = "https://raw.githubusercontent.com/areliw/mt-score-up-skill/main/skills/"
START, END = "<!-- CATALOG:START -->", "<!-- CATALOG:END -->"
MAXLEN = 150
SKIP = {"README.md", "INDEX.md"}


def skill_files() -> list[Path]:
    return [f for f in sorted(SKILLS.glob("*.md")) if f.name not in SKIP]


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


def use_when(text: str) -> str:
    """Condensed '## ใช้เมื่อ' triggers — the routing signal — joined to one line."""
    m = re.search(r"(?m)^##\s*ใช้เมื่อ\s*$(.+?)(?=^##\s)", text, flags=re.S)
    if not m:
        return ""
    bullets = []
    for line in m.group(1).splitlines():
        s = line.strip()
        if s.startswith(("-", "*")):
            b = re.sub(r"`([^`]+)`", r"\1", re.sub(r"\*\*(.+?)\*\*", r"\1", s[1:].strip()))
            if b:
                bullets.append(b)
    joined = " · ".join(bullets)
    return joined[:170] + ("…" if len(joined) > 170 else "")


def load_rows():
    rows = []
    for f in skill_files():
        t = f.read_text(encoding="utf-8")
        rows.append((frontmatter_value(t, "skill") or f.stem, intro_line(t),
                     frontmatter_value(t, "last_edited") or "—", use_when(t)))
    rows.sort(key=lambda r: r[0])
    return rows


def _write_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def write_triage_catalog(rows) -> bool:
    if not TRIAGE.exists():
        sys.exit(f"ERROR: router file missing: {TRIAGE} — cannot sync catalog. "
                 "Restore prompts/triage.md (with CATALOG markers) before building.")
    def entry(n, d, u):
        line = f"- `{n}` — {d}" if d else f"- `{n}`"
        return line + (f"\n  ↳ ใช้เมื่อ: {u}" if u else "")
    catalog = "\n".join(entry(n, d, u) for n, d, _e, u in rows)
    doc = TRIAGE.read_text(encoding="utf-8")
    if START not in doc or END not in doc:
        sys.exit(f"ERROR: router file {TRIAGE} is missing CATALOG markers "
                 f"({START} / {END}) — cannot sync catalog. Restore the markers before building.")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), f"{START}\n{catalog}\n{END}", doc, flags=re.S)
    return _write_if_changed(TRIAGE, new) if new != doc else False


def write_index(rows) -> bool:
    lines = [
        "# Skill Index — live links (auto-generated · อย่าแก้มือ)",
        "",
        "**โหลดสด (auto-sync):** บอก AI ที่ต่อเน็ตได้ว่า *“ดึง skill จาก URL นี้มาใช้”* → ได้เวอร์ชัน",
        "ล่าสุดบน `main` ทุกครั้ง. **ก๊อปเนื้อไฟล์** = snapshot แช่แข็ง (เสถียร/cite ได้).",
        "อยากได้ทุก skill ในไฟล์เดียว → [`dist/all-skills.md`](../dist/all-skills.md) (สำหรับ AI context ใหญ่).",
        "",
        "| skill | live URL (raw) | updated |",
        "|---|---|---|",
    ]
    lines += [f"| `{n}` | {RAW}{n}.md | {edited} |" for n, _d, edited, _u in rows]
    return _write_if_changed(INDEX, "\n".join(lines) + "\n")


def write_bundle() -> bool:
    header = (
        "# MT Score UP — ALL skills bundle (auto-generated)\n\n"
        "> ⚠️ ไฟล์ใหญ่ (รวมทุก skill ~90K tokens) — เหมาะกับ AI ที่ context ใหญ่ "
        "(Claude · Gemini · Custom GPT / Claude Project) **ไม่เหมาะแชต GPT เปล่า**. "
        "อยากเบา/โหลดเฉพาะที่ต้องการ → ใช้ [`prompts/triage.md`](../prompts/triage.md)\n\n"
        "**ถึง AI:** ด้านล่างคือชุด *วิจารณญาณ MT* ทั้งหมด. ทุกคำถามของผู้ใช้ → **เลือกใช้เฉพาะ skill "
        "ที่เกี่ยวข้อง 1-2 ตัวเงียบๆ** (ไม่ต้องท่องทั้งหมด) · ทำตามกฎ verify-first / ความปลอดภัยของ skill นั้น · "
        "เนื้อหาเป็น **decision-support ไม่ใช่คำสั่งวินิจฉัย/รักษา** — MT/แพทย์ผู้ใช้ตรวจสอบก่อนใช้จริงเสมอ · "
        "เตือนผู้ใช้ให้ลบข้อมูลคนไข้/สถาบันออกเมื่อแชร์\n\n"
        "เวอร์ชัน/ที่มา: ดู `CHANGELOG.md` + แต่ละ skill มี `last_edited` ใน frontmatter\n"
    )
    parts = [header]
    for f in skill_files():
        parts.append(f"\n\n<!-- ═════════ skill: {f.stem} ═════════ -->\n\n" + f.read_text(encoding="utf-8").strip())
    return _write_if_changed(BUNDLE, "\n".join(parts) + "\n")


def check_readme_coverage(rows) -> dict:
    """Both README.md (root category tables) AND skills/README.md (detailed catalog) are
    hand-curated, so we DON'T auto-gen them — but warn loudly if a skill drifted out of
    EITHER (the classic 'engine auto-syncs, storefront forgotten' bug — which bit
    skills/README.md when 24 skills were added in a parallel session)."""
    out = {}
    for rel in ("README.md", "skills/README.md"):
        p = ROOT / rel
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8")
        miss = [n for n, *_ in rows if f"{n}.md" not in txt and f"`{n}`" not in txt and f"**{n}**" not in txt]
        if miss:
            out[rel] = miss
    return out


def main() -> int:
    rows = load_rows()
    t, i, b = write_triage_catalog(rows), write_index(rows), write_bundle()
    print(
        f"{len(rows)} skills · triage {'updated' if t else 'in-sync'} · "
        f"INDEX {'updated' if i else 'in-sync'} · bundle {'updated' if b else 'in-sync'}"
    )
    missing = check_readme_coverage(rows)
    for rel, miss in missing.items():
        print(f"⚠️  {rel} is MISSING {len(miss)} skill(s): {', '.join(miss)}"
              f"\n   (hand-curated — add manually; auto-gen INDEX/bundle/triage stay synced)")
    if not missing:
        print("README.md + skills/README.md cover all skills ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
