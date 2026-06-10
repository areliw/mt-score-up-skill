# Skill Registry + Dedup/Merge — สเปก (Spec)

> **สถานะ:** spec / ทิศทาง — **ยังไม่ implement ครบ.** Field ที่เสนอด้านล่างเป็น *recommended*
> (ของเดิม 8 key ยังใช้ได้ ไม่ต้องแก้ทุกไฟล์ย้อนหลังพร้อมกัน). เอกสารนี้บอกว่าคลังจะโตยังไงไม่ให้พัง
> และให้ maintainer มีกฎตัดสินตอน merge ของซ้ำ — ไม่ใช่คำสั่งว่าทุก skill ต้องมีครบทุก field วันนี้.
>
> **เป้าไม่ใช่ "โต 1000 ตัว"** — เป้าคือ **"ทุกตัวคุ้มที่จะอยู่"**. commons ต้อง prune พอ ๆ กับ add.
> ตัวเลขในหัวเรื่องนี้คือ stress-test ไม่ใช่ KPI: ถ้าโครงรองรับ 1000 ได้ มันก็รองรับ 87 ได้แบบไม่เน่า.

อ่านคู่กับ: [`CONTRIBUTING.md`](../CONTRIBUTING.md) (รูปแบบไฟล์ + lane) · [`skills/INDEX.md`](../skills/INDEX.md) (manifest auto-gen) · [`prompts/triage.md`](../prompts/triage.md) (router) · [`docs/skill-hub-vision.md`](./skill-hub-vision.md) (ทำไมมีคลังนี้) · [`CHANGELOG.md`](../CHANGELOG.md) (precedent v0.7.0)

---

## 1. ปัญหา — โตแล้วพังตรงไหน

คลังตอนนี้ 87 ตัว ยังคุมด้วยตา + agent audit ไหว. ที่ 200–1000 ตัว สามอย่างพังพร้อมกัน:

- **ใหญ่:** `dist/all-skills.md` ตอนนี้ ~133K tokens. ถ้าโตเชิงเส้น 1000 ตัว = เกิน context ทุกรุ่น → bundle หมดประโยชน์ ต้อง route แบบ select ก่อนโหลด ไม่ใช่ยัดทั้งคลัง.
- **ซ้ำ:** หัวข้อซ้ำกันโดยธรรมชาติ — `bloodbank` กับ `clinical-correlation` แตะ DAT/HDN เหมือนกัน, `data-project-survival` เคยทับ `data-science-workflow` (ดู CHANGELOG v0.8.0). ที่ 1000 ตัว สองคนเขียนเรื่องเดียวกันคนละไฟล์ = แน่นอน ไม่ใช่ "ถ้า".
- **route ยาก:** triage วันนี้อ่าน `## ใช้เมื่อ` เป็น free text แล้วให้ AI เดา. ที่ 1000 ตัว free-text matching จะ ambiguous — ผู้ใช้ถามเรื่องหนึ่ง ตรงกับ 6 skill พอ ๆ กัน AI เลือกมั่ว.

ทางแก้ไม่ใช่ "เขียนให้ดีขึ้น" (subjective, ไม่ scale) แต่คือ **metadata ต่อ skill ที่ machine-readable** — ให้ script flag ของซ้ำ + ให้ router เลือกถูก + ให้ audit ตรวจได้โดยไม่ต้องอ่านครบทุกไฟล์.

---

## 2. Frontmatter schema ที่เสนอ — ต่อยอดของเดิม 8 key

ของเดิม (บังคับ — ห้ามถอด): `skill` · `title` · `type` · `needs` · `author` · `last_edited` · `status` · `disclaimer`

เพิ่ม **4 field แนะนำ** ที่จ่ายไฟให้ dedup + routing + audit:

```yaml
---
skill: bloodbank-judgment
title: โค้ชธนาคารเลือด — ตัดสินใจหน้างาน ไม่ให้คนไข้ตาย
type: ADVISE
needs: any
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "..."
# ── เสนอเพิ่ม (recommended) ──
decision: "หน้า bench ธนาคารเลือด เลือก resolve/จ่าย/workup อะไรก่อน ในเคสผลแปลก/เข้ากันไม่ได้/reaction"
domain: lab/transfusion
triggers: [ABO discrepancy, antibody ID, crossmatch, transfusion reaction, HDN, จ่าย O ฉุกเฉิน]
audience: [MT-bench, MT-student, ivd-sales]
---
```

แต่ละ field จ่ายไฟยังไง:

| field | ตัวอย่าง | จ่ายไฟให้ **dedup** | จ่ายไฟให้ **routing** | จ่ายไฟให้ **audit** |
|---|---|---|---|---|
| **`decision`** | "เลือก resolve/จ่าย/workup อะไรก่อน…" (1 ประโยค, 1 การตัดสินใจ) | 2 skill ที่ `decision` พูดเรื่องเดียวกัน = candidate ให้ merge | router จับคู่ "ผู้ใช้กำลังตัดสินใจอะไร" → `decision` ตรงสุด | เขียน `decision` ไม่ได้เป็น 1 ประโยค = นี่หัวข้อ ไม่ใช่ skill (ดู §3) |
| **`domain`** | `lab/transfusion`, `research/stats`, `career`, `code/data` | ตีกรอบให้ dedup เทียบเฉพาะ domain เดียวกัน (ไม่เทียบ bloodbank กับ pomodoro) | filter ชั้นแรกก่อน match `triggers` → ลดของที่ต้องเทียบ | จัดกลุ่มดู coverage/gap ต่อ domain ได้โดยไม่ต้องอ่านทั้งคลัง |
| **`triggers`** | keyword/วลีที่ผู้ใช้พิมพ์จริง | trigger ทับกันเยอะ = สัญญาณซ้ำ | router หลัก: match คำผู้ใช้ → trigger (เร็ว, deterministic กว่าอ่าน free text) | flag trigger ที่ไม่มีใน body (โฆษณาเกินของจริง) |
| **`audience`** | `MT-bench`, `MT-student`, `ivd-sales`, `researcher`, `lab-manager` | 2 skill เนื้อเหมือนแต่ audience ต่าง = อาจ "เลือก X เมื่อ Y" ไม่ใช่ merge | router เสริม: ผู้ใช้บอกบทบาท → กรอง skill ที่ตรงคน | เห็น audience ไหนคลังขาด (เช่นไม่มีอะไรเล็งสาย sales) |

**กฎความเข้ากันได้ (backward-compat):**
- field ใหม่ทั้ง 4 = **optional**. skill เดิมที่ไม่มี ยังโหลด/route ได้ปกติ (triage fallback ไป `## ใช้เมื่อ` แบบเดิม).
- เติมแบบ incremental — แตะ skill ตอนแก้อยู่แล้วก็เติมไปด้วย ไม่ต้อง big-bang migration.
- `triggers`/`audience` เป็น YAML list. `decision`/`domain` เป็น string. ค่า `domain`/`audience` ใช้ controlled vocab (ดู §6) เพื่อไม่ให้สะกดเพี้ยนจน filter พลาด.

---

## 3. วินัย: scope ตาม "การตัดสินใจ" ไม่ใช่ "หัวข้อ"

นี่คือกฎที่กันคลังบวมมากกว่า field ใด ๆ.

- **หัวข้อซ้ำกันโดยธรรมชาติ** — "ธนาคารเลือด" "anemia" "SQL" เป็นก้อนกว้าง คนสิบคนเขียนได้สิบไฟล์ ทับกันหมด.
- **การตัดสินใจมีขอบคม** — "เลือก crossmatch แบบไหนเมื่อ screen ลบ vs บวก" คือจุดเดียว ตอบได้ว่าซ้ำหรือไม่ซ้ำ.

คลังนี้เก็บ **judgment (เลือกอะไรเมื่อไหร่ + กับดัก)** ไม่ใช่ **knowledge (ตำรา/AI รู้อยู่แล้ว)**. scope ตามการตัดสินใจเป็นวิธีบังคับให้เป็น judgment โดยอัตโนมัติ — เพราะ "การตัดสินใจ" ต้องมีทางเลือก ≥2 + เกณฑ์เลือก ซึ่งคือ judgment พอดี.

### แบบทดสอบรับ skill (acceptance test)

> **"skill นี้ช่วยตัดสินใจอะไร 1 อย่าง?"**
> **ตอบเป็นประโยคเดียวไม่ได้ = นี่คือหัวข้อ ไม่ใช่ skill.**

- ตอบได้ 1 ประโยค → เขียนลง field `decision` ได้เลย → ผ่าน.
- ต้องใช้ "และ…และ…และ" หลายเรื่อง → นี่คือ **หัวข้อ** → แตกเป็นหลาย skill ตามการตัดสินใจ หรือมันคือ knowledge ที่ควรชี้ไป digest/ตำรา.
- เขียนได้แต่ไปชนกับ `decision` ของ skill ที่มีอยู่ → ไป **§4 (merge play)** ไม่ใช่สร้างไฟล์ใหม่.

ตัวอย่างขอบคม:
- ❌ หัวข้อ: "ธนาคารเลือดทั้งหมด" — ตอบ 1 ประโยคไม่ได้.
- ✅ การตัดสินใจ: "ผลแปลก/เข้ากันไม่ได้/reaction → ทำอะไรก่อน + กับดักที่ถึงตาย" — 1 ประโยค, มี fork ในตัว, นี่คือ `bloodbank-judgment`.

(หมายเหตุขนาด: skill clinically-dense อย่าง `bloodbank-judgment` ยาว ~206 บรรทัด มีหลาย fork — **ไม่ขัดกฎ** เพราะทุก fork อยู่ใต้การตัดสินใจเดียว "หน้า bench นี้ ทำอะไรก่อน". หลาย fork ≠ หลายหัวข้อ.)

---

## 4. Merge play — ของซ้ำจากหลายคน (90% ซ้ำ เพชรคนละ ~10%)

สถานการณ์ที่จะเกิดบ่อยที่ 200+ ตัว: สามคนส่ง skill เรื่องเดียวกัน เนื้อ 90% ทับกัน แต่แต่ละคนมี **เพชร ~10%** ที่คนอื่นไม่มี (war-story, กับดักเฉพาะ, เกณฑ์ที่เจอจริง).

**สองทางที่ผิดทั้งคู่:**
- ❌ เลือก 1 ตัว ทิ้งที่เหลือ → ทิ้งเพชรของอีกสองคน + contributor ถอดใจ ("ส่งไปก็ไม่ได้ใช้").
- ❌ เก็บหมดทุกไฟล์ → คลังบวม ซ้ำ 90% router งง.

**ทางที่ถูก — graft (ต่อกิ่ง):**

1. เลือก **1 canonical** (โครงดีสุด/ครบสุดเป็นฐาน).
2. **สกัดเพชรจากทุกคน** graft เข้า canonical — เพชร = judgment/trap/เกณฑ์ที่ **unique จริง** (ไม่ใช่พูดเรื่องเดิมด้วยคำต่าง).
3. **ติดชื่อทุกคน** — ทุกคนที่มีเพชรเข้า canonical ได้เครดิต (frontmatter `author` + footer provenance, ดู §5).
4. ไฟล์ที่ถูกดูดเพชรออกแล้ว → ลบไฟล์ แต่ **คุณค่าไม่หาย** (อยู่ใน canonical).

**Precedent มีจริงในคลังนี้:** CHANGELOG **v0.7.0** — drop 19 skill ตอน reconcile PR #11 แต่ **สกัด 33 เพชร graft เข้า 15 skill เดิม** (ตัวไฟล์ทิ้ง คุณค่าดูดเข้าตัวที่อยู่). ขนาดไม่บวม (+40 บรรทัดรวม 15 ไฟล์), จำนวน skill คงที่ 87. **3/19 ไม่มีเพชร → รายงานตรง ๆ ไม่ยัด.** นั่นคือ play นี้ทำงานแล้ว ไม่ใช่ทฤษฎี.

### กฎย่อยตอน graft

- **reword ≠ diamond.** พูดเรื่องเดิมด้วยสำนวนสวยกว่า = ไม่ใช่เพชร อย่า graft. เพชรต้องเพิ่ม *การตัดสินใจหรือกับดักใหม่*.
- **conflict = signal ไม่ใช่ noise.** สองคนเขียนขัดกัน → อย่าเลือกข้างมั่ว:
  - **คนละบริบท** → graft เป็น **"เลือก X เมื่อ Y, เลือก Z เมื่อ W"** (ทั้งคู่ถูกในที่ของมัน).
  - **มีคนผิดจริง** → **verify** กับมาตรฐาน/ของจริงก่อน แล้วเก็บตัวถูก + บันทึกว่าทำไม (กัน regress).
- **เพชร 0 ก้อนก็มีจริง** → ไฟล์นั้นซ้ำสนิท ทิ้งได้ตรง ๆ ติดเครดิต "ยืนยันของเดิม" ให้ก็พอ.

**Dignity:** ติดชื่อครบทุกคนคือเรื่องเป็นเป็นตาย ไม่ใช่มารยาท. นี่คือ **"กองกลางที่ทุกคนช่วยกันลงขัน"** — contributor ที่ส่งของแล้วเห็นชื่อตัวเองในของที่คนใช้จริง = ส่งต่อ. ส่งแล้วหาย = ถอดใจ คลังตาย. graft + ติดชื่อ = กลไกกัน contributor ถอดใจ.

---

## 5. สองชั้น: provenance แยกจาก judgment body

ปัญหาเมื่อ graft หลายคน: ถ้าเอา "ใครเขียนอะไร / ขัดกันตรงไหน / ประวัติแก้" ไปแทรกในเนื้อ judgment — **AI ที่โหลดไฟล์จะงง** (อ่านเจอ meta-talk ปนคำแนะนำ แยกไม่ออกว่าอันไหนคือสิ่งที่ต้องทำ).

แยกสองชั้น:

- **Layer A — Judgment body (สำหรับ AI โหลด):** เนื้อ skill สะอาด — `## ใช้เมื่อ` → fork → กับดัก. **ไม่มี** "คนนี้เถียงคนนั้น" "เวอร์ชันก่อนเขียนว่า". AI อ่านแล้วทำตามได้เลย.
- **Layer B — Provenance (สำหรับคน):** ชื่อ contributor + เพชรของใคร + conflict ที่ resolve ยังไง + ประวัติ merge → อยู่ใน **frontmatter (`author`)** + **footer block** ใต้ `---` ปิดไฟล์ + **`CHANGELOG.md`**. คนอ่านเพื่อให้เครดิต/ตรวจสอบ/เข้าใจที่มา.

ตัวอย่าง footer provenance (Layer B):

```markdown
---
*เครื่องมือช่วยคิด...เพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์... (disclaimer เดิม)*

<!-- provenance — สำหรับคน ไม่ใช่ instruction ให้ AI -->
> **ที่มา/เครดิต:** canonical โดย [A]. graft เพชร: [B] (กับดัก daratumumab interfere panel) · [C] (เกณฑ์ FMH > standard dose → KB/flow).
> **conflict ที่ resolve:** [B] ว่า prewarm ทุกเคส cold-auto / [C] ว่าเฉพาะเมื่อบัง allo → เก็บเป็น "prewarm เมื่อ auto บัง screen, ไม่ใช่ทุกเคส" (verify กับ AABB).
```

> **กฎสัญญาณ:** ถ้า **AI งง** เวลาใช้ skill ที่ merge มา = สัญญาณว่า merge แบบ **"ต่อกัน" (concatenate) ไม่ใช่ "ย่อย" (integrate)** — provenance รั่วเข้า body, หรือ fork ซ้อนกันจน contradictory. กลับไป integrate ใหม่: เพชรต้องหลอมเข้า fork เดิม ไม่ใช่แปะต่อท้ายเป็นก้อนแยก.

---

## 6. เครื่องมือ — flag กับ enforce อยู่คนละที่

สเปกนี้ไม่มีค่าถ้าไม่มีของบังคับ. แบ่งงานสองชั้น:

### `scripts/check_duplicates.py` — flag cluster (ผู้ช่วย ไม่ใช่ผู้ตัดสิน)

> **สถานะ: มีแล้ว (v1) — รัน `python scripts/check_duplicates.py`.** v1 วัดด้วย char-3gram Jaccard บน *body* (ไม่ต้องรอ field ใหม่). ขอบเขตที่ยังเสนอต่อยอด:

- v1 ทำแล้ว: เทียบ body ทุกคู่ → flag คู่ที่ similarity ≥ threshold (default 0.22) → **รายการ candidate ให้คนรีวิว** ("A ↔ B ทับ 0.27 — merge ไหม?") · `--json`/`--fail-over` สำหรับ CI · **ไม่ auto-merge** (merge ต้องใช้ judgment คนตาม §4). เหมือน `standards-recheck.yml` ที่ flag edition ให้คนดู ไม่ auto-push.
- ต่อยอด (เมื่อ field ใหม่แพร่หลายพอ): เทียบบน `triggers` + `domain` + `decision` แทน body ดิบ → cluster แม่นขึ้น (เทียบเฉพาะ domain เดียวกัน, trigger Jaccard).
- ต่อยอด: flag `triggers` ที่ไม่ปรากฏใน body (overclaim), skill ที่ไม่มี `decision`, ชื่อไฟล์/`skill:` ไม่ slug-case.

### `build-triage` CI — enforce schema (gate จริง)

`.github/workflows/build-triage.yml` + `scripts/build_triage.py` เป็นที่ **บังคับ schema** เพราะรันทุก push อยู่แล้ว. เพิ่ม validation:

- **required key ครบ** (8 เดิม) + ค่าไม่ว่าง + `type ∈ {ADVISE, DO, CALIBRATION}` · `needs ∈ {any, code-interpreter, persistent-memory}`.
- **`domain`/`audience` ตรง controlled vocab** (ถ้ามี field) — กันสะกดเพี้ยน.
- **`skill:` unique + slug-case** — กันชื่อชน/`_` vs `-` ที่ทำ raw-URL พัง.
- **fail build ถ้าผิด** → skill malformed ไม่หลุดเข้า `main` ทำ INDEX/triage/bundle พัง.

> controlled vocab ของ `domain`/`audience` เก็บที่เดียว (เสนอ: ต้นไฟล์ `build_triage.py` หรือ `docs/skill-registry-spec.md` นี้) — เพิ่มค่าใหม่ = แก้ที่เดียว.

---

## 7. สรุปสั้น — สิ่งที่ทำได้เลย vs สิ่งที่เป็นทิศทาง

**ทำได้เลย (low-cost, ไม่ต้องรอ implement):**
- ใช้ **แบบทดสอบ §3** กับทุก skill ที่รับเข้าใหม่ (ถามคำเดียว, ไม่ต้องมีเครื่องมือ).
- ใช้ **merge play §4** ทุกครั้งที่เจอของซ้ำ (precedent v0.7.0 พิสูจน์แล้ว).
- เติม field `decision`/`domain`/`triggers`/`audience` แบบ incremental ตอนแก้ skill อยู่แล้ว.

**ทำได้เลย — มีเครื่องมือแล้ว:**
- `scripts/check_duplicates.py` (v1 — รันได้: char-3gram Jaccard บน body, flag candidate ให้คนรีวิว).

**เป็นทิศทาง (ต้อง implement):**
- ต่อยอด `check_duplicates.py` ให้ใช้ `triggers`/`domain`/`decision` แทน body ดิบ (เมื่อ field ใหม่แพร่หลายพอ).
- schema validation ใน `build_triage.py` CI.
- controlled vocab สำหรับ `domain`/`audience`.

**ไม่ลืม:** เป้าคือ **"ทุกตัวคุ้มที่จะอยู่"** ไม่ใช่ตัวเลข. ทุก add ควรมาคู่กับคำถาม "ตัวไหนควร prune". registry ที่ดีไม่ใช่ที่ที่ของเข้าง่าย — แต่เป็นที่ที่ของซ้ำถูกหลอม ของตายถูกตัด และคนให้ทุกคนได้ชื่อติดของที่คนใช้จริง.

---
*เอกสารสเปก/ทิศทางสำหรับ maintainer — ไม่ใช่ instruction ให้ AI โหลดเป็น skill. ทุก skill ในคลังยังเป็น `status: draft` ยังไม่ผ่าน clinical peer-review.*
