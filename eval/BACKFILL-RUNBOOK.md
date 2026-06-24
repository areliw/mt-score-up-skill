# BACKFILL-RUNBOOK — ปิดช่อง full-tier A/B ที่ยังขาด

> ไทยก่อน · ใช้เมื่อ `eval/coverage-gap.md` ยังมี 🟡 SCREEN-only / 🟠 MANUAL-only / 🔴 NONE  
> **ห้าม** manual same-model A/B ในแชทเดียว — ดู [`ANTI-BIAS-PROTOCOL.md`](ANTI-BIAS-PROTOCOL.md)

## สถานะหลัง PR นี้ (2026-06-24)

- **94 skills** ทั้งหมด
- **94 full-tier** ใน `eval/_ab_slim.json` (backfill 18 แถวจาก `round6-probe.md`)
- **0** screen-only / manual-only / NONE ที่ยังขาด full-tier
- ไฟล์ batch: [`harness/backfill-screen-only.json`](harness/backfill-screen-only.json) — `remaining_gaps: 0` (เก็บไว้เป็น template เมื่อ skill ใหม่เข้ามา)

---

## เมื่อมีช่องใหม่ (skill ใหม่ หรือ body hash stale)

### 1) ดูว่าขาดอะไร

```bash
python scripts/maturity_report.py
python scripts/ab_gate_check.py --all
python scripts/refresh_coverage_gap.py   # อัปเดต coverage-gap.md + backfill JSON
```

### 2) ลำดับ backfill (ไม่ bias)

1. **ค้น evidence เก่าก่อน** — `eval/round6-probe.md`, `round4-new-skills.md`, `round5-remaining.md`  
   ถ้ามี full blind-judge ×3 บันทึกไว้ → append `_ab_slim` ด้วย `"tier":"full"`, `"method":"x3"`, `"run":"round6-probe"` (หรือ `wf_…`)  
   **อย่า** copy จาก `manual-ab-*.md` เป็น full-tier
2. **ที่เหลือ** → รัน harness จริง (ขั้นตอน 3–5)

### 3) รัน harness (Python CLI — แนะนำ)

จาก repo root (Cursor terminal / Codex / local):

```bash
pip install -r requirements-dev.txt
export ANTHROPIC_API_KEY=…

# ทีละ skill
python scripts/ab_harness.py --skill foo-judgment --reps 3 --append-slim

# batch จาก config (เมื่อ backfill JSON มี targets)
python scripts/ab_harness.py --config eval/harness/backfill-screen-only.json --reps 3 --append-slim
```

Dry-run (ไม่ต้องมี API key): `--dry-run`

Protocol: [`harness/PROTOCOL.md`](harness/PROTOCOL.md) · Adapters: [`harness/README.md`](harness/README.md)

#### ทางเลือก: Claude Code Workflow

เปิด repo ใน Claude Code แล้วรัน Workflow (ไม่ใช่ `node`):

```javascript
Workflow({
  scriptPath: 'eval/harness/ab-x3.js',
  args: [{
    skill: 'foo-judgment',
    file: 'skills/foo-judgment.md',
    focus: "the skill's own #1 anti-pattern"
  }]
})
```

- **Answerer = Haiku** · **Judge = Opus แยก** · blind + สลับลำดับ A/B  
- **×3** = screen · **×5** ก่อน promote/cut/rewrite  
- Clinical (🩸) = วัดอย่างเดียว — ห้ามแก้เนื้อจาก eval โดยไม่ peer-review

### 4) Append ผลลง `_ab_slim.json`

ตัวอย่างแถวที่ gate ยอมรับ:

```json
{
  "skill": "foo-judgment.md",
  "effect": "lift",
  "withScore": 4.0,
  "withoutScore": 2.0,
  "delta": 2.0,
  "trapAvoid": "with-only",
  "method": "x3",
  "tier": "full",
  "run": "wf_<workflow-id>",
  "note": "Haiku+Opus blind harness"
}
```

Checklist: [`ANTI-BIAS-PROTOCOL.md`](ANTI-BIAS-PROTOCOL.md) §6

### 5) Rebuild + verify

```bash
python scripts/build_ab_coverage.py
python scripts/ab_gate_check.py --all
python scripts/validate_repo.py
pytest
python scripts/refresh_coverage_gap.py
git add eval/_ab_slim.json eval/ab-coverage.json eval/coverage-gap.md eval/harness/backfill-screen-only.json
git commit -m "eval: append full-tier A/B for …"
```

---

## แบ่ง batch (แนะนำเมื่อ gaps > 0)

| Batch | ขนาด | เหตุผล |
|---|---|---|
| Probe | 1–2 skill | ยืนยัน harness ก่อน fan-out |
| Fan-out | 8–10 / ครั้ง | คุม token · ดู regression เร็ว |
| Clinical | แยก batch | flag-only · ไม่ auto-promote |

---

## อ้างอิง

- วิธีวัด: [`METHOD.md`](METHOD.md) Layer 2  
- Gate PR: [`AB-GATE.md`](AB-GATE.md)  
- ช่องว่างรายตัว: [`coverage-gap.md`](coverage-gap.md)  
- Round 6 raw: [`round6-probe.md`](round6-probe.md)
