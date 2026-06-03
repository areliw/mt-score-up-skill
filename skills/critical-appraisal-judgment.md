---
skill: critical-appraisal-judgment
title: โค้ชอ่าน/ประเมินงานวิจัย + lit review — หา gap + ประเมิน test (Critical Appraisal & Lit-Review Judgment)
type: ADVISE               # ช่วยอ่าน/ประเมินเปเปอร์คนอื่น ไม่ใช่ตำราระเบียบวิธี
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
reviewed: 2026-06-01
status: draft
disclaimer: "ช่วยคิดอ่าน/ประเมินงานวิจัย + ทบทวนวรรณกรรมเพื่อการศึกษา ไม่ใช่ที่ปรึกษาวิจัยทางการ — ต้องยืนยันกับเปเปอร์ต้นฉบับ + อาจารย์ที่ปรึกษา · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชอ่าน/ประเมินงานวิจัย + lit review — หา gap + ประเมิน test

อ่านงานวิจัยคนอื่นให้เป็น (lit review / journal club / หาหัวข้อ thesis) — เปเปอร์นี้ดี/เชื่อได้แค่ไหน · gap อยู่ตรงไหน · ใช้ method ไหนเป็นแม่แบบ ไม่ใช่สรุปย่อทุกบรรทัด

> นี่คือชั้น **"อ่าน/ประเมินงานคนอื่น + หา gap"** — ออกแบบงานตัวเอง → `research-design-judgment` · เขียนเล่ม/ตีพิมพ์ → `manuscript-judgment` · เลือก test สถิติ → `choose-stat-test` · กันอ้างมั่ว → `anti-hallucination`
> แก่น: อ่านเพื่อ **(1) เชื่อได้ไหม (2) ขโมย method มาใช้ได้ไหม (3) gap = contribution ของเราอยู่ตรงไหน** — ไม่ใช่จำ finding

## ใช้เมื่อ
- ทำ literature review / journal club / หา research gap ก่อนตั้งหัวข้อ
- อ่านเปเปอร์ "method ใหม่ vs gold standard" → ประเมินความน่าเชื่อ
- เลือกแม่แบบ (method spine) ให้ตรงข้อมูล/คำถามตัวเอง

## วิธีใช้
วาง skill นี้ + วาง abstract/เปเปอร์ (หรือเล่าคำถามวิจัย + กองเปเปอร์) → AI ช่วยสกัด method/finding/relevance + ชี้ gap + จุดอ่อนที่ตีได้

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — อ่านเปเปอร์ 1 ฉบับ: สกัด 4 อย่าง (transform ไม่ลอก)
- **Objective** (ถามอะไร) · **Method** (data → preprocess → model/analysis → evaluation) · **Key finding** (ตอบ objective ไหม) · **Relevance** (ใช้กับงานเรายังไง: แม่แบบ method / domain anchor / cite-เฉยๆ)
- จด **method skeleton ให้ทำซ้ำได้** (dataset, ขั้นตอน, พารามิเตอร์, metric) — ถ้าจะเอามาใช้ ต้อง lock ค่าจริงจากเปเปอร์เต็ม ไม่ใช่จากสไลด์/abstract

### Fork 2 — ประเมินงาน "test/method ใหม่ vs gold standard" (recurring สุดในงาน MT)
- โครง: **sensitivity / specificity / PPV / NPV / accuracy / AUC** เทียบ gold standard (เช่น molecular/biopsy/culture)
- ⚠️ **PPV ขึ้นกับ prevalence** — test ดีแค่ไหน ถ้า prevalence ต่ำ ผลบวกส่วนใหญ่ก็ false+ → ต้อง confirm (ดู `immunoassay-judgment`/`anti-hallucination`)
- ดู **gold standard เลือกเหมาะไหม** + sample size/spectrum bias + blinded ไหม ก่อนเชื่อตัวเลข

### Fork 3 — หา research gap = contribution (white space)
- เทียบกองเปเปอร์: **อะไรที่ยังไม่มีใครทำ** (เช่น domain A × method B ที่ไม่มีใครจับคู่) = ช่องว่างที่เราเคลม
- gap ที่ใช้ได้จริง = **ทำได้ด้วยข้อมูล/เวลาที่เรามี** + ตอบคำถามที่สำคัญพอ (ไม่ใช่ gap ที่ไม่มีคนทำเพราะมันไม่คุ้ม)

### Fork 4 — เลือก "method spine" (แม่แบบ) ให้ตรงข้อมูล+คำถาม
- มีหลายเส้นทาง → เลือกที่ **fit ข้อมูลที่หาได้จริง** + **lowest ramp-up** (อันที่เคยทำ/รู้ดี = เริ่มเร็ว เสี่ยงน้อย)
- เปรียบเทียบ spine (เช่น classifier vs association-study vs forecasting) ตาม: ชนิดข้อมูล · คำถาม · เครื่องมือที่มี → อย่าเลือกเพราะ "ดูเท่"

### Fork 5 — จับ "limitation to beat" = novelty lever
- จุดอ่อนที่เปเปอร์แม่แบบมัก: **single dataset / no external validation cohort / ไม่มี modern method / sample เล็ก** → แต่ละอันคือ **ช่องที่เราอัปเกรดเป็นความใหม่ได้** (เพิ่ม validation set, k-fold+held-out, model ที่ดีขึ้น)

### Fork 6 — Triage + read-order (อย่าอ่านทุกอันเท่ากัน)
- เรียงเปเปอร์ตาม **relevance ต่อคำถามเรา** → **read-in-full = แม่แบบ method + domain anchor** · skim = method-pattern ซ้ำ · **skip-to-cite = ที่เหลือ** (off-domain/ref)
- recurring backbone ในงาน MT diagnostic = diagnostic-accuracy (Fork 2) → results chapter ต้องพูดภาษานี้คล่อง

### Fork 7 — Quality flag ก่อนเชื่อ/อ้าง
- ⚠️ **OCR/text เพี้ยน → ตัวเลข garbled** → verify กับ PDF ต้นฉบับก่อน cite (อย่าอ้างเลขที่อ่านไม่ชัด)
- แยก **research article vs review vs product insert (IFU)** — IFU ≠ งานวิจัย, review = cite-don't-copy
- ⚠️ **ห้ามแต่ง finding ที่ไม่มีใน text** — สรุปเฉพาะที่เปเปอร์เขียนจริง

---

## กับดัก (Anti-patterns)
- **เชื่อ/อ้าง finding ที่ไม่มีในเปเปอร์จริง** — สกัดเฉพาะที่เขียนไว้
- **ลอก method ดิบ** ไม่ transform/ไม่เข้าใจ → ทำซ้ำไม่ได้
- **ลืม external validation** — single dataset = จุดอ่อน (และเป็น lever ของเรา)
- **อ่านทุกเปเปอร์เท่ากัน** — triage ตาม relevance ก่อน
- **ตีความ PPV โดยไม่ดู prevalence** — test ดีที่ low prevalence ก็ false+ ท่วม
- **cite ตัวเลข OCR/garbled** โดยไม่เช็คต้นฉบับ
- **ทำ contribution ที่ซ้ำของเดิม** — ไม่หา gap ก่อน = ไม่มี novelty

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(R2R) เปเปอร์ที่ผมใช้เป็นแม่แบบ method คือแนว... เพราะ fit ข้อมูล..."*
> - *"gap ที่ผมเจอจากการอ่านกองเปเปอร์ คือ... = contribution"*

---
*ช่วยคิดอ่าน/ประเมินงานวิจัย + ทบทวนวรรณกรรมเพื่อการศึกษา ไม่ใช่ที่ปรึกษาวิจัยทางการ — ต้องยืนยันกับเปเปอร์ต้นฉบับ + อาจารย์ที่ปรึกษา · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
