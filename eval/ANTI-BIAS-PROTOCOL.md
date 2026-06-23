# ANTI-BIAS-PROTOCOL — วิธีวัด A/B ที่ gate ยอมรับ

> สั้น · ไทยก่อน · ใช้ก่อน append แถวใหม่ใน `eval/_ab_slim.json`

## ทำไมต้องมี tier

ผล A/B ที่ **answerer กับ judge เป็นโมเดล/เซสชันเดียวกัน** หรือ **ไม่ blind** มักได้ Δ สูงเกินจริง (เช่น 6/6 rescued +3 ใน manual session 2026-06-24) — ใช้คัดแยg ทิศทางได้ แต่ **ห้ามนับเป็น full evidence** สำหรับ `semi-stable`

Gate อ่าน field **`tier`** ใน `_ab_slim.json`:

| tier | ความหมาย | ใช้ promote `semi-stable`? |
|---|---|---|
| **`full`** | harness blind-judge (Opus gen → Haiku ×3 → Opus judge, สลับลำดับ) | ✅ ใช่ |
| **`screen`** | แถว screen ใน `_ab_slim` (หายาก) | ❌ ไม่ — ใช้ round4/5 markdown แทน |
| **`manual`** | same-session / same-model manual | ❌ ไม่ — exploratory เท่านั้น |

Legacy แถวไม่มี `tier` → infer จาก `method`: `manual*` → `manual` · `x3`/`x5`/ไม่มี → `full`

---

## 1) ทำไมต้อง Haiku เป็น answerer

สกิลเขียนให้ **MT จบใหม่ / โมเดลอ่อน** — frontier model รู้ judgment อยู่แล้ว → with/without แทบไม่ต่าง (null result). Haiku จึงเป็น **control arm ที่มีสัญญาณ** ตาม `eval/METHOD.md` Layer 2

## 2) ทำไมต้อง blind judge + สลับลำดับ

Judge ที่รู้ว่าอันไหน “มีสกิล” จะให้คะแนนสูงกว่าโดยไม่รู้ตัว — harness ใช้ Opus แยกจาก Haiku และ **สลับ A/B ต่อ rep** (`ab-x3.js`)

## 3) ทำไม ×3 ขั้นต่ำ · ×5 ก่อนตัดสินใจ

คะแนน 0–5 มี variance สูง → **×3 = screen** (คัด rescued ชัดจาก tie) · **×5 = act** ก่อน promote/cut/rewrite · ขอบเขตใช้ **Δ ≥ 2·SE(Δ)** ไม่ใช่เลข magic 1.4

## 4) ทำไม manual same-model = tier `manual` เท่านั้น

Composer/Opus ทั้งตอบและให้คะแนนในเซสชันเดียว → ไม่ blind · weak MT ถูก **เขียนให้ตกหลุม** → Δ สูงเกินจริง  
บันทึกได้ใน `eval/manual-ab-*.md` + `_ab_slim` ด้วย `"tier": "manual"`, `"method": "manual-screen"` — **ไม่นับ semi-stable**

---

## 5) คำสั่ง harness ที่ไม่ bias (Claude Code Workflow)

```javascript
Workflow({
  scriptPath: 'eval/harness/ab-x3.js',
  args: [
    {
      skill: 'foo-judgment',
      file: 'skills/foo-judgment.md',
      focus: "the skill's own #1 anti-pattern"
    }
  ]
})
```

ก่อน **promote / cut / rewrite** ใช้ `reps: 5`:

```javascript
Workflow({
  scriptPath: 'eval/harness/ab-x3.js',
  args: { targets: [/* ... */], reps: 5 }
})
```

---

## 6) Checklist ก่อน append `_ab_slim.json`

- [ ] รันผ่าน `eval/harness/ab-x3.js` (ไม่ใช่ manual ในแชทเดียว)
- [ ] Answerer = **Haiku** · Judge = **Opus แยก** · blind + order swap
- [ ] **×3 ขึ้นไป** (×5 ถ้าจะ act)
- [ ] `"tier": "full"` · `"method": "x3"` หรือ `"x5"` · `"run": "wf_…"`
- [ ] ไม่ overwrite แถว `tier: full` ด้วย manual — ใส่ manual เป็นแถวแยก `tier: manual`
- [ ] `python scripts/build_ab_coverage.py` แล้ว commit `ab-coverage.json`

---

## อ้างอิง

- วิธีวัดเต็ม: [`METHOD.md`](METHOD.md) Layer 2  
- Gate PR: [`AB-GATE.md`](AB-GATE.md)  
- ตัวอย่าง manual ที่ **superseded**: [`manual-ab-2026-06-24.md`](manual-ab-2026-06-24.md)
