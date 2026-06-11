---
skill: molecular-judgment
title: โค้ช Molecular Dx — เลือก method/แปลผล/กัน false (Molecular Diagnostics Judgment)
type: ADVISE               # ช่วยตัดสินใจหน้างาน molecular ไม่ใช่ตำรา PCR
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดเลือก method/แปลผล molecular เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รักษา — งานวินิจฉัยระดับโมเลกุลกระทบการรักษาผู้ป่วยโดยตรง ต้องตาม SOP + validation ของแล็บ และยืนยันกับ MT/แพทย์ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช Molecular Dx — เลือก method/แปลผล/กัน false

ตัดสินใจในงาน molecular — "variant/เชื้อ/marker นี้ตรวจด้วยอะไรดี + อย่าพลาดตรงไหน" ไม่ใช่ท่อง central dogma / ขั้น PCR / ตาราง codon (= commodity ดูตำรา)

> **กฎ #1 (เลือก method):** รู้ตำแหน่ง variant แน่ → targeted + ถูก (RFLP/ASO/HRM/qPCR); ไม่รู้/discovery → sequencing (Sanger เดี่ยว, NGS หลาย loci). อย่ายิง NGS สิ่งที่ ASO-PCR ตอบได้ใน 3 ชม.
> **กับดัก #1 (กัน false):** ก่อนแปลผลทุกครั้งต้องครบ **control + tube ถูก (heparin = ห้าม) + NTC สะอาด** — ไม่มี internal control = ห้ามอ่าน "negative" (อาจ reaction fail = false-neg); NTC ขึ้น = ทั้ง run โมฆะ (contamination = false-pos)
> เลือกโมเดล ML ต่อจาก genotype → ดู `ml-judgment` · วาง stat/sens-spec → `choose-stat-test`

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ (คู่กับ `anti-hallucination`)

## ใช้เมื่อ
- ต้อง detect mutation/SNP/fusion/เชื้อ → **เลือก method ไหน** (cost/turnaround/known-vs-unknown variant)
- แปล real-time PCR (Ct, melt curve, HRM) · ตัดสิน positive/negative/invalid
- วาง pipeline genotyping/sequencing · ตัดสิน sample/tube/anticoagulant · DNA vs RNA workflow
- HLA typing (transplant) · pharmacogenomics gate ก่อนให้ยา · companion Dx

## วิธีใช้
วาง skill นี้ + เล่า variant/เชื้อ/ผล qPCR → AI ชี้ method/การแปลผล + กับดัก

---

## ก่อนรัน/แปลผลเสมอ — 3 ด่าน (ขาด = หยุด)
1. **Sample/nucleic-acid integrity** — tube ถูกมั้ย (**heparin = ห้าม ยับยั้ง PCR**) · hemolysis (Hb ยับยั้ง) · RNA สลายรึยัง (RNase ทุกที่) · อุณหภูมิ (DNA ทน, RNA −70°C)
2. **Controls ครบมั้ย** — positive + negative (NTC) + internal/amplification control · qPCR ที่ quantify ต้องมี standard curve · **ขาด internal control = แปล "negative" ไม่ได้** (อาจ reaction fail)
3. **Variant รู้จักมั้ย** — known single vs unknown/scanning vs discovery → กำหนด method (Fork 1) · **polymorphism (MAF≥1%, มักไม่ก่อโรค) ≠ pathogenic mutation**

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — ตรวจ variant นี้ด้วย method ไหน (การตัดสินใจหลัก)
ถามก่อน: (ก) รู้ตำแหน่ง variant แน่ๆ มั้ย (ข) กี่ตำแหน่ง/loci (ค) งบ+turnaround (ง) ขนาด (point vs deletion ใหญ่)
- **Known point + สร้าง/ทำลาย restriction site** → **PCR-RFLP (CAPS)** — ถูกสุด ไม่ต้องเครื่องแพง (คลาสสิก sickle cell *Dde*I)
- **Known point, allele-specific** → **ASO-PCR / ARMS** หรือ **real-time + HRM** (ถูก ไม่ต้อง probe ไม่มี post-PCR)
- **Unknown ในยีนสั้น (scanning)** → **SSCP / HA** คัด → **Sanger ยืนยัน**
- **Large deletion / copy-number** → **gap-PCR / MLPA / qPCR-CNV** (PCR-sequence ทั่วไปมองไม่เห็น deletion ทั้ง allele = trap)
- **ยืนยัน variant เดี่ยว / ตัวอย่างน้อย / <900 bp** → **Sanger** (ground-truth ระดับเดี่ยว)
- **หลาย loci / discovery / VAF ต่ำ (tumor) / high-throughput** → **NGS** (ต้อง validate + bioinformatics + coverage/VAF cutoff)
> หลัก: known → targeted+ถูก (RFLP/ASO/HRM) · unknown/discovery → sequencing. อย่าใช้ NGS ยิงสิ่งที่ ASO-PCR ตอบได้ใน 3 ชม. (over-engineer); อย่าใช้ Sanger ไล่ทีละตำแหน่งกับ panel ใหญ่

### Fork 2 — Sanger vs NGS
- **Sanger:** ยืนยัน variant เดี่ยวที่รู้ตำแหน่ง, ตัวอย่างน้อย, region สั้น, ต้องการ certainty · จุดอ่อน: ไม่เห็น low-VAF (<15–20%), throughput ต่ำ
- **NGS:** discovery, panel/exome/genome, low VAF (somatic/tumor) · ต้องมี validation + bioinformatics + coverage depth + VAF threshold และมัก **confirm hit สำคัญด้วย Sanger** (orthogonal)

### Fork 3 — Real-time PCR: chemistry ไหน (SYBR vs TaqMan vs HRM)
- **SYBR Green** — จับ dsDNA ทุกตัว → ถูก ง่าย **ไม่จำเพาะ ต้องอ่าน melt curve ยืนยัน** (กัน primer-dimer); ดีกับ single amplicon/screening
- **TaqMan probe** — จำเพาะ sequence, **multiplex ได้**, เหมาะ clinical quantitative/viral load · แพงกว่า
- **HRM** — แยก genotype/SNP จากรูป melt (saturating dye) → ถูก ไม่ต้อง probe ไม่มี post-PCR; เหมาะ SNP/point mutation จำนวนมากแบบประหยัด (rpoB/katG ใน MDR-TB)
> 1 target + งบจำกัด → SYBR+melt · multiplex/quantitative clinical → TaqMan · genotype SNP เยอะ-ถูก → HRM

### Fork 4 — Ct / melt → positive, negative, หรือ invalid
- **Ct ต่ำ = template เริ่มต้นเยอะ** (quantify ผ่าน standard curve; relative ต้องมี housekeeping gene)
- **ไม่ขึ้น amplification + internal control ก็ไม่ขึ้น** = **INVALID (inhibition/reaction fail) ไม่ใช่ "negative"** → repeat/extract ใหม่ (ห้ามรายงาน "ไม่พบเชื้อ" จาก reaction ที่ fail)
- **NTC ขึ้น signal** = **contamination → ทั้ง run ใช้ไม่ได้** (Fork 6)
- **SYBR ขึ้นแต่ melt peak ผิด/หลายพีค** = primer-dimer/non-specific ไม่ใช่ true positive

### Fork 5 — Internal / amplification control = บังคับ
ทุก assay ตรวจเชื้อ/mutation ต้องมี control ที่บอกว่า reaction ทำงาน + ไม่มี inhibitor:
- ขาด → negative อาจเป็น false-negative จาก inhibitor/extraction fail (เช่นบอก HIV/TB negative ผิด)
- qPCR quantify → standard curve (efficiency 90–110%, R²>0.98) ก่อนเชื่อค่า

### Fork 6 — Contamination control (amplicon carryover = ศัตรู #1)
- **Unidirectional workflow:** reagent prep → sample prep → amplification/detection (clean→dirty ทางเดียว ห้ามย้อน) · แยกห้อง/พื้นที่/อุปกรณ์
- กัน: UNG/dUTP, aerosol-barrier tips, NTC ทุก run
- **NTC ขึ้น = หยุด ล้าง สืบหา source** ก่อนรันต่อ

### Fork 7 — Oncogene vs tumor-suppressor → test logic
- **Oncogene (gain-of-function, 1 allele พอ)** → หา activating mutation/fusion/amplification + จับคู่ targeted drug (BCR-ABL→imatinib · EGFR→gefitinib/osimertinib · BRAF V600E→vemurafenib · EML4-ALK→crizotinib · HER2 amp→trastuzumab)
- **Tumor suppressor (loss-of-function, ต้อง 2 alleles, Knudson two-hit)** → หา biallelic loss (TP53, RB, BRCA1/2, APC) — prognosis/germline risk

### Fork 8 — HLA typing: resolution แค่ไหน
- **Serology (CDC)** ต่ำ/เร็ว/screening · **PCR-SSP/SSOP** กลาง · **SBT (Sanger)/NGS** สูงสุด
- **Transplant matching (BMT, kidney) → high-resolution (SBT/NGS)** · disease association → กลางพอ
- HLA = ยีน polymorphic ที่สุด, exon 2 (+3 สำหรับ Class I) = region ที่ต้อง type

### Fork 9 — Pharmacogenomics: test "ก่อน" ให้ยา (สำคัญในคนไทย)
- **HLA-B*15:02 ก่อน carbamazepine** → กัน SJS/TEN (**prevalence สูงในคนไทย/จีน** = high-yield จริง) · ⚠️ ผลใช้ **rule-OUT ไม่ใช่ rule-IN**: NPV ~100% (negative → ให้ยาได้ค่อนข้างมั่นใจ) แต่ PPV เพียง ~1.8% (carrier ส่วนใหญ่กินได้ไม่เป็นไร — positive = หลีกเลี่ยง/เปลี่ยนยา ไม่ใช่ทำนายว่าจะเป็นโรค)
- **HLA-B*57:01 ก่อน abacavir** · **HLA-B*58:01 ก่อน allopurinol** · **CYP2C19 + clopidogrel** (poor metabolizer → ยาไม่ทำงาน)
- **G6PD ก่อน primaquine / dapsone / rasburicase / ยา oxidant** → กัน acute hemolysis (G6PD def พบบ่อยในไทย/มาเลย์ + เกี่ยวกับ malaria → ตรวจก่อนให้ primaquine เสมอ) · **TPMT/NUDT15 ก่อน thiopurine** (azathioprine/6-MP → myelosuppression รุนแรงถ้า deficient; NUDT15 สำคัญในเอเชีย) · **DPYD ก่อน 5-FU/capecitabine**
> ตรวจ **ก่อน** prescribe ไม่ใช่หลังเกิด ADR — เฉพาะยา/เชื้อชาติที่ risk สูง (ไม่ใช่ทุกยา) · ⚠️ คู่ที่ขาดบ่อยในไทย: **G6PD↔primaquine** (malaria) + **HLA-B*15:02↔carbamazepine** (SJS)

---

## กับดัก (Anti-patterns) — อันตราย เช็คทุกครั้ง
- 🚫 **Heparin tube ส่ง molecular** = ยับยั้ง Taq → PCR fail/Ct เลื่อน → ใช้ **EDTA (ม่วง) / ACD (เหลือง)**; hemolysis ก็ยับยั้ง
- 🚫 **ลืม internal/amplification control** → reaction fail ถูกอ่านเป็น "negative" → **false-negative**
- 🚫 **Amplicon contamination** → false-positive; **NTC ขึ้น = ทั้ง run โมฆะ**; workflow ต้อง unidirectional
- 🚫 **RNA สลาย** (ไม่ cold chain/ไม่ RNase-free) → RNA target (HIV/SARS-CoV-2 viral load) ต่ำ/negative ปลอม → RT เร็ว, −70°C
- 🚫 **PCR-sequencing แล้วเชื่อว่าครบ ทั้งที่มี large deletion** → allele ที่ถูกลบ "มองไม่เห็น" (het deletion อ่านเป็น homozygous WT) → MLPA/gap-PCR/qCNV
- 🚫 **สับ polymorphism กับ mutation** — MAF≥1% มักไม่ก่อโรค; อย่ารายงาน pathogenic โดยไม่เช็ค database/ACMG
- 🚫 **SYBR/HRM โดยไม่ดู melt curve** → primer-dimer/non-specific นับเป็นบวก
- 🚫 **NGS variant → รายงาน actionable ทันที** โดยไม่ดู VAF/coverage/database + ไม่ confirm orthogonal ตัวสำคัญ
- 🚫 **qPCR quantify โดยไม่มี standard curve / efficiency ไม่ดี** → copy number เชื่อไม่ได้
- 🚫 **Pharmacogenomics ข้าม HLA-B*15:02 ก่อน carbamazepine ในคนไทย** → SJS/TEN ที่ป้องกันได้
- 🚫 **เทียบ/รวม variant coordinate ข้าม genome build** (GRCh37/hg19 vs GRCh38/hg38) โดยไม่ liftover → ตำแหน่ง/ยีน/ผลแปลเพี้ยนทั้งสาย → ระบุ build ของทุกแหล่งให้ตรง + liftover ก่อนเทียบ (และ pin DB release ไว้ reproduce ได้)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง / สะพานสู่งานอื่น เช่น:
> - *"(MT molecular) เคส false-negative/contamination ที่ผมเจอ คือ... จับได้เพราะ..."*
> - *"(งานวิจัย genomics) pipeline genotype→label ของผม: PCR → genotype (RFLP/HRM/NGS) → Sanger/NGS = ground truth → feature/label → validate ด้วย sens/spec"*
> - *"(สาย MolDx sales) targeted/POCT → cartridge qPCR · genomics center → NGS · companion Dx = 'ตรวจก่อนสั่งยา'"*

---
*ช่วยคิดเลือก method/แปลผล molecular เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รักษา — ต้องตาม SOP + validation ของแล็บ และยืนยันกับ MT/แพทย์ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
