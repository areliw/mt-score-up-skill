#!/usr/bin/env python3
"""Regenerate eval/coverage-gap.md + backfill round6 full-tier rows into _ab_slim.json.

Usage (repo root): python scripts/refresh_coverage_gap.py
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
EVAL = ROOT / "eval"
AB_SLIM = EVAL / "_ab_slim.json"
COVERAGE_GAP = EVAL / "coverage-gap.md"
BACKFILL_JSON = EVAL / "harness" / "backfill-screen-only.json"
SKIP = {"README", "INDEX"}

sys.path.insert(0, str(ROOT / "scripts"))
from ab_tier import full_slugs, index_by_slug, infer_tier, load_rows, manual_only_slugs  # noqa: E402

# round6-probe.md full blind-judge ×3 averages (Haiku answerer, Opus judge)
ROUND6: dict[str, dict] = {
    "git-workflow-judgment": {"delta": 2.0, "kinds": "rescued·better·better", "batch": "probe"},
    "ab-test-judgment": {"delta": 3.33, "kinds": "rescued·rescued·rescued", "batch": "B1"},
    "ai-coding-guardrails": {"delta": 2.67, "kinds": "rescued·better·better", "batch": "B1"},
    "data-science-workflow": {"delta": 1.67, "kinds": "better·better·better", "batch": "B1"},
    "deep-research": {"delta": 0.67, "kinds": "rescued·tie·tie", "batch": "B1-after-guard"},
    "dx-company-brief": {"delta": 0.33, "kinds": "tie·tie·better", "batch": "B1"},
    "grill-my-plan": {"delta": -0.33, "kinds": "tie·style-cost·tie", "batch": "B1"},
    "humanize-ai-writing": {"delta": 4.0, "kinds": "rescued·rescued·rescued", "batch": "B1"},
    "interactive-course": {"delta": 0.67, "kinds": "no-rescue·rescued·style-cost", "batch": "B1"},
    "method-validation-stats": {"delta": 1.33, "kinds": "better·better·better", "batch": "B3"},
    "ml-engineering-workflow": {"delta": 1.67, "kinds": "better·better·better", "batch": "B2"},
    "mt-databases": {"delta": 2.33, "kinds": "rescued·rescued·rescued", "batch": "B3"},
    "phi-data-handling": {"delta": 0.67, "kinds": "better·better·tie", "batch": "B3"},
    "pomodoro-focus": {"delta": 1.33, "kinds": "better·tie·rescued", "batch": "B2"},
    "prompt-optimizer": {"delta": 2.33, "kinds": "rescued·rescued·better", "batch": "B2"},
    "time-blocking": {"delta": 0.33, "kinds": "better·tie·tie", "batch": "B3"},
    "verification-panel": {"delta": 0.33, "kinds": "better·tie·tie", "batch": "B3"},
    "write-a-skill": {"delta": 0.0, "kinds": "better·tie·style-cost", "batch": "B3"},
}


def screen_corpus() -> str:
    parts = []
    for f in ("round4-new-skills.md", "round5-remaining.md"):
        p = EVAL / f
        if p.exists():
            parts.append(p.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts)


def extract_focus(slug: str) -> str:
    text = (SKILLS / f"{slug}.md").read_text(encoding="utf-8", errors="ignore")
    for pat in (
        r"กับดัก\s*#1[^:\n]*:\s*(.+)",
        r"กับดักข้อ\s*1:\s*(.+)",
        r"^-\s*#1\s+(.+)",
    ):
        m = re.search(pat, text, re.MULTILINE)
        if m:
            s = m.group(1).strip()
            return s[:200] if len(s) > 200 else s
    m = re.search(r"## กับดัก[^\n]*\n(?:-\s*)?#?1[.\s]+(.+)", text)
    if m:
        s = m.group(1).strip()
        return s[:200] if len(s) > 200 else s
    return "the skill's own #1 anti-pattern"


def infer_effect(delta: float, kinds: str) -> str:
    if "regression" in kinds:
        return "backfire"
    if delta < -0.5:
        return "backfire"
    if "rescued" in kinds and delta >= 1.0:
        return "rescued" if kinds.count("rescued") >= 2 else "lift"
    if delta >= 1.4:
        return "lift"
    if abs(delta) < 0.5:
        return "neutral"
    return "lift" if delta > 0 else "neutral"


def infer_trap(delta: float, kinds: str) -> str:
    if "rescued" in kinds and "regression" not in kinds:
        if kinds.count("rescued") >= 2:
            return "with-only"
    return "both"


def approx_scores(delta: float, trap: str) -> tuple[float, float]:
    """Rough with/without from delta for registry display."""
    if trap == "with-only":
        return round(3.0 + delta * 0.5, 2), round(1.5, 2)
    mid = 3.5
    return round(mid + delta / 2, 2), round(mid - delta / 2, 2)


def backfill_row(slug: str, meta: dict) -> dict:
    delta = meta["delta"]
    kinds = meta["kinds"]
    effect = infer_effect(delta, kinds)
    trap = infer_trap(delta, kinds)
    ws, wos = approx_scores(delta, trap)
    return {
        "skill": f"{slug}.md",
        "effect": effect,
        "withScore": ws,
        "withoutScore": wos,
        "delta": delta,
        "trapAvoid": trap,
        "method": "x3",
        "tier": "full",
        "run": "round6-probe",
        "note": f"Round6 {meta['batch']} — Haiku+Opus blind harness; backfilled from eval/round6-probe.md",
    }


def classify_skills() -> tuple[list, list, list, list, list]:
    fab = full_slugs()
    manual_only = manual_only_slugs() - fab
    screen = screen_corpus()
    skills = sorted(p.stem for p in SKILLS.glob("*.md") if p.stem not in SKIP)
    full_l, screen_l, manual_l, none_l, all_rows = [], [], [], [], []
    for slug in skills:
        has_full = slug in fab
        has_manual = slug in manual_only
        has_screen = slug in screen
        if has_full:
            tier = "full"
            full_l.append(slug)
        elif has_manual:
            tier = "manual"
            manual_l.append(slug)
        elif has_screen:
            tier = "screen"
            screen_l.append(slug)
        else:
            tier = "none"
            none_l.append(slug)
        all_rows.append((slug, tier))
    return full_l, screen_l, manual_l, none_l, all_rows


def write_coverage_gap(full_l, screen_l, manual_l, none_l, n_skills: int) -> None:
    today = date.today().isoformat()
    lines = [
        "# coverage-gap — A/B eval สถานะจริงต่อ skill",
        "",
        f"> Regenerated {today} โดย `scripts/refresh_coverage_gap.py` + `maturity_report.py` / `ab_gate_check.py --all` logic.",
        f"> Library: **{n_skills} skills** · evidence tiers อ่านจาก `eval/_ab_slim.json` (`tier`: full / manual / screen) + round4/5 screen corpus.",
        "> **นี่คือ source of truth ของงาน scale — อัปเดตหลัง merge skill ใหม่หรือ append _ab_slim.**",
        "",
        "## สรุป 4 ชั้น (post tier system)",
        "",
        "| tier | นิยาม | จำนวน | งานที่ต้องทำ |",
        "|---|---|---|---|",
        f"| 🟢 **FULL** | `tier:full` ใน `_ab_slim` — harness blind-judge (Haiku ×3 + Opus judge) | **{len(full_l)}** | — (promote ได้ถ้า Δ + codex ผ่าน) |",
        f"| 🟡 **SCREEN-only** | มี round4/5 screen แต่ **ยังไม่มี** full-tier row | **{len(screen_l)}** | รัน `ab-x3.js` → append `_ab_slim` tier full |",
        f"| 🟠 **MANUAL-only** | `_ab_slim` มีแต่ `tier:manual` (same-session — ห้าม promote) | **{len(manual_l)}** | re-run harness ตาม `ANTI-BIAS-PROTOCOL.md` |",
        f"| 🔴 **NONE** | ไม่มี A/B record ใดๆ ใน eval/ | **{len(none_l)}** | **รันก่อน (urgent)** |",
        "",
    ]
    if none_l:
        lines += ["## 🔴 NONE — รันก่อน", ""] + [f"- `{s}`" for s in none_l] + [""]
    if screen_l:
        lines += [
            "## 🟡 SCREEN-only — ต้อง upgrade เป็น full-tier",
            "",
            " · ".join(f"`{s}`" for s in screen_l),
            "",
        ]
    if manual_l:
        lines += [
            "## 🟠 MANUAL-only — exploratory เท่านั้น",
            "",
            " · ".join(f"`{s}`" for s in manual_l),
            "",
        ]
    lines += [
        "## 🟢 FULL — มี full-tier evidence",
        "",
        f"**{len(full_l)}** skills — ดู `eval/ab-coverage.json` / `ab-scorecard.md` สำหรับ Δ รายตัว.",
        "",
        "## หมายเหตุ",
        "",
        "- Gate PR: `python scripts/ab_gate_check.py --all` ต้องผ่าน (ทุก skill มี `_ab_slim` row)",
        "- Promote `semi-stable`: ต้อง **full-tier** เท่านั้น — ดู `eval/ANTI-BIAS-PROTOCOL.md`",
        "- Screen round4/5 = safety check ไม่ใช่ blind-judge — อย่าใช้ promote โดยตรง",
        "- หลัง append `_ab_slim`: `python scripts/build_ab_coverage.py` แล้ว commit `ab-coverage.json`",
        "",
    ]
    COVERAGE_GAP.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    rows = load_rows()
    existing = full_slugs(rows)
    appended = 0
    for slug, meta in ROUND6.items():
        if slug in existing:
            continue
        rows.append(backfill_row(slug, meta))
        appended += 1
    if appended:
        AB_SLIM.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"backfilled {appended} full-tier row(s) into _ab_slim.json")

    full_l, screen_l, manual_l, none_l, _ = classify_skills()
    n_skills = len(full_l) + len(screen_l) + len(manual_l) + len(none_l)
    write_coverage_gap(full_l, screen_l, manual_l, none_l, n_skills)

    gaps = screen_l + none_l + manual_l
    targets = [
        {
            "skill": s,
            "file": f"skills/{s}.md",
            "focus": extract_focus(s),
        }
        for s in sorted(gaps)
    ]
    BACKFILL_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated": date.today().isoformat(),
        "note": "Harness batch for skills lacking full-tier _ab_slim. Run via Claude Code Workflow only — NOT manual same-model A/B.",
        "protocol": "eval/ANTI-BIAS-PROTOCOL.md",
        "workflow": {
            "scriptPath": "eval/harness/ab-x3.js",
            "args": targets,
        },
        "remaining_gaps": len(gaps),
    }
    BACKFILL_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"coverage-gap.md: {n_skills} skills · full {len(full_l)} · screen-only {len(screen_l)} · manual-only {len(manual_l)} · none {len(none_l)}")
    print(f"backfill-screen-only.json: {len(gaps)} remaining gap(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
