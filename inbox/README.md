# 📥 inbox/

**Drop WI ที่นี่** — ไม่ต้องคิด structure / ชื่อ / แผนก. AI scan content เองทุก session แล้วใช้เป็น template เมื่อ MT ขอ WI

## วิธี contribute

1. ใช้ WI จริงที่ทำเสร็จ + ผ่าน QC แล้ว
2. **Anonymize** (สำคัญ!) — ลบ:
   - ชื่อคนไข้ / HN / MRN → ลบหรือใช้ `[ผู้ป่วย]`
   - ชื่อ MT / supervisor / QC manager → `[MT name]`, `[supervisor]`
   - เลขที่เอกสารเฉพาะ → `WI-BB-[TBD]`
   - Lot number / date ที่ correlate กับ patient → ลบ
3. Save เป็น `.md` (เปิด Word → Save As → Markdown หรือ copy text ไป notepad → save `.md`)
4. **ชื่อไฟล์อะไรก็ได้** — ไทย / อังกฤษ / ผสม:
   - ✅ `PRC ตัวอย่าง B.md`
   - ✅ `abo-grouping.md`
   - ✅ `gram_stain_example.md`
   - ✅ `WI-การตรวจ-platelet-count.md`
5. Drop ไฟล์เข้า `inbox/` → commit

## ที่มีตอนนี้

- [PRC-preparation-DEMO.md](PRC-preparation-DEMO.md) — Generic ISO 15189:2022 + AABB 21st ed (DEMO — ห้ามใช้จริงโดยไม่ verify)

## AI ทำอะไรกับไฟล์ที่นี่

ตอน MT ขอ "ทำ WI <X>" (ใน Custom GPT / Claude Project / Gemini Gem ที่ upload `inbox/` เข้าไปแล้ว):

1. **Scan ทุกไฟล์** ที่นี่ → read first heading + first paragraph
2. **Match topic** กับ request:
   - Match 1 ไฟล์ → ใช้เป็น template หลัก (structure + tone + ระดับรายละเอียด) + ถาม clarifying แค่ 1-2 ข้อที่ template ไม่ครอบคลุม
   - Match หลายไฟล์ (เช่น PRC ตัวอย่าง B + PRC ) → ถาม user เลือกก่อน
   - ไม่ match → ใช้ default 12-section ISO 15189:2022 structure + ถาม clarifying 4 ข้อ

ดู [`../prompts/system.md`](../prompts/system.md) Step 0 สำหรับ logic เต็ม

## ⚠️ Privacy reminder

`inbox/` เป็น **public** ใน open source repo — ทุกไฟล์ที่ commit จะถูกเห็นโดยใครก็ตามที่ดู repo

- ถ้าไม่แน่ใจว่า anonymize ครบไหม → **อย่า commit** ขอ QC manager / supervisor review ก่อน
- ถ้าเป็น proprietary SOP ของโรงพยาบาล → ขออนุญาตก่อน submit
- ถ้าอยากเก็บ local อย่างเดียว (ไม่ commit) → ไม่ต้องวางใน `inbox/`, ใช้ folder ส่วนตัวที่อยู่ใน `.gitignore`
