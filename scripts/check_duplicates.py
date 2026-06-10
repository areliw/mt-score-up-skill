#!/usr/bin/env python3
"""
ตรวจ "ของซ้ำ/ทับซ้อน" ข้าม skills (overlap report) — ไม่ใช่ตัวลบอัตโนมัติ.

ทำไมต้องมี: ที่ 87 skills ความเสี่ยงคือมีคู่ที่เนื้อหาทับกันจนผู้ใช้สับสนว่าจะ
route ไปตัวไหน. สคริปต์นี้คำนวณความเหมือนของ "body" (เนื้อหลังตัด frontmatter)
ทุกคู่ แล้ว flag คู่ที่คล้ายกันเกิน threshold ออกมาให้คน "ดูด้วยตา".

วิธีวัด (language-agnostic — รองรับไทยที่ไม่มีเว้นวรรค):
    character n-gram (n=3) Jaccard similarity บน body ที่ normalize แล้ว
    (lower + ตัด markdown/เครื่องหมายวรรคตอน เหลือแต่ตัวอักษร/ตัวเลข).
    n-gram ระดับตัวอักษรใช้ได้ทั้งไทยและอังกฤษ ไม่ต้องตัดคำ ไม่ต้องพึ่งไลบรารีนอก.

⚠️ สำคัญ: score สูง = "ดูด้วยตา" ไม่ใช่ "ลบอัตโนมัติ".
   บางคู่ใกล้กันโดยตั้งใจ (เช่น data-project-survival ↔ data-science-workflow ที่จง
   ใจแยกเป็นคนละ boundary, หรือ bloodbank ↔ clinical-correlation ที่แชร์ศัพท์แล็บ).
   คนรีวิวเป็นผู้ตัดสิน merge / graft / ปล่อยไว้ — ไม่ใช่สคริปต์.

วิธีรัน:
    python scripts/check_duplicates.py                 # รายงาน top คู่ที่คล้าย (>= threshold)
    python scripts/check_duplicates.py --top 15        # จำกัด 15 คู่บนสุด
    python scripts/check_duplicates.py --threshold 0.30  # ลด/เพิ่มเส้น flag (default 0.22)
    python scripts/check_duplicates.py --json          # output JSON (สำหรับ CI / เครื่องอ่าน)
    python scripts/check_duplicates.py --fail-over 0.6 # exit 1 ถ้ามีคู่ score เกิน 0.6 (gate CI)

exit code: 0 เสมอ (เป็น report ไม่ fail build) — ยกเว้นใส่ --fail-over แล้วมีคู่เกินค่านั้น → exit 1.
stdlib ล้วน · Python 3.8+ · ไม่มี dependency ภายนอก (เหมือน recheck_standards.py / build_triage.py).
"""
from __future__ import annotations

import argparse
import json
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
SKIP = {"README.md", "INDEX.md"}
NGRAM = 3
# 0.22 calibrated to Thai char-3gram Jaccard บน body จริง: คู่ที่ทับซ้อนสุดในคลังปัจจุบัน
# อยู่ ~0.27 (Thai ไม่มี space → n-gram overlap ต่ำกว่าอังกฤษโดยธรรมชาติ). 0.22 = เห็นคู่
# ที่ควรดู ~28 คู่ โดยไม่ท่วม noise. ปรับได้ด้วย --threshold. (0.35 = แทบไม่ flag อะไรเลย)
DEFAULT_THRESHOLD = 0.22
SPEC_HINT = "docs/skill-registry-spec.md §4 (merge play / graft)"


def skill_files() -> list[Path]:
    return [f for f in sorted(SKILLS.glob("*.md")) if f.name not in SKIP]


def strip_frontmatter(text: str) -> str:
    """ตัดบล็อก YAML frontmatter (--- ... ---) หัวไฟล์ออก เหลือเฉพาะ body."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            # ข้ามบรรทัด '---' ปิด ไปจุดเริ่ม body
            nl = text.find("\n", end + 1)
            return text[nl + 1:] if nl != -1 else ""
    return text


def normalize(text: str) -> str:
    """
    ลด body ให้เหลือ 'ตัวอักษร/ตัวเลขล้วน' เพื่อเทียบความเหมือนแบบ language-agnostic:
      - ตัด code block / inline code (โครงโค้ดทำให้คู่ที่ไม่เกี่ยวดูคล้ายกันลวงๆ)
      - ตัด markdown syntax + เครื่องหมายวรรคตอน + ช่องว่างทั้งหมด
      - lowercase
    ผลลัพธ์เป็นสตริงตัวอักษรไทย/อังกฤษ/ตัวเลขติดกัน → ใช้ทำ char n-gram ได้ทั้งสองภาษา.
    """
    text = re.sub(r"```.*?```", " ", text, flags=re.S)  # fenced code
    text = re.sub(r"`[^`]*`", " ", text)                # inline code
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links/images → keep label
    text = text.lower()
    # เก็บเฉพาะตัวอักษร (รวมไทย ผ่าน \w ที่ unicode) และตัวเลข — ทิ้งที่เหลือ
    text = re.sub(r"[^0-9a-z฀-๿]+", "", text)
    return text


def char_ngrams(s: str, n: int = NGRAM) -> set[str]:
    if len(s) < n:
        return {s} if s else set()
    return {s[i:i + n] for i in range(len(s) - n + 1)}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a) + len(b) - inter
    return inter / union if union else 0.0


def load_profiles() -> list[tuple[str, set[str]]]:
    """คืน [(skill_name, ngram_set), ...] — อ่านครั้งเดียว ทำ n-gram ครั้งเดียวต่อไฟล์."""
    profiles = []
    for f in skill_files():
        body = strip_frontmatter(f.read_text(encoding="utf-8"))
        grams = char_ngrams(normalize(body))
        profiles.append((f.stem, grams))
    return profiles


def pairwise(profiles: list[tuple[str, set[str]]], threshold: float) -> list[tuple[str, str, float]]:
    pairs = []
    for i in range(len(profiles)):
        name_a, grams_a = profiles[i]
        if not grams_a:
            continue
        for j in range(i + 1, len(profiles)):
            name_b, grams_b = profiles[j]
            if not grams_b:
                continue
            score = jaccard(grams_a, grams_b)
            if score >= threshold:
                pairs.append((name_a, name_b, score))
    pairs.sort(key=lambda p: p[2], reverse=True)
    return pairs


def render_text(pairs, threshold, top, n_skills) -> str:
    shown = pairs[:top] if top else pairs
    lines = [
        f"# overlap report — {n_skills} skills · char-{NGRAM}gram Jaccard · threshold {threshold:.2f}",
        "",
    ]
    if not pairs:
        lines.append(f"ไม่พบคู่ที่ similarity ≥ {threshold:.2f} — ไม่มี overlap ที่ต้องดู ✓")
        return "\n".join(lines)

    lines.append(f"พบ {len(pairs)} คู่ที่ similarity ≥ {threshold:.2f}"
                 + (f" (แสดง top {len(shown)})" if top and len(pairs) > top else "") + ":")
    lines.append("")
    width = max(len(a) for a, _b, _s in shown)
    for a, b, s in shown:
        lines.append(f"  {s:.3f}  {a:<{width}}  ↔  {b}")
    lines.append("")
    lines.append("→ คู่ score สูง = พิจารณา merge / graft (ดู " + SPEC_HINT + ")")
    lines.append("  ⚠️ ดูด้วยตา ไม่ใช่ลบอัตโนมัติ — บางคู่ใกล้กันโดยตั้งใจ (คนละ boundary).")
    return "\n".join(lines)


def render_json(pairs, threshold, top, n_skills) -> str:
    shown = pairs[:top] if top else pairs
    payload = {
        "skills_scanned": n_skills,
        "method": f"char-{NGRAM}gram-jaccard",
        "threshold": threshold,
        "flagged_pairs": len(pairs),
        "advice": "score สูง = พิจารณา merge/graft (ดู " + SPEC_HINT + ") — ดูด้วยตา ไม่ใช่ลบอัตโนมัติ",
        "pairs": [{"a": a, "b": b, "score": round(s, 4)} for a, b, s in shown],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="รายงานคู่ skills ที่เนื้อหาทับซ้อน (char-3gram Jaccard). report-only — ไม่ลบอะไร."
    )
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                    help=f"เส้น similarity ที่จะ flag (default {DEFAULT_THRESHOLD})")
    ap.add_argument("--top", type=int, default=0,
                    help="แสดงเฉพาะ N คู่บนสุด (0 = ทั้งหมด)")
    ap.add_argument("--json", action="store_true", help="output เป็น JSON (สำหรับ CI)")
    ap.add_argument("--fail-over", type=float, default=None, metavar="SCORE",
                    help="exit 1 ถ้ามีคู่ score เกินค่านี้ (ใช้ gate CI); ไม่ใส่ = exit 0 เสมอ")
    args = ap.parse_args()

    profiles = load_profiles()
    n_skills = len(profiles)
    pairs = pairwise(profiles, args.threshold)

    if args.json:
        print(render_json(pairs, args.threshold, args.top, n_skills))
    else:
        print(render_text(pairs, args.threshold, args.top, n_skills))

    if args.fail_over is not None:
        over = [p for p in pairs if p[2] > args.fail_over]
        if over:
            if not args.json:
                print(f"\n[FAIL] {len(over)} คู่ score เกิน --fail-over {args.fail_over} → exit 1",
                      file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
