# `synthesis/` — domain theses (the L3-over-signals layer)

> สิ่งที่ `skills/` เป็นต่อ **"รุ่นพี่ที่จำเคสได้"** · `synthesis/` เป็นต่อ **"รุ่นพี่ที่มองทะลุ"** —
> การอ่านโลก MT ที่ **ไม่มีสกิลเดี่ยวไหนถือได้** เพราะมันเกิดจาก *เชื่อม* signal หลายตัว ไม่ใช่จากเคสเดียว.

## ทำไมมีโฟลเดอร์นี้
`skills/` เก็บ **atom** (judgment ทีละเรื่อง) · `eval/` พิสูจน์ atom ด้วย A/B (เลข). แต่ insight ที่เกิดจาก
**เชื่อม signal หลายตัว** (เช่น *"ปัญหาราก MT = value-capture"* จาก 6 เธรด) **ไม่มี atom ไหนถือ** —
เดิมมันหายไปกับ chat. นี่คือ home ของมัน: เก็บแบบ versioned · กู้คืนได้ทุก session · ป้อนกลับให้ skills.

## รูปแบบ (1 thesis = 1 ไฟล์)
frontmatter → `## Claim` (1–2 ประโยค) → `## หลักฐาน` (signal ที่สังเคราะห์ — de-identified) →
`## นัย` (ระดับบุคคล/นโยบาย) → `## ป้อนอะไร` (skills/scope ที่ thesis ชี้) → `## คำถามเปิด`.

frontmatter keys: `thesis` · `title` · `status` · `signals` (จำนวน signal ที่สังเคราะห์) ·
`confidence` (low/medium/high) · `date` · `feeds` (สกิลที่ได้รับ insight นี้ คั่นด้วย comma).

## Intake: signal → thesis
1. รวบ signal **de-identified** ≥ จำนวนหนึ่ง (เธรด/เคส/ข้อมูล — ไม่อ้างกลุ่มปิด/บุคคล/quote)
2. สังเคราะห์: claim + หลักฐาน + confidence — **อย่า cherry-pick**; signal ที่ขัดกัน บันทึกใน `## คำถามเปิด`
3. เก็บเป็น `draft` → ป้อนให้ skills (ชี้ว่าควรเก็บ landmine/fork ไหนต่อ)
4. เจอ signal-set **อิสระ** ที่ยืนยัน → เลื่อนเป็น `corroborated`

## Status ladder (mirror ของ skill maturity)
- `draft` — สังเคราะห์รอบเดียว (agent-assisted) ยังไม่ verify ข้าม signal-set
- `corroborated` — ≥2 signal-set อิสระเห็นตรง หรือ human-verified
- (`validated` สงวนไว้ — peer/expert ยืนยัน · ยังไม่มี)

## ขอบเขต
- **คนละชั้นกับ `eval/INSIGHTS.md`:** อันนั้น = L3 บน **เลข A/B** · อันนี้ = L3 บน **signal โดเมน**
- **upstream ของ skills:** thesis ชี้ทิศ → skills เก็บ landmine ตามทิศ (thesis ≠ skill: ไม่ใช่ "เลือกอะไรเมื่อไหร่" แต่เป็น "โลกนี้ทำงานยังไง")
- **PII-clean + public-appropriate · Thai-first** — ห้ามอ้างกลุ่มปิด/บุคคล/quote
- regen index: `python scripts/build_synthesis_index.py` (commit ผลด้วย)
