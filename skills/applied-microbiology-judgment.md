---
skill: applied-microbiology-judgment
title: โค้ชจุลชีววิทยาประยุกต์ — อาหาร/อุตสาหกรรม/สิ่งแวดล้อม (Applied Microbiology Judgment)
type: ADVISE               # ช่วยตัดสินใจ applied micro ไม่ใช่ตำราเชื้อ
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-01
status: draft
disclaimer: "ช่วยคิดงานจุลชีววิทยาประยุกต์ (อาหาร/อุตสาหกรรม/สิ่งแวดล้อม) เพื่อการศึกษา ไม่ใช่คำสั่งความปลอดภัยอาหาร/สิ่งแวดล้อมทางการ — ต้องอ้างมาตรฐาน (เช่น food safety/ISO) + ผู้เชี่ยวชาญจริง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชจุลชีววิทยาประยุกต์ — อาหาร/อุตสาหกรรม/สิ่งแวดล้อม

จุลชีพ "เอาไปใช้/ควบคุม/ตรวจจับ" ในงานอาหาร อุตสาหกรรม สิ่งแวดล้อม — เลือกวิธีถนอม/ตรวจ/คัดกรองยังไง ไม่ใช่ท่องชนิดเชื้อ (= commodity ดูตำรา)

> คนละเลนกับ clinical micro (เจอเชื้อในคนไข้ → ID+AST ดู `clinmicro-judgment`) · เลือก molecular method/แปล qPCR → `molecular-judgment` · บริหาร/ขายเครื่องตรวจ → `lab-management-judgment`

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- เลือกวิธีถนอมอาหาร / เข้าใจทำไม spoilage เกิด
- ตรวจหา food-borne pathogen — เลือก conventional vs rapid vs molecular
- คัดกรองจุลินทรีย์/สารออกฤทธิ์ (screening, antibiotic R&D, metagenomics)
- bioremediation / probiotic-prebiotic / microbiome

## วิธีใช้
วาง skill นี้ + เล่าโจทย์ (ถนอมอะไร / ตรวจเชื้ออะไร / คัดกรองอะไร) → AI ชี้วิธี + trade-off + กับดัก

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — เลือกวิธีถนอมอาหาร (เป้าหมาย × เชื้อ × ผลต่ออาหาร)
| วิธี | อุณหภูมิ | ฆ่าอะไร | กับดัก |
|---|---|---|---|
| Pasteurization | <100°C | pathogen + spoilage ส่วนใหญ่ | **ไม่ฆ่า spore** → ยังต้องแช่เย็น/preservative (LTLT 62.8°C/30min · HTST 71.7°C/15s) |
| Boiling | =100°C | vegetative; spore บางส่วน | **Tyndallization** = ต้มซ้ำ 3 วันจัดการ spore ที่ germinate |
| Sterilization | >100°C | vegetative + spore | UHT 135-150°C/1-4s; commercial-sterile = canned ไม่ต้องแช่เย็น |
- ⚠️ pasteurize/canning ≠ ปลอดเชื้อ — canned อาศัย **acidity**; low-acid (เนื้อ/ผัก) underprocess → *C. botulinum*
- **Cold:** refrigerate ชะลอไม่หยุด → **psychrophile/psychrotroph (Listeria) โตในตู้เย็นได้** · **aw:** ลดเหลือ 0.65-0.75 ยับยั้ง (drying/salt/sugar) · **Radiation:** UV = ผิวเท่านั้น (ไม่ทะลุ); gamma ทะลุได้

### Fork 2 — Food-borne pathogen detection: screen ≠ confirm
3 ชั้น: **conventional culture** (gold แต่ช้า; plate count CFU/mL นับ 30-300; MPN จากตาราง; selective/differential media) → **rapid** (ID kit/automated/immunoassay เช่น ELISA) → **molecular** (PCR/16S/microarray)
- ⚠️ **screen positive = presumptive** — chromogenic/selective + rapid kit ต้อง **confirm biochem+serology** เสมอ
- ⚠️ **rapid ≠ ไม่ต้อง enrichment** — immunoassay ส่วนใหญ่ยัง pre-enrich + เสี่ยง matrix interference (salt/acid/metal) → อย่าอ้างเกินจริงว่า "ใส่ตัวอย่างได้เลย"
- อ่าน plate count → ชี้แหล่งปนเปื้อน: coliform = สุขอนามัยมือ · Salmonella = พาหะ/ปนข้าม · Staph = คนทำไอจาม

### Fork 3 — Microbial screening / antibiotic R&D: culture-dependent vs independent vs polyphasic
- ปัญหา: จุลินทรีย์ **>99% เพาะไม่ขึ้น** (soil) + classical screen เจอซ้ำ → ต้อง culture-independent
| วิธี | หลักการ | กับดัก |
|---|---|---|
| Classical (culture-dependent) | เพาะ → biochem | เพาะไม่ขึ้น 99%, ID ซ้ำ |
| Metagenomics (culture-independent) | total DNA → 16S/NGS | ได้ diversity แต่ไม่ได้เชื้อจริง, ORF function ไม่รู้เพียบ |
| **Polyphasic (ผสม)** | culture + molecular | **คำตอบจริงของ R&D** (ไม่เลือกข้างเดียว) |
- screening 2 ทาง: **activity-based** (คัดจากฤทธิ์; พึ่ง heterologous expression — ติด promoter/codon/folding) vs **sequence-based** (หา gene เช่น 16S/**NRPS/PKS**; ไม่พึ่ง expression แต่ ORF เยอะ)
- **NRPS** → peptide antibiotic (vancomycin/bacitracin) · **PKS** → polyketide (erythromycin/tetracycline/amphotericin)

### Fork 4 — Bioremediation: in-situ vs ex-situ + ย่อยได้/ไม่ได้
- **in-situ** (bioventing/biosparging) = ย่อยหน้างาน ไม่ขนย้าย · **ex-situ** (bioreactor) = คุม O₂/อาหาร/pH → มีประสิทธิภาพสุด · **bioaugmentation** = เติมเชื้อ
- ย่อยได้: petroleum hydrocarbon, chlorinated aromatic, solvent, pesticide
- ⚠️ **heavy metal ย่อยไม่ได้** — ทำได้แค่เปลี่ยน valence/immobilize (Cr⁶⁺→Cr³⁺ insoluble = **transformation ไม่ใช่ degradation**) · by-product ระหว่างย่อยอาจพิษกว่าเดิม → ต้อง monitor

### Fork 5 — Beneficial microbes: probiotic/prebiotic/synbiotic + FMT
- **Probiotic** = จุลินทรีย์ **มีชีวิต** + ปริมาณพอ + สายพันธุ์ถูก + ไม่พา resistance gene (Lactobacillus/Bifidobacterium) · **Prebiotic** = อาหารของมัน (FOS/inulin/fiber, non-digestible) · **Synbiotic** = pro+pre
- ⚠️ "มีแบคทีเรีย = probiotic" ผิด — ต้องครบ 4 เงื่อนไข; prebiotic (อาหาร) ≠ probiotic (ตัวเชื้อ)
- **FMT** (fecal microbiota transplant) = ปลูกถ่ายอุจจาระคนสุขภาพดี → รักษา ***C. difficile* infection** ที่เกิดจาก antibiotic ทำลาย flora = bacteriotherapy ได้ผลสูง

---

## กับดัก (Anti-patterns)
- **pasteurize/canning = sterile** — ไม่ฆ่า spore; low-acid underprocess → *C. botulinum*
- **refrigeration หยุดเชื้อ** — psychrophile/Listeria ยังโต
- **UV ทะลุอาหาร** — ใช้ผิว/เครื่องมือเท่านั้น; ทะลุต้อง gamma
- **screen = confirm** — selective/chromogenic/rapid = presumptive ต้อง confirm
- **rapid/ELISA ไม่ต้อง enrichment** — ส่วนใหญ่ยังต้อง + matrix interference
- **molecular แทน culture 100%** — metagenomics ให้ diversity แต่ไม่ได้เชื้อจริง → **polyphasic**
- **bioremediation ย่อย heavy metal** — ทำได้แค่ immobilize (transformation); by-product อาจพิษกว่า
- **probiotic = อะไรก็ได้** — ต้องมีชีวิต + dose พอ + สายพันธุ์ถูก

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT food/QC) เคส food pathogen ที่ screen บวกแต่ confirm ลบ เพราะ..."*
> - *"วิธีถนอม/กระบวนการที่สายผมใช้ + จุดที่ underprocess เคยพลาด..."*
> - *"งาน screening/metagenomics ที่ทำ + ทำไมเลือก polyphasic..."*

---
*ช่วยคิดงานจุลชีววิทยาประยุกต์ (อาหาร/อุตสาหกรรม/สิ่งแวดล้อม) เพื่อการศึกษา ไม่ใช่คำสั่งความปลอดภัยอาหาร/สิ่งแวดล้อมทางการ — ต้องอ้างมาตรฐาน (เช่น food safety/ISO) + ผู้เชี่ยวชาญจริง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
