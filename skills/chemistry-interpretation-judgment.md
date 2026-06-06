---
skill: chemistry-interpretation-judgment
title: โค้ชแปลผลเคมีคลินิก — เลือก marker + อ่าน pattern (Clinical Chemistry Interpretation Judgment)
type: ADVISE               # ช่วยแปลผล/เลือก marker ไม่ใช่ตำราค่า analyte
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดแปลผลเคมีคลินิกเพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รักษา — MT ตีความ/flag/ส่งต่อ การวินิจฉัยเป็นหน้าที่แพทย์ · ทุกผลต้อง correlate clinical + ทำตาม SOP/reference range ของห้องแล็บ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชแปลผลเคมีคลินิก — เลือก marker + อ่าน pattern

ค่าเคมีออกมาแล้ว "แปลว่าอะไร + เลือก marker/สูตรไหนเมื่อไหร่" แบบ organ-system ไม่ใช่ท่องค่า analyte (= commodity ดูตำรา)

> **กฎ #1 — อ่าน pattern + correlate clinical ก่อนเชื่อเลขเดี่ยว:** ค่าแปลกสวนอาการ = สงสัย interference/method (HIL/paraprotein/drug) ก่อน อย่าเพิ่งรายงาน · อ่าน LFT/bilirubin/cardiac/ABG เป็นชุด ไม่ใช่ทีละตัว
> **กับดัก #1 — เชื่อเลขปลอมแล้วรายงาน:** รายงาน **K⁺ critical จากตัวอย่าง hemolyzed** (สูงปลอม) · เชื่อ **troponin↑ = MI** (ไตวาย/sepsis ก็ขึ้น — ต้องดู delta + EKG) · **Cr ปกติ = ไตปกติ** ในคนแก่/cirrhosis
> นี่คือชั้น "ค่าออกมาแล้วแปลผล" — ส่วน QC/accept-reject run/Westgard ดู `clinchem-judgment` · ร้อยผลข้ามแขนง → ตั้ง DDx → ส่งต่อแพทย์ ดู `clinical-correlation-judgment`
> ⚠️ MT ตีความ/flag/ชี้ทาง — **การวินิจฉัยเป็นหน้าที่แพทย์**

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- อ่าน LFT/renal/cardiac/ABG/tumor marker แล้วต้องบอก pattern + ขั้นถัดไป
- เลือก marker/สูตร (eGFR ตัวไหน · marker หัวใจตามเวลา · tumor marker ใช้/ไม่ใช้)
- ค่าแปลกสวนอาการ → สงสัย interference (HIL/paraprotein/drug/method)
- (สาย sales) เข้าใจ "method matters" → คุย lab ลูกค้า (ดู `ivd-sales-judgment`)

## วิธีใช้
วาง skill นี้ + ค่าที่เจอ + clinical → AI ชี้ pattern + marker/สูตรที่เหมาะ + interference ที่ต้องตัดออกก่อนเชื่อค่า

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — Tumor marker: ใช้/ไม่ใช้เมื่อไหร่
- ⚠️ **ไม่ใช่ screening คนทั่วไป** (sens+spec ต่ำ → false +/− ท่วม) · gold standard diagnosis = **histology** · marker ส่วนใหญ่ใช้ **monitor/recurrence/prognosis** ไม่ใช่จับมะเร็งครั้งแรก
- benign ที่ดันค่าสูงปลอม (กับดัก): PSA↔prostatitis/BPH · AFP↔cirrhosis/ตั้งครรภ์ · CEA↔**สูบบุหรี่**/IBD · CA125↔**ประจำเดือน/ตั้งครรภ์/endometriosis** · β-hCG↔ตั้งครรภ์
- กฎสั่ง: **ห้ามเชื่อค่าเดียว** · **serial = assay/kit/ห้องเดิม** (assay ต่าง → ค่าต่าง) · ดู **half-life** (hCG เร็วสุด · PSA หลัง radiotherapy ช้าหลายเดือน) — ลดช้ากว่าคาด = residual/ดื้อยา · screen เฉพาะ high-risk (HBV/cirrhosis → AFP+US)

### Fork 2 — Renal: เลือก marker + สูตร
- **BUN↑เดี่ยว** (Cr ปกติ) → prerenal/dehydration/**GI bleed**/high-protein/steroid · **BUN+Cr↑** → GFR ลดจริง · BUN:Cr >20 = prerenal/GI bleed
- **CrCl (24h urine)** กับดัก: เก็บไม่ครบ (urine Cr ควร ~ชาย 18.5–25 · หญิง 15–20 mg/kg/day; ต่ำกว่า ~15 มาก = under-collect) · GFR ต่ำมาก → tubule หลั่ง Cr → **CrCl overestimate**
- **eGFR (serum Cr):** **CKD-EPI 2021 (race-free) = default ทุกช่วง GFR** · MDRD = legacy · Cockcroft-Gault (ปรับยา) · gold จริง = inulin (ไม่ routine)
- ⚠️ **Cr ปกติ ≠ ไตปกติ:** glomerulus เสีย <25% Cr ยังปกติ · **คนแก่** muscle↓ ชน GFR↓ หักล้าง · **cirrhosis** สร้าง creatine น้อย → Cr ต่ำปลอม eGFR สูงเกินจริง → ใช้ **cystatin C** (ไม่ขึ้น muscle)
- **Jaffe vs enzymatic:** Jaffe ถูกแต่ interference เยอะ — positive chromogen (glucose/protein/vit C/ASA/ceph/ketone) **↑Cr ปลอม → UNDERestimate GFR** (เกินจริงว่าไตเสีย); bilirubin **↓Cr → overestimate GFR** → ใช้ **enzymatic creatinine** คำนวณ GFR

### Fork 3 — LFT: อ่าน pattern อย่าอ่านทีละตัว
- จัดกลุ่ม: **hepatocellular** (AST/ALT) · **cholestatic** (ALP/GGT/5'-NT) · **synthetic** (albumin/PT) · **excretion** (bilirubin)
- **AST:ALT ratio:** ตับเจ็บทั่วไป ALT>AST · **≥2:1 = alcoholic** (GGT/ALP หนุน; **AST>500 ในคนดื่ม = ผิดปกติ หาเหตุอื่น** alcoholic มัก <300)
- **DB/TB ratio** (ตัวตัดสิน bilirubin; % = สัดส่วน direct/conjugated): <20% (ส่วนใหญ่ unconjugated) → **hemolysis/Gilbert** (prehepatic) · >70% conjugated → **cholestasis/obstruction** · 30-60% mixed → hepatitis/cirrhosis
- **ALP สูง → ตับหรือกระดูก?** confirm ด้วย GGT/5'-NT (สูงคู่=ตับ; ปกติ=กระดูก)
- **PT prolong → ตับหรือ vit K?** ฉีด vit K ดีขึ้น = **cholestasis** (ดูดซึมไม่ได้); ไม่ดีขึ้น = **hepatocellular** (สร้าง factor ไม่ได้)
- ⚠️ **ischemic hepatitis "shock liver":** AST/ALT พุ่ง >2000 แต่ลงเร็วใน 1 สัปดาห์ (low-flow: HF/shock/sepsis) — เลขน่ากลัวแต่ self-limited อย่าตื่น

### Fork 4 — Cardiac marker: timing คือทุกอย่าง
| marker | ขึ้นหลังเจ็บอก | คงอยู่ | บทบาท/กับดัก |
|---|---|---|---|
| **Myoglobin** | 1-3 h (เร็วสุด) | สั้น | early, spec ต่ำ; **ห้ามใช้ในไตวาย** (สูงปลอม) |
| **CK-MB mass** | 3-6 h | 2-3 วัน | ดู **re-infarction** ดี; index (MB×100/CK) <~2.5% skeletal · >5% cardiac · 2.5–5% ก้ำกึ่ง (lab-dependent; รอง troponin) |
| **cTnI/cTnT** | 3-7 h | 7-14 วัน | **definitive** (sens+spec สูงสุด) + risk stratify |
- ⚠️ **troponin↑ ≠ MI เสมอ** (ไตวาย/sepsis/PE/HF/exercise) → ดู **rise/fall (delta 0h/1h) + clinical + EKG** · **BNP/NT-proBNP = heart failure** ไม่ใช่ MI

### Fork 5 — Acid-base/ABG: 5 ขั้น + anion gap
1. pH → acidosis/alkalosis · 2. PCO2 (↑=resp acid) · 3. HCO3⁻ (↓=metabolic acid) · 4. ตัวที่ไปทางเดียวกับ pH = สาเหตุ (CO2→resp / HCO3→metabolic) · 5. compensation (un/partial/full)
- **Metabolic acidosis → AG = (Na+K)−(Cl+HCO3):** **high AG** = DKA/lactic/renal/toxin (methanol/glycol/salicylate) · **normal AG (hyperchloremic)** = diarrhea/RTA/CA-inhibitor
- **Metabolic alkalosis:** urine Cl<10 = **saline-responsive** (vomit/NG/diuretic) · >20 = **saline-resistant** (mineralocorticoid excess)
- ⚠️ **calculated SO2 จาก ABG ผิด** ถ้ามี COHb/MetHb → ต้อง **co-oximeter** (วัดจริง) ไม่ใช่คำนวณจาก PO2
- ⚠️ **ABG pre-analytical (เช็คก่อนเชื่อค่า):** ฟองอากาศ/สัมผัสอากาศ → **pO₂↑ pCO₂↓ pH↑** · ทิ้งนานไม่แช่เย็น (เซลล์ยังใช้ O₂) → **pO₂↓ pCO₂↑ pH↓** · ต้องกันด้วย **heparin (balanced/dried) ไม่ใช่ NaF** · ไม่รีบวัด = แช่น้ำแข็ง

### Fork 6 — Interference (HIL/paraprotein/drug): ตัดออกก่อนเชื่อค่า
- **Hemolysis:** K⁺↑ (intracellular ~40×), LDH/AST/phosphate↑ → **อย่ารายงาน K critical จากตัวอย่าง hemolyzed**
- **Lipemia:** **pseudo-hyponatremia** (indirect ISE), รบกวน 340nm → fast 12h / clear ก่อนวัด
- **Icterus:** bilirubin รบกวน assay ที่ใช้ H₂O₂
- **Paraprotein:** ⚠️ **ตาไม่เห็น (gross ปกติ)** แต่รบกวน → สงสัยเมื่อค่าแปลกในผู้ป่วย myeloma
- **Drug method-dependent:** Jaffe Cr ↑ (ceph/ASA/vit C) · ดู `clinchem-judgment` สำหรับ HIL index/QC angle
> หลัก "method matters" — ค่าแปลกสวน clinical → สงสัย interference ก่อนเชื่อ/ก่อนรายงาน

### Fork 7 — Protein electrophoresis (SPEP) + lipid: อ่าน pattern
- **SPEP region (จาก anode):** prealbumin (malnutrition ไว) · albumin (↓ inflammation/liver/nephrotic/malnutrition) · **α1** (α1-antitrypsin — ขาด→emphysema; AFP) · **α2** (**haptoglobin ↓ = hemolysis**; α2-macroglobulin↑ nephrotic; ceruloplasmin↓ Wilson) · **β** (**transferrin** — แยก anemia DDx; C3/C4) · **γ** (immunoglobulin)
- **pattern ที่ต้องอ่าน:** **polyclonal gammopathy** (γ กว้าง = infection/chronic inflammation) vs **monoclonal (M-spike/paraprotein = แหลมเดียว)** → **สงสัย multiple myeloma** → confirm **immunofixation (IFE)** + free light chain (ดู `immunoassay-judgment`) · TP↑ dehydration/myeloma · TP↓ liver/nephrotic
- 🩸 **haptoglobin ↓ = hemolysis marker** (โยง transfusion reaction/hemolytic anemia); transferrin/iron = anemia DDx
- **Friedewald LDL = TC − HDL − TG/5** ⚠️ **TG > 400 = ห้ามใช้เด็ดขาด** → direct LDL · แต่ >400 เป็น **เพดานล่าง ไม่ใช่ใบรับรองว่าต่ำกว่านี้แม่น** — underestimate เริ่มตั้งแต่ TG ~150 (+ ใช้ไม่ได้กับ non-fasting/type III) → LDL ต่ำๆ ที่ TG ปานกลางก็พลาดได้

---

## กับดัก (Anti-patterns)
- **ใช้ tumor marker screen คนทั่วไป** / เชื่อค่าเดียว / serial คนละ assay
- **troponin↑ = MI เสมอ** — ดู delta + clinical (ไตวาย/sepsis/PE ก็ขึ้น)
- **Cr ปกติ = ไตปกติ** ในคนแก่/cirrhosis — ใช้ eGFR/cystatin C
- **รายงาน K สูงจากตัวอย่าง hemolyzed** (สูงปลอม → critical ปลอม)
- **ตื่นกับ ischemic hepatitis** AST/ALT >2000 ที่ self-limited
- **ตัด DKA เพราะ urine ketone ลบ** (early DKA β-OHB เด่น; dipstick จับ acetoacetate)
- **เชื่อ calculated SO2** เมื่อมี CO/MetHb — ต้อง co-oximeter
- **อ่าน LFT/bilirubin ทีละตัว** แทน pattern (DB/TB + AST:ALT + GGT)
- **มองข้าม M-spike (monoclonal)** บน SPEP — แหลมเดียว = สงสัย myeloma → IFE confirm; haptoglobin↓ = hemolysis อย่ามองข้าม
- **ใช้ Friedewald LDL เมื่อ TG > 400** — ผิด ต้อง direct LDL (และอย่าวางใจค่าต่ำกว่า 400 เต็มร้อย — underestimate ตั้งแต่ ~150)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT chem) เคสที่ค่าแปลกเพราะ interference ... จับได้เพราะ..."*
> - *"reference range / method ของแล็บผม (Jaffe vs enzymatic, hs-troponin cutoff) คือ..."*
> - *"pattern LFT/ABG ที่ผมเคยอ่านพลาด คือ..."*

---
*ช่วยคิดแปลผลเคมีคลินิกเพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รักษา — MT ตีความ/flag/ส่งต่อ การวินิจฉัยเป็นหน้าที่แพทย์ · ทุกผลต้อง correlate clinical + ทำตาม SOP/reference range ของห้องแล็บ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
