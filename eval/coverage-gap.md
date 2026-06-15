# coverage-gap — A/B eval สถานะจริงต่อ skill (Phase 0 output)

> Generated 2026-06-15 โดย diff: `ab-scorecard.md` (full blind-judge 53) ·
> `round4-new-skills.md` (8) · `round5-remaining.md` (26) เทียบ `skills/*.md` บนดิสก์ (89 ตัว).
> validate แล้ว: ทุกชื่อ map ตรง slug จริง · 53+34+2 = 89 · ไม่มี dup.
> **นี่คือ source of truth ของงาน scale — ไม่ใช่ "~36" ลอยๆ.**

## สรุป 3 ชั้น

| tier | นิยาม | จำนวน | งานที่ต้องทำ |
|---|---|---|---|
| 🟢 **FULL** | full blind-judge (round 1-3): strong-gen scenario + Haiku ×2 + blind judge + Δ | **53** | — (มีเลขแล้ว ดู `ab-scorecard.md`) |
| 🟡 **SCREEN-only** | light screen (round 4-5): self-derived trap, single-pass, assessed ไม่ใช่ blind-judge | **34** | **upgrade → full blind-judge** (งานหลัก) |
| 🔴 **NONE** | ไม่เคย A/B เลย | **2** | **รันก่อน (urgent)** — ปิดรู zero-coverage |

> ข้อค้นพบที่เปลี่ยน premise: รูที่ "อันตราย" จริง (zero coverage) มีแค่ **2 ตัว** ไม่ใช่ 36.
> งาน scale ส่วนใหญ่ = **ยกระดับ 34 ตัวจาก screen → full rigor** (มี safety check แล้ว แต่ยังไม่มี Δ/blind-judge).

## 🔴 NONE — รันก่อน (2)

- `git-workflow-judgment`
- `interprofessional-communication-judgment`

## 🟡 SCREEN-only — upgrade เป็น full blind-judge (34)

ab-test-judgment · ai-coding-guardrails · data-science-workflow · debugging-judgment · deep-research ·
dx-company-brief · flow-cytometry-judgment · grill-my-plan · humanize-ai-writing ·
incident-postmortem-judgment · interactive-course · lab-clinic-business-judgment ·
lead-intelligence-judgment · literature-review-judgment · market-research-judgment ·
method-validation-stats · ml-engineering-workflow · mt-databases · phi-data-handling · poct-judgment ·
pomodoro-focus · preanalytical-judgment · prompt-optimizer · pubmed-search-judgment · report-up-judgment ·
source-credibility-judgment · spreadsheet-judgment · tdd-judgment · time-blocking · token-budget-judgment ·
urinalysis-judgment · verification-panel · write-a-skill · writing-judgment

## ลำดับงานที่แนะนำ (Phase 1)

1. **1a — probe:** รัน full A/B pipeline บน **2 NONE ก่อน** (probe-before-fanout) → ยืนยัน harness ทำงาน + ได้ผลจริง ก่อนยิงทั้ง batch
2. **1b — fanout:** upgrade **34 SCREEN-only** → full blind-judge (3-run averaging, clinical +1 edge-case)
3. clinical (🩸) ในกลุ่มนี้ = flag-only mindset, ห้ามแก้เนื้อจาก eval โดยไม่ peer-review

## หมายเหตุ

- 🟡 SCREEN-only ทั้ง 34 = round4/5 รายงาน **0 regression** อยู่แล้ว (ปลอดภัยที่จะโหลด) — การ upgrade คือเพื่อ **เลข Δ ที่ขายได้/promote ได้** ไม่ใช่เพราะสงสัยว่าอันตราย
- clinical หลายตัวใน round 1-3 ได้ `tie` เพราะ Haiku ตอบ textbook trap ถูกอยู่แล้ว → rescue จริงต้อง **human test กับรุ่นน้อง MT จริง** (limitation ที่ round4/5 ย้ำ) — เป็น layer ที่อยู่นอก A/B นี้
