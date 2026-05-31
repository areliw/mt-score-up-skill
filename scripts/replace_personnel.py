#!/usr/bin/env python3
"""
Personnel replacement utility — swap names across a filled WI docx.

Handles the personnel-rotation scenario (per rule-mt-in-drivers-seat): when a
person leaves/changes role, their name in the template's signature block (footer,
header, or body) must update across all WIs. Template hardcodes names (not
placeholders), so we post-process the rendered docx.

Searches ALL locations: body paragraphs + body tables + every section's
header/footer paragraphs + header/footer tables.

Usage:
    python scripts/replace_personnel.py <doc.docx> "<old name>=<new name>" ["<old2>=<new2>" ...]

Example:
    python scripts/replace_personnel.py wi.docx "[ชื่อเดิม นามสกุล]=[ชื่อใหม่ นามสกุล]"
"""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document


if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def replace_in_paragraph(paragraph, replacements: dict[str, str]) -> int:
    """If paragraph text contains any old string, rebuild paragraph with replacement.

    Collapses runs (loses intra-paragraph formatting) — acceptable for name lines
    where formatting is uniform. Returns count of replacements made.
    """
    full = paragraph.text
    changed = 0
    new_full = full
    for old, new in replacements.items():
        if old in new_full:
            new_full = new_full.replace(old, new)
            changed += 1
    if changed and new_full != full:
        for r in paragraph.runs:
            r.text = ""
        if paragraph.runs:
            paragraph.runs[0].text = new_full
        else:
            paragraph.add_run(new_full)
    return changed


def replace_in_tables(tables, replacements: dict[str, str]) -> int:
    count = 0
    for t in tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    count += replace_in_paragraph(p, replacements)
    return count


def replace_all(doc, replacements: dict[str, str]) -> int:
    count = 0
    # Body paragraphs + tables
    for p in doc.paragraphs:
        count += replace_in_paragraph(p, replacements)
    count += replace_in_tables(doc.tables, replacements)
    # Section headers + footers (paragraphs + tables)
    for section in doc.sections:
        for hf in (section.header, section.footer,
                   section.first_page_header, section.first_page_footer,
                   section.even_page_header, section.even_page_footer):
            for p in hf.paragraphs:
                count += replace_in_paragraph(p, replacements)
            count += replace_in_tables(hf.tables, replacements)
    return count


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    doc_path = Path(sys.argv[1])
    replacements: dict[str, str] = {}
    for pair in sys.argv[2:]:
        if "=" in pair:
            old, _, new = pair.partition("=")
            replacements[old.strip()] = new.strip()
    if not doc_path.exists():
        print(f"ERROR: {doc_path} not found")
        return 1

    doc = Document(doc_path)
    n = replace_all(doc, replacements)
    doc.save(doc_path)
    print(f"Replaced {n} occurrence(s) in {doc_path.name}")
    for old, new in replacements.items():
        print(f"  '{old}' -> '{new}'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
