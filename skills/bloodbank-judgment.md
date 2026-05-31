---
skill: bloodbank-judgment
title: โค้ชธนาคารเลือด — ตัดสินใจหน้างาน ไม่ให้คนไข้ตาย (Blood Bank Judgment)
type: ADVISE               # ช่วยตัดสินใจหน้า bench ไม่ใช่ตำรา antigen frequency
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
reviewed: 2026-06-01
status: draft
disclaimer: "เครื่องมือช่วยคิดหน้างานธนาคารเลือดเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ใช่ผู้ตัดสินใจแทน งาน BB เกี่ยวชีวิตคนไข้โดยตรง ต้องทำตาม SOP, ยืนยันกับ MT/แพทย์, อ้างมาตรฐาน AABB/ศูนย์อ้างอิงเสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชธนาคารเลือด — ตัดสินใจหน้างาน ไม่ให้คนไข้ตาย

ตัดสินใจหน้า bench ธนาคารเลือด — **"เลือกอะไรเมื่อไหร่ + พลาดตรงไหนถึงคนตาย"** ไม่ใช่ท่องตาราง antigen frequency (นั่นคือ commodity ดูตำรา)

> งาน BB คือจุดที่ "ตัดสินใจผิด = คนไข้ตาย" ตรงไปตรงมาที่สุดในวิชาชีพ MT — **ABO mislabel = สาเหตุ #1 ของ fatal acute hemolytic reaction**. skill นี้จึงนำด้วยความปลอดภัย: clerical ก่อน serology เสมอ

## ใช้เมื่อ
- ABO ไม่ตรง (cell ≠ serum) · antibody screen บวก → จะ ID ยังไง · DAT/IAT อันไหน · crossmatch แบบไหน
- เลือก component / เมื่อไหร่ irradiate / leukoreduce · transfusion reaction → workup · ฉุกเฉินจ่าย O เมื่อไหร่

## วิธีใช้
วาง skill นี้ + เล่าเคส (ผล forward/reverse, screen, ประวัติ) → AI ชี้ "ทำอะไรก่อน" + กับดักอันตราย

---

## กฎเหล็กก่อนทุกอย่าง — CLERICAL ก่อนเสมอ
ผลแปลก / เข้ากันไม่ได้ / reaction → **เช็ค clerical ก่อนคิด serology**: ชื่อ-HN ถูกคน? หลอดติดป้ายถูก? sample เก่า/clot/hemolyze? group เดิมในประวัติตรงไหม? — แก้ที่ serology ก่อนตัด clerical = พลาดที่อันตรายสุดของทั้งวิชา

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — decision forks

### Fork 1 — ABO discrepancy (cell ≠ serum) → resolve ยังไง
**ลำดับเสมอ:** (1) ทำซ้ำ + ล้าง RBC ตัด technical error (2) เก็บ sample ใหม่ + ถาม Dx/อายุ/transfusion-transplant/ยา (3) แยกปัญหาที่ **RBC (forward)** หรือ **serum (reverse)** → WEAK/MISSING/EXTRA

| เคส | เบาะแส | resolve | จ่ายเลือด |
|---|---|---|---|
| **Acquired B** (RBC extra) | group A + มะเร็งลำไส้/septicemia (E.coli) | anti-B acidified pH6, autocontrol (ตัวเองไม่จับ) | **group A** (หมู่จริง) |
| **B(A)/A(B)** (RBC extra) | weak extra reaction | molecular/ref lab ยืนยัน | ตามหมู่จริง |
| **Mixed-field** (RBC) | บางเซลล์จับ; post-BMT / ได้ O เยอะ / A3 | ดูประวัติ transfuse-transplant + titer | ฉุกเฉิน **O** ก่อน |
| **anti-A1** (serum extra) | A2/A2B reverse จับ A1 cell | A1 vs A2 cell + **anti-A1 lectin (Dolichos)** | **A2 หรือ O** |
| **Cold autoAb** (serum extra) | anti-I/IH; **screen+ AND auto+** | **prewarm 37°C** / cold autoadsorption | warm Ab ที่เหลือ |
| **Rouleaux** (serum) | โปรตีนสูง (myeloma), "stack of coins" | **saline replacement** | ตามหมู่จริง |
| **anti-H / Bombay** (serum extra) | screen+, **auto−**, จับ O cell แรง; XM ไม่เข้ากับ O ใครเลย | ยืนยัน Bombay RBC + saliva | **เลือด Bombay เท่านั้น** |
| **Missing/weak Ab** (serum) | ทารก/สูงอายุ/hypogamma/BMT/myeloma | incubate RT/4°C นานขึ้น + autocontrol | ตามหมู่ที่ยืนยันได้ |

### Fork 2 — antibody screen บวก → ID strategy
- **อ่าน autocontrol ก่อน:** auto− = **allo**antibody (panel ID ปกติ) · auto+ → คิด AIHA/cold-auto/recent transfusion ก่อน
- **rule-out บน panel:** ขีดฆ่า antigen ที่ "cell ลบแต่ reaction บวก" → เหลือตัวที่ fit ทุกแถว = candidate; **ต้อง rule-out ด้วย homozygous cell** (เลี่ยง dosage บัง)
- **dosage:** anti-Jk/Rh/Duffy/Kell/MNS จับ homo แรงกว่า het → het cell อ่าน "ลบลวง" ได้
- **enzyme (ficin/papain):** Rh/Kidd/P/Lewis **เด่นขึ้น** · MNS/Duffy **ถูกทำลาย** → ใช้แยก 2 ระบบทับกัน
- **multiple/pan-react:** ไม่ fit ตัวเดียว → selected cell + enzyme + เผื่อ HTLA/HFA → ส่ง ref lab (ศูนย์อ้างอิงระดับชาติ)

### Fork 3 — DAT vs IAT เมื่อไหร่
- **DAT** = RBC ถูกเคลือบ in vivo → สงสัย **AIHA / HDFN (cord) / HTR / drug-induced**; sample = **EDTA whole blood**
- **IAT** = Ab ในซีรั่มจับ antigen in vitro → **antibody screen/ID, crossmatch AHG, phenotyping, weak D**; sample = **serum/plasma สด**
- "ทำไม transfusion reaction" → DAT บวกหลังให้เลือด = สงสัย HTR → DAT + clerical + ABO ซ้ำ pre/post
- **QC พลาดบ่อย:** AHG ออก negative ต้องหยอด **CCC (Coombs Control Cell)** — CCC ไม่จับ = ล้างไม่พอ → test ใช้ไม่ได้

### Fork 4 — crossmatch ไหน (IS / AHG / electronic)
| สถานการณ์ | crossmatch |
|---|---|
| screen ลบ + ไม่มีประวัติ Ab + ยืนยัน ABO 2 ครั้ง | **electronic / immediate-spin** พอ |
| screen บวก / มีประวัติ clinically-sig Ab | **full AHG XM** + antigen-negative unit |
| cold autoAb / Bombay / anti-H บัง | **prewarmed 37°C** |
| ฉุกเฉินไม่ทันรอ | **O uncrossmatched** (ดู Fork 7) |
> ⚠️ เคยมี clinically-sig Ab แม้ตอนนี้ screen ลบ (titer ตก) → **ยังต้องให้ antigen-neg + AHG XM** (anti-Jk anamnestic = delayed HTR)

### Fork 5 — component selection + เมื่อไหร่ irradiate/leukoreduce
- **PRC:** anemia/thalassemia · **FFP:** ↑PT/aPTT, factor deficiency, warfarin reversal · **Platelet:** thrombocytopenia/bleeding (20-22°C agitation, ห้ามแช่เย็น) · **Cryo:** fibrinogen<100-150, FVIII, vWF, FXIII
- **Irradiate (25 Gy) — กัน TA-GVHD:** immunocompromised, **intrauterine/exchange/neonate**, **HLA-matched / เลือดจากญาติ (directed)**, Hodgkin, BMT, congenital T-cell defect → ลืม = TA-GVHD เกือบ 100% ตาย
- **Leukoreduce:** ประวัติ **febrile NHTR ซ้ำ**, ลด **HLA alloimmunization** (จะ transplant/platelet refractory), ลด **CMV** (ทารก/ตั้งครรภ์/immunocompromise CMV−)
- **Washed:** IgA deficiency / anaphylaxis ต่อ plasma protein
- ABO: RBC ใช้ O universal ได้ · plasma AB universal · platelet เลี่ยง ABO-incompat plasma ในเด็ก

### Fork 6 — transfusion reaction → workup
**ทันที:** หยุดเลือด, KVO saline, เช็ค vital + clerical (ถุง vs ผู้ป่วย), แจ้งแพทย์+BB
**lab:** (1) clerical recheck (2) **DAT** post (3) **ABO ซ้ำ** pre+post (4) ดู plasma/urine hemolysis (pink = intravascular)
- ไข้+หนาวสั่น → FNHTR vs เริ่ม acute HTR (แยกด้วย DAT/ABO/hemolysis) · ป้องกัน FNHTR ซ้ำ = leukoreduce
- **ABO-incompat (intravascular):** back/flank pain, hypotension, hemoglobinuria, DIC → เกือบทุกเคสจาก **clerical mislabel**
- **delayed (5-14 วัน, Hb ตก, DAT+, anamnestic anti-Jk/Kidd):** ให้ antigen-neg ครั้งถัดไป
- หายใจลำบาก: **TACO** (overload, BP↑) vs **TRALI** (anti-HLA donor, BP↓, <6 ชม.) · anaphylaxis ทันที → คิด IgA deficiency → washed unit

### Fork 7 — emergency uncrossmatched (O) เมื่อไหร่
- เลือดออกมาก/shock รอ XM ไม่ได้ → **O RBC** ทันที (หญิงวัยเจริญพันธุ์/เด็ก = **O neg**; ชาย/หญิงสูงอายุ = O pos ได้เมื่อ O neg ขาด)
- เก็บ pretransfusion sample **ก่อน** ให้เลือดเสมอ · แพทย์เซ็น emergency release · ยืนยันหมู่แล้วสลับ type-specific เร็วสุด → full XM ภายหลัง

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

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติม war-story หน้า bench จริง เช่น:
> - *"(MT BB) เคส ABO discrepancy ที่ผมเจอจริง คือ... resolve โดย..."*
> - *"เคสที่เกือบจ่ายเลือดผิด จับได้เพราะ clerical/anti-H ตรง..."*
> - *(สาย sales) เทคนิคหน้างาน → product: gel/CAT = Ortho/Bio-Rad · SPRCA = Immucor · HLA SSO = One Lambda/Thermo · NAT/molecular = Grifols/Roche*

---
*เครื่องมือช่วยคิดหน้างานธนาคารเลือดเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ใช่ผู้ตัดสินใจแทน งาน BB เกี่ยวชีวิตคนไข้โดยตรง ต้องทำตาม SOP, ยืนยันกับ MT/แพทย์, อ้างมาตรฐาน AABB/ศูนย์อ้างอิงเสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
