---
skill: poct-judgment
title: โค้ช POCT — แล็บนอกแล็บต้องเชื่อได้เท่าแล็บกลาง (Point-of-Care Testing Judgment)
type: ADVISE               # ช่วยตัดสินใจการใช้/คุม POCT ไม่ใช่คู่มือเครื่อง
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-08
status: draft
disclaimer: "ช่วยคิดการใช้/กำกับ POCT เพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ตัดสินใจแทน · ผล POCT ที่กระทบการรักษาต้องผ่าน QC + operator competency + ทำตาม SOP/ISO 15189; ค่าวิกฤตแจ้ง/ยืนยันตาม policy · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช POCT (Point-of-Care Testing)

ตัวช่วยตัดสินใจตอน MT ดูแล/ใช้ POCT (glucose meter, blood gas, i-STAT, rapid test, HbA1c POC) นอกแล็บกลาง — เน้น "เมื่อไหร่ใช้ + คุมยังไงให้เชื่อได้ + limitation" ไม่ใช่คู่มือเครื่อง

> **กฎ #1:** POCT = **แล็บที่ทำนอกแล็บ** → ต้องมี **QC + operator competency + connectivity** เหมือนแล็บกลาง (ISO 15189:2022 รวม POCT เข้ามาแล้ว) ไม่ใช่ "เครื่องง่ายๆ ใครก็กดได้"
> **กับดัก #1 (ขั้น hard):** ผล POCT ที่ **ไม่ผ่าน QC / operator ไม่ผ่าน competency = ค่าที่เชื่อไม่ได้** แต่ถูกเอาไปรักษาทันที (ER/ICU). ค่าวิกฤตจาก POCT ต้องแจ้ง/พิจารณา confirm เหมือนแล็บกลาง

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยัน

## ใช้เมื่อ
- ตัดสินใจว่างานนี้ควรใช้ POCT หรือส่งแล็บกลาง
- วางระบบ QC/competency/connectivity สำหรับ POCT ในหน่วยงาน
- เจอผล POCT ที่ขัดอาการ/ขัดแล็บกลาง → เชื่อตัวไหน

## วิธีใช้
วาง skill นี้ + บริบท (เทสต์อะไร/ที่ไหน/ใครทำ/เร่งแค่ไหน) → AI ช่วยชั่ง POCT vs แล็บกลาง + เตือน QC/competency/limitation แล้วชี้ให้ทำตาม SOP + ยืนยันเอง

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### Fork 1 — ควรใช้ POCT ไหม
- **ใช่**: TAT เป็นเรื่องเป็นเรื่องชีวิต (ER/ICU/OR/ห่างแล็บ), ปริมาณน้อย-ต้องเร็ว
- **ส่งแล็บกลางดีกว่า**: ต้องการความแม่นสูง, ปริมาณมาก (ถูกกว่าต่อเทสต์), มี QC/validation เต็ม
- ไม่ใช่ทุกอย่างควร POCT เพราะ "เร็ว"

### Fork 2 — QC + operator competency
- QC ตามรอบ/ตาม manufacturer + ระบบบันทึก · **operator ต้อง train + competency assessment เป็นระยะ** · lot verification เมื่อเปลี่ยน lot (เชื่อม `lab-management-judgment`, `clinchem-judgment`)

### Fork 3 — limitation ของ POCT (รู้ก่อนเชื่อ)
- **interference**: Hct + oxygen + สารรบกวน ใน glucose meter; linear range แคบ; แม่นน้อยกว่าแล็บกลาง
- correlate POCT กับแล็บกลางเป็นระยะ; ค่าขัดอาการ/ขัดแล็บกลาง → ตรวจซ้ำ/ส่งแล็บกลาง

### Fork 4 — connectivity + บันทึก
- ผลต้องเข้า **LIS/บันทึกได้ + traceable** (ไม่ใช่จดมือแล้วหาย) → audit + ความต่อเนื่องการดูแล

### Fork 5 — critical value + confirm
- ค่าวิกฤตจาก POCT → **แจ้งตาม policy** + พิจารณา confirm แล็บกลาง (เชื่อม `clinical-correlation-judgment`)

## กับดัก (Anti-patterns)
- #1 ถือว่า POCT ไม่ต้อง QC / operator ไม่ต้อง competency (กับดัก #1)
- #2 ลืม interference (Hct/oxygen ใน glucose meter) → ค่าเพี้ยนในคนไข้ป่วยหนัก
- #3 ใช้นอก linear range → ค่าผิด
- #4 ผล POCT ไม่เข้าระบบ/จดมือหาย → ไม่ traceable
- #5 ไม่ confirm/ไม่แจ้งค่าวิกฤตจาก POCT
- #6 ใช้ POCT แทนแล็บกลางทุกอย่างเพราะเร็ว (ละเลยความแม่น/ต้นทุน)
- #7 ไม่ correlate POCT กับแล็บกลางเป็นระยะ → drift ไม่รู้ตัว
- #8 lot ใหม่ไม่ verify

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - รายการ POCT ที่หน่วยงานคุณใช้ + ใครเป็น operator + ระบบ QC/competency ปัจจุบัน
> - policy ค่าวิกฤต + การ confirm แล็บกลางของ รพ.คุณ
> - interference/limitation ของเครื่อง POCT รุ่นที่ใช้ที่ทีมต้องระวัง

NOTE: QC/Westgard เชิงลึก → `clinchem-judgment`; ระบบ QMS/competency → `lab-management-judgment`; คู่มือเครื่องเฉพาะรุ่น → manufacturer

---
*skill นี้ช่วย "คิด" เพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์ · ผล POCT ที่กระทบการรักษาต้องผ่าน QC + competency + SOP; ค่าวิกฤตแจ้ง/ยืนยันตาม policy · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
