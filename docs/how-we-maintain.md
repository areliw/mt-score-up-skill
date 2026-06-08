# How we maintain — ให้คลังไม่เน่าเมื่อโตเกิน 80 สกิล

> เมื่อ skill เยอะ ปัญหาเปลี่ยนจาก "มีไหม" → "ยังถูก/ยังสอดคล้องกันไหม". เอกสารนี้คือจังหวะดูแล.

## จังหวะออดิต (stocktake)
- **Quick scan** — เฉพาะสกิลที่เพิ่ง add/แก้ (ทุก PR): format/scope/PDPA/disclaimer/ลิงก์
- **Full stocktake** — เป็นรอบ (เช่นทุกไตรมาส): อ่านทั้งคลัง หา drift, ตัวซ้ำ, เนื้อหาเก่า, กับดักที่ขัดกันเอง

## กลั่นกฎร่วม (distill)
- เจอ pattern ที่ใช้ซ้ำหลายสกิล → กลั่นเป็นกฎกลาง (house style / `STANDARDS.md`) ไม่ใช่ปล่อยกระจาย
- ตัวอย่างกฎร่วมปัจจุบัน: verdict-first (กฎ#1→กับดัก#1→verify-first) · risk-tiered disclaimer · กับดัก #1 ของสกิล MT++ ผูกกับ PDPA/verify-against-source

## โครงสร้าง = source of truth
- **`scripts/build_triage.py`** regenerate `skills/INDEX.md` + `dist/all-skills.md` + `prompts/triage.md` แบบ deterministic → **อย่าแก้ไฟล์ generated ด้วยมือ** รันสคริปต์แทน
- **`STANDARDS.md`** auto-recheck รายเดือน (edition ISO/AABB) — ดู `scripts/recheck_standards.py`
- เพิ่มสกิล → bump count ใน `README.md` + `skills/README.md`

## เขียน/ขัดภาษา (house writing style)
- **judgment ไม่ใช่ knowledge** — ตัดสิ่งที่ตำรา/AI รู้แล้ว เก็บ "เลือกอะไรเมื่อไหร่ + กับดัก"
- **ภาษาเป็นมนุษย์** — ตัดกลิ่น AI (รายการยืดเยื้อ, คำคุณศัพท์เฟ้อ, em-dash เกิน) ให้อ่านลื่น กระชับ (แนวคิดจาก `humanizer`)
- **เสียงสม่ำเสมอ** ทั้งคลัง — Thai-first, ตรงไปตรงมา, verdict นำ (แนวคิดจาก `article-writing`)

## เก็บบทเรียน (post-mortem)
- เจอ error/issue (เช่น clinical error ที่ audit จับ) → บันทึก root cause + กฎกันซ้ำ → feed กลับเข้า how-we-audit / STANDARDS
- สกิลโตจาก "สิ่งที่เจอซ้ำ" → instinct → สกิล (อย่ารอจน perfect ค่อยเขียน)

## อ้างอิงในรีโป
- `docs/how-we-audit.md` · `docs/how-we-eval.md` · `CONTRIBUTING.md` · `STANDARDS.md` · `docs/EXPANSION-PLAN.md`
