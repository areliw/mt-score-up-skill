# SCALE-PLAN — ขยาย Layer-2 A/B ให้ครอบทั้งคลัง (53 → 89)

> เป้า: เปลี่ยน eval จาก "วัดครั้งเดียว 53 ตัว" เป็น **benchmark ยืนที่ทุก skill มีเลข lift กำกับ** —
> เพื่อให้คำว่า "รุ่นน้องไม่โดนเจื๋อน" มีหลักฐาน ไม่ใช่ vibes. นี่คือ moat + วัตถุดิบ thesis.
> Harness เดิม (`METHOD.md` Layer 2) ดีอยู่แล้ว — แผนนี้ **ขยาย ไม่รื้อ**.

## สถานะตอนนี้ (กับดักที่ต้องปิด)

- Full blind-judge A/B: **53 ตัว** (v0.2 era) · คลังตอนนี้ **89** → ~36 ยังไม่ผ่าน full eval
- ที่เพิ่มมาหลัง v0.2: round4/5 ได้แค่ **spot-A/B screen** (เบากว่า) · ตัวใหม่สุดบางตัว (เช่น `git-workflow-judgment`) **ยังไม่ test เลย**
- noise floor = **~1.4** (per-skill Δ ต้องเกินนี้ถึงนับเป็นสัญญาณจริง — จาก round3 2-run averaging)

---

## Phase 0 — หา "uncovered list" จริง (อย่าเดา)

**ก่อนรันอะไร:** diff รายชื่อใน `ab-scorecard.md` (53 ที่ test แล้ว) กับ `skills/INDEX.md` (89 ปัจจุบัน)
→ ได้ exact list ของตัวที่ยังขาด + แยกป้าย `never-tested` vs `spot-only`.
เขียนผลเป็น `eval/coverage-gap.md` (table: skill · last-A/B-round · status). **นี่คือ source of truth ของงาน**, ไม่ใช่ "~36" ลอยๆ.

## ขั้นที่ scale (reuse 4-step harness เดิม)

ต่อ 1 skill:
1. **Scenario gen** — strong model อ่าน skill → ดึง anti-pattern #1 → เขียน scenario ที่ bait กับดักนั้น (skill เลือก softball เองไม่ได้)
2. **Weak answerer ×2** — Haiku 4.5 ตอบ blind 2 ครั้ง: ไม่มี skill / มี skill วางหน้า
3. **Blind judge** — strong model คนละตัว ให้ 0–5 ด้าน trap-avoidance โดยไม่รู้ว่าอันไหนมี skill + ระบุ `trapAvoid`
4. **Classify** Δ = with − without → rescued/better/tie/style-cost/no-rescue/**regression**

## การตัดสินใจ scale (default ที่แนะนำ — เคาะได้)

| จุด | เดิม | แผนนี้ (แนะนำ) | เหตุผล |
|---|---|---|---|
| runs/skill | 1 (เก่า) → 2 (round3) | **3 runs averaging** | กด noise ต่ำกว่า 1.4, per-skill เชื่อได้ขึ้น |
| scenarios/skill | 1 (headline trap) | non-clinical = 1 · **clinical = 2** (+1 edge-case) | แก้ threat "clinical ties hide value" |
| weak model | Haiku | **Haiku 4.5** (+ optional 2nd weak model รอบ spot) | robustness ข้ามโมเดล |
| judge | strong, blind | **Opus 4.8 blind** + self-consistency 2 ครั้ง บนเคสที่ Δ ใกล้ noise floor | กัน judge variance |
| human check | ไม่มี | **spot 10-15% โดยคน** (rescued + regression ก่อน) | แก้ threat "judge เป็น LLM" |

## Automation = Workflow pipeline (ไม่ใช่มือ)

งานนี้ = fan-out over work-list → ใช้ **Workflow tool** (orchestrated A/B). โครง:

```
pipeline(uncoveredSkills,
  skill   => genScenario(skill),            // strong model
  scen    => parallel([answerNo, answerYes].map(haiku))   // weak ×2
  answers => judgeBlind(answers),           // strong, blind
  verdict => classify(verdict))             // Δ + taxonomy
→ append ลง ab-scorecard.md + เขียน round6.json
```

- คุม cost: concurrency cap ~10-16, schema-validated output ต่อ stage
- est. โหลด: 36 ตัว × (1 gen + 2 answer + 1 judge) × 3 runs ≈ **~430 LLM calls** (re-run ทั้ง 89 เพื่อ consistency ≈ ~1,070)
- ทุก stage เขียน checkpoint ไฟล์ (กู้ได้ถ้าหลุดกลางคัน)

## Phasing

1. **Phase 1 — non-clinical ~รอบ 36** (judgment/AI/career/data/stats) → ปลอดภัยสุด, ได้ headline ใหม่เร็ว
2. **Phase 2 — clinical (🩸)** → flag-only mindset, 2 scenarios/ตัว, ห้ามแก้เนื้อคลินิกจาก eval โดยไม่ peer-review
3. **Phase 3 — human spot-check** rescued+regression → ยกระดับความเชื่อ headline

## Standing benchmark (ทำให้เป็นจุดขาย ไม่ใช่ snapshot)

- **CI gate:** skill ใหม่/แก้ใหญ่ → ต้องมี A/B result ก่อน merge (wire เข้า `build_triage` / PR check)
- **Public scorecard:** ทุก skill โชว์ Δ + kind + วันที่วัด ใน `ab-scorecard.md` (+ badge ใน catalog)
- **Re-baseline policy:** โมเดลเปลี่ยน gen ใหม่ → re-run + เก็บ version (อย่าเทียบข้ามรุ่นโมเดลแบบมั่ว)

## Success criteria

- 89/89 มี Δ + kind + ≥3-run average · 0 ตัวเหลือ `never-tested`
- **regression = 0** ยังต้องจริง (อันที่ condemn skill)
- promote draft→semi-stable เฉพาะตัวที่: ผ่าน A/B (Δ ไม่ติดลบ + 0 regression) **และ** codex review — clinical ยังต้อง peer-review จริงถึงแตะ stable

## เลขที่ผมยังเดาไม่ได้ — ต้องพี่เคาะ

1. **Scope:** แค่ ~36 ที่ขาด หรือ **re-run ทั้ง 89** สด (คลังโต+โมเดลใหม่ → consistency ดีกว่า แต่ ~2.5× cost)?
2. **Compute route:** ยิงผ่าน **Workflow** (orchestrate ด้วย Claude session นี้, billed ที่นี่) หรือเขียน **standalone script + API key** (รันเองนอก session, คุม cost ตรง)?
3. **Budget เพดาน:** กี่ call/กี่บาท ที่ยอมได้ต่อรอบ — ผมจะ size fleet ตามนั้น
