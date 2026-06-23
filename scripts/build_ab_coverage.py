#!/usr/bin/env python3
"""Build eval/ab-coverage.json — the maturity registry (item 1 of maturity-ladder.md).

For every skill records: status, a BODY hash (sha256 of the content after the frontmatter —
so editing `status:`/`last_edited:` does NOT invalidate evidence, only a real judgment change
does), and what evidence exists (full A/B in _ab_slim, light screen, signed peer-review).

`body_hash` is the **hash-currency anchor**: check_maturity_gate.py compares a skill's current
body hash to this; if they differ, the skill's body changed since its A/B was recorded → the
evidence is stale → re-test (run eval/harness/ab-x3.js) and rebuild this file.

NOTE on the baseline: this is a forward-looking reset stamped at build time. It does NOT claim a
legacy (v0.2) A/B used this exact body — it means "from now, any body edit flags stale." Re-running
this builder after a re-A/B re-anchors the hash.

Usage: python scripts/build_ab_coverage.py   (writes eval/ab-coverage.json)
"""
import sys
import json
import hashlib
import pathlib

from ab_tier import index_by_slug, infer_tier, load_rows, any_slugs

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
EVAL = ROOT / "eval"
OUT = EVAL / "ab-coverage.json"
SCREEN_FILES = ["round4-new-skills.md", "round5-remaining.md"]
PEER_DIR = EVAL / "peer-review"
SKIP = {"README", "INDEX"}

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def split_body(text: str) -> str:
    """Return the content after the YAML frontmatter (or the whole file if none)."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            nl = text.find("\n", end + 1)
            return text[nl + 1:] if nl != -1 else ""
    return text


def body_hash(text: str) -> str:
    body = split_body(text).strip()
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]


def status_of(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "?"


def ab_index() -> dict:
    idx = index_by_slug(load_rows())
    out = {}
    for slug, r in idx.items():
        out[slug] = {
            "delta": r.get("delta"),
            "method": r.get("method", "legacy"),
            "tier": infer_tier(r),
        }
    return out


def screen_corpus() -> str:
    parts = []
    for f in SCREEN_FILES:
        p = EVAL / f
        if p.exists():
            parts.append(p.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts)


def peer_signed() -> set[str]:
    out = set()
    if not PEER_DIR.exists():
        return out
    for p in PEER_DIR.glob("*.md"):
        if p.stem.upper() == "TEMPLATE":
            continue
        body = p.read_text(encoding="utf-8", errors="ignore")
        if "SIGN" in body:
            stem = p.stem
            out.add(stem.rsplit("-", 3)[0] if stem.count("-") >= 3 else stem)
    return out


def main() -> int:
    abi = ab_index()
    promo = {s: r for s, r in abi.items() if r.get("tier") == "full"}
    any_ab = any_slugs()
    screen = screen_corpus()
    signed = peer_signed()
    reg = {}
    for p in sorted(SKILLS.glob("*.md")):
        if p.stem in SKIP:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        slug = p.stem
        ab = abi.get(slug)
        full = promo.get(slug)
        reg[slug] = {
            "status": status_of(text),
            "body_hash": body_hash(text),
            "ab": slug in any_ab,
            "ab_full": bool(full),
            "ab_tier": (ab or {}).get("tier"),
            "ab_method": (full or ab or {}).get("method"),
            "ab_delta": (full or ab or {}).get("delta"),
            "screen": slug in screen,
            "peer": slug in signed,
        }
    OUT.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    n_full = sum(1 for v in reg.values() if v["ab_full"])
    n_manual = sum(1 for v in reg.values() if v["ab"] and not v["ab_full"])
    print(f"ab-coverage.json: {len(reg)} skills · full-tier {n_full} · manual-tier {n_manual} · screen-only {sum(1 for v in reg.values() if v['screen'] and not v['ab'])} · peer {sum(1 for v in reg.values() if v['peer'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
