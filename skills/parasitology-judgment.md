---
skill: parasitology-judgment
title: ตัวช่วยตัดสินใจในแล็บปรสิตวิทยา (Parasitology Lab Judgment)
type: ADVISE
needs: any
author: "MT Score UP!"
last_edited: 2026-06-01
status: draft
disclaimer: "skill นี้ช่วย 'คิด' การตัดสินใจในแล็บปรสิตวิทยา เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รายงาน — ผลลบจาก stool/film ตัวอย่างเดียว 'ไม่ตัดโรคออก' การเลือก technique/stain/การตีความทุกครั้งต้องทำตาม SOP ของหน่วยงาน และยืนยันกับ MT ผู้รับผิดชอบ/แพทย์เสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ตัวช่วยตัดสินใจในแล็บปรสิตวิทยา

ตัวช่วยตัดสินใจในแล็บปรสิตวิทยาสำหรับ MT — เน้น "เลือก technique/stain/ตีความยังไง" + "พลาดตรงไหน" ไม่ใช่ลอก atlas รูปไข่/life cycle

> ความปลอดภัยหลัก: ผลลบจาก stool หรือ film ตัวอย่างเดียว "ไม่ตัดโรคออก" — parasitemia/การขับเชื้อเป็นวงจร ต้องตรวจซ้ำตามจำนวนที่กำหนด และเลือก technique/stain ให้ตรงกับปรสิตเป้าหมายเสมอ

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- "ตัวอย่างนี้ใช้ concentration ไหน?" · "ย้อมสีอะไรถึงจะเห็น?" · "malaria ดู film ไหน / ต้องตรวจซ้ำมั้ย?"
- "stool ตรวจกี่ครั้งถึงเชื่อผลลบได้?" · "เก็บเลือด/อุจจาระตอนไหน?" · "ใช้ serology หรือ microscopy?"
- กำลังจะ report ผล negative แล้วอยากรู้ว่า "ตัดออกได้จริงมั้ย"

## วิธีใช้
วาง skill นี้ + บอกสถานการณ์ (สงสัยเชื้อกลุ่มไหน · specimen อะไร · อาการ/immune status · timing การเก็บ) → AI พาเดินผ่าน fork การตัดสินใจ ชี้ technique/stain/จำนวนตรวจที่เหมาะ และเตือนกับดักก่อนคุณรายงานผล

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

ก่อนเลือก technique/stain เสมอ — ตอบ 4 อย่างนี้ก่อน:
1. สงสัยปรสิตกลุ่มไหน — protozoa cyst/tropho · helminth egg · blood parasite (malaria/microfilaria) · coccidia/spore (opportunist) · tissue
2. specimen อะไร + สด/ค้าง — stool (formed→cyst, watery→tropho), blood, urine, sputum, CSF, biopsy, scraping
3. อาการ + immune status — ภูมิต่ำ/HIV → คิด opportunist (Crypto/Cyclospora/Microsporidia/Toxo) ทันที
4. timing — เก็บมาตอนไหน (กลางวัน/คืน), เก็บกี่ครั้งแล้ว

### FORK 1 — เลือก concentration / technique
| สถานการณ์ | เลือก | เหตุผล / ห้าม |
|---|---|---|
| ดู motile trophozoite / cyst สด | Direct wet smear (NSS + Lugol's iodine) | iodine ย้อม nucleus+glycogen แต่ฆ่า tropho → ดู motility ดู NSS ก่อน |
| routine helminth egg + protozoan cyst | Formalin-ether (ethyl acetate) sedimentation = ครอบคลุมสุด | gold ของ concentration; ข้อเสีย ether ไวไฟ + ทำลาย tropho |
| protozoan cyst + nematode egg ลอย | Zinc sulfate flotation (sp.gr.1.18) | |
| roundworm/hookworm/whipworm egg | Brine/Willis flotation (1.20) | ลอย tapeworm/trematode/protozoa ไม่ได้ (egg หนัก/operculated จม) |
| Cryptosporidium oocyst | Sheather's sugar (1.27) + modified acid-fast | |
| นับความหนาแน่นไข่ (EPG) Ascaris/Trichuris/Opisthorchis | Kato / Kato-Katz thick smear (quantitative) | แยก species ไม่ได้ — แค่ count |

Decision: คุณภาพ morphology (tropho สด) → direct · ความไว (egg/cyst น้อย) → formalin-ether · ปริมาณ/ระบาดวิทยา → Kato-Katz

### FORK 2 — เลือก stain
- Trichrome / iron-hematoxylin → permanent stain ของ intestinal protozoa (แยก E.histolytica vs coli, เห็น nucleus/chromatoid)
- Modified acid-fast (modified Ziehl-Neelsen) → coccidia oocyst (Cryptosporidium / Cyclospora / Cystoisospora) — แดงบนพื้นเขียว · ย้อมธรรมดาจะมองข้าม oocyst
- Modified trichrome → Microsporidia spore (เห็น "เข็มขัด/belt" สีแดง) · CFW ก็ได้
- Giemsa (Romanowsky) → blood parasite: malaria, microfilaria, Leishmania amastigote, Toxoplasma tachyzoite, Trypanosoma
- Lugol's iodine → wet-mount ย้อม cyst (ชั่วคราว)
- Calcofluor white (CFW) → Acanthamoeba cyst (corneal scraping), Microsporidia
- Toluidine blue O / methenamine silver → Pneumocystis cyst (BAL)

Decision: oocyst ทน → acid-fast · spore → mod.trichrome · เลือด/เนื้อเยื่อ → Giemsa · ลำไส้ protozoa permanent → trichrome

### FORK 3 — Malaria: thick vs thin film + เมื่อไหร่ซ้ำ
- Thick film = gold standard ความไว (lyse RBC, threshold ~20/µl) → screen + ประเมิน density/parasite count
- Thin film = species ID (RBC ยังอยู่ → Schüffner's dots / banana gametocyte / band form / RBC โต)
- Parasite count (thick): ปรสิต/200 WBC × 8,000 = /µl (>40,000/µl นับ WBC/500 parasites)
- ผลลบ 1 ชุดไม่ตัด malaria ออก → ตรวจซ้ำทุก 12-24 ชม. × อย่างน้อย 3 ครั้ง (parasitemia เป็นวงจร)
- RDT (HRP-2 = Pf เท่านั้น, pLDH/aldolase = pan) เสริม แต่ยืนยัน species + count ด้วย thin film เสมอ

Decision: negative ครั้งแรก ≠ negative — repeat ก่อนรายงาน "ไม่พบ"

### FORK 4 — Serology / molecular vs Microscopy
ใช้ serology/PCR เมื่อ microscopy ทำไม่ได้/ไม่ไว:
- เชื้ออยู่ในเนื้อเยื่อ → Trichinella (muscle), Toxoplasma, Gnathostoma (ELISA 24kDa), Echinococcus (cyst)
- ช่วง prepatent / periodicity (filaria), light infection
- E. histolytica vs E. dispar แยก morphology ไม่ได้ → ต้อง PCR/Ag (อย่ารายงาน "histolytica" จาก cyst เปล่าๆ)
- serology มี cross-reaction + sens/spec ไม่ 100% → แปลคู่อาการ

Ag detection (Crypto/Giardia/Histolytica feces; Plasmodium/Wuchereria เลือด) ปรากฏเร็วกว่า Ab + สัมพันธ์ปริมาณเชื้อ

### FORK 5 — Specimen timing
- Microfilaria (W.bancrofti/B.malayi) → เจาะเลือดกลางคืน (nocturnal periodicity) หรือ provocation: DEC 2mg/kg → เจาะ 0.1ml ใน 15-30นาที–5ชม. · เจาะกลางวัน = false-neg
- Enterobius (pinworm) → Scotch tape ก้น ตอนเช้าก่อนอาบน้ำ/ถ่าย · หาในอุจจาระ = พลาด
- Trophozoite → ตรวจภายใน 30 นาที หลังถ่าย
- Trichinella → muscle biopsy ~3–4 สัปดาห์หลังกิน (รอ encyst)

## กับดัก (Anti-patterns)
- Single stool = false-negative → routine 1 ครั้ง แต่ยืนยัน/exclude ต้อง 3 ตัวอย่างวันเว้นวัน · E. histolytica = 6 ครั้ง
- Low-parasitemia malaria พลาด → ดู thick ให้ครบ (≥100–200 field) + repeat 12–24 ชม.; เห็น ring เดียวอย่ารีบสรุป species
- misID — E. histolytica vs E. coli → histolytica: กิน RBC, karyosome centric, cyst ≤4 นิวเคลียส, chromatoid ปลายมน · coli: ไม่กิน RBC, karyosome eccentric, cyst ถึง 8 นิวเคลียส, ปลายแหลม. (histolytica vs dispar = PCR เท่านั้น)
- Stain ผิด → ไม่เห็น oocyst/spore → HIV ท้องเสีย ต้องสั่ง modified acid-fast (+ mod.trichrome สำหรับ microsporidia)
- เก็บ specimen ผิดเวลา → microfilaria กลางวัน, pinworm ในอุจจาระ, tropho ตรวจช้า = false-neg จาก timing
- Artifact = parasite → pollen, plant cell, yeast, RBC/WBC, air bubble, starch, Charcot-Leyden → แยกด้วยขนาด/ผนัง/internal structure; วัด micrometer + ย้อม ก่อนรายงาน
- Flotation ผิดชนิดงาน → Brine/Willis หา tapeworm/fluke egg = เจอศูนย์ (egg หนักเกินจะลอย) → sedimentation
- specimen ปนเปื้อน → ปัสสาวะปน stool ทำลาย tropho · ดินปน = artifact → ปฏิเสธ/เก็บใหม่
- ยาก่อนเก็บ → antacid/oil (งด 7–10 วัน), antibiotic (2–3 สัปดาห์), barium (3 สัปดาห์) บังเชื้อ → ถามประวัติยา

หมายเหตุ: ความรู้พื้นฐาน (morphology, life cycle, vector-disease, egg sizes, species tables) → ดูจากตำรา/แหล่งอ้างอิงมาตรฐาน skill นี้เน้นการตัดสินใจ ไม่ใช่ atlas

## ช่องสำหรับผู้เชี่ยวชาญเติม
> SOP ของหน่วยงานคุณกำหนดจำนวน stool ขั้นต่ำเท่าไรสำหรับ rule-out (เทียบกับ routine)?
> มี panel/algorithm เฉพาะหรือไม่สำหรับผู้ป่วยภูมิต่ำ (เช่น บังคับ modified acid-fast + mod.trichrome อัตโนมัติ)?
> เกณฑ์ของหน่วยงานในการส่งต่อ PCR/serology (เช่น E. histolytica/dispar, tissue parasite) เป็นอย่างไร?

---
*skill นี้ช่วย "คิด" การตัดสินใจในแล็บปรสิตวิทยา เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รายงาน — ผลลบจาก stool/film ตัวอย่างเดียวไม่ตัดโรคออก ทุกการเลือก technique/stain/การตีความต้องทำตาม SOP ของหน่วยงาน และยืนยันกับ MT ผู้รับผิดชอบ/แพทย์ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
