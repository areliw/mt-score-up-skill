---
skill: flow-cytometry-judgment
title: โค้ช flow cytometry — gate ถูก + อ่าน pattern + correlate (Flow Cytometry Judgment)
type: ADVISE               # ช่วยตัดสินใจ gating/panel/ตีความ ไม่ใช่ atlas marker
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-08
status: draft
disclaimer: "ช่วยคิดงาน flow cytometry เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รักษา และไม่ตัดสินใจแทน · ผล immunophenotyping ต้อง correlate morphology/clinical/genetics + ยืนยันโดยผู้เชี่ยวชาญ/แพทย์ ทำตาม SOP/QC ของแล็บ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช flow cytometry

ตัวช่วยตัดสินใจงาน flow (immunophenotyping leukemia/lymphoma, CD4, PNH, lymphocyte subset, MRD) — เน้น "gate ถูก + อ่าน pattern + correlate" ไม่ใช่ atlas CD marker

> **กฎ #1:** flow ตีความจาก **population + pattern (intensity/relationship)** ไม่ใช่ marker เดี่ยว — ต้อง **gate ให้ถูก population ก่อน** + correlate morphology/clinical เสมอ
> **กับดัก #1 (ขั้น hard):** **gating ผิด** (รวม debris/doublet/เซลล์ตาย หรือ gate ผิด population) → ผล % เพี้ยน + แปล population ผิด. ต้อง gate **viability + singlet + scatter (CD45/SSC)** ก่อนอ่าน marker

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = ผู้เชี่ยวชาญ/แพทย์ยืนยัน

## ใช้เมื่อ
- วาง gating strategy / panel หรือ debug ผล flow ที่ดูแปลก
- อ่าน immunophenotype → blast lineage / lymphoma / PNH / CD4
- ผล flow ขัด smear/clinical → เชื่อ/ทำอะไรต่อ

## วิธีใช้
วาง skill นี้ + บอกงาน (panel/ผล/scatter plot ที่อธิบายได้) + บริบทคน → AI ช่วยไล่ gating + ชี้ pattern + เตือน control/compensation แล้วชี้ให้ correlate morphology + ยืนยันเอง

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### ก่อนวิเคราะห์ — เช็คคุณภาพ
- sample viability + อายุ sample + จำนวนเซลล์พอไหม · **compensation/spillover** ตั้งถูกไหม · มี **control (FMO/isotype)** ไหม

### Fork 1 — gating strategy (ลำดับ)
scatter (FSC/SSC) → **singlet** (กัน doublet) → **viable** (กัน dead) → **CD45 vs SSC** (แยก blast gate / lymphocyte / mono / granulocyte) → marker เฉพาะใน gate ที่สนใจ

### Fork 2 — panel design
- lineage marker + maturation marker; เลือก CD ให้ครอบ DDx (AML vs ALL vs lymphoma)
- **aberrant phenotype** (marker ผิดที่/ผิดเวลา) = clue สำคัญของ malignancy/MRD

### Fork 3 — อ่าน pattern ไม่ใช่ marker เดี่ยว
- ดู **% + intensity (dim/bright) + ความสัมพันธ์ระหว่าง marker** (co-expression)
- เทียบกับ normal maturation pattern → ผิดปกติตรงไหน

### Fork 4 — แอปจริง
- leukemia/lymphoma immunophenotyping · **CD4** (HIV monitoring) · **PNH** (CD55/CD59 loss, FLAER) · **MRD** · lymphocyte subset

### Fork 5 — correlate (flow ไม่ใช่คำตอบเดี่ยว)
- correlate **smear/morphology + clinical + cytogenetics/molecular** (เชื่อม `hematology-judgment`, `pathology-judgment`, `molecular-judgment`) — diagnosis เป็นหน้าที่แพทย์/ผู้เชี่ยวชาญ

### Fork 6 — QC instrument
- setup/CST beads, PMT voltage, daily QC, compensation matrix เป็นปัจจุบัน

## กับดัก (Anti-patterns)
- #1 gate ไม่ตัด dead/doublet/debris → % เพี้ยน, population ผิด (กับดัก #1)
- #2 compensation/spillover ผิด → marker ดู positive ปลอม
- #3 ไม่มี FMO/isotype control → ขีดเส้น positive/negative มั่ว
- #4 อ่าน marker เดี่ยวไม่ดู pattern/co-expression
- #5 ไม่สน intensity (dim vs bright) → พลาด aberrant phenotype
- #6 ไม่ correlate morphology/clinical → ตีความลอย
- #7 สรุป diagnosis จาก flow อย่างเดียว (ข้าม smear/genetics/แพทย์)
- #8 sample เก่า/viability ต่ำ แล้วเชื่อผลเต็มร้อย

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - panel + gating template ที่แลบคุณใช้ (marker/fluorochrome/เครื่อง)
> - เกณฑ์ positive/aberrant + cutoff ของแลบคุณ (โดยเฉพาะ MRD/PNH)
> - เคสที่ flow ขัด morphology → ทีมตัดสินยังไง

NOTE: knowledge (CD marker เต็ม, fluorochrome spectra, ตาราง phenotype ต่อโรค) → ตำรา/แหล่งอ้างอิง; smear/morphology → `hematology-judgment`; skill นี้ช่วย "gate/อ่าน pattern/correlate"

---
*skill นี้ช่วย "คิด" เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย · ผล immunophenotyping ต้อง correlate morphology/clinical/genetics + ยืนยันโดยผู้เชี่ยวชาญ/แพทย์ ทำตาม SOP/QC · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
