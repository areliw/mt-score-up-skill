---
skill: spreadsheet-judgment
title: ใช้ Excel/Sheets ให้ถูก + กัน error เงียบ (Spreadsheet Judgment for MT)
type: ADVISE               # ช่วยตัดสินใจวิธีใช้/วางโครง ไม่ใช่ตำราสูตร Excel
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-10-08
status: draft
disclaimer: "ช่วยคิดวิธีใช้ spreadsheet เพื่อการศึกษา ไม่ใช่คำแนะนำทางการ · ค่าที่กระทบคนไข้/QC ต้อง sanity-check + ยืนยันเอง; ไฟล์ที่มีข้อมูลผู้ป่วยอยู่ใต้ PDPA — ใส่รหัส/ไม่แชร์ลิงก์เปิด · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ใช้ Excel/Sheets ให้ถูก + กัน error เงียบ

ตัวช่วยตัดสินใจตอนใช้ spreadsheet (log, คำนวณ QC, ตาราง, สรุป) — เน้น "วางโครง + สูตร + กับดักที่ทำข้อมูลเสียเงียบ" ไม่ใช่ตำรารวมสูตร Excel

> **กฎ #1:** spreadsheet error **เงียบและแพร่** — สูตรผิด 1 ช่องลามทั้งไฟล์โดยไม่มี error สีแดง. ต้อง **sanity-check ผลรวม/ช่วงค่า** + ล็อก/ตรวจสูตรสำคัญเสมอ
> **กับดัก #1 (ขั้น hard):** **Excel แปลงข้อมูลเองทำลายของถาวร** — รหัส/วันที่/ชื่อยีน (เช่น `SEPT9`), barcode, HN ที่มี 0 นำหน้า ถูก autoconvert เป็นวันที่/เลข → ข้อมูลเสียกู้ยาก. **ตั้ง format เป็น Text ก่อน paste/import** + ตรวจคอลัมน์เสี่ยง

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`)

## เครื่องมือ (รันก่อนคิดเลข)
มีไฟล์ CSV ที่กำลังจะเปิดใน Excel/Sheets หรือมีตัวเลข SD/percentile จากเวิร์กบุ๊กที่จะเชื่อ → **รันสคริปต์ก่อน แล้วค่อยใช้ judgment ข้างล่างตัดสิน** (อย่าเปิดไฟล์ด้วย double-click เพื่อ "ลองดู" — การแปลงเกิดตอนเปิด) · รัน `--help` ก่อน ไม่ต้องอ่านซอร์ส · ไฟล์อยู่ใน `scripts/` ของโฟลเดอร์ skill (ใน repo: `skills/spreadsheet-judgment/scripts/`)
- `python scripts/sheet_audit.py samples.csv` → อ่าน CSV เป็นข้อความล้วน (ไม่แปลงอะไร) แล้วรายงานพร้อมแถว/คอลัมน์: **A001** เซลล์ที่ Excel จะแปลงเอง — `leading-zero` `00123`→123 · `gene-date` `SEPT2`→2-Sep, `MARCH1`→1-Mar, `DEC1`→1-Dec · `long-digits` เกิน 15 หลัก · `date-like` `1-2` `3/4` · `sci-notation` `12E3` พร้อมบอกว่า Excel จะโชว์อะไร · **A002** ข้อความ/หน่วย/`<5` ปนในคอลัมน์ตัวเลข (SUM/AVERAGE ข้ามเงียบๆ) · **A003** header ว่าง/ซ้ำ · **A004** แถวว่าง, แถวกลุ่ม/subtotal เซลล์เดียว, เซลล์ key ว่างใต้เซลล์ที่มีค่า (merge cell) · **A005** เซลล์ที่ "ถูกแปลงไปแล้ว" (เช่น `2-Sep` ในคอลัมน์ชื่อยีน) · exit 1 เมื่อมี ERROR · ข้อมูลตัวอย่าง `data/samples_example.csv` เป็นข้อมูลสังเคราะห์ ไม่ใช่ข้อมูลผู้ป่วย
- `python scripts/sheet_stats.py stdev 1345 1301 1368 …` → **STDEV.S (n−1) vs STDEV.P (n)** คู่กัน + mean, %CV, เส้น Levey-Jennings ±1/2/3 SD (จาก STDEV.S) · `percentile --p 0.9 [--exc] …` → PERCENTILE.INC/.EXC ตามนิยาม Excel (EXC นอกช่วง = `#NUM!`) · `summary FILE --col tat_min` → n, mean, median, P90, P95 + ธง "mean สูงกว่า median เกิน 10% (`--gap`) = เบ้ขวา ใช้ median + P90/P95" และรายการเซลล์ข้อความที่ Excel จะข้ามเงียบๆ
- ไม่ตรวจ: สูตรในเวิร์กบุ๊ก (VLOOKUP approximate, `$`, hardcode cutoff อยู่ในไฟล์ .xlsx ไม่ใช่ CSV) · ธงเป็น heuristic = "ไปเปิดเซลล์นี้ดู" ไม่ใช่คำตัดสิน · ทุก output มีบรรทัด `ADVISORY` (ไฟล์ที่มี PHI อยู่ใต้ PDPA)
- ทดสอบแล้ว: `evals/test_sheet_tools.py` (17 ข้อ เทียบตัวอย่างในเอกสาร Microsoft: STDEV.S 27.46391572 / STDEV.P 26.05455814, PERCENTILE.INC({1,2,3,4}, 0.3) = 1.9, EXC 0.25 = 1.25 และ `#NUM!` · Ziemann 2016 SEPT2/MARCH1/DEC1 · must-fail control 3 ตัว: ใช้ STDEV.P กับ sample · rank ของ percentile เลื่อนหนึ่งตำแหน่ง · เชื่อว่า Excel ไม่แปลงอะไร → ต้องแดง)

## ใช้เมื่อ
- เก็บ log/ผล/สต็อก ใน Excel/Sheets แล้วอยากให้ใช้ต่อ/วิเคราะห์ได้
- สูตร VLOOKUP/IF เพี้ยน, ค่าผิดไม่รู้ทำไม, ข้อมูลเปลี่ยนเองหลัง paste
- ไม่แน่ใจว่าควรอยู่ Excel ต่อ หรือย้ายไป DB

## วิธีใช้
วาง skill นี้ + เล่าว่าจะเก็บ/คำนวณอะไร (+ ตัวอย่างคอลัมน์) → AI ช่วยวางโครง tidy + เลือกสูตร + เตือนกับดัก autoconvert/สูตร แล้วชี้ให้คุณ sanity-check เอง

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### Fork 1 — วางโครงให้ถูก (tidy data)
- **1 แถว = 1 record, 1 คอลัมน์ = 1 ตัวแปร** · ไม่ merge cell · ไม่ใส่หน่วยปนค่า (แยกคอลัมน์หน่วย) · header ชื่อเดียวชัด
- โครง tidy → pivot/กรอง/วิเคราะห์/ย้ายไป tool อื่นได้ทันที (โครงสวยตาแต่ merge cell = วิเคราะห์ต่อไม่ได้)

### Fork 2 — สูตรที่ MT ใช้บ่อย + กับดัก
- **VLOOKUP/XLOOKUP**: บังคับ **exact match** (VLOOKUP ตัวที่ 4 = FALSE; XLOOKUP ปลอดภัยกว่า/ไม่พังเมื่อแทรกคอลัมน์)
- **IF ซ้อนหลายชั้น** → ใช้ IFS หรือ lookup table แทน (อ่าน/แก้ง่าย, พลาดยาก)
- **absolute ref `$`** เวลา copy สูตร (กัน range เลื่อน) · **อย่า hardcode ค่ากลางสูตร** (cutoff/factor → ใส่ในเซลล์อ้างอิง)

### Fork 3 — QC / สถิติใน Sheets
- **STDEV.S (ตัวอย่าง) vs STDEV.P (ประชากร)** — เลือกผิด = SD เพี้ยน
- Levey-Jennings = scatter + เส้น mean ±1/2/3 SD · นับด้วย COUNTIF/COUNTIFS
- **TAT distribution มักเบ้ → median + P90/P95 สื่อจริงกว่า mean** (mean ไม่ผิดเสมอ — เลือกตามว่าจะสื่ออะไร; เบ้มาก = median) (เชื่อม `build-a-dashboard`)

### Fork 4 — กัน error เชิงระบบ
- **Data validation** (dropdown/ช่วงค่า) กันกรอกมั่วตั้งแต่ต้นทาง
- **Conditional formatting** ไฮไลต์ outlier/ค่านอกช่วง · **freeze header** · แยก sheet **raw / calc** (อย่าคำนวณทับ raw)
- **version/backup** (Sheets มี version history; Excel เซฟสำเนา)

### Fork 5 — เมื่อไหร่เลิก Excel ไป DB/code
- เริ่มอืด/สูตรพัง · หลายคนแก้พร้อมกัน (ชนกัน) · ต้อง relationship/ประวัติ/audit → ย้ายไป **`mt-databases`** · *(จำนวนแถวเป็นสัญญาณคร่าวๆ — Sheets/Excel เอาอยู่หลายหมื่น–แสนแถวถ้า structure ดี; ตัดสินที่ workload/ความซับซ้อน ไม่ใช่เลขแถวตายตัว)*

### Fork 6 — ข้อมูลคนไข้
- ไฟล์มี HN/ชื่อ → **ไม่แชร์ลิงก์ "ใครมีลิงก์ก็เปิดได้"**, จำกัดสิทธิ์, ใส่รหัส, de-identify ก่อนส่งออก (เชื่อม `digital-judgment`)

## กับดัก (Anti-patterns)
- #1 Excel autoconvert รหัส/วันที่/ยีน/HN-นำ-0 → ข้อมูลเสียถาวร (กับดัก #1)
- #2 VLOOKUP approximate match (ลืม FALSE) → จับคู่ผิดเงียบ
- #3 merge cell / หน่วยปนค่า / หลาย record ต่อแถว → วิเคราะห์ต่อไม่ได้
- #4 STDEV.S vs STDEV.P ผิดตัว → QC/SD เพี้ยน
- #5 AVERAGE กับ TAT ที่เบ้ → ควร median + P90
- #6 hardcode cutoff/factor กลางสูตร → แก้ยาก/พังเงียบเมื่อค่าเปลี่ยน
- #7 ไม่มี data validation → ขยะเข้าตั้งแต่กรอก
- #8 คำนวณทับ sheet raw / ไม่ backup → กู้ไม่ได้
- #9 แชร์ไฟล์ที่มี PHI แบบลิงก์เปิด
- #10 ดันใช้ Excel กับข้อมูลที่ควรเป็น DB (โต/หลายคน/relationship)

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - ไฟล์ Excel ที่ทีมคุณใช้หนักสุด + จุดที่เคยพลาด (สูตรเพี้ยน/ข้อมูลเปลี่ยนเอง)
> - คอลัมน์เสี่ยง autoconvert ในข้อมูลคุณ (รหัสตัวอย่าง/วันที่/ผล)
> - QC rule/สูตรที่ใช้จริง + ค่าที่ห้ามคำนวณพลาด

---
*skill นี้ช่วย "คิด" เพื่อการศึกษา · ค่ากระทบคนไข้/QC ต้อง sanity-check + ยืนยันเอง; ไฟล์มี PHI อยู่ใต้ PDPA · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
