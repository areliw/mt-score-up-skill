# MT Score UP — Skills Hub สำหรับ MT ไทย

แหล่งรวม **"สกิล" + เครื่องมือฟรี** สำหรับ Medical Technologist (MT) ไทย — เอาไปวางในแชต AI ที่คุณมีอยู่แล้ว (Claude / ChatGPT / Gemini) ใช้ได้เลย **ไม่ต้องติดตั้ง ไม่ต้องจ่ายค่า token เพิ่ม**

> แนวคิด: แพ็ก **"วิจารณญาณ" ของ MT ที่เก่งแล้ว** ให้กลายเป็นไฟล์ที่ใครก็หยิบไปใช้ได้ — ไม่ใช่แค่ "ความรู้" (ตำรา/AI มีอยู่แล้ว) แต่คือ **"เลือกอะไรเมื่อไหร่ + กับดักที่มือใหม่ไม่รู้"**

---

## ⚡ เห็นภาพใน 10 วินาที — judgment ไม่ใช่ความรู้

ให้ AI ช่วยเขียนโค้ดเทรนโมเดลทำนายจากชุดข้อมูล (Titanic) แล้ววัด ROC-AUC:

| | ผลที่**วัดได้จริง** |
|---|---|
| 🤖 **AI เปล่า** | เลือก feature จากข้อมูล*ทั้งก้อน*ก่อนแบ่ง train/test → **AUC 0.850** สวยมาก ✨ *(แต่ปลอม — ข้อมูล test รั่วเข้าตอนเลือก feature)* |
| 🔬 **+ [`ml-judgment`](./skills/ml-judgment.md)** | "นั่นคือ **data leakage** — เลือก feature/scale **ภายใน CV fold** เท่านั้น" → **AUC 0.819** ที่ไม่หายตอนเจอข้อมูลจริง |

กับดักนี้อันตรายเพราะ **ทางผิดให้คะแนน *สูงกว่า*** — 0.031 AUC ที่ปลอมขึ้นมา คือเลขที่จะไปอยู่บนสไลด์/เปเปอร์ แล้วโมเดลพังตอน deploy โดยไม่รู้ตัว 👈
**วัดจริง ทำซ้ำได้** (data + โมเดลเดียวกัน ต่างแค่จุดที่เลือก feature) → [`eval/titanic/`](./eval/titanic) · ตัวอย่าง before/after เพิ่ม → [`examples/`](./examples)

---

> ⚠️ **เพื่อการศึกษา / ช่วยคิดเท่านั้น — NOT FOR CLINICAL USE.** กลุ่มสกิลงานแล็บ (🩸) เป็นกรอบช่วย *ตัดสินใจ/ทบทวน* ไม่ใช่คำสั่งวินิจฉัย/รักษา และไม่รับประกันความถูกต้อง — การใช้กับผู้ป่วยจริงต้องอิง SOP + วิจารณญาณของ MT/แพทย์ผู้มีใบประกอบวิชาชีพเสมอ · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้

## 📚 ส่วนที่ 1 — Skills (93 สกิล)

**🧭 ไม่รู้จะใช้ตัวไหน? เริ่มที่นี่:** วาง [`prompts/triage.md`](./prompts/triage.md) ในแชต AI แล้วเล่าปัญหา/เคส/งานวิจัยของคุณ → AI จะบอกว่าใช้ skill ไหน (หรือถ้าคลังยังไม่มี จะช่วยร่างให้ส่งเข้า GitHub)

**วิธีใช้ (รู้แล้วว่าจะใช้ตัวไหน):** เปิดไฟล์ในโฟลเดอร์ [`skills/`](./skills) → copy ทั้งไฟล์ → วางในแชต AI → พิมพ์ปัญหาของคุณ

**ใช้บน platform อื่น** (Custom GPT / Claude Project / Gemini Gem / Claude Code / live-load) → [`docs/USING.md`](./docs/USING.md) — ครบทุกช่องทางใน 1 หน้า

**ยังไม่เห็นภาพ?** ดู [`examples/`](./examples) — skill ทำงานจริง before/after ใน 30 วินาที 👀 · อยากฝึก → [`exercises/`](./exercises)

<sub>🇬🇧 **EN:** Free, portable *judgment skills* for Thai Medical Technologists — paste one markdown file into your AI chat (Claude / ChatGPT / Gemini). No install, no extra cost. Thai-first. See [`examples/`](./examples).</sub>
รายการเต็ม + คำอธิบายอยู่ที่ [`skills/README.md`](./skills/README.md)

### 💻 โค้ด / เทคนิค / data
| skill | ช่วยอะไร |
|---|---|
| [python-coach](./skills/python-coach.md) | เลือกเครื่องมือ + ไม่ตกหลุม Python |
| [db-judgment](./skills/db-judgment.md) | ตัดสินใจ SQL / ออกแบบ DB ไม่ให้ระเบิด |
| [ml-judgment](./skills/ml-judgment.md) | เลือกโมเดล/metric/validation ML + เลี่ยงกับดัก |
| [cv-judgment](./skills/cv-judgment.md) | เลือกเทคนิควิเคราะห์ภาพ + เลน blood smear/เซลล์ |
| [optimization-judgment](./skills/optimization-judgment.md) | เลือกวิธี optimize (LP/heuristic/sim) จัดเวร/ทรัพยากร |
| [data-project-survival](./skills/data-project-survival.md) | โปรเจกต์ data/ML ไม่ให้ล้ม + ประเมิน vendor |
| [data-science-workflow](./skills/data-science-workflow.md) | เดินโปรเจกต์ DS ตาม CRISP-DM — อยู่ phase ไหน + กัน data leakage |
| [ml-engineering-workflow](./skills/ml-engineering-workflow.md) | นำโมเดลขึ้นใช้จริง — train ซ้ำได้ + monitor drift/rollback |
| [tdd-judgment](./skills/tdd-judgment.md) | เขียนเทสต์ให้คุ้ม + TDD — เทสต์อะไรก่อน ไม่หลงว่าผ่านแล้วชัวร์ |
| [debugging-judgment](./skills/debugging-judgment.md) | ดีบักมีวินัย — reproduce→trace→falsify หา root cause ไม่ปะ symptom |
| [ai-coding-guardrails](./skills/ai-coding-guardrails.md) | กันกับดักให้ AI เขียนโค้ด — ขอบเขตแคบ + กัน over-engineer |
| [spreadsheet-judgment](./skills/spreadsheet-judgment.md) | ใช้ Excel/Sheets ให้ถูก + กัน silent error ในข้อมูลแล็บ |
| [mt-databases](./skills/mt-databases.md) | เก็บข้อมูล MT — Sheets vs Access vs SQL เลือกเมื่อไหร่ + กันพัง |
| [git-workflow-judgment](./skills/git-workflow-judgment.md) | Git — branch/commit/merge/conflict ไม่ให้งานหาย + กู้ commit ที่หาย |

### 🔬 งานวิจัย / สถิติ (R2R)
| skill | ช่วยอะไร |
|---|---|
| [r2r-research-proposal](./skills/r2r-research-proposal.md) | ปั้นโจทย์วิจัย: ปัญหา → คำถาม → objective |
| [research-design-judgment](./skills/research-design-judgment.md) | เลือก study design + กัน bias/confounder + gate IRB |
| [choose-stat-test](./skills/choose-stat-test.md) | เลือก statistical test ให้ถูกตัว |
| [sample-size-power](./skills/sample-size-power.md) | หาขนาดตัวอย่าง N (power analysis) |
| [r2r-stats](./skills/r2r-stats.md) | รัน + แปลผลสถิติ R2R |
| [manuscript-judgment](./skills/manuscript-judgment.md) | เขียน manuscript/proposal (IMRaD) ให้ผ่าน reviewer |
| [critical-appraisal-judgment](./skills/critical-appraisal-judgment.md) | อ่าน/ประเมินงานวิจัย + หา gap + ประเมิน test (sens/spec/PPV) |
| [literature-review-judgment](./skills/literature-review-judgment.md) | รีวิววรรณกรรมเป็นระบบ — ค้นหลายแหล่ง→screen→สังเคราะห์ theme/gap |
| [deep-research](./skills/deep-research.md) | ค้นเรื่องใดก็ได้ลึก หลายแหล่ง + cross-check ≥2 แหล่งอิสระ |
| [source-credibility-judgment](./skills/source-credibility-judgment.md) | ประเมินความน่าเชื่อแหล่ง/ผู้เขียน — peer-review tier + จับ predatory journal |
| [pubmed-search-judgment](./skills/pubmed-search-judgment.md) | ค้น PubMed ให้เจอของจริง — MeSH vs keyword + กับดัก search |
| [method-validation-stats](./skills/method-validation-stats.md) | สถิติ validate วิธี — method comparison + reference interval (≠ research stats) |

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
| [ab-test-judgment](./skills/ab-test-judgment.md) | วัด prompt/skill ดีขึ้นจริงไหม — ไม่ไล่จับ noise + รู้ noise floor |
| [prompt-optimizer](./skills/prompt-optimizer.md) | เขียน/ซ่อม prompt ให้ AI ตอบตรง — แก้ที่สาเหตุ ไม่ยัดยาวเฟ้อ |
| [verification-panel](./skills/verification-panel.md) | ตั้งคณะตรวจ 3 มุม (Factual/Logic/Context) ก่อนเชื่อคำตอบ high-stakes |
| [write-a-skill](./skills/write-a-skill.md) | แพ็กวิจารณญาณคุณเป็น skill — judgment ไม่ใช่ knowledge + ส่งเข้า repo |
| [token-budget-judgment](./skills/token-budget-judgment.md) | คุมบริบท AI — เมื่อไหร่แตกงาน/สรุป/reset + จับสัญญาณบริบทล้น |

### 💬 สื่อสาร
| skill | ช่วยอะไร |
|---|---|
| [polite-but-clear](./skills/polite-but-clear.md) | ปรับถ้อยคำให้สุภาพแต่ยังได้ใจความ |
| [explain-simply](./skills/explain-simply.md) | อธิบายเรื่องยากแบบเด็ก ป.3 (ไม่ผิด) |
| [content-creator-judgment](./skills/content-creator-judgment.md) | เลือกหัวข้อคอนเทนต์ให้ความรู้ + ไม่ทำให้เพจตาย |
| [photography-judgment](./skills/photography-judgment.md) | ถ่ายภาพ/วิดีโอ + photomicrography (สไลด์/colony/gel) ให้คม |
| [humanize-ai-writing](./skills/humanize-ai-writing.md) | เกลางานที่ AI ร่างให้เป็นคนเขียน — ตัดสัญญาณ AI โดยคงความถูกต้อง |
| [writing-judgment](./skills/writing-judgment.md) | เขียนงานยาวมีโครง+น้ำเสียง — เลือกโครงตามผู้อ่าน (≠ manuscript วิชาการ) |
| [report-up-judgment](./skills/report-up-judgment.md) | สื่อสารขึ้นผู้บริหาร — bottom-line first + แปลเทคนิค→ผลกระทบ |
| [interprofessional-communication-judgment](./skills/interprofessional-communication-judgment.md) | คุยสหวิชาชีพด้วยภาษาของเขา + golden-period: แจ้งเร็วสำคัญกว่าแจ้งครบ |
| [receiving-review-judgment](./skills/receiving-review-judgment.md) | รับรีวิว/คำติ — take/drop/push-back ไม่ caved ไม่ ego + อ่าน nit ทะลุ |

### 🧭 ชีวิต / อาชีพ
| skill | ช่วยอะไร |
|---|---|
| [ikigai-finder](./skills/ikigai-finder.md) | หา ikigai แบบไม่หลอกตัวเอง |
| [self-development-coach](./skills/self-development-coach.md) | โค้ชพัฒนาตัวเองแบบตรงไปตรงมา |
| [know-yourself](./skills/know-yourself.md) | สัมภาษณ์ตัวเองให้ลึก → master profile ที่ reuse ได้ (resume/สัมภาษณ์/pivot) |
| [mt-career-judgment](./skills/mt-career-judgment.md) | เส้นทางอาชีพ MT — bench→industry/commercial/AI + โครงรายได้/skill gap |
| [professional-voice-exit-judgment](./skills/professional-voice-exit-judgment.md) | ไม่เห็นด้วยกับองค์กร/สภาวิชาชีพ → voice/exit/loyalty + อ่าน governance |
| [digital-judgment](./skills/digital-judgment.md) | privacy/PDPA/security/ลิขสิทธิ์/ลงทุน — ไม่โดนหลอก |
| [finance-judgment](./skills/finance-judgment.md) | การเงิน/ลงทุน/อ่านงบ/ธุรกิจ — ลำดับเงิน + กันกับดัก/scam |
| [financial-statement-judgment](./skills/financial-statement-judgment.md) | อ่านงบ 5 ฉบับ + คุณภาพกำไร (CFO) + จับ window-dressing |
| [mt-law-ethics-judgment](./skills/mt-law-ethics-judgment.md) | กฎหมาย/จรรยาบรรณ MT — ใบอนุญาต/ขอบเขตวิชาชีพ + ความลับ/PDPA |
| [mt-exam-strategy-judgment](./skills/mt-exam-strategy-judgment.md) | กลยุทธ์สอบใบประกอบฯ MT — บริหารเวลา/blueprint + จับ distractor |
| [grill-my-plan](./skills/grill-my-plan.md) | ให้ AI ซักไซ้แผนก่อนลงมือ — หาจุดอ่อน/worst-case ก่อน decision แก้ยาก |
| [pomodoro-focus](./skills/pomodoro-focus.md) | โฟกัสแบบ Pomodoro สำหรับคนเข้าเวร — เลือก cycle ตามงาน/พลังงาน |
| [time-blocking](./skills/time-blocking.md) | จัดเวลาแบบ time-blocking รอบเวร — งานหนักตรงพลังงานสูง + เผื่อ buffer |
| [interactive-course](./skills/interactive-course.md) | ให้ AI ติว interactive ทีละขั้น — recall > อ่านซ้ำ + cross-check |

### 💼 บริหารแล็บ / ขาย IVD
| skill | ช่วยอะไร |
|---|---|
| [lab-management-judgment](./skills/lab-management-judgment.md) | QMS/ISO 15189 + QC strategy (sigma/IQCP) + งบ/verification |
| [ivd-sales-judgment](./skills/ivd-sales-judgment.md) | ขาย IVD/diagnostics — ขายผลลัพธ์บริหาร + ROI/spec-in |
| [crm-judgment](./skills/crm-judgment.md) | คิดแบบลูกค้า สำหรับ MT สาย sales/คลินิก/แอป |
| [marketing-judgment](./skills/marketing-judgment.md) | กลยุทธ์การตลาด B2B — STP + pricing/positioning |
| [sales-psychology-judgment](./skills/sales-psychology-judgment.md) | จิตวิทยาขาย/อ่านคน — active listening/trust + โน้มน้าวอย่างมีจริยธรรม |
| [lab-clinic-business-judgment](./skills/lab-clinic-business-judgment.md) | เปิด/บริหารคลินิกแล็บ MT เอง — เลือกโมเดล + moat/unit economics |
| [dx-company-brief](./skills/dx-company-brief.md) | ทำ brief บริษัท diagnostics ก่อนสัมภาษณ์/ขาย — portfolio/ตลาด + verify |
| [market-research-judgment](./skills/market-research-judgment.md) | วิจัยตลาด/คู่แข่ง — TAM/SAM/SOM + แหล่งเชื่อได้ vs marketing |
| [lead-intelligence-judgment](./skills/lead-intelligence-judgment.md) | หา+คัดกรอง lead B2B — signal scoring/mutual fit + PDPA |
| [incident-postmortem-judgment](./skills/incident-postmortem-judgment.md) | ถอดบทเรียนหลังเหตุ + CAPA — blameless RCA + ป้องกันซ้ำที่ระบบ |

### 🗂️ จัดการ
| skill | ช่วยอะไร |
|---|---|
| [never-lose-a-file](./skills/never-lose-a-file.md) | จัดไฟล์ให้เป็นระเบียบ แล้วไม่หายอีก |
| [phi-data-handling](./skills/phi-data-handling.md) | จัดการข้อมูลคนไข้/PHI — de-identify ให้จริง + PDPA/IRB + แชร์ปลอดภัย |

### 🩸 งานแล็บ (Lab bench)
| skill | ช่วยอะไร |
|---|---|
| [bloodbank-judgment](./skills/bloodbank-judgment.md) | ตัดสินใจหน้างานธนาคารเลือด (ฝั่งผู้รับ) — ABO discrepancy / antibody ID / transfusion reaction |
| [blood-donor-component-judgment](./skills/blood-donor-component-judgment.md) | ฝั่งผู้บริจาค/ผลิตเลือด — eligibility · apheresis · component QC · TTI/recall (≠ ฝั่งผู้รับ) |
| [hematology-judgment](./skills/hematology-judgment.md) | อ่าน CBC/smear/coag — review smear เมื่อไหร่ + thal vs IDA + PT/aPTT |
| [clinchem-judgment](./skills/clinchem-judgment.md) | QC accept/reject (Westgard) + interference HIL + critical value |
| [chemistry-interpretation-judgment](./skills/chemistry-interpretation-judgment.md) | แปลผล organ-system — tumor/renal(eGFR)/LFT/cardiac + ABG/anion gap |
| [clinmicro-judgment](./skills/clinmicro-judgment.md) | เชื้อจริง vs contaminate + อ่าน AST/MDR + culture vs molecular |
| [applied-microbiology-judgment](./skills/applied-microbiology-judgment.md) | จุลชีววิทยาประยุกต์ (อาหาร/อุตสาหกรรม) — screen≠confirm + metagenomics |
| [immunoassay-judgment](./skills/immunoassay-judgment.md) | เลือก format + อ่าน HBV/HIV/syphilis/ANA panel + prozone/hook/window |
| [molecular-judgment](./skills/molecular-judgment.md) | เลือก method (Sanger/NGS/qPCR) + แปล Ct + กัน false +/− |
| [pathology-judgment](./skills/pathology-judgment.md) | อ่าน pattern — benign/malignant + grading/staging + dysplasia |
| [histotech-cytology-judgment](./skills/histotech-cytology-judgment.md) | งาน histo/cyto (process) — adequacy/fixation/stain QC/artifact (≠ อ่านผล) |
| [parasitology-judgment](./skills/parasitology-judgment.md) | เลือก concentration/stain + malaria thick/thin + กัน single-stool false-neg |
| [toxicology-judgment](./skills/toxicology-judgment.md) | screen vs confirm + antidote (OP/paraquat) + TDM timing |
| [pharmacology-judgment](./skills/pharmacology-judgment.md) | ยาเบื้องต้น — ADME + แพ้ยา vs ผลข้างเคียง (SJS/TEN) + ยาตีกัน |
| [clinical-correlation-judgment](./skills/clinical-correlation-judgment.md) | อ่านผลแล็บข้ามแขนง → ตั้ง DDx/ชี้ทางให้แพทย์ (pivotal → rule-out) |
| [infection-control-judgment](./skills/infection-control-judgment.md) | IPC/biosafety — hand hygiene + N95 vs surgical + precaution/เข็มตำ |
| [urinalysis-judgment](./skills/urinalysis-judgment.md) | ยูริน + body-fluid micro — strip↔micro↔clinical ให้ตรง + กับดัก strip |
| [preanalytical-judgment](./skills/preanalytical-judgment.md) | pre-analytical/phlebotomy — ลำดับเจาะ/หลอด/ระบุตัว ให้ตัวอย่างเชื่อได้ |
| [result-release-judgment](./skills/result-release-judgment.md) | post-analytical/ปล่อยผล — delta-check · autoverify · critical · corrected |
| [poct-judgment](./skills/poct-judgment.md) | Point-of-care testing — ให้แล็บนอกแล็บเชื่อได้เท่าแล็บกลาง + QC/connectivity |
| [flow-cytometry-judgment](./skills/flow-cytometry-judgment.md) | flow cytometry — gate ถูก/อ่าน pattern + กับดัก compensation/artifact |

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
- **ทุก skill ทีเดียว (AI เลือกใช้เอง)** → [`dist/all-skills.md`](./dist/all-skills.md) — รวมทุกตัวในไฟล์เดียว · ก๊อป/โหลดสดก็ได้ · AI self-route ตามคำถาม · **เฉพาะ AI context ใหญ่** (Claude/Gemini/Project, ไม่เหมาะ GPT chat เปล่า)
- ⚠️ live link ใช้ได้เฉพาะ AI ที่ดึง URL ได้ (Claude web · ChatGPT browse · Gemini) — แชตเปล่า offline ใช้ก๊อป

## โครงสร้าง

```
mt-score-up-skill/
├── skills/        # ★ 93 สกิล — copy (แช่แข็ง) หรือโหลดสดผ่าน INDEX.md (auto-sync)
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
└── CHANGELOG.md   # Version history (v0.9.0)
```

## ความปลอดภัย & Privacy

- ✅ ทำงานบนเครื่อง/บราวเซอร์คุณเท่านั้น — ไม่มี server กลาง ไม่เก็บข้อมูล · open-source (MIT) ตรวจได้ทุกบรรทัด
- ⚠️ **ห้ามใส่ข้อมูลระบุตัวคนไข้** (ชื่อ/HN/MRN) — ใช้ placeholder
- ⚠️ **สกิลงานแล็บ (🩸) = ตัวช่วย "คิด" ไม่ใช่คำตอบสุดท้าย** — วิจารณญาณ MT/แพทย์นำเสมอ + verify ก่อนใช้จริง; โหลดคู่สกิลคลินิก ให้ "ความรอบคอบ" ชนะ "ความสั้น" และวางคู่ [`anti-hallucination`](./skills/anti-hallucination.md)
- ความเข้มของ disclaimer แบ่งตามความเสี่ยง (กระทบคนไข้ = หนัก + มี guard ในตัว · จัดไฟล์/สื่อสาร = เบา) — by design

## วัดผลสกิล (eval)

ทดสอบจริง: ให้ **model อ่อน (Haiku)** ตอบโจทย์กับดัก *มี* vs *ไม่มี* สกิล → กรรมการตาบอดให้คะแนน. อ่านเป็น **grade-book ไม่ใช่ leaderboard** (ไม่ตีเกรด A-F):
- ตัวเลขมี noise (~1.4 จุด) → เชื่อเฉพาะ delta ที่เกินจริง; **8 ตัว "bulletproof"** ยกคะแนนนิ่งหลายรอบ
- **0 dangerous regression** — ไม่มีสกิลไหนทำให้ AI ตอบแย่ลง
- รายละเอียด/ข้อจำกัด → [`eval/ab-scorecard.md`](./eval/ab-scorecard.md) · [`eval/METHOD.md`](./eval/METHOD.md)

## ที่มา & การอ้างอิง (Sources)

- **ที่มา:** ผมสกัดจากที่เรียน ฝึกงาน และประสบการณ์หน้างาน — เก็บ "วิจารณญาณ" (เลือกอะไรเมื่อไหร่ + กับดัก) เรียบเรียงใหม่ ไม่ใช่ลอกสไลด์/ตำรามาตรง
- ตัวเลข/ค่าอ้างอิง = **illustrative** ยึดของแล็บ/ตำราจริงเสมอ · มาตรฐาน (ISO 15189:2022 · ISO 15190:2020 · AABB Tech Manual 21st / Standards 35th) อ้าง **หัวข้อ/edition** ไม่ได้คัดเนื้อความมา (ดู [`STANDARDS.md`](./STANDARDS.md))
- **เจอจุดไหนคล้ายแหล่งมีลิขสิทธิ์เกินไป หรือผิด — เปิด issue บอกได้ จะแก้/ถอดให้**

## License

MIT ([LICENSE](./LICENSE)) — ใช้ฟรี / แก้ได้ / share ได้ · เงื่อนไขการใช้เชิงคลินิก/healthcare → [NOTICE](./NOTICE)

## Contributing

อยากเพิ่ม skill ของตัวเอง / ปรับปรุงของเดิม? ดู [CONTRIBUTING.md](./CONTRIBUTING.md) — เล่าปัญหาหรือวิจารณญาณในสายงานคุณมาได้เลย

> **ไม่มี GitHub ก็ส่งได้** และ **ไม่ต้องเขียนให้สวย** — ส่งทาง **[Google Form](https://forms.gle/cWivk9zh6hJ5vdiy5)** (หรือทักเพจ Score UP) → maintainer + AI เรียบเรียงเป็น skill ให้ (มี [prompt ตัวช่วยร่างด้วย AI](./CONTRIBUTING.md#-ตัวช่วยร่างด้วย-ai) แปะใช้ได้เลย)

> 🎙️ **เป็นผู้เชี่ยวชาญ/ใกล้เกษียณ ไม่ถนัดเขียน?** วาง [`prompts/skill-interview.md`](./prompts/skill-interview.md) (Skill Maker) ในแชต AI → มันสัมภาษณ์ถอดวิจารณญาณของคุณเป็นร่าง skill ให้เอง · ผู้ลงขันได้ credit ใน [`CONTRIBUTORS.md`](./CONTRIBUTORS.md)
>
> 💬 เจอจุดผิด หรืออยากบอกว่า skill ช่วย/ไม่ช่วยของจริง → [`docs/FEEDBACK.md`](./docs/FEEDBACK.md)

## Credits

โดย **Phanuphong Tameesak — MT Score UP!** เพื่อชุมชน MT ไทย
ส่วนหนึ่งของ **Score UP** ecosystem

**ขอบคุณ** ครูบาอาจารย์เทคนิคการแพทย์และพี่ๆ MT หน้างานที่ปูพื้นฐานวิชาชีพให้ผม 🙏 ส่วนสกิลด้านอื่น (วิจัย/การเงิน/ขาย/AI ฯลฯ) มาจากการเรียนรู้และประสบการณ์ข้ามสายงานของผมเอง — *เป็นโปรเจกต์ส่วนตัว ไม่ได้เป็นตัวแทนหรือรับรองโดยสถาบันใด*
