---
skill: clinical-correlation-judgment
title: โค้ชอ่านผลแล็บข้ามแขนง — correlate + ตั้ง DDx ชี้ทางให้แพทย์ (Clinical Correlation Judgment)
type: ADVISE
needs: any
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-10-08
status: draft
disclaimer: "เครื่องมือช่วยคิดเชิงวินิจฉัยจากผลแล็บข้ามแขนงเพื่อการศึกษา — ช่วยคิด ไม่ใช่คำสั่งทางการแพทย์และไม่ตัดสินใจแทน การตีความผลแล็บกระทบการวินิจฉัยและรักษาผู้ป่วยโดยตรง ต้องยืนยันกับ MT/แพทย์ผู้ดูแล + ทำตาม SOP และตำรา/แหล่งอ้างอิงมาตรฐานเสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชอ่านผลแล็บข้ามแขนง — correlate + ตั้ง DDx ชี้ทางให้แพทย์

ตัวช่วยอ่านผลแล็บข้ามแขนง (hema + chem + micro + immuno + blood-bank) แล้วร้อยเรื่องเป็นภาพเดียว → **ตั้ง DDx + ชี้ทาง + flag ให้แพทย์** — เน้น **วิธีคิดเชื่อมโยงผล + กับดักที่ทำให้พลาด** ไม่ใช่ท่องค่า

> 🎯 **กฎ #1: ก่อนเชื่อค่าใดๆ เช็ค clinical context + pre-analytical ก่อน** (อายุ/อาการ/ยา + hemolysis/clot/tube ผิด) — "ตัวเลขลอยไม่มีคนไข้ = อ่านผิด" แล้วร้อยค่าผิด *ทุกตัว* ให้อธิบายได้ด้วย **กลไกเดียว**
> 🚩 **กับดัก #1: anchoring** — อย่า lock ธงแรก. บังคับตั้ง DDx ≥3 + สั่ง test ที่ *หักล้าง* DDx อื่น (ไม่ใช่แค่ยืนยันของตัวเอง). ค่าเดี่ยว positive ≠ diagnosis → confirm เสมอ
> ⚠️ **ขอบเขต: MT ไม่วินิจฉัย** — MT correlate/flag + ชี้ทาง reflex test + ส่งต่อ; **วินิจฉัยเป็นหน้าที่แพทย์**

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## เครื่องมือ (รันก่อนคิดเลข)
แยกทาง anemia / อ่าน DB/TB / ตรวจ worksheet ก่อน lock คำตอบ → **รันสคริปต์ก่อน แล้วค่อยใช้ fork ข้างล่างตีความ** · รัน `--help` ก่อน ไม่ต้องอ่านซอร์ส · ไฟล์อยู่ใน `scripts/` ของโฟลเดอร์ skill (ใน repo: `skills/clinical-correlation-judgment/scripts/`)
- `python scripts/pivot_check.py anemia --mcv 66 --ferritin N --hba2 5.2` — MCV → branch (micro/normo/macro) → iron pattern จาก **flag ของแล็บเอง** (`L/N/H` เทียบ reference range ของแล็บ ไม่มีช่วงค่าฝังในสคริปต์) → ferritin ปกติใน microcytic = ห้ามหยุดที่ IDA · HbA2 ≥ 3.5% = pattern β-thal trait + เตือน KLF1 · พิมพ์ DDx ที่ต้องเปิดไว้เสมอ (กัน anchoring)
- `python scripts/pivot_check.py jaundice --db 2.9 --tb 5.0` — คิด DB/TB แล้ววางบน heuristic **ทั้ง 3 แหล่ง** (การ์ดนี้ · 505402 §5.3 · 510416 §2) · แหล่งขัดกัน/ตกช่องว่าง = `SOURCES DISAGREE` → ตัดสินด้วย enzyme pattern + clinical ไม่ใช่ ratio (เช่น DB/TB 0.58 ของเคส DILI ใน 510416 ตกช่อง post-hepatic ตาม heuristic ของการ์ด)
- `python scripts/ddx_check.py worksheet.json` — ตรวจ worksheet ตาม § ผลงานที่ต้องส่ง: กฎเหล็ก 4 ข้อ · DDx ≥ 3 + test หักล้างทุกตัว · ruled-out ต้องมีหลักฐาน · ห้ามประกาศ exclusion ขณะยังมี DDx เปิด · screen บวกต้องมี confirm · ถ้อยคำแบบ "วินิจฉัย" = เตือน (MT ไม่วินิจฉัย)
- hs-troponin delta (0h→1h) → คิดด้วย `scripts/delta_check.py` ของ `result-release-judgment` โดยใส่ delta limit ของ assay/SOP เอง
- สคริปต์ = ตัวช่วยตรวจ ไม่ใช่ผู้ตัดสิน: ทุก output มีบรรทัด `ADVISORY` · วินิจฉัยเป็นหน้าที่แพทย์ · ทดสอบแล้ว: `evals/test_clinical_correlation_tools.py` (23 ข้อ รวม must-fail control: ใช้ DB/TB cutoff ชุดเดียวเป็นค่าตายตัว และยอมให้ DDx ตัวเดียว — ต้องแดง)

## ใช้เมื่อ
- มีผลแล็บหลายตัว/หลายแขนงในผู้ป่วยคนเดียว → "ค่าไหนชี้ทางไหน → DDx → ตัดออกจนเหลือคำตอบ"
- ฝึก case study / ตอบสอบ integrate / งานวิจัย · ถาม "ค่านี้ใช่โรคจริงหรือ artifact?"
- เตือนตัวเองก่อนสรุป/ชี้ทาง (ส่งต่อแพทย์): เช็ค trap list ด้านล่าง

## วิธีใช้
วาง skill นี้ + เล่าเคส (ผลแล็บที่ได้ + อายุ/เพศ/อาการ/ประวัติ) → AI ชี้ "ค่าไหน pivotal → ชี้ทางไหน → reflex test อะไร" + กับดักที่ทำให้พลาด

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### กฎเหล็กก่อนสรุป/ชี้ทางเสมอ — ถาม/เช็ค 4 อย่าง
1. **Clinical context คืออะไร** (อายุ/เพศ/อาการ/ประวัติยา/ประวัติเดินทาง/โรคประจำตัว) — ตัวเลขลอยไม่มีคนไข้ = อ่านผิด
2. **ตัวอย่างถูกต้องไหม (pre-analytical):** hemolysis? clot? heparin tube กับ PCR? เก็บผิดเวลา? → ถ้าสงสัย ขอ recollect ก่อนเชื่อค่า
3. **ค่าผิดปกติเด่น (pivotal) คือตัวไหน** + มัน "ชี้ทางเดียว" หรือ "ชี้หลายทาง" (ต้อง reflex test เพิ่ม)
4. **ยา/ภาวะที่รบกวนผลได้** (anti-CD38, biotin, autoAb, ภาวะ in-vivo) — interference ≠ โรค

### Fork 1 — เบาะแส lab ตัวไหน → ชี้ทางไหน (pivotal value → DDx branch)
- **MCV เป็นแยกแรกของ anemia:** <80 microcytic → iron study; >100 macrocytic → B12/folate; normo → retic/hemolysis
- **iron study 4 ตัวรวมกัน ตัดสินทิศ:** ferritin↓ + TIBC↑ + %sat↓ = IDA แท้ → ต้องหา **แหล่งเสียเลือด** ต่อ (เช่น CT เจอ leiomyoma) · ถ้า ferritin ปกติ ในคน microcytic → **ห้ามหยุดที่ IDA** → reflex Hb typing/DNA
- **AST/ALT vs ALP/GGT = แยก liver pattern:** transaminase >>300 = hepatocellular (เช่น DILI); ALP/GGT เด่น = cholestatic · ⚠️ **albumin↓ + AST/ALT ปกติ ≠ ตัดตับออก** — cirrhosis ชดเชย ~37-48% LFT ปกติ; albumin↓ = ตับ (synthetic fail) / ไตรั่ว / ทุพโภชนาการ-อักเสบ → แยกด้วย PT/INR + GGT/ALP + urinalysis (RBC cast = glomerular)
- **conjugated fraction (DB/TB) แบ่งดีซ่าน (heuristic สอน ไม่ใช่ cutoff ตายตัว — ขอบเบลอ/ทับซ้อน, ตำราใช้ 15–30% ก็มี):** ~<20% = pre-hepatic (unconjugated) / ~20–50% = hepatocellular / ~>50% = post-hepatic (obstructive) · ต้องดู pattern + clinical ประกอบเสมอ
- **TSH ต่ำ + FT3/FT4 สูง = thyrotoxic** → fork สำคัญคือ RAIU + thyroglobulin: ทั้งคู่ต่ำ + autoAb ลบ = hormone จากภายนอก (factitia) ไม่ใช่ Graves
- **panreactive ทุก cell ที่ AHG** (auto+screen+unit 1+) + ประวัติยา → คิด drug interference (anti-CD38/daratumumab) **ก่อน** alloantibody
- **cardiac:** อ่าน delta (0h→1h) ของ hs-troponin ไม่ใช่ค่าเดี่ยว — single value ปกติไม่ตัด MI

### Fork 2 — rule-out DDx ทีละตัว (diagnosis of exclusion)
ใช้เมื่อ pivotal value ชี้หลายทาง ลำดับ: **viral → autoimmune → metabolic → toxin/drug → "เหลือคำตอบเดียว"**
- DILI: ตัด viral/autoimmune/Wilson/acetaminophen/pregnancy หมด → เหลืออาหารเสริม (usnic acid)
- factitia: ตัด Graves/thyroiditis ด้วย RAIU+Tg → เหลือ exogenous hormone
- **กฎ:** อย่าประกาศ "diagnosis of exclusion" จนกว่าจะ **ตัดตัวที่ treatable/อันตรายกว่าออกก่อน**

### Fork 3 — เมื่อไหร่ต้อง reflex / confirm test เพิ่ม
- **screening positive ≠ จบ → ยืนยันเสมอ:** micro = culture → Gram → biochemical → AST (disk+MIC) → resistance gene · serology = Ag/NS1 (acute) ตามด้วย PCR ยืนยัน serotype
- **iron ปกติในคน microcytic** → reflex Hb typing → ถ้า typing งง/A2A สูงโดยไม่เข้า thal → NGS (เจอ KLF1)
- **smear เจอ blast** → reflex BM + immunophenotyping (TdT/CD19 = Pre-B-ALL) + cytogenetic บอก prognosis
- **plasma cell + M-protein** → reflex β2-MG, Bence Jones, CD138; ถ้ามีอาการ CNS → body fluid (CSF) จับ relapse

### Fork 4 — pre-analytical / artifact ก่อนเชื่อค่า (ค่าผิด = artifact ไม่ใช่โรค)
- **specimen/tube ผิด:** heparin tube ห้ามใช้กับ RT-PCR → ผลลบเทียม
- **in-vivo/in-vitro interference:** serum GM false-negative ใน non-neutropenic → ต้องส่ง tracheal aspirate/BDG เสริม · daratumumab ทำ AHG panreactive → ไม่ใช่ alloAb
- **biology ของค่า:** วัด 25(OH)D (half-life ยาว = สถานะจริง) ไม่ใช่ 1,25(OH)₂D (อาจปกติทั้งที่ขาด)
- **ถ้าค่าวิกฤตขัดกับคนไข้** (เช่น Hb 1.4 แต่คนยังเดินได้) → ยืนยัน + ดู clinical (มี flow murmur จริง = anemia จริง)

### Fork 5 — เขียน cause→effect chain (เชื่อม lab ให้เป็นเรื่องเดียว)
แทนที่จะ list ค่าผิดทีละตัว → ร้อยเป็น flow: **trigger → mechanism → lab abnormality → clinical sign**
- ตัวอย่าง: แยกตัว → แดด/อาหารน้อย → 25(OH)D↓ → Ca ดูดซึม↓ → Ca↓ → secondary hyperPTH (iPTH↑) → bone resorption↑ (CTx/NTx↑) → Trousseau/Chvostek+ / QT ยาว
- **ทุกค่าผิด อธิบายได้ด้วยกลไกเดียว = ชี้ทางแน่น (ส่งต่อแพทย์วินิจฉัย)**

---

## กับดัก (Anti-patterns) — เช็คทุกเคสก่อน lock
- **Anchoring** — ติดธงแรกแล้วไม่ดู alternative · ก่อน lock IDA ในคน microcytic ต้องเช็ค ferritin (ดูเหมือน thal แต่จริงเป็น KLF1) · บังคับตัวเองตั้ง DDx ≥3 ก่อนเลือก
- **เชื่อ single test ไม่ cross-check** — screen/serology/typing ตัวเดียว positive ≠ diagnosis · ต้อง confirm (culture, PCR, biopsy, NGS) · serum GM ลบ แต่ BDG+culture บวก → อย่าตัดจากค่าเดียว
- **ละเลย pre-analytical / interference** — heparin+PCR, daratumumab+AHG, hemolysis ดัน K⁺/LDH · เห็นค่าแปลก "เกินคนไข้" → สงสัย artifact ก่อนสร้างโรคใหม่
- **ตัวเลขลอย ไม่ดู clinical context** — albumin ต่ำ → ตับหรือไต? ต้องดู AST/ALT + urinalysis (red cell cast = glomerular)
- **Miss zebra ที่ pattern ชัด** — panreactive AHG → นึก anti-CD38; thyrotoxic + RAIU ต่ำ → นึก factitia ไม่ใช่ Graves อัตโนมัติ; coinfection (dengue+COVID)
- **Confirmation bias** — สั่งเฉพาะ test ที่ยืนยันสมมติฐานตัวเอง · ต้องสั่ง test ที่ **หักล้าง DDx อื่น** ด้วย (rule-out cascade)
- **ไม่ดู progression/timing** — micro→macroalbuminuria, NS1 (≤7วัน) vs IgM/IgG, troponin delta
- **ตัด hemolysis/B12/folate ไม่ครบ** ก่อนสรุป anemia type (เช็ค bilirubin/haptoglobin/LDH/B12/folate หมดก่อน)

## Quick reference — 8 reasoning patterns
| Pattern | สาระสั้น |
|---|---|
| Microcytic anemia workup | MCV<80 → iron study → iron ปกติ? → Hb typing/DNA |
| Rule-out cascade | ตัด viral/AI/metabolic/toxin จนเหลือ 1 |
| Jaundice by DB/TB | pre / intra / post-hepatic (heuristic, ขอบเบลอ — ดู clinical ประกอบ) |
| Enzyme → liver pattern | AST/ALT=hepatocellular · ALP/GGT=cholestatic · alb↓+enzyme ปกติ → อย่าตัดตับ (cirrhosis/synthetic) vs ไต/อักเสบ |
| Serology timing | Ag/NS1=acute · IgM/IgG=primary/secondary · PCR=ยืนยัน+serotype |
| Confirmatory cascade (micro) | culture→Gram→biochem→AST(MIC)→resistance gene |
| Hormone source localization | RAIU+Tg+autoAb แยก endo vs exo |
| BB interference recognition | panreactive AHG + ยา → drug interference |

## ผลงานที่ต้องส่ง
เมื่อ output เป็น **คำตอบ case study / ข้อสอบ integrate / บันทึกส่งต่อแพทย์** — เขียนเป็น worksheet นี้ (คีย์ตรงกับ `scripts/ddx_check.py`; ตัวอย่างเต็ม: `data/worksheet_example.json`)

| ส่วน | เขียนอะไร |
|---|---|
| `context` | อายุ/เพศ/อาการ/ยา/ประวัติ (กฎเหล็ก 1) |
| `preanalytical` | เช็คตัวอย่างแล้วเจออะไร (กฎเหล็ก 2) |
| `pivotal` | ค่าเด่น + ชี้ทางเดียวหรือหลายทาง (กฎเหล็ก 3) |
| `interference` | ยา/ภาวะที่รบกวนผล (กฎเหล็ก 4) |
| `ddx` (≥ 3) | ชื่อ · สถานะ open/leading/ruled-out · test ที่หักล้างหรือยืนยันได้ · หลักฐาน (บังคับเมื่อ ruled-out) |
| `screens` | screen ที่บวก → confirmatory test |
| `chain` | trigger → mechanism → lab → clinical sign (Fork 5) |
| `conclusion` | "ผลเข้าได้กับ / ชี้ทาง ... แนะนำ reflex test ... ส่งต่อแพทย์" — ไม่ใช่ "วินิจฉัยว่า" |

นิยามเสร็จ: `python scripts/ddx_check.py worksheet.json` ขึ้น `DONE (no FAIL)` · WARN ที่เหลือ (ไม่มี chain / ถ้อยคำแบบวินิจฉัย) แก้แล้วหรือมีเหตุผล · ทุก DDx ที่ตัดออกอ้างหลักฐานจริง ไม่ใช่ความรู้สึก

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริงที่เคยร้อยผลแล็บข้ามแขนงได้/พลาด เช่น:
> - *"เคสที่ค่า pivotal ดูชี้ทางหนึ่ง แต่ reflex test กลับพลิกเป็นอีกโรค คือ..."*
> - *"เคสที่เกือบสรุปผิดเพราะ artifact/interference จับได้เพราะ..."*
> - *"pattern ข้ามแขนงที่เจอบ่อยในแล็บผม + วิธีร้อยให้เป็นเรื่องเดียว..."*

---
*เครื่องมือช่วยคิดเชิงวินิจฉัยจากผลแล็บข้ามแขนงเพื่อการศึกษา — ช่วยคิด ไม่ใช่คำสั่งทางการแพทย์และไม่ตัดสินใจแทน การตีความผลแล็บกระทบการวินิจฉัยและรักษาผู้ป่วยโดยตรง ต้องยืนยันกับ MT/แพทย์ผู้ดูแล + ทำตาม SOP และตำรา/แหล่งอ้างอิงมาตรฐานเสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
