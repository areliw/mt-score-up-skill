---
skill: result-release-judgment
title: ปล่อยผล/post-analytical ให้เป็น — delta-check · autoverify · critical · corrected (Result Release & Verification Judgment)
type: ADVISE               # ช่วยตัดสินใจด่าน post-analytical ไม่ใช่สั่งปล่อย/วินิจฉัยแทน
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-15
status: draft
disclaimer: "เพื่อการศึกษา/ช่วยทบทวน ไม่ใช่คำสั่งปล่อยผลหรือวินิจฉัย — ทุกการปล่อย/ยับยั้ง/แก้ไขผลต้องอิง SOP ของแล็บ + วิจารณญาณ MT/แพทย์ผู้มีใบประกอบฯ และเกณฑ์/threshold/limit ต่างกันตามเครื่อง/analyte/ประชากร/มาตรฐาน (verify เอง) · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ปล่อยผล/post-analytical ให้เป็น — delta-check · autoverify · critical · corrected

ด่าน post-analytical คือ **ด่านสุดท้ายก่อนผลถึงมือคนรักษา** — ผิดตรงนี้ = ถึงคนไข้ตรงๆ. หลายคนคิดว่า "ค่าออกจากเครื่องแล้ว = เสร็จ" แต่จริงๆ ต้องตัดสิน: **ปล่อย / repeat / recollect / hold / แจ้งด่วน / แก้ที่ปล่อยไปแล้ว**. สกิลนี้ช่วยตัดสินด่านนี้ + กันกับดักที่ patient-safety สูง

> **กฎ #1:** **delta check เด้ง = อย่าเพิ่งเชื่อว่า "คนไข้เปลี่ยนจริง" — rule-out สาเหตุอื่นก่อน** โดยเฉพาะ **specimen mix-up/mislabel** (error อันตรายสุด, delta เป็นด่านสำคัญที่ดักได้). สาเหตุ delta = biological change/รักษา/transfusion · timing · pre-analytical · analytical · mix-up — น้ำหนักต่างกันตาม analyte/ช่วงเวลา/SOP ไม่ใช่ลำดับตายตัว
> **กับดัก #1:** ปล่อยผลจาก **รอบ QC ที่ fail** หรือจาก **ตัวอย่างที่ integrity เสีย** (HIL/clot/wrong tube) โดยไม่สอบสวนก่อน — ผลจาก process ที่ invalid = ขยะที่ดูเหมือนข้อมูล (เช็ค QC + sample ก่อนดูตัวเลข — โยง `clinchem-judgment` · `preanalytical-judgment`)
> โยง: `clinchem-judgment` (QC accept/reject · critical · repeat-vs-report) · `chemistry-interpretation-judgment` (plausible กับ clinical ไหม) · `interprofessional-communication-judgment` (แจ้ง critical — golden-period) · `incident-postmortem-judgment` (root-cause เมื่อต้องแก้ผล)

## ใช้เมื่อ
- ผลออกจากเครื่องแล้ว ต้องตัดสิน **ปล่อย / repeat / recollect / hold / dilute / escalate**
- **delta check เด้ง** (ค่าต่างจากครั้งก่อนมาก) — เปลี่ยนจริงหรือ artifact/สลับตัวอย่าง?
- ตั้ง/ทบทวน **autoverification (auto-release) rule** — ปล่อยอัตโนมัติได้แค่ไหน เมื่อไหร่ต้องหยุดให้คนดู
- เจอ **critical value** — แจ้งยังไงให้ครบ + เป็นหลักฐาน
- พบว่า **ผลที่ปล่อยไปแล้วผิด** — corrected/amended report ยังไง

## วิธีใช้
วาง skill นี้ + เล่าสถานการณ์ (analyte, ค่าที่ได้, ค่าก่อนหน้า, QC รอบนี้, สภาพ sample, flag เครื่อง) → AI ช่วยชี้ว่า ปล่อย/repeat/recollect/hold/แจ้ง + จุดที่ต้องเช็คก่อน + กับดัก patient-safety. *threshold/limit ต้องอิง SOP แล็บจริง*

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — ด่านปล่อยผล: ปล่อย / repeat / recollect / hold / escalate
เช็คเป็นชั้น **ก่อน**ตัดสินจากตัวเลข:
1. **QC รอบนั้นผ่านไหม?** fail → ผลของ **analyte/ช่วงที่กระทบ** น่าสงสัย → สอบสวนว่าครอบคลุมผลไหน/ตั้งแต่เมื่อไร แล้วแก้+rerun *เฉพาะที่กระทบ* (ไม่ใช่ rerun ทุกอย่างอัตโนมัติ — โยง `clinchem`)
2. **Sample integrity?** HIL/clot/wrong-tube/ปริมาณไม่พอ → analyte ที่กระทบ = ไม่ปล่อย/ใส่หมายเหตุ/recollect (โยง `preanalytical`)
3. **Flag เครื่อง / เกิน AMR?** → ตาม SOP: **validated dilution** *หรือ* report `>limit` *หรือ* วิธีอื่น/เก็บใหม่ (ไม่ใช่ dilute เสมอ — dilution ต้อง validated ก่อน)
4. **Delta check เด้ง?** → Fork 2
5. **Plausible กับ clinical/ค่าอื่นในแผง?** ขัดแรงหาเหตุไม่ได้ → hold + สืบ (โยง `chemistry-interpretation`)
6. **Critical?** → Fork 4 (แจ้ง ไม่ใช่แค่ปล่อย)
- ผ่านทุกชั้น → ปล่อยได้. ติดชั้นไหน → เลือก **repeat (sample เดิม) / recollect (เก็บใหม่) / alternate method / hold / แจ้ง / escalate** ตามชั้นนั้น + SOP

### Fork 2 — delta check เด้ง → แยก เปลี่ยนจริง vs artifact vs สลับตัวอย่าง
ค่าต่างจากครั้งก่อนเกิน threshold → **สอบสวนตาม SOP (analyte-specific) = follow-up ที่กำหนด ไม่ใช่ไล่ exclude ทุกอย่างเสมอ; ถ้ายังรับรอง identity/integrity ไม่ได้ → hold/recollect/escalate.** สาเหตุที่ต้องนึกถึง (เรียงตามความอันตราย):
- **specimen mix-up / mislabel (อันตรายสุด — ห้ามข้าม):** เช็ค ID ตัวอย่าง, เวลาเก็บ; ถ้าค่า "อื่นๆ" ของคนไข้พลิกทั้งแผง = **เพิ่มความสงสัย** สลับคน (ไม่ใช่ยืนยัน — บางภาวะก็พลิกหลายค่าได้)
- **pre/analytical artifact:** wrong tube/order-of-draw, carryover, drift, IV-contamination → repeat/recollect ให้ถูกต้อง
- **เปลี่ยนจริง:** ได้รักษา/transfusion/ภาวะเปลี่ยน/timing — พิจารณาบริบท clinical ประกอบ (ตาม SOP)
- ⚠️ **อย่าปล่อยเพราะ "ค่าใหม่ดูเป็นไปได้"** — plausible ≠ ถูกคน

### Fork 3 — autoverification (auto-release): เปิดได้แค่ไหน
- **auto-release มักให้ผ่านเมื่อครบ:** QC ผ่าน · อยู่ในช่วงรายงานได้ (ไม่เกิน AMR) · ไม่ใช่ critical · delta ผ่าน · ไม่มี instrument/sample flag
- **มักตั้งให้ STOP → คนรีวิว / เข้า workflow เฉพาะ (ตาม SOP/validated config):** critical · delta เด้ง · flag เครื่อง · HIL · เกิน AMR · บาง first-time-abnormal
- ⚠️ **autoverify rule = แล็บออกแบบเอง ต้อง validate + มี exception handling + audit + ทบทวนเป็นรอบ** *ก่อน*ใช้ — ไม่ใช่ข้อกำหนดสำเร็จรูปจากมาตรฐาน (มาตรฐานเช่น CLSI AUTO15 [AUTO10 เดิม archived] / ISO 15189 ให้กรอบ — อ้าง edition ที่ใช้จริง). เปิด auto โดยไม่มี stop-condition = critical/ผิด หลุดออกเงียบ

### Fork 4 — critical value: แจ้ง ≠ แค่ปล่อย
- **critical = ค่าที่ "ไม่แจ้งทันที = เสี่ยงอันตรายร้ายแรง/ทันทีต่อคนไข้"** ตาม list ของแล็บ (ไม่จำเป็นต้อง "ถึงชีวิต" เท่านั้น) — ไม่ใช่ทุกค่าผิดปกติ = critical
- **ต้องครบ (ตาม SOP/ข้อกำหนด accreditor):** แจ้งคนรับผิดชอบ **ทันที**ตาม turnaround + **ยืนยันการรับ + ตัวตนคนไข้** ด้วย method/identifiers ที่ SOP/accreditor กำหนด (**read-back สำหรับแจ้งทางวาจา** เท่าที่กำหนด) + **log** (เวลา/ใครแจ้ง/ใครรับ) + **escalate ถ้าหาคนรับไม่ได้**
- **repeat ก่อนแจ้ง = เฉพาะเมื่อ SOP กำหนด/สงสัย analytical จริง** ไม่ใช่ routine — และ **ห้ามหน่วงจนเกิน turnaround** (เร็วสำคัญ — โยง `interprofessional`)

### Fork 5 — corrected/amended report: แก้/เพิ่มผลที่ปล่อยไปแล้ว
- แยก (คำนิยามต่างตาม LIS/สาขา/SOP): **corrected** = แก้ที่ *ผิด* · **amended** = เพิ่ม/เปลี่ยนข้อมูลภายหลัง — ทั้งคู่ **เก็บ original + audit trail** (รูปแบบที่แสดงตามระบบ ไม่จำเป็นต้องโชว์ "เดิม→ใหม่" ทุกที่)
- **ห้ามลบ/ทับเงียบ** · **แจ้งคนที่ใช้ผลเดิม ตามข้อกำหนด** — ความเร่งด่วนตามความเสี่ยง (กระทบการดูแล/อาจ act ตามค่าผิดไปแล้ว = ด่วนสุด)
- **root-cause ตามระดับความเสี่ยง** — ทุก correction บันทึก/ทบทวน แต่ RCA เต็มรูปทำตามความรุนแรง (โยง `incident-postmortem-judgment`) — กันซ้ำ ไม่ใช่แค่แก้ตัวเลข

---

## กับดัก (Anti-patterns)
- **"ค่าออกจากเครื่อง = เสร็จ"** — post-analytical คือด่านที่ผิดแล้วถึงคนไข้ตรงๆ
- **ปล่อยผลจาก run ที่ QC fail / sample integrity เสีย** โดยไม่สอบสวน — ขยะที่ดูเหมือนข้อมูล
- **delta เด้งแล้วปล่อยเพราะ "ดูเป็นไปได้"** → มองข้าม specimen mix-up (error อันตรายสุด)
- **เชื่อ autoverify ดิบ ไม่มี stop-rule / ไม่ validate** → critical/flag/HIL หลุดออกเงียบ
- **เกิน AMR แล้วปล่อยตรงๆ** โดยไม่ validated-dilution / report-`>limit` / วิธีอื่น
- **critical value แจ้งแล้วไม่ read-back / ไม่ระบุ identifier / ไม่ log** → แจ้งผิดค่า/ผิดคน/พิสูจน์ไม่ได้
- **แก้ผลที่ปล่อยแล้วแบบลบเงียบ** ไม่มี audit trail + ไม่แจ้งคนที่ใช้ผลเดิม
- **หน่วงแจ้ง critical เพื่อ repeat จนเกิน turnaround** — repeat ก่อนแจ้งไม่ใช่ routine

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมจากประสบการณ์จริง เช่น:
> - *"เคส delta เด้งที่กลายเป็นสลับตัวอย่างจริง — จับได้ตอน..."*
> - *"autoverify rule ที่แล็บผมตั้ง stop-condition ไว้ที่... เพราะเคยหลุด..."*
> - *"critical value ที่เคยแจ้งพลาด (ผิดคน/ผิดค่า) เพราะไม่ได้ read-back — บทเรียนคือ..."*

---
*เพื่อการศึกษา/ช่วยทบทวน ไม่ใช่คำสั่งปล่อยผลหรือวินิจฉัย — ทุกการปล่อย/ยับยั้ง/แก้ไขผลต้องอิง SOP ของแล็บ + วิจารณญาณ MT/แพทย์ และเกณฑ์/threshold/limit ต่างกันตามเครื่อง/analyte/ประชากร/มาตรฐาน (verify เอง) · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
