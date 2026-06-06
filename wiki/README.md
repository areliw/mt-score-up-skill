# Wiki — เข้าใจโปรเจกต์ลึกขึ้น

หน้ารวมลิงก์ไปเอกสารที่อธิบาย "ของพวกนี้คืออะไร + ทำมายังไง + เชื่อได้แค่ไหน"

## skill คืออะไร
ไฟล์ markdown ที่แพ็ก **"วิจารณญาณ"** ของ MT ที่เก่งแล้ว — ไม่ใช่ "ความรู้" (ตำรา/AI มีหมดแล้ว) แต่เป็น **"เลือกอะไรเมื่อไหร่ + กับดักที่มือใหม่ไม่รู้"**. วางในแชต AI → AI ตอบในสายงานนั้นคมขึ้น/ปลอดภัยขึ้น
- วิธีใช้ + รายการทั้งหมด → [`skills/README.md`](../skills/README.md)
- เห็นตัวอย่างทำงานจริง → [`examples/`](../examples) · ลองฝึกเอง → [`exercises/`](../exercises)

## ทำมายังไง (หลักการ)
- **เก็บ judgment ไม่ใช่ knowledge** — ตัดสูตร/ตำราที่ AI รู้อยู่แล้วทิ้ง เก็บ "เลือกอันไหนเมื่อไหร่ + กับดักที่ผู้เชี่ยวชาญรู้"
- **verdict-first** — กฎ #1 + กับดัก #1 อยู่บนสุด เพื่อให้ AI ที่อ่านผ่านๆ ก็ดึงไปใช้ได้
- **risk-tiered disclaimer** — งานคลินิก (ผิด=คนเจ็บ) disclaimer หนัก + verify-first guard; งานทั่วไป disclaimer เบา
- วิสัยทัศน์เต็ม → [`docs/skill-hub-vision.md`](../docs/skill-hub-vision.md)

## เชื่อได้แค่ไหน (ทดสอบยังไง)
ไม่ได้เคลมลอยๆ — มีการวัดจริงพร้อม caveat:
- **eval 3 รอบ** (weak-model A/B + literature + Titanic) → [`eval/RESULTS.md`](../eval/RESULTS.md) · scorecard ต่อ skill → [`eval/ab-scorecard.md`](../eval/ab-scorecard.md)
- **วิธีวัด + ข้อจำกัด** → [`eval/METHOD.md`](../eval/METHOD.md)
- **บทเรียนสำคัญ: ปรับ skill ยังไงให้ดีขึ้น + วัดยังไงไม่ไล่จับ noise** → [`eval/IMPROVE-PLAYBOOK.md`](../eval/IMPROVE-PLAYBOOK.md)

## อยากเขียน/แก้ skill เอง
- หลักการวัดว่า skill ดีจริงไหม → skill [`ab-test-judgment`](../skills/ab-test-judgment.md)
- วิธีร่วมสมทบ → [`CONTRIBUTING.md`](../CONTRIBUTING.md)

## เครื่องมือเสริม
- **WI generator** (เขียน Work Instruction ตาม ISO 15189:2022) → [`prompts/system.md`](../prompts/system.md) · ตั้งเป็น Custom GPT → [`docs/setup-custom-gpt.md`](../docs/setup-custom-gpt.md)
- **มาตรฐาน source-of-truth** → [`STANDARDS.md`](../STANDARDS.md)
