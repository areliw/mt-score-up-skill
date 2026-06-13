---
skill: research-design-judgment
title: โค้ชออกแบบวิจัย — เลือก design + กัน bias/confounder (Research Design Judgment)
type: ADVISE               # ช่วยตัดสินใจออกแบบวิจัย ไม่ใช่ตำราระเบียบวิธี
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: semi-stable
disclaimer: "ช่วยคิดออกแบบวิจัยเพื่อการศึกษา ไม่ใช่ที่ปรึกษาวิจัย/จริยธรรมทางการ — design/ethics ต้องผ่านอาจารย์ที่ปรึกษา + IRB/EC จริงเสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชออกแบบวิจัย — เลือก design + กัน bias/confounder

วาง R2R/thesis แล้วต้องตัดสิน "ใช้ design ไหน · ข้อมูลชนิดอะไร · bias/confounder ตรงไหน · ผ่าน IRB ยัง" → โค้ชนี้ช่วยเลือก + เลี่ยงกับดักที่ reviewer ตีกลับ

> **กฎ #1: เลือก design จากคำถาม ไม่ใช่จากความสะดวก** — outcome หายาก→case-control · exposure หายาก→cohort · "สัมพันธ์มั้ย ณ จุดเดียว" + เวลาจำกัด→cross-sectional · จะพิสูจน์ causation→ต้อง RCT. **กับดัก #1: ตีความ association เป็น causation** — cross-sectional/observational บอกได้แค่ "associated with" ห้ามเขียน "ทำให้/causes" และต้องคุม confounder (stratify/regression) ก่อนเชื่อความสัมพันธ์ใดๆ. และ **ห้ามเก็บข้อมูลคนก่อนผ่าน IRB** — ไม่มีเลข approval = ตีพิมพ์ไม่ได้ + ผิดกฎหมาย.
> reviewer reject ส่วนใหญ่ไม่ใช่ "คำนวณผิด" แต่เพราะ design/bias/causation/ethics ที่ตัดสินผิด **ก่อนเก็บข้อมูล** — skill นี้เก็บการตัดสินใจช่วงนั้น
> ตั้งโจทย์ → `r2r-research-proposal` · หา N → `sample-size-power` · เลือก test → `choose-stat-test` · รัน/แปลผล → `r2r-stats` · เขียนเล่ม → `manuscript-judgment`

## ใช้เมื่อ
- จะวางโครงวิจัย/thesis → เลือก study design
- กังวล bias / confounder / validity
- ต้องเตรียม IRB/consent ก่อนเก็บตัวอย่าง
- นิยามตัวแปร (operational definition) + ชนิดข้อมูล → กำหนดทิศสถิติ

## วิธีใช้
วาง skill นี้ + เล่าคำถามวิจัย + ข้อมูลที่จะเก็บ → AI ชี้ design + bias ที่ต้องระวัง + วิธีคุม confounder + gate ethics

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — Descriptive vs Analytic (จุดแยกแรก)
- **Descriptive** = "มีเท่าไหร่ / เป็นยังไง" (prevalence, distribution, allele frequency) — เน้น*บรรยาย* (มี hypothesis เชิงประมาณค่า/เทียบเกณฑ์ได้ แต่ไม่ใช่การทดสอบความสัมพันธ์ exposure↔outcome แบบ analytic)
- **Analytic** = ทดสอบความสัมพันธ์ exposure ↔ outcome (มี hypothesis test) — งานที่ตีพิมพ์ดีมักเป็น analytic
> H0 (ไม่ต่าง/ไม่สัมพันธ์) vs H1 (ต่าง/สัมพันธ์) · test ได้แค่ **reject / fail to reject H0** ไม่เคย "ยอมรับว่า H1 จริง" (กับดักภาษาที่ reviewer จับ) · **default two-tailed** (one-tailed เพื่อให้ p ผ่านง่าย = p-hacking) · ⚠️ "fail to reject" ≠ "พิสูจน์ว่าไม่ต่าง" — อาจแค่ **power ต่ำ/N น้อย**; รายงาน CI ของ effect ไม่ใช่สรุปว่า "ไม่มีผล"

### Fork 2 — เลือก study design ตามคำถาม
| คำถามแบบ | design | หมายเหตุ |
|---|---|---|
| ความชุก/ค่าปกติเท่าไหร่ | **Cross-sectional (descriptive)** | survey, ถูก/เร็ว |
| exposure สัมพันธ์ outcome มั้ย (วัดพร้อมกัน) | **Cross-sectional analytic** | default ของงานเทียบ genotype↔phenotype; วัดครั้งเดียว |
| คนเป็นโรค vs ไม่เป็น ต่างที่ exposure มั้ย | **Case-control** (เลือกตาม *outcome* แล้วมองย้อน exposure — มัก retrospective แต่นิยามจาก sampling ไม่ใช่ทิศเวลา) | ดีเมื่อ **outcome หายาก** |
| exposure → outcome ตามเวลามั้ย | **Cohort** (ตั้งกลุ่ม *at-risk* → จำแนก/วัด exposure → ตามดู outcome ตามเวลา; prospective *หรือ* historical/retrospective) | ดีเมื่อ **exposure หายาก**; แพง/นาน |
| intervention/ยา ได้ผลมั้ย | **RCT** | gold standard causation; randomize + control — *causal ไม่จำกัดแค่ RCT: observational + วิธี causal (ปรับ confounder/propensity) อนุมานได้ภายใต้สมมติฐานชัด* |
- rule: outcome หายาก → case-control · exposure หายาก → cohort · อยากรู้ "สัมพันธ์มั้ย ณ จุดเดียว" + เวลาจำกัด (thesis 1-2 ปี) → cross-sectional

### Fork 3 — ชนิดตัวแปร (scale) → กำหนดทิศสถิติ
- scale ชี้ **test ที่พบบ่อย**: **Nominal** (หมู่เลือด/genotype/เพศ) → สัดส่วน/chi-square (หรือ logistic) · **Ordinal** → median/non-parametric (หรือ ordinal regression) · **Interval/Ratio** (ต่อเนื่อง) → t/ANOVA/Pearson · ⚠️ **"parametric" = สมมติรูป distribution ไม่ได้ผูกกับ scale** (logistic/Poisson บน categorical/count ก็ parametric) → เลือกจริงต้องเช็ค assumption ของ *model นั้น* ไม่ใช่แค่ดู scale (ดู `choose-stat-test`)
- ระบุ **independent (exposure)** vs **dependent (outcome)** · เลือก test ลึก → `choose-stat-test`
- **operational definition:** นิยามทุกตัวแปรให้วัดซ้ำได้ (เช่น cutoff ของ "ค่าสูง", coding ของ genotype, นิยาม carrier) — ไม่นิยาม = reviewer ตีกลับ · ⚠️ อย่า **dichotomize** ต่อเนื่องเป็น 2 กลุ่มถ้าไม่จำเป็น (เสีย info; เลือก cutoff ทีหลังให้ p สวย = p-hacking)

### Fork 4 — Validity / Reliability + Bias
- **Validity** = วัดสิ่งที่ตั้งใจวัดจริงไหม · **Reliability** = วัดซ้ำได้ค่าเดิมไหม (precision; CV ของเครื่องแล็บ = ตัววัด reliability) · reliable แต่ไม่ valid = แม่นแต่ผิดเป้า
- **Selection bias:** sample ไม่เป็นตัวแทน (convenience/volunteer/snowball เสี่ยงสูง) · **Volunteer bias:** คนอาสา ≠ คนไม่อาสา
- งานที่เก็บจากตัวอย่างที่มีอยู่ (residual/donor) มัก convenience → **เขียน limitation selection bias ตรงๆ + เกณฑ์ inclusion/exclusion ให้ชัด**

### Fork 5 — Confounder → คุมยังไง (กับดักยอดฮิตที่ reject genomics paper)
- confounder = ตัวแปรที่สัมพันธ์กับทั้ง exposure และ outcome แต่ไม่ใช่ตัวกลางในเส้นทาง → ทำให้ association เป็น "ของปลอม"
- ⚠️ อย่าคุม **mediator** (ตัวกลางบนเส้นทาง exposure→outcome) แบบเดียวกับ confounder — adjust ตัวกลาง = **over-adjustment** บัง effect จริงที่ควรเห็น (คุม confounder เท่านั้น ไม่ใช่ทุกตัวที่สัมพันธ์)
- ตัวอย่าง: ในงานหา genotype↔phenotype ของ thalassemia/HbF → **α-thalassemia co-inheritance, อายุ, เพศ** เป็น confounder ต่อ HbF
- คุมด้วย: **restriction / matching (ตอน design)** หรือ **stratify / multivariable regression (ตอนวิเคราะห์)** — ระบุวิธีคุมตั้งแต่ proposal

### Fork 6 — Ethics / IRB gate (ก่อนเก็บข้อมูลเสมอ)
- งานในมนุษย์ **ต้องผ่าน IRB/EC ก่อนเก็บ** — ไม่มีเลข approval = ตีพิมพ์ไม่ได้ + ผิดกฎหมาย
- **Informed consent** (เป็นลายลักษณ์): วัตถุประสงค์ + ความเสี่ยง + สิทธิถอนตัว · หลัก 3: respect (autonomy), beneficence (ประโยชน์>เสี่ยง), justice
- ใช้เลือด/DNA/ข้อมูลพันธุกรรม = **sensitive data** → IRB + consent + **PDPA (de-identify)** · residual sample ก็มักต้องขอ waiver/approval

---

## กับดัก (Anti-patterns)
- **ตีความ cross-sectional เป็น causation** — วัดพร้อมกันบอก "associated with" เท่านั้น อย่าเขียน "ทำให้/causes"
- **confounder ไม่คุม** → association ปลอม (α-thal/อายุ/เพศ ฯลฯ); คุม stratify/regression
- **selection bias** — convenience/volunteer แล้วอ้าง generalize; เขียน limitation + inclusion/exclusion
- **design ไม่ตรงคำถาม** — เอา cross-sectional ตอบคำถาม temporality, ใช้ case-control กับ outcome ไม่หายาก
- **เลือก scale/ชนิดข้อมูลผิด** → เลือก stat ผิดทั้ง chain (เอา nominal ไปหา mean)
- **dichotomize / one-tail / เลือก cutoff ทีหลัง** เพื่อให้ p สวย = p-hacking → ตั้ง hypothesis + analysis plan ก่อนเก็บ
- **ไม่มี IRB/consent** → เก็บตัวอย่างคนไข้โดยไม่ผ่านจริยธรรม = ตีพิมพ์ไม่ได้ + ผิด PDPA

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT R2R) งานที่ผมเลือก design... เพราะ outcome/exposure มันลักษณะ..."*
> - *"confounder ที่ reviewer ในสายผมจับบ่อย คือ... คุมโดย..."*
> - *"IRB ที่ รพ./คณะ เรา ใช้เวลา... ต้องเตรียม..."*

---
*ช่วยคิดออกแบบวิจัยเพื่อการศึกษา ไม่ใช่ที่ปรึกษาวิจัย/จริยธรรมทางการ — design/ethics ต้องผ่านอาจารย์ที่ปรึกษา + IRB/EC จริงเสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
