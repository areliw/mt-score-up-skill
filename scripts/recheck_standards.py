#!/usr/bin/env python3
"""
Standards recheck — fetch current published edition from iso.org / aabb.org,
update STANDARDS.md if newer edition detected.

Exit codes:
    0 = success, no changes (Last verified date refreshed only)
    1 = error (e.g., page unreachable, HTML pattern changed) — workflow opens issue
    2 = changes detected (newer edition found) — workflow commits + pushes

Run: python scripts/recheck_standards.py [--dry-run]
"""

import datetime
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
STANDARDS_FILE = ROOT / "STANDARDS.md"
TODAY = datetime.date.today().isoformat()
NEXT_RUN = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()

# Sources to check — keep tight; add more carefully (each needs unique HTML pattern).
# Pattern uses ISO's universal naming convention `ISO <number>:<year>` which appears in
# both the page title and the `standard-reference` block — stable across iso.org redesigns.
SOURCES = [
    {
        "name": "ISO 15189",
        "url": "https://www.iso.org/standard/76677.html",
        "pattern": re.compile(r"ISO\s+15189:(\d{4})"),
        "current_year": "2022",
    },
    {
        "name": "ISO 15190",
        "url": "https://www.iso.org/standard/72191.html",
        "pattern": re.compile(r"ISO\s+15190:(\d{4})"),
        "current_year": "2020",
    },
]


def fetch(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "mt-score-up-skill-bot/1.0 "
                "(+https://github.com/areliw/mt-score-up-skill; "
                "monthly standards recheck)"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def check_source(source: dict) -> dict:
    try:
        html = fetch(source["url"])
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        return {"name": source["name"], "error": f"fetch failed: {e}"}

    matches = source["pattern"].findall(html)
    if not matches:
        return {"name": source["name"], "error": "edition pattern not found on page"}

    # Use the most recent year found on page — guards against stale entries
    # (the page lists the current edition first / most prominently)
    detected_year = max(matches)

    return {
        "name": source["name"],
        "current_year": source["current_year"],
        "detected_year": detected_year,
        "changed": detected_year != source["current_year"],
    }


def update_file(results: list, dry_run: bool) -> bool:
    text = STANDARDS_FILE.read_text(encoding="utf-8")
    new_text = text

    new_text = re.sub(
        r"\*\*Date:\*\*\s+\d{4}-\d{2}-\d{2}",
        f"**Date:** {TODAY}",
        new_text,
        count=1,
    )
    new_text = re.sub(
        r"\*\*Next scheduled recheck:\*\*\s+\d{4}-\d{2}-\d{2}",
        f"**Next scheduled recheck:** {NEXT_RUN}",
        new_text,
        count=1,
    )

    for r in results:
        if "error" in r:
            continue
        pattern = (
            rf"(\*\*{re.escape(r['name'])}\*\*[^\n]*?\|\s*)"
            r"\d{4}-\d{2}-\d{2}"
            r"(\s*\|)"
        )
        new_text = re.sub(pattern, rf"\g<1>{TODAY}\g<2>", new_text)

    if dry_run:
        print("DRY RUN — STANDARDS.md not written")
        return False

    if new_text == text:
        print("STANDARDS.md unchanged")
        return False

    STANDARDS_FILE.write_text(new_text, encoding="utf-8")
    print("STANDARDS.md updated")
    return True


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    print(f"Recheck date: {TODAY}\n")

    results = [check_source(s) for s in SOURCES]

    has_change = False
    has_error = False
    for r in results:
        if "error" in r:
            print(f"  [ERR] {r['name']}: {r['error']}")
            has_error = True
        elif r["changed"]:
            print(
                f"  [NEW] {r['name']}: file=:{r['current_year']} "
                f"page=:{r['detected_year']}"
            )
            has_change = True
        else:
            print(f"  [OK]  {r['name']}: confirmed :{r['detected_year']}")

    update_file(results, dry_run=dry_run)

    if has_change:
        return 2
    if has_error:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
