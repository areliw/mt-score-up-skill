#!/usr/bin/env python3
"""Regenerate synthesis/INDEX.md from the frontmatter of synthesis/*.md theses.

synthesis/ is the L3-over-domain-signals layer (vs eval/INSIGHTS.md = L3-over-A/B-metrics):
cross-signal reads of the MT world that no single skill holds. This keeps a generated,
non-drifting index — same deterministic, stdlib-only, no-AI pattern as build_triage.py.
Run after adding/editing a thesis: `python scripts/build_synthesis_index.py` (commit the result).
"""
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SYN = ROOT / "synthesis"
SKIP = {"README", "INDEX"}

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def frontmatter(text: str) -> dict:
    fm = {}
    if not text.startswith("---"):
        return fm
    end = text.find("\n---", 3)
    if end == -1:
        return fm
    for line in text[3:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def main() -> int:
    theses = []
    for p in sorted(SYN.glob("*.md")):
        if p.stem in SKIP:
            continue
        fm = frontmatter(p.read_text(encoding="utf-8", errors="ignore"))
        if fm.get("thesis"):
            theses.append((p.name, fm))

    lines = [
        "# Synthesis INDEX (generated — do not edit by hand)",
        "",
        "> Regenerate with `python scripts/build_synthesis_index.py`. "
        "Source of truth = the frontmatter of `synthesis/*.md`.",
        "",
        f"{len(theses)} thesis · L3-over-domain-signals (cross-signal reads no single skill holds).",
        "",
        "| thesis | สถานะ | signals | confidence | feeds | date |",
        "|---|---|---|---|---|---|",
    ]
    for name, fm in theses:
        lines.append(
            f"| [{fm.get('title', fm['thesis'])}]({name}) "
            f"| {fm.get('status', '?')} | {fm.get('signals', '?')} "
            f"| {fm.get('confidence', '?')} | {fm.get('feeds', '—')} | {fm.get('date', '?')} |"
        )
    (SYN / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"build_synthesis_index: {len(theses)} thesis -> synthesis/INDEX.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
