# Skills — คลังวิจารณญาณ MT

**36 สกิล** ที่แพ็ก "วิจารณญาณ" (judgment) ของ MT ให้พกพาได้ — copy ทั้งไฟล์ไปวางในแชต AI ที่คุณใช้อยู่ (Claude / ChatGPT / Gemini) แล้วพิมพ์ปัญหาของคุณ

> skill พวกนี้ไม่ได้เพิ่ม "ความรู้" ให้ AI (ตำรามีหมดแล้ว) — มันให้ **"เลือกอะไรเมื่อไหร่ + กับดักที่มือใหม่ไม่รู้"** ซึ่งเป็นส่วนที่ AI ทั่วไปทำพลาดบ่อย

## อ่านหัวไฟล์ก่อนใช้
แต่ละ skill มี frontmatter บอก:
- **type** — `ADVISE` (ให้คำแนะนำ) · `DO` (ต้องรันจริง เช่นคำนวณ) · `CALIBRATION` (ปรับวิธีทำงานของ AI)
- **needs** — `any` (AI ตัวไหนก็ได้) · `code-interpreter` (ต้องรัน Python ได้) · `persistent-memory` (ต้องจำข้ามวันได้)

---

## รายการ

### 🩸 งานแล็บ (Lab bench)
- **bloodbank-judgment** — ตัดสินใจหน้างานธนาคารเลือด (CLERICAL ก่อน · ABO discrepancy 8 เคส · antibody ID · crossmatch IS/AHG/electronic · เมื่อไหร่ irradiate · transfusion reaction) — patient-safety สูงสุด
- **hematology-judgment** — อ่าน CBC/smear/coag (review smear เมื่อไหร่ · anemia ตาม MCV · blast=urgent · thal vs IDA · PT/aPTT + mixing test · platelet จริงหรือ pseudo)
- **clinchem-judgment** — accept/reject QC run (Westgard) · interference HIL กระทบ analyte ไหน · critical value · recalibrate vs troubleshoot · dilute/repeat/report
- **clinmicro-judgment** — เชื้อจริง vs contaminate · ID workflow + เมื่อไหร่พอ · อ่าน AST (ESBL/MRSA/inducible-clinda/CRE) · เลือก media/atmosphere · culture vs molecular
- **immunoassay-judgment** — เลือก format (sandwich/competitive/CLIA/lateral flow) · อ่าน HBV/HIV/syphilis/ANA panel · prozone/hook/window/confirm
- **molecular-judgment** — เลือก method detect variant (RFLP/ASO/HRM/Sanger/NGS) · real-time chemistry · แปล Ct/melt valid-invalid · กัน contamination/false-neg · HLA typing · pharmacogenomics
- **pathology-judgment** — อ่าน pattern: benign/malignant (5 แกน) · cell injury reversible/irreversible · necrosis type · acute/chronic อักเสบ · grading/staging · dysplasia→cancer (basement membrane) · granuloma/hypersensitivity
- **parasitology-judgment** — เลือก concentration/stain ตามเป้า · malaria thick vs thin + ตรวจซ้ำ · single-stool false-neg · artifact vs parasite
- **toxicology-judgment** — screen vs confirm · antidote tree (OP/carbamate/paraquat/โลหะ) · chelator คู่โลหะ · RBC-AChE vs plasma ChE · TDM timing · chain of custody
- **clinical-correlation-judgment** — อ่านผลแล็บข้ามแขนง (hema+chem+micro+immuno+BB) → ร้อยเป็นภาพเดียว ตั้ง DDx/ชี้ทางให้แพทย์ (pivotal value → DDx → rule-out → cause-effect chain) · *MT ไม่วินิจฉัย*

### 🔬 งานวิจัย / สถิติ (R2R)
- **r2r-research-proposal** — ปั้นโจทย์วิจัยจากปัญหา → คำถาม → objective + เช็คคู่ objective↔method
- **choose-stat-test** — decision tree เลือก statistical test จาก 3 คำถาม (เป้าหมาย × ชนิด outcome × กี่กลุ่ม)
- **sample-size-power** — หาขนาดตัวอย่าง N ด้วย power analysis + สูตร + ตัวอย่างมีเลข
- **r2r-stats** — ผู้ช่วยรัน/แปลผลสถิติ R2R + กับดัก lab (method comparison ≠ validation ฯลฯ) `needs: code-interpreter`

### 🤖 ใช้ AI อย่างคม / ปลอดภัย
- **ai-assistant-calibration** — ปรับ "นิสัยการตอบ" ของ AI ให้คม ตรงสไตล์คุณ `CALIBRATION`
- **ai-agent-team** — ตั้ง AI เป็นทีมผู้เชี่ยวชาญหลายตำแหน่ง + หัวหน้าคอย route/รวบ `CALIBRATION`
- **self-improving-agent** — ให้ agent จดบทเรียนจากความผิดพลาด เก่งขึ้นข้ามวัน `needs: persistent-memory`
- **what-skill-do-i-need** — วินิจฉัยว่าคุณต้องการอะไรจริงๆ (skill? tool? ลงมือ? คนจริง?)
- **offload-to-automation** — งานที่ต้องเป๊ะ (เลข/จัดเวร) โยนให้ code AI เป็นคนคุม+ตรวจ `CALIBRATION`
- **anti-hallucination** — กัน + จับ AI มั่วข้อเท็จจริง/ตัวเลข/citation (สำคัญสายแพทย์) `CALIBRATION`
- **progress-tracker** — วางคู่สกิลไหนก็ได้ → AI โชว์ความคืบหน้าเป็น checklist/flowchart (ทำถึงไหน·เลือกกิ่งไหน) `CALIBRATION`

### 💬 สื่อสาร
- **polite-but-clear** — ปรับข้อความห้วน/แรง → สุภาพ แต่ยังได้ใจความ (ปฏิเสธ/ตักเตือน/แย้งหัวหน้า)
- **explain-simply** — อธิบายเรื่องยากแบบเด็ก ป.3 — ง่ายแต่ห้ามผิด (โดยเฉพาะเรื่องแพทย์)
- **content-creator-judgment** — เลือกหัวข้อคอนเทนต์ให้ความรู้ (มี hook ไหม/จับเทรนด์ตอนไหน) + ไม่ทำให้เพจตาย

### 🧭 ชีวิต / อาชีพ
- **ikigai-finder** — หา ikigai แบบไม่หลอกตัวเอง → จบที่ "1 การทดลอง" ไม่ใช่ลาออกตามฝัน
- **self-development-coach** — โค้ชพัฒนาตัวเองแบบตรงไปตรงมา ไม่ปลอบใจลอยๆ
- **crm-judgment** — คิดแบบลูกค้า (segment/CLV 2×2/CF-CBF/วิกฤต PR) สำหรับ MT สาย sales/คลินิก/แอป
- **digital-judgment** — privacy/PDPA/de-identify/security/ลิขสิทธิ์/ลงทุนออนไลน์ — ตัดสินใจปลอดภัย ไม่โดนหลอก
- **finance-judgment** — การเงิน/ลงทุน/ธุรกิจ (บันไดเงิน · asset ตาม horizon · อ่านงบ/CFO · valuation · หนี้ดี-เลว · go/pivot · จับ scam)

### 💻 โค้ด / เทคนิค / data
- **python-coach** — เลือก data structure/วิธี + กับดัก Python (.sort() คืน None, mutable default ฯลฯ)
- **db-judgment** — ตัดสินใจ JOIN/index/normalize + กับดัก SQL (DELETE ไม่มี WHERE, NOT IN+NULL ฯลฯ)
- **ml-judgment** — เลือก paradigm/classifier/metric/validation (6 decision forks) + กับดัก ML (leakage, tune บน test)
- **cv-judgment** — เลือกเทคนิควิเคราะห์ภาพ (preprocess/edge/feature/classical-vs-deep/segment) + เลน blood-smear/cell ML
- **optimization-judgment** — เลือกวิธี optimize (LP vs heuristic vs simulation) + อ่าน shadow price + กับดัก (ลืม constraint)
- **data-project-survival** — รันโปรเจกต์ data/ML ตาม CRISP-DM (9 จุดตัดสินใจ: phase/goal/missing/scale/SMOTE/eval) + ประเมิน vendor

### 🗂️ จัดการ
- **never-lose-a-file** — ระบบจัดไฟล์ให้เป็นระเบียบ แล้วไม่หายอีก

---

## 🔗 Combos — ใช้สกิลเป็นชุด (พลังจริงอยู่ตอนต่อกัน)

> สกิลเดี่ยวก็ใช้ได้ แต่ของจริงคือ **ต่อกันเป็นสาย** — วางหลายไฟล์พร้อมกันในแชต แล้วบอก AI ว่าจะทำงานแบบไหน

**🩸 อ่านผลแล็บ → correlate + ชี้ทาง (ส่งต่อแพทย์วินิจฉัย)**
`clinical-correlation-judgment` (ร้อยผลข้ามแขนง → ตั้ง DDx/flag) → สกิลแล็บเฉพาะทาง (`hematology`/`clinchem`/`clinmicro`/`immunoassay`/`bloodbank`/`molecular`/`pathology`...) → `anti-hallucination` (กันมั่วค่า/อ้างอิง) → `explain-simply` (สื่อสารผล/อธิบายในขอบเขต)
*confirm lane:* reactive screen → `immunoassay-judgment` + `molecular-judgment` (ยืนยัน) · ⚠️ **MT ตีความ/flag/ส่งต่อ — การวินิจฉัยเป็นหน้าที่แพทย์**

**🔬 ทำวิจัย R2R ครบวงจร**
`r2r-research-proposal` → `choose-stat-test` → `sample-size-power` → `r2r-stats` → `polite-but-clear` (ตอบ reviewer) + `explain-simply` (อธิบายผลให้คนทั่วไป)

**💻 โปรเจกต์ data/ML**
`data-project-survival` (วางโครง) → `ml-judgment` (เลือกโมเดล/metric) → `cv-judgment` (ถ้าเป็นภาพ) → `python-coach`/`db-judgment` (เขียนจริง) → `offload-to-automation` + `anti-hallucination` (กันพลาด + verify)

**🤖 ใช้ AI ให้คม + ปลอดภัย**
`what-skill-do-i-need` (ขาดอะไร) → `ai-assistant-calibration` (ตั้งนิสัย) → `ai-agent-team` (ตั้งทีม) → `offload-to-automation` + `anti-hallucination` (กันพลาด) → `self-improving-agent` (เก่งขึ้นข้ามวัน)

**💬 ทำคอนเทนต์ / สื่อสาร**
`content-creator-judgment` (เลือกหัวข้อ) → `explain-simply` (ทำให้ง่าย) → `anti-hallucination` (อย่ามั่ว) → `polite-but-clear` (ปรับโทน)

**🧭 ตัดสินใจชีวิต / อาชีพ**
`what-skill-do-i-need` → `ikigai-finder` (ทิศทาง) → `self-development-coach` (ลงมือโต) → `crm-judgment`/`finance-judgment` (สาย sales/ธุรกิจ) + `digital-judgment` (PDPA/กัน scam)

**🛠️ จัดการงาน / ทรัพยากร**
`never-lose-a-file` (จัดไฟล์) + `optimization-judgment` (จัดเวร/จัดสรร) + `offload-to-automation` (อัตโนมัติ)

> เคล็ด: ไม่รู้จะเริ่ม combo ไหน → เริ่มที่ `what-skill-do-i-need` · อยากให้ AI route เอง → ใช้ `ai-agent-team` เป็นหัวหน้าทีม · **อยากเห็น AI ทำถึงไหน → วาง `progress-tracker` คู่ combo ไหนก็ได้**

---

## รูปแบบไฟล์ (สำหรับคนอยากเพิ่ม skill)
ทุก skill ใช้โครงเดียวกัน: frontmatter → ใช้เมื่อ → วิธีใช้ → วิธีทำ (AI ทำตาม) → กับดัก (Anti-patterns) → ช่องผู้เชี่ยวชาญเติม → disclaimer
ดูวิธี contribute ที่ [../CONTRIBUTING.md](../CONTRIBUTING.md)
