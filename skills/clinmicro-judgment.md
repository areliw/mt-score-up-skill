---
skill: clinmicro-judgment
title: ตัวช่วยตัดสินใจแล็บจุลชีววิทยาคลินิก (Clinical Micro Judgment)
type: ADVISE
needs: any
author: "MT Score UP!"
reviewed: 2026-06-01
status: draft
disclaimer: "Skill นี้เป็นตัวช่วย 'คิด' สำหรับการตัดสินใจในแล็บจุลชีววิทยาคลินิกเพื่อการศึกษา ไม่ตัดสินแทน และไม่ใช่คำสั่งวินิจฉัย/รักษา ทุกผลต้อง correlate กับ Gram stain + clinical + colony morphology และทำตาม SOP/QC ของห้องแล็บเสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง ความผิดพลาดในการรายงานเชื้อก่อโรค/ความไวต่อยา อาจกระทบความปลอดภัยของผู้ป่วยโดยตรง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ตัวช่วยตัดสินใจแล็บจุลชีววิทยาคลินิก

ตัวช่วย "ตัดสินใจ" ในแล็บจุล ไม่ใช่ตำราชนิดเชื้อ/สูตร media — ทุกคำตอบตอบ 2 อย่าง: "ตรงนี้เลือกอะไร" + "พลาดตรงไหน".

> กฎเหล็ก: correlate กับ Gram/clinical เดิมเสมอ ก่อน report. ผลที่ขัดกับ Gram smear, site, หรือ colony morphology = หยุด ทวนก่อน.

## ใช้เมื่อ
- ต้อง decide ในงาน Micro — เชื้อจริงหรือปน, ID พอยัง, อ่าน AST, รายงาน MDR
- รับ/ปฏิเสธ specimen, เลือก culture vs molecular
- ก้ำกึ่งว่าจะ ID/AST ต่อหรือพอแค่นี้
- (สาย sales/MolDx) เตรียมคุยงาน Lab/MolDx — bioMérieux VITEK, Cepheid GeneXpert, AST/MALDI automation

## วิธีใช้
วาง skill นี้ + เคส/ผลที่เจอ (Gram, media, colony, AST, specimen info) → AI เดินตาม fork ด้านล่าง บอก "เลือกอะไร" + "กับดักที่ต้องระวัง" โดย correlate กลับ Gram/clinical เสมอ

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### FORK 1 — ID workflow: เดินยังไง + เมื่อไหร่พอ
ลำดับ: Gram stain → เลือก media + atmosphere → biochem/MALDI-TOF → S/I/R.
- Gram บอกทาง: GPC cluster → Staph lane (catalase → coagulase/cefoxitin). GPC chain/diplo → Strep lane (hemolysis + bile-esculin/optochin). GNB → lactose vs non-lactose → oxidase แยก non-fermenter (Pseudo/Acineto).
- เมื่อไหร่พอ: ID ละเอียดแค่ที่ เปลี่ยนการรักษา/รายงาน. Urine E. coli predominant + AST = พอ. alert organism / sterile site (blood, CSF) → ID ให้ถึง species + เก็บ isolate.
- MALDI-TOF vs biochem: มี MALDI → ใช้แทน biochem panel ยาวได้. biochem/VITEK ยังจำเป็นตอน MALDI ก้ำกึ่ง หรือเชื้อไม่อยู่ใน library.
- (สาย sales/MolDx) VITEK/MALDI ตัด hands-on time + standardize ID; ชู turnaround + reproducibility.

### FORK 2 — เลือก media + atmosphere (ผิด = เชื้อไม่ขึ้น เงียบๆ)
- Fastidious (Strep, Neisseria, Haemophilus) → Chocolate agar + 5% CO₂.
- Anaerobe สงสัย (abscess, deep wound) → anaerobic jar/chamber + media anaerobe.
- Selective ตาม specimen: stool → MacConkey + selective (Salmonella/Shigella) + enrichment Selenite F; urine → CLED/CHROMagar; GBS screen → enrichment broth.
- trade-off: เพิ่มจาน selective/atmosphere = sensitivity ขึ้น แต่ cost/labor ขึ้น. เลือกตาม specimen + clinical question.

### FORK 3 — เชื้อจริง หรือ contaminate (สำคัญที่สุด)
| สถานการณ์ | ถาม | ตัดสิน |
|---|---|---|
| Blood culture ขึ้น CoNS / diphtheroid / Bacillus 1 ขวด จาก 2+ | กี่ขวด? sterile site? sepsis? | 1/2 ขวด skin flora → contaminate; ทั้ง 2 ขวด + line/clinical → อาจจริง |
| Urine ขึ้น >3 ชนิด ใกล้กัน | colony count? predominant? | "Mixed bacterial growth" → contamination, ขอ specimen ใหม่ |
| Urine CoNS/α-strep/diphtheroid นับน้อย | urethral flora? | normal flora → ไม่ต้อง ID/AST เว้นแต่ predominant + count สูง |
| Sputum ขึ้น normal oral flora ล้วน | Q-score ผ่านไหม? | คุณภาพแย่ → ปฏิเสธ/ขอใหม่ |

Urine colony count (loop 0.001 ml): ≥10⁵ CFU/ml pure/predominant = indicated pathogen (ID+AST); 10⁴–10⁵ = suspected; <10³ = "no significant growth".
- หลัก: site + count + จำนวนชนิด + clinical ประกอบกัน.

### FORK 4 — AST: เลือก method + อ่าน S/I/R + escalate MDR
- Disk diffusion vs MIC: disk (Kirby-Bauer, MHA/0.5 McFarland/35±2°C/16-18h) = routine. MIC (broth microdilution/E-test/VITEK) เมื่อต้องการค่าตัวเลข — sterile site, ปรับ dose, หรือ disk ก้ำกึ่ง.
- อ่าน zone — 3 ข้อยกเว้น: (1) sulfa/co-trimox → ignore growth จางใน zone <20%; (2) Proteus swarm → อ่านขอบ inhibition จริง; (3) β-lactamase+ Staph vs penicillin → ขอบ zone คม "cliff" = R เสมอ.
- confirmatory + escalate: MRSA (cefoxitin → report เป็น oxacillin, zone ≤21=R) → report + infection control. Inducible clindamycin (Erythro=R + Clinda=S → D-test; D+ → report clindamycin R). ESBL (ดื้อ ceph 3rd → combo disk +clav ≥5mm). CRE/carbapenemase (mCIM/eCIM; eCIM+EDTA → metallo/NDM → รายงานด่วน + แยกผู้ป่วย). VRE (screen + รายงาน alert).
- (สาย sales/MolDx) GeneXpert Carba-R / mecA PCR = ตัดเวลา confirmatory phenotype.

### FORK 5 — Specimen quality: รับหรือปฏิเสธ
- Sputum Q-score/Bartlett: WBC เยอะ + squamous epithelial cell น้อย = ดี → process. SEC เยอะ (>25/lpf) = ปนน้ำลาย → ปฏิเสธ ขอใหม่.
- Reject เมื่อ: ฉลากไม่ตรง/ไม่มี, container รั่ว, transport ผิด, ปริมาณไม่พอ, ซ้ำใน 24h ไม่จำเป็น.
- GIGO. แต่ specimen หายาก (CSF, biopsy, intraop) → อย่าทิ้ง ติดต่อแพทย์/process + note limitation.

### FORK 6 — Culture vs Molecular (GeneXpert / PCR)
- TB: AFB smear sens ต่ำ + ไม่แยก viable/MTB-NTM; culture = gold แต่ 4–8 สัปดาห์ → GeneXpert MTB/RIF เมื่อต้องการผลเร็ว + ดื้อ rifampin (rpoB) (<2 ชม.). ยังต้อง culture+DST สำหรับ panel ยาเต็ม.
- Virus / culture ช้า-อันตราย: HIV viral load, HBV/HCV-RNA, respiratory panel → real-time PCR. Infant HIV → DNA/RNA PCR ไม่ใช่ Ab.
- หลัก: molecular เมื่อ culture ช้า/อันตราย/sens ต่ำ, ต้องการ resistance gene เร็ว, เชื้อเพาะยาก. Culture ชนะตอนต้องการ isolate ไปทำ AST เต็ม + cost.

### FORK 7 — Specimen-site → เชื้อที่คาด + media ตาม syndrome (อย่าหว่านจานเดียวกันทุก site)
อ่าน **site + host + syndrome** กำหนด workup ก่อนเพาะ:
- **CSF/meningitis:** อ่าน CSF profile ก่อนเดา — neutrophil↑ + glucose↓มาก + protein↑ = bacterial (รายงานด่วน); lymphocyte + glucose ปกติ = viral; lymphocyte + glucose↓ ปานกลาง = TB/fungal · เชื้อตาม **อายุ** (newborn GBS/E.coli/Listeria · เด็ก Nm/Spn/Hib · สูงอายุ +GNB/Listeria) · ⚠️ Cryptococcus cell count อาจปกติ → **สั่ง CrAg/India ink เสมอ อย่าตัดออกเพราะ cell ปกติ**
- **LRTI:** Gram screen ก่อนเพาะ (PMN>25 + squamous<10/LPF = รับ) · **VAP/BAL = quantitative** (≥10⁴ CFU/ml = จริง) ไม่ใช่ qualitative · TB ใช้ early-morning sputum ×3
- **Stool:** เพาะเมื่อ bloody/leukocyte+/ไข้/travel · media ตาม syndrome (TCBS+APW→Vibrio · SS/XLD/HE+enrich→Salmonella/Shigella · CCFA→C.diff · 42°C microaerophilic→Campylobacter) · ⚠️ ไม่ enrich = จับ Vibrio/Salmonella ไม่ได้
- **Genital:** GC→Thayer-Martin/VCN · **BV ไม่เพาะ** ใช้ pH>4.5 + whiff + clue cells
- **Sterile fluid** (pleural/peritoneal/joint/CSF): เชื้อใดก็ significant → ลง BA/CA/MC + **thioglycollate (anaerobe, ดู 7 วัน)**; อย่ามองข้าม anaerobe ใน deep pus

### FORK 8 — Special-organism pathways (fungi · mycobacteria · zoonosis/Rickettsia)
- **Fungi yeast-vs-mold:** KOH/calcofluor direct → SDA ± additive · ⚠️ **cycloheximide กด opportunistic mold (Aspergillus/Fusarium/Zygomycetes/Cryptococcus) + Nocardia** → ถ้าสงสัยพวกนี้ **อย่าใช้สื่อ cycloheximide จานเดียว** · Cryptococcus → CrAg เร็วกว่ารอเพาะ
- **Mycobacteria ladder:** ZN/auramine smear (sens ต่ำ 5,000–10,000/ml, **smear-neg ไม่ตัด TB**, แยก MTB/NTM ไม่ได้) → culture gold (MGIT 1–3wk เร็วกว่า LJ 6–8wk) → MTB-vs-NTM (niacin+/nitrate+/MPT64+) → DST/GeneXpert สำหรับ MDR
- **Zoonosis/Rickettsia/Chlamydia:** serology+molecular เป็นหลัก, culture ทำไม่ได้/ต้อง BSL-3 → paired serology 4-fold + IFA + PCR · Weil-Felix = screening หยาบ ไม่ confirm · ⚠️ **Leptospira/PCR ห้าม heparin** (ยับยั้ง Taq + citrate ฆ่าเชื้อ) · ผู้ป่วยหนัก ใช้ PCR/Giemsa buffy coat เร็วกว่ารอ serology

## กับดัก (Anti-patterns)
1. รายงาน contaminant เป็น pathogen — CoNS 1 ขวด, urine 3+ ชนิด, sputum oral flora.
2. ไม่ correlate กับ Gram เดิม — AST/ID ขัด Gram smear = หยุด ทวน.
3. Misread AST — ESBL / inducible clinda / β-lactamase Staph → ปล่อยยาที่ใช้ไม่ได้จริง.
4. Miss MDR ที่ต้องรายงานด่วน — MRSA/VRE/ESBL/CRE/MDR-TB ไม่ flag → ระบาดในวอร์ด.
5. เลือก media/atmosphere ผิด → false-negative เงียบ.
6. Process sputum คุณภาพแย่ → เลี้ยง oral flora รายงานเป็นเชื้อปอด.
7. Smear-negative = ไม่มี TB (ผิด) — ต้อง culture/GeneXpert.
8. QC strain หลุดแต่ยังรายงานผล — ATCC (S.aureus 25923, E.coli 25922, P.aeruginosa 27853, E.faecalis 29212) นอก range → หยุด ห้าม report.
9. Over-ID / over-AST เชื้อ commensal → เปลือง + ชวนใช้ยาเกิน.
10. ลืม intrinsic resistance — รายงาน amp/ceph สำหรับ P.aeruginosa (ดื้อโดยธรรมชาติ).

> NOTE: knowledge (taxonomy, media recipes, colony-count tables, MIC/MBC, AFB grading) → point to "ตำรา/แหล่งอ้างอิงมาตรฐาน", no path.

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - เพิ่ม antibiogram/MDR pattern เฉพาะของ รพ. ที่ผู้ใช้ทำงาน (intrinsic resistance + breakpoint local)
> - เติม cutoff/criteria ของ specimen rejection ตาม SOP ห้องแล็บนั้นๆ
> - ระบุ alert organism list + ช่องทางแจ้ง infection control ที่ใช้จริง

---
*Skill นี้เป็นตัวช่วย "คิด" เพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ตัดสินแทน ทุกผลต้อง correlate กับ Gram/clinical + ทำตาม SOP/QC ของห้องแล็บ — ความผิดพลาดกระทบความปลอดภัยผู้ป่วยโดยตรง ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
