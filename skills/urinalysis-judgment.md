---
skill: urinalysis-judgment
title: โค้ชยูริน + body fluid microscopy — strip↔micro↔clinical ให้ตรง (Urinalysis & Body-Fluid Judgment)
type: ADVISE               # ช่วยตัดสินใจหน้า bench ไม่ใช่ atlas ตะกอน/ผลึก
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-10-20
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
- `python scripts/fluid_calc.py tnc --cells 389 --squares 9 --sample-ul 20 --diluent-ul 80` (Neubauer: 1 ช่องใหญ่ = 0.1 µL; DF คิดจาก**ปริมาตร** ไม่รับ "1:9") · `eqa-check --reported 432 --low 1800 --high 2400 --df 5 --other A2=80-120` (หลุดช่วง → บอกว่า slip ไหนพาเข้าช่วง: ลืม/คูณ DF ซ้ำ · ×10 ห้องนับ · ×1000 หน่วย · เข้าช่วงหลอดอื่น = สลับหลอด · ค่ากำหนด 0: ≤ background limit = background, เกิน = สืบสวน) · `pd --wbc 240 --neut-pct 62` (WBC > 100 **และ** neut > 50%; 50% พอดี = `INDETERMINATE` boundary · ไม่เข้าเกณฑ์ ≠ ตัด peritonitis · PMN สูงแต่ count ต่ำ = `INDETERMINATE` ถามเวลา dwell)
- สคริปต์ = ตัวช่วยตรวจ ไม่ใช่ผู้ตัดสิน: ทุก output มีบรรทัด `ADVISORY` · ทดสอบแล้ว: `evals/test_urinalysis_tools.py` (43 ข้อ รวม must-fail control 5 ตัว: "nitrite ลบ = ไม่มี UTI", Light's ที่บังคับครบ 3 ข้อ, tnc ที่ลืม DF, eqa-check ที่ตัดการเช็คสลับหลอด, pd ที่ใช้ OR แทน AND — ต้องแดง)

## ใช้เมื่อ
- strip ↔ sediment ไม่ตรง → ตัวไหนเชื่อ? ต้อง resolve ยังไง
- เห็น RBC/WBC/cast/crystal/cell → significant หรือ artifact/contamination? ต้อง flag ไหม
- automated UA flag → ต้อง confirm ด้วยกล้องเมื่อไหร่
- ขยับไป body fluid: CSF cell count, serous transudate/exudate, synovial crystal (gout/pseudogout)
- ดูภาพ body fluid smear (EQA photo / cytospin) → เซลล์นี้คืออะไร ต้องรายงานคำไหน · นับ TNC ด้วยห้องนับ / ผล EQA นับเซลล์ตก

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
- **เครื่องหมาย birefringence ยึดฟิสิกส์ ไม่ยึดตารางสรุป**: ผลึกวางขนานแกน slow ray ของ red compensator → MSU = **เหลือง** (negative) · CPPD = **น้ำเงิน** (positive) — ตาราง/สไลด์สรุปบางชุดพิมพ์สลับ ถ้าขัดกันให้เชื่อหลักนี้ + ตำรา (กับดัก #14)
- **Peritoneal dialysate**: WBC > 100/µL **และ** neutrophil > 50% (ISPD 2022 หลัง dwell ≥ 2 ชม.; บางเอกสารเขียน ≥ 50% → 50% พอดี = boundary `INDETERMINATE` ทำตาม SOP) → สงสัย peritonitis → Gram + culture (`fluid_calc.py pd`) · count ต่ำแต่ PMN สูงใน dwell สั้น → ถามเวลา dwell · **ไม่เข้าเกณฑ์ effluent ≠ ตัด peritonitis** (ISPD: 2 ใน 3 = อาการ, effluent, culture; WBC สูงแต่ mononuclear เด่น → นึกถึง TB/เชื้อรา ส่ง culture ตาม SOP)

### Fork 6 — ภาพ smear สารน้ำ (Wright-Giemsa) → เรียกชื่อให้ตรงช่องรายงาน
ช่องรายงานแบบหนึ่งของ EQA body fluid (เช็คแบบฟอร์มของ scheme ตัวเอง): blood cells · **monocyte + macrophage (ช่องเดียว)** · mesothelial · other abnormal/unidentified + จุลชีพ · ผลึก · LE cell · กลุ่มเซลล์ผิดปกติ/N/C
1. **ตระกูล mesothelial = จุดตกอันดับ 1** (ชุด macrophage / mesothelial / reactive mesothelial = หมวดภาพที่ EQA body fluid ตกสูงสุด; AI ทำแบบปิดตาก็พลาดครบ 3/3 ข้อในแกนนี้ — n เล็ก) — คำตอบต้องมี "normal" หรือ "reactive" เสมอ ห้ามหยุดที่ "mesothelial"
   - **macrophage**: cytoplasm ฟองใส มีของกิน ขอบไม่ชัด นิวเคลียสรูปไต/เยื้อง
   - **mesothelial ปกติ**: cytoplasm ฟ้าเทา **แน่นสม่ำเสมอ**, นิวเคลียสกลมกลางเซลล์ chromatin ละเอียด, ขอบฟูจางๆ
   - **reactive**: เรียก reactive เมื่อเห็น ≥ 1: cytoplasm **2 โซน** (รอบนิวเคลียสซีด ขอบนอกฟ้าเข้ม) · ขอบเป็นขน/blebs ชัด · 2 นิวเคลียสขึ้นไป · nucleolus เห็น · ใหญ่ขึ้น — แต่ chromatin ยังเรียบ และมีตัวกลางๆ ต่อเนื่องกับตัวปกติ
   - เห็น "two-tone" แล้วอย่าเขียนแค่ "mesothelial (two-tone)" → เขียน **reactive**; กลับกัน ตัวที่ cytoplasm แน่นสม่ำเสมอ ไม่มี 2 โซน = **ปกติ** อย่าเหมา reactive
   - ⚠️ ขอบเขต: เกณฑ์ "≥ 1 ข้อ" ข้างบนจูนกับคำเฉลยภาพ EQA (ภาพเดี่ยว ต้องเลือกคำ) — ในงานจริง two-tone / ขอบขน / 2 นิวเคลียส **เดี่ยวๆ พบใน mesothelial ปกติได้** → เรียก reactive เมื่อเห็นหลายข้อร่วมกัน (ใหญ่ขึ้น + N/C สูงขึ้น + nucleolus ชัด + หลายนิวเคลียส/เป็นกลุ่ม) และใช้คำตาม SOP
2. **benign ↔ malignant — ดูนิวเคลียส ไม่ใช่ดูฟอง**: vacuole ใหญ่ดันนิวเคลียสไปขอบ + นิวเคลียส**เล็ก เข้ม เรียบ ไม่โต** = signet-ring-**like** (macrophage/mesothelial เสื่อม — **เอนไปทาง benign แต่ไม่ตัดมะเร็ง**: signet-ring carcinoma จากกระเพาะ/เต้านมแบบ lobular นิวเคลียสเล็กเรียบได้ → เจอจำนวนมาก/เป็นกลุ่ม/มี 2 ประชากร/มีประวัติ primary → atypical → cytology) · malignant signet ring = นิวเคลียส**โต** hyperchromatic ขอบไม่เรียบ ถูกดันเป็นเสี้ยว · ก้อน 3 มิติขอบโค้ง (community border) + 2 ประชากรชัด = suspicious · ไม่แน่ใจ → "atypical cells → ส่ง cytology" (ห้ามเรียกมะเร็งจาก Wright อย่างเดียว — signet-ring บน Wright-Giemsa เป็น pitfall ที่รู้กันในงาน cytology)
3. **ภาษารายงานของ MT** (ถ้อยคำตาม SOP แล็บ): มัก "atypical / abnormal cells present → refer for pathologist review" — **ไม่ตั้งชนิดมะเร็งเอง** (adenocarcinoma = งานพยาธิแพทย์) · **blast ใน CSF/สารน้ำ: รายงานว่าพบตาม SOP อย่าละไว้** แล้วส่งยืนยัน (flow/พยาธิแพทย์)
4. **phagocyte**: erythrophage (RBC ทั้งเม็ด) → siderophage (เม็ดเหล็กน้ำเงินดำ, Prussian blue +) → hematoidin (ผลึกเหลืองทอง, เหล็ก −) = ยิ่งไปขวายิ่งเก่า · erythrophagocytosis เกิดในหลอดได้ถ้าตั้งนาน · macrophage กิน WBC = เรียกชื่อ **leucophage** (อย่าแค่บรรยาย) · **LE cell** = neutrophil กินก้อนเนียนไร้ลาย vs tart cell = monocyte กินนิวเคลียสที่ยังเห็นลาย
5. **เชื้อ/ผลึก**: แบคทีเรีย**ในเซลล์** ใน specimen สด = หนุนติดเชื้อจริงมาก → ยืนยัน Gram + โทรตาม critical-value SOP (ตั้งนาน เชื้อปนโตแล้วถูกกินได้ · granule/ตะกอนสีหลอกได้) · วัตถุกลมนอกเซลล์**ชิ้นเดียว** ไม่มี budding = แยก yeast จาก platelet/คราบสีไม่ได้ → รายงาน "cannot confirm, Gram/culture" (ภาพแบบนี้คนกับ AI ตอบสวนกันได้) · ผลึกใน synovial ยืนยันด้วย polarized + compensator เสมอ
6. **mitosis ≠ มะเร็ง** — reactive mesothelial แบ่งตัวได้; ผิดรูป/หลายขั้ว/ไม่สมมาตร = suspicious

### Fork 7 — นับ TNC / ผล EQA นับเซลล์ตก (งานนับสารน้ำเทียม = จุดที่ EQA body fluid ตกบ่อยที่สุด)
- สูตร: เซลล์ที่นับ × DF ÷ (ช่องใหญ่ × 0.1 µL) — 0.1 µL/ช่องใหญ่ = improved Neubauer; ห้องนับอื่น (เช่น Fuchs-Rosenthal ลึก 0.2 mm) → ตั้ง `--depth-mm` / `--square-mm2` · /µL = /cu.mm = ×10⁶/L · รัน `fluid_calc.py tnc` แทนคิดเอง
- หลุดช่วง → `eqa-check` ก่อนโทษเครื่อง: ลืม DF · ×10 ห้องนับ · ×1000 หน่วย · **เลขเข้าช่วงหลอดอื่น = สลับหลอด** · ค่ากำหนด 0 เซลล์ + เครื่องขึ้นเลข → รัน background ก่อน: ≤ background/LoQ limit = **background count** รายงานต่ำกว่า LoQ ตาม SOP · เกิน limit ชัด = เซลล์จริง/ปนเปื้อน/carry-over/สลับหลอด → สืบสวน ห้ามรายงาน < LoQ
- ผล EQA เชิงปริมาณ (bias/SDI) + ลำดับสืบสวนก่อน CAPA → `lab-management-judgment` (`eqa_eval.py`)

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
- #11 ตอบแค่ "mesothelial" ไม่บอก normal/reactive → EQA นับผิด (Fork 6.1)
- #12 เห็นฟองใหญ่ดันนิวเคลียส → เรียก signet ring มะเร็ง โดยไม่ดูว่านิวเคลียสโตจริงไหม (Fork 6.2)
- #13 ตั้งชื่อชนิดมะเร็งเองในรายงาน body fluid → เกินหน้าที่ MT ใช้ "atypical → refer" (blast = รายงานว่าพบตาม SOP แล้วส่งยืนยัน) (Fork 6.3)
- #14 เชื่อตาราง/สไลด์สรุป (รวมที่ AI ช่วยทำ) โดยไม่เทียบตำรา — ข้อผิดที่พบได้: เครื่องหมาย birefringence สลับ (Fork 5) · เรียก lymphocyte ใน BAL ว่า "ปนเปื้อน" (lymphocyte เป็นเซลล์ประจำของ BAL; ตัวบ่งชี้ปนเปื้อนคือ squamous/bronchial epithelial cells)
- #15 คิด DF จากสตริง "1:9" / ใช้จำนวนช่องเป็นตัวหาร / ลืม background count บนตัวอย่าง 0 เซลล์ (Fork 7)

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - SOP แลบคุณกำหนด strip↔micro reflex / criteria การ confirm กล้อง / re-collect ไว้อย่างไร?
> - เครื่อง automated UA รุ่นที่ใช้ (UF-/iQ/cobas u) flag ตัวไหนที่ทีมตีความต่างจาก default?
> - reference/critical สำหรับ body fluid (CSF cell, synovial) ในแลบคุณ + ขั้นตอนส่งต่อด่วน

NOTE: knowledge (ค่าปกติ strip, รูปร่างตะกอน/ผลึกละเอียด, birefringence physics, Light's criteria สูตร) → ดู "ตำรา/แหล่งอ้างอิงมาตรฐาน" ไม่ใช่หน้าที่ของ skill นี้

---
*skill นี้เป็นตัวช่วย "คิด" เพื่อการศึกษา ไม่ใช่ตัวตัดสินใจหรือวินิจฉัยแทน · RBC cast / crystal พิษ / CSF-synovial ผิดปกติ = กระทบการดูแล ต้องดูกล้อง + correlate clinical + ยืนยันกับ MT/แพทย์ก่อนรายงาน · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
