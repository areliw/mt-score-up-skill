---
skill: lab-management-judgment
title: โค้ชบริหารแล็บ — QMS/accreditation/QC strategy/งบ (Lab Management Judgment)
type: ADVISE               # ช่วยตัดสินใจบริหารแล็บ ไม่ใช่ตำรา ISO
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดบริหารแล็บเพื่อการศึกษา ไม่ใช่ที่ปรึกษา accreditation/จัดซื้อ/กฎหมายทางการ — ข้อกำหนด ISO/มาตรฐานจริงต้องอ้างฉบับล่าสุด + ผู้ตรวจประเมิน/ผู้มีอำนาจของหน่วยงาน · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชบริหารแล็บ — QMS / accreditation / QC strategy / งบ

ตัดสินใจระดับ "บริหารแล็บ" — เลือก accreditation ไหน · วางแผน QC ให้ประหยัด · สั่งน้ำยายังไง · ของบเครื่องลงช่องไหน · verify เครื่องใหม่ ไม่ใช่ท่องข้อกำหนด ISO (= commodity ดูมาตรฐานตัวจริง)

> **กฎ #1: ตั้ง QC limit จาก mean/SD ที่แล็บคำนวณเอง — ห้ามใช้ค่าจากกล่องน้ำยา/insert (นั่นคือ peer range ไม่ใช่ performance เครื่องคุณ → limit หลวม จับ error ไม่ได้).**
> **กับดักขั้นกว่า (จุดที่พลาดจริง): "ใช้ค่าแล็บเอง" ยังไม่พอ — ต้องเก็บ ≥20 จุด คนละวัน ≥20 วัน. เก็บ 20 จุดรวดเดียววันเดียว = ได้แค่ within-run SD (แคบเกิน) → false reject ท่วม. และพอ "เปลี่ยน lot control/น้ำยา" ต้องตั้ง mean/SD ใหม่ ห้าม carry ค่าเก่าข้าม lot.**
> นี่คือชั้น "วางระบบ/วางแผน" เหนือหน้า bench — QC accept/reject รายวันดู `clinchem-judgment`; skill นี้คือ **ออกแบบ QC ทั้งระบบ + ผ่าน audit + คุมต้นทุน**
> กรอบร้อยทุกอย่าง = **Total Testing Process: Pre → Analytical → Post** (~46–68% error อยู่ที่ pre-analytical, มัก quote ~60%; Plebani)

## ใช้เมื่อ
- เตรียม/ต่ออายุ accreditation (ISO 15189 / LA / HA) — เลือกระดับ + เตรียมเอกสาร
- QC แพง/รันซ้ำเปลือง → วางแผน QC ตาม sigma/IQCP
- สั่งน้ำยา-คุมสต็อก · ของบเครื่อง/น้ำยา · รับเครื่องใหม่ (verification) · จัดการความเสี่ยง/TAT

## วิธีใช้
วาง skill นี้ + เล่าสถานการณ์ (กำลัง accredit / QC เปลือง / จะซื้อเครื่อง) → AI ชี้ทางเลือก + กับดักบริหาร

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — เลือก accreditation ระดับไหน
- **งบจำกัด/เริ่มต้น** → มาตรฐานงานเทคนิคการแพทย์ (ไทย) ก่อน
- **ต้องการ recognition สากล / รับงานนอก / วิจัย** → **ISO 15189** (เฉพาะ medical lab; ต่างจาก 17025 lab ทั่วไป / 9001 องค์กรทั่วไป)
- **ยกระดับทั้ง รพ.** → HA (รพ.) + LA (แล็บ) ไปด้วยกัน
- 15189 = Management requirements (QMS/document control/CAPA/internal audit/management review) + Technical (บุคลากร/เครื่อง-น้ำยา/pre-exam-post/รายงานผล/LIS) · ความปลอดภัยใช้ **ISO 15190** คู่

### Fork 2 — IQC vs EQA: คุมคนละอย่าง อย่าสับ
- **IQC** (control ทุกวันก่อนตรวจคนไข้) คุม **precision** → ดู %CV, Levey-Jennings · ⚠️ ตั้ง limit ตามกฎ #1 (mean/SD แล็บเอง, CLSI C24)
- **EQA/PT** (ส่งเทียบ peer) คุม **accuracy** → ได้ **bias** = (mean lab − mean peer)/mean peer ×100
- กับดัก: **IQC ผ่านสวยแต่ inaccurate ได้** (bias คงที่ L-J จับไม่ได้ — ต้องพึ่ง EQA)

### Fork 3 — Sigma-based QC planning (จุดประหยัดจริง)
```
Sigma = [TEa(%) − Bias(%)] / CV(%)   ← ทั้ง 3 ตัวต้องหน่วยเดียวกัน (% หรือ conc.)
```
ยิ่ง sigma สูง = method ดี = **คุม QC น้อยลงได้ = ประหยัด control/แรง/เวลา**
| Sigma | QC ที่พอ |
|---|---|
| **6** | 1₃s, N=2 (เกือบไม่ต้องคุมหนัก) |
| **5** | + 2of3₂s, R₄s |
| **4** | + 4₁s |
| **<4** | ทุกกฎ + N=6 (เปลือง = สัญญาณ method แย่ → ปรับปรุง/เปลี่ยน) |
- **IQCP** (Individualized QC Plan, CLSI EP23): วาง QC ตามความเสี่ยงจริงของ 5 จุด — **Specimen / Operator / Reagent / Environment / Measuring system** → ลด QC ได้อย่างมีหลักฐาน

### Fork 4 — error อยู่ phase ไหน → ลงทุนแก้ตรงนั้น
- **Pre (~46–68% มัก quote ~60%; Plebani)** หลอดผิด/สัดส่วนเลือด-สารกันแข็ง/hemolysis/label ผิด → คุมด้วยระบบ/automation/barcode (คุ้มสุด)
- **Analytical** calibration drift/lot เสื่อม/อุณหภูมิ → MT + QC
- **Post** พิมพ์ผิด/ไม่แจ้ง critical/TAT เกิน → LIS auto-verify
> อย่าทุ่มแก้ analytical ทั้งที่ปัญหาจริงอยู่ pre-analytical

### Fork 5 — สั่งน้ำยา/คุมสต็อก
- ปัจจัย: consumption rate · **packing size** (กล่องใหญ่ถูก/เทสต์ แต่หมดอายุก่อนใช้หมด = เสียเปล่า) · expiry + **FEFO** · พื้นที่เก็บ controlled
- **fork:** สั่งมาก (ส่วนลด แต่เสี่ยงหมดอายุ + แช่เงินทุน) vs สั่งบ่อย (สดเสมอ แต่เสี่ยงขาด + ค่าขนส่ง) → ขึ้นกับ stability น้ำยา + ความแน่นอน demand

### Fork 6 — ของบ: เครื่อง vs น้ำยา คนละกระเป๋า
- **เครื่อง = งบลงทุน (capital)** → อนุมัติยาก รอบยาว ผ่านกรรมการ จัดซื้อภาครัฐ (TOR/e-bidding)
- **น้ำยา = งบดำเนินงาน (operating)** → คล่อง อนุมัติเร็ว
- ⚠️ เสนอผิดกระเป๋า = ลูกค้า/ผู้บริหารอนุมัติไม่ได้ → ดู `ivd-sales-judgment` สำหรับ reagent rental ที่ย้าย capex→opex

### Fork 7 — รับเครื่อง/method ใหม่: Verification ≠ Validation
- **Validation** = ผู้ผลิตพิสูจน์แล้วว่า method ใช้ได้ · **Verification** = **แล็บทวนสอบเองก่อนใช้จริง** ว่าได้ตามที่อ้างในสภาพแล็บตน (ISO 15189 บังคับ) — precision/accuracy/linearity/reportable range
- เครื่องใหม่ / method ใหม่ / เปลี่ยน lot ใหญ่ → re-verify

### Fork 8 — Risk management + LIS/TAT
- ระบุความเสี่ยง → ประเมิน **Likelihood × Impact** → จัดลำดับ → จัดการ: **ยอมรับ / ลด-คุม / โอน (ประกัน-outsource) / เลี่ยง** → ทบทวน
- **LIS/LIMS** (ISO บังคับ): สิทธิ์เข้าถึง, ใคร approve, กันแก้-สูญหาย, **audit trail**, ความลับคนไข้ (PDPA)
- **TAT** = KPI ที่ ward/แพทย์กดดันสุด → automation/STAT pathway ลด TAT

---

## กับดัก (Anti-patterns)
- ละเมิดกฎ #1: ใช้ค่าจากกล่องน้ำยา · เก็บ 20 จุดวันเดียว (SD แคบ → false reject) · carry mean/SD ข้าม lot
- **2SD กับทุก test** → false reject ท่วม รันซ้ำเปลืองเงิน (สับ warning 1₂s กับ reject)
- **QC out → รันซ้ำจนผ่าน** โดยไม่หา root cause → ปล่อย systematic error หลุด
- **EQA fail = โทษเครื่องทันที** → อาจ pre-analytical / ลงค่าผิด / lot
- **สั่งล็อตใหญ่เพราะถูก/หน่วย** → หมดอายุก่อนใช้ + แช่เงินทุน
- **มอง pre-analytical ว่าไม่ใช่ปัญหาแล็บ** ทั้งที่เป็น error อันดับ 1
- **สับ verification กับ validation** → รับเครื่องโดยไม่ทวนสอบเองก่อนใช้

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT หัวหน้าแล็บ) ตอนเตรียม ISO 15189 จุดที่ผู้ตรวจจับบ่อยคือ... เตรียมโดย..."*
> - *"sigma ของ analyte ... ในแล็บผม = ... เลยตั้ง QC เป็น..."*
> - *"กับดักสั่งน้ำยา/สต็อกที่ผมเคยพลาด คือ..."*

---
*ช่วยคิดบริหารแล็บเพื่อการศึกษา ไม่ใช่ที่ปรึกษา accreditation/จัดซื้อ/กฎหมายทางการ — ข้อกำหนด ISO/มาตรฐานจริงต้องอ้างฉบับล่าสุด + ผู้ตรวจประเมิน/ผู้มีอำนาจของหน่วยงาน · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
