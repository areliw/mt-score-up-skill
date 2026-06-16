---
skill: histotech-cytology-judgment
title: งานชิ้นเนื้อ/เซลล์วิทยา (histo/cyto) ให้เป็น — adequacy · fixation · stain QC · artifact vs จริง (Histotechnology & Cytology Process Judgment)
type: ADVISE               # ช่วยตัดสินด่าน process ไม่ใช่วินิจฉัย/อ่านผลแทน pathologist
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-16
status: draft
disclaimer: "เพื่อการศึกษา/ช่วยทบทวนงาน process ทาง histo/cyto ไม่ใช่การวินิจฉัย — เกณฑ์ adequacy/fixation time/protocol ต่างกันตาม guideline (เช่น Bethesda, CAP/ASCO)/SOP/ชนิดงาน ต้อง verify ฉบับล่าสุดเอง · การแปลผล benign/malignant เป็นของพยาธิแพทย์ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# งานชิ้นเนื้อ/เซลล์วิทยา (histo/cyto) ให้เป็น — adequacy · fixation · stain QC · artifact vs จริง

ก่อนพยาธิแพทย์จะอ่านสไลด์ได้ ต้องผ่าน **fixation → processing → sectioning → staining → adequacy**. ผิดตรงนี้ = แพทย์อ่านของเสีย/พลาดมะเร็ง โดยที่ตัวเลขไม่ฟ้อง. สกิลนี้ช่วยตัดสิน **adequacy / fixation / stain QC / artifact** — *ไม่ใช่* การอ่านว่า benign/malignant (นั่นคือ `pathology-judgment` + พยาธิแพทย์; **MT ไม่วินิจฉัย**)

> **กฎ #1:** **fixation/cold-ischemia = ขั้นที่ "ทำซ้ำบนเนื้อเดิมไม่ได้"** (ต่างจาก re-cut/re-stain). fixation ช้า/ผิด/นานเกิน → **อาจ**กระทบ morphology + antigen/nucleic-acid → IHC/molecular (เช่น ER/PR/HER2) **อาจ uninterpretable** (ขึ้นกับ assay/tissue/marker/validation) → document/flag ให้แล็บ/พยาธิแพทย์ตัดสิน repeat/specimen ใหม่. เวลา/ชนิด fixative ตาม guideline (เช่น CAP/ASCO breast markers — verify edition) + ปลายทางที่จะส่งตรวจ — *ตัดสินก่อนจุ่ม*
> **กับดัก #1:** รับ specimen ที่ **inadequate** มา process/screen แล้วอ่าน → **false-negative** เพราะ "ไม่มีเซลล์เป้า" ≠ "ปกติ" (พลาดมะเร็งได้). เช็ค adequacy *ก่อน*
> โยง: `pathology-judgment` (ฝั่งอ่านผล — MT ไม่วินิจฉัย) · `preanalytical-judgment` (การรับ/ขนส่ง specimen ต้นทาง) · `molecular-judgment` (fixation/decalcification กระทบ molecular downstream)

## ใช้เมื่อ
- รับชิ้นเนื้อ/cytology แล้วตัดสิน **accept / process-with-flag / recollect** (adequate ไหม)
- ตัดสิน **fixation** (fixative อะไร · นานเท่าไร · cold-ischemia เกินไหม) โดยเฉพาะเมื่อมี IHC/molecular ปลายทาง
- cytology: เลือก **air-dried vs wet-fixed** ให้ตรง stain
- เจอสไลด์ "ดูแปลก" — **artifact หรือของจริง** → re-cut/re-stain หรือส่งอ่าน?
- **stain/IHC control** ไม่ติด — เชื่อผลได้ไหม

## วิธีใช้
วาง skill นี้ + เล่า (ชนิด specimen, fixative/เวลา, จะส่ง IHC/molecular ไหม, อาการสไลด์) → AI ช่วยชี้ accept/recollect + จุด fixation/stain ที่ต้องระวัง + แยก artifact. *เกณฑ์ตัวเลขตาม guideline/SOP จริง — verify*

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — specimen adequacy: accept / process-with-flag / recollect
- **cytology:** มีเซลล์เป้า "พอประเมิน" ไหมตามเกณฑ์ของงานนั้น (เช่น Pap cervical: ดู cellularity/สิ่งบดบัง ตาม Bethesda — **รายงานการมี/ไม่มี TZ/endocervical component ตาม edition/SOP แต่ "ไม่มี TZ" อย่างเดียว *ไม่ได้* แปลว่า unsatisfactory** · FNA: cellularity พอ/ROSE · body fluid: ปริมาณ+การถนอม)
- **histo:** fix ถูก/พอ · ระบุ orientation/margin/ฝั่ง · ขนาดพอตัด section
- **inadequate → flag/แจ้ง-แนะนำ recollect (ตาม SOP/พยาธิแพทย์/แพทย์เจ้าของไข้)** ดีกว่าเงียบแล้วปล่อยอ่านมั่ว (false-negative อันตราย). *แต่*ถ้า recollect ไม่ได้ (เช่น resection ก้อนเดียว) → process + **flag limitation** ให้พยาธิแพทย์
- *เกณฑ์ adequacy เป็นของ guideline/SOP — ไม่ฟันธงตัวเลขสากล*

### Fork 2 — fixation: ด่านทำลาย downstream เงียบ (irreversible)
- **เลือก fixative ตามปลายทาง *ก่อน*จุ่ม:** 10% neutral buffered formalin = มาตรฐาน histo ส่วนใหญ่ · บางงานต้องการ fresh/แช่แข็ง หรือ medium เฉพาะ (เช่น บาง molecular/flow/microbiology/frozen section) — จุ่ม formalin ไปแล้วบางอย่างทำไม่ได้
- **cold-ischemia + fixation time:** สั้นเกิน (under-fix) / นานเกิน (over-fix) → **อาจ**กระทบ morphology + antigenicity/nucleic-acid → IHC/molecular **อาจ uninterpretable** (ขึ้นกับ assay/marker/validation) — สำคัญกับ predictive markers เช่น ER/PR/HER2 (เวลาตาม CAP/ASCO — verify ฉบับล่าสุด)
- **decalcification** (ชิ้นกระดูก): **acid-decalc เสี่ยงสุด** (ทำลาย nucleic acid/antigen) · EDTA อ่อนกว่าแต่ช้า → **validate IHC/molecular บนเนื้อ decalcified** ก่อนเชื่อ
- ⚠️ **fixation/decalc = ทำซ้ำบนเนื้อเดิมไม่ได้** → ระวังสูงสุด (re-cut/re-stain แก้ทีหลังได้ แต่ขั้น fixation ไม่ได้)

### Fork 3 — air-dried vs wet-fixed (cytology) — เลือกตาม stain ที่จะใช้
- **air-dried → Romanowsky (Diff-Quik/Giemsa)** (เด่น cytoplasm/background/organism/colloid) · **wet-fixed (alcohol/spray ทันที) → Pap stain** (เด่น nuclear detail/chromatin)
- ⚠️ **mismatch = สไลด์เสีย** (air-dried แล้วย้อม Pap → nuclear detail พัง · ปล่อยแห้งก่อน wet-fix → drying artifact) — ตัดสิน fixation **ตอนเก็บ/ป้าย** ตาม stain เป้าหมาย
- FNA มัก smear ทั้ง 2 แบบ (air-dried + wet-fixed) เพื่อได้ทั้งสองมุม + เผื่อ ancillary
- *นี่คือ routine/SOP — มีข้อยกเว้น เช่น rehydrated/ultrafast Pap ที่ rehydrate air-dried smear ได้*

### Fork 4 — artifact vs ของจริง (อย่าให้ artifact ถูกอ่านเป็น pathology)
- **artifact ที่พบบ่อย:** fold/wrinkle, chatter, knife mark, bubble, over/under-stain, drying artifact, formalin pigment, crush (FNA), cautery — *ดูเหมือน*ผิดปกติแต่ไม่ใช่
- **ตัดสิน:** artifact ที่บัง diagnosis → **re-cut / re-stain / re-process** (ทำซ้ำได้) ก่อนส่งอ่าน — อย่าให้แพทย์อ่านสไลด์ที่ artifact บัง
- ⚠️ ขอบเขต: **MT/histo-cyto-tech ไม่วินิจฉัย** — แต่ "สไลด์นี้พร้อมอ่าน/artifact บังไหม / ต้อง re-cut ไหม" = หน้าที่ตรงๆ (cytotech บางระบบมีบทบาท screen/flag ตามกฎหมายแต่ละที่ — *การยืนยัน dx = พยาธิแพทย์*, โยง `pathology-judgment`)

### Fork 5 — stain/IHC QC: control slide
- **special stain/IHC ต้องมี control ที่เหมาะสม** (positive/internal/batch/on-slide; negative reagent control **ตาม CAP/SOP/validated protocol** ไม่ใช่ทุกการตั้งค่า) — **control ที่กระทบไม่ติด = ผล/assay *ตัวที่กระทบ* invalid จนแก้** (อาจไม่กระทบ antibody/stain อื่นใน run เดียว) → re-stain
- ⚠️ **IHC "negative" ที่ control ก็ไม่ติด = invalid ไม่ใช่ true-negative** (เหมือน QC fail — ห้าม report ผลจาก run ที่ control fail)
- H&E: เช็ค nuclear/cytoplasmic contrast + ความสม่ำเสมอ · ติดซีด/เข้มเกิน/ไม่ differentiate → re-stain

---

## กับดัก (Anti-patterns)
- **process/screen specimen ที่ inadequate โดยไม่ flag adequacy** → false-negative (พลาดมะเร็ง) เพราะ "ไม่เจอเซลล์เป้า" ≠ "ปกติ"
- **fixation ช้า/ผิด/decalc acid แรงเกิน** → IHC/molecular (ER/PR/HER2 ฯลฯ) *อาจ* uninterpretable (validate/flag ให้พยาธิแพทย์ตัดสิน — ขั้น fixation ทำซ้ำบนเนื้อเดิมไม่ได้)
- **air-dried vs wet-fixed mismatch** → สไลด์เสีย ย้อมไม่ขึ้น/nuclear พัง
- **ปล่อย artifact ถูกอ่านเป็น pathology / ส่งสไลด์ artifact-บัง** โดยไม่ re-cut/re-stain
- **IHC/special-stain control fail แล้วรายงาน negative** (invalid ≠ negative)
- **จุ่ม formalin ทันทีทั้งที่ปลายทางต้องการ fresh** (frozen/flow/บาง molecular) — เลือก fixative หลังคิดปลายทางไม่ได้
- **MT ก้าวไปวินิจฉัย benign/malignant** — เกินขอบเขต (งานคือ process + adequacy + flag)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมจากประสบการณ์จริง เช่น:
> - *"เคส fixation/cold-ischemia ที่ทำให้ HER2/IHC ใช้ไม่ได้ — บทเรียนคือ..."*
> - *"adequacy ที่แล็บผมใช้ตัดสิน recollect-vs-process คือ..."*
> - *"artifact ที่เคยเกือบถูกอ่านเป็น pathology — แยกได้เพราะ..."*

---
*เพื่อการศึกษา/ช่วยทบทวนงาน process ทาง histo/cyto ไม่ใช่การวินิจฉัย — เกณฑ์ adequacy/fixation/protocol ต่างกันตาม guideline (Bethesda, CAP/ASCO ฯลฯ)/SOP/ชนิดงาน ต้อง verify ฉบับล่าสุดเอง · การแปลผล benign/malignant เป็นของพยาธิแพทย์ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
