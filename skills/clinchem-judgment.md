---
skill: clinchem-judgment
title: ตัวช่วยตัดสินใจแล็บเคมีคลินิก (Clinical Chemistry Judgment)
type: ADVISE
needs: any
author: "MT Score UP!"
last_edited: 2026-06-01
status: draft
disclaimer: "skill นี้เป็นตัวช่วย 'คิด' สำหรับการตัดสินใจในแล็บเคมีคลินิกเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ใช่ผู้ตัดสินแทน. ปล่อยผลผิด 1 ค่า = หมอรักษาผิด 1 คน — นี่คือความปลอดภัยผู้ป่วยโดยตรง. AI ช่วยไล่ logic/Westgard/interference เท่านั้น ทุกการตัดสิน accept/reject/report ต้องเป็นไปตาม SOP + QC policy ของแล็บ และยืนยันกับ MT/ผู้มีอำนาจลงนามก่อนเสมอ. ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ตัวช่วยตัดสินใจแล็บเคมีคลินิก

ตัวช่วยตัดสินใจในแล็บเคมีคลินิก — เน้น "จะ accept/reject run นี้มั้ย", "ค่านี้ปล่อยได้มั้ย", "interference ตัวนี้ทำผลเพี้ยนตัวไหน" ไม่ใช่ที่ท่อง reference range / นิยาม analyte

> หลักความปลอดภัย: **Sample integrity gate มาก่อน QC; QC gate มาก่อนปล่อยผล.** ปล่อยผลผิด 1 ค่า = หมอรักษาผิด 1 คน. เมื่อสงสัย → repeat/hold ก่อน report เสมอ.

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- ดู QC แล้วต้องตัดสิน accept หรือ reject run · Westgard ตัวไหน fire · L-J chart shift/trend แปลว่าอะไร
- เจอ sample hemolyzed/lipemic/icteric/clotted → ปล่อยผลได้มั้ย ตัวไหนเชื่อไม่ได้
- ได้ค่า critical / outlier / เกิน linearity → dilute / repeat / โทร หรือ report
- เลือกทาง recalibrate vs troubleshoot vs เปลี่ยน lot น้ำยา เมื่อ QC พัง
- (สาย sales/IVD) คุยภาษา sigma/TEa/QC กับ lab head ให้ตรงประเด็น

## วิธีใช้
วาง skill นี้ + ข้อมูล QC/sample/ค่าที่ได้ (control values, L-J pattern, สภาพตัวอย่าง, ค่าที่สงสัย) → AI ไล่ fork ตามลำดับ gate (sample → QC → report) แล้วบอกว่าควร accept/reject/repeat/dilute/โทร พร้อมเหตุผลและกับดักที่ต้องระวัง

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### FORK 1 — accept หรือ reject run? Westgard ตัวไหน fire
ลำดับอ่าน control แต่ละ run: 1₂ₛ คือ "ไฟเตือน" ไม่ใช่ตัด → ถ้าเกิน ±2SD ให้ไล่กฎ reject ต่อ:

| เห็นอะไร | กฎ | error | ตัดสิน |
|---|---|---|---|
| 1 ค่าเกิน ±2SD (ไม่เข้ากฎอื่น) | 1₂ₛ | — | warning เท่านั้น → ปล่อยได้ (อย่า reject ทันที = false reject ~5%) |
| 1 ค่าเกิน ±3SD | 1₃ₛ | random | REJECT |
| 2 ค่าติดกันเกิน +2SD (หรือ −2SD) ด้านเดียว | 2₂ₛ | systematic | REJECT |
| ค่าหนึ่ง >+2SD อีกค่า <−2SD ใน run เดียว (ห่าง >4SD) | R₄ₛ | random | REJECT |
| 4 ค่าติดกันเกิน ±1SD ด้านเดียว | 4₁ₛ | systematic | REJECT (stable system อาจตั้งเป็น warning) |
| 10 ค่าติดกันอยู่ด้านเดียวของ mean | 10ₓ | systematic | REJECT (stable system อาจเป็น warning) |

- กฎ random (1₃ₛ/R₄ₛ) → นึกถึง: ฟองอากาศ, mix ไม่ทั่ว, อุณหภูมิ/ไฟไม่นิ่ง, pipette/timing ผิด → มักแก้ด้วย repeat control
- กฎ systematic (2₂ₛ/4₁ₛ/10ₓ) → นึกถึง: น้ำยาเสื่อม/หมดอายุ, calibration drift, light source/probe เสื่อม → repeat เฉยๆ ไม่หาย → ต้อง troubleshoot/recalibrate
- sigma สูง → ใช้กฎน้อยลง: 6σ = 1₃ₛ เดี่ยว (N=2) · 5σ = 1₃ₛ/2₂ₛ/R₄ₛ · 4σ ค่อยเพิ่ม 4₁ₛ · ≤3σ ต้องเพิ่ม 8ₓ/control เยอะ

### FORK 2 — L-J shift vs trend → คนละสาเหตุ คนละการแก้
- Shift (จุดกระโดดไปอยู่ด้านเดียว mean ทันที) → เปลี่ยน lot น้ำยา/calibrator, หลัง maintenance/recalibrate → verify lot/calibration ก่อนโทษเครื่อง
- Trend (ค่อยๆ ไหลขึ้น/ลง) → น้ำยาเสื่อม, light source เสื่อม, electrode/probe ค่อยๆ ตัน → คาดการณ์ล่วงหน้าได้ อย่ารอจน reject
- IQC ผ่านสวยทุกวัน แต่ EQA fail = precise but inaccurate (bias ซ่อน) = บทเรียน Theranos. "IQC OK ≠ ผลถูก" — bias คงที่ L-J จับไม่ได้ ต้องพึ่ง EQA/method comparison

### FORK 3 — interference (HIL) กระทบ analyte ไหน → ปล่อยได้/ไม่ได้
กฎเหล็ก: interference ไม่ได้เพี้ยนทุกตัวเท่ากัน — รู้ว่ากระทบ "ตัวไหน + ทิศไหน" ก่อนตัดสินปล่อย

| ปัญหา sample | ทำเพี้ยนตัวไหน (ทิศ) | ตัดสิน |
|---|---|---|
| Hemolysis (Hb แดง รั่วจาก RBC) | K⁺ สูงปลอม, LDH/AST สูงปลอม + รบกวน absorbance | K⁺/LDH/AST จาก hemolyzed = ห้าม report → เจาะใหม่ |
| Lipemia (TG สูง ขุ่น) | รบกวน spectrophotometry → หลาย analyte เพี้ยน | repeat หลัง centrifuge/blank หรือ direct assay; flag |
| Icterus (bilirubin) | bili >10 ทำ Creatinine (Jaffe) ต่ำปลอม | สลับ enzymatic Cr / blank; flag |
| Glycolysis (แยก RBC ช้า) | glucose ต่ำปลอม | เจาะ NaF tube / แยก serum เร็ว |
| Ascorbic acid | Cr (Jaffe) −bias, glucose interference | ทราบ med history; blank |

- ก่อนสรุปว่า "เครื่องเพี้ยน" → เช็ค sample integrity ก่อนเสมอ (HIL index): ถ้า HIL จริง = ปัญหา pre-analytical ไม่ใช่เครื่อง อย่าไป recalibrate

### FORK 4 — QC พัง: recalibrate vs troubleshoot vs เปลี่ยน reagent
1. เช็คก่อน: control หมดอายุ/reconstitute ผิด? (ALP เปลี่ยน activity เร็วหลังละลาย) · vial ผิด · pipette
2. random error (1₃ₛ/R₄ₛ): repeat control 1 รอบ → หาย = ปล่อย; ไม่หาย → หาฟองอากาศ/mix/อุณหภูมิ
3. systematic / shift หลังเปลี่ยน lot: → recalibrate
4. trend ไหลลง + recalibrate ไม่อยู่: → เปลี่ยน lot reagent
5. เปลี่ยนหมดแล้วยังพัง → troubleshoot hardware → แจ้ง service
- เกณฑ์ method (sigma): <3σ = ต้อง correct/เปลี่ยน method · <2σ = เปลี่ยน technology/analyzer

### FORK 5 — ได้ค่าแล้ว: dilute / repeat / report / โทร
- เกิน linearity → dilute แล้ววัดใหม่ × dilution factor
- outlier เดี่ยว / ไม่เข้ากับ clinical → repeat ก่อน ห้าม trust ค่าแรกทันที
- critical value → (1) verify sample integrity (2) repeat (3) โทรแจ้ง ward + บันทึก ใคร/เวลา/อ่านทวน
- ผล run ที่ Westgard fail → ห้าม report ผู้ป่วยใน run นั้น จนกว่าจะแก้ QC + รัน control ผ่าน แล้ว re-run

### FORK 6 — เชื่อค่าแรกหรือ repeat?
Repeat ก่อนปล่อย เมื่อ: ค่า critical, ค่าขัด clinical/ผล panel อื่น (Cr สูงแต่ BUN ปกติ), delta check ต่างมาก, run QC borderline, มี HIL flag. Repeat ได้ค่าเดิม = เชื่อ; ต่าง = หา pre-analytical/carryover

## กับดัก (Anti-patterns)
- 🚫 report ผลจาก run ที่ Westgard FAIL — run reject = ผู้ป่วยทุกคนใน run นั้น hold; แก้ QC ก่อน
- 🚫 report K⁺ (หรือ LDH/AST) จากตัวอย่าง hemolyzed — สูงปลอม → เจาะใหม่ อย่า report
- 🚫 ไม่ flag / ไม่โทร critical value — ต้อง verify→repeat→โทร→บันทึก read-back
- 🚫 ตี 1₂ₛ เป็น reject — 1₂ₛ = warning เท่านั้น (โอกาส ~5% ออกนอก ±2SD ตามธรรมชาติ)
- 🚫 calibration drift / trend จับไม่ทัน — trend = แก้เชิงรุก. IQC ผ่าน ≠ accurate (Theranos)
- 🚫 ละเลย sample integrity — clotted / wrong tube (fluoride กับ urease-BUN ใช้ไม่ได้) / underfill / hemolyzed → อย่าโทษเครื่องแล้ว recalibrate มั่ว
- 🚫 trust outlier ไม่ repeat
- 🚫 report ค่าที่เกิน linearity โดยไม่ dilute
- 🚫 recalibrate ทันทีทุกครั้งที่ QC พัง — เช็ค control/sample/reagent expiry ก่อน
- 🚫 ลืม carryover — ตัวอย่างเข้มข้นสูงตามด้วยต่ำ → ค่าต่ำสูงปลอม; repeat

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคส QC จริงที่เจอ: Westgard ตัวไหน fire บ่อยกับ analyte ไหนในแล็บคุณ และ root cause จริงที่เจอคืออะไร
> เติม interference/wrong-tube ที่เคยพลาด: เคยปล่อยผลจาก sample ปนเปื้อนแล้วหมอ flag กลับมามั้ย แก้ระบบยังไง
> เติมเกณฑ์ critical value + read-back ของแล็บคุณ: ค่าไหนต้องโทรทันที ขั้นตอนบันทึกเป็นแบบไหน

NOTE: ความรู้พื้นฐาน (reference range, assay principles เช่น GOD-POD/Jaffe/Friedewald, TEa, sigma-DPMO) ให้ดูจาก "ตำรา/แหล่งอ้างอิงมาตรฐาน" — skill นี้เน้นการ "ตัดสินใจ" เท่านั้น

---
*skill นี้เป็นตัวช่วยคิดเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ตัดสินแทน. การตัดสิน accept/reject/report ทุกครั้งต้องเป็นไปตาม SOP + QC policy ของแล็บ และยืนยันกับ MT/ผู้มีอำนาจลงนามก่อน. ปล่อยผลผิด = รักษาผิด — ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
