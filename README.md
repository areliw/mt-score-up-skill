# MT Score UP — Skills Hub สำหรับ MT ไทย

แหล่งรวม **"สกิล" + เครื่องมือฟรี** สำหรับ Medical Technologist (MT) ไทย — เอาไปวางในแชต AI ที่คุณมีอยู่แล้ว (Claude / ChatGPT / Gemini) ใช้ได้เลย **ไม่ต้องติดตั้ง ไม่ต้องจ่ายค่า token เพิ่ม**

> แนวคิด: แพ็ก **"วิจารณญาณ" ของ MT ที่เก่งแล้ว** ให้กลายเป็นไฟล์ที่ใครก็หยิบไปใช้ได้ — ไม่ใช่แค่ "ความรู้" (ตำรา/AI มีอยู่แล้ว) แต่คือ **"เลือกอะไรเมื่อไหร่ + กับดักที่มือใหม่ไม่รู้"**

---

> ⚠️ **เพื่อการศึกษา / ช่วยคิดเท่านั้น — NOT FOR CLINICAL USE.** กลุ่มสกิลงานแล็บ (🩸) เป็นกรอบช่วย *ตัดสินใจ/ทบทวน* ไม่ใช่คำสั่งวินิจฉัย/รักษา และไม่รับประกันความถูกต้อง — การใช้กับผู้ป่วยจริงต้องอิง SOP + วิจารณญาณของ MT/แพทย์ผู้มีใบประกอบวิชาชีพเสมอ · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้

## 📚 ส่วนที่ 1 — Skills (82 สกิล)

**🧭 ไม่รู้จะใช้ตัวไหน? เริ่มที่นี่:** วาง [`prompts/triage.md`](./prompts/triage.md) ในแชต AI แล้วเล่าปัญหา/เคส/งานวิจัยของคุณ → AI จะบอกว่าใช้ skill ไหน (หรือถ้าคลังยังไม่มี จะช่วยร่างให้ส่งเข้า GitHub)

**วิธีใช้ (รู้แล้วว่าจะใช้ตัวไหน):** เปิดไฟล์ในโฟลเดอร์ [`skills/`](./skills) → copy ทั้งไฟล์ → วางในแชต AI → พิมพ์ปัญหาของคุณ

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
| [urinalysis-judgment](./skills/urinalysis-judgment.md) | UA + body fluid (CSF/serous/synovial) — strip↔micro↔clinical · nitrite-neg ≠ no UTI · cast/crystal · gout vs pseudogout |
| [preanalytical-judgment](./skills/preanalytical-judgment.md) | เจาะ/หลอด/ระบุตัว/ขนส่ง = error #1 ของแล็บ · order of draw · HIL · รีรัน≠เจาะใหม่ · wrong-blood-in-tube |
| [poct-judgment](./skills/poct-judgment.md) | POCT = แล็บนอกแล็บ ต้องมี QC+competency+connectivity · interference (Hct) · confirm ค่าวิกฤต |
| [flow-cytometry-judgment](./skills/flow-cytometry-judgment.md) | gate ถูก (singlet/viable/CD45-SSC) · อ่าน pattern ไม่ใช่ marker เดี่ยว · PNH/CD4/leukemia · correlate |

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
| [method-validation-stats](./skills/method-validation-stats.md) | สถิติเฉพาะ MT: method comparison (Bland-Altman/PB ไม่ใช่ r) · reference interval (EP28) · diagnostic accuracy · CV/sigma |
| [pubmed-search](./skills/pubmed-search.md) | ค้น PubMed: PICO→MeSH+synonym · ขยาย/แคบ · "ไม่เจอ"≠"ไม่มี" · verify PMID |
| [source-credibility](./skills/source-credibility.md) | ประเมินแหล่งเชื่อได้แค่ไหน: คัด predatory · ลำดับชั้นหลักฐาน · COI/retract · IF สูง≠ถูก |
| [deep-research](./skills/deep-research.md) | research หลายแหล่ง + cross-check + สังเคราะห์ + อ้างอิง · ไม่เชื่อ AI รอบเดียว |
| [gget-genomics](./skills/gget-genomics.md) | ดึง gene/variant/structure ด้วย gget · ระวัง genome build (hg19/hg38) · classify ตาม ACMG |

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
| [prompt-craft](./skills/prompt-craft.md) | เขียน prompt ให้ได้ผล: role+context+task+format · กัน AI เดา/มั่ว · ไม่ใส่ข้อมูลคนไข้ |
| [plan-with-ai](./skills/plan-with-ai.md) | ใช้ AI วางแผนงานใหญ่: แตกงาน+หา risk+ให้ AI ถามกลับ · ไม่เชื่อแผนดิ่ง · ตรวจ assumption |

### 💬 สื่อสาร
| skill | ช่วยอะไร |
|---|---|
| [polite-but-clear](./skills/polite-but-clear.md) | ปรับถ้อยคำให้สุภาพแต่ยังได้ใจความ |
| [explain-simply](./skills/explain-simply.md) | อธิบายเรื่องยากแบบเด็ก ป.3 (ไม่ผิด) |
| [content-creator-judgment](./skills/content-creator-judgment.md) | เลือกหัวข้อคอนเทนต์ให้ความรู้ + ไม่ทำให้เพจตาย |
| [photography-judgment](./skills/photography-judgment.md) | ถ่ายภาพ/วิดีโอ + photomicrography (สไลด์/colony/gel): exposure/DOF/composition/WB |
| [design-a-clear-figure](./skills/design-a-clear-figure.md) | กราฟ/โปสเตอร์/รูปวิจัยให้อ่านรู้เรื่อง: เลือก chart · colorblind-safe · แกนไม่หลอกตา |

### 🎬 สอน / สื่อ / เรียนรู้
| skill | ช่วยอะไร |
|---|---|
| [learn-anything-fast](./skills/learn-anything-fast.md) | ใช้ AI เป็นติวเตอร์เรียนของใหม่ให้ "ทำได้จริง": active recall · Feynman · verify เนื้อหา med |
| [make-a-teaching-video](./skills/make-a-teaching-video.md) | ทำคลิปสอน/explainer: objective+script · de-identify เคสคนไข้ · เนื้อหาถูก+disclaimer |

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
| [personal-brand](./skills/personal-brand.md) | สร้างตัวตนวิชาชีพออนไลน์ (LinkedIn/เพจ): จุดยืนจากตัวจริง · pillar · อยู่ในขอบเขตจรรยาบรรณ |
| [focus-and-time](./skills/focus-and-time.md) | บริหารเวลา/โฟกัส สำหรับ MT เวรหมุน: สำคัญ>เร่ง · time-block รอบเวร · กัน burnout |
| [manage-up](./skills/manage-up.md) | คุยกับหัวหน้าให้ได้ผล: ปัญหา+ทางออก+impact · พูดภาษาหัวหน้า (เงิน/เสี่ยง) · timing |

### 💼 บริหารแล็บ / ขาย IVD
| skill | ช่วยอะไร |
|---|---|
| [lab-management-judgment](./skills/lab-management-judgment.md) | QMS/ISO 15189 · QC strategy (sigma/IQCP) · งบ · verification · inventory |
| [ivd-sales-judgment](./skills/ivd-sales-judgment.md) | ขาย IVD/diagnostics — ขายผลลัพธ์บริหาร · budget-pocket · ROI · spec-in |
| [crm-judgment](./skills/crm-judgment.md) | คิดแบบลูกค้า สำหรับ MT สาย sales/คลินิก/แอป |
| [marketing-judgment](./skills/marketing-judgment.md) | กลยุทธ์การตลาด B2B: STP · buying center · pricing · positioning · push/pull |
| [sales-psychology-judgment](./skills/sales-psychology-judgment.md) | จิตวิทยาขาย/อ่านคน: แรงจูงใจ · active listening · trust · โน้มน้าว(+จริยธรรม) · เจรจา |
| [lab-clinic-business-judgment](./skills/lab-clinic-business-judgment.md) | เปิด/บริหารคลินิกแล็บ MT เอง: เลือกโมเดล · moat (วิชาชีพ+จดทะเบียน+LIS-HIS) · รายได้รัฐ · อ่านใจ buyer · unit economics |
| [market-opportunity](./skills/market-opportunity.md) | ประเมินช่องว่างตลาดก่อนลงเงิน (ธุรกิจ/แอป/แล็บ): ปัญหาที่คนจ่าย · validate ก่อน build · unit economics |
| [content-distribution](./skills/content-distribution.md) | กระจายคอนเทนต์ข้ามแพลตฟอร์ม + ให้คนเจอ: 1 ชิ้น→native หลายที่ · discoverability · วัดผลถูก |

### 💻 โค้ด / data / สร้างของเอง (MT++ : T-shaped MT)
> ยุค AI — MT ไม่ต้องเป็นโปรแกรมเมอร์ก็ทำ dashboard / automate / data เองได้. สกิลกลุ่มนี้ reframe ให้ "MT ที่ไม่ใช่ dev" — กับดัก #1 ผูกกับ **ความปลอดภัยข้อมูลคนไข้ (PDPA)** เสมอ (ดูแผนเต็ม [`docs/EXPANSION-PLAN.md`](./docs/EXPANSION-PLAN.md))

| skill | ช่วยอะไร |
|---|---|
| [build-a-dashboard](./skills/build-a-dashboard.md) | MT ทำ dashboard เอง (TAT/QC/workload) — เลือกเครื่องมือ + กราฟไม่หลอกตา + ไม่รั่วข้อมูลคนไข้ |
| [automate-lab-tasks](./skills/automate-lab-tasks.md) | งานซ้ำ (รายงาน/คำนวณ/จัดเวร) ควร automate ไหม + ไม่พังเงียบ (verify + alert) |
| [clean-messy-data](./skills/clean-messy-data.md) | ล้างข้อมูล lab/วิจัยรกๆ ก่อนวิเคราะห์ — date/หน่วย/missing/duplicate · เก็บ raw เสมอ |
| [vibe-coding-safely](./skills/vibe-coding-safely.md) | ให้ AI เขียนโค้ดให้แบบไม่พัง/ไม่รั่ว — "รันได้ ≠ ถูก" · ไม่ paste PHI/key |
| [ship-a-small-app](./skills/ship-a-small-app.md) | ทำเครื่องมือเล็กให้ทีมใช้ (calculator/ฟอร์ม) — no-code ก่อน + auth/PDPA |
| [spreadsheet-judgment](./skills/spreadsheet-judgment.md) | Excel/Sheets ให้ถูก — กัน autoconvert ทำลายข้อมูล · VLOOKUP/STDEV · median TAT |
| [mt-databases](./skills/mt-databases.md) | เก็บข้อมูล Sheets vs Access vs SQL vs REDCap เมื่อไหร่ + ออกแบบไม่ให้พัง/หาย |
| [deploy-ml-safely](./skills/deploy-ml-safely.md) | MT เอาโมเดลไปใช้จริง — "แม่นตอนเทรน≠ใช้ได้จริง" · drift/monitor · human-in-loop คลินิก |
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

## 🔄 ก๊อป (แช่แข็ง) vs โหลดสด (auto-sync)

skill เป็นไฟล์ — มี 2 วิธีโหลด เลือกตามงาน:
- **ก๊อปเนื้อไฟล์** → snapshot **แช่แข็ง**: เสถียร, cite เวอร์ชันใน audit trail ได้, ไม่เปลี่ยนกลางคัน (เหมาะงานคลินิก)
- **โหลดสด (live link)** → บอก AI ที่ต่อเน็ตได้ว่า *"ดึง skill จาก `<raw URL>` มาใช้"* → ได้ `main` ล่าสุด**ทุกครั้ง = auto-sync** ไม่ต้องก๊อปใหม่ · รายการ URL ทั้งหมด → [`skills/INDEX.md`](./skills/INDEX.md) (CI อัปเดตอัตโนมัติ)
- **ทุก skill ทีเดียว (AI เลือกใช้เอง)** → [`dist/all-skills.md`](./dist/all-skills.md) — รวมทุกตัวในไฟล์เดียว (~90K tokens) · ก๊อป/โหลดสดก็ได้ · AI self-route ตามคำถาม · **เฉพาะ AI context ใหญ่** (Claude/Gemini/Project, ไม่เหมาะ GPT chat เปล่า)
- ⚠️ live link ใช้ได้เฉพาะ AI ที่ดึง URL ได้ (Claude web · ChatGPT browse · Gemini) — แชตเปล่า offline ใช้ก๊อป

## โครงสร้าง

```
mt-score-up-skill/
├── skills/        # ★ 82 สกิล — copy (แช่แข็ง) หรือโหลดสดผ่าน INDEX.md (auto-sync)
├── examples/      # ★ เห็น skill ทำงานจริง (before/after) — เริ่มที่นี่
├── exercises/     # โจทย์ฝึก ลองเองแล้วเทียบเฉลย
├── dist/          # all-skills.md — รวมทุก skill ไฟล์เดียว (auto-generated)
├── prompts/       # วางในแชต AI
│   ├── triage.md  # 🧭 ไม่รู้ใช้ skill ไหน → เริ่มที่นี่ (catalog auto-updated)
│   └── system.md  # WI generator (ISO 15189)
├── scripts/       # md→docx + standards auto-recheck (ดู scripts/README.md)
├── templates/     # (optional) วาง .docx แม่แบบ WI ของแล็บคุณเอง — generator ทำงานได้โดยไม่ต้องมี
├── profiles/      # Layout profile ต่อโรงพยาบาล (generic)
├── inbox/         # Drop WI ตัวอย่าง — AI scan ใช้เป็น template
├── eval/          # วัดผลสกิลจริง: weak-model A/B 3 รอบ + literature + Titanic (ดู eval/ab-scorecard.md)
├── docs/          # Vision, setup guides
├── wiki/          # คู่มือเข้าใจโปรเจกต์ลึกขึ้น (รวมลิงก์)
├── contributions/ # พื้นที่ชุมชน — ส่ง skill/เคสจริงมาสมทบ
├── STANDARDS.md   # Source-of-truth edition + auto-recheck รายเดือน
└── CHANGELOG.md   # Version history (v0.3.0)
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
- **0 regression อันตราย** ใน 53 ตัว — ไม่มีสกิลไหนทำให้ตอบ "พังลง" <sub>(eval รันบน 53 สกิล ณ ตอนนั้น; 2 ตัวล่าสุด `lab-clinic-business` + `ab-test-judgment` ผ่าน critical review แล้วแต่ยังไม่ A/B)</sub>

## ที่มา & การอ้างอิง (Sources)

- **ที่มา:** ผมสกัดจากที่เรียน ฝึกงาน และประสบการณ์หน้างาน — เก็บ "วิจารณญาณ" (เลือกอะไรเมื่อไหร่ + กับดัก) เรียบเรียงใหม่ ไม่ใช่ลอกสไลด์/ตำรามาตรง
- ตัวเลข/ค่าอ้างอิง = **illustrative** ยึดของแล็บ/ตำราจริงเสมอ · มาตรฐาน (ISO 15189:2022 · ISO 15190:2020 · AABB Tech Manual 21st / Standards 35th) อ้าง **หัวข้อ/edition** ไม่ได้คัดเนื้อความมา (ดู [`STANDARDS.md`](./STANDARDS.md))
- **เจอจุดไหนคล้ายแหล่งมีลิขสิทธิ์เกินไป หรือผิด — เปิด issue บอกได้ จะแก้/ถอดให้**

## License

MIT — ใช้ฟรี / แก้ได้ / share ได้

## Contributing

อยากเพิ่ม skill ของตัวเอง / ปรับปรุงของเดิม? ดู [CONTRIBUTING.md](./CONTRIBUTING.md) — เล่าปัญหาหรือวิจารณญาณในสายงานคุณมาได้เลย

## Credits

โดย **Phanuphong Tameesak — MT Score UP!** เพื่อชุมชน MT ไทย
ส่วนหนึ่งของ **Score UP** ecosystem

**ขอบคุณ** ครูบาอาจารย์เทคนิคการแพทย์และพี่ๆ MT หน้างานที่ปูพื้นฐานวิชาชีพให้ผม 🙏 ส่วนสกิลด้านอื่น (วิจัย/การเงิน/ขาย/AI ฯลฯ) มาจากการเรียนรู้และประสบการณ์ข้ามสายงานของผมเอง — *เป็นโปรเจกต์ส่วนตัว ไม่ได้เป็นตัวแทนหรือรับรองโดยสถาบันใด*
