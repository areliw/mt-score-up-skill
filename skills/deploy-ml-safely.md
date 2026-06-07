---
skill: deploy-ml-safely
title: MT เอาโมเดล ML ไปใช้จริง — ไม่ให้เงียบๆ พัง (Deploy ML Safely)
type: ADVISE               # ช่วยตัดสินใจการนำโมเดลไปใช้ ไม่ใช่สอนเทรน
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-08
status: draft
disclaimer: "ช่วยคิดการนำโมเดล ML ไปใช้จริงเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์ · โมเดลในงานแล็บ/คลินิก = decision-support ต้องมี MT/แพทย์ยืนยัน + validate ก่อนใช้จริง; ข้อมูล training ต้อง de-identify + IRB · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# MT เอาโมเดล ML ไปใช้จริง

ตัวช่วยตอน MT เทรนโมเดลได้แล้ว (เช่น smear/cell classifier, ทำนาย thal, จัด priority) จะเอาไป **ใช้จริง** ยังไงไม่ให้พังเงียบ — เน้น "ก่อน deploy ต้องเช็คอะไร + monitor + human-in-loop" ไม่ใช่สอนเทรนโมเดล

> **กฎ #1:** โมเดลที่ **"แม่นตอนเทรน" ≠ "ใช้ได้จริง"** — performance ตก/drift เมื่อเจอข้อมูลจริง/เครื่องใหม่/เวลาผ่าน → ต้อง validate external + monitor + มีคนตรวจ
> **กับดัก #1 (ขั้น hard):** **model ที่ผิดเงียบในงานคลินิก อันตรายกว่าไม่มีโมเดล** — ไม่มี monitoring + ไม่มี human-in-the-loop จุดที่กระทบคนไข้ = ปล่อยผิดสะสม. โมเดลแล็บ/คลินิก = **decision-support** ต้องมี MT/แพทย์ยืนยัน

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`)

## ใช้เมื่อ
- เทรนโมเดลได้แล้ว (thesis/งานวิจัย/เครื่องมือทีม) จะเอาไปใช้จริง
- กลัวโมเดลแม่นตอนเทสต์แต่พังกับข้อมูลจริง
- ไม่แน่ใจต้องมี monitoring/คนตรวจแค่ไหน (โดยเฉพาะงานคลินิก)

## วิธีใช้
วาง skill นี้ + บอกโมเดล (ทำอะไร/เทรนกับข้อมูลอะไร/จะใช้ที่ไหน) → AI ช่วยไล่ checklist ก่อน deploy + วาง monitoring/fallback + ชี้จุดที่ต้องมี human-in-loop

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### Fork 1 — ก่อน deploy (validation จริง)
- validate บน **external/prospective data** ไม่ใช่แค่ test split ของชุดเดิม
- เช็ค **data leakage** (เชื่อม `ml-judgment`) · ดู **calibration** ไม่ใช่แค่ accuracy/AUC
- งาน imbalanced → **sens/spec/PR curve** ไม่ใช่ accuracy ลอยๆ

### Fork 2 — data drift / distribution shift
- เครื่องใหม่/น้ำยา lot ใหม่/ย้อมต่าง/ประชากรต่าง → performance ตกเงียบ
- monitor **input distribution + output distribution** ต่อเนื่อง → alert เมื่อเพี้ยน

### Fork 3 — monitoring + fallback
- track performance หลัง deploy (ไม่ใช่ deploy แล้วลืม)
- **fallback ไปคน** เมื่อ confidence ต่ำ / input นอก distribution (**reject option**)

### Fork 4 — human-in-the-loop
- งานคลินิก = **โมเดลเสนอ คนตัดสิน**; ทุกผลที่กระทบคนไข้ผ่าน MT/แพทย์ (เชื่อม `clinical-correlation-judgment`, `cv-judgment` สำหรับ image)

### Fork 5 — reproducibility + versioning
- เก็บ version (model + data + เกณฑ์), เงื่อนไข retrain, audit ว่าโมเดลไหนตัดสินอะไรเมื่อไหร่

### Fork 6 — กฎ/จริยธรรม
- training data: **consent/de-identify/IRB** · ระวัง **bias ในข้อมูล** (ประชากร/เครื่องเดียว) · อธิบายได้แค่ไหน (explainability) · ระบุ **ขอบเขตที่ validate** แล้วใช้ในขอบเขตนั้น

## กับดัก (Anti-patterns)
- #1 deploy คลินิกโดยไม่มี human-in-the-loop / monitoring → ผิดเงียบสะสม (กับดัก #1)
- #2 validate แค่ test split (ไม่ external/prospective)
- #3 ดู accuracy บนข้อมูล imbalanced (ควร sens/spec/PR)
- #4 ไม่ monitor drift → ตกเงียบเมื่อเครื่อง/ประชากรเปลี่ยน
- #5 ไม่มี fallback/reject option เมื่อโมเดลไม่มั่นใจ
- #6 ไม่ version โมเดล/ข้อมูล → audit/reproduce ไม่ได้
- #7 training data มี bias/leakage/ไม่ de-identify/ไม่ผ่าน IRB
- #8 ใช้โมเดลนอกขอบเขตที่ validate (เทรนผู้ใหญ่ → ใช้เด็ก; เครื่อง A → เครื่อง B)

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - โมเดลที่คุณทำ + เทรนกับข้อมูลอะไร (เครื่อง/ประชากร/จำนวน) + จะใช้ที่ไหน
> - ใครจะเป็นคน review ผลโมเดลในงานจริง + เกณฑ์ fallback
> - นโยบาย รพ./IRB เรื่อง AI/ML ในงานคลินิก + ข้อมูลผู้ป่วย

NOTE: เลือกโมเดล/metric/validation เชิงลึก → `ml-judgment`; งานภาพ (cell/smear) → `cv-judgment`; รันโปรเจกต์ data → `data-project-survival`; skill นี้ช่วย "เอาโมเดลไปใช้จริงอย่างปลอดภัย"

---
*skill นี้ช่วย "คิด" เพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์ · โมเดลคลินิก = decision-support ต้องมี MT/แพทย์ยืนยัน + validate; training data de-identify + IRB · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
