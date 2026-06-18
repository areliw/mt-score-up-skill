---
skill: pubmed-search-judgment
title: ค้น PubMed ให้เจอของจริง (PubMed Search)
type: ADVISE               # ช่วยวางวิธีค้น + กับดัก ไม่ได้ค้นแทน
needs: any                 # ใช้ได้ทุก AI — เต็มที่สุดกับ AI ที่เปิด PubMed/เน็ตได้
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-08
status: semi-stable
disclaimer: "ช่วยวางกลยุทธ์ค้น PubMed/วรรณกรรม ไม่ใช่คำแนะนำทางการแพทย์ — ผลที่เจอต้องเปิดอ่านต้นฉบับจริงก่อนอ้าง (AI แต่ง PMID/citation ได้เนียน) ผู้นำไปใช้รับผิดชอบงานที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ค้น PubMed ให้เจอของจริง

วาง query ให้ "เจอครบแต่ไม่จม" บน pubmed.ncbi.nlm.nih.gov — เน้น **ตัดสินใจว่าจะค้นยังไง + คัดผลยังไง** ไม่ใช่ท่องคำสั่งหรือเชื่อสรุปจาก AI ดิบๆ

> **กฎข้อ 1:** แตกคำถามเป็น concept **เท่าที่จำเป็นพอให้ recall ดี** (มัก 2-3: โรค/ภาวะ × test/method) → แต่ละ concept หา **MeSH + คำพ้อง OR กัน** แล้ว AND — อย่าพิมพ์ทั้งประโยคยาวรวดเดียว. *เพิ่ม concept "ชนิดงานวิจัย" เฉพาะเมื่อจำเป็น และใช้ validated filter ดีกว่าผูกเอง (design term รัดแน่นเกิน → ตกงานเงียบ).*
> **กับดักข้อ 1:** **อย่าเชื่อสรุป/รายการเปเปอร์ที่ AI ร่ายให้โดยไม่เปิด PubMed จริง** — AI แต่ง PMID, ชื่อเปเปอร์, ปี, ผลการศึกษา ได้เนียนมาก. ทุก citation ที่จะอ้าง = เปิด pubmed.ncbi.nlm.nih.gov ใส่ PMID/ชื่อ ดูว่ามีจริง + abstract ตรงที่อ้าง (ดู `anti-hallucination`).

## ใช้เมื่อ
- หาเปเปอร์ทำ lit review / R2R / thesis / journal club จากคำถามจริง
- ค้นแนว "test/method ใหม่ vs gold standard" ในงาน MT (ความไว/จำเพาะ, validation)
- เจอผลน้อยเกิน (0-3 อัน) หรือ เยอะเกิน (พันๆ) แล้วไม่รู้จะแคบ/กว้างยังไง
- จะให้ AI ช่วยร่าง query หรือสรุปเปเปอร์ แต่กลัวมันมั่ว/แต่งอ้างอิง

## วิธีใช้
วาง skill นี้ + เล่าคำถามวิจัยของคุณ (โรค/test/อยากได้งานชนิดไหน) → AI ช่วยแตก concept, เสนอ MeSH + คำพ้อง, ประกอบ query ให้ก๊อปไปวางช่องค้น PubMed ได้เลย + บอกวิธีกรองผล. **ผลที่เจอต้องเปิดอ่านเองก่อนอ้างทุกครั้ง**

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — MeSH หรือ keyword เมื่อไหร่
| สถานการณ์ | ใช้อะไร | เพราะ |
|---|---|---|
| concept มีศัพท์มาตรฐานนิ่ง (โรค/สาร classic) | **MeSH** `[mh]` | จับทุกบทความที่ index ไว้ แม้คำผู้เขียนต่างกัน |
| หัวข้อใหม่/ศัพท์ยังไม่ลงตัว/ของปีล่าสุด | **keyword** `[tiab]` | งานใหม่ยัง MeSH ไม่ทัน index |
| อยากชัวร์ ไม่ตก | **MeSH OR keyword** ของ concept เดียวกัน | กันงานใหม่หลุดจาก MeSH |
| ต้องให้ตรงเป๊ะ central topic | `[majr]` (major MeSH) | precision ขึ้น แต่ **เสี่ยงตกงานที่เกี่ยวแต่ไม่ใช่ธีมหลัก** |

> **VERDICT:** ของปีล่าสุด/หัวข้อ niche → อย่าพึ่ง MeSH อย่างเดียว, OR keyword เข้าไปด้วย. งาน classic ที่ต้องครบ → MeSH นำ.

### Fork 2 — ประกอบ query: AND / OR / filter
- **OR = ในกลุ่มคำพ้อง** (กว้างขึ้น): `(thalassemia[mh] OR thalassaemia[tiab])`
- **AND = เชื่อม concept ต่างกลุ่ม** (แคบลง): `concept1 AND concept2 AND concept3`
- **field tag ที่ใช้คุ้ม:** `[tiab]` ชื่อเรื่อง+บทคัดย่อ · `[mh]` MeSH · `[pt]` ชนิดบทความ · `[dp]` ปี · `[la]` ภาษา · `[au]` ผู้เขียน
- **filter ที่ช่วยได้ — แต่ใส่เมื่อ justified เท่านั้น** (date/article-type/Humans ตัด record ใหม่หรือที่ยังไม่ index ใน MEDLINE ทิ้งได้ — เลือกจากแถบซ้ายของ PubMed ก็ได้):
  - ปี: ช่อง Custom range หรือ `2020:2026[dp]`
  - ชนิดงาน: `systematic review[pt]` / `meta-analysis[pt]` / `randomized controlled trial[pt]` / `review[pt]` / `guideline[pt]`
  - มนุษย์เท่านั้น: ติ๊ก **Humans** (กัน in-vitro/animal ปน) มีประโยชน์ในงาน diagnostic คน — *แต่กรองได้เฉพาะ record ที่ index แล้ว → งานใหม่ยังไม่ index อาจหลุด, ใช้เมื่อจำเป็น*
  - Free full text: ติ๊กถ้าจะอ่านฟรีตอนนี้ (แต่ **อย่าใช้กรองคุณภาพ** — ของดีหลายอันไม่ฟรี)

> **VERDICT — ลำดับหลักฐานขึ้นกับ "ชนิดคำถาม":** การรักษา/ป้องกัน → SR/MA → RCT → cohort. **diagnostic accuracy (คำถามหลักของ MT) → cross-sectional/cohort accuracy study เทียบ reference standard ที่เหมาะ ไม่ใช่ RCT** · ความชุก → survey. **อย่ากรอง RCT-only กับคำถาม diagnostic** (ตกงานที่ใช่).

### Fork 3 — ผลน้อยเกิน vs เยอะเกิน → ปรับยังไง
| อาการ | สาเหตุที่พบบ่อย | แก้ |
|---|---|---|
| 0-3 ผล | สะกดผิด / แคบไป / ลืมคำพ้อง / `[majr]`+`[ti]` รัดแน่นไป | OR คำพ้องเพิ่ม, เปลี่ยน `[ti]`→`[tiab]`, ตัด concept ที่ 3 ออก, ผ่อนปี |
| เป็นพันๆ | concept กว้างลอย / ไม่มี filter | AND concept เจาะจงเพิ่ม, ใส่ปี+ชนิดงาน, ใช้ `[majr]` |
| เจอแต่ที่ไม่เกี่ยว | คำมีหลายความหมาย / animal/in-vitro ปน | ติ๊ก Humans, เพิ่มคำบริบท, ใช้ MeSH แทน keyword กว้าง |
| ตกงานที่รู้ว่ามี | คำพ้อง/สะกดอังกฤษ-อังกฤษ(UK/US) ไม่ครบ | เติม OR (เช่น anemia/anaemia, leukemia/leukaemia) |

### Fork 4 — อ่าน abstract เพื่อ "คัด" ไม่ใช่ "เชื่อ"
- คัดเร็วจากหน้า results: ดู **ชนิดงาน + ปี + ตรง concept เราไหม** ก่อนเปิดเต็ม
- ในงาน MT recurring สุด = "test ใหม่ vs gold standard": มอง **sensitivity/specificity เทียบ gold standard อะไร** — ⚠️ **PPV ขึ้นกับทั้ง prevalence และ specificity: โรคหายาก + spec ไม่สูงพอ → ผลบวกส่วนใหญ่อาจเป็น false+** (ดู `critical-appraisal-judgment` Fork ประเมิน test)
- abstract ใช้ **คัดเข้า/คัดออก** เท่านั้น — **ตัวเลข/ข้อสรุปจริงต้องเปิด full text** ก่อนเอาไปอ้าง (abstract ตัดบริบทบ่อย)

### Fork 5 — บันทึกให้ค้นซ้ำได้ (reproducible)
จดทุกรอบที่ค้น เพื่อทำซ้ำ/เขียน method ได้: **query เป๊ะ · วันที่ค้น · filter · จำนวนผล · ที่คัดออกเอง**
- ⚠️ **อย่าพึ่ง PubMed ฐานเดียวกับงานที่ต้องครบ** (systematic review/thesis) — Scopus/Embase/Google Scholar coverage+recall ต่างกัน, ค้นเสริมถ้ามีสิทธิ์; พึ่ง Google Scholar อย่างเดียว = คุณภาพปนเปื้อน

| วันที่ค้น | Query | Filter | ผล |
|---|---|---|---:|
| 2026-06-08 | `(thalassemia[mh]) AND (machine learning[tiab] OR deep learning[tiab])` | 2018:2026, Humans | (เปิดดูจริง) |

> ตารางนี้ = ตัวอย่างฟอร์แมต **ห้ามกรอกตัวเลขผลจากการเดา** — เลขผลต้องมาจากหน้าจอ PubMed จริง

---

## กับดัก (Anti-patterns)
- **เชื่อรายการเปเปอร์/PMID/ตัวเลขที่ AI ร่ายให้ โดยไม่เปิด PubMed จริง** — AI แต่งได้เนียน, เปิดยืนยันทุก citation
- **พิมพ์ทั้งประโยคยาวรวดเดียว** ("what is the best test for...") — แตก concept + AND/OR ก่อน
- **ลืมคำพ้อง / สะกด UK-US** (anaemia, thalassaemia, paediatric) → ตกงานเงียบๆ
- **พึ่ง MeSH อย่างเดียวกับหัวข้อปีล่าสุด** — งานใหม่ยังไม่ index, ต้อง OR keyword
- **กรองด้วย Free full text เพื่อเอาคุณภาพ** — ของดีหลายอันไม่ฟรี, ฟรี≠ดี
- **อ่านแค่ abstract แล้วอ้างตัวเลข** — เปิด full text ก่อน, abstract ตัดบริบท
- **ลืมติ๊ก Humans ในงาน diagnostic** → in-vitro/animal ปนจนตีความเพี้ยน
- **ไม่จด query/วันที่** → ทำซ้ำไม่ได้ เขียน method ไม่ได้

> ค้นเจอแล้ว → ประเมิน/หา gap ต่อที่ `literature-review-judgment` · งานค้นลึกหลายแหล่ง → `deep-research` · กันอ้างมั่ว/แต่ง citation → `anti-hallucination`

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริงในสายงานคุณ เช่น:
> - *"(R2R) query ที่ผมใช้หางาน method-comparison ของ test ... ที่เวิร์กคือ..."*
> - *"คำพ้อง/MeSH ที่ผมเคยลืมแล้วตกงานสำคัญ คือ..."*
> - *"เคสที่ AI แต่ง PMID/เปเปอร์ให้ผม แล้วจับได้ตอนเปิดจริง คือ..."*

---
*ช่วยวางกลยุทธ์ค้น PubMed/วรรณกรรม ไม่ใช่คำแนะนำทางการแพทย์ — ผลที่เจอต้องเปิดอ่านต้นฉบับจริงก่อนอ้าง (AI แต่ง PMID/citation ได้เนียน) ผู้นำไปใช้รับผิดชอบงานที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
