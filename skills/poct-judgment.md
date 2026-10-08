---
skill: poct-judgment
title: โค้ช POCT — แล็บนอกแล็บต้องเชื่อได้เท่าแล็บกลาง (Point-of-Care Testing Judgment)
type: ADVISE               # ช่วยตัดสินใจการใช้/คุม POCT ไม่ใช่คู่มือเครื่อง
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-10-08
status: draft
disclaimer: "ช่วยคิดการใช้/กำกับ POCT เพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ตัดสินใจแทน · ผล POCT ที่กระทบการรักษาต้องผ่าน QC + operator competency + ทำตาม SOP/ISO 15189; ค่าวิกฤตแจ้ง/ยืนยันตาม policy · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช POCT (Point-of-Care Testing)

ตัวช่วยตัดสินใจตอน MT ดูแล/ใช้ POCT (glucose meter, blood gas, i-STAT, rapid test, HbA1c POC) นอกแล็บกลาง — เน้น "เมื่อไหร่ใช้ + คุมยังไงให้เชื่อได้ + limitation" ไม่ใช่คู่มือเครื่อง

> **กฎ #1:** POCT = **แล็บที่ทำนอกแล็บ** → ต้องมี **QC + operator competency + connectivity** เหมือนแล็บกลาง (ISO 15189:2022 รวม POCT เข้ามาแล้ว) ไม่ใช่ "เครื่องง่ายๆ ใครก็กดได้"
> **กับดัก #1 (ขั้น hard):** ผล POCT ที่ **ไม่ผ่าน QC / operator ไม่ผ่าน competency = ค่าที่เชื่อไม่ได้** แต่ถูกเอาไปรักษาทันที (ER/ICU). ค่าวิกฤตจาก POCT ต้องแจ้ง/พิจารณา confirm เหมือนแล็บกลาง

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยัน

## เครื่องมือ (รันก่อนคิดเลข)
จะใช้ผล POCT ตัวไหน หรือเทียบ POCT กับแล็บกลาง → **รันสคริปต์ก่อน แล้วค่อยใช้ fork ข้างล่างตีความ** (อย่าไล่ gate ด้วยความจำ) · รัน `--help` ก่อน ไม่ต้องอ่านซอร์ส · ไฟล์อยู่ใน `scripts/` ของโฟลเดอร์ skill (ใน repo: `skills/poct-judgment/scripts/`)
- `python scripts/poct_gate.py --value 45 --qc pass --operator-competent --lot-verified --range <ช่วงวัดของเครื่อง> --critical <ค่าวิกฤตตาม policy> --method gdh-pqq --interferent icodextrin --hct 65 --hct-range <ช่วง Hct ของเครื่อง>` → finding เรียงระดับ `BLOCK` / `CONFIRM` / `NOTIFY` / `CAUTION` + บรรทัด `STATUS` · ไล่ gate: QC, competency (+ วันหมดอายุด้วย `--competency-date --competency-interval-days`), lot verify, นอกช่วงวัด, **ทิศ Hct** (สูง → ต่ำปลอม / ต่ำ → สูงปลอม), GDH-PQQ + maltose/icodextrin/galactose, GOx + O₂/arterial, capillary ใน shock/บวม/vasopressor, จดมือ, ค่าวิกฤต · ทุกช่วง/ค่าวิกฤต = ของผู้ผลิต/policy ที่ต้องใส่เอง ไม่มีค่าฝังในสคริปต์
- `python scripts/poct_compare.py data/poct_pairs_teaching_example.csv --limit-pct <เกณฑ์ยอมรับของ policy> [--limit-abs --switch-at] --drift-pct 5` → ตาราง diff/% ต่อคู่ (แล็บกลางเป็นตัวเทียบ), mean bias, % คู่ที่ผ่านเกณฑ์ และ **drift ครึ่งแรก vs ครึ่งหลัง** (ไฟล์ตัวอย่าง = ค่าสอน: ผ่านเกณฑ์ทุกคู่แต่ยังไหล — กับดัก #7) · `--meter-cal whole-blood` เตือนว่า plasma สูงกว่า whole blood ~12–15% = matrix ไม่ใช่ error
- สคริปต์ = ตัวช่วยตรวจ ไม่ใช่ผู้ตัดสิน: ทุก output มีบรรทัด `ADVISORY` · ทดสอบแล้ว: `evals/test_poct_tools.py` (16 ข้อ รวม must-fail control 2 ตัว: gate ที่ไม่ดู QC และทิศ Hct กลับด้าน — ต้องแดง)

## ใช้เมื่อ
- ตัดสินใจว่างานนี้ควรใช้ POCT หรือส่งแล็บกลาง
- วางระบบ QC/competency/connectivity สำหรับ POCT ในหน่วยงาน
- เจอผล POCT ที่ขัดอาการ/ขัดแล็บกลาง → เชื่อตัวไหน

## วิธีใช้
วาง skill นี้ + บริบท (เทสต์อะไร/ที่ไหน/ใครทำ/เร่งแค่ไหน) → AI ช่วยชั่ง POCT vs แล็บกลาง + เตือน QC/competency/limitation แล้วชี้ให้ทำตาม SOP + ยืนยันเอง

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### Fork 1 — ควรใช้ POCT ไหม
- **ใช่**: TAT เป็นเรื่องชีวิต (ER/ICU/OR/ห่างแล็บ), ปริมาณน้อย-ต้องเร็ว
- **ส่งแล็บกลางดีกว่า**: ต้องการความแม่นสูง, ปริมาณมาก (ถูกกว่าต่อเทสต์), มี QC/validation เต็ม
- ไม่ใช่ทุกอย่างควร POCT เพราะ "เร็ว"

### Fork 2 — QC + operator competency
- QC ตามรอบ/ตาม manufacturer + ระบบบันทึก · **operator ต้อง train + competency assessment เป็นระยะ** · lot verification เมื่อเปลี่ยน lot · **เข้าร่วม EQA/PT** (หรือ alternative assessment ถ้าไม่มี scheme — ISO 15189:2022 Annex A) (เชื่อม `lab-management-judgment`, `clinchem-judgment`)

### Fork 3 — limitation ของ POCT (รู้ก่อนเชื่อ)
- **interference (glucose meter — landmine จริง):** **Hct สูง → glucose ต่ำปลอม / Hct ต่ำ (เด็ก/anemia/dialysis) → สูงปลอม** · **O₂ สูงรบกวนเฉพาะ glucose-oxidase** (ได้ O₂/arterial sample → ต่ำปลอม; GDH ไม่ไว O₂) · ⚠️ **GDH-PQQ meter โดน maltose/icodextrin (น้ำยา PD)/galactose → สูงปลอมรุนแรง** (FDA boxed warning — เคยให้ insulin เกินจนตาย) · acetaminophen/vit C/uric acid รบกวน amperometric · linear range แคบ
- ⚠️ **capillary glucose เชื่อไม่ได้ใน shock/ความดันตก/บวม/vasopressor** (perfusion แย่) → ใช้ venous/blood-gas analyzer
- correlate POCT กับแล็บกลางเป็นระยะ; ค่าขัดอาการ/ขัดแล็บกลาง → ตรวจซ้ำ/ส่งแล็บกลาง

### Fork 4 — connectivity + บันทึก
- ผลต้องเข้า **LIS/บันทึกได้ + traceable** (ไม่ใช่จดมือแล้วหาย) → audit + ความต่อเนื่องการดูแล

### Fork 5 — critical value + confirm
- ค่าวิกฤตจาก POCT → **แจ้งตาม policy** + พิจารณา confirm แล็บกลาง (เชื่อม `clinical-correlation-judgment`)

## กับดัก (Anti-patterns)
- #1 ถือว่า POCT ไม่ต้อง QC / operator ไม่ต้อง competency (กับดัก #1)
- #2 ลืม interference glucose meter (ทิศ Hct · GDH-PQQ+maltose/PD-fluid · capillary ใน shock) → ค่าเพี้ยนในคนไข้ ICU/ป่วยหนัก → insulin ผิด
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
