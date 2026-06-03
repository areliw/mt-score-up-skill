# DEMO — WI การเตรียม Packed Red Cells (PRC)

> ⚠️ **DEMO ONLY** — ตัวอย่างเพื่อแสดงรูปแบบ output ที่ AI จะ generate
> **ห้ามใช้จริงโดยไม่ verify** กับ manual เครื่อง centrifuge + SOP ของโรงพยาบาลคุณ
> Parameter จริง (rpm, เวลา, hematocrit range) ต้องระบุตาม Standard ของแต่ละสถาบัน

---

## หัวเอกสาร

| รายการ | ค่า |
|---|---|
| ชื่อเอกสาร | Work Instruction: การเตรียม Packed Red Cells (PRC) |
| เลขที่เอกสาร | WI-BB-[TBD] |
| Revision | 0 (draft) |
| วันที่ effective | [DD/MM/YYYY] |
| จำนวนหน้า | [X] |
| ผู้จัดทำ | [ชื่อ-นามสกุล MT] |
| ผู้ตรวจสอบ | [ชื่อ supervisor] |
| ผู้อนุมัติ | [ชื่อ QC manager / หัวหน้าธนาคารเลือด] |

---

## 1. วัตถุประสงค์ (Purpose)

เพื่อกำหนดขั้นตอนมาตรฐานในการเตรียม **Packed Red Cells (PRC)** จาก Whole Blood (WB) ให้ได้ผลิตภัณฑ์ที่มีคุณภาพตามมาตรฐาน AABB และผ่านเกณฑ์ Quality Control ของห้องปฏิบัติการ พร้อมสำหรับการ transfusion ให้ผู้ป่วย

## 2. ขอบเขต (Scope)

ใช้กับ Whole Blood ทุก unit ที่ผ่านการเก็บจาก donor ในธนาคารเลือด ที่จะนำมาเตรียมเป็น PRC สำหรับ allogeneic transfusion

## 3. ความรับผิดชอบ (Responsibility)

| บทบาท | หน้าที่ |
|---|---|
| MT operator | ปฏิบัติตาม WI · ตรวจสอบคุณภาพแต่ละขั้นตอน · บันทึกในแบบฟอร์ม |
| Supervisor | ตรวจสอบความถูกต้อง · approve การ release product |
| QC manager | review บันทึก QC รายเดือน · จัดการเมื่อ QC out of range |
| Technical staff | maintenance เครื่อง centrifuge + plasma extractor |

## 4. คำจำกัดความ (Definitions)

- **Whole Blood (WB)** — เลือดที่เก็บจาก donor ในถุง CPDA-1 หรือ CPD/SAGM (volume 450 ± 45 mL)
- **Packed Red Cells (PRC)** — เลือดที่แยก plasma ออก, hematocrit สูง 65-75% (CPDA-1) หรือ 50-70% (SAGM)
- **Heavy spin** — การปั่นแยกที่ความเร็วสูงเพื่อแยก cell components สมบูรณ์
- **Closed system** — การเตรียมใน sterile tubing ไม่เปิดถุง

## 5. วัสดุ อุปกรณ์ และน้ำยา (Materials, Equipment, Reagents)

### อุปกรณ์
- Refrigerated centrifuge (เช่น Sorvall RC-3BP+ หรือเทียบเท่า) — calibrated, last QC date ระบุ
- Plasma extractor (Manual / Automated)
- Tube sealer
- Balance scale (±1 g accuracy)
- Refrigerator 2-6°C with continuous temperature monitoring

### วัสดุสิ้นเปลือง
- Triple bag system (CPDA-1 หรือ CPD/SAGM ตาม inventory)
- Sample tubes สำหรับ QC test (Hematocrit)
- Label สำหรับ product (barcode-compatible)

### PPE
- Lab coat · gloves · safety glasses · closed-toe shoes

## 6. ขั้นตอนการปฏิบัติ (Procedure)

### 6.1 การเตรียมก่อนปั่น

1. **ตรวจสอบ WB unit:**
   - Donor ID ตรงกับ label
   - Volume อยู่ในช่วง 405-495 mL
   - ไม่มี clot, hemolysis, หรือ contamination
   - Expiry date ยังไม่หมด
2. **บันทึก unit ID** ลงในแบบฟอร์ม PRC preparation log
3. **Balance bags** — จัด unit คู่ที่มี weight ใกล้กัน (Δ ≤ 5 g) ใน centrifuge bucket ตรงข้าม

### 6.2 การปั่นแยก (Centrifugation)

4. **โหลด centrifuge** — วาง unit ใน bucket, ปิดฝา
5. **ตั้งค่า:**
   - Speed: **[ระบุตาม manual เครื่อง — โดยทั่วไป 3,500-5,000 rpm สำหรับ heavy spin]**
   - Time: **[ระบุตาม manual — โดยทั่วไป 7-10 นาที]**
   - Temperature: **4°C ± 2°C**
6. **เริ่มปั่น** — ห้ามเปิดฝาระหว่างปั่น
7. **หลังปั่นเสร็จ** — รอ rotor หยุดสมบูรณ์ก่อนเปิดฝา
8. **ตรวจสอบ unit:**
   - ⚠️ Hemolysis (สีแดงใน plasma layer) → discard unit
   - ⚠️ Bag เสียหาย → discard unit
   - การแบ่ง layer ชัดเจน → ผ่าน

### 6.3 การแยก Plasma

9. **ย้าย unit ไป plasma extractor** ด้วยความระมัดระวัง (อย่าให้ layer ผสม)
10. **เปิด clamp** ของ satellite bag, ปล่อย plasma ไหลเข้า
11. **หยุดเมื่อ:**
    - Plasma layer ใกล้หมด (เหลือ buffy coat บาง ๆ)
    - หรือ volume ตามเป้าหมาย (ดู section 6.4)
12. **Seal tubing** ด้วย tube sealer 2 ตำแหน่ง
13. **ตัดแยก** PRC bag กับ plasma bag

### 6.4 การควบคุม volume

14. **ชั่ง PRC bag:**
    - Target volume: 250-300 mL (ขึ้นกับ starting WB volume)
    - ถ้า > 300 mL → ปล่อย plasma เพิ่ม
    - ถ้า < 200 mL → consult supervisor (อาจ split unit ผิดพลาด)

### 6.5 การ label และเก็บ

15. **Label PRC bag** ระบุ:
    - Product type: "Packed Red Cells"
    - Unit ID
    - Blood group + Rh
    - Collection date + expiry date (35 วันสำหรับ CPDA-1, 42 วันสำหรับ SAGM)
    - Volume
16. **เก็บ PRC** ที่ refrigerator 2-6°C — บันทึก time-in
17. **Plasma bag** → freeze ที่ ≤-18°C ภายใน 8 ชั่วโมง (สำหรับ FFP) หรือเก็บที่ 2-6°C (สำหรับ FP)
18. **บันทึก** การเตรียมในแบบฟอร์ม + ระบบ LIS

## 7. การควบคุมคุณภาพ (Quality Control)

| Parameter | Acceptance criteria | Frequency | Action ถ้า fail |
|---|---|---|---|
| Volume | 250-300 mL (CPDA-1) / 250-350 mL (SAGM) | ทุก unit | discard หรือ adjust |
| Hematocrit | 65-75% (CPDA-1) / 50-70% (SAGM) | 4 units/เดือน random sampling | review centrifuge speed/time |
| Hemolysis | < 0.8% ของ red cell mass ใน last day of expiry *(ค่า illustrative — ทวนกับ AABB Standards ฉบับจริง)* | 1 unit/เดือน | review storage temp + handling |
| Sterility | ไม่พบเชื้อใน 10% ของ products at expiry *(ค่า illustrative — ทวนกับ AABB Standards ฉบับจริง)* | quarterly | re-train staff + review SOP |
| Storage temp | 2-6°C continuous | 24/7 monitoring | corrective action ตาม WI-BB-temp |

## 8. การคิดคำนวณ / การแปลผล

ไม่มี calculation specific สำหรับ WI นี้ — ตรวจสอบ volume ด้วย scale โดยตรง

## 9. การบันทึก (Records)

| บันทึก | เก็บที่ | ระยะเวลา |
|---|---|---|
| PRC preparation log | ธนาคารเลือด, binder ปีปัจจุบัน | 10 ปี (per AABB) |
| QC monthly summary | QC manager | 10 ปี |
| Equipment maintenance log | technical staff | ตลอดอายุเครื่อง |
| Temperature monitoring | refrigerator log | 1 ปี (digital backup ตลอด) |

## 10. เอกสารอ้างอิง (References)

- AABB Technical Manual, 21st edition (2023) — Component Preparation section
- ISO 15189:2022 — หัวข้อ Quality control (ทวนเลข clause กับฉบับจริงที่แล็บถือ)
- ISO 15190:2020 — หัวข้อ biological hazards / PPE / waste management (ทวนเลข clause กับฉบับจริง)
- Manual เครื่อง centrifuge: [ระบุยี่ห้อ/รุ่น/version]
- SOP-BB-001 — General Blood Bank Operations
- WI-BB-002 — Temperature Monitoring of Blood Storage Refrigerators

## 11. ประวัติการแก้ไข (Revision History)

| Rev | Date | Description | Author |
|---|---|---|---|
| 0 | [date] | Initial draft (AI-assisted via mt-score-up-skill) — **NEEDS LAB REVIEW** | [MT name] |

---

## 📝 หมายเหตุสำหรับผู้ใช้ DEMO นี้

1. **ทุก parameter ที่ระบุในวงเล็บ `[...]`** = ต้องกรอกตาม standard/manual ของห้องปฏิบัติการคุณ
2. **Hematocrit range + spin parameter** = ขึ้นกับยี่ห้อ centrifuge + bag system → consult manual
3. **ต้องผ่าน QC manager review** ก่อน implement ใน production
4. **เปรียบเทียบกับ SOP เดิม** ของโรงพยาบาล — ถ้ามี discrepancy ให้ priority SOP เดิม
