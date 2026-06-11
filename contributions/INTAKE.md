# INTAKE — playbook สำหรับ maintainer

> รับของที่ MT คนอื่นส่งเข้ามา → แปลงเป็น skill ที่ขึ้นคลังได้จริง. ไฟล์นี้คือ
> "ทำตามได้ทีละขั้น" ไม่ใช่หลักการลอยๆ. คนนอกที่อยากส่งของ ไปที่
> [`../CONTRIBUTING.md`](../CONTRIBUTING.md) แทน — ไฟล์นี้สำหรับคนที่ **รับของแล้วแปลง**.

หลักที่ค้ำทุกขั้น: **กองกลางที่ทุกคนลงขัน ข้ามรุ่น** — คนส่งของไม่ใช่ "ขอความเมตตา"
เขาลงขันให้คลัง. หน้าที่ maintainer = ทำให้ของเขา **ขึ้นคลัง + ติดชื่อเขา** ไม่ใช่
ดองจนเงียบหาย. ของที่กระทบคนไข้ = **ต้องมีคนยืนยัน ห้าม auto-publish** (ดูขั้น 5).

ก่อนเริ่ม: `gh auth status` ผ่านไหม · อยู่ branch ไหน (ไม่ commit ตรง `main`).

---

## ภาพรวม 7 ขั้น

```
รับเข้า → triage → dedup → draft → verify → credit → ship
  1        2        3       4       5        6       7
```

แต่ละขั้นมี gate. **ตกขั้นไหน หยุดที่ขั้นนั้น** — อย่าดันต่อทั้งที่ยังไม่ผ่าน
(โดยเฉพาะ verify ของ clinical).

---

## ขั้น 1 — รับเข้า: รวมทุกช่องมาที่เดียว

ของไหลเข้าได้ 3 ทาง — ทุกทางจบที่ **GitHub Issue 1 ใบ** (single source of truth):

| ช่อง | มาจากไหน | maintainer ทำอะไร |
|---|---|---|
| **GitHub Issue** `skill-proposal` / `correction` | คนมี GitHub กดเอง | มีอยู่แล้ว — ไป triage ต่อได้เลย |
| **[Google Form](https://forms.gle/N7RsgZqrHkikgfKK6)** | MT หน้างาน ไม่มี GitHub | ก๊อปคำตอบ → เปิด Issue ใหม่แทนเขา ใส่ label `skill-proposal` |
| **เพจ / แชต / โน้ตมือ / เสียง** | ทักมาตรงๆ | สรุปเป็นข้อความ → เปิด Issue แทนเขา · เก็บที่มาไว้ให้ credit |

**ทำไมต้องรวมที่ Issue:** ทุกอย่างมี trail เดียว ค้นซ้ำได้ ไม่ตกหล่น และ PR ที่ตามมา
link `Closes #<issue>` ได้ → ปิด loop อัตโนมัติ.

ตอนเปิด Issue แทนคนอื่น ใส่ในตัว Issue:
- ที่มา (เช่น "ส่งทาง Google Form 2026-06-xx" / "ทักเพจ") — ไว้ติดต่อกลับ + ให้ credit
- ข้อความดิบที่เขาส่ง (เท่าที่ de-identify แล้ว — ดูขั้น 2)
- ชื่อ/สังกัดที่เขาอยากให้ลง credit (ถ้าให้มา) **หรือ** ระบุว่าขอ anonymous

> **Google Form (live):** [forms.gle/N7RsgZqrHkikgfKK6](https://forms.gle/N7RsgZqrHkikgfKK6) — สร้างจาก [`../scripts/create_contribution_form.gs`](../scripts/create_contribution_form.gs). คำตอบเข้า Google Sheet → maintainer ก๊อป → เปิด Issue `skill-proposal` แทนผู้ส่ง (เก็บที่มา + credit).

**Gate 1:** รู้ที่มา + มีข้อความพอจะเข้าใจว่าเขาจะสื่ออะไร → ผ่าน. ถ้ากำกวมจน
triage ไม่ได้ → ถามกลับเขา **1-2 คำถาม** (อย่าถามพร่ำเพรื่อ) ก่อนไปขั้น 2.

- [ ] ของอยู่ในรูป GitHub Issue แล้ว (เปิดเอง หรือเปิดแทน)
- [ ] รู้ที่มา + ช่องติดต่อกลับ
- [ ] รู้ว่าเขาอยากให้ credit ชื่ออะไร (หรือ anonymous)

---

## ขั้น 2 — triage: ของชิ้นนี้ "เอาขึ้นคลัง" ไหม

ตอบ 3 คำถาม. **ตกข้อไหน = ไม่ขึ้นคลัง** (แต่ตอบกลับเขาดีๆ เสมอ — เขาลงขันมา).

### 2.1 เป็น judgment จริงไหม (ไม่ใช่ตำราล้วน)
หัวใจคลัง = **"เลือกอะไรเมื่อไหร่ + กับดักที่มือใหม่ไม่รู้"** ไม่ใช่ความรู้ที่ตำรา/AI
มีอยู่แล้ว.
- ✅ เอา: "เจอ X → คนชอบเลือก A แต่จริงควร B เพราะ..." · "เคสที่ QC/reviewer ตีกลับเพราะ..." · "ตำราบอกใช้ได้ แต่ของจริงต้องระวัง..."
- ❌ ตัดทิ้ง: นิยาม / สูตร / ตาราง reference range / life cycle / รายการชนิดเชื้อ — พวกนี้ commodity, AI รู้อยู่แล้ว

ถ้าของเขา **มีเพชร judgment ปนอยู่ในตำรา** → เก็บเฉพาะเพชร โยนตำราทิ้ง (transform
ไม่ใช่ echo ดิบ).

### 2.2 อยู่ใน mission ไหม
mission = วิจารณญาณที่ **MT ไทยใช้จริง** (lab · research/R2R · career/sales · ทักษะ
AI/เครื่องมือที่ MT ต้องใช้). นอกนี้ (เช่น เรื่องทั่วไปไม่เกี่ยว MT) → ขอบคุณแล้วบอก
ตรงๆ ว่าไม่ตรงคลัง.

### 2.3 PII สะอาดไหม — **gate แข็ง ห้ามผ่านถ้าไม่สะอาด**
ของสาธารณะ ห้ามมี: ชื่อคน · HN/MRN · ชื่อโรงพยาบาล/สถาบัน · รหัสวิชา · เลขเอกสาร
เฉพาะ · lot number · วันที่ที่ผูกกับคนไข้.
- เจอ PII → **de-identify ก่อนทำต่อทุกครั้ง** (generalize: ชื่อ→`[ผู้ป่วย]`/`[MT]`, รพ.→ตัดทิ้งหรือ "รพ.แห่งหนึ่ง", เคสจริง→ทำให้เป็น generic)
- ถ้า de-identify แล้วเนื้อหาหายหมด (เคสเฉพาะเกินจนเอาคืนไม่ได้) → ไม่ขึ้นคลัง

**Gate 2:**
- [ ] เป็น judgment (มี "เลือกเมื่อไหร่ + กับดัก") ไม่ใช่ตำราล้วน
- [ ] อยู่ใน mission MT
- [ ] PII สะอาด (de-identify แล้ว หรือไม่มีตั้งแต่แรก)

ผ่านทั้ง 3 → ไปขั้น 3. ตกข้อใด → ตอบกลับ Issue สุภาพ + อธิบายเหตุผล + ปิด Issue
(หรือ label `wontfix`/`needs-info`).

---

## ขั้น 3 — dedup: ซ้ำกับ skill เดิมไหม

ก่อนสร้างใหม่ **เช็คเสมอ** ว่ามีตัวที่ทับ domain อยู่แล้วไหม (คลังมี 87 ตัว — ทับกันง่าย).

### 3.1 อ่าน catalog
เปิด [`../skills/INDEX.md`](../skills/INDEX.md) (manifest ทุก skill) + กวาด
`ใช้เมื่อ` ใน [`../prompts/triage.md`](../prompts/triage.md) — หา domain ที่ใกล้.
ตัวอย่างคู่ที่เคยเฉียดทับ: `bloodbank` ↔ `clinical-correlation`,
`data-project-survival` ↔ `data-science-workflow`.

### 3.2 รัน build script เพื่อจับ drift
```bash
python scripts/build_triage.py
```
สคริปต์นี้ regen CATALOG/INDEX/bundle จาก frontmatter จริง **และเตือนถ้า skill ตัวไหน
หลุดจาก `README.md` หรือ `skills/README.md`** (storefront ลืม sync). มันไม่ได้ทำ
semantic-dedup ให้ — **การตัดสินว่า "ทับ" หรือ "ไม่ทับ" ยังเป็นงานคน**: เทียบ `ใช้เมื่อ`
+ intro ของตัวใหม่กับตัวที่ใกล้ที่สุด แล้วถามตัวเอง "ผู้ใช้จะสับสนว่าหยิบตัวไหนไหม".

### 3.3 ตัดสิน: ตัวใหม่ vs merge
| สถานการณ์ | ทำ |
|---|---|
| ไม่มีตัวไหนทับ domain | → **สร้างใหม่** (ขั้น 4) |
| มีตัวเดิมครอบ domain อยู่แล้ว แต่ของใหม่มี **เพชรที่ตัวเดิมไม่มี** | → **merge play** (ล่าง) |
| ของใหม่ = subset ของตัวเดิมล้วน (ไม่มีเพชรใหม่) | → ไม่สร้าง · ตอบกลับว่า "มีอยู่แล้วที่ `<ตัวเดิม>`" + ชวนเขาไปเติม **"ช่องสำหรับผู้เชี่ยวชาญเติม"** ของตัวนั้นแทน |

**merge play (diamond mantra — 1 canonical + graft เพชร):**
1. เลือก **1 ไฟล์ canonical** ที่จะอยู่ (ปกติคือตัวเดิมที่ครอบ domain กว้างกว่า)
2. สกัด **เฉพาะเพชร** จากของใหม่ (judgment/trap/เกณฑ์ที่ unique จริง ไม่ซ้ำของเดิม)
3. graft เพชรเข้า canonical — ลง fork ที่เกี่ยวหรือ "ช่องผู้เชี่ยวชาญเติม"
4. **ติดชื่อคนส่ง** ที่เพชรนั้น (credit ไม่หาย แม้ไฟล์เขาไม่ได้อยู่เดี่ยว — ดูขั้น 6)
5. ถ้า 2 ตัวเดิมทับกันเอง → คม boundary ให้ชัด (ตัวนึงชี้ไปอีกตัว) แทนลบดื้อๆ

> รายละเอียด fuse/merge/split + เหตุผล diamond mantra: ดูตัวอย่างใน
> [`../CHANGELOG.md`](../CHANGELOG.md) (v0.7.0 graft 33 เพชรจาก 19 ตัว drop เข้า 15 skill).

**Gate 3:**
- [ ] อ่าน `skills/INDEX.md` + triage CATALOG หา domain ที่ใกล้แล้ว
- [ ] รัน `build_triage.py` แล้ว ไม่มี drift warning ค้าง
- [ ] ตัดสินชัด: สร้างใหม่ / merge / ชี้ไปตัวเดิม

---

## ขั้น 4 — draft: แปลงเป็น canonical format

ตอนนี้ของผ่าน triage + รู้แล้วว่าสร้างใหม่หรือ merge. แปลงเป็นไฟล์ skill จริง.

**ใช้เครื่องมือที่มี — อย่าเขียนมือเปล่า:**
- [`../skills/write-a-skill.md`](../skills/write-a-skill.md) — วางในแชต AI แล้วป้อน judgment ดิบ → ได้โครง canonical (เครื่องมือหลัก)
- AI-draft helper (prompt ใน [`../CONTRIBUTING.md`](../CONTRIBUTING.md) หัวข้อ "ตัวช่วยร่างด้วย AI") — ถ้าคนส่งร่างมาให้แล้ว ใช้ขัดต่อ

**โครง canonical ที่ทุก skill ต้องมี** (ดูของจริงเทียบ:
[`../skills/bloodbank-judgment.md`](../skills/bloodbank-judgment.md)):

frontmatter ≥8 key:
```yaml
---
skill: <slug-case>            # ตรงกับชื่อไฟล์ <slug>.md เป๊ะ
title: <ไทย> (<English short>)
type: ADVISE | DO | CALIBRATION
needs: any | code-interpreter | persistent-memory
author: "<ชื่อผู้ส่ง> + MT Score UP!"   # ดู credit ขั้น 6
last_edited: YYYY-MM-DD
status: draft                # ทุกตัว draft — ห้าม flip เป็น stable
disclaimer: "<ข้อความ disclaimer ตามความเสี่ยง — ดูขั้น 5>"
---
```
body:
```
# <title>
## ใช้เมื่อ        ← (สำคัญ — เป็น routing signal ที่ build_triage.py ดูด)
## วิธีใช้
## วิธีทำ / fork   ← decision forks: เจอ X → ทำ Y · เลือก A เมื่อ...
## กับดัก          ← สิ่งที่ผู้เชี่ยวชาญรู้ มือใหม่พลาด
## ช่องสำหรับผู้เชี่ยวชาญเติม   ← ที่ให้คนอื่นมาเติมเคสจริงต่อ
*<disclaimer ปิดท้าย italics ก่อน --- สุดท้าย>*
```

**voice (house style — บังคับ):** Thai-first · blunt · verdict-first · หนาแน่น ·
ศัพท์เทคนิคคงไว้ · **ไม่มี AI-tropes** (ไม่ "ในยุคดิจิทัล", ไม่ rule-of-three เฟ้อ,
ไม่ em-dash ถี่, ไม่ promotional fluff). เขียนเหมือนคนเขียน. ตัวเลขในตัวอย่าง = ระบุ
ว่า **illustrative** (อย่าให้ดูเหมือนค่า validated).

**Gate 4:**
- [ ] frontmatter ครบ ≥8 key · `skill:` ตรงชื่อไฟล์ · `status: draft`
- [ ] มีครบ: ใช้เมื่อ / fork / กับดัก / ช่องผู้เชี่ยวชาญเติม / disclaimer
- [ ] voice ผ่าน house style · ไม่มี AI-trope · ไม่มี PII หลุด
- [ ] ตัวเลขตัวอย่างกำกับว่า illustrative

---

## ขั้น 5 — verify: ก่อนปล่อย ตามความเสี่ยง

**นี่คือ gate ที่ห้ามข้าม.** ระดับ verify ขึ้นกับ **ของชิ้นนั้นกระทบคนไข้แค่ไหน**.

| ความเสี่ยง | ตัวอย่าง domain | ต้องทำก่อน ship |
|---|---|---|
| 🔴 **กระทบคนไข้โดยตรง** | bloodbank, hema/coag, clinchem critical value, transfusion, micro MDR report, tox confirm | **ขอ MT อีกคน/peer-review ยืนยัน** · disclaimer แข็ง (ตามแบบ bloodbank) · ใส่ **verify-first guard** ในตัว skill ("ก่อนเชื่อ → ทำตาม SOP + ยืนยันกับ MT/แพทย์ + อ้างมาตรฐาน") · **ห้าม auto-publish** |
| 🟡 **เทคนิค/ตกรุ่นได้** | method-validation, stats, lab-management, standard edition | verify อย่างน้อย logic ภายในไม่ขัดกันเอง · เช็ค edition มาตรฐานล่าสุด (ดู [`../STANDARDS.md`](../STANDARDS.md)) · disclaimer ระดับกลาง |
| ⚪ **non-clinical** | career, sales, prompt/AI, productivity, coding | self-review + house-style ผ่านพอ · disclaimer มาตรฐาน |

**กฎเหล็ก clinical (🔴):**
- ตัวเลข/breakpoint/dose ที่ assert = ต้องมีคนยืนยัน **หรือ** เปลี่ยนเป็น "สอนชนิด
  กับดัก + ให้ผู้ใช้ verify ตัวบท/SOP เอง" (เคยทำกับ `mt-exam-strategy`: เลิก assert
  เลขกฎหมาย → สอนชนิดกับดักแทน)
- disclaimer ต้องบอกชัด: **decision-support ไม่ใช่คำสั่งวินิจฉัย/รักษา · งานคลินิกต้อง
  MT/แพทย์ยืนยัน + อิง SOP/มาตรฐาน · ผู้นำไปใช้รับผิดชอบเอง**
- ❌ ห้ามเขียนคำว่า verified / validated / รับรองทางคลินิก / แม่นยำพิสูจน์แล้ว — **ทุก
  ตัวคือ draft ยังไม่ผ่าน formal clinical peer-review** (พูดเกินนี้ = ทำลาย credibility คลัง)

ถ้า 🔴 แต่ **ยังหา MT ยืนยันไม่ได้** → อย่าดันขึ้น `main`. ค้างไว้ใน PR (draft PR)
รอ reviewer · หรือ merge เฉพาะส่วน non-clinical ก่อน.

**Gate 5:**
- [ ] จัดระดับความเสี่ยงแล้ว (🔴/🟡/⚪)
- [ ] 🔴 → มี MT อีกคน/peer ยืนยัน + verify-first guard ในตัว skill + ไม่ auto-publish
- [ ] disclaimer match ความเสี่ยง · ไม่มีคำ overclaim · ตัวเลข = illustrative/มีที่มา

---

## ขั้น 6 — credit: ติดชื่อคนส่ง **เสมอ**

dignity = กองกลางไม่ตาย. คนลงขันต้องเห็นชื่อตัวเอง (เว้นแต่เขาขอ anonymous).

ติด credit 2 ที่:

**1. ใน `author:` ของ skill** (ถ้าเขาส่งทั้งตัว/เป็นแกนหลักของไฟล์)
```yaml
author: "<ชื่อ-สังกัด ที่เขายอมให้ลง> + MT Score UP!"
```
ถ้าเขาขอ anonymous หรือไม่ระบุ → ใช้ `author: "MT Score UP!"` เฉยๆ.

**2. ใน `CONTRIBUTORS.md`** (ราก repo) — **ทุกคน ทุกรูปแบบการสมทบ** (รวมเคสที่เพชร
ของเขาถูก graft เข้าตัวเดิมแบบ merge — ไฟล์เดี่ยวไม่มี แต่ credit ต้องมี)

รูปแบบบรรทัด (ตาม CONTRIBUTING.md):
```
[ชื่อ-นามสกุล / นามแฝง] — [โรงพยาบาล/สังกัด ถ้าให้] — [สิ่งที่สมทบ]
```

> **`CONTRIBUTORS.md` มีในรีโปแล้ว** (header + ตารางว่างรอคนแรก). contributor คนแรก
> ที่ผ่าน intake นี้ = **เติมบรรทัดเขาในตาราง "รายชื่อผู้ลงขัน"** (แทนที่ comment
> ตัวอย่าง) ในขั้นนี้ พร้อม PR เดียวกับ skill — ไม่ต้องสร้างไฟล์ใหม่.

**Gate 6:**
- [ ] ถาม/ยืนยันแล้วว่าเขาอยากให้ลงชื่ออะไร (หรือ anonymous)
- [ ] `author:` ใน skill ตั้งถูก
- [ ] เพิ่มบรรทัดใน `CONTRIBUTORS.md` (ไฟล์มีแล้ว — เติมในตาราง "รายชื่อผู้ลงขัน")

---

## ขั้น 7 — ship: เข้าคลัง + บันทึก

1. **regen artifacts** (อย่าแก้ INDEX/triage/bundle ด้วยมือ — มัน auto-gen):
   ```bash
   python scripts/build_triage.py
   ```
   ดู output: ต้องขึ้น `... in-sync/updated` + **`README.md + skills/README.md cover
   all skills ✓`**. ถ้าขึ้น `⚠️ ... MISSING` → ไปเติมตัวใหม่ใน `README.md`
   (ตารางหมวด) + `skills/README.md` (catalog ละเอียด) ด้วยมือก่อน (2 ไฟล์นี้ hand-curated).

2. **CI ทำต่อให้:** push แล้ว `.github/workflows/build-triage.yml` regen INDEX/triage/
   dist อัตโนมัติเมื่อ `skills/` เปลี่ยน. (`standards-recheck.yml` เช็ค ISO edition
   รายเดือน — แยกเรื่อง ไม่เกี่ยว intake นี้.)

3. **เขียน `CHANGELOG.md`** — entry ใหม่ใต้ version ปัจจุบัน:
   - `Added` ถ้า skill ใหม่ · `Changed` ถ้า merge/graft เพชรเข้าตัวเดิม
   - บอก **ใครสมทบ + เพชรคืออะไร** สั้นๆ (เช่น "graft trap X จาก contributor เข้า `<skill>`")
   - ถ้าเป็น clinical ที่ยังรอ peer-review → โน้ตไว้ ("ยังควร peer-review")

4. **PR:** branch (ไม่ commit ตรง `main`) → commit → `Closes #<issue>` ใน PR body →
   review. clinical 🔴 → **draft PR จนกว่า reviewer MT ยืนยัน**.

5. **ปิด loop:** ตอบ Issue เดิม + แจ้งคนส่ง (ทางที่เขาส่งมา) ว่าขึ้นคลังแล้ว + ลิงก์
   raw ของ skill เขา. คนลงขันได้เห็นของตัวเองมีชีวิต = เขากลับมาอีก.

**Gate 7:**
- [ ] `build_triage.py` ขึ้น cover all ✓ (ไม่มี MISSING)
- [ ] `CHANGELOG.md` มี entry + ระบุผู้สมทบ
- [ ] PR link `Closes #<issue>` · clinical = draft PR รอ verify
- [ ] ตอบกลับ + แจ้งคนส่งว่าขึ้นคลังแล้ว

---

## สรุป checklist ทั้งสาย (ปริ้นต์ติ๊กได้)

```
ขั้น 1 รับเข้า   [ ] อยู่ในรูป Issue · รู้ที่มา+ติดต่อกลับ · รู้ชื่อ credit
ขั้น 2 triage    [ ] judgment(ไม่ใช่ตำรา) · ใน mission · PII สะอาด
ขั้น 3 dedup     [ ] อ่าน INDEX+CATALOG · รัน build_triage · ตัดสิน ใหม่/merge/ชี้เดิม
ขั้น 4 draft     [ ] frontmatter ≥8key · ใช้เมื่อ/fork/กับดัก/ช่องเติม/disclaimer · voice ผ่าน
ขั้น 5 verify    [ ] จัดระดับเสี่ยง · 🔴 มีคนยืนยัน+guard+ไม่ auto-publish · ไม่ overclaim
ขั้น 6 credit    [ ] author: ถูก · เพิ่มชื่อใน CONTRIBUTORS.md (มีไฟล์แล้ว เติมในตาราง)
ขั้น 7 ship      [ ] build_triage cover✓ · CHANGELOG · PR Closes #x · แจ้งคนส่ง
```

---

## ของค้าง maintainer (ทำให้ funnel เปิดเต็ม)

งานค้างที่ปลดล็อกช่อง "ไม่มี GitHub":
- [x] **deploy Google Form** — ✅ live: [forms.gle/N7RsgZqrHkikgfKK6](https://forms.gle/N7RsgZqrHkikgfKK6) · เสียบลิงก์ทุกจุดแล้ว
- [ ] **เติม contributor คนแรกใน `CONTRIBUTORS.md`** เมื่อผ่าน intake (ขั้น 6) — ไฟล์ + ตารางมีแล้ว รอแค่ชื่อแรก

---

*INTAKE playbook นี้เป็นแนวทางปฏิบัติของ maintainer ไม่ใช่คำสั่งทางคลินิก · ของที่กระทบคนไข้ต้องผ่านการยืนยันโดย MT/แพทย์เสมอ · ทุก skill ในคลังคือ draft ยังไม่ผ่าน formal clinical peer-review*
