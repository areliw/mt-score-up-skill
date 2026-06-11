# Setup Guide — Custom GPT / Project / Gem

วิธีตั้ง **MT WI Generator** บน 3 platform หลัก เพื่อใช้ครั้งเดียวต่อใน 1 คลิก

> 📖 อยากใช้ **skills** (ไม่ใช่ WI Generator) บนทุก platform → ดู [`USING.md`](./USING.md) · ไฟล์นี้เน้น WI Generator + การตั้ง Custom GPT / Project / Gem

---

## 🤖 ChatGPT Plus → Custom GPT (5 นาที setup)

1. เปิด https://chatgpt.com/gpts/editor
2. แท็บ **Configure**:
   - **Name**: `MT WI Generator (ISO 15189:2022 + ISO 15190:2020)`
   - **Description**: `ช่วย Medical Technologist ไทยเขียน WI ตาม ISO 15189:2022 + ISO 15190:2020 (safety) ใน 10 นาที`
   - **Instructions**: Copy ทั้งหมดใน [`../prompts/system.md`](../prompts/system.md) (ตั้งแต่ "## บทบาทของคุณ" จนจบ)
3. **Knowledge** — upload:
   - ไฟล์ใน `../templates/*.docx`
   - ไฟล์ใน `../inbox/*.md`
4. **Capabilities**: เปิด `Code Interpreter` (จำเป็นสำหรับ generate .docx)
5. คลิก **Create** → ตั้ง public/private/link sharing
6. Copy share link → paste FB post

**MT ที่มี ChatGPT Plus คลิก link → ใช้ได้เลย**

---

## 🟣 Claude Pro/Max → Project (3 นาที setup)

1. เปิด https://claude.ai/projects → **Create Project**
2. **Name**: `MT WI Generator`
3. **Custom instructions** (system prompt): Copy ทั้งหมดใน [`../prompts/system.md`](../prompts/system.md)
4. **Project knowledge** — upload:
   - ไฟล์ใน `../templates/*.docx`
   - ไฟล์ใน `../inbox/*.md`
5. คลิก **Save**
6. Share project (ปุ่มมุมขวาบน) → copy link → paste FB post

**MT ที่มี Claude Pro คลิก link → join project → ใช้ได้เลย**

---

## 🔵 Gemini Advanced → Gem (3 นาที setup)

1. เปิด https://gemini.google.com/gems
2. **Create new Gem**
3. **Name**: `MT WI Generator`
4. **Instructions**: Copy ทั้งหมดใน [`../prompts/system.md`](../prompts/system.md)
5. (Gemini ยังไม่รองรับ upload .docx ใน Gem — แปะ template เป็นข้อความใน instructions แทน)
6. Save → share link → paste FB post

**MT ที่มี Gemini Advanced คลิก link → ใช้ได้เลย**

---

## 📋 FB post template

```
🩺 เครื่องมือฟรีสำหรับ MT — เขียน WI (ISO 15189:2022 + ISO 15190:2020) ใน 10 นาที

ใช้ subscription AI ที่คุณมีอยู่แล้ว ไม่ต้องสมัครเพิ่ม:

🤖 ChatGPT Plus → [link Custom GPT]
🟣 Claude Pro/Max → [link Project]
🔵 Gemini Advanced → [link Gem]

หรือใช้ฟรี: paste prompt ด้านล่างใน Claude.ai/ChatGPT.com
→ github.com/areliw/mt-score-up-skill

ส่วนหนึ่งของ Score UP ecosystem
สร้างโดย MT จากตัวอย่าง B +  สำหรับ MT community ไทย
```

---

## Update Custom GPT/Project/Gem เมื่อ repo update

เมื่อ repo มี prompt ใหม่ / template ใหม่:
1. ไป Custom GPT/Project/Gem editor
2. Re-paste prompt จาก `prompts/system.md`
3. Re-upload `templates/*.docx`
4. Save → users ทุกคนได้ update อัตโนมัติ (ไม่ต้องทำอะไรเลย)
