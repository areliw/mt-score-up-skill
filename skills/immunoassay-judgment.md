---
skill: immunoassay-judgment
title: ตัวช่วยตัดสินใจ Immunoassay และ Serology (Immunoassay & Serology Judgment)
type: ADVISE
needs: any
author: "MT Score UP!"
reviewed: 2026-06-01
status: draft
disclaimer: "Skill นี้เป็นตัวช่วย 'คิด' เพื่อการศึกษาเรื่อง immunoassay/serology ไม่ใช่คำสั่งวินิจฉัย/รักษา ผล reactive screen ไม่เท่ากับการวินิจฉัย ต้อง confirm ด้วย test ที่ specificity สูงก่อนรายงานเสมอ ทุกผลต้องยืนยันกับ MT/แพทย์ และทำตาม SOP/QC ของห้องแล็บ ความผิดพลาดในการตีความ serology อาจกระทบความปลอดภัยของผู้ป่วยโดยตรง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ตัวช่วยตัดสินใจ Immunoassay และ Serology

ตัวช่วย "ตัดสินใจ" เรื่อง immunoassay/serology สำหรับคนหน้างาน lab — ไม่ใช่ตำราท่องนิยาม — ทุกคำตอบตอบ 2 อย่าง: "เลือก/ตีความอะไร" + "พลาดตรงไหน".

> กฎเหล็ก: reactive screen ≠ diagnosis — ต้อง confirm ด้วย test ที่ specificity สูงก่อน report เสมอ. และเลือก format ตาม analyte (ใหญ่ = sandwich, เล็ก = competitive).

## ใช้เมื่อ
- ต้องเลือก immunoassay format ให้เหมาะกับ analyte (sandwich vs competitive vs CLIA/ECLIA vs lateral flow)
- ต้องตีความ serology panel — HBV, HIV algorithm, syphilis NTT/TT, ANA pattern
- ก้ำกึ่งว่า reactive screen ต้อง confirm ไหม / dilute เพราะ prozone-hook ไหม
- ผลลบสวนอาการ หรือ ผลบวกในคน prevalence ต่ำ — ต้องตัดสินใจว่าเชื่อหรือทวน
- เลือก/อ่าน non-label (agglutination/nephelometry/precipitation) · immunoblot/Western · IGRA (QFT) · ระวัง HAMA/biotin interference
- (สาย sales/IVD) เตรียมคุยงาน diagnostics — Abbott Architect/Alinity, Roche Elecsys/cobas, Bio-Rad, Siemens

## วิธีใช้
วาง skill นี้ + เคส/ผลที่เจอ (analyte, format, ค่า screen/confirm, clinical) → AI เดินตาม fork ด้านล่าง บอก "เลือก/ตีความอะไร" + "กับดักที่ต้องระวัง" โดยยึดหลัก confirm-ก่อน-report เสมอ

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### FORK 1 — เลือก immunoassay FORMAT (analyte นี้ ใช้แบบไหน)
ถามก่อน: analyte ใหญ่หรือเล็ก? ต้องการ throughput/quant แค่ไหน? อยู่ที่ไหน (lab vs POC)?
- Analyte = โมเลกุลใหญ่ (โปรตีน, ≥2 epitope) → Sandwich (non-competitive): 2 Ab จับคนละ epitope, signal แปรผันตรง. เช่น HBsAg, troponin, tumor marker, hormone โปรตีน.
- Analyte = โมเลกุลเล็ก / hapten (drug, steroid, T4, epitope เดียว) → Competitive: Ab ตัวเดียว, labeled-Ag แข่งกับ sample, signal แปรผกผัน. เช่น drug-of-abuse, cortisol, digoxin. → เล็ก = competitive = ผกผัน.
- ต้องการ throughput สูง + quant + automation → CLIA/ECLIA/CMIA. ECLIA = Roche Elecsys/cobas; CMIA = Abbott Architect/Alinity; CLIA/EIA = Bio-Rad/Siemens.
- ตรวจ Ab (ไม่ใช่ Ag) → Indirect format (+ secondary anti-human IgG/IgM). แยก IgM (acute) vs IgG (past/immune).
- ผลเร็ว / POC → Lateral flow (immunochromatographic, colloidal gold): hCG, dengue NS1, COVID Ag, HIV/syphilis rapid.
- quantitate Ig/RF/complement/CRP → Nephelometry/turbidimetry (particle-enhanced latex).
- Heterogeneous (ล้าง bound-free: ELISA/CLIA) vs Homogeneous (ไม่ล้าง: EMIT/CEDIA) → homogeneous เร็ว/automate ง่ายแต่ไวต่อ interference มากกว่า.

### FORK 2 — SEROLOGY interpretation forks
HBV panel (HBsAg / anti-HBs / anti-HBc) — อ่าน 3 ตัวรวมกัน:

| HBsAg | anti-HBc (total) | anti-HBs | → สถานะ |
|---|---|---|---|
| + | + (IgM) | − | Acute infection |
| + | + (IgG) | − | Chronic (HBsAg + > 6 เดือน) |
| − | + | + | Recovered (หายเอง, มีภูมิ) |
| − | − | + | Vaccinated (ภูมิจากวัคซีน, ไม่มี anti-HBc) |
| − | + | − | "core-only" → window/occult/false-pos → follow-up |

ตัวชี้ขาด vaccinated vs recovered = anti-HBc.

- HIV algorithm: screen 4th-gen Ag/Ab combo (p24 + Ab) → reactive → confirm (Ab differentiation / particle agglutination / WB) → discordant/acute → NAT (viral load). อย่ารายงาน positive จาก screen เดี่ยว.
- Syphilis: NTT (RPR/VDRL, titer ติดตามการรักษา) + TT (TPHA/TPPA/FTA, จำเพาะ, บวกตลอดชีวิต). Traditional: NTT screen → TT confirm. Reverse: TT screen → NTT confirm + titer. TT+ NTT− → early หรือ treated-old → TT ตัวที่สอง.
- ANA (IIF บน HEp-2 = gold) → รายงาน pattern + titer: Homogeneous → dsDNA/histone → SLE/drug-induced; Speckled → Sm/RNP; Peripheral/rim → active SLE; Nucleolar → scleroderma; Centromere → CREST. ↑titer → ↓false-positive. confirm ด้วย anti-dsDNA / anti-ENA.

### FORK 3 — เมื่อไหร่ "ต้อง CONFIRM" reactive screen
- screen sensitivity สูง (↓FN) → มี false-positive ปนเสมอ. reactive screen ≠ diagnosis. ต้อง confirm ด้วย test specificity สูง (↓FP) ก่อนรายงาน (HIV, syphilis, HCV).
- PPV ขึ้นกับ prevalence: prevalence ต่ำ + screen reactive → ส่วนใหญ่อาจ false-pos → confirm ยิ่งจำเป็น.

### FORK 4 — Non-label techniques + agglutination
- **Precipitin zone:** ตะกอนเฉพาะ equivalence · **prozone (Ab เกิน) / postzone (Ag เกิน)** → false negative → เจือจางแล้วซ้ำ
- **Turbidimetry vs Nephelometry:** turbidimetry วัดแสง**ลด** (180°) · **nephelometry วัด scatter** (10-90°) ไวกว่า → ใช้กับ Ig/complement/CRP/RF · particle-enhanced (latex) ตรวจ analyte เล็กลงได้
- **RID/Ouchterlony/IFE:** RID = quant Ag จากวงตะกอน · Ouchterlony = identity/non-identity · **IFE = typing monoclonal protein** (myeloma)
- **Agglutination 4 ชนิด:** Direct (Ag บน particle เอง — blood typing) · Passive (soluble Ag เคลือบ → ตรวจ Ab) · **Reverse passive** (Ab เคลือบ → ตรวจ Ag: CRP/HBsAg latex) · Inhibition (ยับยั้ง=บวก, hapten) · **IgM จับกลุ่มดีกว่า IgG มาก** (10 site) · titer = dilution สูงสุดที่ยังบวก

### FORK 5 — Immunoblotting / Western blot (confirm + characterize)
- SDS-PAGE แยกตาม **ขนาด (MW)** → blot ลง membrane → block → Ab จำเพาะ → enzyme/chemiluminescent substrate
- ใช้: **confirmatory** (Ab จับโปรตีนเป้าตัวไหน) + **characterize Ag** · **reducing (+2-ME) vs non-reducing** → MW เปลี่ยน = มี disulfide bond

### FORK 6 — Cell-based / IGRA (เช่น QFT-TB)
- whole blood + peptide จำเพาะ TB (ESAT-6/CFP-10) → วัด **IFN-γ ที่ T cell หลั่ง ด้วย ELISA (sandwich)** = ตรวจ cell-mediated immunity (รวม latent TB) แทน/เสริม TST (ไม่ false+ จาก BCG)
- ⚠️ **Indeterminate** = mitogen control ไม่ขึ้น / nil สูง → ตีความไม่ได้ ต้องเจาะใหม่ · clotted = invalid

## กับดัก (Anti-patterns)
1. Prozone (false-negative ที่ titer สูง) #1 — Ab เกินมาก → ไม่เกิด lattice → ผลลบทั้งที่ป่วยหนัก (RPR ใน secondary syphilis). เจอ clinical สงสัยแต่ผลลบ → เจือจาง (dilute) ทดสอบใหม่. Postzone = Ag เกิน. optimal = equivalence.
2. Hook effect (high-dose hook) — sandwich CLIA: analyte สูงมาก (tumor marker, β-hCG) → saturate Ab ทั้งสองข้าง → signal ต่ำหลอก. ผลต่ำสวนอาการ → dilute ซ้ำ.
3. Window period — ตรวจเร็วเกินยังไม่มี marker. HIV: RNA ~7-14 วัน → p24 ~16 วัน → Ab ~25 วัน. HBV: core-window. ผลลบในคนเพิ่งเสี่ยง → ยังไม่ตัดโรค, นัดซ้ำ.
4. Cross-reactivity / false-positive → ไม่ confirm — biological false-pos RPR (SLE, ตั้งครรภ์, ติดเชื้ออื่น); RF รบกวน; heterophile Ab.
5. อ่าน HBV panel ทีละตัว — HBsAg+ เดี่ยวไม่บอก acute vs chronic; anti-HBs+ เดี่ยวไม่บอก vaccinated vs recovered → ดู anti-HBc.
6. สับ competitive กับ sandwich — ใช้ sandwich กับ hapten เล็ก = พัง; ใช้ competitive แล้วลืม signal ผกผัน = อ่านกลับด้าน.
7. ลืมเตรียม specimen — ไม่ heat-inactivate complement (56°C 30 นาที); lipemia/hemolysis รบกวน optical; IgM ทำงานดีที่เย็น.
8. ใช้ test ผิดจุดประสงค์ — screen ไปใช้ confirm; TT (บวกตลอดชีวิต) ไปติดตามการรักษาแทน NTT titer → ตีความผิดว่า "ไม่หาย".
9. HAMA (human anti-mouse Ab) — คนไข้เคยรับ mAb บำบัด → จับ capture+detection Ab ของ sandwich → false +/− → ต้อง blocking reagent.
10. Biotin interference — กิน biotin (วิตามินผม/เล็บ) สูง รบกวน assay biotin-streptavidin → ผลเพี้ยน (TSH/troponin ต่ำปลอม อันตราย) → งด biotin ก่อนเจาะ.
11. Competitive / lateral-flow อ่านกลับด้าน — สัญญาณต่ำ หรือ "ไม่มีแถบ test" = analyte สูง (ชุดยาเสพติด); **control line ไม่ขึ้น = invalid ไม่ใช่ลบ**.

> NOTE: knowledge (Ig class, complement pathway, hypersensitivity I-IV, Sens/Spec/PPV/NPV) → point to "ตำรา/แหล่งอ้างอิงมาตรฐาน", no path.

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - เติม cutoff/algorithm ของ HIV/HCV/syphilis ที่ใช้จริงตาม SOP ห้องแล็บนั้นๆ (traditional vs reverse)
> - ระบุ analyzer + reagent platform ที่ใช้ (Abbott/Roche/Bio-Rad/Siemens) + protocol dilution เมื่อสงสัย prozone/hook
> - เพิ่ม panel/marker เฉพาะที่ รพ. ใช้บ่อย + criteria การ confirm/repeat ตาม policy ห้องแล็บ

---
*Skill นี้เป็นตัวช่วย "คิด" เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รักษา — reactive screen ต้อง confirm ก่อน report ทุกผลต้องยืนยันกับ MT/แพทย์ + ทำตาม SOP/QC ของห้องแล็บ ความผิดพลาดในการตีความ serology กระทบความปลอดภัยผู้ป่วยโดยตรง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
