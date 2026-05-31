---
skill: crm-judgment
title: โค้ช CRM ขับเคลื่อนด้วยข้อมูล — สำหรับ MT สาย sales/คลินิก (Data-Driven CRM Judgment)
type: ADVISE               # ช่วยตัดสินใจเรื่องลูกค้า ไม่ใช่ตำรา framework
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
reviewed: 2026-06-01
status: draft
disclaimer: "ช่วยคิดเรื่องลูกค้า/CRM เพื่อการศึกษา ไม่ใช่คำแนะนำทางกฎหมาย — การใช้ข้อมูลส่วนบุคคลต้องผ่าน consent (PDPA) เสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช CRM ขับเคลื่อนด้วยข้อมูล (สำหรับ MT สาย sales / คลินิก / แอป)

MT ที่ไปสาย **diagnostics sales, เปิดคลินิก, หรือทำแอป/บริการ** แล้วต้องคิดแบบ "ลูกค้า" → โค้ชนี้ช่วย **ตัดสินใจเรื่องลูกค้า + เลี่ยงกับดัก** ไม่ใช่ท่องนิยาม framework

> นิยาม framework เป็น commodity — ที่นี่เก็บแต่ **"เลือกอะไรเมื่อไหร่" + กับดักที่คนพลาด** (โดยเฉพาะเรื่อง consent/PDPA ที่ผิดแล้วโดนฟ้อง)

## ใช้เมื่อ
- ออกแบบ segment ลูกค้า / logic แนะนำสินค้า / แผน retention-loyalty
- ตอบวิกฤต/คำร้องเรียน (PR) · คิด cross-sell น้ำยา/บริการ
- "segment ลูกค้ายังไง", "แนะนำสินค้า CF/CBF", "ลูกค้ากลุ่มนี้ทำไงต่อ"

## วิธีใช้
วาง skill นี้ + เล่าสถานการณ์ลูกค้า → AI ชี้ทางเลือก + กับดัก

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### 1. เลือก segmentation แบบไหน (เริ่มจาก "มีข้อมูลอะไร + จะเอาไปทำอะไร")
| ถ้า… | เลือก |
|---|---|
| อยากรู้ใครทำเงิน + จัดสรร resource | **Value-based** |
| มีแค่ log การใช้/ซื้อ (data หาง่าย) | **Behavioral** (เริ่มจากนี่ถ้าไม่มีอย่างอื่น) |
| อยากกัน churn / ดัน cross-sell ล่วงหน้า | **Propensity** (value-at-risk = propensity × value) |
| แยกคนภักดี vs คนจะหนี | **Loyalty** |

### 2. รู้ CLV 2×2 (กำไร × ความยาวความสัมพันธ์) แล้ว → ลงทุนกลุ่มไหนยังไง (fork ที่มีค่าสุด)
- **True Friends** (กำไรสูง/อยู่นาน) → **เทงบ nurture + retain** = กลุ่มที่ควรทุ่ม
- **Butterflies** (กำไรสูง/อยู่สั้น) → **เก็บช่วงสั้นแบบ transactional แล้ว STOP เมื่อจะไป** (อย่าฝืนดึงให้ loyal = เผางบ)
- **Barnacles** (กำไรต่ำ/อยู่นาน) → **cross-sell/up-sell หรือคุมต้นทุน** (push self-service); ดันไม่ขึ้น → ลดต้นทุนบริการ
- **Strangers** (กำไรต่ำ/อยู่สั้น) → **ไม่ลงทุน**

### 3. recommendation: CF vs CBF vs Hybrid
- **Collaborative Filtering (CF)** — "คนคล้ายกันชอบ" ใช้เมื่อมี history เยอะ (⚠️ พังกับลูกค้าใหม่ = cold-start)
- **Content-Based (CBF)** — เทียบ content กับ profile ใช้ตอน **cold-start/ลูกค้าใหม่**
- **Hybrid** — CBF อุ้มช่วงแรก → ผสม CF เมื่อ history พอ
- กฎจำง่าย: **ลูกค้าใหม่=CBF, เก่ามีประวัติ=CF, ระบบโตจริง=Hybrid**

### 4. crisis/PR posture (เลือกจาก "ความรับผิดชอบ")
- ไม่ใช่ความผิดเรา/ข่าวลือ → **Denial** · ผิดน้อย/สุดวิสัย → **Diminishment** · เราผิดหลัก → **Rebuilding** (ขอโทษ+ชดเชย ห้ามแถ)
- ใส่ **instructing + adjusting info ทุกวิกฤต** · **ห้ามใช้ Denial ปนกับ rebuilding** (ขัดกันเอง ดูไม่จริงใจ)

### 5. เมื่อไหร่ทำ Market-Basket / Association
มี transaction แบบตะกร้า + อยากหา bundle/cross-sell → วัด Support / Confidence P(B|A) / **Lift>1 = สัมพันธ์จริง** (อย่าเชื่อ confidence ลอยถ้า lift≈1)

---

## กับดัก (Anti-patterns)
- **ใช้ data ก่อนได้ consent (PDPA/GDPR)** — ☠️ ใหญ่สุด ต้อง **explicit consent ก่อน** เอา personal/behavioral data ไปใช้/ส่งต่อ; privacy by design ตั้งแต่ออกแบบ ไม่ใช่แปะทีหลัง
- **Cold-start ใน CF** — ยัด CF ให้ลูกค้าใหม่ที่ไม่มี history → แนะนำมั่ว → CBF อุ้มก่อน
- **ลงทุนผิดกลุ่ม (เท Butterflies)** — ทุ่ม retain คนที่ยังไงก็ไป = เผางบ; งบไปลง True Friends
- **Vanity metric** — วัด like/engagement ที่ไม่เชื่อมกับ revenue/retention; ถามทุกครั้ง: metric นี้แปลงเป็นเงิน/การอยู่ต่อยังไง
- **ใช้ Denial ผิดเคส** — ผิดจริงแต่ปฏิเสธ → เสีย trust ถาวร
- **Data quality หลุด** — segment จาก data accuracy/timeliness แย่ = garbage in/out
- **สับ Profiling กับ Segmentation** — profile = persona รายคน (วัตถุดิบ) · segment = กลุ่ม (ผลลัพธ์)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT→sales) lab ลูกค้าแบบ True Friend ผมดูแลโดย... · แบบ Butterfly ผม..."*
> - *"cross-sell น้ำยา/บริการ จังหวะที่ได้ผลคือ..."*

---
*ช่วยคิดเรื่องลูกค้า/CRM เพื่อการศึกษา ไม่ใช่คำแนะนำทางกฎหมาย — การใช้ข้อมูลส่วนบุคคลต้องผ่าน consent (PDPA) เสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
