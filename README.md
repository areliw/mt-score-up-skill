# MT Score UP — Skills Hub สำหรับ MT ไทย

แหล่งรวม **"สกิล" + เครื่องมือฟรี** สำหรับ Medical Technologist (MT) ไทย — เอาไปวางในแชต AI ที่คุณมีอยู่แล้ว (Claude / ChatGPT / Gemini) ใช้ได้เลย **ไม่ต้องติดตั้ง ไม่ต้องจ่ายค่า token เพิ่ม**

> แนวคิด: แพ็ก **"วิจารณญาณ" ของ MT ที่เก่งแล้ว** ให้กลายเป็นไฟล์ที่ใครก็หยิบไปใช้ได้ — ไม่ใช่แค่ "ความรู้" (ตำรา/AI มีอยู่แล้ว) แต่คือ **"เลือกอะไรเมื่อไหร่ + กับดักที่มือใหม่ไม่รู้"**

---

> ⚠️ **เพื่อการศึกษา / ช่วยคิดเท่านั้น — NOT FOR CLINICAL USE.** กลุ่มสกิลงานแล็บ (🩸) เป็นกรอบช่วย *ตัดสินใจ/ทบทวน* ไม่ใช่คำสั่งวินิจฉัย/รักษา และไม่รับประกันความถูกต้อง — การใช้กับผู้ป่วยจริงต้องอิง SOP + วิจารณญาณของ MT/แพทย์ผู้มีใบประกอบวิชาชีพเสมอ · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้

## 📚 ส่วนที่ 1 — Skills (51 สกิล)

**วิธีใช้:** เปิดไฟล์ในโฟลเดอร์ [`skills/`](./skills) → copy ทั้งไฟล์ → วางในแชต AI → พิมพ์ปัญหาของคุณ
รายการเต็ม + คำอธิบายอยู่ที่ [`skills/README.md`](./skills/README.md)

### 🩸 งานแล็บ (Lab bench)
| skill | ช่วยอะไร |
|---|---|
| [bloodbank-judgment](./skills/bloodbank-judgment.md) | ตัดสินใจหน้างานธนาคารเลือด — ABO discrepancy / antibody ID / crossmatch / transfusion reaction |
| [hematology-judgment](./skills/hematology-judgment.md) | อ่าน CBC/smear/coag — review smear เมื่อไหร่ · anemia path · blast · thal vs IDA · PT/aPTT |
| [clinchem-judgment](./skills/clinchem-judgment.md) | QC accept/reject (Westgard) · interference HIL · critical value · recalibrate vs troubleshoot |
| [chemistry-interpretation-judgment](./skills/chemistry-interpretation-judgment.md) | แปลผล organ-system: tumor/renal(eGFR)/LFT pattern/cardiac timing/ABG+anion gap |
| [clinmicro-judgment](./skills/clinmicro-judgment.md) | เชื้อจริง vs contaminate · ID workflow · อ่าน AST/MDR · culture vs molecular |
| [applied-microbiology-judgment](./skills/applied-microbiology-judgment.md) | จุลชีววิทยาประยุกต์ (อาหาร/อุตสาหกรรม): ถนอม · screen≠confirm · metagenomics · bioremediation · probiotic |
| [immunoassay-judgment](./skills/immunoassay-judgment.md) | เลือก format · อ่าน HBV/HIV/syphilis/ANA panel · prozone/hook/window |
| [molecular-judgment](./skills/molecular-judgment.md) | เลือก method (RFLP/ASO/HRM/Sanger/NGS) · แปล qPCR/Ct · กัน false +/− · pharmacogenomics |
| [pathology-judgment](./skills/pathology-judgment.md) | อ่าน pattern: benign/malignant · necrosis · อักเสบ · grading/staging · dysplasia |
| [parasitology-judgment](./skills/parasitology-judgment.md) | เลือก concentration/stain · malaria thick/thin + ตรวจซ้ำ · single-stool false-neg |
| [toxicology-judgment](./skills/toxicology-judgment.md) | screen vs confirm · antidote (OP/carbamate/paraquat) · chelator · TDM timing |
| [pharmacology-judgment](./skills/pharmacology-judgment.md) | ยาเบื้องต้น: ADME · แพ้ยา vs ผลข้างเคียง (SJS/TEN) · ยาตีกัน · pharmacogenomics |
| [clinical-correlation-judgment](./skills/clinical-correlation-judgment.md) | อ่านผลแล็บข้ามแขนง → ตั้ง DDx/ชี้ทางให้แพทย์ (pivotal → DDx → rule-out) |
| [infection-control-judgment](./skills/infection-control-judgment.md) | IPC/biosafety: hand hygiene (C.diff spore) · N95 vs surgical · precaution · ความดันลบ/บวก · เข็มตำ |

### 🔬 งานวิจัย / สถิติ (R2R)
| skill | ช่วยอะไร |
|---|---|
| [r2r-research-proposal](./skills/r2r-research-proposal.md) | ปั้นโจทย์วิจัย: ปัญหา → คำถาม → objective |
| [research-design-judgment](./skills/research-design-judgment.md) | เลือก study design + กัน bias/confounder + gate IRB |
| [choose-stat-test](./skills/choose-stat-test.md) | เลือก statistical test ให้ถูกตัว |
| [sample-size-power](./skills/sample-size-power.md) | หาขนาดตัวอย่าง N (power analysis) |
| [r2r-stats](./skills/r2r-stats.md) | รัน + แปลผลสถิติ R2R |
| [manuscript-judgment](./skills/manuscript-judgment.md) | เขียน manuscript/proposal (IMRaD) ให้ผ่าน reviewer |
| [critical-appraisal-judgment](./skills/critical-appraisal-judgment.md) | อ่าน/ประเมินงานวิจัย + lit review + หา gap + ประเมิน test (sens/spec/PPV) |

### 🤖 ใช้ AI อย่างคม / ปลอดภัย
| skill | ช่วยอะไร |
|---|---|
| [ai-assistant-calibration](./skills/ai-assistant-calibration.md) | คาลิเบรต AI ให้ตอบคม ตรงนิสัยคุณ |
| [ai-agent-team](./skills/ai-agent-team.md) | ตั้ง AI เป็นทีมหลายตำแหน่งแบบบริษัท |
| [self-improving-agent](./skills/self-improving-agent.md) | ให้ agent เรียนรู้จากความผิดพลาด |
| [what-skill-do-i-need](./skills/what-skill-do-i-need.md) | วินิจฉัยว่าคุณต้องการ skill ไหนจริงๆ |
| [offload-to-automation](./skills/offload-to-automation.md) | งานเป๊ะให้ code ทำ AI เป็นคนคุม+ตรวจ |
| [anti-hallucination](./skills/anti-hallucination.md) | กัน + จับ AI มั่วข้อเท็จจริง/อ้างอิง |
| [progress-tracker](./skills/progress-tracker.md) | วางคู่สกิลไหนก็ได้ → AI โชว์ checklist/flowchart ว่าทำถึงไหน |

### 💬 สื่อสาร
| skill | ช่วยอะไร |
|---|---|
| [polite-but-clear](./skills/polite-but-clear.md) | ปรับถ้อยคำให้สุภาพแต่ยังได้ใจความ |
| [explain-simply](./skills/explain-simply.md) | อธิบายเรื่องยากแบบเด็ก ป.3 (ไม่ผิด) |
| [content-creator-judgment](./skills/content-creator-judgment.md) | เลือกหัวข้อคอนเทนต์ให้ความรู้ + ไม่ทำให้เพจตาย |
| [photography-judgment](./skills/photography-judgment.md) | ถ่ายภาพ/วิดีโอ + photomicrography (สไลด์/colony/gel): exposure/DOF/composition/WB |

### 🧭 ชีวิต / อาชีพ
| skill | ช่วยอะไร |
|---|---|
| [ikigai-finder](./skills/ikigai-finder.md) | หา ikigai แบบไม่หลอกตัวเอง |
| [self-development-coach](./skills/self-development-coach.md) | โค้ชพัฒนาตัวเองแบบตรงไปตรงมา |
| [digital-judgment](./skills/digital-judgment.md) | privacy/PDPA/security/ลิขสิทธิ์/ลงทุน — ไม่โดนหลอก |
| [finance-judgment](./skills/finance-judgment.md) | การเงิน/ลงทุน/อ่านงบ/ธุรกิจ — ลำดับเงิน + กันกับดัก/scam + เลนส์ econ |
| [financial-statement-judgment](./skills/financial-statement-judgment.md) | อ่านงบ 5 ฉบับ + ลำดับอ่าน + คุณภาพกำไร (CFO) + จับ window-dressing/OCI |
| [mt-law-ethics-judgment](./skills/mt-law-ethics-judgment.md) | กฎหมาย/จรรยาบรรณ MT: ใบอนุญาต · ขอบเขตวิชาชีพ · ความลับ/PDPA · เครื่องมือแพทย์ |
| [mt-exam-strategy-judgment](./skills/mt-exam-strategy-judgment.md) | กลยุทธ์สอบใบประกอบฯ MT: blueprint/บริหารเวลา · จับ distractor · study ROI |

### 💼 บริหารแล็บ / ขาย IVD
| skill | ช่วยอะไร |
|---|---|
| [lab-management-judgment](./skills/lab-management-judgment.md) | QMS/ISO 15189 · QC strategy (sigma/IQCP) · งบ · verification · inventory |
| [ivd-sales-judgment](./skills/ivd-sales-judgment.md) | ขาย IVD/diagnostics — ขายผลลัพธ์บริหาร · budget-pocket · ROI · spec-in |
| [crm-judgment](./skills/crm-judgment.md) | คิดแบบลูกค้า สำหรับ MT สาย sales/คลินิก/แอป |
| [marketing-judgment](./skills/marketing-judgment.md) | กลยุทธ์การตลาด B2B: STP · buying center · pricing · positioning · push/pull |
| [sales-psychology-judgment](./skills/sales-psychology-judgment.md) | จิตวิทยาขาย/อ่านคน: แรงจูงใจ · active listening · trust · โน้มน้าว(+จริยธรรม) · เจรจา |

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
├── skills/        # ★ 51 สกิล — copy ไฟล์ไปวางในแชต AI
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

## เนื้อหา & การอ้างอิง (Content & sources)

- เนื้อหาทุกสกิล **เรียบเรียงใหม่จากองค์ความรู้มาตรฐานของวิชาชีพ** (ตำรา MT, แนวทางสากล, ประสบการณ์หน้างาน) — สกัดเป็น "วิจารณญาณ" (เลือกอะไรเมื่อไหร่ + กับดัก) **ไม่ได้คัดลอกสไลด์/เอกสารมีลิขสิทธิ์ของผู้ใด**
- มาตรฐานที่อ้างถึง (ISO 15189:2022 · ISO 15190:2020 · AABB Technical Manual 21st / Standards 35th ฯลฯ) = อ้าง **หัวข้อ/edition เพื่อชี้ทาง ไม่ได้คัดเนื้อความในมาตรฐานมา** — ผู้ใช้ต้องทวนกับฉบับจริงที่หน่วยงานถือ (ดู [`STANDARDS.md`](./STANDARDS.md))
- ตัวเลข/ค่าอ้างอิงในสกิลเป็น **illustrative** — ยึดค่าจริงของแล็บ/ตำราเสมอ

## License

MIT — ใช้ฟรี / แก้ได้ / share ได้

## Contributing

อยากเพิ่ม skill ของตัวเอง / ปรับปรุงของเดิม? ดู [CONTRIBUTING.md](./CONTRIBUTING.md) — เล่าปัญหาหรือวิจารณญาณในสายงานคุณมาได้เลย

## Credits

โดย **Phanuphong Tameesak — MT Score UP!** เพื่อชุมชน MT ไทย
ส่วนหนึ่งของ **Score UP** ecosystem
