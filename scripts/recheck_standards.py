#!/usr/bin/env python3
"""
Standards recheck — fetch current published edition from iso.org and refresh
STANDARDS.md date stamps on a clean run. A newer edition is NOT auto-applied:
the script leaves STANDARDS.md untouched and signals for human review, so a
fresh "verified" date is never stamped over an un-applied edition change.

Exit codes:
    0 = clean run, current editions confirmed — date stamps refreshed
    1 = error (page unreachable / HTML pattern changed) — workflow opens issue;
        date stamps NOT refreshed (never stamp "verified" on a failed check)
    2 = newer edition detected — STANDARDS.md left unchanged; workflow opens an
        issue/PR for human review (no silent auto-commit)

Run: python scripts/recheck_standards.py [--dry-run]
"""

import datetime
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
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
        # iso.org stage 90.92 "International Standard to be revised" (revision opened
        # 2025-11-28); the 2020 edition is still the current published one. Acknowledged on
        # human review 2026-06-11 so the monthly recheck doesn't re-flag this known state.
        # Drop/update this line when a new edition publishes or the stage advances.
        "known_stage": "90.92",
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


_VOID_TAGS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
})
_STAGE_TITLE_RE = re.compile(
    r"international standard (?:published|to be revised|withdrawn|confirmed|under review)"
    r"|withdrawal of international standard"
)


class _StageBlockParser(HTMLParser):
    """Collect the text of ONLY the element whose ``id="stageId"`` (including its nested tags),
    so stage parsing can never spill into the page-wide ``#lifecycle`` legend or other markup.
    Depth tracking ignores void tags so an unclosed ``<img>``/``<br>`` can't unbalance it."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._depth = 0
        self.text_parts = []

    def handle_starttag(self, tag, attrs):
        if self._depth:
            if tag not in _VOID_TAGS:
                self._depth += 1
        elif dict(attrs).get("id") == "stageId":
            self._depth = 1

    def handle_endtag(self, tag):
        if self._depth and tag not in _VOID_TAGS:
            self._depth -= 1

    def handle_data(self, data):
        if self._depth:
            self.text_parts.append(data)


def _active_stage(html: str):
    """Return ``(title, code)`` of the standard's ACTIVE lifecycle stage, read from the text of
    iso.org's ``id="stageId"`` element — e.g. ``Stage : International Standard to be revised
    [90.92]`` -> ``("International Standard to be revised", "90.92")``. Returns ``(None, None)``
    if the element is absent, carries no bracketed ``[code]``, names more than one stage, or is
    implausibly long (an unclosed block that would otherwise swallow the rest of the page).

    The element is ISOLATED with an HTML parser before parsing — never a free-text scan of the
    whole page — so it cannot drift into the page-wide ``#lifecycle`` legend (which lists every
    stage for every standard) or a link to another standard. A global phrase match used to flag
    even a Published standard (false positive); a proximity window missed the active banner ~1.9k
    chars away (false negative) and could still reach an adjacent legend entry. Reading only the
    stageId element's own text removes both failure modes: anything unexpected yields
    ``(None, None)`` -> the caller emits an exit-1 "fix parser" signal, never a silent OK."""
    parser = _StageBlockParser()
    parser.feed(html)
    text = re.sub(r"\s+", " ", "".join(parser.text_parts)).strip()
    if not text or len(text) > 300:                 # absent, or an unclosed block that ran away
        return None, None
    if len(set(_STAGE_TITLE_RE.findall(text.lower()))) > 1:   # ambiguous: more than one stage
        return None, None
    code_m = re.search(r"\[\s*(\d{2}\.\d{2})", text)
    if not code_m:                                  # the active stage must carry its own [code]
        return None, None
    title = re.sub(r"^\s*Stage\s*:?\s*", "", text.split("[", 1)[0], flags=re.IGNORECASE).strip()
    return (title or None), code_m.group(1)


def check_source(source: dict) -> dict:
    try:
        html = fetch(source["url"])
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        return {"name": source["name"], "error": f"fetch failed: {e}"}

    matches = source["pattern"].findall(html)
    if not matches:
        return {"name": source["name"], "error": "edition pattern not found on page"}

    # Use the most recent year found on page — guards against stale entries.
    # key=int → numeric comparison (robust if a stray non-4-digit token is ever matched).
    detected_year = max(matches, key=int)

    # Close the silent false-OK gap: a pinned standard URL keeps serving its OWN edition
    # forever, so "detected==current" alone can't tell "still current" from "superseded but
    # not yet republished". iso.org signals a successor two ways — (a) a newer `ISO <n>:<year>`
    # reference (caught by max() above), or (b) the standard's lifecycle STAGE flipping from
    # "published" to "to be revised"/"withdrawn". Read (b) from the page's single ACTIVE stage
    # (the `id="stageId"` block) via _active_stage(), NOT from free-text phrases: every page
    # embeds a `#lifecycle` legend naming all stages, so a global match false-positived a
    # Published standard and a proximity window false-negatived an actively-revised one.
    active_title, active_code = _active_stage(html)
    if active_title is None:
        # Can't read the active stage — never stamp OK on a page we don't understand.
        return {
            "name": source["name"],
            "error": "active-stage block not found (iso.org layout changed — fix parser)",
        }
    title_low = active_title.lower()
    superseded = ("to be revised" in title_low) or ("withdraw" in title_low)
    # `known_stage` is a human-in-the-loop PIN (same pattern as current_year): once a reviewer
    # has seen the active stage they record its CODE, so the monthly workflow stops re-opening an
    # issue for that exact acknowledged stage. The pin acknowledges ONE specific code, so ANY
    # drift away from it must trip re-review — not only moves to "to be revised"/"withdrawn", but
    # also a move back to published/confirmed/under-review (which would otherwise stamp a fresh
    # "verified" date and silently bury the fact that the pin is now stale).
    known = source.get("known_stage")
    if known is not None:
        acknowledged = active_code == known   # pinned and still matching -> stay quiet
        pin_drift = not acknowledged          # pinned but the stage moved -> stale, re-review
        stage_alarm = pin_drift
    else:
        acknowledged = False
        pin_drift = False
        stage_alarm = superseded              # un-pinned: only revised/withdrawn is an alarm
    changed = (detected_year != source["current_year"]) or stage_alarm

    return {
        "name": source["name"],
        "current_year": source["current_year"],
        "detected_year": detected_year,
        "active_stage": f"{active_title} [{active_code}]" if active_code else active_title,
        "active_code": active_code,
        "known_stage": known,
        "superseded": superseded,
        "acknowledged": acknowledged,
        "pin_drift": pin_drift,
        "changed": changed,
    }


def update_file(results: list, dry_run: bool) -> bool:
    """Refresh STANDARDS.md date stamps. Call ONLY on a clean run — never when an
    edition change is pending, or the fresh date would mask staleness."""
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
            reasons = []
            if r["detected_year"] != r["current_year"]:
                reasons.append(
                    f"new edition :{r['detected_year']} (file :{r['current_year']})"
                )
            if r.get("pin_drift"):
                reasons.append(
                    f"stage drifted from acknowledged [{r.get('known_stage')}] "
                    f"-> {r.get('active_stage')}"
                )
            elif r.get("superseded"):
                reasons.append(f"stage -> {r.get('active_stage', 'revision/withdrawal')}")
            if not reasons:  # never emit an empty reason
                reasons.append(f"stage {r.get('active_stage')}")
            print(f"  [NEW] {r['name']}: " + " · ".join(reasons))
            has_change = True
        elif r.get("acknowledged"):
            print(
                f"  [ACK] {r['name']}: edition :{r['detected_year']} still current; "
                f"known stage {r.get('active_stage')} (acknowledged, not re-flagged)"
            )
        else:
            print(
                f"  [OK]  {r['name']}: confirmed :{r['detected_year']} "
                f"({r.get('active_stage', '')})"
            )

    # A detected edition change must NOT silently rewrite STANDARDS.md or refresh the
    # "last verified" stamp — that would mask staleness. Leave the file untouched and
    # signal for human review (the workflow opens an issue/PR on exit 2).
    if has_change:
        print(
            "\n[ACTION] Newer edition detected — STANDARDS.md left unchanged.\n"
            "         A human must verify the edition, update STANDARDS.md, and bump\n"
            "         current_year in this script via PR."
        )
        return 2

    # On a fetch/parse error, do NOT refresh date stamps — stamping "verified" when a
    # source was unreachable would itself mask staleness.
    if has_error:
        return 1

    update_file(results, dry_run=dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
