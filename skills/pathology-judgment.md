---
skill: pathology-judgment
title: โค้ชพยาธิวิทยา — อ่าน pattern + ให้เกณฑ์ + confirm (Pathology Pattern Judgment)
type: ADVISE               # ช่วยอ่าน pattern/กลไก ไม่ใช่ตำราลิสต์โรค
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดอ่าน pattern/กลไกโรคทางพยาธิ เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย — การวินิจฉัยพยาธิจริงต้องโดยพยาธิแพทย์ + ยืนยันด้วย test/IHC/molecular ตาม SOP · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชพยาธิวิทยา — อ่าน pattern + ให้เกณฑ์ + confirm

อ่านกลไกโรค + ตัดสิน pattern ทางพยาธิ — "นี่ benign/malignant? injury กลับได้ไหม? อักเสบบอกอะไร? ต้อง confirm ด้วยอะไร" ไม่ใช่ท่องลิสต์โรค/Robbins (= commodity ดูตำรา)

> **กฎ #1 (benign vs malignant):** **invasion ทะลุ basement membrane / metastasis = ตัวชี้ขาด** — **atypia/pleomorphism/mitosis อย่างเดียวไม่เคยพอ** ฟันธงมะเร็ง (reactive atypia จากอักเสบ/ซ่อมหลอกตาได้)
> **กับดัก #1:** ตี atypia เดี่ยว = มะเร็ง → ผิด. ดูว่า "ทะลุ BM ยัง / มี metastasis ไหม" ก่อนเสมอ
> ⚠️ **ขอบที่ลื่น:** metastasis เป็น **เกณฑ์เดี่ยวที่แข็งสุด** แต่ **ไม่ใช่ 100%** — มีข้อยกเว้นหายาก (Spitz nevus, benign metastasizing leiomyoma); ไม่มีเกณฑ์ใดเกณฑ์เดียวฟันธงเด็ดขาด → อ่านครบทุกแกน + confirm ด้วย test ที่ถูก
> เชื่อมเคส lab → ตั้ง DDx/ชี้ทาง (ส่งต่อแพทย์) → ดู `clinical-correlation-judgment`

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- อ่านชิ้นเนื้อ/รายงานพยาธิ/เคส → **benign หรือ malignant**, dysplasia ข้ามเส้นยัง, grade/stage
- เชื่อมโยง **lab/morphology → กลไกโรค** (ทำไมค่านี้ผิด, อักเสบแบบไหน, injury กลับได้ไหม)
- (สาย sales) เข้าใจ pathophysiology โรค → ทำไม test/biomarker/companion Dx จำเป็นใน pathway

## วิธีใช้
วาง skill นี้ + เล่าภาพ/รายงาน/เคส → AI อ่าน pattern + เกณฑ์ (benign/malignant · reversible/irreversible · acute/chronic) → confirm + ส่งต่อพยาธิแพทย์

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — Benign vs Malignant (เกณฑ์ 5 แกน — metastasis แน่สุด)
อย่าตัดสินจากแกนเดียว — ดูครบ:
| แกน | Benign | Malignant |
|---|---|---|
| Differentiation | ดี เหมือนเนื้อต้นกำเนิด | anaplasia, pleomorphism, N:C สูง, mitosis ผิดปกติ |
| Growth rate | ช้า | เร็ว |
| **Invasion** | มี capsule ไม่ลุก | **ทะลุ basement membrane / ลุกลามรอบ** |
| **Metastasis** | ไม่มี | **มี = พิสูจน์ malignant แน่นอนสุด** |
| Border | ขอบเรียบ | ขอบรุก |
- ⚠️ **metastasis = เกณฑ์เดี่ยวที่แข็งสุด** (เกือบทั้งหมด benign ไม่ metastasis) — แต่ **ไม่ใช่ 100%** (Spitz nevus, benign metastasizing leiomyoma เป็นข้อยกเว้นหายาก); ตัวอื่นช่วยชี้แต่ไม่ขาด
- ⚠️ **atypia/mitosis เดี่ยว ≠ มะเร็ง** — reactive atypia (อักเสบ/ซ่อม) ดูดุได้; เส้นตัดสินจริงที่อ่านได้คือ **ทะลุ BM / invasion** (Fork 7)
- nomenclature: -oma = benign · carcinoma (epithelial)/sarcoma (mesenchymal) = malignant · ⚠️ ข้อยกเว้นหลอก: **lymphoma/melanoma/seminoma = malignant** แม้ลงท้าย -oma

### Fork 2 — Reversible vs Irreversible cell injury (point of no return)
- **Reversible:** cell swelling, fatty change, ribosome หลุด — ตัดต้นเหตุแล้วฟื้น
- **Irreversible:** **เยื่อหุ้มเซลล์/mitochondria พัง + Ca²⁺ ไหลเข้า + เอนไซม์รั่ว** → necrosis · สัญญาณ: nuclear change (pyknosis→karyorrhexis→karyolysis), enzyme รั่วเข้าเลือด (troponin/AST/LDH)
- judgment: เห็น enzyme รั่ว (cardiac/liver) = เซลล์ตายจริง ไม่ใช่บาดเจ็บชั่วคราว

### Fork 3 — Necrosis type → ชี้สาเหตุ/ตำแหน่ง
**Coagulative** = ischemia/infarct อวัยวะแข็ง (หัวใจ/ไต) · **Liquefactive** = สมอง (CNS infarct)/หนอง (bacterial) · **Caseous** = **TB/granuloma** · **Fat** = ตับอ่อนอักเสบ (saponification) · **Fibrinoid** = vessel ใน immune/vasculitis/malignant HT · **Gangrene** = แขนขา ischemia (dry/wet) — อ่านชนิด necrosis ย้อนหาสาเหตุได้

### Fork 4 — Necrosis vs Apoptosis (มีอักเสบหรือไม่)
- **Necrosis** = บาดเจ็บ เซลล์บวมแตก เนื้อหารั่ว → **มี inflammation**
- **Apoptosis** = programmed เซลล์หด apoptotic body **ไม่มี inflammation** (councilman body, เซลล์ที่ถูกกำจัดปกติ)

### Fork 5 — Acute vs Chronic inflammation → implication
- **Acute** = นาที-วัน, **neutrophil**, exudate, 5 อาการ (rubor/tumor/calor/dolor/functio laesa)
- **Chronic** = สัปดาห์+, **lymphocyte/plasma cell/macrophage**, มี **tissue destruction + repair (fibrosis) + angiogenesis** พร้อมกัน
- ⚠️ **chronic inflammation = ปัจจัยเสี่ยงมะเร็ง** (HBV→HCC, H.pylori→gastric, chronic colitis→colon, O.viverrini→cholangio) → เห็น chronic ที่ไหน คิดถึง malignant transformation · granuloma (subtype) → Fork 8

### Fork 6 — Grading vs Staging (อันไหน drive อะไร)
- **Grade** = เนื้อร้ายดูดุแค่ไหน (differentiation, mitosis) — well/moderate/poorly diff
- **Stage (TNM)** = ลุกลามไปไกลแค่ไหน (Tumor invasion, Node, Metastasis)
- ⚠️ **Staging มีผลต่อ prognosis + เลือกการรักษา > grading** (M1 = เปลี่ยนเกม) → ตอบ "ทำไม biopsy + imaging + sentinel node" = เพื่อ stage
- *(สาย sales)* companion Dx/molecular มักเข้ามาที่จุด "เลือก targeted therapy ตาม stage/marker"

### Fork 7 — Dysplasia → Cancer (เส้นแบ่งคือ basement membrane)
- **Dysplasia** (low→high grade) = เซลล์ผิดปกติแต่ **ยังไม่ทะลุ BM** = reversible ได้ · **CIS** = ผิดเต็มความหนาแต่ยังไม่ทะลุ · **Invasive cancer** = **ทะลุ BM แล้ว** = irreversible, metastasis ได้
- judgment: รายงานบอก "ทะลุ BM ยัง" = จุดตัดสินสำคัญสุด (in-situ vs invasive เปลี่ยนการรักษาทั้งหมด)

### Fork 8 — Effusion · Thrombus vs clot · Granuloma DDx · Hypersensitivity
- **Exudate (อักเสบ/มะเร็ง/ติดเชื้อ) vs Transudate (CHF/cirrhosis/nephrotic)** → ตัดสินด้วย **Light's criteria เป็นหลัก** (pleural/serum protein >0.5 · LDH ratio >0.6 · LDH >⅔ ULN — เข้าข้อใดข้อหนึ่ง = exudate); **SG/โปรตีนเป็นแค่ตัวประมาณคร่าว** (SG cutoff จริง ~1.022 ไม่ใช่ 1.020) · Light's เองก็ misclassify transudate ~15-20% เป็น exudate → exudate ต้องหา cause (มะเร็ง/ติดเชื้อ) + ส่ง cytology
- **Thrombus (ก่อนตาย) vs postmortem clot:** thrombus = **lines of Zahn** + เกาะผนัง vessel · postmortem = "chicken fat/currant jelly" ไม่เกาะ
- **Granuloma → DDx:** **caseating = TB** (confirm AFB/culture/GeneXpert ก่อนเสมอ) · non-caseating = sarcoid/Crohn/foreign body/leprosy/fungal → อย่าฟันธง TB จากภาพอย่างเดียว
- **Hypersensitivity I–IV:** I = IgE/anaphylaxis · **II = Ab ต่อ Ag บนเซลล์** (transfusion reaction, HDFN, AIHA) · **III = immune complex ลอย** (SLE, serum sickness, GN) · IV = T-cell delayed (TB skin test, contact derm) → สับบ่อยที่ **II (Ag ติดเซลล์) vs III (complex ลอยแล้วตก)**

---

## กับดัก (Anti-patterns)
- 🚫 **ฟันธง malignant จาก atypia/mitosis เดี่ยว** — ไม่เคยพอ; **invasion ทะลุ BM / metastasis** คือตัวชี้ขาด · reactive atypia (อักเสบ/ซ่อม) ดูน่ากลัวแต่ไม่ใช่มะเร็ง · กลับกัน อย่าอ่าน metastasis ว่า 100% (ข้อยกเว้นหายากมี)
- 🚫 **tumor marker / IHC เดี่ยว = วินิจฉัย** — marker (PSA/CEA/CA125/AFP) ใช้ติดตาม/ชี้ทาง ไม่ใช่ฟันธง; IHC ต้องเป็น panel + บริบท morphology
- 🚫 **miss invasion ผ่าน basement membrane** — in-situ vs invasive ต่างกันที่ BM = เปลี่ยนการรักษา/พยากรณ์ทั้งหมด
- 🚫 **granuloma = TB เลย** ไม่ confirm — caseating ชวน TB แต่ต้อง AFB/culture/molecular ยืนยัน
- 🚫 **ตี postmortem clot เป็น thrombus** — ไม่มี lines of Zahn + ไม่เกาะผนัง = clot หลังตาย
- 🚫 **มองข้าม malignant effusion** — exudate (ตาม Light's, ไม่ใช่ SG เดี่ยว) ต้องส่ง cytology หาเซลล์มะเร็ง; ตี exudate เป็น transudate = พลาด cause
- 🚫 **ลืม chronic inflammation = precancer** — chronic ที่ไม่หาย (HBV/HCV, H.pylori, fluke, colitis) → เฝ้าระวัง dysplasia/มะเร็ง
- 🚫 **สับ necrosis กับ apoptosis** — apoptosis ไม่มีอักเสบ; เห็นอักเสบรอบ = necrosis
- 🚫 **สับ hypersensitivity II vs III** — transfusion/AIHA = II (Ag บนเซลล์); SLE/serum sickness = III (complex ลอย)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติม war-story จริง เช่น:
> - *"(MT) เคสที่เกือบอ่าน reactive atypia เป็นมะเร็ง จับได้เพราะ..."*
> - *"granuloma ที่ดูเหมือน TB แต่จริงเป็น... จับได้เพราะ confirm ด้วย..."*

---
*ช่วยคิดอ่าน pattern/กลไกโรคทางพยาธิ เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย — การวินิจฉัยพยาธิจริงต้องโดยพยาธิแพทย์ + ยืนยันด้วย test/IHC/molecular ตาม SOP · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
