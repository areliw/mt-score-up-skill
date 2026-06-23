# coverage-gap — A/B eval สถานะจริงต่อ skill

> Regenerated 2026-06-24 โดย `scripts/refresh_coverage_gap.py` + `maturity_report.py` / `ab_gate_check.py --all` logic.
> Library: **94 skills** · evidence tiers อ่านจาก `eval/_ab_slim.json` (`tier`: full / manual / screen) + round4/5 screen corpus.
> **นี่คือ source of truth ของงาน scale — อัปเดตหลัง merge skill ใหม่หรือ append _ab_slim.**

## สรุป 4 ชั้น (post tier system)

| tier | นิยาม | จำนวน | งานที่ต้องทำ |
|---|---|---|---|
| 🟢 **FULL** | `tier:full` ใน `_ab_slim` — harness blind-judge (Haiku ×3 + Opus judge) | **94** | — (promote ได้ถ้า Δ + codex ผ่าน) |
| 🟡 **SCREEN-only** | มี round4/5 screen แต่ **ยังไม่มี** full-tier row | **0** | รัน `ab-x3.js` → append `_ab_slim` tier full |
| 🟠 **MANUAL-only** | `_ab_slim` มีแต่ `tier:manual` (same-session — ห้าม promote) | **0** | re-run harness ตาม `ANTI-BIAS-PROTOCOL.md` |
| 🔴 **NONE** | ไม่มี A/B record ใดๆ ใน eval/ | **0** | **รันก่อน (urgent)** |

## 🟢 FULL — มี full-tier evidence

**94** skills — ดู `eval/ab-coverage.json` / `ab-scorecard.md` สำหรับ Δ รายตัว.

## หมายเหตุ

- Gate PR: `python scripts/ab_gate_check.py --all` ต้องผ่าน (ทุก skill มี `_ab_slim` row)
- Promote `semi-stable`: ต้อง **full-tier** เท่านั้น — ดู `eval/ANTI-BIAS-PROTOCOL.md`
- Screen round4/5 = safety check ไม่ใช่ blind-judge — อย่าใช้ promote โดยตรง
- หลัง append `_ab_slim`: `python scripts/build_ab_coverage.py` แล้ว commit `ab-coverage.json`
