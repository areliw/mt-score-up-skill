---
skill: source-credibility
title: ประเมินแหล่งเชื่อได้แค่ไหน — กัน predatory/มั่ว/เก่า (Source Credibility)
type: ADVISE               # ช่วยประเมินความน่าเชื่อแหล่ง ไม่ใช่ฐานข้อมูล journal
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-08
status: draft
disclaimer: "ช่วยคิดประเมินความน่าเชื่อของแหล่งเพื่อการศึกษา ไม่ใช่การรับรอง/ตัดสินทางวิชาการขั้นสุดท้าย · เรื่องการแพทย์ต้องยืนยันกับ guideline/แหล่ง authoritative + ผู้เชี่ยวชาญ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ประเมินแหล่งเชื่อได้แค่ไหน

ตัวช่วยตัดสินว่า "แหล่ง/งานวิจัย/journal/เว็บนี้ เชื่อได้แค่ไหน" ก่อนเอาไปอ้าง/ตัดสินใจ — เน้น "คัด + จัดลำดับความน่าเชื่อ + กับดัก" ไม่ใช่ลิสต์ journal ดี

> **กฎ #1:** เชื่อตาม **หลักฐาน + วิธี** ไม่ใช่ "ใครพูด/journal ดัง" — แต่ต้อง **คัด predatory/แหล่งกำมะลอออกก่อน**เสียเวลาอ่าน
> **กับดัก #1 (ขั้น hard):** **impact factor สูง / "peer-reviewed" ไม่การันตีว่าถูก** และ predatory journal เลียนแบบเนียนมาก → เช็ค **indexing (PubMed/Scopus/DOAJ), publisher, peer-review จริง** ก่อนอ้าง

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ตามไป primary source เสมอ

## ใช้เมื่อ
- จะอ้างงานวิจัย/แหล่งแต่ไม่แน่ใจเชื่อได้ไหม (predatory? เก่า? ถูก retract?)
- เจอข้อมูล/ข่าว/โพสต์ทางการแพทย์ จะแชร์/เชื่อดีไหม
- AI ให้ข้อมูล+อ้างอิงมา จะ trust แค่ไหน

## วิธีใช้
วาง skill นี้ + แหล่ง/paper/ลิงก์ที่จะประเมิน → AI ช่วยไล่เช็ค (indexing/หลักฐาน/COI/ปี/retract) + จัดระดับความน่าเชื่อ แล้วชี้ให้คุณตามไป primary + ยืนยันเอง

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### Fork 1 — คัด predatory ก่อน
- อยู่ใน **PubMed/Scopus/DOAJ/Web of Science** ไหม · publisher น่าเชื่อไหม · **ค่าตีพิมพ์เร่ง/ถูกผิดปกติ + รับเร็วเกิน** · สเปม invite · editorial board มั่ว/ปลอม · ISSN ตรวจได้ไหม (เชื่อม `manuscript-judgment` ฝั่งเลือกที่ตีพิมพ์)

### Fork 2 — ลำดับชั้นหลักฐาน
- systematic review/meta > RCT > cohort > case-control > case series > opinion/expert
- ปรับตามคำถาม — ไม่ใช่ทุกคำถามต้อง RCT (เช่น harm/prognosis ใช้ cohort เหมาะกว่า)

### Fork 3 — ประเมินตัวงาน
- **COI/funding** (ใครจ่าย) · method/sample size สมเหตุผลไหม · **ปีที่ตีพิมพ์** (เก่าเกินจน guideline เปลี่ยนแล้ว?) · reproducible ไหม · **ถูก retract ไหม** (Retraction Watch / PubMed notice)

### Fork 4 — แหล่งที่ไม่ใช่ paper
- เว็บ/ข่าว/social → **ใครเขียน, อ้างอะไร, มี primary source ไหม, วันที่**
- guideline จากองค์กรไหน (WHO/CDC/ราชวิทยาลัย/CLSI vs บล็อก/เพจ) — แยกระดับ authority

### Fork 5 — ใช้ AI
- AI สรุป/อ้างผิดได้ + **แต่ง citation เนียน** → ตามไป **primary source + verify ว่ามีจริง** เสมอ (เชื่อม `anti-hallucination`)

## กับดัก (Anti-patterns)
- #1 เชื่อเพราะ IF สูง/journal ดัง/"peer-reviewed" (กับดัก #1)
- #2 อ้าง predatory journal โดยไม่รู้ (ไม่เช็ค indexing)
- #3 ไม่ดู COI/funding ที่อาจ bias ผล
- #4 อ้างงานเก่าที่ guideline เปลี่ยนแล้ว / งานที่ถูก retract
- #5 เชื่อ secondary (ข่าว/รีวิว/AI สรุป) โดยไม่ตามไป primary
- #6 เชื่อ citation จาก AI โดยไม่ verify
- #7 เหมาว่า "ออนไลน์/มีคนแชร์เยอะ = จริง"
- #8 ใช้ระดับหลักฐานเดียวกับทุกคำถาม (บังคับ RCT ทุกเรื่อง)

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - แหล่ง/journal ที่สายงานคุณใช้อ้างประจำ + ตัวที่เคยพบว่า predatory
> - guideline/องค์กร authoritative ในสาขาคุณ (ที่ถือเป็นมาตรฐาน)
> - กรณีที่เคยเกือบเชื่อแหล่งผิด → เป็นบทเรียน

NOTE: ประเมิน method งานวิจัยเชิงลึก (bias/validity) → `critical-appraisal-judgment`; กลยุทธ์ค้นหาแหล่ง → `pubmed-search`

---
*skill นี้ช่วย "คิดประเมินแหล่ง" เพื่อการศึกษา · เรื่องการแพทย์ยืนยันกับ guideline/แหล่ง authoritative + ผู้เชี่ยวชาญ; ตามไป primary เสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
