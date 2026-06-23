# วิธีใช้ Skills — ครบทุก platform ใน 1 หน้า

skill ทุกตัวเป็น **ไฟล์ markdown** — ไม่ต้องติดตั้ง ไม่ต้องจ่าย token เพิ่ม ใช้บัญชี AI ของคุณเอง (Claude / ChatGPT / Gemini / Claude Code). เปิดหน้านี้ครั้งเดียวแล้วใช้เป็นทุกช่องทาง

> 🧭 **ไม่รู้จะใช้ skill ตัวไหน?** วาง [`prompts/triage.md`](../prompts/triage.md) ในแชต AI → เล่าปัญหา/เคส/งานวิจัยของคุณ → AI route ให้ว่าควรใช้ตัวไหน (หรือถ้าคลังยังไม่มี จะช่วยร่างให้ส่งเข้าคลัง)

---

## ตารางสรุป — แต่ละ platform ทำอะไรได้

| platform | ก๊อปวางในแชต | live-load ผ่าน raw URL | ใช้ทั้งคลัง (`dist/all-skills.md`) | ตั้งเป็น Project/GPT/Gem ถาวร |
|---|---|---|---|---|
| **แชตเปล่า (any AI)** | ✅ | ⚠️ เฉพาะตัวที่ต่อเน็ต/browse | ⚠️ เฉพาะ context ใหญ่ | ❌ |
| **Claude.ai + Project** | ✅ | ✅ | ✅ | ✅ |
| **ChatGPT + Custom GPT** | ✅ | ⚠️ เปิด browsing ก่อน | ⚠️ ไม่เหมาะ chat เปล่า/ฟรี | ✅ |
| **Gemini + Gem** | ✅ | ✅ | ✅ (context ใหญ่) | ✅ |
| **Claude Code / CLI** | ✅ | ✅ (`WebFetch`/วาง raw URL) | ✅ (วางไฟล์ในโปรเจกต์) | ✅ (เก็บเป็นไฟล์/`CLAUDE.md`) |

> **ก๊อปวาง** = ใช้ได้ทุกที่ แม้ offline · **live-load** = ได้เวอร์ชัน `main` ล่าสุดเสมอ แต่ AI ต้องดึง URL ได้ · **ทั้งคลัง** = ~133K tokens เหมาะเฉพาะ AI context ใหญ่

---

## (a) แชตเปล่า — AI ตัวไหนก็ได้ (ง่ายสุด)

ใช้ได้ทุกตัว ทุก tier แม้ offline-ish (ไม่ต้องให้ AI ต่อเน็ต)

1. เปิดไฟล์ใน [`skills/`](../skills) ที่ต้องการ เช่น `skills/bloodbank-judgment.md`
2. กดดูแบบ **Raw** บน GitHub → เลือกทั้งหมด → ก๊อป
3. วางในแชต AI → เว้นบรรทัด → **พิมพ์โจทย์/เคสของคุณต่อท้าย**
4. AI จะตอบตามวิจารณญาณใน skill นั้น

> ใช้กับ Claude.ai · ChatGPT · Gemini · Copilot · Poe · LLM local — เหมือนกันหมด

---

## (b) Claude.ai web + Claude Project (วางได้หลาย skill)

เหมาะเมื่ออยากให้ skill **ติดอยู่ถาวร** ไม่ต้องวางใหม่ทุกแชต และอยากผสมหลาย skill

1. เปิด [claude.ai/projects](https://claude.ai/projects) → **Create Project**
2. **Project knowledge** → วางเนื้อ skill ที่ใช้บ่อย ได้**หลายตัว** (เช่น `bloodbank-judgment` + `anti-hallucination` คู่กัน)
3. ทุกแชตใน Project นั้นจะเห็น skill โดยไม่ต้องก๊อปซ้ำ
4. อยากให้สดเสมอ → แทนที่จะก๊อปเนื้อ ใส่บรรทัด *"ดึง skill จาก `<raw URL>` มาใช้"* (Claude web ดึง URL ได้)

> Claude อ่าน context ยาวได้ → วาง `dist/all-skills.md` ทั้งคลังลง Project ก็ได้ แล้วให้ AI เลือก skill เองตามคำถาม

---

## (c) ChatGPT + Custom GPT

ตั้งครั้งเดียว แชร์ลิงก์ให้ทีมใช้ได้

- **แชตปกติ:** ก๊อปวาง (ข้อ a) ได้เลย
- **Custom GPT (ChatGPT Plus):** เอา skill ใส่ใน **Instructions** หรือ **Knowledge** ของ GPT → คลิกเดียวใช้ได้ทุกครั้ง
- ขั้นตอนตั้ง Custom GPT แบบละเอียด (รวม WI Generator) → ดู [`docs/setup-custom-gpt.md`](./setup-custom-gpt.md)
- อยากให้ live-load: เปิด **Browsing** ของ GPT ก่อน แล้วสั่งดึง raw URL
- ⚠️ `dist/all-skills.md` (~133K tokens) **หนักเกิน** chat เปล่า/ฟรี — ใส่เฉพาะ skill ที่ต้องใช้ดีกว่า

---

## (d) Gemini + Gem

1. ก๊อปวาง (ข้อ a) ในแชต Gemini ได้เลย
2. อยากถาวร → [gemini.google.com/gems](https://gemini.google.com/gems) → **Create Gem** → วาง skill ใน **Instructions**
3. Gemini ต่อเน็ต → live-load ผ่าน raw URL ได้
4. Gemini context ใหญ่ → วาง `dist/all-skills.md` ทั้งคลังได้

---

## (e) Claude Code / CLI

มี 3 ทาง เลือกตามงาน:

1. **วางไฟล์ในโปรเจกต์** — ก๊อป `skills/<name>.md` ลงในโฟลเดอร์งานคุณ แล้วอ้างถึงในแชต (`อ่าน bloodbank-judgment.md แล้ว...`) — เหมาะเมื่อทำงานซ้ำในโปรเจกต์เดิม
2. **ดึงสดด้วย raw URL** — สั่ง *"WebFetch `https://raw.githubusercontent.com/areliw/mt-score-up-skill/main/skills/<name>.md` มาใช้"* → ได้ `main` ล่าสุด
3. **ทั้งคลังในโปรเจกต์** — ก๊อป `dist/all-skills.md` ลงโปรเจกต์ หรือใส่ path ใน `CLAUDE.md` ให้ทุก session เห็น

> raw URL ทุกตัว → [`skills/INDEX.md`](../skills/INDEX.md) (CI อัปเดตให้)

---

## (f) live-load ผ่าน raw URL (สำหรับ AI ที่ต่อเน็ต)

ไม่ต้องก๊อปเนื้อ — บอก AI ดึงสด:

```
ดึง skill จาก https://raw.githubusercontent.com/areliw/mt-score-up-skill/main/skills/<ชื่อ-skill>.md มาใช้
แล้วช่วยผมเรื่อง <โจทย์ของคุณ>
```

- ได้เวอร์ชัน `main` **ล่าสุดทุกครั้ง = auto-sync** ไม่ต้องก๊อปใหม่เมื่อมีแก้
- รายการ URL ครบ → [`skills/INDEX.md`](../skills/INDEX.md)
- ⚠️ ใช้ได้เฉพาะ AI ที่ดึง URL ได้ (Claude web · ChatGPT browsing · Gemini · Claude Code) — **แชตเปล่า offline ใช้ก๊อป (ข้อ a)**

---

## (g) ทั้งคลังในไฟล์เดียว — `dist/all-skills.md`

[`dist/all-skills.md`](../dist/all-skills.md) รวม **94 skill ในไฟล์เดียว** (~140K tokens) → AI เลือกใช้เองตามคำถาม (self-route) ไม่ต้องเลือกตัวเอง

- **เหมาะ:** Claude / Gemini / Project ที่ context ใหญ่ + อยากให้ AI หยิบ skill เองทั้งบทสนทนา
- **ไม่เหมาะ:** ChatGPT chat เปล่า/ฟรี — หนักเกิน context · งานที่อยากคุม version เป๊ะ (133K tokens กินที่ ทำให้แชตเต็มเร็ว)
- ก๊อปหรือ live-load ก็ได้ (ไฟล์เดียวกัน)

---

## ก๊อป (แช่แข็ง) vs live-load (auto-sync) — เลือกเมื่อไหร่

| | **ก๊อปเนื้อไฟล์ (แช่แข็ง)** | **live-load ผ่าน raw URL (auto-sync)** |
|---|---|---|
| ความเสถียร | เนื้อหานิ่ง ไม่เปลี่ยนกลางคัน | ได้ `main` ล่าสุดทุกครั้ง |
| audit trail | **cite เวอร์ชันได้** (รู้ว่าใช้เนื้อหาตอนไหน) | เนื้อหาเปลี่ยนได้ — cite ยาก |
| ต้องต่อเน็ต? | ไม่ต้อง | ต้อง (AI ต้องดึง URL ได้) |
| **เลือกตัวนี้เมื่อ** | **งานคลินิก / ต้องอ้างอิงในรายงาน-audit / offline** | **อยากได้สดเสมอ / ไม่ต้องก๊อปใหม่ / งานทดลอง-สำรวจ** |

> งานที่กระทบคนไข้/ต้องตรวจสอบย้อนหลัง → **ก๊อปแช่แข็ง** แล้วบันทึกว่าใช้เนื้อหาวันไหน

---

## stack หลาย skill เข้าด้วยกัน

วางได้หลายตัวในแชต/Project เดียว — แต่มีกฎ:

- **วาง skill หลักก่อน แล้วตามด้วยตัวเสริม** เช่น `bloodbank-judgment` (หลัก) + `anti-hallucination` (กัน AI มั่ว)
- **งานคลินิก (🩸) → วาง [`anti-hallucination`](../skills/anti-hallucination.md) คู่เสมอ** เมื่อให้ AI ช่วยคิดเรื่องที่กระทบคนไข้
- ⚠️ **"ระวัง" ชนะ "สั้น":** ถ้าใช้ [`ai-assistant-calibration`](../skills/ai-assistant-calibration.md) (เน้นตอบสั้น) คู่กับ skill งานแล็บ — **ให้ความรอบคอบ/verify ของ skill คลินิก override ความสั้นเสมอ** (ความปลอดภัยผู้ป่วย > ความกระชับ)
- อยากเห็น AI ทำถึงไหนในงานหลายขั้น → วาง [`progress-tracker`](../skills/progress-tracker.md) เพิ่ม

---

## ⚠️ เตือนก่อนใช้ (อ่านสั้นๆ)

- skill = **ตัวช่วยคิด/decision-support ไม่ใช่คำสั่งวินิจฉัย/รักษา** — งานคลินิกต้องอิง SOP + ให้ MT/แพทย์ผู้มีใบประกอบฯ ยืนยันก่อนลงมือเสมอ
- ทุก skill ยังเป็น **draft** (ยังไม่ผ่าน clinical peer-review) — verify กับแหล่งทางการ + คนก่อนใช้จริง
- **ห้ามใส่ข้อมูล identifying ของคนไข้** (ชื่อ / HN / MRN / ชื่อ รพ.) ในแชต — ใช้ generic placeholder

---

*คู่มือนี้เพื่อช่วยให้ใช้ skill ได้สะดวก ไม่ใช่คำรับรองความถูกต้องของเนื้อหา skill — เนื้อหาทุกตัวเป็นตัวช่วยคิด ต้องตรวจสอบกับ SOP/มาตรฐาน + วิจารณญาณของผู้ใช้เสมอ*
