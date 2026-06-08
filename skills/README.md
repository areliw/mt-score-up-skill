# Skills — คลังวิจารณญาณ MT

**82 สกิล** ที่แพ็ก "วิจารณญาณ" (judgment) ของ MT ให้พกพาได้ — copy ทั้งไฟล์ไปวางในแชต AI ที่คุณใช้อยู่ (Claude / ChatGPT / Gemini) แล้วพิมพ์ปัญหาของคุณ

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
- **chemistry-interpretation-judgment** — แปลผล organ-system (ค่าออกมาแล้วแปลว่าอะไร): tumor marker ใช้/ไม่ใช้ · renal (eGFR/cystatin/Jaffe) · LFT pattern (AST:ALT, DB/TB) · cardiac timing (troponin/CK-MB) · acid-base + anion gap · interference (HIL/paraprotein/drug) — *MT ไม่วินิจฉัย*
- **clinmicro-judgment** — เชื้อจริง vs contaminate · ID workflow + เมื่อไหร่พอ · อ่าน AST (ESBL/MRSA/inducible-clinda/CRE) · เลือก media/atmosphere · culture vs molecular
- **applied-microbiology-judgment** — จุลชีววิทยาประยุกต์ (อาหาร/อุตสาหกรรม/สิ่งแวดล้อม คนละเลน clinical): ถนอมอาหาร · food pathogen screen≠confirm · culture-dependent vs metagenomics vs polyphasic · bioremediation · probiotic/prebiotic/FMT
- **immunoassay-judgment** — เลือก format (sandwich/competitive/CLIA/lateral flow) · อ่าน HBV/HIV/syphilis/ANA panel · prozone/hook/window/confirm
- **molecular-judgment** — เลือก method detect variant (RFLP/ASO/HRM/Sanger/NGS) · real-time chemistry · แปล Ct/melt valid-invalid · กัน contamination/false-neg · HLA typing · pharmacogenomics
- **pathology-judgment** — อ่าน pattern: benign/malignant (5 แกน) · cell injury reversible/irreversible · necrosis type · acute/chronic อักเสบ · grading/staging · dysplasia→cancer (basement membrane) · granuloma/hypersensitivity
- **parasitology-judgment** — เลือก concentration/stain ตามเป้า · malaria thick vs thin + ตรวจซ้ำ · single-stool false-neg · artifact vs parasite
- **toxicology-judgment** — screen vs confirm · antidote tree (OP/carbamate/paraquat/โลหะ) · chelator คู่โลหะ · RBC-AChE vs plasma ChE · TDM timing · chain of custody
- **clinical-correlation-judgment** — อ่านผลแล็บข้ามแขนง (hema+chem+micro+immuno+BB) → ร้อยเป็นภาพเดียว ตั้ง DDx/ชี้ทางให้แพทย์ (pivotal value → DDx → rule-out → cause-effect chain) · *MT ไม่วินิจฉัย*
- **pharmacology-judgment** — ยาเบื้องต้นมุม MT: ADME (ตับ/ไตเสื่อม→พิษ) · แพ้ยา vs ผลข้างเคียง (SJS/TEN) · ยาตีกัน (ยา-ยา/อาหาร/โรค) · ใช้ยาถูก (ห้ามบด EC/SR) · TDM (peak/trough) · anticoag↔coag · pharmacogenomics — *MT ไม่สั่งจ่ายยา*
- **infection-control-judgment** — ป้องกันการติดเชื้อ/biosafety: hand hygiene (alcohol vs สบู่ C.diff spore) · N95 vs surgical · transmission precaution (contact/droplet/airborne) · ห้องความดันลบ/บวก · post-exposure · BSL
- **urinalysis-judgment** — ตรวจปัสสาวะ + body fluid microscopy: strip↔micro↔clinical ต้องตรง · nitrite-neg ไม่ตัด UTI · RBC/WBC/cast/crystal significant vs artifact · CSF/serous/synovial (gout vs pseudogout)
- **preanalytical-judgment** — คุณภาพตัวอย่างก่อนวิเคราะห์ (error #1 ของแล็บ ~60–70%): order of draw · หลอด/ratio · HIL กระทบ analyte ไหน · timing/tourniquet/IV-line · รีรัน≠เจาะใหม่ · wrong-blood-in-tube
- **poct-judgment** — POCT = แล็บนอกแล็บ (ISO 15189:2022): เมื่อไหร่ใช้ vs ส่งแล็บกลาง · QC+operator competency+connectivity · interference (Hct/oxygen) · linear range · confirm/แจ้งค่าวิกฤต
- **flow-cytometry-judgment** — gating ถูก (scatter→singlet→viable→CD45/SSC) · compensation+FMO control · อ่าน pattern/intensity ไม่ใช่ marker เดี่ยว · leukemia/lymphoma/PNH/CD4/MRD · correlate morphology

### 🔬 งานวิจัย / สถิติ (R2R)
- **r2r-research-proposal** — ปั้นโจทย์วิจัยจากปัญหา → คำถาม → objective + เช็คคู่ objective↔method
- **research-design-judgment** — เลือก study design (descriptive/analytic · cross-sectional/case-control/cohort/RCT) + ชนิดตัวแปร + bias/confounder + gate IRB/ethics
- **manuscript-judgment** — เขียน proposal/manuscript (IMRaD) ให้ผ่าน reviewer + เกณฑ์ accept/reject + objective=results=conclusion
- **critical-appraisal-judgment** — อ่าน/ประเมินเปเปอร์คนอื่น + lit review: สกัด method/finding · diagnostic-accuracy (sens/spec/PPV vs gold standard) · หา research gap=contribution · เลือก method spine · จับ limitation-to-beat
- **choose-stat-test** — decision tree เลือก statistical test จาก 3 คำถาม (เป้าหมาย × ชนิด outcome × กี่กลุ่ม)
- **sample-size-power** — หาขนาดตัวอย่าง N ด้วย power analysis + สูตร + ตัวอย่างมีเลข
- **r2r-stats** — ผู้ช่วยรัน/แปลผลสถิติ R2R + กับดัก lab (method comparison ≠ validation ฯลฯ) `needs: code-interpreter`
- **method-validation-stats** — สถิติเฉพาะ MT: method comparison (Bland-Altman + Passing-Bablok/Deming ไม่ใช่ r/paired-t) · reference interval (CLSI EP28, n≥120) · diagnostic accuracy (sens/spec/PPV-ตาม prevalence/ROC) · precision/CV/sigma · kappa
- **pubmed-search** — ค้น PubMed: PICO→MeSH+synonym+Boolean · filter ฉลาด · ขยาย/แคบ · "ค้นไม่เจอ"≠"ไม่มีงาน" · verify PMID (AI แต่ง citation ได้)
- **source-credibility** — ประเมินแหล่งเชื่อได้แค่ไหน: คัด predatory (indexing/publisher) · ลำดับชั้นหลักฐาน · COI/funding/retract · IF สูง/"peer-reviewed"≠ถูก · ตามไป primary
- **deep-research** — research หลายแหล่งอิสระ + cross-check + สังเคราะห์ (ระบุระดับความมั่นใจ) + อ้างอิง · ไม่เชื่อ AI รอบเดียว · กัน confirmation bias
- **gget-genomics** — ดึง gene/variant/seq/structure ด้วย gget (Ensembl/NCBI/UniProt/AlphaFold) · ระวัง genome build (hg19↔hg38) · presence≠pathogenic (classify ACMG) · PHI

### 🤖 ใช้ AI อย่างคม / ปลอดภัย
- **ai-assistant-calibration** — ปรับ "นิสัยการตอบ" ของ AI ให้คม ตรงสไตล์คุณ `CALIBRATION`
- **ai-agent-team** — ตั้ง AI เป็นทีมผู้เชี่ยวชาญหลายตำแหน่ง + หัวหน้าคอย route/รวบ `CALIBRATION`
- **self-improving-agent** — ให้ agent จดบทเรียนจากความผิดพลาด เก่งขึ้นข้ามวัน `needs: persistent-memory`
- **ab-test-judgment** — วัด prompt/skill ดีขึ้นจริงไหม ไม่ไล่จับ noise: control + delta-of-deltas · noise floor · weak vs frontier answerer · เมื่อไหร่ตัดสินด้วย review แทนเลข
- **what-skill-do-i-need** — วินิจฉัยว่าคุณต้องการอะไรจริงๆ (skill? tool? ลงมือ? คนจริง?)
- **offload-to-automation** — งานที่ต้องเป๊ะ (เลข/จัดเวร) โยนให้ code AI เป็นคนคุม+ตรวจ `CALIBRATION`
- **anti-hallucination** — กัน + จับ AI มั่วข้อเท็จจริง/ตัวเลข/citation (สำคัญสายแพทย์) `CALIBRATION`
- **progress-tracker** — วางคู่สกิลไหนก็ได้ → AI โชว์ความคืบหน้าเป็น checklist/flowchart (ทำถึงไหน·เลือกกิ่งไหน) `CALIBRATION`
- **prompt-craft** — เขียน prompt ให้ได้ผล: role+context+task+format+example · ให้บริบทพอ · iterate ทีละจุด · กัน hallucination (ขอแหล่ง/บอกเมื่อไม่รู้) · ไม่ใส่ PHI/secret
- **plan-with-ai** — ใช้ AI วางแผนงานใหญ่: แตก milestone/task+dependency · หา risk/unknown · ให้ AI grill เรา · ตรวจ assumption · แผน=hypothesis ปรับได้ · ไม่เชื่อแผนดิ่ง

### 💬 สื่อสาร
- **polite-but-clear** — ปรับข้อความห้วน/แรง → สุภาพ แต่ยังได้ใจความ (ปฏิเสธ/ตักเตือน/แย้งหัวหน้า)
- **explain-simply** — อธิบายเรื่องยากแบบเด็ก ป.3 — ง่ายแต่ห้ามผิด (โดยเฉพาะเรื่องแพทย์)
- **content-creator-judgment** — เลือกหัวข้อคอนเทนต์ให้ความรู้ (มี hook ไหม/จับเทรนด์ตอนไหน) + ไม่ทำให้เพจตาย
- **photography-judgment** — ถ่ายภาพ/วิดีโอ + photomicrography: exposure triangle · DOF เพื่อสื่อความหมาย · composition · WB/metering · ถ่ายสไลด์/colony/gel ให้คม-สีตรง · video grammar
- **design-a-clear-figure** — กราฟ/โปสเตอร์/รูปวิจัย/สไลด์ให้อ่านรู้เรื่อง: 1 message · เลือก chart ตาม message · visual hierarchy · colorblind-safe (เลี่ยงแดง-เขียว) · แกนซื่อสัตย์ (เริ่มศูนย์) · label+หน่วย

### 🎬 สอน / สื่อ / เรียนรู้
- **learn-anything-fast** — ใช้ AI เป็นติวเตอร์เรียนของใหม่ให้ "ทำได้จริง": ตั้งเป้า · active recall+spaced repetition · Feynman (อธิบายกลับ) · ตรวจความเข้าใจจริง · verify เนื้อหา med (illusion of competence)
- **make-a-teaching-video** — คลิปสอน/explainer: learning objective+script · เลือกรูปแบบ (screen/animation/talking head) · de-identify เคสคนไข้ (PDPA) · เนื้อหาถูก+disclaimer+ในขอบเขต · ลิขสิทธิ์

### 🧭 ชีวิต / อาชีพ
- **ikigai-finder** — หา ikigai แบบไม่หลอกตัวเอง → จบที่ "1 การทดลอง" ไม่ใช่ลาออกตามฝัน
- **self-development-coach** — โค้ชพัฒนาตัวเองแบบตรงไปตรงมา ไม่ปลอบใจลอยๆ
- **know-yourself** — สัมภาษณ์ตัวเองให้ลึก → master profile ก้อนเดียวที่ slice ไปใช้ได้ (resume/LinkedIn/เตรียมสัมภาษณ์/เปลี่ยนสาย/ป้อน AI ให้รู้จักเรา)
- **mt-career-judgment** — เส้นทางอาชีพ MT (bench→industry/commercial/AI): แผนที่สาย · ladder ฝั่งขาย+โครงรายได้ · skill gap (KOL/English/commercial-craft) · T-shaped Data&AI 3 ระดับ · เป็นเจ้าของแล็บ
- **lab-clinic-business-judgment** — เปิด/บริหารคลินิกแล็บ MT เอง: เลือกโมเดล (premium-longevity vs volume-รัฐ vs hybrid) · moat จริง (วิชาชีพ+จดทะเบียน+LIS-HIS ไม่ใช่เครื่อง) · ปิด business-gap ที่ MT ขาด · เข้าระบบรายได้รัฐเมื่อไหร่ · อ่านใจ buyer (สาย sales) · หา unit economics ก่อนลงเงิน
- **digital-judgment** — privacy/PDPA/de-identify/security/ลิขสิทธิ์/ลงทุนออนไลน์ — ตัดสินใจปลอดภัย ไม่โดนหลอก
- **finance-judgment** — การเงิน/ลงทุน/ธุรกิจ (บันไดเงิน · asset ตาม horizon · อ่านงบ/CFO · valuation · หนี้ดี-เลว · go/pivot · จับ scam · เลนส์ econ: opportunity cost/elasticity/real-vs-nominal)
- **financial-statement-judgment** — อ่านงบ 5 ฉบับ + ลำดับอ่าน (audit→CFO→ฐานันดรกำไร→งบดุล→หมายเหตุ) + คุณภาพกำไร + จับ window-dressing (OCI recycling/ตีราคา/FIFO/cookie-jar/งบรวม)
- **mt-law-ethics-judgment** — กฎหมาย/จรรยาบรรณวิชาชีพ MT: ใบอนุญาต+CMTE · ขอบเขตวิชาชีพ (ทำได้/ต้องมีแพทย์/ทำไม่ได้) · ความลับ+PDPA · กฎหมายเครื่องมือแพทย์ (ขาย IVD) · คิดก่อนโพสต์
- **mt-exam-strategy-judgment** — กลยุทธ์ทำข้อสอบใบประกอบฯ MT: blueprint+บริหารเวลา (ทุ่ม 3 สาขาใหญ่ + เก็บ recall/QC ก่อน) · จับ distractor (สลับคู่/ครบ-keyword/ยกเว้น) · study ROI · ชี้สกิลรายสาขา
- **personal-brand** — สร้างตัวตนวิชาชีพออนไลน์ (LinkedIn/เพจ/พอร์ต): จุดยืนจากตัวจริง (know-yourself) · เลือกแพลตฟอร์ม · pillar topics · authentic · สม่ำเสมอ>viral · อยู่ในขอบเขตจรรยาบรรณ+PDPA
- **focus-and-time** — บริหารเวลา/โฟกัส สำหรับ MT เวรหมุน: สำคัญ>เร่ง (busy≠productive) · time-block รอบเวร (ไม่ใช่ 9-5) · deep work/pomodoro · จัดงานยากตอนพลังงาน peak · กัน burnout
- **manage-up** — คุยกับหัวหน้าให้ได้ผล: ปัญหา+ทางออก+impact+data · พูดภาษาหัวหน้า (เงิน/เสี่ยง/คุณภาพ/เวลา) · timing/ช่องทาง · แย้ง/บอกข่าวร้ายปลอดภัย · follow-up

### 💼 บริหารแล็บ / ขาย IVD
- **lab-management-judgment** — บริหารแล็บ: accreditation (ISO 15189/LA/HA) · QC strategy (sigma metric/IQCP) · งบ (เครื่อง=ลงทุน vs น้ำยา=ดำเนินงาน) · verification vs validation · inventory/FEFO
- **ivd-sales-judgment** — ขาย IVD/diagnostics: ขายผลลัพธ์บริหารไม่ใช่สเปก · budget-pocket (rental→opex) · sigma-ROI · cost-per-reportable-result · spec-in · after-sales
- **crm-judgment** — คิดแบบลูกค้า (segment/CLV 2×2/CF-CBF/วิกฤต PR) สำหรับ MT สาย sales/คลินิก/แอป
- **marketing-judgment** — กลยุทธ์การตลาด B2B: STP ก่อน 4P · buying center 5 บทบาท · pricing (อย่าตัดราคา/elasticity) · positioning · push vs pull · razor-blade install base
- **sales-psychology-judgment** — จิตวิทยาการขาย/อ่านคน: อ่านแรงจูงใจ (Maslow/McClelland) · คนซื้อด้วย Ideal/Public self · active listening · trust/social proof · เทคนิคโน้มน้าว + เส้นจริยธรรม · เจรจา win-win
- **market-opportunity** — ประเมินช่องว่างตลาดก่อนลงเงิน (ธุรกิจ/แอป/แล็บ): ปัญหาจริงที่คนจ่าย · TAM/SAM/SOM bottom-up · คู่แข่งรวม "ไม่ทำอะไรเลย" · validate ด้วย pre-sell ไม่ใช่ survey · unit economics · กัน solution-looking-for-problem
- **content-distribution** — กระจายคอนเทนต์ข้ามแพลตฟอร์ม: 1 pillar→repurpose native (Reels/LinkedIn/X/YT ต่างกัน) · discoverability (keyword/hashtag) · timing/ความถี่ · วัด save/share ไม่ใช่ like · เนื้อหา med ถูกทุกที่

### 💻 โค้ด / data / สร้างของเอง (MT++ : T-shaped MT)
> ยุค AI — MT ไม่ต้องเป็นโปรแกรมเมอร์ก็ทำ dashboard/automate/data เองได้. กลุ่มนี้ reframe ให้ "MT ที่ไม่ใช่ dev" — กับดัก #1 ผูกกับ PDPA/ข้อมูลคนไข้เสมอ (แผนเต็ม: [`../docs/EXPANSION-PLAN.md`](../docs/EXPANSION-PLAN.md))
- **build-a-dashboard** — MT ทำ dashboard เอง (TAT/QC/workload/stock): เริ่มที่คำถามไม่ใช่กราฟ · เลือกเครื่องมือ (Sheets/Looker/Power BI/Streamlit) · กราฟไม่หลอกตา (median TAT, ไม่ pie เยอะ) · ไม่เอา HN/ผลรายคนขึ้น cloud
- **automate-lab-tasks** — งานซ้ำควร automate ไหม (ROI: บ่อย×กฎนิ่ง) · code-vs-AI-vs-มือ · กัน "ผิดเงียบ" (validate/alert/idempotent) · ไม่ส่ง PHI ออก
- **clean-messy-data** — ล้างข้อมูล lab/วิจัย: ดูดิบก่อน+เก็บ raw · ลำดับ structural→ค่า→missing→dup · date นรก · regex-vs-AI · blank≠0
- **vibe-coding-safely** — ให้ AI เขียนโค้ดให้แบบ non-coder: "รันได้≠ถูก" verify known-answer · ไม่ paste PHI/key · ไม่รันคำสั่งที่ไม่เข้าใจ · กันพังเงียบ
- **ship-a-small-app** — เครื่องมือเล็กให้ทีมใช้: เล็กสุดที่ใช้ได้ก่อน · no-code/low-code (Forms/AppSheet/Streamlit) · auth+PDPA ตั้งแต่แรก · verify สูตรคลินิก
- **spreadsheet-judgment** — Excel/Sheets: กัน autoconvert (รหัส/วันที่/ยีน) · tidy data · VLOOKUP exact/STDEV.S-vs-P · data validation · median TAT · เมื่อไหร่ย้าย DB
- **mt-databases** — เลือกที่เก็บ (Sheets/Access/SQL/REDCap) ตามขนาด×คน×relationship · ออกแบบ non-DBA (1 entity/ตาราง, unique id) · backup+ห้ามแก้ raw · DELETE มีเงื่อนไข
- **deploy-ml-safely** — MT เอาโมเดลไปใช้จริง: "แม่นตอนเทรน≠ใช้ได้จริง" · validate external (ไม่ใช่ test split) · data drift+monitor · fallback/reject option · human-in-loop คลินิก · version/IRB
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
`clinical-correlation-judgment` (ร้อยผลข้ามแขนง → ตั้ง DDx/flag) → สกิลแล็บเฉพาะทาง (`hematology`/`clinchem`/`chemistry-interpretation`/`clinmicro`/`immunoassay`/`bloodbank`/`molecular`/`pathology`...) → `anti-hallucination` (กันมั่วค่า/อ้างอิง) → `explain-simply` (สื่อสารผล/อธิบายในขอบเขต)
*confirm lane:* reactive screen → `immunoassay-judgment` + `molecular-judgment` (ยืนยัน) · ⚠️ **MT ตีความ/flag/ส่งต่อ — การวินิจฉัยเป็นหน้าที่แพทย์**

**🔬 ทำวิจัย R2R ครบวงจร**
`critical-appraisal-judgment` (อ่าน lit + หา gap) → `r2r-research-proposal` (โจทย์) → `research-design-judgment` (design+bias+IRB) → `sample-size-power` (N) → `choose-stat-test` (test) → `r2r-stats` (รัน) → `manuscript-judgment` (เขียน/ตีพิมพ์) + `polite-but-clear` (ตอบ reviewer)

**💻 โปรเจกต์ data/ML**
`data-project-survival` (วางโครง) → `ml-judgment` (เลือกโมเดล/metric) → `cv-judgment` (ถ้าเป็นภาพ) → `python-coach`/`db-judgment` (เขียนจริง) → `offload-to-automation` + `anti-hallucination` (กันพลาด + verify)

**🤖 ใช้ AI ให้คม + ปลอดภัย**
`what-skill-do-i-need` (ขาดอะไร) → `ai-assistant-calibration` (ตั้งนิสัย) → `ai-agent-team` (ตั้งทีม) → `offload-to-automation` + `anti-hallucination` (กันพลาด) → `self-improving-agent` (เก่งขึ้นข้ามวัน)

**💬 ทำคอนเทนต์ / สื่อสาร**
`content-creator-judgment` (เลือกหัวข้อ) → `photography-judgment` (ถ่าย/ตัดต่อให้คม) → `explain-simply` (ทำให้ง่าย) → `anti-hallucination` (อย่ามั่ว) → `polite-but-clear` (ปรับโทน)

**🧭 ตัดสินใจชีวิต / อาชีพ**
`what-skill-do-i-need` → `ikigai-finder` (ทิศทาง) → `self-development-coach` (ลงมือโต) → `finance-judgment` (เงิน/ธุรกิจ) + `financial-statement-judgment` (อ่านงบ) + `digital-judgment` (PDPA/กัน scam) · สาย sales/แล็บ ดูคอมโบ 💼

**💼 บริหารแล็บ / ขาย IVD**
`marketing-judgment` (กลยุทธ์/STP/buying center) → `sales-psychology-judgment` (อ่านคน/โน้มน้าว/เจรจา) → `lab-management-judgment` (เข้าใจ QMS/QC/งบ) → `ivd-sales-judgment` (ปิดดีล) → `crm-judgment` (คิดแบบลูกค้า) + `finance-judgment` (ROI/CPR) + `mt-law-ethics-judgment` (กฎหมายเครื่องมือแพทย์/เคลมไม่เกินจริง) · คู่กับ `clinchem-judgment` (QC bench ↔ strategy)

**🛠️ จัดการงาน / ทรัพยากร**
`never-lose-a-file` (จัดไฟล์) + `optimization-judgment` (จัดเวร/จัดสรร) + `offload-to-automation` (อัตโนมัติ)

> เคล็ด: ไม่รู้จะเริ่ม combo ไหน → เริ่มที่ `what-skill-do-i-need` · อยากให้ AI route เอง → ใช้ `ai-agent-team` เป็นหัวหน้าทีม · **อยากเห็น AI ทำถึงไหน → วาง `progress-tracker` คู่ combo ไหนก็ได้**

---

## รูปแบบไฟล์ (สำหรับคนอยากเพิ่ม skill)
ทุก skill ใช้โครงเดียวกัน: frontmatter → ใช้เมื่อ → วิธีใช้ → วิธีทำ (AI ทำตาม) → กับดัก (Anti-patterns) → ช่องผู้เชี่ยวชาญเติม → disclaimer
ดูวิธี contribute ที่ [../CONTRIBUTING.md](../CONTRIBUTING.md)
