# MT Score UP — Skills Hub สำหรับ MT ไทย

แหล่งรวม **"สกิล" + เครื่องมือฟรี** สำหรับ Medical Technologist (MT) ไทย — เอาไปวางในแชต AI ที่คุณมีอยู่แล้ว (Claude / ChatGPT / Gemini) ใช้ได้เลย **ไม่ต้องติดตั้ง ไม่ต้องจ่ายค่า token เพิ่ม**

> แนวคิด: แพ็ก **"วิจารณญาณ" ของ MT ที่เก่งแล้ว** ให้กลายเป็นไฟล์ที่ใครก็หยิบไปใช้ได้ — ไม่ใช่แค่ "ความรู้" (ตำรา/AI มีอยู่แล้ว) แต่คือ **"เลือกอะไรเมื่อไหร่ + กับดักที่มือใหม่ไม่รู้"**

---

> ⚠️ **เพื่อการศึกษา / ช่วยคิดเท่านั้น — NOT FOR CLINICAL USE.** กลุ่มสกิลงานแล็บ (🩸) เป็นกรอบช่วย *ตัดสินใจ/ทบทวน* ไม่ใช่คำสั่งวินิจฉัย/รักษา และไม่รับประกันความถูกต้อง — การใช้กับผู้ป่วยจริงต้องอิง SOP + วิจารณญาณของ MT/แพทย์ผู้มีใบประกอบวิชาชีพเสมอ · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้

## 📚 ส่วนที่ 1 — Skills (87 สกิล)

**🧭 ไม่รู้จะใช้ตัวไหน? เริ่มที่นี่:** วาง [`prompts/triage.md`](./prompts/triage.md) ในแชต AI แล้วเล่าปัญหา/เคส/งานวิจัยของคุณ → AI จะบอกว่าใช้ skill ไหน (หรือถ้าคลังยังไม่มี จะช่วยร่างให้ส่งเข้า GitHub)

**วิธีใช้ (รู้แล้วว่าจะใช้ตัวไหน):** เปิดไฟล์ในโฟลเดอร์ [`skills/`](./skills) → copy ทั้งไฟล์ → วางในแชต AI → พิมพ์ปัญหาของคุณ

**ใช้บน platform อื่น** (Custom GPT / Claude Project / Gemini Gem / Claude Code / live-load) → [`docs/USING.md`](./docs/USING.md) — ครบทุกช่องทางใน 1 หน้า

**ยังไม่เห็นภาพ?** ดู [`examples/`](./examples) — skill ทำงานจริง before/after ใน 30 วินาที 👀 · อยากฝึก → [`exercises/`](./exercises)

<sub>🇬🇧 **EN:** Free, portable *judgment skills* for Thai Medical Technologists — paste one markdown file into your AI chat (Claude / ChatGPT / Gemini). No install, no extra cost. Thai-first. See [`examples/`](./examples).</sub>
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
| [urinalysis-judgment](./skills/urinalysis-judgment.md) | ยูริน + body-fluid micro — strip↔micro↔clinical ให้ตรง · cast/crystal · กับดัก strip false +/− |
| [preanalytical-judgment](./skills/preanalytical-judgment.md) | pre-analytical/phlebotomy — ลำดับเจาะ/หลอด/ระบุตัว/ขนส่ง ให้ตัวอย่างเชื่อได้ก่อนถึงเครื่อง |
| [poct-judgment](./skills/poct-judgment.md) | Point-of-care testing — ให้แล็บนอกแล็บเชื่อได้เท่าแล็บกลาง · QC/connectivity/ผู้ใช้นอกสายแล็บ |
| [flow-cytometry-judgment](./skills/flow-cytometry-judgment.md) | flow cytometry — gate ถูก · อ่าน pattern · correlate clinical · กับดัก compensation/artifact |

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
| [literature-review-judgment](./skills/literature-review-judgment.md) | รีวิววรรณกรรมเป็นระบบ: ตั้งคำถาม→ค้นหลายแหล่ง→screen→สังเคราะห์ theme/gap |
| [deep-research](./skills/deep-research.md) | ค้นเรื่องใดก็ได้ลึก หลายแหล่ง + cross-check ≥2 แหล่งอิสระ + cite ตรวจได้ |
| [source-credibility-judgment](./skills/source-credibility-judgment.md) | ประเมินความน่าเชื่อแหล่ง/ผู้เขียน — peer-review tier · CoI · predatory journal · primary vs secondary |
| [pubmed-search-judgment](./skills/pubmed-search-judgment.md) | ค้น PubMed ให้เจอของจริง — MeSH vs keyword · query/filter · กับดัก search + แต่ง PMID |
| [method-validation-stats](./skills/method-validation-stats.md) | สถิติ validate วิธี: method comparison (Bland-Altman/Deming) · reference interval · diagnostic accuracy (≠ research stats) |

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
| [ab-test-judgment](./skills/ab-test-judgment.md) | วัด prompt/skill ดีขึ้นจริงไหม ไม่ไล่จับ noise: control + delta-of-deltas · noise floor · review vs A/B · scaling |
| [prompt-optimizer](./skills/prompt-optimizer.md) | เขียน/ซ่อม prompt ให้ AI ตอบตรง — แก้สาเหตุที่ใช่ก่อน · few-shot · สเปก output · ไม่ยัดยาวเฟ้อ |
| [verification-panel](./skills/verification-panel.md) | ตั้งคณะตรวจ 3 มุม (Factual/Logic/Context) หักล้างก่อนเชื่อคำตอบ high-stakes |
| [write-a-skill](./skills/write-a-skill.md) | แพ็กวิจารณญาณคุณเป็น skill — judgment ไม่ใช่ knowledge · เลือก type · ส่งเข้า repo |
| [token-budget-judgment](./skills/token-budget-judgment.md) | คุมบริบท AI — เมื่อไหร่แตกงาน/สรุป/reset · สัญญาณบริบทล้น (AI ลืม/วน) |

### 💬 สื่อสาร
| skill | ช่วยอะไร |
|---|---|
| [polite-but-clear](./skills/polite-but-clear.md) | ปรับถ้อยคำให้สุภาพแต่ยังได้ใจความ |
| [explain-simply](./skills/explain-simply.md) | อธิบายเรื่องยากแบบเด็ก ป.3 (ไม่ผิด) |
| [content-creator-judgment](./skills/content-creator-judgment.md) | เลือกหัวข้อคอนเทนต์ให้ความรู้ + ไม่ทำให้เพจตาย |
| [photography-judgment](./skills/photography-judgment.md) | ถ่ายภาพ/วิดีโอ + photomicrography (สไลด์/colony/gel): exposure/DOF/composition/WB |
| [humanize-ai-writing](./skills/humanize-ai-writing.md) | เกลางานที่ AI ร่างให้เป็นคนเขียน — ตัดสัญญาณ AI โดยคงความถูกต้อง/ศัพท์เทคนิค |
| [writing-judgment](./skills/writing-judgment.md) | เขียนงานยาวมีโครง+น้ำเสียง — เลือกโครงตามผู้อ่าน · hook · ตัดน้ำ (≠ manuscript วิชาการ) |
| [report-up-judgment](./skills/report-up-judgment.md) | สื่อสารขึ้นบน/ผู้บริหาร — bottom-line first · แปลเทคนิค→ผลกระทบ · ขอ decision ชัด · escalate NC |

### 🧭 ชีวิต / อาชีพ
| skill | ช่วยอะไร |
|---|---|
| [ikigai-finder](./skills/ikigai-finder.md) | หา ikigai แบบไม่หลอกตัวเอง |
| [self-development-coach](./skills/self-development-coach.md) | โค้ชพัฒนาตัวเองแบบตรงไปตรงมา |
| [know-yourself](./skills/know-yourself.md) | สัมภาษณ์ตัวเองให้ลึก → master profile ที่ reuse ได้ (resume/LinkedIn/สัมภาษณ์/pivot) |
| [mt-career-judgment](./skills/mt-career-judgment.md) | เส้นทางอาชีพ MT: bench→industry/commercial/AI · ladder+โครงรายได้+skill gap · T-shaped Data&AI · เป็นเจ้าของแล็บ |
| [digital-judgment](./skills/digital-judgment.md) | privacy/PDPA/security/ลิขสิทธิ์/ลงทุน — ไม่โดนหลอก |
| [finance-judgment](./skills/finance-judgment.md) | การเงิน/ลงทุน/อ่านงบ/ธุรกิจ — ลำดับเงิน + กันกับดัก/scam + เลนส์ econ |
| [financial-statement-judgment](./skills/financial-statement-judgment.md) | อ่านงบ 5 ฉบับ + ลำดับอ่าน + คุณภาพกำไร (CFO) + จับ window-dressing/OCI |
| [mt-law-ethics-judgment](./skills/mt-law-ethics-judgment.md) | กฎหมาย/จรรยาบรรณ MT: ใบอนุญาต · ขอบเขตวิชาชีพ · ความลับ/PDPA · เครื่องมือแพทย์ |
| [mt-exam-strategy-judgment](./skills/mt-exam-strategy-judgment.md) | กลยุทธ์สอบใบประกอบฯ MT: blueprint/บริหารเวลา · จับ distractor · study ROI |
| [grill-my-plan](./skills/grill-my-plan.md) | ให้ AI ซักไซ้แผนก่อนลงมือ — หาจุดอ่อน/worst-case/เกณฑ์ตัดสิน ก่อน decision แก้ยาก |
| [pomodoro-focus](./skills/pomodoro-focus.md) | โฟกัสแบบ Pomodoro สำหรับคนเข้าเวร — เลือก cycle ตามงาน/พลังงาน · เมื่อไหร่ไม่ควรใช้ |
| [time-blocking](./skills/time-blocking.md) | จัดเวลาแบบ time-blocking รอบเวร — จัดทุก ชม. · งานหนักตรงพลังงานสูง · เผื่อ buffer/เดินทาง |
| [interactive-course](./skills/interactive-course.md) | ให้ AI ติว interactive ทีละขั้น — explain→ถาม→ปรับระดับ · recall > อ่านซ้ำ · cross-check |

### 💼 บริหารแล็บ / ขาย IVD
| skill | ช่วยอะไร |
|---|---|
| [lab-management-judgment](./skills/lab-management-judgment.md) | QMS/ISO 15189 · QC strategy (sigma/IQCP) · งบ · verification · inventory |
| [ivd-sales-judgment](./skills/ivd-sales-judgment.md) | ขาย IVD/diagnostics — ขายผลลัพธ์บริหาร · budget-pocket · ROI · spec-in |
| [crm-judgment](./skills/crm-judgment.md) | คิดแบบลูกค้า สำหรับ MT สาย sales/คลินิก/แอป |
| [marketing-judgment](./skills/marketing-judgment.md) | กลยุทธ์การตลาด B2B: STP · buying center · pricing · positioning · push/pull |
| [sales-psychology-judgment](./skills/sales-psychology-judgment.md) | จิตวิทยาขาย/อ่านคน: แรงจูงใจ · active listening · trust · โน้มน้าว(+จริยธรรม) · เจรจา |
| [lab-clinic-business-judgment](./skills/lab-clinic-business-judgment.md) | เปิด/บริหารคลินิกแล็บ MT เอง: เลือกโมเดล · moat (วิชาชีพ+จดทะเบียน+LIS-HIS) · รายได้รัฐ · อ่านใจ buyer · unit economics |
| [dx-company-brief](./skills/dx-company-brief.md) | ทำ brief บริษัท diagnostics ก่อนสัมภาษณ์/ขาย — portfolio/ตลาด/ลูกค้า/มุมขาย + verify |
| [market-research-judgment](./skills/market-research-judgment.md) | วิจัยตลาด/คู่แข่ง — TAM/SAM/SOM · top-down vs bottom-up · แหล่งเชื่อได้ vs marketing |
| [lead-intelligence-judgment](./skills/lead-intelligence-judgment.md) | หา+คัดกรอง lead B2B — signal scoring · mutual fit · warm path · follow-up + PDPA |
| [incident-postmortem-judgment](./skills/incident-postmortem-judgment.md) | ถอดบทเรียนหลังเหตุ + CAPA — blameless RCA (5-why) · root vs symptom · ป้องกันซ้ำที่ระบบ |

### 💻 โค้ด / เทคนิค / data
| skill | ช่วยอะไร |
|---|---|
| [python-coach](./skills/python-coach.md) | เลือกเครื่องมือ + ไม่ตกหลุม Python |
| [db-judgment](./skills/db-judgment.md) | ตัดสินใจ SQL / ออกแบบ DB ไม่ให้ระเบิด |
| [ml-judgment](./skills/ml-judgment.md) | เลือกโมเดล/metric/validation ML + เลี่ยงกับดัก |
| [cv-judgment](./skills/cv-judgment.md) | เลือกเทคนิควิเคราะห์ภาพ + เลน blood smear/เซลล์ |
| [optimization-judgment](./skills/optimization-judgment.md) | เลือกวิธี optimize (LP/heuristic/sim) จัดเวร/ทรัพยากร |
| [data-project-survival](./skills/data-project-survival.md) | โปรเจกต์ data/ML ไม่ให้ล้ม + ประเมิน vendor |
| [data-science-workflow](./skills/data-science-workflow.md) | เดินโปรเจกต์ DS ตาม CRISP-DM — อยู่ phase ไหน/loop เมื่อไหร่ · กัน data leakage |
| [ml-engineering-workflow](./skills/ml-engineering-workflow.md) | นำโมเดลขึ้นใช้จริง: reproducible train · shadow/A-B · monitor drift · rollback |
| [tdd-judgment](./skills/tdd-judgment.md) | เขียนเทสต์ให้คุ้ม + TDD — เทสต์อะไรก่อน · mock/coverage เป็นเครื่องมือ · เทสต์ผ่านแต่ไม่จับบั๊ก |
| [debugging-judgment](./skills/debugging-judgment.md) | ดีบักมีวินัย — reproduce→trace→falsify→cross-ref · หา root cause ไม่ใช่ปะ symptom |
| [ai-coding-guardrails](./skills/ai-coding-guardrails.md) | กันกับดักให้ AI เขียนโค้ด — ขอบเขตแคบ · surgical edit · success ที่ตรวจได้ · กัน over-engineer |
| [spreadsheet-judgment](./skills/spreadsheet-judgment.md) | ใช้ Excel/Sheets ให้ถูก + กัน silent error (date/auto-convert/copy เพี้ยน) ในข้อมูลแล็บ |
| [mt-databases](./skills/mt-databases.md) | เก็บข้อมูล MT: Sheets vs Access vs SQL เลือกเมื่อไหร่ · structure กันพัง · backup/สิทธิ์ |

### 🗂️ จัดการ
| skill | ช่วยอะไร |
|---|---|
| [never-lose-a-file](./skills/never-lose-a-file.md) | จัดไฟล์ให้เป็นระเบียบ แล้วไม่หายอีก |
| [phi-data-handling](./skills/phi-data-handling.md) | จัดการข้อมูลคนไข้/PHI — จัดระดับข้อมูล · de-identify ให้จริง · PDPA/IRB · ช่องทางแชร์ปลอดภัย |

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

## 🔄 ก๊อป (แช่แข็ง) vs โหลดสด (auto-sync)

skill เป็นไฟล์ — มี 2 วิธีโหลด เลือกตามงาน:
- **ก๊อปเนื้อไฟล์** → snapshot **แช่แข็ง**: เสถียร, cite เวอร์ชันใน audit trail ได้, ไม่เปลี่ยนกลางคัน (เหมาะงานคลินิก)
- **โหลดสด (live link)** → บอก AI ที่ต่อเน็ตได้ว่า *"ดึง skill จาก `<raw URL>` มาใช้"* → ได้ `main` ล่าสุด**ทุกครั้ง = auto-sync** ไม่ต้องก๊อปใหม่ · รายการ URL ทั้งหมด → [`skills/INDEX.md`](./skills/INDEX.md) (CI อัปเดตอัตโนมัติ)
- **ทุก skill ทีเดียว (AI เลือกใช้เอง)** → [`dist/all-skills.md`](./dist/all-skills.md) — รวม 87 ตัวในไฟล์เดียว (~133K tokens) · ก๊อป/โหลดสดก็ได้ · AI self-route ตามคำถาม · **เฉพาะ AI context ใหญ่** (Claude/Gemini/Project, ไม่เหมาะ GPT chat เปล่า)
- ⚠️ live link ใช้ได้เฉพาะ AI ที่ดึง URL ได้ (Claude web · ChatGPT browse · Gemini) — แชตเปล่า offline ใช้ก๊อป

## โครงสร้าง

```
mt-score-up-skill/
├── skills/        # ★ 87 สกิล — copy (แช่แข็ง) หรือโหลดสดผ่าน INDEX.md (auto-sync)
├── examples/      # ★ เห็น skill ทำงานจริง (before/after) — เริ่มที่นี่
├── exercises/     # โจทย์ฝึก ลองเองแล้วเทียบเฉลย
├── dist/          # all-skills.md — รวมทุก skill ไฟล์เดียว (auto-generated)
├── prompts/       # วางในแชต AI
│   ├── triage.md  # 🧭 ไม่รู้ใช้ skill ไหน → เริ่มที่นี่ (catalog auto-updated)
│   ├── skill-interview.md # 🎙️ Skill Maker — AI สัมภาษณ์ถอดวิจารณญาณผู้เชี่ยวชาญ/คนเกษียณ
│   └── system.md  # WI generator (ISO 15189)
├── scripts/       # md→docx · standards recheck · check_duplicates (ดู scripts/README.md)
├── templates/     # (optional) วาง .docx แม่แบบ WI ของแล็บคุณเอง — generator ทำงานได้โดยไม่ต้องมี
├── profiles/      # Layout profile ต่อโรงพยาบาล (generic)
├── inbox/         # Drop WI ตัวอย่าง — AI scan ใช้เป็น template
├── eval/          # วัดผลสกิลจริง: weak-model A/B 3 รอบ + literature + Titanic (ดู eval/ab-scorecard.md)
├── docs/          # USING (ใช้ทุก platform) · LAUNCH (แผนปล่อย) · FEEDBACK · skill-registry-spec · vision · setup-custom-gpt
├── wiki/          # คู่มือเข้าใจโปรเจกต์ลึกขึ้น (รวมลิงก์)
├── contributions/ # พื้นที่ชุมชน — ส่ง skill/เคสจริง (+ INTAKE.md = playbook maintainer)
├── CONTRIBUTORS.md # ผู้ลงขันกองกลาง (credit)
├── STANDARDS.md   # Source-of-truth edition + auto-recheck รายเดือน
└── CHANGELOG.md   # Version history (v0.7.0)
```

## Privacy & ความปลอดภัย

- ✅ ทำงานบน browser / เครื่องของคุณเท่านั้น — ไม่มี server กลาง ไม่เก็บข้อมูล
- ✅ Open source — audit ได้ทุกบรรทัด (MIT)
- ⚠️ **ห้ามใส่ข้อมูล identifying ของคนไข้** (ชื่อ / HN / MRN) — ใช้ generic placeholder
- ⚠️ skill ช่วย "คิด/ร่าง" ไม่ใช่แหล่งความจริงสุดท้าย — เรื่องการแพทย์/สำคัญ ต้องตรวจกับแหล่งทางการ + มนุษย์

## ความปลอดภัย & การ stack สกิล (clinical use)

- **สกิลกลุ่มงานแล็บ (🩸) = ตัวช่วย "คิด" ทางเลือก** — หยิบไปใช้หรือไม่ก็ได้ ไม่ใช่ของบังคับ/ไม่ใช่แหล่งความจริงสุดท้าย · **วิจารณญาณของ MT/แพทย์ผู้ใช้นำเสมอ** มันแค่เสริมตอนอยากได้มุมคิด — verify ก่อนใช้จริงทุกครั้ง
- **โหลดสกิลคลินิก → "ระวัง" ชนะ "สั้น":** ถ้าใช้ [`ai-assistant-calibration`](./skills/ai-assistant-calibration.md) (เน้นตอบสั้น) คู่กับสกิลงานแล็บ (🩸) — **ให้ความรอบคอบ/verify ของสกิลคลินิก override ความสั้นเสมอ** (ความปลอดภัยผู้ป่วย > ความกระชับ)
- **สกิลคลินิกมี guard ในตัว** (`verify-first: decision-support ไม่ใช่คำตอบสุดท้าย`) — และแนะนำวางคู่ [`anti-hallucination`](./skills/anti-hallucination.md) เสมอเมื่อให้ AI ช่วยคิดเรื่องที่กระทบคนไข้ · ทุกขั้นที่กระทบคนไข้ต้องให้ MT/แพทย์ผู้รับผิดชอบยืนยันก่อนลงมือ
- **disclaimer แบ่งระดับตามความเสี่ยง (by design ไม่ใช่ copy-paste):** ผิดแล้วกระทบคนไข้ (bloodbank / toxicology / molecular / clinical-correlation / งานแล็บ) = disclaimer หนัก + guard ในตัว · จัดไฟล์/สื่อสาร/วางแผน = disclaimer สั้นตามบริบท

## วัดผลสกิล (eval) — อยากรู้ตัวไหนพิสูจน์แล้ว?

ทดสอบจริง: ให้ **model อ่อน (Haiku)** ตอบโจทย์กับดัก *มี* vs *ไม่มี* สกิล → กรรมการตาบอดให้คะแนน (3 รอบ + เทียบ literature + ตัวอย่างโค้ด Titanic). ผลต่อสกิล → [`eval/ab-scorecard.md`](./eval/ab-scorecard.md) · [`eval/round3/`](./eval/round3/) · วิธี/ข้อจำกัด → [`eval/METHOD.md`](./eval/METHOD.md) · [`eval/RESULTS.md`](./eval/RESULTS.md)

อ่านเป็น **grade-book ไม่ใช่ leaderboard** — และนี่คือเหตุผลที่เรา **ไม่ตีเกรด A-F ต่อสกิล**:

- **ตัวเลขมี noise** (วัดซ้ำต่างกันเฉลี่ย ~1.4 จุดบนโจทย์เดียวกัน) → delta ต้องเกิน ~1.4 ถึงเชื่อ. มี **8 ตัว "bulletproof"** ที่ยกคะแนนนิ่งหลายรอบ = เชื่อได้สุด
- **"เสมอ (tie)" ≠ แย่** — แปลว่า AI ตอบถูกเองในโจทย์นั้นอยู่แล้ว; ค่าจริงของสกิลอยู่ที่ **ความสม่ำเสมอ + เคสยาก (edge case) + ช่วยคนที่ยังไม่เชี่ยว/model อ่อน** (frontier model ไม่ต้องใช้ก็ได้)
- **0 regression อันตราย** ใน 53 ตัว — ไม่มีสกิลไหนทำให้ตอบ "พังลง" <sub>(eval เต็มรูป blind-judge รันบน 53 สกิล; อีก 34 ที่เพิ่มภายหลังผ่าน **spot-A/B screen** ครบแล้ว — [`round4`](./eval/round4-new-skills.md) (8) + [`round5`](./eval/round5-remaining.md) (26) · **ทั้งคลัง 87 = 0 dangerous regression** · screen เบากว่า round 1-3)</sub>

## ที่มา & การอ้างอิง (Sources)

- **ที่มา:** ผมสกัดจากที่เรียน ฝึกงาน และประสบการณ์หน้างาน — เก็บ "วิจารณญาณ" (เลือกอะไรเมื่อไหร่ + กับดัก) เรียบเรียงใหม่ ไม่ใช่ลอกสไลด์/ตำรามาตรง
- ตัวเลข/ค่าอ้างอิง = **illustrative** ยึดของแล็บ/ตำราจริงเสมอ · มาตรฐาน (ISO 15189:2022 · ISO 15190:2020 · AABB Tech Manual 21st / Standards 35th) อ้าง **หัวข้อ/edition** ไม่ได้คัดเนื้อความมา (ดู [`STANDARDS.md`](./STANDARDS.md))
- **เจอจุดไหนคล้ายแหล่งมีลิขสิทธิ์เกินไป หรือผิด — เปิด issue บอกได้ จะแก้/ถอดให้**

## License

MIT — ใช้ฟรี / แก้ได้ / share ได้

## Contributing

อยากเพิ่ม skill ของตัวเอง / ปรับปรุงของเดิม? ดู [CONTRIBUTING.md](./CONTRIBUTING.md) — เล่าปัญหาหรือวิจารณญาณในสายงานคุณมาได้เลย

> **ไม่มี GitHub ก็ส่งได้** และ **ไม่ต้องเขียนให้สวย** — ส่งทางเพจ Score UP (Google Form ⏳ กำลังเปิด) → maintainer + AI เรียบเรียงเป็น skill ให้ (มี [prompt ตัวช่วยร่างด้วย AI](./CONTRIBUTING.md#-ตัวช่วยร่างด้วย-ai) แปะใช้ได้เลย)

> 🎙️ **เป็นผู้เชี่ยวชาญ/ใกล้เกษียณ ไม่ถนัดเขียน?** วาง [`prompts/skill-interview.md`](./prompts/skill-interview.md) (Skill Maker) ในแชต AI → มันสัมภาษณ์ถอดวิจารณญาณของคุณเป็นร่าง skill ให้เอง · ผู้ลงขันได้ credit ใน [`CONTRIBUTORS.md`](./CONTRIBUTORS.md)
>
> 💬 เจอจุดผิด หรืออยากบอกว่า skill ช่วย/ไม่ช่วยของจริง → [`docs/FEEDBACK.md`](./docs/FEEDBACK.md)

## Credits

โดย **Phanuphong Tameesak — MT Score UP!** เพื่อชุมชน MT ไทย
ส่วนหนึ่งของ **Score UP** ecosystem

**ขอบคุณ** ครูบาอาจารย์เทคนิคการแพทย์และพี่ๆ MT หน้างานที่ปูพื้นฐานวิชาชีพให้ผม 🙏 ส่วนสกิลด้านอื่น (วิจัย/การเงิน/ขาย/AI ฯลฯ) มาจากการเรียนรู้และประสบการณ์ข้ามสายงานของผมเอง — *เป็นโปรเจกต์ส่วนตัว ไม่ได้เป็นตัวแทนหรือรับรองโดยสถาบันใด*
