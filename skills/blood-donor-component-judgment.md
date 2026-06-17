---
skill: blood-donor-component-judgment
title: ฝั่งผู้บริจาค/ผลิตเลือด — eligibility · apheresis · component QC · hemovigilance (Blood Donor & Component Judgment)
type: ADVISE               # ช่วยตัดสินใจฝั่ง donor/collection/ผลิต/QC ไม่ใช่ตำราเกณฑ์/วินิจฉัยแทน
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-16
status: draft
disclaimer: "เพื่อการศึกษา/ช่วยทบทวน ไม่ใช่คำสั่งทางการแพทย์หรือผู้ตัดสินใจแทน — งานบริการโลหิตเกี่ยวกับชีวิตทั้งผู้บริจาคและผู้รับโดยตรง ต้องทำตาม SOP ของหน่วยงาน + วิจารณญาณ MT/แพทย์ผู้มีใบประกอบฯ และยึด มาตรฐานธนาคารเลือดและงานบริการโลหิต ศูนย์บริการโลหิตแห่งชาติ สภากาชาดไทย (AABB/ISBT/FDA = อ้างอิงสากล) เสมอ · **ตัวเลขทุกตัวในสกิล (Hb/น้ำหนัก/อายุ/ระยะห่าง/อุณหภูมิ/อายุเก็บ/เกณฑ์ QC/dose) = teaching illustration ต่างกันตามมาตรฐาน/ชนิด anticoagulant/ประชากร/edition — verify กับ SOP จริงทุกครั้ง** · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ฝั่งผู้บริจาค/ผลิตเลือด — eligibility · apheresis · component QC · hemovigilance

ฝั่ง **ก่อน**เลือดถึงคนไข้ — รับบริจาค → เก็บ → ผลิต component → QC → จ่ายเข้า stock → ตามรอย. ผิดตรงนี้ = ส่งหน่วยที่ไม่ปลอดภัย/ด้อยคุณภาพออกไปทั้ง batch (ไม่ใช่แค่ unit เดียว) และกระทบ **donor safety** ด้วย. สกิลนี้ช่วยตัดสิน: **รับ/defer · whole blood vs apheresis · ทำ component ไหนได้ · QC ผ่าน/fail/quarantine · เก็บ/คืน stock · TTI reactive ทำไง · recall/look-back เมื่อไหร่**

> **ขอบเขต (อ่านก่อน):** สกิลนี้ = ฝั่ง **donor / collection / manufacturing / QC / donor-hemovigilance** (งานศูนย์บริการโลหิต/หน่วยรับบริจาค). ฝั่ง **ผู้รับ/เข้ากันได้** — ABO discrepancy resolve · antibody ID · crossmatch · transfusion reaction ผู้รับ · HDN · เลือก component ให้คนไข้รายนั้น — อยู่ที่ **`bloodbank-judgment`** (อย่าตอบข้ามฝั่ง). จุดต่อ: unit ผ่าน QC+TTI ที่นี่ → ไปเข้า compatibility ที่ `bloodbank-judgment`

> **กฎ #1:** **defer ปกป้อง 2 ทางเสมอ** — donor (สุขภาพคนให้) + recipient (ความปลอดภัยเลือด). "เสียดาย unit / ขาดเลือด" แล้วฝืนรับคนที่เข้าเกณฑ์ defer = เสี่ยงทั้งคู่ — ตัวเลข/เกณฑ์ยึด SOP+มาตรฐานกาชาด ไม่ใช่ดุลพินิจหน้างานลดเอง
> **กับดัก #1:** **screen-reactive TTI ≠ ติดเชื้อยืนยัน** — *unit* ห้ามจ่าย → quarantine ทันที (discard ตอน disposition) แต่ *donor* ห้ามแจ้งว่า "ติดเชื้อ" ก่อน confirmatory (false-positive มีจริง → กระทบจิตใจ/ตีตรา) · กลับกัน **screen-negative ≠ ปลอดภัย 100%** — window period ยังเหลือแม้มี NAT → donor honesty/self-exclusion ยังจำเป็น
> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริง/เกณฑ์ตัวเลขก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบ donor/ผู้รับ = MT อาวุโส/แพทย์/ศูนย์บริการโลหิตยืนยันก่อนลงมือ
>
> 🇹🇭 **มาตรฐานอ้างอิง (ไทย):** ยึด **มาตรฐานธนาคารเลือดและงานบริการโลหิต — ศูนย์บริการโลหิตแห่งชาติ สภากาชาดไทย** เป็นหลัก (AABB/ISBT/EU/FDA = อ้างอิงสากล, เกณฑ์ต่างกัน — อ้าง edition ที่ใช้จริง) · "ref lab / NAT lab / ศูนย์อ้างอิง" = ศูนย์บริการโลหิตแห่งชาติ สภากาชาดไทย
> ⚠️ **logic เน้นผู้ใหญ่/ผู้บริจาคทั่วไป** — autologous · directed · neonatal/intrauterine component · apheresis ในเด็ก = ยึด protocol เฉพาะ + ปรึกษาแพทย์

> 🛑 **RED FLAGS — เจอข้อใด = หยุด ยืนยันกับแพทย์/MT อาวุโส/ศูนย์บริการโลหิตก่อน อย่าเชื่อ AI เดี่ยว:** TTI confirmed-positive → แจ้ง/counsel donor · **look-back / recall** หน่วยที่อาจ transfuse ไปแล้ว · apheresis citrate reaction รุนแรง (tetany/arrhythmia) · donor reaction รุนแรง/หมดสติ/ชัก · **hematoma โตเร็ว/ปวดรุนแรง/ชา-อ่อนแรง/มือซีดเย็น** (สงสัยโดนเส้นเลือดแดง-เส้นประสาท) · **granulocyte** collection/component (donor ต้องกระตุ้นยา + protocol เฉพาะ) · component สำหรับทารก/intrauterine/exchange · สงสัย **bacterial contamination** ของ platelet — กลุ่มนี้กระทบชีวิตจริง ต้องมีคนยืนยันเสมอ

## ใช้เมื่อ
- donor มา → **รับ / defer ชั่วคราว / defer ถาวร / ส่งต่อ** (Hb/vitals/ประวัติ/ระยะห่าง)
- เลือก **whole blood vs apheresis** (platelet/plasma/double-RBC/granulocyte) + จัดการ citrate/ECV
- **donor reaction** (vasovagal/hematoma/citrate/delayed faint) → จัดการ + กันซ้ำ
- whole blood unit → **ทำ component ไหนได้** ตามเวลา/ระบบ (timing window)
- **QC component** ผ่าน/fail → ทิ้ง unit หรือ quarantine ทั้ง batch?
- เก็บรักษา/ขนส่ง · **unit คืนมา รับกลับ stock ได้ไหม** (30-min/temp)
- **TTI reactive** → unit/donor ทำไง · **post-donation info / look-back / recall**

## วิธีใช้
วาง skill นี้ + เล่าสถานการณ์ (donor profile/ค่าที่วัด/ชนิดบริจาค/component/ผล QC/ผล TTI/เวลาที่ผ่าน) → AI ช่วยชี้ทางตัดสิน + จุดที่ต้องเช็คก่อน + กับดัก safety. *ทุก threshold/เกณฑ์ ต้องอิง SOP + มาตรฐานกาชาดจริง*

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — Donor eligibility: รับ / defer ชั่วคราว / defer ถาวร / ส่งต่อ
เช็คเป็นชั้น (ลำดับตาม SOP — ไม่ใช่ลำดับตายตัว):
1. **ยืนยันตัวตน + ลงทะเบียน + ระยะห่างจากครั้งก่อน** (whole blood vs apheresis ระยะห่างต่างกัน — apheresis platelet มักสั้นกว่า)
2. **วัดได้: Hb/Hct · BP · ชีพจร · อุณหภูมิ · น้ำหนัก** — ต่ำ/สูงเกินเกณฑ์ → defer ชั่วคราว (ส่วนใหญ่กลับมาได้)
3. **แบบสอบถามสุขภาพ/พฤติกรรมเสี่ยง** — อาการป่วย/ไข้ · เพิ่งสัก-เจาะ-ฝังเข็ม · เดินทางพื้นที่มาลาเรีย/โรคประจำถิ่น · ตั้งครรภ์/ให้นม · เพิ่งฉีดวัคซีน/ถอนฟัน/ผ่าตัด · ยาบางชนิด (เช่น ยากลุ่ม teratogen, antiplatelet สำหรับ platelet donor)
4. **เกณฑ์ permanent defer:** ประวัติติดเชื้อทางเลือด (HIV/HBV/HCV) · พฤติกรรมเสี่ยงสูงต่อเนื่อง · มะเร็งบางชนิด · ภาวะที่ความเสี่ยงถาวร — ตาม list ของมาตรฐาน
- ⚠️ ตัวเลขเกณฑ์ (เช่น Hb, น้ำหนักขั้นต่ำ, ช่วงอายุ, ระยะห่างการบริจาค, ระยะ defer หลังสัก/มาลาเรีย/วัคซีน) = **teaching illustration — ต่างกันตามมาตรฐาน/ประเทศ/edition + ปรับปรุงเป็นรอบ → verify กับ SOP+กาชาดทุกครั้ง** ห้ามจำเป็นเลขสากล
- **defer = ปกป้องทั้ง donor และ recipient** — อย่าฝืนรับเพราะขาดเลือด/เสียดาย
- **confidential / self-exclusion** ต้องมีช่องให้ donor ถอนหน่วยเงียบ ๆ (กัน window-period unit จากคนที่ตอบไม่ตรงต่อหน้า)
- autologous/directed = เกณฑ์ต่าง · **directed จากญาติสายเลือด / HLA-selected / ผู้รับกลุ่มเสี่ยง = irradiate ตาม SOP** (ไม่ใช่ "directed" ทุกชนิดอัตโนมัติ; irradiation = วิธีมาตรฐานป้องกัน TA-GVHD — โยง `bloodbank-judgment` Fork 5)

### Fork 2 — Whole blood vs apheresis + citrate/ECV
> **verdict:** อยากได้ component เดี่ยว yield สูง/ลด donor exposure ของผู้รับ → **apheresis** · อยากได้หลาย component/ง่าย/donor ทั่วไป → **whole blood**
- **whole blood:** เก็บง่าย → แยกได้หลาย component, ระยะห่างนานกว่า
- **apheresis:** เก็บเฉพาะส่วน (platelet/plasma/2-RBC/granulocyte) คืนส่วนที่เหลือ → **single-donor yield สูง = ลดจำนวน donor ที่ผู้รับสัมผัส** (อาจลด HLA-alloimmunization/refractory — **ไม่ใช่กฎตายตัว** ขึ้นกับ leukoreduction/HLA strategy/ประวัติตั้งครรภ์-รับเลือด/สาเหตุ non-immune), platelet ระยะห่างสั้นกว่า; double-RBC เหมาะ donor ตัวใหญ่ Hb สูง (ระวัง Hb ตกหลังบริจาค)
- ⚠️ **granulocyte = protocol พิเศษเท่านั้น (ไม่ใช่ apheresis ทั่วไป):** donor มักต้องกระตุ้น (steroid/G-CSF) + sedimenting agent (เช่น HES) ตาม protocol (วิธีต่างกันตามหน่วย) · อายุสั้นมาก · ต้อง irradiate · บางครั้งจ่ายก่อนผล TTI ครบ → เก็บ/จ่ายเฉพาะมีคำสั่งแพทย์ + SOP/ศูนย์อ้างอิง (RED FLAG)
- ⚠️ **citrate (ACD) toxicity / hypocalcemia** = ภาวะเด่นของ apheresis: ชา/เสียวรอบปาก-ปลายมือเท้า → รุนแรง = เกร็ง (tetany)/หัวใจเต้นผิดจังหวะ → **ลดอัตราคืนเลือด/หยุดพัก + แคลเซียม ตาม SOP** (severe = RED FLAG)
- ⚠️ **ECV (extracorporeal volume)** ต้องคุมเป็น % ของปริมาตรเลือดรวม donor (เด็ก/คนตัวเล็กเสี่ยง) · vascular access/hemolysis ในสาย · ค่าตัวเลข (ECV %, ACD ratio) = ตาม SOP เครื่อง/มาตรฐาน

### Fork 3 — Donor adverse reaction → จัดการ + กันซ้ำ
> **verdict:** หยุดเก็บ → ดูแลตามชนิด → **อย่าปล่อย donor ออกก่อนหายดี** (delayed faint นอกหน่วย = อันตรายสุด)
- **vasovagal (พบบ่อยสุด):** ซีด/เหงื่อ/คลื่นไส้/หน้ามืด/เป็นลม → หยุดเจาะ, นอนราบยกขา, สังเกตอาการ · กัน: applied muscle tension, ดื่มน้ำ/กินก่อนบริจาค, คัดคนเสี่ยง (อายุน้อย/น้ำหนักน้อย/บริจาคครั้งแรก)
- **hematoma:** กดให้แน่นพอ, ประคบตาม SOP · ⚠️ บวมโตเร็ว/ปวดรุนแรง/ชา-อ่อนแรง/มือซีดเย็น/สงสัยโดนเส้นเลือดแดง-เส้นประสาท = หยุด + ส่งแพทย์ประเมินด่วน (ไม่ใช่แค่ประคบ)
- **citrate (apheresis):** Fork 2
- ⚠️ **delayed/late faint** (เป็นลมหลังออกจากหน่วย — ขับรถ/ตกบันได) = อันตราย → ให้ **นั่งพัก กินดื่ม สังเกต ก่อนปล่อย** + คำแนะนำหลังบริจาค
- donor reaction ไม่ใช่แค่ safety — กระทบ **retention** (donor หาย = blood supply หาย) → จัดการดี + บันทึก hemovigilance

### Fork 4 — Component preparation: ทำ component ไหนได้ (timing เป็นตัวตัดสิน)
> **verdict:** ดู **เวลาที่ผ่าน + อุณหภูมิที่เก็บมา + ระบบ closed/open** ก่อนตัดว่ายังทำ component อะไรได้
- whole blood → **PRC + plasma**; platelet (จาก PRP หรือ buffy-coat); cryo (จาก plasma)
- ⚠️ **platelet ไวต่อเวลา/อุณหภูมิ** — ต้องแยกภายในเวลาที่กำหนด และ **ห้ามแช่เย็น whole blood ก่อนตั้งใจแยก platelet** (เย็น = platelet เสียหน้าที่) — *กรณี routine RT platelet*; cold-stored/cryopreserved platelet = program เฉพาะที่ SOP validate + label ต่างหาก ไม่ใช่ของทั่วไป
- ⚠️ **plasma จะเป็น "FFP" ต้อง freeze ภายในเวลาที่กำหนดหลังเก็บ** — ช้ากว่านั้น = plasma/“FP24” (labile factor V, VIII ตก) → ใช้แทนกันไม่ได้ทุกข้อบ่งชี้ · cryo = thaw FFP ที่ 1–6°C เก็บส่วนตกตะกอน
- ⚠️ **ตัวเลขเวลา (platelet แยกภายในกี่ ชม. · plasma freeze ภายในกี่ ชม. · FFP vs FP24) = ต่างตาม anticoagulant/SOP/edition → verify** ไม่ใช่เลขสากลตัวเดียว
- **closed vs open system:** เปิดระบบ (เช่น pooling/แบ่ง) → sterility ลด → **shelf-life สั้นลงตาม SOP**

### Fork 5 — Component QC: ผ่าน / fail → ทิ้ง unit หรือ quarantine ทั้ง batch
> **verdict:** QC fail → จัดการตาม **ความรุนแรง/SOP**: **quarantine unit/co-component/pool ที่เกี่ยวข้องก่อน** → ขยายเป็น **ทั้ง lot เมื่อชี้ว่าเป็น process/equipment/trend** (critical/bacterial/ซ้ำ) · isolated noncritical outlier = บันทึก + investigate + trend (อย่าทิ้ง unit เดียวแล้วเดินต่อเงียบ ๆ โดยไม่ดู process)
- **พารามิเตอร์ตามชนิด (ตัวอย่าง — เกณฑ์ยึดมาตรฐาน):** PRC = Hct/ปริมาตร · platelet = yield (จำนวน), pH, swirling, ปริมาตร · FFP = ระดับ factor (เช่น FVIII), ปริมาตร · leukoreduced = residual WBC · cryo = fibrinogen/FVIII
- **QC เชิงสถิติ:** สุ่มตรวจ **% ของ production** (ไม่ใช่ทุก unit) → ต้องผ่านสัดส่วนที่กำหนด → fail = ทบทวนทั้งกระบวนการ (เครื่องปั่น/อุณหภูมิ/เทคนิค) — โยง `lab-management-judgment` (EQA/process control)
- ⚠️ **bacterial/sterility โดยเฉพาะ platelet** (เก็บอุณหภูมิห้อง = เสี่ยง bacterial สูงสุด) → มีระบบตรวจ/เฝ้าระวังตามมาตรฐาน
- ⚠️ เกณฑ์ตัวเลข QC (% ที่ต้องผ่าน · ค่า cut-off แต่ละ parameter) = ตาม AABB/มาตรฐานกาชาด/edition → **verify** ไม่ใช่จำลอย

### Fork 6 — Storage / shelf-life / cold-chain / unit คืน
> **verdict:** unit ออกจากตู้ควบคุมอุณหภูมิ → **รับกลับ stock ได้ก็ต่อเมื่อยังอยู่ในเกณฑ์ temp/เวลาที่ SOP กำหนด** เท่านั้น — เลยเกณฑ์ = quarantine/ทิ้ง (ไม่เดาว่า "ยังเย็นอยู่")
- อุณหภูมิ/อายุเก็บ (ตัวอย่าง — **ขึ้นกับ anticoagulant/additive**): RBC เก็บเย็น (เช่น 1–6°C) · platelet อุณหภูมิห้องพร้อม agitation (ห้ามแช่เย็น — *routine RT*; cold-stored/cryopreserved = program เฉพาะที่ validate/label) · FFP แช่แข็ง · plasma ละลายแล้วมีอายุสั้น
- ⚠️ **อายุ RBC ต่างตาม anticoagulant/additive (CPDA vs SAG-M/AS-x)** → ตัวเลขวันเป็นตัวอย่าง verify · platelet อายุสั้น (เสี่ยง bacterial) — บางที่ขยายอายุได้เมื่อมีระบบตรวจเชื้อ
- **กฎรับคืน (เช่น "30-min rule"/เกณฑ์ temp):** unit ที่ออกไปแล้วกลับมา → วัด/ประเมินตาม SOP ว่ารับกลับได้ไหม — **อย่ารับคืนโดยดู "เวลา" อย่างเดียวถ้า cold-chain หลุด**
- transport/cold-chain ต้อง validate (กล่อง/น้ำแข็ง/เวลา)

### Fork 7 — TTI (donor infectious screening): reactive → unit/donor ทำไง
> **verdict:** screen reactive → **unit: ห้ามจ่าย → quarantine/segregate ทันที** (discard ตอน disposition หลัง repeat/confirm — เก็บ sample/record ไว้เพื่อ traceability) · **donor: ยังไม่ใช่ "ติดเชื้อ" จนกว่าจะ confirm** → ทำซ้ำ/ยืนยันตามอัลกอริทึม → confirmed = defer + แจ้ง+counsel (RED FLAG)
- ตรวจตามมาตรฐาน (ตัวอย่าง): HBsAg · anti-HCV · anti-HIV 1/2 · ซิฟิลิส · + **NAT** (HBV/HCV/HIV) · (ตามพื้นที่: HTLV/malaria ฯลฯ)
- **screen reactive → repeat/confirmatory ตามอัลกอริทึม** ก่อนสรุปสถานะ donor — **false-positive มีจริง** → แจ้ง donor ว่า "ติดเชื้อ" ก่อนยืนยัน = ผิดจริยธรรม/ตีตรา
- ⚠️ **window period:** NAT ลดช่วงหน้าต่างแต่ **ไม่เป็นศูนย์** → screen-negative ≠ ปลอดภัยสัมบูรณ์ → ต้องมี donor self-exclusion + ประวัติพฤติกรรมเสี่ยง (Fork 1)
- confirmed-positive → donor deferral (ชั่วคราว/ถาวรตามเชื้อ/มาตรฐาน) + ส่ง counsel/รักษา + เชื่อมไป **look-back** (Fork 8)

### Fork 8 — Hemovigilance ฝั่ง donor + look-back / recall / quarantine
> **verdict:** มีข้อมูลใหม่ที่ทำให้หน่วยเดิม "อาจไม่ปลอดภัย" → **เร็วคือชีวิต** — quarantine หน่วยที่ยังไม่ใช้ + recall/แจ้ง รพ. ของหน่วยที่จ่ายไปแล้ว
- **post-donation information:** donor โทรกลับว่าป่วย/มีอาการ/นึกออกว่ามีพฤติกรรมเสี่ยงหลังบริจาค → **quarantine/recall** component ที่ยังไม่ transfuse
- **look-back:** donor รอบใหม่ TTI **reactive** → *initial reactive* = hold/quarantine หน่วยที่เกี่ยวข้อง + เริ่มตามรอยภายใน · *confirmed / repeat-reactive ตามอัลกอริทึม* = counsel donor + ตามรอย component **ครั้งก่อน ๆ** → แจ้ง รพ./ผู้รับ/look-back ตามระบบ (reactive เดี่ยว ≠ ติดเชื้อ/แจ้งผู้รับทันที — สอดคล้อง Fork 7)
- **TRALI mitigation (ฝั่งผลิต):** plasma/platelet ที่มี plasma มากจาก **donor หญิงที่เคยตั้งครรภ์** อาจมี anti-HLA/anti-HNA → ใช้นโยบาย male-predominant plasma / คัดกรองตามมาตรฐาน (กัน TRALI ที่ผู้รับ — โยง `bloodbank-judgment` Fork 6)
- **bacterial contamination (platelet):** สงสัย → recall + สอบสวน + แจ้ง (RED FLAG)
- ⚠️ **recall = แข่งกับการ transfuse** — ยิ่งช้า หน่วยยิ่งถูกใช้ไปก่อน → มีระบบ traceable donor→unit→ผู้รับ (โยง `interprofessional-communication-judgment` แจ้ง รพ. · `incident-postmortem-judgment` RCA)

---

## กับดัก (Anti-patterns) — เช็คทุกครั้ง
- **ฝืนรับ donor ที่เข้าเกณฑ์ defer เพราะขาดเลือด/เสียดาย** → เสี่ยงทั้ง donor และ recipient (defer ปกป้อง 2 ทาง)
- **จำเลขเกณฑ์เป็น "กฎสากล"** (Hb/น้ำหนัก/อายุ/ระยะห่าง/defer-period) → ต่างตามมาตรฐาน/edition → ต้อง verify SOP เสมอ
- **แจ้ง donor ว่า "ติดเชื้อ" จาก screen-reactive ก่อน confirm** → false-positive ตีตราคนบริสุทธิ์ (unit ห้ามจ่าย/quarantine ทันที แต่ donor ต้อง confirm ก่อนแจ้ง)
- **เชื่อ screen-negative = ปลอดภัย 100%** → ลืม window period → ตัด self-exclusion/ประวัติเสี่ยงทิ้ง
- **citrate reaction มองเป็นแค่ "ชา ๆ"** → ปล่อยจนเกร็ง/หัวใจเต้นผิดจังหวะ (apheresis) — ต้องลด rate/หยุด/แคลเซียมตาม SOP
- **ปล่อย donor ออกทั้งที่ยังไม่หายดี** → delayed faint นอกหน่วย (ขับรถ/ล้ม)
- **แช่เย็น whole blood ก่อนแยก platelet / เลยเวลาแล้วยังทำ FFP** → component เสียหน้าที่เงียบ ๆ (labile factor/platelet ตาย)
- **QC fail แล้วทิ้งแค่ unit เดียว เดินต่อ** → process ทั้ง batch อาจเสีย → ต้อง quarantine + สอบสวน
- **รับ unit คืนเข้า stock โดยดูแค่เวลา ไม่ดู cold-chain** → หน่วยที่อุ่นเกินกลับเข้าคลัง
- **ลืม irradiate หน่วยกลุ่มเสี่ยง TA-GVHD** (ญาติสายเลือด/HLA-selected/granulocyte + ผู้รับตามบ่งชี้เฉพาะ — **รายการบ่งชี้เต็มเป็นฝั่งผู้รับ ดู `bloodbank-judgment`**) → TA-GVHD ที่ผู้รับ (irradiation = วิธีมาตรฐานป้องกัน; leukoreduction อย่างเดียวไม่กัน)
- **post-donation info / TTI look-back แล้วไม่ recall เร็ว** → หน่วยถูก transfuse ไปก่อน
- **ตอบข้ามฝั่งไป compatibility/ABO discrepancy/transfusion reaction ผู้รับ** → นั่นคือ `bloodbank-judgment` ไม่ใช่สกิลนี้

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมจากประสบการณ์จริงหน้างานหน่วยรับบริจาค/ศูนย์ผลิต เช่น:
> - *"(MT donor unit) เคส donor reaction ที่เกือบพลาด คือ... จับได้เพราะ..."*
> - *"เกณฑ์ defer ที่หน่วยผมต่างจากตำราตรงไหน เพราะมาตรฐาน/บริบท..."*
> - *"เคส look-back/recall ที่เคยเจอ — ตามรอย unit ทันเพราะ... / เกือบไม่ทันเพราะ..."*
> - *(สาย sales/ผลิต) apheresis platform · NAT · automated component processor · QC analyzer ที่ใช้จริง = ..."*

---
*เพื่อการศึกษา/ช่วยทบทวน ไม่ใช่คำสั่งทางการแพทย์หรือผู้ตัดสินใจแทน — งานบริการโลหิตเกี่ยวกับชีวิตทั้งผู้บริจาคและผู้รับ ต้องทำตาม SOP + วิจารณญาณ MT/แพทย์ และยึดมาตรฐานธนาคารเลือดฯ ศูนย์บริการโลหิตแห่งชาติ สภากาชาดไทย (AABB/ISBT/FDA = อ้างอิงสากล) เสมอ · ตัวเลขทุกตัว = teaching illustration ต่างตามมาตรฐาน/anticoagulant/edition — verify เอง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
