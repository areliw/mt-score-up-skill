# Catalog Steward — ระบบดูแลคลังตัวเอง (draft 2026-06-15)

> "ระบบประสาท" ของคลัง: **auto-detect → propose → gate → apply**. ทำให้คลังมีชีวิต/ดูแลตัวเอง (หลอมรวม·แยกร่าง·upgrade·ลบ·สร้าง) **โดยไม่กินตัวเอง**.
> คู่กับ [`maturity-ladder.md`](./maturity-ladder.md) (tier-signal) + [`contribution-credit.md`](./contribution-credit.md) (U/credit). **ต้องมี 2 ตัวนั้นก่อน** (steward ใช้เป็น input).

## หลักเดียวที่กันระบบกินตัวเอง
**mechanical + conservative + reversible → auto ได้** · **content-altering + irreversible + value-laden → auto-*เสนอ* + gate (codex/A/B/PR) ก่อนลงมือ**

| operation | auto? | เหตุผล |
|---|---|---|
| detect (overlap/orphan/drift/stale/gap) | ✅ auto เต็ม | ชี้เฉยๆ ไม่แตะเนื้อ |
| demote ชั้น (hash เปลี่ยน→ตก) | ✅ auto | conservative — ลดคำเคลม ไม่เคยดันขึ้น |
| promote L2/L5 (codex pass + A/B logged, hash ตรง) | ✅ auto | gate ด้วยหลักฐาน mechanical |
| upgrade L7+ (peer/field) | ❌ คน | ต้องมีคนจริงเซ็น |
| **merge / split / delete / create** | ⚠️ **propose only** | lossy/irreversible/value-laden → ต้อง codex+PR |

> full-auto self-modify knowledge base = **silent corruption** — สิ่งที่ระบบคุณภาพทั้ง repo สู้อยู่. steward ต้อง *เสนอ* ไม่ใช่ *ทำดิบ*

## v1 = detect-only (`scripts/catalog_steward.py`)
อ่าน skills/ + registry → ออก **`eval/steward-report.md`** ที่ list candidate ต่อ op (ไม่แตะไฟล์):

| สัญญาณ | คำนวณจาก | เสนอ op |
|---|---|---|
| **overlap** | `check_duplicates.py` (3gram) + cross-link density | → MERGE candidate (คู่ที่ทับ >threshold) |
| **bloat / multi-topic** | ไฟล์ยาวผิดปกติ + จำนวน fork มาก + "ใช้เมื่อ" หลายแกน | → SPLIT candidate |
| **orphan / dead** | ไม่มี cross-link เข้า + ไม่ถูก triage route + 0 ครั้งใน eval นาน | → DELETE-review candidate |
| **tier-drift (stale)** | hash ไฟล์ ≠ hash ใน evidence registry | → auto-DEMOTE (ทำเลย) + flag re-test |
| **promotable** | codex-pass + A/B logged + hash ตรง แต่ status ต่ำกว่า evidence | → auto-PROMOTE L2/L5 (ทำเลย) |
| **coverage gap** | โดเมน MT / cross-cutting ที่ไม่มี skill (เทียบ taxonomy) | → CREATE candidate |
| **factual-stale** | STANDARDS edition bump / source เก่า | → CORRECTION candidate (โยง `recheck_standards`) |

**output ต่อ candidate:** `{op, skill(s), signal+เลข, ความมั่นใจ, ผลถ้าทำ, ผลถ้าไม่ทำ}` — เรียงตาม impact (north-star)

## v2 = auto ส่วนที่ปลอดภัย
- เปิด auto-DEMOTE (hash stale) + auto-PROMOTE L2/L5 (evidence-gated) เข้า `build_triage` CI — status ในไฟล์ที่เกิน evidence = **CI แดง**
- ยังไม่แตะ merge/split/delete/create

## v3 = AI execute ผ่าน gate
- AI (ผม) หยิบ candidate จาก report → ทำ op → **codex review + (ถ้าแก้เนื้อ) A/B + PR** → user merge
- merge/split = AI ร่างผลลัพธ์ + diff cleanly · delete = ต้องมีเหตุผล + ไม่มี cross-link เหลือ + user nod
- **ทุก content-change ผ่าน PR เสมอ** (ไม่มี auto-commit เนื้อ)

## Guardrails (ห้ามหลุด)
- steward **ไม่เคย** auto-apply: merge/split/delete/create/upgrade-L7+
- demote/promote-mechanical/regen = auto ได้ (conservative + evidence-gated)
- ทุก auto-op log ลง `eval/steward-log.md` (audit, ย้อนได้)
- candidate "DELETE" ต้องผ่าน 2 รอบ (รอบแรก flag, ถ้ายัง orphan รอบถัดไป + user nod) — กันลบของที่แค่ยังไม่ถูกใช้
- steward เสนอเท่านั้นใน gap/create — **ไม่ auto-เขียนสกิลใหม่** (writing judgment)

## มีชิ้นส่วนอยู่แล้ว (ขาดแค่ loop ร้อย)
`check_duplicates.py` (overlap) · `build_triage.py` (regen) · `recheck_standards.py` (factual-stale) · `validate_repo.py` (structure) · ladder hash-currency (demote) · `self-improving-agent` (concept) → **steward = ตัว orchestrate ทั้งหมด + ออก report เดียว**
