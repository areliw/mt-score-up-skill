#!/usr/bin/env python3
"""
Repo validator — fast, zero-dependency CI guard for the skills library.

Checks (fails CI on any error):
  1. Frontmatter — every skills/*.md (except catalogs) has the required keys,
     a valid `type` / `needs` / `last_edited` format, and a title within length.
  2. Structure — every skill keeps the canonical sections (ใช้เมื่อ / กับดัก /
     ช่องสำหรับผู้เชี่ยวชาญ) so the judgment-skill shape can't silently erode.
  3. Internal links — every relative markdown link in README + skills/ resolves
     to a real file or folder (catches dead links as the repo grows).

Stdlib only (no PyYAML / external action) → matches the project's 0-dependency,
0-build ethos and the existing scripts/ style.

Exit codes:
    0 = all good
    1 = one or more validation errors (printed, grouped)

Run: python scripts/validate_repo.py
"""

import re
import sys
from pathlib import Path

# Force UTF-8 stdout so the ✅/❌ summary prints on a default Windows (cp1252) console.
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).parent.parent
SKILLS = ROOT / "skills"

REQUIRED_KEYS = ["skill", "title", "type", "needs", "author", "last_edited", "status", "disclaimer"]
VALID_TYPE = {"ADVISE", "DO", "CALIBRATION"}
VALID_NEEDS = {"any", "code-interpreter", "persistent-memory"}
# Structural lint: every skill keeps the canonical sections (all 93 comply as of
# 2026-06-18 — gate guards against future skills silently dropping them). Substring,
# not heading-anchored, so legitimate heading variants ("## กับดัก (Anti-patterns)") pass.
REQUIRED_SECTIONS = ["ใช้เมื่อ", "กับดัก", "ช่องสำหรับผู้เชี่ยวชาญ"]
TITLE_MAXLEN = 160  # catalog/triage truncates ~150; keep titles scannable
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
KEY_RE = re.compile(r"^([A-Za-z_]+):\s*(.*)$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

# catalogs / non-skill markdown living inside skills/
NON_SKILL = {"README.md", "INDEX.md"}

errors: list[str] = []


def frontmatter(path: Path):
    """Return {key: value} from the leading --- ... --- block, or None."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm = {}
    for line in text[3:end].splitlines():
        m = KEY_RE.match(line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


# 1. frontmatter
skill_files = [m for m in sorted(SKILLS.glob("*.md")) if m.name not in NON_SKILL]
for md in skill_files:
    rel = md.relative_to(ROOT)
    fm = frontmatter(md)
    if fm is None:
        errors.append(f"{rel}: no YAML frontmatter block")
        continue
    for key in REQUIRED_KEYS:
        if not fm.get(key):
            errors.append(f"{rel}: missing/empty frontmatter key '{key}'")
    if fm.get("type") and fm["type"].split()[0] not in VALID_TYPE:
        errors.append(f"{rel}: type '{fm['type'].split()[0]}' not in {sorted(VALID_TYPE)}")
    if fm.get("needs") and fm["needs"].split()[0].strip(",") not in VALID_NEEDS:
        errors.append(f"{rel}: needs '{fm['needs'].split()[0]}' not in {sorted(VALID_NEEDS)}")
    if fm.get("last_edited") and not DATE_RE.match(fm["last_edited"].split()[0]):
        errors.append(f"{rel}: last_edited '{fm['last_edited']}' not YYYY-MM-DD")
    if fm.get("title") and len(fm["title"]) > TITLE_MAXLEN:
        errors.append(f"{rel}: title {len(fm['title'])} chars > {TITLE_MAXLEN} (keep it scannable)")
    body = md.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f"{rel}: missing canonical section '{section}'")

# 2. internal links (README + every skill file)
for md in [ROOT / "README.md", SKILLS / "README.md", *skill_files]:
    if not md.exists():
        continue
    for target in LINK_RE.findall(md.read_text(encoding="utf-8")):
        target = target.strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0]  # drop anchor
        if not target:
            continue
        if not (md.parent / target).resolve().exists():
            errors.append(f"{md.relative_to(ROOT)}: dead link → {target}")

if errors:
    print(f"❌ validate_repo: {len(errors)} problem(s)\n")
    for e in errors:
        print("  -", e)
    sys.exit(1)

print(f"✅ validate_repo: frontmatter + internal links OK "
      f"({len(skill_files)} skill files scanned)")
