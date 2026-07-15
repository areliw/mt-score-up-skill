---
skill: hematology-judgment
title: ตัวช่วยตัดสินใจในแล็บโลหิตวิทยา (Hematology Judgment)
type: ADVISE
needs: any
author: "Phanuphong Tameesak - MT Score UP!"
contributors: ["สมาชิกแห่งความมืด–องค์กรลับแห่งรัตติกาล — graft กับดัก pseudothrombocytopenia (Fork 4)"]
last_edited: 2026-07-16
status: draft
disclaimer: "skill นี้ช่วย 'คิด' เพื่อการศึกษา ไม่ตัดสินใจแทนและไม่วินิจฉัยแทนผู้ป่วย · blast / ค่าวิกฤต = เร่งด่วน ต้องแจ้งแพทย์ทันที · ทุกผลที่กระทบการรักษาต้อง review smear ด้วยตา + ยืนยันกับ MT ผู้รับผิดชอบ/แพทย์ก่อนรายงาน · AI อาจผิดได้ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ตัวช่วยตัดสินใจในแล็บโลหิตวิทยา

ตัวช่วยตัดสินใจในแล็บโลหิตวิทยา — เน้น "ผล CBC/smear/coag นี้ ต้องทำอะไรต่อ + อย่าพลาดตรงไหน" ไม่ใช่ atlas รูปเซลล์หรือตารางค่าปกติ

> **กฎ #1:** ทุกผลที่กระทบการรักษา (blast, platelet ต่ำ) **ต้อง review smear ด้วยตาก่อน report เสมอ** — flag จากเครื่อง = สัญญาณ ไม่ใช่คำตอบ
> **กับดัก #1 (ขั้น hard):** ตัวเลข/flag เครื่อง "ปกติ" ≠ smear ปกติ — เครื่องนับ blast เป็น lymph/mono ได้ ปล่อย acute leukemia ทั้งที่ WBC ปกติ. **เลขปกติแต่อาการ/บริบทค้าน = ยังต้อง smear** อย่าให้ "ไม่มี flag" เป็นใบผ่าน

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- เห็น CBC/analyzer flag → ต้อง review smear ด้วยตามั้ย? reflex test อะไร?
- วาง anemia workup · แยก thal vs IDA · เจอ blast/abnormal cell · platelet ต่ำ จริงหรือ artifact
- แปล PT/aPTT + ตัดสินใจ mixing test · ESR/abnormal flag
- (สาย sales) เตรียมขาย hematology analyzer หรือออกแบบ screening logic สำหรับงานวิจัย (RBC/Hb/thalassemia)

## วิธีใช้
วาง skill นี้ + ผล CBC/smear/coag (หรือ analyzer flag) ที่กำลังตัดสินใจ → AI เดินตาม fork ด้านล่าง บอกว่า "ต้องทำอะไรต่อ + กับดักตรงไหน" แล้วชี้กลับให้คน review smear + ยืนยันเอง

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### ก่อนแปลผลเสมอ — ดู 3 อย่าง
1. ตัวอย่าง OK มั้ย — clot? hemolysis? lipemia? เก็บนานเกิน? (pre-analytical = error ~60-70%)
2. บริบทคน — อายุ/เพศ/ตั้งครรภ์/ประวัติ transfusion/ยา (warfarin, heparin, aspirin)
3. เทียบของเดิม (delta check) + correlate ค่า analyzer กับ smear

### Fork 1 — CBC flag → เมื่อไหร่ "ต้อง" review smear ด้วยตา
Review smear เสมอเมื่อ:
- blast flag / "abnormal/immature cell" / WBC สูงมากผิดปกติ → smear ทันที
- platelet ต่ำ → ห้ามรายงานเลย ดู clump ก่อน
- MCHC > 36–37 → smear ตรวจ. ส่วนใหญ่ **artifact** (cold agglutinin / lipemia / hyperbili / paraprotein → เครื่องเชื่อไม่ได้ แก้แล้ว rerun) แต่ **hereditary spherocytosis = MCHC สูงจริง** (เสีย membrane จริง ไม่ใช่ปลอม) → ดู spherocyte + ยืนยัน อย่าปัดทิ้งเป็น error
- WBC สูงแต่ค้านอาการ → NRBC/cryoglobulin นับเป็น WBC ปลอม → smear + แก้ค่า
- RBC indices ไม่ลงรอย (MCV ต่ำมากแต่ RDW ปกติ) → smear ยืนยัน + คิด thal
- delta check fail → smear + คิด sample mix-up/artifact

หลัก: flag ที่กระทบการรักษาทันที (blast, plt ต่ำจริง) = smear ก่อน report เสมอ

### Fork 2 — Anemia workup เดินตาม MCV ก่อน
- Microcytic (MCV < 80): IDA / thal / chronic dz / sideroblastic → reflex Fe studies (ferritin) + ถ้าสงสัย thal → OFT/DCIP → Hb typing. RDW + RBC count ช่วยฟันธง · (lead = normo-to-microcytic + basophilic stippling — ไม่ใช่ pure microcytic cause; เบาะแสคือ stippling + ประวัติสัมผัสตะกั่ว)
- Normocytic (80–100): ดู retic ก่อน — retic สูง / RPI ≥2 → hemolysis/acute blood loss → reflex hemolysis panel (LDH, bilirubin, haptoglobin, DAT); retic ต่ำ / RPI <2 → hypoproliferative (chronic dz/CKD/aplastic/early IDA)
- Macrocytic (MCV > 100): B12/folate / liver / alcohol / MDS / reticulocytosis (macro เทียม) → reflex retic ก่อน — retic สูง = macro เทียมจาก hemolysis; retic ปกติ → B12/folate + smear (hypersegmented neutrophil)

เมื่อไหร่ reflex retic: normo/macro ทุกราย. เมื่อไหร่ reflex Hb-typing: micro ที่ Fe ปกติ/RBC สูง/RDW ปกติ.

### Fork 3 — เจอ blast / abnormal cell → URGENT escalate
- blast บน smear = critical/urgent → แจ้งแพทย์ทันที + ไม่ auto-release; ส่ง bone marrow + cytochemistry/flow
- แยก lineage: MPO/SBB + → myeloid (AML) · MPO − + PAS block + → lymphoid (ALL) · NSE + (ยับยั้งด้วย NaF) → monocytic
- ⚠️ **Auer rod / "faggot cell" (Auer หลายอันมัดรวม) → สงสัย APL (AML-M3, t(15;17))** = leukemia ที่ฉุกเฉินสุดเพราะมาคู่ **DIC/เลือดออกรุนแรง** → flag แพทย์ + ส่ง **coag (PT/aPTT/fibrinogen/D-dimer)** ทันที ไม่รอ confirm marrow
- WBC สูงมาก: CML (full myeloid spectrum + baso/eos, LAP ต่ำ <20) vs leukemoid reaction (toxic granule, LAP สูง >100)

### Fork 4 — Platelet ต่ำ → "จริงหรือ pseudo"
0. เช็คก่อนเชื่อเลขเครื่อง: **QC วันนั้นผ่านไหม · หลอด partial clot / mix ไม่ดีไหม** (สาเหตุค่าต่ำปลอมที่พบบ่อยสุด) · **delta check เทียบประวัติเก่า**
1. ดู smear หา platelet clump (feather edge) — มี clump = EDTA-induced pseudothrombocytopenia
2. **ทำ platelet estimation จาก smear cross-check ค่า analyzer** (เฉลี่ยหลาย OIF ในเขต monolayer × factor ที่แล็บ validate, ทั่วไป ~15–20k) — estimate ค้าน analyzer มาก = สงสัย clump/clot/artifact ก่อนเชื่อเลข
3. clump → เก็บใหม่ใน citrate (3.2%) แล้วคูณ dilution factor หรือ heparin tube → รายงานค่าแก้
4. ไม่มี clump + estimate สอดคล้อง + smear ยืนยันต่ำจริง → รายงาน + ต่ำมาก = critical แจ้งแพทย์ตาม SOP

ห้าม auto-report plt ต่ำจาก analyzer โดยไม่ดู smear.

### Fork 4B — Platelet "สูงลวง" (spurious thrombocytosis): ชิ้นส่วน RBC ถูกนับเป็นเกล็ดเลือด
กระจกเงาของ Fork 4 — เครื่องรายงาน plt **สูง**เกินจริง (เคสจริงเคยพบ >1,000 ×10⁹/L ที่ไม่เข้ากับคลินิก โดยเฉพาะ **severe burn / ภาวะที่มี RBC fragment เยอะ**):
0. เช็คก่อน: plt สูงค้านคลินิก / delta check กระโดด = ตั้งข้อสงสัย อย่าเพิ่งเชื่อเลขเครื่อง
1. 🔑 **กลไก:** schistocyte / microspherocyte / RBC fragment (burn ทำ spectrin เสียสภาพ · MAHA/DIC · severe microcytosis) ขนาดใกล้เกล็ดเลือด → **impedance นับรวมเป็น platelet** → สูงลวง · optical-scatter ธรรมดาก็ยังแยกไม่หมดในบางราย
2. 🔑 **จับได้ยังไง:** ดู **platelet histogram/scattergram** ผิดปกติไหม + **review smear** → platelet estimate + หา RBC fragment/schistocyte/microspherocyte
3. ✅ **ยืนยัน:** เครื่องมี **optical fluorescent platelet count (ย้อม RNA)** = จำเพาะกว่า impedance/optical-scatter → ใช้ตัวนี้ · ไม่มี → manual count / วิธีอ้างอิงตามศักยภาพแล็บ + แจ้งแพทย์เจ้าของเคส
4. 🚫 **อย่า auto-report plt สูงลวง** — อาจกลบ thrombocytopenia จริงที่ผู้ป่วยต้องได้เกล็ดเลือด (โยง กฎ #1: flag เครื่อง = สัญญาณ ไม่ใช่คำตอบ)

### Fork 5 — Thalassemia vs IDA
- เบาะแส: Mentzer MCV/RBC < 13 → thal (RBC สูง), > 13 → IDA · thal มัก RDW ปกติ + RBC count สูง · IDA มัก RDW สูง + RBC ต่ำ + ferritin ต่ำ
- ยืนยัน: thal → HbA2 (HPLC/CZE) สูง = β-thal trait · IDA → ferritin/Fe panel
- IDA กด HbA2 ลง → ต้องแก้ IDA ก่อนวัด HbA2 ไม่งั้น false negative
- screening flow: OFT + MCV/MCH + DCIP → positive → Hb typing → สงสัย α⁰/severe → DNA (Gap-PCR ↔ α deletion, ARMS ↔ β point)
- แยก HbA2 จาก HbE: CZE (Sebia) แยกได้, HPLC co-elute.

### Fork 6 — Coagulation: PT/aPTT pattern → mixing test
- PT ยาวเดี่ยว → FVII (early warfarin/vit K/liver)
- aPTT ยาวเดี่ยว → hemophilia A/B, vWD, heparin, lupus anticoagulant
- PT + aPTT ยาว, TT ปกติ → FX/V/II, liver, vit K def
- PT + aPTT + TT ยาว → DIC / afibrinogenemia (fibrinogen + D-dimer)
- CBC + PT/aPTT ปกติ แต่เลือดออกจริง → mild factor (>5%), FXIII def, fibrinolysis
- mixing test: PT/aPTT ยาว → mix 1:1 normal plasma → corrected = factor deficiency; not corrected = inhibitor (FVIII inhibitor / lupus anticoagulant)
- snake bite: 20-min WBCT ไม่แข็ง = viperine; Russell's → DIC.
- ⚠️ 🩸 **Bleeding time (BT — Duke/Ivy) ไม่แนะนำเป็น pre-op bleeding screen แล้ว:** ทำนายเลือดออกตอนผ่าตัดจริงได้ไม่ดี + ไม่ standardize (Duke ไม่คุมความดัน/ขนาด-ความลึกแผล → variability สูง) + ไวต่ำ (mild platelet dysfunction/mild (type 1) vWD พลาด) · แนวทางปัจจุบันยึด **ประวัติเลือดออก + coag/platelet-function test ที่เหมาะ** (เช่น PFA/ตรวจจำเพาะ) แทน · *ถ้าหน่วยยังมี order ก็ทำตาม SOP แต่รู้ข้อจำกัด — verify guideline ฉบับที่ถือใช้*

### Fork 7 — ESR / abnormal flag = prognostic ไม่ใช่ diagnostic
- ESR สูง → บอก "มีอักเสบ" ไม่ชี้โรค → ติดตาม; เช็ค rouleaux/anemia ที่ดันค่า
- heparin ห้ามใช้กับ ESR; Westergren = citrate 4:1

## กับดัก (Anti-patterns)
- #1 Miss blast: ปล่อย CBC flag ผ่านเครื่องไม่ review smear → ปล่อย acute leukemia.
- #2 Platelet clump = pseudothrombocytopenia: อย่ารายงาน plt ต่ำจาก analyzer โดยไม่ดู clump.
- #3 เลือก anemia path ผิด: ไม่ดู MCV (+ RDW + retic) ก่อน.
- #4 Thal/IDA สับสน: Mentzer + RDW + RBC count + ferritin; IDA กด HbA2 → confirm β-thal ต้องแก้ Fe ก่อน.
- #5 Clotted / partial-clot sample: plt ต่ำปลอม + CBC เพี้ยน → ตรวจ clot/feather edge ก่อน.
- #6 Cold agglutinin: MCHC สูงปลอม (>36–37) + RBC ต่ำปลอม → อุ่น 37°C 30 นาที แล้ว rerun. แต่อย่าเหมา MCHC สูงทุกตัวเป็น artifact — spherocytosis คือสูงจริง.
- #7 Lipemia → Hb สูงปลอม (saline replacement); NRBC/cryoglobulin → WBC สูงปลอม.
- #8 MCV เกิน 100 = B12 ทุกราย (ผิด): retic สูง = macro เทียมจาก hemolysis — ดู retic ก่อน.
- #9 รายงาน PT/aPTT "ปกติ" แล้วจบทั้งที่เลือดออก: คิด FXIII def / mild factor / vWD / fibrinolysis.
- #10 Pre-analytical ละเลย: tourniquet นาน, blood:anticoag ผิด (coag 1:9 + แก้ตาม Hct >55), hemolysis.
- #11 🩸 ใช้ Bleeding time (Duke/Ivy) เป็น pre-op bleeding screen / เชื่อว่า normal = ผ่าตัดปลอดภัย → BT ทำนาย surgical bleeding ไม่ได้ + ไวต่ำ (vWD/mild dysfunction พลาด); ยึดประวัติ + test จำเพาะ (Fork 6).

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - SOP ของแล็บคุณกำหนด smear-review criteria / critical-value list / delta-check rule ไว้อย่างไร? (เติมให้ตรงเครื่องและ policy จริง)
> - analyzer รุ่นที่ใช้ (เช่น Sysmex/Beckman) มี flag เฉพาะตัวไหนที่ทีมตีความต่างจาก default?
> - screening flow thalassemia / reflex algorithm ในพื้นที่คุณ ต่างจากที่ระบุไว้ตรงไหน (cut-off, DNA referral)?

NOTE: knowledge (MCV/MCH/MCHC/RPI formulas, OFT/DCIP principles, thal genotype tables, cytochemistry stains) → ดู "ตำรา/แหล่งอ้างอิงมาตรฐาน" ไม่ใช่หน้าที่ของ skill นี้

---
*skill นี้เป็นตัวช่วย "คิด" เพื่อการศึกษา ไม่ใช่ตัวตัดสินใจหรือวินิจฉัยแทน · blast / ค่าวิกฤต = เร่งด่วน แจ้งแพทย์ทันที · ทุกผลที่กระทบการรักษาต้อง review smear + ยืนยันกับ MT ผู้รับผิดชอบ/แพทย์ก่อนรายงาน · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
