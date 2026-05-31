# MT Score UP — Skills Hub สำหรับ MT ไทย

แหล่งรวม **"สกิล" + เครื่องมือฟรี** สำหรับ Medical Technologist (MT) ไทย — เอาไปวางในแชต AI ที่คุณมีอยู่แล้ว (Claude / ChatGPT / Gemini) ใช้ได้เลย **ไม่ต้องติดตั้ง ไม่ต้องจ่ายค่า token เพิ่ม**

> แนวคิด: แพ็ก **"วิจารณญาณ" ของ MT ที่เก่งแล้ว** ให้กลายเป็นไฟล์ที่ใครก็หยิบไปใช้ได้ — ไม่ใช่แค่ "ความรู้" (ตำรา/AI มีอยู่แล้ว) แต่คือ **"เลือกอะไรเมื่อไหร่ + กับดักที่มือใหม่ไม่รู้"**

---

## 📚 ส่วนที่ 1 — Skills (23 สกิล)

**วิธีใช้:** เปิดไฟล์ในโฟลเดอร์ [`skills/`](./skills) → copy ทั้งไฟล์ → วางในแชต AI → พิมพ์ปัญหาของคุณ
รายการเต็ม + คำอธิบายอยู่ที่ [`skills/README.md`](./skills/README.md)

### 🔬 งานวิจัย / สถิติ (R2R)
| skill | ช่วยอะไร |
|---|---|
| [r2r-research-proposal](./skills/r2r-research-proposal.md) | ปั้นโจทย์วิจัย: ปัญหา → คำถาม → objective |
| [choose-stat-test](./skills/choose-stat-test.md) | เลือก statistical test ให้ถูกตัว |
| [sample-size-power](./skills/sample-size-power.md) | หาขนาดตัวอย่าง N (power analysis) |
| [r2r-stats](./skills/r2r-stats.md) | รัน + แปลผลสถิติ R2R |

### 🤖 ใช้ AI อย่างคม / ปลอดภัย
| skill | ช่วยอะไร |
|---|---|
| [ai-assistant-calibration](./skills/ai-assistant-calibration.md) | คาลิเบรต AI ให้ตอบคม ตรงนิสัยคุณ |
| [ai-agent-team](./skills/ai-agent-team.md) | ตั้ง AI เป็นทีมหลายตำแหน่งแบบบริษัท |
| [self-improving-agent](./skills/self-improving-agent.md) | ให้ agent เรียนรู้จากความผิดพลาด |
| [what-skill-do-i-need](./skills/what-skill-do-i-need.md) | วินิจฉัยว่าคุณต้องการ skill ไหนจริงๆ |
| [offload-to-automation](./skills/offload-to-automation.md) | งานเป๊ะให้ code ทำ AI เป็นคนคุม+ตรวจ |
| [anti-hallucination](./skills/anti-hallucination.md) | กัน + จับ AI มั่วข้อเท็จจริง/อ้างอิง |

### 💬 สื่อสาร
| skill | ช่วยอะไร |
|---|---|
| [polite-but-clear](./skills/polite-but-clear.md) | ปรับถ้อยคำให้สุภาพแต่ยังได้ใจความ |
| [explain-simply](./skills/explain-simply.md) | อธิบายเรื่องยากแบบเด็ก ป.3 (ไม่ผิด) |
| [content-creator-judgment](./skills/content-creator-judgment.md) | เลือกหัวข้อคอนเทนต์ให้ความรู้ + ไม่ทำให้เพจตาย |

### 🧭 ชีวิต / อาชีพ
| skill | ช่วยอะไร |
|---|---|
| [ikigai-finder](./skills/ikigai-finder.md) | หา ikigai แบบไม่หลอกตัวเอง |
| [self-development-coach](./skills/self-development-coach.md) | โค้ชพัฒนาตัวเองแบบตรงไปตรงมา |
| [crm-judgment](./skills/crm-judgment.md) | คิดแบบลูกค้า สำหรับ MT สาย sales/คลินิก/แอป |

### 💻 โค้ด / เทคนิค / data
| skill | ช่วยอะไร |
|---|---|
| [python-coach](./skills/python-coach.md) | เลือกเครื่องมือ + ไม่ตกหลุม Python |
| [db-judgment](./skills/db-judgment.md) | ตัดสินใจ SQL / ออกแบบ DB ไม่ให้ระเบิด |
| [ml-judgment](./skills/ml-judgment.md) | เลือกโมเดล/metric/validation ML + เลี่ยงกับดัก |
| [cv-judgment](./skills/cv-judgment.md) | เลือกเทคนิควิเคราะห์ภาพ + เลน blood smear/เซลล์ |
| [optimization-judgment](./skills/optimization-judgment.md) | เลือกวิธี optimize (LP/heuristic/sim) จัดเวร/ทรัพยากร |
| [data-project-survival](./skills/data-project-survival.md) | โปรเจกต์ data/ML ไม่ให้ล้ม + ประเมิน vendor |

### 🗂️ จัดการ
| skill | ช่วยอะไร |
|---|---|
| [never-lose-a-file](./skills/never-lose-a-file.md) | จัดไฟล์ให้เป็นระเบียบ แล้วไม่หายอีก |

> แต่ละไฟล์มี `type` (ADVISE = ให้คำแนะนำ · DO = รันจริง · CALIBRATION = ปรับวิธีทำงานของ AI) และ `needs` (AI แบบไหนใช้ได้) บอกไว้ในหัวไฟล์

---

## 🧪 ส่วนที่ 2 — WI Generator (ISO 15189:2022)

ช่วยเขียน **Work Instruction (WI)** ตาม **ISO 15189:2022** + **ISO 15190:2020** (safety) ให้เสร็จไว

1. เปิด [Claude.ai](https://claude.ai) / [ChatGPT.com](https://chatgpt.com) / [Gemini.google.com](https://gemini.google.com)
2. Copy [`prompts/system.md`](./prompts/system.md) → paste เป็นข้อความแรก
3. ตอบคำถามที่ AI ถาม → ได้ร่าง WI ใน 5–10 นาที
4. Copy output → จัด format ใน Word

อยากให้ AI จำ context: ทำเป็น Custom GPT / Claude Project / Gemini Gem — ดู [`docs/setup-custom-gpt.md`](./docs/setup-custom-gpt.md)

> MT เป็นเจ้าของผลงาน AI เป็นแค่ปากกาช่วยร่าง — ตรวจสอบความถูกต้องและรับผิดชอบเนื้อหาก่อนใช้จริงเสมอ

---

## โครงสร้าง

```
mt-score-up-skill/
├── skills/        # ★ 18 สกิล — copy ไฟล์ไปวางในแชต AI
├── prompts/       # System prompt สำหรับ WI generator
│   └── system.md
├── templates/     # WI .docx templates (generic)
├── profiles/      # Layout profile ต่อโรงพยาบาล (generic)
├── inbox/         # Drop WI ตัวอย่าง — AI scan ใช้เป็น template
└── docs/          # Vision, setup guides
```

## Privacy & ความปลอดภัย

- ✅ ทำงานบน browser / เครื่องของคุณเท่านั้น — ไม่มี server กลาง ไม่เก็บข้อมูล
- ✅ Open source — audit ได้ทุกบรรทัด (MIT)
- ⚠️ **ห้ามใส่ข้อมูล identifying ของคนไข้** (ชื่อ / HN / MRN) — ใช้ generic placeholder
- ⚠️ skill ช่วย "คิด/ร่าง" ไม่ใช่แหล่งความจริงสุดท้าย — เรื่องการแพทย์/สำคัญ ต้องตรวจกับแหล่งทางการ + มนุษย์

## License

MIT — ใช้ฟรี / แก้ได้ / share ได้

## Contributing

อยากเพิ่ม skill ของตัวเอง / ปรับปรุงของเดิม? ดู [CONTRIBUTING.md](./CONTRIBUTING.md) — เล่าปัญหาหรือวิจารณญาณในสายงานคุณมาได้เลย

## Credits

โดย **Phanuphong Tameesak — MT Score UP!** เพื่อชุมชน MT ไทย
ส่วนหนึ่งของ **Score UP** ecosystem
