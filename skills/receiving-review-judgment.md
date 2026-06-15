---
skill: receiving-review-judgment
title: รับคำติ/รีวิวให้เป็น — take/drop/push-back ไม่ใช่ caved หรือ ego (Receiving Review Judgment)
type: ADVISE               # ช่วยตัดสินใจตอบ feedback ไม่ใช่ที่ปรึกษา HR/relationship
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-15
status: draft
disclaimer: "กรอบคิดการรับ/ตอบ feedback เพื่อการศึกษา — บริบทงาน/ทีม/เจ้าของ-decision ต่างกัน ต้องปรับเอง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# รับคำติ/รีวิวให้เป็น — take/drop/push-back ไม่ใช่ caved หรือ ego

เวลามี feedback เข้ามา (code review · รีวิวเปเปอร์ · หัวหน้าติงาน · codex/linter/CI) คนส่วนใหญ่พลาด 2 ทางสุดขั้ว: **caved** (แก้ตามทุก comment จนเสียของที่ตั้งใจ) หรือ **ego** (ปกป้องตัวเองไม่ฟัง). สกิลนี้ช่วย **triage แต่ละ comment + รู้เมื่อไหร่ push-back + apply ให้ตรง intent** — ไม่ใช่รับดิบหรือปัดทิ้ง

> **กฎ #1:** feedback ไม่ได้น้ำหนักเท่ากัน — แยก **correctness/security (รับก่อน)** vs **style/taste (ใช้วิจารณญาณ/disagree-and-commit ได้)**. แก้ทุก comment เท่ากัน = เสียทั้งเวลาและ design
> **กับดัก #1:** apply feedback แบบ **literal** โดยไม่เข้าใจ "ทำไม" → แก้ผิดจุด. comment คือ *อาการ* ที่ reviewer เห็น — หา intent/ root ก่อนแก้ (โดยเฉพาะ nit เล็กๆ ที่จริงชี้ปัญหาใหญ่)
> โยง: `critical-appraisal-judgment` (ฝั่งประเมินงานคนอื่น) · `verification-panel` (ตรวจของตัวเองหลายมุมก่อนยอมรับ) · `anti-hallucination` (verify ข้อ flag จาก tool ก่อนเชื่อ) · `polite-but-clear` (เรียบเรียง push-back) · `report-up-judgment` (ตอบกลับขึ้นบน)

## ใช้เมื่อ
- ได้ code review / รีวิวเปเปอร์ / คอมเมนต์งาน แล้วต้องตัดสินว่า comment ไหนแก้ ไหนแย้ง ไหนพอ
- รู้สึกอยากแก้ตามทุกอย่าง (กลัวดื้อ) หรืออยากเถียงทุกอย่าง (รู้สึกโดนจับผิด) — เช็คตัวเองก่อนตอบ
- feedback จาก AI/automated (codex/linter/CI) แล้วไม่แน่ใจว่าเชื่อแค่ไหน
- มีหลาย comment เยอะจนงง ว่าจะเริ่มตรงไหน + อันไหนสำคัญจริง

## วิธีใช้
วาง skill นี้ + แปะ feedback ที่ได้มา + บอก context (เจ้าของ decision คือใคร, deadline, นี่ของใคร) → AI ช่วยจัด take/drop/push-back ต่อ comment + ชี้ตัวที่ต้องหา root ก่อนแก้ + ร่างคำตอบกลับที่ไม่ ego

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — triage ทีละ comment: TAKE / DROP-or-defer / PUSH-BACK
จัดทุก comment ตามเกณฑ์ **"ถูกต้องไหม × กระทบอะไร × cost-of-change"** (3 verdict):
- **TAKE (แก้):** ถูกต้องเชิงข้อเท็จจริง · กระทบ correctness/security/ความเข้าใจผิด · cost ต่ำ-value สูง
- **PUSH-BACK (แย้งด้วยเหตุผล):** reviewer พลาด context / เป็น style preference ไม่ใช่ correctness / ขัด requirement หรือ constraint ที่ reviewer ไม่เห็น → ตอบด้วย *เหตุผล + ทางเลือก* ไม่ใช่ "ไม่เอา"
- **DROP-or-defer:** จริงแต่ out-of-scope/nice-to-have → ปิดพร้อมเหตุผล หรือถ้าคุ้มทำทีหลัง = log (issue/TODO); *feedback ที่ไม่ถูก/ไม่คุ้ม ปิดได้เลย ไม่ต้อง log ทุกอัน*
- **ทางออกเมื่อ push-back บน *taste* แล้วไม่จบ = disagree-and-commit:** ถ้าเป็น taste และ **เจ้าของ decision ไม่ใช่คุณ** → แย้งครั้งเดียว เขายืน = ทำตาม (อย่าตายเพราะ taste คนอื่น). **⚠️ ยกเว้น correctness/security/legal/ethics — ห้าม commit เงียบ → escalate หรือบันทึกความเสี่ยงเป็นลายลักษณ์อักษร**

### Fork 2 — เมื่อไหร่ push-back (ไม่ใช่ caving, ไม่ใช่ ego)
- **push-back ได้/ควร เมื่อ:** comment อิงข้อมูลผิด · reviewer ไม่เห็น constraint (perf/deadline/compat) · เป็น preference ที่ทั้งสองทางโอเค · แก้ตามแล้วจะ *แย่ลง*
- **ห้าม push-back เพราะ:** เสียหน้า · ขี้เกียจแก้ · "โค้ดฉัน" → นั่นคือ ego ไม่ใช่เหตุผล
- **ท่า push-back ที่ดี:** ยอมรับประเด็น → ให้ข้อม./constraint ที่ขาด → เสนอทางเลือก → ถามกลับ ("ติดตรง X เลยเลือกแบบนี้ — มีมุมที่ผมมองข้ามไหม?") (เรียบเรียง → `polite-but-clear`)
- ⚠️ **push-back ทุกอย่าง = คนเลิกอยากรีวิวให้** (เสีย feedback loop — เหมือน lazy-monopoly ในองค์กร)

### Fork 3 — อ่าน "nit" ให้ทะลุ (comment เล็กที่ *อาจ* ชี้ root ใหญ่)
- nit ซ้ำๆ (ชื่อสับสน, comment เยอะผิดปกติ, "ตรงนี้งงๆ") **บางครั้ง** = สัญญาณ design/abstraction ผิด — **แต่ก็อาจแค่ naming/convention/docs ไม่พอ** → เช็คก่อนรื้อ design
- **อย่าแก้แค่ surface ที่เขาชี้โดยไม่ถาม "ทำไม reviewer สะดุดตรงนี้"** → ถ้า root อยู่ลึกกว่า ค่อยแก้ลึก
- หลาย comment ชี้อาการเดียวกัน = อาจเป็น **pattern** → *ถ้ายืนยันว่า root เดียวกันจริง* แก้เชิงโครงสร้างทีเดียวคุ้มกว่าไล่ทีละจุด (ระวังเพิ่ม scope/risk ถ้าไม่ใช่ root เดียว)

### Fork 4 — feedback จาก AI/automated (codex/linter/CI) ต่างจากคน
- **น้ำหนักต่างกัน:** flag severity สูง (security/correctness) = **จัดลำดับตรวจก่อน/เร่งด่วน** *ไม่ใช่ "รับข้อสรุปเลย"* · style/heuristic/"best practice" = ใช้วิจารณญาณ (มัก overstate/ไม่รู้ context)
- **false-positive เกิดได้เสมอ** → **verify ก่อน apply ทุกครั้ง** อย่าเชื่อ tool ดิบ (เคยเจอ: tool เคลม PII/bug ที่จริงเป็น false alarm — โยง `anti-hallucination`)
- **take/drop ไม่ raw:** เข้าใจว่ามันชี้อะไร → apply เฉพาะที่ **verify แล้วว่าจริง** + แก้ให้ตรง intent ไม่ใช่ก๊อปคำแก้มาทั้งดุ้น
- AI review ดีที่ **ครอบคลุม + ไม่เกรงใจ** แต่แย่ที่ **ไม่รู้ business context** → **เจ้าของ decision** (คุณ หรือ owner/maintainer/security ตามเรื่อง) คือคนตัดสินสุดท้าย ไม่ใช่ tool

---

## กับดัก (Anti-patterns)
- **Caved — แก้ตามทุก comment** จนเสีย design/scope ที่ตั้งใจ (รวมถึง taste คนอื่นที่ไม่ใช่เจ้าของ)
- **Ego — ปัดทุก comment / push-back เพราะเสียหน้า** ไม่ใช่เพราะเหตุผล
- **treat ทุก feedback น้ำหนักเท่ากัน** (nit = blocker, style = correctness)
- **apply literal ไม่เข้าใจ intent** → แก้ผิดจุด / แก้ surface ทั้งที่ root อยู่ลึกกว่า
- **มองข้าม nit ที่ชี้ปัญหาใหญ่** (ชื่อสับสน = อาจ design ผิด)
- **เชื่อ automated review ดิบ** — ไม่ verify false-positive ก่อน apply
- **push-back ทุกอย่างจนคนเลิกรีวิวให้** — ฆ่า feedback loop ตัวเอง
- **ดอง comment "drop" ไว้เฉยๆ** ไม่ log → ลืม → หนี้ทางเทคนิคสะสม

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมจากประสบการณ์จริง เช่น:
> - *"รีวิวที่ผม push-back แล้วถูก/ผิด ต่างกันตรงที่..."*
> - *"comment เล็กๆ ที่กลายเป็นว่าชี้ปัญหาใหญ่ คือเคส..."*
> - *"feedback จาก tool ที่ผมเคยเชื่อดิบแล้วพลาด คือ..."*

---
*กรอบคิดการรับ/ตอบ feedback เพื่อการศึกษา — บริบทงาน/ทีม/เจ้าของ-decision ต่างกัน ต้องปรับเอง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
