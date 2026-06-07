---
skill: gget-genomics
title: ดึงข้อมูล gene/variant ด้วย gget — สาย molecular/bioinformatics (gget Genomics)
type: ADVISE               # ช่วยเลือก module + ตีความ ไม่ใช่รัน CLI ให้
needs: any                 # ใช้ได้กับ AI ทุกตัว (ลงมือจริงต้องลง gget/รัน Python)
author: "MT Score UP!"
last_edited: 2026-06-08
status: draft
disclaimer: "ช่วยคิดการใช้ gget ดึงข้อมูลจีโนมเพื่อการศึกษา ไม่ใช่การแปลผลทางคลินิก · variant pathogenicity ต้อง classify ตาม ACMG + ยืนยันโดยผู้เชี่ยวชาญ; sequence/variant ของผู้ป่วยจริง = PHI อย่าอัปขึ้น service สาธารณะ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ดึงข้อมูล gene/variant ด้วย gget

ตัวช่วยสำหรับ MT สาย molecular/bioinformatics ที่ใช้ [gget](https://github.com/pachterlab/gget) ดึงข้อมูลจากฐานข้อมูลจีโนม (Ensembl/NCBI/UniProt/PDB/AlphaFold) — เน้น "เลือก module + กับดัก build/ตีความ" ไม่ใช่ตำรา bioinformatics

> **กฎ #1:** gget ดึงจากฐานมาตรฐานได้เร็ว แต่ **ต้องระบุ reference genome + release ให้ตรง** — coordinate ผิด build = ผิดทั้งสาย
> **กับดัก #1 (ขั้น hard):** **variant coordinate ขึ้นกับ genome build** (GRCh37/hg19 vs GRCh38/hg38) — ใช้ผิด build → ตำแหน่ง/ยีน/ผลแปลผิด. ตรวจ build ของทุกแหล่งก่อนเทียบ/รวม (ต้อง liftover เมื่อข้าม build)

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`)

## ใช้เมื่อ
- ต้องดึง gene info / sequence / ortholog / structure / variant สำหรับงานวิจัย/thesis
- ทำ enrichment / BLAST / alignment เร็วๆ จาก CLI/notebook
- ไม่แน่ใจ module ไหนตอบโจทย์ + กลัว build/version เพี้ยน

## วิธีใช้
วาง skill นี้ + บอกว่าต้องการข้อมูลอะไร (gene/variant/structure/enrichment) → AI ช่วยเลือก gget module + เตือน build/version + ชี้การตีความที่ต้อง verify แล้วให้คุณรันจริง

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### Fork 1 — เลือก module ตามงาน
- `gget search`/`info` — หา/ดูข้อมูลยีน (Ensembl ID, ชื่อ, ตำแหน่ง)
- `gget seq` — ลำดับ nucleotide/amino · `gget blast`/`muscle` — BLAST/alignment
- `gget ref` — ดึง reference genome/annotation (FASTA/GTF) ของ species+release
- `gget enrichr`/`archs4` — GO/pathway enrichment, expression
- `gget pdb`/`alphafold` — โครงสร้างโปรตีน · `gget cosmic`/`mutate`/`cellxgene` — variant/single-cell

### Fork 2 — build / version (หัวใจ)
- ระบุ **species + Ensembl release** ชัด · ข้ามแหล่งต่าง build → **liftover (hg19↔hg38)** ก่อนเทียบ
- บันทึก gget version + database release (reproducibility)

### Fork 3 — ตีความ + verify (อย่าข้ามไปคลินิก)
- ผลจากฐานข้อมูล ≠ ผลคลินิก — **variant ต้อง classify ตาม ACMG** + ดู population frequency (gnomAD) (เชื่อม `molecular-judgment`)
- อย่าสรุป "pathogenic" จากแค่ presence/ชื่ออยู่ใน DB
- AI อาจให้พารามิเตอร์/ผลผิด → ตรวจกับ output จริง (เชื่อม `anti-hallucination`)

### Fork 4 — ข้อมูลผู้ป่วย
- sequence/variant ของคนไข้จริง = **PHI** → รันบนเครื่อง/สภาพแวดล้อมที่ปลอดภัย, อย่าอัปขึ้น public tool โดยไม่ระวัง (เชื่อม `digital-judgment`)

## กับดัก (Anti-patterns)
- #1 ลืมระบุ build/release → coordinate เพี้ยน (กับดัก #1)
- #2 สับ hg19 ↔ hg38 ตอนรวมแหล่ง (ไม่ liftover)
- #3 สรุป pathogenic จาก presence โดยไม่ดู ACMG/frequency
- #4 ไม่บันทึก version (gget/DB) → reproduce ไม่ได้
- #5 เชื่อพารามิเตอร์/ผลที่ AI แนะนำโดยไม่ตรวจ output จริง
- #6 อัป sequence/variant ผู้ป่วยขึ้น public service
- #7 ใช้ default species (human) กับข้อมูลที่เป็น species อื่น

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - งาน molecular/thesis ที่คุณใช้ gget + species/build ที่ใช้จริง
> - pipeline ที่ทีมคุณใช้ (gget เชื่อมกับ tool อื่นยังไง) + version ที่ pin ไว้
> - เกณฑ์ classify variant (ACMG/in-house) ในงานคุณ

NOTE: การแปลผล variant/molecular เชิงคลินิก → `molecular-judgment`; bioinformatics ทฤษฎี/syntax gget ละเอียด → docs ของ gget; skill นี้ช่วย "เลือก module + กัน build/ตีความพลาด"

---
*skill นี้ช่วย "คิด/เลือกใช้ gget" เพื่อการศึกษา ไม่ใช่การแปลผลทางคลินิก · variant classify ตาม ACMG + ผู้เชี่ยวชาญ; ข้อมูลผู้ป่วย = PHI · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
