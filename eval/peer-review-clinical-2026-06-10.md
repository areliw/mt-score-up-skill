# Clinical peer-review — 4 สกิลคลินิกใหม่ (2026-06-10)

> **นี่คือ AI peer-review (pre-screen) ไม่ใช่การเซ็นรับรองโดย MT ผู้มีใบประกอบฯ.** ทำหน้าที่จับ error/landmine ก่อนปล่อย public แบบเดียวกับ [`../docs/audit-2026-06-03.md`](../docs/audit-2026-06-03.md) (ที่เคยจับ Bombay/anti-H could-kill ได้จริง) — **แต่ยังไม่แทนรอบที่ MT คนที่สองในสายนั้นตรวจ.** ทั้ง 4 สกิลยังคง `status: draft`.

**Method:** 4 agent (สวมบทบาท MT อาวุโสต่อสาขา) รีวิว adversarial เทียบมาตรฐานปัจจุบัน (CLSI GP16/GP41-PRE02/H21 · ISO 15189:2022 · ISO 15197 · ICCS/ICSH flow · FDA glucose-meter warnings) → maintainer apply เฉพาะ finding ที่ชัด+high-confidence+cite ได้ · ที่เหลือ flag ไว้ให้ MT รีวิว.

**Result:** 1 error จริง (preanalytical Mg) + landmine ที่ขาด 5 จุด → แก้แล้ว · urinalysis ผ่านสะอาด · **0 critical ที่นำไป misdiagnosis ทันที**

---

## preanalytical-judgment — ⚠️ 1 error → แก้แล้ว
- **[CRITICAL → FIXED]** Fork 1: "EDTA carryover → Mg**↑**" ผิด. EDTA chelate Mg → **Mg↓** (กลไกเดียวกับ Ca↓) + ALP↓ (ดึง Zn/Mg cofactor). ขัดกับ Fork 3 ในไฟล์เอง (hemolysis → Mg↑ ถูก). *(Gama/Ford, Ann Clin Biochem)* → แก้เป็น `K↑ Ca↓ Mg↓ + ALP↓`
- **[MEDIUM → FIXED]** Fork 2: NaF ออกฤทธิ์ช้า ~1–4 ชม.แรก → glucose ยังตกแม้อยู่หลอด NaF → เติมคำเตือนปั่นแยกเร็ว/citrate-buffered tube *(IFCC/ADA)*
- **[flag — ไม่แก้]** WBIT: เพิ่มเตือน "ห้าม batch labeling หลายคนพร้อมกัน" (ไฟล์มี "ห้าม pre-label + label ข้างเตียง" ครอบอยู่แล้ว — ปล่อยให้ MT พิจารณาเสริม)

## poct-judgment — ⚠️ 1 HIGH landmine → แก้แล้ว
- **[HIGH → FIXED]** Fork 3 glucose interference เดิมตื้น ("Hct+oxygen") → เติม landmine จริง: **ทิศ Hct** (สูง→ต่ำปลอม / ต่ำ→สูงปลอม) · **O₂ เฉพาะ glucose-oxidase** · **GDH-PQQ + maltose/icodextrin(PD)/galactose → สูงปลอมรุนแรง (FDA boxed warning, เคยให้ insulin เกินจนตาย)** · **capillary เชื่อไม่ได้ใน shock** *(FDA 2009; ISO 15197:2013; CLSI POCT12)*
- **[LOW → FIXED]** Fork 2: เติม EQA/PT *(ISO 15189:2022 Annex A)*
- **[note]** ไฟล์อ้าง ISO 15189:2022 ถูกแล้ว (ISO 22870 ถูก withdrawn 2025 ย้ายเข้า 15189 Annex A — ไฟล์ไม่ได้อ้าง 22870 จึงไม่ต้องแก้)

## flow-cytometry-judgment — ⚠️ 2 HIGH → แก้แล้ว
- **[HIGH → FIXED]** "FMO/isotype" วางคู่กันลวงว่าเท่ากัน → **FMO = control หลักขีด gate; isotype = legacy เชื่อไม่ได้** (match fluorochrome:protein ไม่ได้จริง) *(ICCS; Maecker & Trotter, Cytometry A 2006)*
- **[HIGH → FIXED]** gating order ขาด time gate + dump channel → เพิ่ม `time/flow-stability → scatter → singlet → viable+dump → CD45/SSC` + เตือน blast=CD45-dim, plasma cell หลุด gate *(EuroFlow/OMIP)*
- **[MEDIUM → FIXED]** กับดัก #2: เพิ่ม over-comp → **negative ปลอม** (ไม่ใช่แค่ positive ปลอม) — กระทบ MRD
- **[MEDIUM → FIXED]** PNH: เพิ่ม lineage-specific (FLAER + ≥2 GPI marker บน WBC; FLAER ใช้ RBC ไม่ได้; RBC โดน transfusion บิดผล) + MRD ต้อง acquire events เยอะ *(ICCS PNH consensus, Sutherland 2018)*

## urinalysis-judgment — ✅ clean
- ไม่พบ error / outdated / คำแนะนำอันตราย. ทุก fork ตรง CLSI GP16 + Strasinger
- **[LOW → FIXED]** CSF: เพิ่ม "xanthochromia ดูจาก supernatant ปั่นทันที (whole specimen ค้าง → false xanthochromia)" + "clearing tube 1→3 ไม่ตัด SAH"
- **[flag — ไม่แก้]** SG strip mechanism / calcium-oxalate monohydrate form = completeness nice-to-have (by-design ไฟล์ไม่ใช่ atlas)

---

## ค้างให้ MT จริงตรวจต่อ (AI review ไม่แทน)
ทั้ง 4 ผ่าน AI pre-screen แล้วแต่ **ยังต้องการ MT คนที่สองในสายนั้นตรวจ judgment + กับดัก** ก่อนชูขึ้น public (gate เฟส 2→3 ใน [`../docs/LAUNCH.md`](../docs/LAUNCH.md)). status คง `draft`.
