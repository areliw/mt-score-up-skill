---
skill: clinchem-judgment
title: ตัวช่วยตัดสินใจแล็บเคมีคลินิก (Clinical Chemistry Judgment)
type: ADVISE
needs: any
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-07-03
status: draft
disclaimer: "skill นี้เป็นตัวช่วย 'คิด' สำหรับการตัดสินใจในแล็บเคมีคลินิกเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ใช่ผู้ตัดสินแทน. ปล่อยผลผิด 1 ค่า = หมอรักษาผิด 1 คน — นี่คือความปลอดภัยผู้ป่วยโดยตรง. AI ช่วยไล่ logic/Westgard/interference เท่านั้น ทุกการตัดสิน accept/reject/report ต้องเป็นไปตาม SOP + QC policy ของแล็บ และยืนยันกับ MT/ผู้มีอำนาจลงนามก่อนเสมอ. ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ตัวช่วยตัดสินใจแล็บเคมีคลินิก

ตัวช่วยตัดสินใจในแล็บเคมีคลินิก — เน้น "จะ accept/reject run นี้มั้ย", "ค่านี้ปล่อยได้มั้ย", "interference ตัวนี้ทำผลเพี้ยนตัวไหน" ไม่ใช่ที่ท่อง reference range / นิยาม analyte

> **VERDICT: เมื่อสงสัย → HOLD ก่อน report เสมอ.** เช็คตามลำดับ gate: **sample (HIL/clot/tube) → QC (Westgard) → report.** gate ใดไม่ผ่าน = ไม่ปล่อยผล.
> **กับดักอันดับ 1:** report ผลจาก run ที่ Westgard FAIL หรือจาก sample hemolyzed — ปล่อยผิด 1 ค่า = หมอรักษาผิด 1 คน.

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ
>
> ⚠️ **ขอบเขต:** ทุก cutoff/ค่าในสกิล = teaching illustration — **ค่าตัดสินจริงยึด reference range + critical-value limit + SOP ของแลบคุณ** เท่านั้น ไม่ใช่ค่ากล่อง/ตำรา

> 🛑 **RED FLAGS — เจอข้อใด = HOLD ห้ามปล่อยผล ยืนยัน QC + sample + ผู้ลงนามก่อน:** run ที่ Westgard FAIL · critical value (K⁺/glucose/Ca/troponin) · HIL กระทบ analyte (hemolysis → K⁺, lipemia, icterus) · ผลขัด delta-check/clinical ชัด · สงสัย calibration drift. — ปล่อยผิด 1 ค่า = รักษาผิด 1 คน

> **ตอบคำถามจริงก่อน — คงคำเตือน/เซฟตี้ไว้เสมอ:** ตอบสิ่งที่ถามตรงๆ ก่อน แล้วดึงเฉพาะ fork/กับดักที่เกี่ยวข้องมาเสริม · **อย่า dump ทุก fork/checklist** กับคำถามง่าย (definition / แปล / เทียบ / "อันนี้แปลว่าอะไร") — ใช้ framework เต็ม (sample→QC→report) เฉพาะเมื่อเป็นคำถาม accept/reject/report/repeat/dilute/โทร หรือข้อมูลที่ให้ trigger safety gate จริง · ข้อควรระวังด้านความปลอดภัย (Westgard fail, HIL, critical value, reject sample, calibration drift ฯลฯ) ที่เกี่ยวกับเคสตรงหน้า **ต้องคงไว้เสมอ ไม่ตัดออกเพื่อความสั้น**

## ใช้เมื่อ
- ดู QC แล้วต้องตัดสิน accept หรือ reject run · Westgard ตัวไหน fire · L-J chart shift/trend แปลว่าอะไร
- เจอ sample hemolyzed/lipemic/icteric/clotted → ปล่อยผลได้มั้ย ตัวไหนเชื่อไม่ได้
- ได้ค่า critical / outlier / เกิน linearity → dilute / repeat / โทร หรือ report
- เลือกทาง recalibrate vs troubleshoot vs เปลี่ยน lot น้ำยา เมื่อ QC พัง
- เครื่องหลักล่ม / โหลดถล่ม → triage STAT, เปิด backup/ส่งต่อ, แจ้ง delay ยังไง
- (สาย sales/IVD) คุยภาษา sigma/TEa/QC กับ lab head ให้ตรงประเด็น

## วิธีใช้
วาง skill นี้ + ข้อมูล QC/sample/ค่าที่ได้ (control values, L-J pattern, สภาพตัวอย่าง, ค่าที่สงสัย) → AI ไล่ fork ตามลำดับ gate (sample → QC → report) แล้วบอกว่าควร accept/reject/repeat/dilute/โทร พร้อมเหตุผลและกับดักที่ต้องระวัง

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### FORK 1 — accept หรือ reject run? Westgard ตัวไหน fire
**Verdict: 1₂ₛ = warning อย่าเพิ่ง reject; เจอ 1₃ₛ/2₂ₛ/R₄ₛ/4₁ₛ/10ₓ = REJECT.** (modern multirule บางที่ตัด 1₂ₛ ทิ้ง เริ่มที่ 1₃ₛ เลย) ถ้าเกิน ±2SD ให้ไล่กฎ reject ต่อ:

| เห็นอะไร | กฎ | error | ตัดสิน |
|---|---|---|---|
| 1 ค่าเกิน ±2SD (ไม่เข้ากฎอื่น) | 1₂ₛ | — | warning เท่านั้น → ปล่อยได้ (อย่า reject ทันที = false reject ~5%) |
| 1 ค่าเกิน ±3SD | 1₃ₛ | random | REJECT |
| 2 ค่าติดกันเกิน +2SD (หรือ −2SD) ด้านเดียว | 2₂ₛ | systematic | REJECT |
| ค่าหนึ่ง >+2SD อีกค่า <−2SD ใน run เดียว (ห่าง >4SD) | R₄ₛ | random | REJECT |
| 4 ค่าติดกันเกิน ±1SD ด้านเดียว | 4₁ₛ | systematic | REJECT (ตัดเป็น warning ได้เฉพาะเมื่อ method sigma สูง + ออกแบบ QC plan ไว้ล่วงหน้า ไม่ใช่ดุลพินิจหน้างาน) |
| 10 ค่าติดกันอยู่ด้านเดียวของ mean | 10ₓ | systematic | REJECT (ตัดเป็น warning ได้เฉพาะเมื่อ method sigma สูง + ออกแบบ QC plan ไว้ล่วงหน้า ไม่ใช่ดุลพินิจหน้างาน) |

- กฎ random (1₃ₛ/R₄ₛ) → นึกถึง: ฟองอากาศ, mix ไม่ทั่ว, อุณหภูมิ/ไฟไม่นิ่ง, pipette/timing ผิด → มักแก้ด้วย repeat control
- กฎ systematic (2₂ₛ/4₁ₛ/10ₓ) → นึกถึง: น้ำยาเสื่อม/หมดอายุ, calibration drift, light source/probe เสื่อม → repeat เฉยๆ ไม่หาย → ต้อง troubleshoot/recalibrate
- sigma สูง → ใช้กฎน้อยลง: 6σ = 1₃ₛ เดี่ยว (N=2) · 5σ = 1₃ₛ/2₂ₛ/R₄ₛ · 4σ ค่อยเพิ่ม 4₁ₛ · ≤3σ ต้องเพิ่ม 8ₓ/control เยอะ

### FORK 2 — L-J shift vs trend → คนละสาเหตุ คนละการแก้
**Verdict: Shift = สงสัย lot/calibration; Trend = สงสัยน้ำยา/ชิ้นส่วนเสื่อม. IQC ผ่านสวยทุกวันก็ยัง bias ได้ — ต้องพึ่ง EQA.**
- Shift (จุดกระโดดไปอยู่ด้านเดียว mean ทันที) → เปลี่ยน lot น้ำยา/calibrator, หลัง maintenance/recalibrate → verify lot/calibration ก่อนโทษเครื่อง
- Trend (ค่อยๆ ไหลขึ้น/ลง) → น้ำยาเสื่อม, light source เสื่อม, electrode/probe ค่อยๆ ตัน → คาดการณ์ล่วงหน้าได้ อย่ารอจน reject
- IQC ผ่านสวยทุกวัน แต่ EQA fail = precise but inaccurate (bias ซ่อน) = บทเรียน Theranos. "IQC OK ≠ ผลถูก" — bias คงที่ L-J จับไม่ได้ ต้องพึ่ง EQA/method comparison
- ⚠️ **เงื่อนไขที่ทำให้ FORK นี้ทำงานจริง = traceability:** จะแยก shift/trend → root cause (lot ใหม่? recal? น้ำยาขวด/cartridge ใหม่?) ได้ ต้องรู้ว่า **อะไรเปลี่ยนวันไหน** — แต่หน้าจอเครื่อง + middleware/3rd-party หลายที่ **ไม่ได้เก็บ/ไม่ sync ครบ** (lot ของ QC, รหัสขวด/cartridge/pack หรือ S/N น้ำยา current/standby, วัน cal, วันปรับ lab-mean มักหลุด → ต้องวนกลับไปกดหน้าเครื่อง) → ควรมี **record ของตัวเอง** (sheet/LIS) ที่ผูกแต่ละจุด QC กับ lot · รหัสขวด/cartridge/pack (S/N) · วัน cal · วันเปลี่ยน lab-mean/SD; ไม่มี annotation นี้ = เห็น shift แต่สืบ root-cause + ทำ CAPA ไม่ได้ · ⚠️ **คิดสถิติให้คงฐานเดียว:** mean/SD/CV เปลี่ยนตามวิธีคิด (per-lot vs per-S/N vs pooled, ตัด ±2SD หรือไม่) — เลือกฐานแล้วอย่าสลับกลางคัน (เทียบข้ามฐาน = หลอกตัวเอง)

### FORK 3 — interference (HIL) กระทบ analyte ไหน → ปล่อยได้/ไม่ได้
**Verdict: hemolyzed → ห้าม report K⁺/LDH/AST (สูงปลอม) เจาะใหม่. เช็ค HIL index ก่อนโทษเครื่อง.** interference ไม่ได้เพี้ยนทุกตัวเท่ากัน — รู้ "ตัวไหน + ทิศไหน" ก่อนตัดสินปล่อย

| ปัญหา sample | ทำเพี้ยนตัวไหน (ทิศ) | ตัดสิน |
|---|---|---|
| Hemolysis (Hb แดง รั่วจาก RBC) | K⁺ สูงปลอม, LDH/AST สูงปลอม + รบกวน absorbance | K⁺/LDH/AST จาก hemolyzed = ห้าม report → เจาะใหม่ |
| Lipemia (TG สูง ขุ่น) | รบกวน spectrophotometry → หลาย analyte เพี้ยน | repeat หลัง centrifuge/blank หรือ direct assay; flag |
| Icterus (bilirubin) | Creatinine (Jaffe) ต่ำปลอม (เริ่มได้ตั้งแต่ ~2 mg/dL, แรงขึ้นเมื่อสูง) | สลับ enzymatic Cr / blank; flag (enzymatic ก็ไม่ immune 100%) |
| Glycolysis (แยก RBC ช้า) | glucose ต่ำปลอม | เจาะ NaF tube / แยก serum เร็ว |
| Ascorbic acid | Cr (Jaffe) −bias, glucose interference | ทราบ med history; blank |

- ก่อนสรุปว่า "เครื่องเพี้ยน" → เช็ค sample integrity ก่อนเสมอ (HIL index): ถ้า HIL จริง = ปัญหา pre-analytical ไม่ใช่เครื่อง อย่าไป recalibrate

### FORK 4 — QC พัง: recalibrate vs troubleshoot vs เปลี่ยน reagent
**Verdict: อย่า recalibrate เป็นรีเฟล็กซ์ — เช็ค control/sample/reagent expiry ก่อน. random→repeat control; systematic/shift→recalibrate; trend ไม่อยู่→เปลี่ยน lot; หมดทาง→service.**
1. เช็คก่อน: control หมดอายุ/reconstitute ผิด? (ALP เปลี่ยน activity เร็วหลังละลาย) · vial ผิด · pipette
2. random error (1₃ₛ/R₄ₛ): repeat control 1 รอบ → หาย = ปล่อย; ไม่หาย → หาฟองอากาศ/mix/อุณหภูมิ
3. systematic / shift หลังเปลี่ยน lot: → recalibrate
4. trend ไหลลง + recalibrate ไม่อยู่: → เปลี่ยน lot reagent
5. เปลี่ยนหมดแล้วยังพัง → troubleshoot hardware → แจ้ง service
- เกณฑ์ method (sigma): <3σ = ต้อง correct/เปลี่ยน method · <2σ = เปลี่ยน technology/analyzer

### FORK 5 — ได้ค่าแล้ว: dilute / repeat / report / โทร
**Verdict: critical value → verify→repeat→โทร→บันทึก read-back เสมอ. เกิน linearity → dilute. run Westgard fail → ห้าม report.**
- เกิน linearity → dilute แล้ววัดใหม่ × dilution factor
- outlier เดี่ยว / ไม่เข้ากับ clinical → repeat ก่อน ห้าม trust ค่าแรกทันที
- critical value → (1) verify sample integrity (2) repeat (3) โทรแจ้ง ward + บันทึก ใคร/เวลา/อ่านทวน
- ผล run ที่ Westgard fail → ห้าม report ผู้ป่วยใน run นั้น จนกว่าจะแก้ QC + รัน control ผ่าน แล้ว re-run

### FORK 6 — เชื่อค่าแรกหรือ repeat?
**Verdict: สงสัย = repeat ก่อนปล่อย. ได้ค่าเดิม = เชื่อ; ต่าง = หา pre-analytical/carryover.**
Repeat ก่อนปล่อย เมื่อ: ค่า critical, ค่าขัด clinical/ผล panel อื่น (Cr สูงแต่ BUN ปกติ), delta check ต่างมาก, run QC borderline, มี HIL flag. Repeat ได้ค่าเดิม = เชื่อ; ต่าง = หา pre-analytical/carryover

### FORK 7 — เครื่องหลักล่ม / โหลดถล่ม: triage STAT + backup/ส่งต่อ (operational continuity)
**Verdict: จัดลำดับตาม downtime/STAT SOP + ความเสี่ยงทางคลินิก (critical/STAT ก่อน routine) — แต่ห้ามข้าม QC/ID/comparability/การแจ้งที่ต้องทำ · เปิด backup/manual ได้เฉพาะที่ "run QC ผ่าน (+ รู้ comparability ตาม SOP)" · แจ้ง ward เชิงรุกเรื่อง delay — อย่าเงียบ.** (เป็นการ "เดินงานต่อ" ตอนเครื่องล่ม ไม่ใช่การ accept/reject run ปกติ — FORK 1)
- **triage:** ทุ่มกำลังที่ critical/STAT ก่อน (เช่น K⁺/glucose/blood gas/troponin) → routine เลื่อนได้ตามเกณฑ์ SOP/แพทย์ · งานที่ผูกธนาคารเลือด = ประสานตาม SOP BB (โยง `bloodbank-judgment`)
- **backup analyzer / method สำรอง:** ใช้ได้ก็ต่อเมื่อ **run QC ผ่านบนเครื่องสำรอง** + (ตาม SOP) รู้ว่าผล comparable กับเครื่องหลัก — คนละเครื่อง/method = calibration/reference อาจต่าง → อย่าปล่อยผลข้ามเครื่องโดยไม่ดู comparability + ใส่หมายเหตุ method ตาม SOP
- **manual/visual method สำรอง:** มักช้ากว่า/precision ต่างกัน (method-specific) → ใช้เฉพาะ method ที่ verified/กำหนดใน SOP + ระบุ method ที่ใช้
- **ส่งต่อ (send-out/refer):** เมื่อ backup ก็ทำไม่ได้ → label/transport/แจ้ง TAT ที่ต่างไป (ผลอาจคนละ unit/method)
- **สื่อสารเชิงรุก:** แจ้ง ward/แพทย์ว่า delay + ค่าไหนยัง report ได้/ไม่ได้ — แจ้งให้รู้ทัน (โยง `interprofessional-communication-judgment`; "เร็ว" = แจ้งข่าว delay ทันเวลา **ไม่ใช่ลัด QC/ID**) · downtime ต้อง document
- **เครื่องกลับมา:** อย่า dump backlog ทันที → **run QC ผ่านก่อน** + reconcile งาน pending/STAT ที่ค้าง

## กับดัก (Anti-patterns)
- 🚫 report ผลจาก run ที่ Westgard FAIL — run reject = ผู้ป่วยทุกคนใน run นั้น hold; แก้ QC ก่อน
- 🚫 report K⁺ (หรือ LDH/AST) จากตัวอย่าง hemolyzed — สูงปลอม → เจาะใหม่ อย่า report
- 🚫 ไม่ flag / ไม่โทร critical value — ต้อง verify→repeat→โทร→บันทึก read-back
- 🚫 ตี 1₂ₛ เป็น reject — 1₂ₛ = warning เท่านั้น (โอกาส ~5% ออกนอก ±2SD ตามธรรมชาติ; modern multirule บางที่ตัด 1₂ₛ ทิ้ง เริ่มที่ 1₃ₛ)
- 🚫 calibration drift / trend จับไม่ทัน — trend = แก้เชิงรุก. IQC ผ่าน ≠ accurate (Theranos)
- 🚫 ละเลย sample integrity — clotted / wrong tube (fluoride กับ urease-BUN ใช้ไม่ได้) / underfill / hemolyzed → อย่าโทษเครื่องแล้ว recalibrate มั่ว
- 🚫 trust outlier ไม่ repeat
- 🚫 report ค่าที่เกิน linearity โดยไม่ dilute
- 🚫 recalibrate ทันทีทุกครั้งที่ QC พัง — เช็ค control/sample/reagent expiry ก่อน
- 🚫 ลืม carryover — ตัวอย่างเข้มข้นสูงตามด้วยต่ำ → ค่าต่ำสูงปลอม; repeat
- 🚫 เครื่องล่มแล้วปล่อยผลจาก backup/manual โดยไม่ run QC + ไม่ดู comparability ข้ามเครื่อง
- 🚫 ทำ routine ก่อน critical/STAT ตอนกำลังจำกัด · เงียบไม่แจ้ง ward เรื่อง delay · dump backlog ตอนเครื่องกลับมาโดยไม่ run QC ก่อน · เร่ง STAT จนลัด QC/ID/comparability (เร่งได้แต่ห้ามข้ามด่าน)
- 🚫 (AI) over-trigger — ถามง่ายๆ ทีเดียวแต่ dump ทั้ง 7 fork/checklist จนคำตอบจริงจม → ตอบตรงคำถามก่อน ดึงเฉพาะ fork ที่เปลี่ยนการตัดสินใจ (คำเตือนเซฟตี้ที่เกี่ยวกับเคสยังต้องคงไว้)

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคส QC จริงที่เจอ: Westgard ตัวไหน fire บ่อยกับ analyte ไหนในแล็บคุณ และ root cause จริงที่เจอคืออะไร
> เติม interference/wrong-tube ที่เคยพลาด: เคยปล่อยผลจาก sample ปนเปื้อนแล้วหมอ flag กลับมามั้ย แก้ระบบยังไง
> เติมเกณฑ์ critical value + read-back ของแล็บคุณ: ค่าไหนต้องโทรทันที ขั้นตอนบันทึกเป็นแบบไหน

NOTE: ความรู้พื้นฐาน (reference range, assay principles เช่น GOD-POD/Jaffe/Friedewald, TEa, sigma-DPMO) ให้ดูจาก "ตำรา/แหล่งอ้างอิงมาตรฐาน" — skill นี้เน้นการ "ตัดสินใจ" เท่านั้น

---
*skill นี้เป็นตัวช่วยคิดเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ตัดสินแทน. การตัดสิน accept/reject/report ทุกครั้งต้องเป็นไปตาม SOP + QC policy ของแล็บ และยืนยันกับ MT/ผู้มีอำนาจลงนามก่อน. ปล่อยผลผิด = รักษาผิด — ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
