---
skill: urinalysis-judgment
title: โค้ชยูริน + body fluid microscopy — strip↔micro↔clinical ให้ตรง (Urinalysis & Body-Fluid Judgment)
type: ADVISE               # ช่วยตัดสินใจหน้า bench ไม่ใช่ atlas ตะกอน/ผลึก
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-10-08
status: draft
disclaimer: "ช่วยคิดงานตรวจปัสสาวะ/น้ำในร่างกายเพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รักษา และไม่ตัดสินใจแทน · ทุกผลที่กระทบการรักษา (RBC cast, crystal พิษ, CSF cell) ต้องดูด้วยกล้อง + correlate clinical + ทำตาม SOP/reference ของแล็บ + ยืนยันกับ MT/แพทย์ก่อนรายงานเสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชยูริน + body fluid microscopy

ตัวช่วยตัดสินใจงานตรวจปัสสาวะ + น้ำในร่างกาย (CSF/serous/synovial) — เน้น "ผล strip/sediment นี้ ต้องทำอะไรต่อ + อย่าพลาดตรงไหน" ไม่ใช่ atlas รูปตะกอน/ตารางผลึก

> **กฎ #1:** strip กับกล้อง **ต้อง correlate กัน** — strip บวก/ลบ ไม่ตรง sediment = ต้อง resolve ก่อน report. flag จากเครื่อง automated (UF/iQ) = สัญญาณ ไม่ใช่คำตอบ
> **กับดัก #1 (ขั้น hard):** **nitrite negative ไม่ตัด UTI** — เชื้อที่ไม่สร้าง nitrate reductase (Enterococcus, Staph, Pseudomonas, Acinetobacter) หรือปัสสาวะค้างใน bladder ไม่นานพอ → nitrite ลบทั้งที่ติดเชื้อ. และ leukocyte esterase ลบได้ใน early/neutropenia. **strip ลบ ≠ ปกติ** → ดู micro + บริบทเสมอ

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## เครื่องมือ (รันก่อนคิดเลข)
ไล่ strip ↔ sediment ↔ specimen หรือคิด Light's / CSF / synovial → **รันสคริปต์ก่อน แล้วค่อยใช้ fork ข้างล่างตีความ** (อย่าไล่กฎด้วยตาเอง) · รัน `--help` ก่อน ไม่ต้องอ่านซอร์ส · ไฟล์อยู่ใน `scripts/` ของโฟลเดอร์ skill (ใน repo: `skills/urinalysis-judgment/scripts/`) · สคริปต์ไม่ได้ "ดูกล้อง" แทนคน — มันเช็ค logic ของสิ่งที่คนอ่านมาแล้ว
- `python scripts/ua_reconcile.py --blood 2+ --rbc 0 --rbc-max <ของแล็บ> --nitrite neg --le 1+ --wbc 25 --wbc-max <ของแล็บ> --bacteria many --ph 7.8 --crystal uric-acid --cast rbc --age-h 1` → รายการ finding เรียงตามระดับ `HOLD` (ต้อง resolve ก่อน report) / `RECOLLECT` / `FLAG` / `CAUTION` / `INFO` พร้อม fork ที่มา + บรรทัด `STATUS` · ครอบคลุม: กฎ 2 ชม./แช่เย็น, blood+ ไม่มี RBC, LE↔WBC ไม่ตรง, **nitrite ลบไม่เคยถูกตีว่า "ไม่มี UTI"**, SSA เมื่อสงสัย myeloma, squamous เยอะ/ประจำเดือน → re-collect, RTE, cast ที่ต้อง flag, crystal↔pH, Ca oxalate + AKI = ethylene glycol · ไม่ใส่ `--rbc-max/--wbc-max` = นับ ">0 ต่อ HPF" ว่า "เห็น" (สคริปต์บอกไว้)
- `python scripts/fluid_calc.py lights --fluid-protein --serum-protein --fluid-ldh --serum-ldh --ldh-uln <ของแล็บ>` (exudate ถ้าเข้า ≥1 ข้อ; เตือนว่าเกณฑ์นี้มาจาก pleural — ascites ใช้ตาม SOP) · `csf --tube1-rbc --tube3-rbc [--minutes-to-count]` (RBC ลดข้ามหลอด = หนุน traumatic tap แต่ **ไม่ตัด SAH**) · `synovial --shape needle --birefringence negative` (MSU/CPPD; ไม่เข้าคู่ = ให้เช็คใหม่)
- สคริปต์ = ตัวช่วยตรวจ ไม่ใช่ผู้ตัดสิน: ทุก output มีบรรทัด `ADVISORY` · ทดสอบแล้ว: `evals/test_urinalysis_tools.py` (22 ข้อ รวม must-fail control 2 ตัว: "nitrite ลบ = ไม่มี UTI" และ Light's ที่บังคับครบ 3 ข้อ — ต้องแดง)

## ใช้เมื่อ
- strip ↔ sediment ไม่ตรง → ตัวไหนเชื่อ? ต้อง resolve ยังไง
- เห็น RBC/WBC/cast/crystal/cell → significant หรือ artifact/contamination? ต้อง flag ไหม
- automated UA flag → ต้อง confirm ด้วยกล้องเมื่อไหร่
- ขยับไป body fluid: CSF cell count, serous transudate/exudate, synovial crystal (gout/pseudogout)

## วิธีใช้
วาง skill นี้ + ผล strip + sediment (หรือ flag เครื่อง / ชนิด fluid) ที่กำลังตัดสินใจ → AI เดินตาม fork บอก "ทำอะไรต่อ + กับดักตรงไหน" แล้วชี้กลับให้คนดูกล้อง + correlate clinical + ยืนยันเอง

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### ก่อนแปลผลเสมอ — ดู 3 อย่าง
1. ตัวอย่าง OK มั้ย — midstream clean-catch? ตรวจภายใน **2 ชม.** (หรือแช่ 2–8°C)? ตั้งทิ้งนาน = cast สลาย, bacteria โต, pH↑ (urea→ammonia), cell/glucose สลาย, crystal ตกใหม่
2. ชนิด specimen ตรงงาน — random (screen) · first-morning (concentration/protein/HCG) · 24h (quantitative) · catheter/supra (ตีความ contamination ต่างกัน)
3. correlate strip ↔ sediment ↔ บริบทคน (อายุ/เพศ/ประจำเดือน/ยา/ไข้)

### Fork 1 — strip บวก/ลบ "ไม่ตรง" sediment → resolve ก่อน report
- **blood บวก แต่ไม่เห็น RBC** → hemoglobinuria (hemolysis) หรือ myoglobinuria (rhabdo) — ไม่ใช่เลือดออก. แยกด้วยบริบท + plasma สี/CK
- **protein บวก** → strip จับ **albumin เด่น** (ไม่จับ Bence-Jones/globulin) → สงสัย myeloma/light chain ต้อง **SSA หรือ electrophoresis** ไม่ใช่ strip
- **nitrite ลบ / LE ลบ แต่สงสัย UTI** → ดู micro (WBC/bacteria) + ส่ง culture; อย่าตัดด้วย strip (กับดัก #1)
- **glucose บวกแต่เลือดปกติ** → renal glycosuria/ตั้งครรภ์; **ketone** → DKA/อดอาหาร/low-carb
- **SG**: strip ผิดที่ pH สูง/protein; **refractometer แม่นกว่า** แต่ glucose/radiocontrast/mannitol ดัน SG refractometer สูงปลอม
- **pH > 8** → มักเก็บนานเกิน/Proteus (urease); pH กับ crystal สัมพันธ์กัน (ใช้ช่วยแยกผลึก)

### Fork 2 — Sediment cells → significant vs contamination
- **RBC**: dysmorphic/acanthocyte → glomerular; isomorphic → lower tract/stone/tumor. ผู้หญิงมีประจำเดือน = contamination → re-collect
- **WBC (pyuria)**: ติดเชื้อ; **sterile pyuria** (WBC+ culture−) → คิด TB, chlamydia/GC, ติดเชื้อที่รักษาแล้ว, นิ่ว, interstitial nephritis
- **Epithelial**: **squamous เยอะ = contamination** (re-collect midstream); **renal tubular epithelial (RTE) = significant** (ATN/active injury) — อย่าสับสน 2 อย่างนี้
- **Bacteria/yeast**: correlate กับ WBC + ความสด; ตั้งนาน bacteria โตเอง = ปลอม

### Fork 3 — Casts = "ปักหมุดว่ามาจากไต" → อันไหนต้อง flag
- hyaline — benign (ขาดน้ำ/ออกกำลัง/ไข้) · **RBC cast = glomerulonephritis → flag** · **WBC cast = pyelonephritis/interstitial nephritis** · granular/**muddy brown = ATN** · waxy/broad = renal failure เรื้อรัง · fatty (+oval fat body, Maltese cross) = nephrotic
- หลัก: เห็น cast = localize ไปไต; RBC/WBC/muddy-brown cast = กระทบการดูแล → flag + correlate

### Fork 4 — Crystals → normal vs pathologic (ผูกกับ pH)
- กรด: uric acid · calcium oxalate (มีได้ทุก pH; **envelope/needle + AKI → สงสัย ethylene glycol poisoning** = ฉุกเฉิน เชื่อม `toxicology-judgment`)
- ด่าง: triple phosphate/struvite (coffin-lid, Proteus), amorphous phosphate
- **always pathologic**: cystine (hexagonal → cystinuria), tyrosine/leucine (liver), cholesterol, **drug crystals** (sulfa/acyclovir/indinavir → ประวัติยา)
- artifact: amorphous, talc, starch, fiber — อย่ารายงานเป็นผลึกโรค

### Fork 5 — Body fluids (ขยายจากปัสสาวะ)
- **CSF**: นับ cell **ทันที** (เซลล์สลายเร็ว) · **xanthochromia → หนุน SAH** — แต่ดูจาก **supernatant ที่ปั่นทันที** (ตั้ง whole specimen ค้าง → RBC แตก in vitro = xanthochromia ปลอม) · **RBC ลดข้าม tube 1→3 → หนุน traumatic tap** (ไม่ใช่เกณฑ์เด็ดขาด — **clearing ไม่ตัด SAH**, SAH จริงอาจมี traumatic tap ซ้อนได้) · ส่ง chem (glucose ratio CSF/serum, protein) + micro/Gram คู่
- **Serous (pleural/peritoneal)**: transudate vs exudate ตัดสินด้วย **Light's criteria** (เป็น chem ไม่ใช่ cell) → ชี้ทางก่อนแปล cell
- **Synovial ใต้ polarized light**: **MSU = เข็ม, negatively birefringent = gout** · **CPPD = rhomboid, positively birefringent = pseudogout** · correlate cell count + Gram (septic = ฉุกเฉิน)

## กับดัก (Anti-patterns)
- #1 ตั้ง UA ทิ้งนานก่อนตรวจ → cast สลาย/bacteria โต/crystal ตกใหม่ → ตรวจภายใน 2 ชม. หรือแช่เย็น
- #2 เหมา nitrite/LE ลบ = ไม่มี UTI → พลาด Enterococcus/Staph/early infection
- #3 รายงาน squamous (contamination) ปนเป็น significant → ควร re-collect; แยก RTE ออก
- #4 พลาด RBC cast / muddy-brown cast → พลาด GN/ATN ที่ต้อง flag
- #5 calcium oxalate + AKI ไม่คิดถึง ethylene glycol → พลาดพิษที่ต้อง antidote ด่วน
- #6 blood strip บวก = เลือดออกเสมอ → จริงๆ อาจ hemoglobin/myoglobin (ไม่เห็น RBC)
- #7 protein strip ลบ = ไม่มี protein → strip ไม่จับ Bence-Jones; สงสัย myeloma ใช้ SSA/electrophoresis
- #8 เชื่อ automated flag โดยไม่ confirm กล้องในเคสที่กระทบการดูแล
- #9 CSF/synovial ปล่อยตั้งนานก่อนนับ → cell สลาย/นับเพี้ยน
- #10 อ่าน crystal โดยไม่ดู pH + ไม่แยก artifact → รายงานผลึกผิด

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - SOP แลบคุณกำหนด strip↔micro reflex / criteria การ confirm กล้อง / re-collect ไว้อย่างไร?
> - เครื่อง automated UA รุ่นที่ใช้ (UF-/iQ/cobas u) flag ตัวไหนที่ทีมตีความต่างจาก default?
> - reference/critical สำหรับ body fluid (CSF cell, synovial) ในแลบคุณ + ขั้นตอนส่งต่อด่วน

NOTE: knowledge (ค่าปกติ strip, รูปร่างตะกอน/ผลึกละเอียด, birefringence physics, Light's criteria สูตร) → ดู "ตำรา/แหล่งอ้างอิงมาตรฐาน" ไม่ใช่หน้าที่ของ skill นี้

---
*skill นี้เป็นตัวช่วย "คิด" เพื่อการศึกษา ไม่ใช่ตัวตัดสินใจหรือวินิจฉัยแทน · RBC cast / crystal พิษ / CSF-synovial ผิดปกติ = กระทบการดูแล ต้องดูกล้อง + correlate clinical + ยืนยันกับ MT/แพทย์ก่อนรายงาน · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
