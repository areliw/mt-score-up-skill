---
skill: bloodbank-judgment
title: โค้ชธนาคารเลือด — ตัดสินใจหน้างาน ไม่ให้คนไข้ตาย (Blood Bank Judgment)
type: ADVISE               # ช่วยตัดสินใจหน้า bench ไม่ใช่ตำรา antigen frequency
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "เครื่องมือช่วยคิดหน้างานธนาคารเลือดเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ใช่ผู้ตัดสินใจแทน งาน BB เกี่ยวชีวิตคนไข้โดยตรง ต้องทำตาม SOP, ยืนยันกับ MT/แพทย์, อ้างมาตรฐาน AABB/ศูนย์อ้างอิงเสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชธนาคารเลือด — ตัดสินใจหน้างาน ไม่ให้คนไข้ตาย

ตัดสินใจหน้า bench ธนาคารเลือด — **"เลือกอะไรเมื่อไหร่ + พลาดตรงไหนถึงคนตาย"** ไม่ใช่ท่องตาราง antigen frequency (นั่นคือ commodity ดูตำรา)

> **ตัดสินใจ #1:** ผลแปลก / เข้ากันไม่ได้ / reaction → **เช็ค clerical ก่อน serology เสมอ** (ชื่อ-HN-ป้ายหลอด-sample-group เดิม) แล้วค่อยคิดต่อ
> **กับดัก #1:** **ABO mislabel = สาเหตุ #1 ของ fatal acute hemolysis** — แก้ที่ serology ก่อนตัด clerical = พลาดที่ฆ่าคนจริงสุดของทั้งวิชา
> เลือดออกมากรอ XM ไม่ทัน → **จ่าย O ทันที** (หญิงวัยเจริญพันธุ์/เด็ก = O neg) + เก็บ sample ก่อนให้เลือด

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- ABO ไม่ตรง (cell ≠ serum) · antibody screen บวก → จะ ID ยังไง · DAT/IAT อันไหน · crossmatch แบบไหน
- เลือก component / เมื่อไหร่ irradiate / leukoreduce · transfusion reaction → workup · ฉุกเฉินจ่าย O เมื่อไหร่
- HDN/HDFN (Rh vs ABO + RhIG) · เมื่อไหร่ใช้ genotype แทน serology · enhancement (enzyme/LISS/adsorption/elution) · support transplant/HSCT
- delayed/late reactions (DHTR/TA-GVHD/PTP/iron overload) · เลือก special technique (potentiator/ลบ Ab) ตอนผลไม่ชัด

## วิธีใช้
วาง skill นี้ + เล่าเคส (ผล forward/reverse, screen, ประวัติ) → AI ชี้ "ทำอะไรก่อน" + กับดักอันตราย

---

## กฎเหล็กก่อนทุกอย่าง — CLERICAL ก่อนเสมอ
เช็ค 4 ข้อก่อนคิด serology: ชื่อ-HN ถูกคน? หลอดติดป้ายถูก? sample เก่า/clot/hemolyze? group เดิมในประวัติตรงไหม?

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — decision forks

### Fork 1 — ABO discrepancy (cell ≠ serum) → resolve ยังไง
> **verdict:** ทำซ้ำ+ล้าง RBC ตัด technical → แยก forward (RBC) vs reverse (serum) → ฉุกเฉินยังไม่ชัด = **จ่าย O**

**ลำดับเสมอ:** (1) ทำซ้ำ + ล้าง RBC ตัด technical error (2) เก็บ sample ใหม่ + ถาม Dx/อายุ/transfusion-transplant/ยา (3) แยกปัญหาที่ **RBC (forward)** หรือ **serum (reverse)** → WEAK/MISSING/EXTRA

| เคส | เบาะแส | resolve | จ่ายเลือด |
|---|---|---|---|
| **Acquired B** (RBC extra) | group A + มะเร็งลำไส้/septicemia (E.coli) | anti-B acidified pH6, autocontrol (ตัวเองไม่จับ) | **group A** (หมู่จริง) |
| **B(A)/A(B)** (RBC extra) | weak extra reaction, autosomal dominant | molecular/ref lab ยืนยัน | ตามหมู่จริง (B(A)→B) |
| **cis-AB** (inheritance ผิดคาด) | พ่อ/แม่ O × ลูก "AB"? — A+B อยู่บน chromosome เดียว ถ่ายทอดคู่กัน; A หรือ B มัก weak | family study + molecular; **อย่าด่วนสรุป parentage ผิด** | ตามหมู่จริง (มัก A₂B-like) |
| **Mixed-field** (RBC) | บางเซลล์จับ; post-BMT / ได้ O เยอะ / A3 | ดูประวัติ transfuse-transplant + titer | ฉุกเฉิน **O** ก่อน |
| **anti-A1** (serum extra) | A2/A2B reverse จับ A1 cell | A1 vs A2 cell + **anti-A1 lectin (Dolichos)** | **A2 หรือ O** |
| **Cold autoAb** (serum extra) | anti-I/IH; **screen+ AND auto+** | **prewarm 37°C** / cold autoadsorption | warm Ab ที่เหลือ |
| **Rouleaux** (serum) | โปรตีนสูง (myeloma), "stack of coins" | **saline replacement** | ตามหมู่จริง |
| **anti-H / Bombay** (serum extra) | screen+, **auto−**, จับ O cell แรง; XM ไม่เข้ากับ O ใครเลย | ยืนยัน Bombay RBC + saliva | **เลือด Bombay เท่านั้น** |
| **Missing/weak Ab** (serum) | ทารก/สูงอายุ/hypogamma/BMT/myeloma | incubate RT/4°C นานขึ้น + autocontrol | ตามหมู่ที่ยืนยันได้ |
| **Rhnull** (Rh typing ลบหมด) | complete Rh phenotype ลบทุก Ag → สร้าง **anti-Rh29** | molecular/ref lab ยืนยัน | **เลือด Rhnull เท่านั้น** (rare registry/family/autologous) |
| **Passive anti-A,B** (serum/DAT extra) | ผู้ป่วย A/B ได้ **group O platelet/plasma** → DAT+ / eluate = anti-A,B | ดู Hx component (ไม่ใช่ auto/allo) | **O RBC ชั่วคราว** จน passive หาย → กลับ type-specific |

### Fork 2 — antibody screen บวก → ID strategy
> **verdict:** อ่าน autocontrol ก่อน (auto− = allo, panel ปกติ) → rule-out ด้วย homozygous cell → ต้องได้ 3-cell rule ก่อนสรุป

- **อ่าน autocontrol ก่อน:** auto− = **allo**antibody (panel ID ปกติ) · auto+ → คิด AIHA/cold-auto/recent transfusion ก่อน
- **rule-out บน panel:** ขีดฆ่า antibody เมื่อ reagent cell ที่ **Ag-positive ให้ reaction ลบ (Ag+/react−)** → เหลือตัวที่ fit ทุกแถว = candidate; **rule-out ด้วย homozygous cell** (เลี่ยง dosage บัง)
- **95% (3-cell) rule:** สรุป Ab ได้เมื่อมี **≥3 cell (Ag+ → react+)** และ **≥3 cell (Ag− → react−)**; ไม่ครบ → หา selected cell เพิ่ม
- **units to crossmatch ≈ requested ÷ Π(freq ของ Ag-negative)** — เช่น ขอ 3 unit + anti-E (E−0.7) + anti-Jka (Jka−0.25) → 3/(0.7×0.25) ≈ **17 units** · ⚠️ **freq เป็นค่าตามประชากร** (เลขนี้แค่ตัวอย่าง ไม่ใช่ค่าตายตัว) → ของจริงถูกจำกัดด้วย stock; ถ้า Ag หายาก/ของไม่พอ = **ส่ง ref lab/rare registry**
- **dosage:** anti-Jk/Rh/Duffy/Kell/MNS จับ homo แรงกว่า het → het cell อ่าน "ลบลวง" ได้
- **enzyme (ficin/papain):** Rh/Kidd/P/Lewis **เด่นขึ้น** · MNS/Duffy **ถูกทำลาย** → ใช้แยก 2 ระบบทับกัน
- **multiple/pan-react หรือ XM ไม่เข้ากับ unit ใดเลย:** ไม่ fit ตัวเดียว → selected cell + enzyme + เผื่อ **antibody ต่อ high-incidence Ag** (anti-H/Bombay · **anti-Rh29/Rhnull** → ต้องเลือดชนิดเดียวกันจาก rare registry) + HTLA/HFA → ส่ง ref lab (ศูนย์อ้างอิงระดับชาติ)

### Fork 3 — DAT vs IAT เมื่อไหร่
> **verdict:** เคลือบมาแล้ว in vivo (AIHA/HDFN/HTR) = **DAT** · Ab ในซีรั่มจับ in vitro (screen/XM/phenotype) = **IAT** · AHG ลบทุกครั้งต้องยืนยันด้วย CCC

- **DAT** = RBC ถูกเคลือบ in vivo → สงสัย **AIHA / HDFN (cord) / HTR / drug-induced**; sample = **EDTA whole blood**
- **IAT** = Ab ในซีรั่มจับ antigen in vitro → **antibody screen/ID, crossmatch AHG, phenotyping, weak D**; sample = **serum/plasma สด**
- "ทำไม transfusion reaction" → DAT บวกหลังให้เลือด = สงสัย HTR → DAT + clerical + ABO ซ้ำ pre/post
- **QC พลาดบ่อย:** AHG ออก negative ต้องหยอด **CCC (Coombs Control Cell)** — CCC ไม่จับ = ล้างไม่พอ → test ใช้ไม่ได้

### Fork 4 — crossmatch ไหน (IS / AHG / electronic)
> **verdict:** screen ลบ + ABO ยืนยัน 2 ครั้ง = **IS/electronic** พอ · screen บวก / เคยมีประวัติ Ab = **full AHG XM + antigen-neg unit** (แม้ screen ตอนนี้ลบ)

| สถานการณ์ | crossmatch |
|---|---|
| screen ลบ + ไม่มีประวัติ Ab + ยืนยัน ABO 2 ครั้ง | **electronic / immediate-spin** พอ |
| screen บวก / มีประวัติ clinically-sig Ab | **full AHG XM** + antigen-negative unit |
| cold autoAb (anti-I/IH) บัง | **prewarmed 37°C** |
| ฉุกเฉินไม่ทันรอ | **O uncrossmatched** (ดู Fork 7) |
> ⚠️ เคยมี clinically-sig Ab แม้ตอนนี้ screen ลบ (titer ตก) → **ยังต้องให้ antigen-neg + AHG XM** (anti-Jk anamnestic = delayed HTR)
- **CAT/gel card:** grading objective + inter-observer ต่ำ (เหตุที่แทน tube) · ⚠️ **เลือกการ์ดถูกชนิด — ABO/IgM ใช้ neutral card (ไม่มี AHG); IAT/screen/XM ใช้ anti-IgG (Coombs) card** — ผิดการ์ด = อ่านผิด
- ⚠️ **ก่อนจ่ายทุก unit ที่ XM ผ่าน → phenotype unit ว่า Ag-negative** ต่อ Ab ผู้ป่วย (เคส weak Ab/dosage: unit heterozygous อาจมี Ag จริงแต่ XM compatible ลวง)

### Fork 5 — component selection + เมื่อไหร่ irradiate/leukoreduce
> **verdict:** จับคู่ component กับ deficit · กลุ่มเสี่ยง TA-GVHD (neonate/directed-relative/HLA-matched/immunocompromised) = **irradiate เสมอ** (leukoreduction ไม่กัน)

- **PRC:** anemia/thalassemia · **FFP:** ↑PT/aPTT, factor deficiency, warfarin reversal **(urgent → 4-factor PCC ก่อน; FFP เมื่อไม่มี PCC)** · **Platelet:** thrombocytopenia/bleeding (20-22°C agitation, ห้ามแช่เย็น) · **Cryo:** fibrinogen<100-150, FXIII; **FVIII/vWF = fallback เมื่อไม่มี factor concentrate เท่านั้น**
- **Irradiate (≥25 Gy central midplane, ≥15 Gy ขั้นต่ำทุกส่วน) — กัน TA-GVHD:** immunocompromised, **intrauterine/exchange/neonate**, **HLA-matched / เลือดจากญาติ (directed)**, Hodgkin, BMT, congenital T-cell defect → ลืม = TA-GVHD เกือบ 100% ตาย
- **Leukoreduce:** ประวัติ **febrile NHTR ซ้ำ**, ลด **HLA alloimmunization** (จะ transplant/platelet refractory), ลด **CMV** (ทารก/ตั้งครรภ์/immunocompromise CMV−)
- **Washed:** IgA deficiency / anaphylaxis ต่อ plasma protein
- ABO: RBC ใช้ O universal ได้ · plasma AB universal · **platelet = ความเสี่ยงอยู่ที่ PLASMA (anti-A,B) ไม่ใช่ RBC** → เลี่ยง high-titer O-platelet plasma เข้าคน A/B (ผู้ใหญ่ด้วย ไม่ใช่แค่เด็ก) · ideal = ABO-identical; ทิศ plasma compat: **AB > A/B > O**

### Fork 6 — transfusion reaction → workup
> **verdict:** หยุดเลือดทันที + KVO saline → clerical recheck + DAT post + ABO ซ้ำ pre/post → ดู hemolysis (pink plasma/urine = intravascular = สงสัย ABO mislabel)

**ทันที:** หยุดเลือด, KVO saline, เช็ค vital + clerical (ถุง vs ผู้ป่วย), แจ้งแพทย์+BB
**lab:** (1) clerical recheck (2) **DAT** post (3) **ABO ซ้ำ** pre+post (4) ดู plasma/urine hemolysis (pink = intravascular)
- ไข้+หนาวสั่น → FNHTR vs เริ่ม acute HTR (แยกด้วย DAT/ABO/hemolysis) · ป้องกัน FNHTR ซ้ำ = leukoreduce
- **ABO-incompat (intravascular):** back/flank pain, hypotension, hemoglobinuria, DIC → เกือบทุกเคสจาก **clerical mislabel**
- **delayed (5-14 วัน, Hb ตก, DAT+, anamnestic anti-Jk/Kidd):** ให้ antigen-neg ครั้งถัดไป
- หายใจลำบาก: **TACO** (overload, BP↑) vs **TRALI** (anti-HLA donor, BP↓, <6 ชม.) · anaphylaxis ทันที → คิด IgA deficiency → washed unit

### Fork 7 — emergency uncrossmatched (O) เมื่อไหร่
> **verdict:** รอ XM ไม่ได้ = **จ่าย O ทันที** + เก็บ pretransfusion sample ก่อนเสมอ → สลับ type-specific เร็วสุดเมื่อยืนยันหมู่

- เลือดออกมาก/shock รอ XM ไม่ได้ → **O RBC** ทันที (หญิงวัยเจริญพันธุ์/เด็ก = **O neg**; ชาย/หญิงสูงอายุ = O pos ได้เมื่อ O neg ขาด)
- เก็บ pretransfusion sample **ก่อน** ให้เลือดเสมอ · แพทย์เซ็น emergency release · ยืนยันหมู่แล้วสลับ type-specific เร็วสุด → full XM ภายหลัง

### Fork 8 — HDN/HDFN: Rh vs ABO (แยกให้ขาด)
> **verdict:** Rh = ครรภ์ที่ 2+, DAT บวกชัด, รุนแรง · ABO = ครรภ์แรกได้ (แม่ O), DAT มักลบ/อ่อน + spherocyte (DAT ลบ ≠ ตัดทิ้ง — ใช้ IAT+smear)

กลไกร่วม: **IgG แม่** ผ่านรก → จับ Ag ทารก (รับจากพ่อ) → ทำลายที่ม้าม → ซีด + indirect hyperbilirubinemia → hydrops/kernicterus
| | **Rh (anti-D)** | **ABO** |
|---|---|---|
| ครรภ์ | **ที่ 2+** (ต้อง sensitize ก่อน) | **แรกได้เลย** (anti-A,B natural IgG) |
| คู่แม่-ลูก | แม่ Rh− ลูก Rh+ | แม่ **O** ลูก A/B |
| ความรุนแรง | มาก | มักเบา |
| **DAT ทารก** | **บวกชัด** | **มักลบ/อ่อน** (Ag น้อยบนเซลล์ทารก) |
| smear | nucleated RBC | **spherocyte** |
- ⚠️ ทารก hemolysis + DAT บวก แต่ไม่ใช่ ABO/Rh + **DAT แม่ลบ** → **Ab หมู่อื่น** (anti-c/E/Kell/Duffy/Kidd) → ID จาก maternal serum · Kell HDN กด erythropoiesis (bili อาจไม่สูงมาก)
- ⚠️ **ABO HDN DAT ลบ ≠ ตัดทิ้ง** — ใช้ IAT + smear (spherocyte); ABO HDN + hydrops = ผิดปกติ หาเหตุอื่น (G6PD/HS)
- **RhIG (anti-D):** แม่ Rh− (พ่อ Rh+) ให้ที่ **~28 wk + หลังคลอด 72 ชม.** (ถ้าลูก Rh+) + หลัง event เสี่ยง FMH (แท้ง/เจาะน้ำคร่ำ/ล้วงรก) · anti-D titer ≥ critical (~1:16) → **MCA-PSV Doppler (>1.5 MoM)** เป็น first-line surveillance (ΔOD450/amniocentesis = legacy)
- ⚠️ **standard dose 300 µg ครอบ FMH ได้แค่ ~30 mL whole blood / 15 mL RBC** — ถ้า FMH มาก (abruption/trauma) ต้อง **Kleihauer-Betke / flow cytometry คำนวณ dose เพิ่ม** มิฉะนั้นแม่ sensitization สร้าง anti-D ทั้งที่ให้ RhIG แล้ว
- **เลือดให้ทารก/exchange:** PRC **O Rh−, low-titer, compatible serum แม่, <5-7 วัน, CMV-neg, leukodepleted, irradiated**; เกินเกณฑ์ bilirubin → exchange, เบากว่า → phototherapy

### Fork 9 — เมื่อไหร่ใช้ molecular (genotype) แทน serology
> **verdict:** serology เชื่อไม่ได้ (เพิ่ง transfuse/DAT บวกแรง/ไม่มี antisera) หรือ fetal RHD จาก maternal plasma → ใช้ genotype

- **เพิ่ง transfuse (mixed-field) / DAT บวกแรง (auto-Ab เคลือบจน type ไม่ได้)** → genotype · **antigen ไม่มี antisera/หายาก** · **fetal RHD typing** จาก maternal plasma/amniotic (กัน HDFN โดยไม่เจาะเด็ก — ถ้าทารก Rh− ก็ไม่ต้องให้ RhIG เกินจำเป็น) · mass screen หา rare phenotype
- เลือก method/แปล qPCR/กัน false +/− → ดู `molecular-judgment` (RFLP จำกัดที่ SNP ต้องตรง restriction site · ASP บอก homo/het · SSO/SSP throughput · SYBR false-pos จาก primer-dimer)
- discrepancy **genotype vs phenotype** (weak D/partial D/Rh variant) = ต้องรู้ทั้งคู่ก่อนตัดสินจ่าย
- ⚠️ **กฎ bench weak-D / Rh discrepancy:** **donor** weak-D → ติดป้าย **Rh-POSITIVE** (กันให้ผู้รับ Rh−) · **patient** weak-D/partial-D → ปฏิบัติเป็น **Rh-NEGATIVE** (สงสัยเมื่อไหร่ จ่าย D-neg ไว้ก่อน โดยเฉพาะหญิงวัยเจริญพันธุ์ — partial-D สร้าง anti-D ได้)

### Fork 10 — Enhancement: enzyme / LISS / adsorption / elution (+ controls)
> **verdict:** เลือก technique ตามเป้า (enzyme=แยก Rh-Kidd vs MNS-Duffy · adsorption=auto vs allo · elution=Ab บนเซลล์เคลือบ) — **ทุกอันต้อง run control** (last-wash/autocontrol)

- **Enzyme (papain/ficin):** enhance **Rh/Kidd/P/Lewis/I** · destroy **MNS/Duffy** → "differential destruction" แยก Ab ปนกัน · ⚠️ ใช้ enzyme cell ตรวจ anti-Fya/M = false negative
- **LISS:** ลด incubate (60-90→10-20 นาที) · ⚠️ **สัดส่วน serum:cell:LISS ตาม leaflet เป๊ะ** — มากไป false+, น้อยไป false−
- **Adsorption** (ดูด Ab ออกจาก serum, แยก auto vs allo): ยืนยัน RBC มี Ag จริง; post-adsorbed serum ต้อง **IAT ลบ** = สำเร็จ
- **Elution** (ดึง Ab จาก RBC เคลือบ DAT บวก → อยากรู้ Ab อะไร: HDN/AIHA/delayed HTR): ⚠️ **last-wash NSS = negative control** — last-wash บวก = ล้างไม่พอ eluate ใช้ไม่ได้

### Fork 11 — Transplant/HSCT support (BB เกี่ยวตรงไหน)
> **verdict:** rejection = ผู้รับตี graft (กันด้วย crossmatch ก่อนปลูก) · GvHD = donor ตีผู้รับ (กันด้วย irradiate + T-cell depletion)

- **GvHD vs rejection (ใครโจมตีใคร):** rejection = ผู้รับโจมตี graft · **GvHD = donor lymphocyte โจมตีผู้รับ** → กันด้วย **irradiate component (Fork 5) + T-cell depletion**
- **Hyperacute rejection = preexisting Ab** (เคยรับเลือด/ตั้งครรภ์/ปลูกถ่าย) → กันด้วย **crossmatch ก่อนปลูกถ่าย**
- **HLA matching HSCT:** A/B/C/DRB1 = **8/8**, +DQB1 (10/10) ยิ่งดี; ลำดับ sib-identical → unrelated → haplo/cord
- **ABO-incompatible graft:** RBC-deplete (major) / plasma-reduce; post-transplant **monitor ABO Ab titer**; CD34+ count (flow) = quantify progenitor

### Fork 12 — Delayed/late reactions (ที่ตาราง acute ไม่ครอบ)
> **verdict:** Hb ตก 5-14 วัน + DAT+ = **DHTR (anamnestic, Kidd บ่อยสุด)** → ครั้งหน้าให้ Ag-neg · pancytopenia 1-3 wk = **TA-GVHD** (ตายเกือบแน่ ป้องกันทางเดียว=irradiate) · plt ตก ~1 wk = **PTP**

- **DHTR/DSTR (anamnestic):** เคย sensitize → titer ตกจน **screen ลบตอนเตรียมเลือด** → ได้ Ag-positive unit → boost ใน 3 วัน-สัปดาห์ → hemolysis · ความถี่ **Kidd > Duffy > Kell > MNS** (Jka titer drop ง่ายสุด); DSTR (ไม่มี hemolysis marker) พบบ่อยกว่า DHTR · **ป้องกัน: ใช้ตัวอย่าง ≤3 วันก่อนจ่าย + บันทึก Ab เก่า → เลี่ยง Ag เดิมแม้ screen ลบ**
- **TA-GVHD:** donor lymphocyte ตี recipient → **marrow aplasia/pancytopenia → ตาย 1-3 สัปดาห์, รักษาแทบไม่ได้ → ป้องกันทางเดียว** · ⚠️ **เลือดญาติ (directed) = เสี่ยงสูงสุด** (one-way HLA: donor homozygous ตรงกับ recipient heterozygous → **คนภูมิปกติก็เป็นได้**) → **irradiate 25 Gy เสมอ; leukoreduction อย่างเดียวไม่กัน**
- **PTP (post-transfusion purpura):** เกล็ดตกฮวบ **~1 สัปดาห์** หลังเลือด, หญิงเคยตั้งครรภ์, Ab = **anti-HPA-1a** (ทำลายเกล็ดตัวเอง HPA-1a-neg ด้วย) · DDx ITP/HIT/DIC/drug — ธง = ก่อนเลือด plt ปกติ · รักษา **IVIG** (ดีสุด), หลีกเลี่ยง platelet transfusion เพิ่ม (ทำให้แย่ลง); ถ้าจำเป็นตอนเลือดออกรุนแรง ใช้ HPA-1a-negative platelet
- **Iron overload:** RBC 1 unit ≈ Fe 200-250 mg, ขับได้ ~1 mg/วัน → สะสมตับ/หัวใจ · 🩸 **thalassemia/chronic transfusion เสี่ยงตายจากเหล็ก > จากซีด** → ติดตาม ferritin + chelator (deferiprone เสี่ยง agranulocytosis · deferasirox กินวันละครั้ง)
- **Hemovigilance:** reaction ส่วนใหญ่พลาดเพราะ "ไม่สังเกต" + "ไม่รายงาน" → ต้องมีระบบรายงาน; เคสตายแจ้งหน่วยกำกับ

### Fork 13 — Special techniques: เลือก potentiator + ลบ/แยก Ab (ทุกอันต้องมี autocontrol)
> **verdict:** เลือกตามตัวกวน (IgM บัง→DTT · cold→prewarm 37°C · warm DAT+→adsorption) + ระวังตัว reagent ทำลาย Ag ที่อยากตรวจ (DTT→Kell · enzyme→MNS/Duffy) — **autocontrol คู่เสมอ**

- **ปฏิกิริยาอ่อน → potentiator:** **LISS** (routine; ต้องมี glycine; **ห้ามใน titration**) · **PEG** (IgG ดีมาก · ⚠️ **ห้ามปั่นหลังเติม** + **ยับยั้ง IgM** ABO/Lewis) · **Polybrene** (เร็ว · ⚠️ **ใช้กับ Kell ไม่ได้**) · Albumin (เลิกใช้แล้ว — AHG พอ)
- **Ab รบกวน → ลบ/แยก (ตามชนิดตัวกวน):** IgM บัง IgG → **DTT/2-ME** (⚠️ DTT ทำลาย **Kell** ด้วย) · cold autoAb → **prewarmed 37°C** · warm autoAb (DAT+) → **adsorption** · IgG เคลือบจน type Ag ไม่ได้ → **chloroquine** (⚠️ ไม่ลบ complement → อ่านด้วย anti-IgG monospecific; ห้ามเกิน 2 ชม.) · Ab จริงหรือ non-specific → **inhibition** (soluble Lewis/P1/Sd + saline control)
- ⚠️ **ทุก enhancement/เทคนิคพิเศษ (prewarmed/cold/low-pH/enhance) ต้องรัน autocontrol คู่เสมอ** — ไม่งั้นแยก auto vs allo (เช่น anti-I บัง) ไม่ออก

---

## กับดัก (Anti-patterns) — อันตราย เช็คทุกเคส
- **ABO mislabel = fatal acute hemolysis** → clerical / ติดป้ายข้างเตียง / 2-sample ABO ก่อน serology เสมอ (กับดักที่ฆ่าคนจริงสุด)
- **Bombay หลุดเป็น group O** → routine เหมือน O แต่ anti-H แรง (37°C IgM); จ่าย O = acute intravascular hemolysis · เบาะแส = XM ไม่เข้ากับ O **ทุก** unit
- **prozone / anti-H บัง** → Ab เข้มทำ reaction อ่อนลวง → เจือจาง/ดู supernatant
- **cold autoAb บังทุกอย่าง** → prewarm 37°C ก่อนสรุป; อย่าทิ้ง alloantibody ที่ซ่อนใต้ cold-auto
- **missed clinically-significant Ab** (Kell/Duffy/Kidd/Ss = IgG, AHG) → screen 3 phase, rule-out homozygous, อย่าหยุดที่ระบบไม่สำคัญ (Lewis/P1/M/N)
- **anti-Jk anamnestic** → screen ลบ ≠ ปลอดภัย; titer ตกแล้วกลับเร็ว = delayed HTR → เช็คประวัติ Ab เก่าเสมอ
- **ลืม irradiate กลุ่มเสี่ยง TA-GVHD** (neonate/directed-relative/HLA-matched/immunocompromised) = ตายเกือบแน่
- **Daratumumab (anti-CD38) interfere panel** → pan-reactive IAT ลวงใน myeloma → DTT-treated cell + phenotype/genotype ก่อนเริ่มยา
- **DAT false neg จากล้างไม่พอ** → CCC ยืนยันทุก negative AHG
- **rouleaux อ่านเป็น true agglutination** → saline replacement แยก
- **platelet แช่เย็น / RBC นอกตู้** = storage lesion (RBC 1-6°C, platelet 20-22°C agitation, thawed plasma ใช้ใน 4 ชม. ห้าม refreeze)
- **ตัด ABO HDN ทิ้งเพราะ DAT ลบ** → DAT มักลบ/อ่อน; ใช้ IAT + spherocyte smear · ทารก DAT+ ที่ไม่ใช่ ABO/Rh = หา Ab หมู่อื่นจาก serum แม่
- **ลืม control ของ enhancement** → last-wash NSS (elution) / สัดส่วน LISS ผิด = อ่าน eluate/reaction ผิดทั้ง run
- **parentage จาก serology = exclude ได้เท่านั้น ไม่ confirm** — "ไม่ขัด" ≠ "เป็นพ่อ"; ยืนยันความเป็นพ่อต้อง molecular/STR
- **passive anti-A,B จาก O component อ่านเป็น auto/alloAb** → เช็ค Hx ได้ platelet/plasma หมู่ O ก่อน (DAT+/eluate anti-A,B)
- **TA-GVHD จากเลือดญาติ (one-way HLA match)** = เสี่ยงสุด คนภูมิปกติก็เป็น → **irradiate เสมอ**; leukoreduction ไม่กัน
- **PTP (เกล็ดต่ำ ~1 สัปดาห์, anti-HPA-1a)** สับกับ ITP/HIT/TA-GVHD → ธง: ก่อนเลือด plt ปกติ; รักษา IVIG (first line), หลีกเลี่ยง platelet transfusion เพิ่ม (ทำให้แย่ลง); ถ้าจำเป็นตอนเลือดออกรุนแรง ใช้ HPA-1a-negative platelet
- **เลือกสารพิเศษผิด → ลบ Ag ที่อยากตรวจ** — DTT ทำลาย Kell · chloroquine ทำลาย HLA-I/Rh · enzyme ทำลาย MNS/Duffy
- **PEG ห้ามปั่น / ห้ามใช้กับ IgM (ABO/Lewis) · Polybrene ใช้กับ Kell ไม่ได้ · LISS ห้ามใน titration**
- **ลืม autocontrol ในเทคนิคพิเศษ** (prewarmed/cold/low-pH/enhance) → แยก cold-auto vs allo ไม่ออก

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติม war-story หน้า bench จริง เช่น:
> - *"(MT BB) เคส ABO discrepancy ที่ผมเจอจริง คือ... resolve โดย..."*
> - *"เคสที่เกือบจ่ายเลือดผิด จับได้เพราะ clerical/anti-H ตรง..."*
> - *(สาย sales) เทคนิคหน้างาน → product: gel/CAT = Ortho/Bio-Rad · SPRCA = Immucor · HLA SSO = One Lambda/Thermo · NAT/molecular = Grifols/Roche*

---
*เครื่องมือช่วยคิดหน้างานธนาคารเลือดเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ใช่ผู้ตัดสินใจแทน งาน BB เกี่ยวชีวิตคนไข้โดยตรง ต้องทำตาม SOP, ยืนยันกับ MT/แพทย์, อ้างมาตรฐาน AABB/ศูนย์อ้างอิงเสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
