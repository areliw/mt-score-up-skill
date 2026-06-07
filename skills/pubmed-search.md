---
skill: pubmed-search
title: ค้น PubMed ให้เจอ + ไม่พลาด (PubMed / Literature Search)
type: ADVISE               # ช่วยสร้าง query + กลยุทธ์ค้น ไม่ใช่ค้นให้
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-08
status: draft
disclaimer: "ช่วยคิดกลยุทธ์ค้นวรรณกรรมเพื่อการศึกษา ไม่ใช่การรับรองความครบถ้วนของผลค้น · ทุก citation ต้อง verify ว่ามีจริง (PMID/DOI) ก่อนอ้าง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ค้น PubMed ให้เจอ + ไม่พลาด

ตัวช่วยตอน MT ต้องค้นงานวิจัย/หาหลักฐาน (lit review, R2R, ตอบคำถามคลินิก) — เน้น "สร้าง query + ขยาย/แคบ + ประเมินเร็ว" ไม่ใช่สอนคลิก PubMed

> **กฎ #1:** เริ่มจากคำถามแบบ **PICO → แปลงเป็น MeSH + คำพ้อง** ไม่ใช่พิมพ์ประโยคยาวลง search box (PubMed ตีความประโยคยาวไม่ตรง)
> **กับดัก #1 (ขั้น hard):** ค้นคำเดียว/ภาษาเดียวแล้วสรุป **"ไม่มีงานวิจัย"** — มักพลาดเพราะไม่ใช้ MeSH + synonym + ไม่ดู related/citing. **absence of evidence ≠ evidence of absence**

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ทุก paper เช็คว่ามีจริงด้วย PMID

## ใช้เมื่อ
- ต้องหางานวิจัยสำหรับ lit review / R2R / ตอบคำถามคลินิก
- ค้นแล้วเจอน้อย/เยอะเกิน ไม่รู้ปรับ query ยังไง
- อยากให้ AI ช่วยร่าง search string

## วิธีใช้
วาง skill นี้ + คำถาม/หัวข้อที่จะค้น → AI ช่วยแปลงเป็น PICO + ร่าง query (MeSH + synonym + Boolean) + แนะ filter แล้วชี้ให้คุณรันใน PubMed จริง + verify ผลเอง

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### Fork 1 — สร้าง query
- คำถาม → **PICO** → concept blocks → `(MeSH OR free-text synonym)` ของแต่ละ concept ต่อด้วย **AND** ระหว่าง concept
- เทคนิค: `[Mesh]`, `[tiab]` (title/abstract), truncation `*`, phrase `"..."`, MeSH subheadings
- ตัวอย่างโครง: `(conceptA[Mesh] OR "synonymA"[tiab]) AND (conceptB ...)`

### Fork 2 — filter อย่างฉลาด (อย่า over-filter)
- ชนิด study (RCT / systematic review / meta-analysis), ปี, humans, ภาษา
- ⚠️ filter แรงเกินตัดของดีทิ้ง — ใช้เมื่อผลเยอะจริง; เริ่มกว้างก่อนค่อยแคบ

### Fork 3 — ขยาย / แคบ
- **เจอน้อยไป**: ลด AND, เพิ่ม synonym/MeSH, ดู "Similar articles" + citing
- **เจอเยอะไป**: เพิ่ม concept/filter, หา **systematic review ก่อน** (สรุปให้แล้ว)

### Fork 4 — ประเมินเร็วก่อนอ่านเต็ม
- abstract + study type + journal + ปี → คัดเข้า/ออก (เชื่อม `critical-appraisal-judgment`, `source-credibility`)
- อย่าอ้างจาก abstract อย่างเดียว — อ่าน full-text ก่อนอ้างผลสำคัญ

### Fork 5 — จัดการผล + reproduce
- เก็บใน reference manager (Zotero ฟรี); **บันทึก query string + วันที่ค้น** ไว้ reproduce (สำคัญสำหรับ systematic review)
- PubMed ฟรี; ถ้ามีสิทธิ์ Scopus/Embase/Google Scholar ใช้เสริม (recall ต่างกัน)

### Fork 6 — ใช้ AI ช่วย
- ให้ AI ร่าง MeSH/synonym/แปลคำถาม — เร็ว
- ⚠️ **AI แต่ง citation ปลอมได้เนียน** → verify ทุก paper ด้วย PMID/DOI ว่ามีจริง (เชื่อม `anti-hallucination`)

## กับดัก (Anti-patterns)
- #1 สรุป "ไม่มีงานวิจัย" จากค้นครั้งเดียว/คำเดียว (กับดัก #1)
- #2 พิมพ์ประโยคยาวแทน keyword/MeSH
- #3 ไม่ใช้ synonym/คำพ้อง → recall ต่ำ
- #4 over-filter จนตัดของดีทิ้ง
- #5 เชื่อ citation จาก AI โดยไม่เช็ค PMID ว่ามีจริง
- #6 อ้างจาก abstract อย่างเดียว ไม่อ่าน full-text
- #7 ไม่บันทึก query → reproduce/อัปเดตไม่ได้
- #8 พึ่งฐานเดียว (เฉพาะ Google Scholar) → คุณภาพ/recall ปนเปื้อน

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - คำถามวิจัย/หัวข้อที่คุณกำลังค้น (จะได้ช่วยร่าง MeSH ให้ตรง)
> - ฐานข้อมูลที่สถาบันคุณเข้าถึงได้ (Scopus/Embase/CINAHL?)
> - เกณฑ์คัดเข้า/ออก (inclusion/exclusion) ของ review คุณ

NOTE: การประเมินคุณภาพงานวิจัยเชิงลึก → `critical-appraisal-judgment`; ประเมินความน่าเชื่อแหล่ง/journal → `source-credibility`; ไวยากรณ์ MeSH ละเอียด → PubMed help

---
*skill นี้ช่วย "คิดกลยุทธ์ค้น" เพื่อการศึกษา ไม่รับรองความครบถ้วน · verify citation (PMID/DOI) ทุกครั้งก่อนอ้าง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
