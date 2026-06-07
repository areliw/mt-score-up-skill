---
skill: preanalytical-judgment
title: โค้ช pre-analytical — เจาะ/หลอด/ระบุตัว/ขนส่ง ให้ตัวอย่างเชื่อได้ (Pre-Analytical & Phlebotomy Judgment)
type: ADVISE               # ช่วยตัดสินใจคุณภาพตัวอย่าง ไม่ใช่ตำราเทคนิคเจาะ
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-08
status: draft
disclaimer: "ช่วยคิดเรื่องคุณภาพตัวอย่างก่อนวิเคราะห์เพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ตัดสินใจแทน · ตัวอย่างผิด = ผลผิด = หมอรักษาผิด → ทุก reject/accept/แก้ค่า ต้องทำตาม SOP แลบ + ยืนยันกับ MT ผู้รับผิดชอบ; การระบุตัวผู้ป่วย/wrong-blood-in-tube เกี่ยวชีวิตโดยตรง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช pre-analytical (เจาะเลือด/จัดการตัวอย่าง)

ตัวช่วยตัดสินใจคุณภาพตัวอย่าง **ก่อน**เข้าเครื่อง — เน้น "ค่านี้น่าสงสัยเพราะตัวอย่างหรือเปล่า + เจาะ/จัดการยังไงไม่ให้พลาด" ไม่ใช่ตำราขั้นตอนเจาะเลือด

> **กฎ #1:** pre-analytical = **~60–70% ของ lab error ทั้งหมด**. ค่าประหลาด → สงสัย "ตัวอย่าง" (เจาะ/หลอด/order/เวลา/ขนส่ง/ระบุตัว) **ก่อน**โทษเครื่องหรือรีรัน
> **กับดัก #1 (ขั้น hard):** "ค่าเพี้ยน แต่ analyzer + QC ปกติ" → ส่วนใหญ่คือ pre-analytical ไม่ใช่ analytic. **รีรันหลอดเดิมได้ค่าเดิม ≠ ค่าถูก** — ถ้า hemolyzed/clotted/wrong-tube/IV-contaminated รีรันก็ผิดซ้ำ. ต้อง **ดูตัวอย่าง + เจาะใหม่** ไม่ใช่กดรีรัน

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- ค่าผิดปกติ/delta check fail → analytic หรือ pre-analytical? รีรันหรือเจาะใหม่?
- สงสัย hemolysis/icteric/lipemic (HIL) → analyte ไหนพัง? reject หรือ report-with-comment?
- เลือกหลอด/ลำดับเจาะ/อัตราส่วน, จัด timing (fasting/trough/tourniquet), ขนส่ง/เก็บ
- เจอ identity/label ไม่ตรง / historical mismatch → จัดการยังไง

## วิธีใช้
วาง skill นี้ + ค่าที่น่าสงสัย + สภาพตัวอย่าง/ชนิดหลอด/บริบทการเจาะ → AI เดินตาม fork บอก "นี่น่าจะ pre-analytical ตรงไหน + ทำอะไรต่อ" แล้วชี้กลับให้คนตรวจตัวอย่าง/เจาะใหม่ + ทำตาม SOP เอง

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### Fork 1 — Order of draw (กัน additive carryover)
ลำดับ: **blood culture → coag (citrate ฟ้า) → serum/SST (แดง/เหลือง) → heparin (เขียว) → EDTA (ม่วง) → fluoride (เทา)**
- ทำไมสำคัญ: **EDTA carryover → K↑ Ca↓ Mg↑ ปลอม + ALP เพี้ยน**; heparin ปน → coag เพี้ยน
- เจาะหลอดเดียว/winged set → ทิ้ง discard tube ก่อน coag (กัน air/underfill)

### Fork 2 — เลือกหลอด/additive + อัตราส่วน
- **coag = citrate 1:9 เป๊ะ**: underfill → citrate เกิน → **aPTT/PT ยาวปลอม**; **Hct > 55% → ต้องปรับปริมาณ citrate** (plasma น้อย)
- CBC = EDTA; **glucose/lactate = fluoride (NaF)** ยับยั้ง glycolysis — ถ้าใช้ผิดหลอด/ทิ้งนานไม่ปั่น glucose ตก ~5–7%/ชม.
- trace metal/บางฮอร์โมน = หลอดเฉพาะ; ตรวจสอบก่อนเจาะ

### Fork 3 — HIL: hemolysis / icteric / lipemic → analyte ไหนพัง
- **Hemolysis → K↑↑, LDH↑, AST↑, Mg↑, phosphate↑, troponin/บาง immunoassay interfere** (สาร intracellular รั่ว). K จาก hemolyzed = ปลอม **ห้ามรายงานเป็น hyperkalemia** → เจาะใหม่
- สาเหตุ hemolysis: เข็มเล็กเกิน/ดูดแรง, เขย่าหลอด, เจาะจาก line/cannula, ทิ้งนาน/ร้อน-เย็นจัด, แอลกอฮอล์ยังไม่แห้ง
- **Lipemic → Hb/บาง analyte สูงปลอม** (turbidity); **icteric → bilirubin interfere บาง method**
- ตัดสิน reject vs report-with-comment ตาม HIL index + SOP (เชื่อม `clinchem-judgment`)

### Fork 4 — Timing / สรีรวิทยา
- **fasting** (glucose/lipid/iron 8–12 ชม.); **TDM trough/peak** (เจาะผิดเวลา = ตีความยาผิด); **diurnal** (cortisol เช้า, iron เช้า); **posture + tourniquet** ดัน protein/Ca/cholesterol
- **tourniquet < 1 นาที**: รัดนาน → hemoconcentration + **K/lactate leak** + เพี้ยน
- **IV-line contamination**: เจาะเหนือสายน้ำเกลือ → เจือจาง + **glucose/K/Na spike ตามน้ำเกลือ** → เจาะแขนตรงข้าม/ใต้ line + ทิ้ง discard

### Fork 5 — Identification = ข้อที่ "ถึงตาย"
- **wrong-blood-in-tube** = สาเหตุ #1 ของ fatal transfusion error → ใช้ **2 identifiers**, label **ข้างเตียงทันที** (ไม่ใช่ที่เคาน์เตอร์), ห้าม pre-label
- **historical/delta mismatch** (เช่น blood group ไม่ตรงของเดิม) → สงสัย mislabel/sample swap **ก่อน**ตีความ serology (เชื่อม `bloodbank-judgment`)

### Fork 6 — Transport / storage / stability
- **ปั่นแยก serum/plasma ช้า/ไม่แยก** → **K↑ glucose↓** (เซลล์ยัง metabolize); แช่ whole blood เย็น → K รั่วจาก RBC
- **บนน้ำแข็งทันที**: ammonia, lactate, blood gas (บาง analyte); **กันแสง**: bilirubin
- เกินเวลา stability ของแต่ละ analyte → reject/หมายเหตุ; อุณหภูมิขนส่งผิด = ผลเพี้ยนเงียบๆ

## กับดัก (Anti-patterns)
- #1 รีรันหลอดเดิมแทนเจาะใหม่ เมื่อค่าเพี้ยน (กับดัก #1) — clotted/hemolyzed รีรันก็ผิดซ้ำ
- #2 รายงาน K จากตัวอย่าง hemolyzed เป็น hyperkalemia → หมออาจรักษาผิด/ฉุกเฉินปลอม
- #3 ไม่สน order of draw → EDTA carryover ดัน K↑ Ca↓ ปลอม
- #4 coag underfill / ไม่ปรับ citrate ตอน Hct สูง → PT/aPTT ยาวปลอม
- #5 glucose ไม่ใช้ fluoride / ทิ้งนานไม่ปั่น → glucose ต่ำปลอม
- #6 เจาะเหนือ IV line → ค่าเจือจาง + spike ตามน้ำเกลือ
- #7 tourniquet รัดนาน/กำมือย้ำ → K/lactate/hemoconcentration เพี้ยน
- #8 label ที่เคาน์เตอร์/pre-label → wrong-blood-in-tube (ถึงตาย)
- #9 ไม่ปั่นแยก serum/แช่ whole blood เย็น → K↑ glucose↓ เงียบๆ
- #10 ตีความ delta/historical mismatch เป็นเรื่องชีวภาพทันที โดยไม่สงสัย mislabel ก่อน

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - SOP แลบคุณตั้ง HIL-index cutoff / reject criteria / repeat-vs-recollect ไว้อย่างไรต่อ analyte?
> - stability table (เวลา/อุณหภูมิ) ของ analyte ที่แลบคุณเจอปัญหาบ่อย
> - ระบบ 2-identifier + จุดที่เคยเกิด wrong-blood-in-tube ในหน่วยงานคุณ + มาตรการกัน

NOTE: knowledge (รายการ analyte stability เต็ม, สูตรปรับ citrate ตาม Hct, HIL index ของแต่ละเครื่อง) → ดู "ตำรา/แหล่งอ้างอิงมาตรฐาน / CLSI" ไม่ใช่หน้าที่ของ skill นี้

---
*skill นี้เป็นตัวช่วย "คิด" เพื่อการศึกษา ไม่ใช่ตัวตัดสินใจแทน · ตัวอย่างผิด = ผลผิด = รักษาผิด → ทุก reject/accept/แก้ค่า ทำตาม SOP + ยืนยันกับ MT ผู้รับผิดชอบ; การระบุตัวผู้ป่วยผิดเกี่ยวชีวิตโดยตรง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
