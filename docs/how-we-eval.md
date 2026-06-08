# How we eval — วัดว่าสกิล "ช่วยจริง" ไม่ใช่เดา

> วิธีวัดผล skill ของรีโปนี้ — อ่านเป็น **grade-book ไม่ใช่ leaderboard**. รายละเอียด/ผลจริงอยู่ใน `eval/`.
> หลักคิดเรื่องวัดผลแบบไม่ไล่จับ noise สรุปไว้ในสกิล `ab-test-judgment`.

## วิธี A/B (with vs without skill)
1. ให้ **model อ่อน (เช่น Haiku)** ตอบโจทย์กับดัก — รอบ *มีสกิล* vs *ไม่มีสกิล* (without-skill = noise control)
2. **กรรมการตาบอด** (ไม่รู้ว่าอันไหนมีสกิล) ให้คะแนน
3. ทำซ้ำหลายรอบ + เฉลี่ย → ลด noise

## อ่านผลให้ถูก (กันหลอกตัวเอง)
- **มี noise เสมอ** (วัดซ้ำต่างกัน ~1.4 จุดบนโจทย์เดียว) → delta ต้องเกิน noise floor ถึงเชื่อ
- **"เสมอ (tie)" ≠ แย่** — แปลว่า AI ตอบถูกเองอยู่แล้ว; ค่าจริงของสกิลอยู่ที่ **ความสม่ำเสมอ + เคสยาก + ช่วย model อ่อน/มือใหม่**
- เกณฑ์ที่แคร์สุด = **0 dangerous regression** (ไม่มีสกิลไหนทำให้ตอบ "พังลง")
- เลือกตัดสินด้วย **review แทน A/B** เมื่อ delta เล็กกว่า noise (ดู `eval/IMPROVE-PLAYBOOK.md`)

## skill ใหม่เข้ายังไง
1. ผ่าน **critical review** (how-we-audit) ก่อน — clinical/scope/format
2. merge ได้ที่ `status: draft`
3. A/B ทำที่ระดับ **library-aggregate** เป็นรอบ (ต่อสกิลมักจมใน noise) → อัปเดต `eval/`
4. clinical content เลื่อนพ้น draft เมื่อมี peer-review

## อ้างอิงในรีโป
- `eval/METHOD.md` · `eval/RESULTS.md` · `eval/ab-scorecard.md` · `eval/round3/` · `eval/IMPROVE-PLAYBOOK.md`
- แนวคิดวัดผล: สกิล `ab-test-judgment`
