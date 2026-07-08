---
skill: method-validation-stats
title: สถิติเฉพาะ MT — method comparison / reference interval / diagnostic accuracy (Method & Validation Stats)
type: ADVISE               # ช่วยเลือก+ตีความสถิติงานแล็บ ไม่ใช่รันเลขให้
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-11
status: draft
disclaimer: "ช่วยคิดสถิติงาน verification/validation/วิจัยแล็บเพื่อการศึกษา ไม่ใช่ที่ปรึกษาสถิติทางการ · เกณฑ์ยอมรับทางคลินิกต้องอิง CLSI/SOP แลบ + ปรึกษานักสถิติเมื่อตีพิมพ์ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# สถิติเฉพาะ MT (method/validation)

ตัวช่วยตัดสินใจสถิติที่ MT เจอจริงแต่ตำราสถิติทั่วไปไม่ครอบ — method comparison, reference interval, diagnostic accuracy, precision/QC. เน้น "ใช้ตัวไหน + กับดัก"

> **กฎ #1:** เลือกสถิติตาม **"คำถามแบบงานแล็บ"** ไม่ใช่ default ทั่วไป — เทียบ 2 วิธีตรวจ ≠ correlation; ตั้ง reference interval ≠ mean±2SD เสมอ
> **กับดัก #1 (ขั้น hard):** ใช้ **correlation (r) หรือ paired t-test ตัดสิน "2 method แทนกันได้ไหม" = ผิด**. r สูงไม่ได้แปลว่า agree (มี constant/proportional bias ได้ทั้งที่ r≈1); paired-t บอกแค่ "ต่างกันเชิงสถิติ" ไม่บอกขนาด bias ที่ยอมรับทางคลินิก → ใช้ **Bland-Altman + Passing-Bablok/Deming**

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`)

## ใช้เมื่อ
- เทียบวิธี/เครื่องตรวจใหม่ vs เก่า (method comparison / verification)
- ตั้งหรือ verify reference interval
- ประเมิน test diagnostic (sens/spec/PPV/ROC)
- ดู precision/QC (CV, repeatability/reproducibility, sigma)

## วิธีใช้
วาง skill นี้ + บอกคำถาม (เทียบ method? ตั้งช่วงอ้างอิง? ประเมิน test?) + ข้อมูลที่มี → AI ชี้สถิติที่ถูก + กับดัก + เกณฑ์ที่ควรอิง (CLSI) แล้วชี้ให้คุณรัน/ปรึกษานักสถิติเอง

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### Fork 1 — Method comparison (วิธีใหม่ vs reference)
- **Bland-Altman**: plot ผลต่าง vs ค่าเฉลี่ย → bias (mean diff) + limits of agreement (±1.96SD); ดูว่า bias อยู่ในเกณฑ์ยอมรับทางคลินิกไหม
- **Passing-Bablok / Deming regression** (ไม่ใช่ OLS — เพราะ x ก็มี error) → จับ **constant bias (intercept) + proportional bias (slope)**
- อ้าง **CLSI EP09**; **ห้ามใช้ r/paired-t** ตัดสิน agreement
- 🇹🇭 CLSI EP เป็นวิธีสากล (ไม่มี Thai equivalent) — แต่ verification ที่ทำเพื่อขอ/ต่อ **accreditation ไทย** ต้องผ่านเกณฑ์แลบ + **อนุมัติโดย MT ผู้รับผิดชอบ ตามมาตรฐานงานเทคนิคการแพทย์ (LA)/สภาเทคนิคการแพทย์** ("CLSI pass" อย่างเดียวไม่พอ)

### Fork 2 — Reference interval
- **CLSI EP28**: nonparametric **2.5/97.5 percentile**, ต้อง **n ≥ 120** (per partition)
- **partition** ตามเพศ/อายุเมื่อต่างจริง · **transference = ยืมช่วงอ้างอิงจากที่อื่น/ผู้ผลิต แล้ว verify ด้วย n=20 ของ population เรา — ≤2/20 หลุดช่วง = ผ่าน (CLSI EP28)**
- **อย่าใช้ mean±2SD** ถ้าข้อมูลไม่ Gaussian (ค่าแล็บส่วนใหญ่เบ้)

### Fork 3 — Diagnostic accuracy
- 2×2 ให้ถูก → **sens/spec/PPV/NPV/LR+,LR−**, **ROC-AUC** เทียบ cutoff
- **PPV/NPV ขึ้นกับ prevalence** — รายงานต้องระบุ population (เชื่อม `immunoassay-judgment`, `critical-appraisal-judgment`)
- ⚠️ **sens/spec/agreement มีความหมายเทียบกับ "reference standard" ที่เลือกเท่านั้น — reference แย่ = ตัวเลขเพี้ยน (imperfect-gold-standard bias):** ถ้า validate เทียบ **gold standard ที่ไม่สมบูรณ์** หรือ (แย่กว่า) **เทียบกับ test อีกตัวที่ไม่ใช่ reference มาตรฐานของโรคนั้น** (เช่น ชุดตรวจ antigen ใหม่เทียบ serology อีกวิธี แทน reference ที่ยอมรับตาม target condition/SOP — microscopy/culture/PCR/composite แล้วแต่โรค) → sens/spec/%agreement/**Kappa** **เพี้ยนได้ทั้งสูง/ต่ำ** (ขึ้นกับ error ของ reference + shared/conditional-dependent error) ทั้งที่ test อาจไม่ดีจริง · **ก่อนเชื่อตัวเลข ถามก่อน: reference คืออะไร + ยอมรับตาม target condition ไหม** (ไม่มี gold สมบูรณ์ → *พิจารณา* composite/latent-class reference — มีสมมติฐาน/ข้อจำกัด ไม่ใช่ fix อัตโนมัติ + รายงานข้อจำกัด)
- ⚠️ **แยก "diagnostic performance ใน study (study-condition)" ออกจาก "implementation/process error ตอนใช้จริง (field)":** false positive ภาคสนามอาจมาจาก **คนอ่าน cut-off ไม่ผ่าน training · เลย time window · lot-to-lot variation (spec แกว่งตาม lot)** — ไม่ใช่ค่า sens/spec ของตัว test ใน study · ตัวเลขจาก 1 study/1 lot ไม่การันตีทุก lot/ทุกมือ (verify เอง)

### Fork 4 — Precision / QC stats
- **repeatability (within-run) vs reproducibility (between-run/day)** — คนละค่า; **CLSI EP05**
- **CV%** เทียบกับ allowable; **sigma metric** = (TEa − bias)/CV → กลยุทธ์ QC (เชื่อม `clinchem-judgment`, `lab-management-judgment`)

### Fork 5 — Sample size (ต่างจาก t-test ทั่วไป)
- method comparison ~**40–100+** (ตาม range + EP09) · reference interval **≥120** · sens/spec ตาม **width ของ CI ที่ยอมรับ** (เชื่อม `sample-size-power`)

### Fork 6 — Agreement แบบ categorical
- ใช้ **Cohen's kappa / weighted kappa** ไม่ใช่ **%agreement** (ซึ่งพอง chance agreement)

## กับดัก (Anti-patterns)
- #1 r / paired-t ตัดสิน method agreement (กับดัก #1) → ควร Bland-Altman + PB/Deming
- #2 OLS regression แทน Deming/Passing-Bablok (ลืมว่า x มี error)
- #3 mean±2SD ตั้ง reference interval ทั้งที่ไม่ Gaussian / n<120
- #4 รายงาน PPV โดยไม่ระบุ prevalence/population
- #5 สับ repeatability กับ reproducibility
- #6 %agreement แทน kappa (categorical)
- #7 ตัดสิน method ด้วย p-value (significance) แทน clinical acceptability (bias ที่ยอมรับได้)
- #8 ใช้ accuracy บน prevalence ต่ำ/ข้อมูล imbalanced → หลอก (ควร sens/spec/LR)
- #9 ประเมิน sens/spec/agreement เทียบ **comparator ที่ไม่ใช่ reference มาตรฐานของโรคนั้น** (เช่น serology อีกตัว แทน microscopy/culture/PCR) → imperfect-gold-standard bias, ตัวเลข**เพี้ยนได้ทั้งสูง/ต่ำ** อ่านความหมายไม่ได้; ระบุ reference + คุณภาพมันเสมอ (Fork 3)

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - TEa/allowable bias ของ analyte ที่คุณ validate (อิง CLIA/biological variation/SOP)
> - เกณฑ์ยอมรับ method comparison ของแลบคุณ + จำนวนตัวอย่างที่ใช้จริง
> - reference interval ที่ใช้มาจากไหน (ตั้งเอง/ยืม/ผู้ผลิต) + verify หรือยัง

NOTE: การรันสถิติจริง (โปรแกรม/สูตร) → ใช้ `r2r-stats` (`needs: code-interpreter`) หรือซอฟต์แวร์สถิติ; เลือก test ทั่วไป → `choose-stat-test`; ทฤษฎีลึก → ตำราสถิติ/CLSI

---
*skill นี้ช่วย "คิด/เลือกสถิติ" เพื่อการศึกษา · เกณฑ์ยอมรับทางคลินิกอิง CLSI/SOP; งานตีพิมพ์ปรึกษานักสถิติ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
