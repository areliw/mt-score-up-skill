# Contribution Credit — นับ "ภูมิที่เก็บได้" เป็นเลข (community tiers)

> **ทำ north-star ให้วัดได้:** "รุ่นพี่เก็บเคสเพื่อรุ่นน้อง" → นับเป็น *"เก็บภูมิจากคนได้กี่คนแล้ว"*.
> โมเดล = **paper-style credit**: 1 contribution ที่ผ่าน validate = +1 ที่ "เจ้าของภูมิ" (source), attribution ติดตัวถาวร แม้คนอื่นเป็นคนส่ง.
> **คู่กับ [`maturity-ladder.md`](./maturity-ladder.md)** — ladder วัด *คุณภาพความรู้แต่ละชิ้น* · credit วัด *คน/ความครอบคลุม* = **คนละแกน ใช้ validation gate ร่วมกัน**. ออกแบบ 2026-06-15 (draft).

## 3 หลักการ (กันเลขเฟ้อ — สำคัญสุด)
1. **นับ "คน" ไม่ใช่ "ชิ้น"** → metric หลัก = distinct credited-source (นับหัว). ไม่งั้นคนเดียวส่ง 50 ชิ้นดันเลขปลอม
2. **"นับ" เมื่อผ่าน gate ขั้นต่ำ** → ผูก maturity-ladder (เริ่มนับที่ **L2 codex-pass**). ไม่ผูก = submit ขยะมา farm เลข
3. **source ได้ tier · scribe ได้เครดิตแยก** → เหมือน paper: author (คนเก็บ/เรียบเรียง) + acknowledgment (เจ้าของความรู้)

## คำนิยาม
- **contribution-unit** = 1 *validated judgment-unit* (fork / trap / เคส / landmine) ที่ **net-new** (ผ่าน `check_duplicates.py`) **และ** แตะ gate ≥ **L2** — *ไม่ใช่* ทั้งสกิล (granular = คนเข้าร่วมได้เยอะ)
- **credited-source** = คน 1 คนที่เป็นเจ้าของภูมิของ contribution-unit ที่นับแล้ว ≥1 ชิ้น (นับ **ครั้งเดียว/คน** ไม่ว่าจะมีกี่ชิ้น)
- **scribe** = คนเก็บ/เรียบเรียง/ส่งฟอร์ม (อาจ = source หรือคนละคน — เช่น เก็บเคสรุ่นพี่มาให้)

## 2 เมตริก (ห้ามรวมกัน)
| เมตริก | นับอะไร | ใช้ทำอะไร |
|---|---|---|
| **U** (Units) | validated contribution-unit (net-new · ≥L2 · มี source) | → **tier** (= north-star "เก็บภูมิได้กี่ก้อน") |
| **P** (People) | distinct คนที่ **ลงชื่อ** (opt-in) | → stat รอง "กี่คนยอมเปิดตัว" |

> **tier เดินด้วย U** — form เปิด/anon เยอะ → นับ "ก้อนภูมิ" ได้จริง + ungameable. P = lower-bound (anon นับหัวไม่ได้) จึงเป็น stat รอง

## Tiers (เดินด้วย U = ก้อนภูมิ validated)
| Tier | ชื่อ (ธีม — optional) | U (ก้อนภูมิ) | ความหมาย |
|---|---|---|---|
| T0 | จุดประกาย (Spark) | 1–49 | เริ่มมีของ ยังบาง |
| T1 | คลังเงา (Vault) | 50 | คลังเริ่มมีน้ำหนัก ใช้ได้หลายเรื่อง |
| **T2** | **องค์กรลับ (Order)** | **100** | **milestone ที่คุยกัน — 100 ก้อนภูมิที่ verify แล้ว** |
| T3 | หอสมุดต้องห้าม (Athenaeum) | 500 | ครอบคลุมกว้าง เป็น reference จริง |
| T4 | มหาคลังรัตติกาล | 1,000+ | infrastructure ความรู้ของวงการ |

> **U นับเฉพาะ contributed unit** (เข้าผ่าน pipeline + มี source) — seed skills เดิมของผู้สร้าง = ฐาน ไม่นับย้อน · ธีมชื่อปรับ/ตัด/เอาเลขเปล่าได้ (ดู `CONTRIBUTORS.md`)
> **P (คนลงชื่อ)** โชว์คู่เป็น stat รอง: *"จาก N คนที่เปิดตัว + เงาอีกเพียบ"*

## วงจรเครดิต (submit → นับ)
1. **รับ** (form/PR) → credit = **provisional** (ยังไม่เข้าเลข P/U) · บันทึก source + scribe
2. **dedup** (`check_duplicates.py`) → ถ้าซ้ำของเดิม = ไม่นับ (อาจ merge เครดิตเข้า unit เดิม)
3. **gate** → แตะ L2 (codex-pass) → credit = **confirmed** → **เข้าเลข P/U**
4. **ladder ขยับ** (L3+ corroborated/proven…) → unit แข็งขึ้น แต่ **P ไม่เพิ่ม** (คนเดิม) — เพิ่มแค่ "น้ำหนัก/ความเชื่อถือ" ของ unit

## Anti-gaming (กับดักที่ต้องปิด)
- **นับชิ้นแทนคน** → คนเดียว spam ดันเลข → *ปิดด้วย:* tier เดินด้วย P (distinct people)
- **submit ขยะมา farm** → *ปิดด้วย:* นับเฉพาะ confirmed (≥L2 codex)
- **ความรู้ซ้ำนับซ้ำ** → *ปิดด้วย:* dedup gate net-new
- **เคลม source ปลอม/แอบอ้างชื่อ** → *ปิดด้วย:* source ที่เปิดชื่อต้อง consent (ดูเคส anon ด้านล่าง)

## ไม่ระบุชื่อ (anon) — นับยังไง
**ความจริงของช่องทาง:** form เปิด ใครก็ส่งได้ **ไม่เก็บ email/login** → *ไม่มี identifier ให้แยก anon ออกจากกันเลย* → **นับหัว anon ไม่ได้ จุดจบ**. (seat-#N / email-hash = สมมุติว่ามีของที่ไม่มีจริง — **ตัดทิ้ง**)

**กฎที่ซื่อสัตย์ — identity = opt-in:**
- **ใส่ชื่อ/handle ที่ตัวเองเป็นเจ้าของ** = **+1 P** (counted) — คนที่ "ยืนขึ้นรับเครดิต"
- **ไม่ใส่อะไร** = **U-only** — ความรู้นับเต็ม (U + ladder) แต่ **ไม่นับหัว** (verify distinct ไม่ได้)
- **"100 คน" (tier-P) = 100 คนที่ยอมลงชื่อ** · anon = ผู้เติม U เงียบๆ ("เงาแห่งรัตติกาล") · handle "สมาชิกแห่งความมืด" = **flavor การโชว์ของ anon-pool ไม่ใช่หน่วยนับ** (ดู `CONTRIBUTORS.md`)
- **โชว์ซื่อสัตย์:** *"ภูมิจาก **X คนที่ลงชื่อ** (+ **Y** units จากผู้ไม่ออกนาม)"*
- **residual:** ปลอมหลายชื่อดัน P ได้ แต่ต้องลงแรงสร้าง persona + โผล่ในลิสต์ + maintainer review (form pipeline) → **P = lower-bound** (จริง ≥ ที่นับ ไม่ปลอมขึ้น)

> 🔑 **สรุป: tier เดินด้วย U (ก้อนภูมิ) เป็นหลัก · P (คนลงชื่อ) เป็น stat รอง** — เพราะช่องทางนับคนไม่ได้จริง + U ungameable กว่า

## Data model (ขั้น implement)
- `eval/contributions.json` — registry: `{id, source, scribe, skill, unit_type, gate_level, content_hash, date, consent}`
- `P = distinct source where gate_level ≥ L2` · `U = count(gate_level ≥ L2)` · คำนวณ tier จาก P
- ต่อยอดจากที่มีแล้ว: `CONTRIBUTORS.md` (3-layer credit) + Google Form pipeline + `check_duplicates.py`
- **gate ใน CI:** เลข P/U ใน README/บนเว็บ = generated จาก registry (อย่า hardcode — audit เลขเฟ้อ)

## Decisions ที่ผมเคาะให้ (review ได้)
- ✅ เริ่มนับที่ **L2** (codex-pass) — strict พอ ไม่สูงจนไม่มีใครติด
- ✅ unit = **judgment-unit** (fork/trap/เคส) net-new ไม่ใช่ทั้งสกิล
- ✅ source = คนได้เครดิต · scribe = เครดิตแยก (author/acknowledgment)
- ✅ **anon: identity opt-in** — ลงชื่อ = +1 P · ไม่ลงชื่อ = U-only (form ไม่มี identifier → นับหัว anon ไม่ได้)
- ✅ **tier เดินด้วย U** (ก้อนภูมิ) · P = stat รอง — form เปิดนับคนไม่ได้จริง + U ungameable

## เปิดไว้ให้คุณตัดสิน
- personal contributor levels (รางวัล scribe ขยัน) — แกน 3 ไหม หรือ community-only พอ?
- ชื่อ tier ใช้ธีม guild จริงไหม หรือเลขเปล่า
