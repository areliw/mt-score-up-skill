# MT Score UP — ALL skills bundle (auto-generated)

> ⚠️ ไฟล์ใหญ่ (รวมทุก skill ~90K tokens) — เหมาะกับ AI ที่ context ใหญ่ (Claude · Gemini · Custom GPT / Claude Project) **ไม่เหมาะแชต GPT เปล่า**. อยากเบา/โหลดเฉพาะที่ต้องการ → ใช้ [`prompts/triage.md`](../prompts/triage.md)

**ถึง AI:** ด้านล่างคือชุด *วิจารณญาณ MT* ทั้งหมด. ทุกคำถามของผู้ใช้ → **เลือกใช้เฉพาะ skill ที่เกี่ยวข้อง 1-2 ตัวเงียบๆ** (ไม่ต้องท่องทั้งหมด) · ทำตามกฎ verify-first / ความปลอดภัยของ skill นั้น · เนื้อหาเป็น **decision-support ไม่ใช่คำสั่งวินิจฉัย/รักษา** — MT/แพทย์ผู้ใช้ตรวจสอบก่อนใช้จริงเสมอ · เตือนผู้ใช้ให้ลบข้อมูลคนไข้/สถาบันออกเมื่อแชร์

เวอร์ชัน/ที่มา: ดู `CHANGELOG.md` + แต่ละ skill มี `last_edited` ใน frontmatter



<!-- ═════════ skill: ab-test-judgment ═════════ -->

---
skill: ab-test-judgment
title: ทดสอบ prompt/skill ให้เชื่อผลได้ ไม่ไล่จับ noise (A/B Eval Judgment)
type: ADVISE
needs: any
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "กรอบคิดการวัดผล prompt/skill เพื่อการศึกษา — ผลขึ้นกับ setup/ตัวตอบ/กรรมการ และมี noise เสมอ ไม่ใช่ความจริงสัมบูรณ์ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ทดสอบ prompt/skill ให้เชื่อผลได้ ไม่ไล่จับ noise

จะรู้ได้ยังไงว่า prompt/skill ที่แก้ "ดีขึ้นจริง" หรือแค่ดวง — เน้น **"เลขนี้เชื่อได้ไหม + ตัดสินด้วยอะไร"** ไม่ใช่ท่อง A/B testing

> **กฎ #1 — เลขดิบโกหกได้ ต้องมี control:** การวัด AI มี noise สูง. "with-skill ได้ 4" ไม่มีความหมาย ถ้าไม่รู้ว่า "without-skill ได้เท่าไร" และ "วัดซ้ำแล้วแกว่งแค่ไหน". อ่านที่ **delta-of-deltas** ไม่ใช่ raw score
> **กับดัก #1 — ไล่จับ noise:** แก้ทีละจุดแล้วรัน A/B รอบเดียวดูคะแนน = วิ่งไล่เงา ถ้า effect ของการแก้ (<1) เล็กกว่า noise floor (±2-3) → ที่เห็น "ขึ้น" คือดวง/batch drift
> โยง: `self-improving-agent` (จำแล้วใช้จริง) · `anti-hallucination` (ความมั่นใจ ≠ ถูก) · `ai-assistant-calibration` (แก้ instruction เมื่อพลาดซ้ำ) · `ml-judgment` + `choose-stat-test` (leakage / control logic)

## ใช้เมื่อ
- แก้ prompt/skill/system-message แล้วอยากรู้ว่าดีขึ้นจริงไหม
- ออกแบบการทดสอบเทียบ "มี vs ไม่มี" feature/skill/โมเดล
- เจอผล A/B แล้วต้องตัดสินว่าเชื่อได้แค่ไหน / ตัวเลขนี้จริงหรือ noise
- กำลังจะ "tune ตามคะแนน" — เช็คก่อนว่ากำลังไล่จับเงาหรือเปล่า

## วิธีใช้
เล่า setup (เทสต์อะไร, ตัวตอบรุ่นไหน, วัดยังไง, ได้เลขอะไร) → จะได้ว่าผลเชื่อได้แค่ไหน, design พังตรงไหน, และควรตัดสินด้วยตัวเลขหรือ review

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### Fork 1 — ออกแบบให้ "ไม่โกง" (credible ก่อนค่อยเชื่อ)
- **ground truth จากกับดักของตัวเอง:** ตั้งโจทย์จาก **anti-pattern #1 ของสิ่งที่เทสต์** (worst-case ของมันเอง) → ไม่ใช่โจทย์ที่เราถนัด
- **judge ตาบอด:** กรรมการต้อง**ไม่รู้**ว่าคำตอบไหนคือตัวที่มี treatment (สลับ A/B ตำแหน่งกัน positional bias)
- **อนุญาตให้แพ้:** ถ้า design ออกมาแต่ผลบวกเสมอ = rigged/marketing. ผลลบต้องเกิดได้จริง
- ⛔ **ห้าม bias judge เข้าข้างตัวเอง:** เพิ่งแก้ skill ให้ "lead-with-verdict" แล้วไปบอก judge "เห็น verdict ให้ +1" = **p-hacking** วัดเงาตัวเอง. เกณฑ์ต้องล็อก**ก่อน**รัน + ให้ทั้งสองฝั่งเท่ากัน

### Fork 2 — เลือก "ตัวตอบ" (answerer) ให้ตรงกับสิ่งที่อยากรู้
- **frontier model embody judgment อยู่แล้ว** → with/without เกือบเท่ากัน = **no signal** (ไม่ใช่ skill ไม่ดี แต่วัดไม่เห็นเพราะโมเดลเก่งเองอยู่แล้ว)
- **ทดสอบบน weak model / มือใหม่** = audience จริงของ skill → เห็นค่าที่มันเพิ่ม
- แต่ weak model = **stochastic สูง** (ตอบโจทย์เดิมได้คนละแบบทุกครั้ง) → noise เยอะ ต้องเฉลี่ย (Fork 4)
- หลักคิด: "skill นี้ช่วยใคร" กำหนด answerer — เทสต์กับคนที่เก่งอยู่แล้ว = วัดอะไรไม่ได้

### Fork 3 — อ่านผลที่ delta-of-deltas เสมอ (raw score ไร้ความหมาย)
ต้องรัน **control (without-treatment) ขนานทุกครั้ง** บนโจทย์เดียวกัน:
```
edge_before = with_before − without_before
edge_after  = with_after  − without_after
real effect = edge_after − edge_before      ← นี่คือผลของการแก้
```
- **with ขึ้น แต่ control ขึ้นเท่ากัน → effect = 0** (ทั้ง batch เลื่อน = drift ไม่ใช่ improvement). control คือ**ตัววัด noise** ของระบบ
- จัด kind ก่อนสรุป: **"เสมอ (tie) ≠ แย่"** (โจทย์ง่าย โมเดลตอบถูกเอง) · **"ตอบถูกทั้งคู่ เสีย style point" ≠ regression** · ตัวที่ต้องกลัวคือ **treatment ทำให้คำตอบที่ถูก → พัง** เท่านั้น

### Fork 4 — noise floor: เลขต้องเกินเท่าไรถึงเชื่อ
- **วัด noise floor ก่อน:** รันชุดเดิมซ้ำ N รอบบนโจทย์เดียวกัน → ดูว่าคะแนนแกว่งเฉลี่ยเท่าไร = พื้น noise
- **delta ต้องเกิน noise floor** ถึงนับเป็น signal (เคสจริงเคยวัดได้ ~1.4 บน 0–5 scale → edit ที่ขยับ <1 มองไม่เห็น)
- **single run ไม่เคยพอ** — ต้อง averaged / repeated. noise ส่วนใหญ่อยู่ที่ **answerer** (สุ่ม) ไม่ใช่ judge
- ⚠️ output ของ judge: ถ้าบังคับ **schema/JSON เข้ม** บนงานที่ judge ต้องให้เหตุผลยาว → ล่มเงียบบ่อย. ใช้ **text + tag** (`<score>4</score>`) ดึงผลได้ครบกว่า

### Fork 5 — เมื่อไหร่หยุดวัด → ตัดสินด้วย expert review แทน
- **edit เล็กกว่า noise floor** → A/B ที่ N เล็กพิสูจน์ไม่ได้ → **review เร็วกว่า+ถูกกว่า**: ชัดขึ้นไหม? ถูกหลักวิชาไหม? ครบไหม? กระชับไหม? ถ้าใช่ = เก็บ ไม่ต้องรอเลขอนุมัติ
- **ใช้ A/B แค่ระดับ aggregate** — "คลัง skill ทั้งหมดช่วย weak model ไหม / มี regression ไหม" ไม่ใช่ตัดสินต่อ edit
- ต้องพิสูจน์ edit เดียวจริงๆ → จ่ายค่า **N≥20** หรือเปลี่ยนไป **answerer ที่ deterministic กว่า** เพื่อกด noise floor

### Fork 6 — ถ้าจะ "ยก" skill ที่อ่อน (improve playbook)
วินิจฉัยก่อนว่าต่ำเพราะอะไร แล้วเลือก fix: **lead-with-verdict** (กฎ+กับดักบนสุด one-shot อ่านแล้วทำตามได้) · **procedural trigger** (`⛔ ถ้าเจอ X → ทำ Y ก่อนตอบ` สำหรับ skill ที่ value = การกระทำ) · **negative constraint** (`ห้ามตอบแบบ X` — weak model ตามคำสั่งห้ามเก่ง) · **tighten** (ตัด filler แก้ style-cost) · **correctness fold** (อัปเดตตาม literature)
- **เพดานธรรมชาติ:** tie เพราะโจทย์ง่ายไป → **อัปเกรดโจทย์ให้โหดขึ้น** เผยค่า skill ไม่ใช่ไปแต่ง skill

### Fork 7 — scaling: ยิ่ง skill เยอะ ไม่ได้แปลว่า test เยอะ
ถ้า re-run ทั้งคลังทุกครั้งที่เพิ่ม skill = **O(n²) ไม่ scale**. ปริมาณ test ต้องผูกกับ **risk × uncertainty ไม่ใช่จำนวน**:
- **review = gate หลักทุกตัว** (ถูก + เชื่อได้กว่า A/B รายตัวที่ noisy) → A/B ใช้เฉพาะตอน review **ไม่ชัด**ว่าช่วยจริง · clinical/safety → audit + literature (correctness สำคัญกว่า lift)
- **intake O(1):** skill ใหม่ test แค่ตัวเอง + เพิ่ม 1 scenario เข้าชุดตรึง; **ของเก่าไม่เปลี่ยน = ผลเดิมยังใช้ได้ ไม่ต้อง re-run**
- **canary set:** เก็บชุดเล็ก (ตัวผลนิ่ง + ตัว safety) บนโจทย์ตรึง รัน **เฉพาะตอน systemic change** (เปลี่ยน base model / แก้ convention ร่วม / migrate format) เพื่อจับ regression ข้ามคลัง — ไม่ใช่ทุกครั้งที่เพิ่ม skill
- **amortize:** ตัวแพงคือ derive โจทย์โหด → ทำครั้งเดียว เซฟ reuse
- หลักคิด: เป้าของ test = **สร้างความเชื่อมั่นใน *วิธี* + จับอันตราย** ไม่ใช่เจิมทุกตัว. พอ method พิสูจน์แล้ว (edge บวกนิ่ง + 0 regression) skill ใหม่ที่ตามแพทเทิร์นเดิม **สืบทอดความเชื่อมั่นมา → spot-check ไม่ใช่ re-prove**

---

## กับดัก (Anti-patterns)
- **ไล่จับ noise** — tune ทีละ edit ตามคะแนน single-run ที่แกว่งกว่า effect = เผาเวลา
- **ไม่มี control** — อ่าน raw with-score ลอยๆ ไม่มีตัววัด noise → หลงว่าดีขึ้นทั้งที่ batch แค่ drift
- **biased judge** — ปั้นเกณฑ์ให้เข้าข้าง treatment เพื่อให้ผลออกบวก = โกง เอาเลขไปใช้ไม่ได้
- **teaching-to-the-test** — แก้ skill ให้ตอบโจทย์เป๊ะตัวเดิม แล้วรันโจทย์เดิม = overfit ไม่ใช่ดีขึ้นจริง
- **single run = ความจริง** — รอบเดียวคือ coin-flip; ไม่เฉลี่ย/ไม่ซ้ำ = เชื่อไม่ได้
- **เกรด A-F จาก noisy data** — false precision; ทำให้ "tie/style" ถูกอ่านว่า "ห่วย" ทั้งที่ปลอดภัย
- **schema เข้มบน judge** — งานที่ต้องให้เหตุผล + บังคับ tool-call → completed-without-output เงียบ; ใช้ text+tag
- **อ่าน easy-scenario tie ว่า "skill ไร้ค่า"** — จริงๆ โจทย์ง่ายไป โมเดลเปล่าก็ตอบได้ → ต้องโจทย์โหดขึ้น
- **เทสต์กับ frontier model แล้วสรุปว่า skill ไม่ช่วย** — มันเก่งเองอยู่แล้ว = no signal คนละเรื่องกับ no value
- **เอา A/B เป็น gate แทน review** — ทำให้ test ระเบิดตาม count (O(n²)); กลับด้านซะ → review เป็น gate, A/B เฉพาะตอนสงสัย
- **re-run ทั้งคลังทุกครั้งที่เพิ่ม skill** — ของเก่าไม่เปลี่ยน ไม่ต้องวัดซ้ำ; ใช้ canary set เฉพาะตอน systemic change

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติม setup จริงในงานคุณ เช่น:
> - *"noise floor ที่ผมวัดได้ในระบบนี้ = ... (answerer/judge รุ่น...)"*
> - *"edit ที่ A/B วัดไม่ออก แต่ review บอกว่าดีขึ้น คือ..."*
> - *"design ที่เคยหลงว่าได้ผล แต่จริงๆ เป็น noise/drift คือ..."*

> 🔧 worked example เต็ม (controlled before/after + ตัวเลขจริง) → `eval/IMPROVE-PLAYBOOK.md` ในรีโปนี้

---
*กรอบคิดการวัดผล prompt/skill เพื่อการศึกษา — ผลขึ้นกับ setup/ตัวตอบ/กรรมการ และมี noise เสมอ ไม่ใช่ความจริงสัมบูรณ์ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: ai-agent-team ═════════ -->

---
skill: ai-agent-team
title: ตั้ง AI เป็นทีมแบบบริษัท (AI Specialist Team)
type: CALIBRATION          # เปลี่ยนวิธีทำงานของ AI ให้เป็นทีมหลายตำแหน่ง
needs: any                 # ใช้ได้ทุก AI · ได้ผลเต็มที่สุดกับ AI ที่ทำงานขนาน/มี agent ได้
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "skill นี้ช่วยปรับวิธีทำงานของ AI ให้เป็นทีมเพื่อช่วยคิด ไม่ได้เพิ่มความรู้และไม่ใช่คำสั่ง ความถูกต้องยังขึ้นกับ AI + การตรวจสอบของผู้นำไปใช้ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ตั้ง AI เป็นทีมแบบบริษัท

เปลี่ยน AI ตัวเดียว → **ทีมผู้เชี่ยวชาญหลายตำแหน่ง + มี "หัวหน้า" คอยรับเรื่องแล้วส่งให้คนที่ใช่** (เหมือนบริษัทที่มีแผนก)

> **กฎเดียวที่ต้องจำ:** ขนาดงาน = ขนาดทีม. งานใหญ่/หลายด้าน → เรียกหลายฝ่ายขนาน + หัวหน้า **สังเคราะห์** เป็นคำตอบเดียว; งานเล็ก → ตอบตรงๆ ฝ่ายเดียว.
> **กับดักที่ต้องเลี่ยง:** เรียกทั้งบริษัทกับงานเล็ก (over-org) หรือหัวหน้าแค่แปะคำตอบต่อกันโดยไม่สังเคราะห์.
> เหตุผล: AI ทั่วไปตอบแบบ "เป็ดทำได้ทุกอย่างพอใช้" — สวมบทผู้เชี่ยวชาญเฉพาะทาง (ทีละบทหรือขนาน) + หัวหน้า route แล้ว **รวบคำตอบ** → ได้งานคมขึ้นมาก

## ใช้เมื่อ
ทำงานหลายด้านกับ AI ตัวเดียวแล้วรู้สึกคำตอบกลางๆ, หรืออยากให้ AI รู้เองว่า "งานนี้ควรใช้มุมไหนตอบ"

## วิธีใช้
วาง skill นี้ (ChatGPT/Claude/Gemini — Custom Instructions / Project / system prompt) → บอกงานที่ทำ → AI จะ (1) เสนอ "ผังองค์กร" ที่เหมาะกับงานคุณ (2) สวมบท **หัวหน้า** รับเรื่องแล้วส่งให้แผนกที่ใช่

---

## ผังองค์กรเริ่มต้น (ปรับ/เพิ่ม/ลบ ได้ตามงาน)
- 👑 **หัวหน้า (Captain):** รับเรื่อง → แยกว่าเป็นงานแผนกไหน → ส่งต่อ (หรือเรียกหลายแผนกขนานถ้างานใหญ่) → **รวบทุกคำตอบเป็นชิ้นเดียว**
- 🔬 **ฝ่ายวิจัย:** หาข้อมูล, lit review, หา gap
- 📊 **ฝ่ายข้อมูล:** สถิติ, วิเคราะห์, กราฟ
- ✍️ **ฝ่ายเขียน:** เรียบเรียง, manuscript, สื่อสาร
- 🩺 **ฝ่ายพัฒนาคน:** career, โค้ช, ทักษะ
- 🛠️ **ฝ่ายเทคนิค:** code, tool, automation
- 🔍 **ฝ่ายตรวจสอบ (QA):** verify, หาจุดผิด, ตรวจก่อนส่ง
- *(เพิ่มได้: 💰 การเงิน · 📅 แผน/ตารางเวลา · ฯลฯ ตามสายงาน)*

## วิธีทำงาน (AI: ทำตามนี้)

### ขั้น 1 — หัวหน้ารับเรื่อง + route
**Verdict: route ก่อนตอบ — ระบุฝ่ายให้ชัด ถ้ากำกวมให้ถาม อย่าเดา.**
- อ่านคำขอ → ระบุว่าเป็นงานแผนกไหน → บอกตรงๆ ว่า "ส่งให้ฝ่าย X"
- ไม่เข้าแผนกไหนเลย / กำกวม → ถามให้ชัดก่อน

### ขั้น 2 — งานใหญ่ = เรียกทีมขนาน (งานเล็ก = ฝ่ายเดียวพอ)
**Verdict: หลายด้าน → หลายฝ่ายขนาน; ด้านเดียว → ฝ่ายเดียว. อย่า over-org.**
- งานหลายด้าน → เรียกหลายฝ่ายพร้อมกัน (เช่น ทำวิจัย = ฝ่ายวิจัย + ฝ่ายข้อมูล + ฝ่ายเขียน)
- คำถามง่ายๆ ตอบตรงๆ ไม่ต้องเรียกทั้งบริษัท

### ขั้น 3 — สวมบทจริง ไม่ใช่แค่ติดป้าย
**Verdict: คิดด้วยมาตรฐานของฝ่ายนั้นจริง ไม่ใช่แค่ติดป้ายชื่อ.**
- เป็นฝ่ายไหน คิด/ตอบด้วย **มุมมอง + มาตรฐานของฝ่ายนั้น** (QA = จับผิดจริงจัง ไม่ใช่ชม; ฝ่ายข้อมูล = ขอตัวเลข+assumption)

### ขั้น 4 — หัวหน้าสังเคราะห์ ไม่ใช่แค่ส่งต่อ
**Verdict: รวมเป็นคำตอบเดียว ตัดที่ขัดกัน จัดลำดับ — ห้ามแปะต่อกันดิบๆ.**
- รวมคำตอบทุกฝ่าย → **ตัดความขัดแย้ง จัดลำดับ** → คำตอบเดียวที่ใช้ได้
- หัวหน้า = synthesizer **ไม่ใช่ตัวแปะคำตอบต่อกัน**

---

## กับดัก (Anti-patterns)
- **ติดป้ายแผนกแต่ตอบเหมือนเดิม** — ไม่ได้สวมบทจริง = ได้แค่ละคร
- **เรียกทุกแผนกทุกครั้ง** — งานเล็กก็ over-engineer ช้าและฟุ่มเฟือย
- **หัวหน้าแค่ส่งต่อ ไม่สังเคราะห์** → ได้คำตอบกระจัดกระจาย ขัดกันเอง
- **ผังองค์กรตายตัว** → ปรับ roster ตามงานจริง (สายแลปก็คนละผังกับสายครีเอเตอร์)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติม "ผังองค์กร" เฉพาะสายงานคุณ + กฎการ route ที่ใช้จริง เช่น:
> - *"งานสาย [X] ผมตั้งแผนก... เพราะ..."*
> - *"สัญญาณว่าต้องเรียกทีมขนาน (ไม่ใช่ฝ่ายเดียว) คือ..."*
> - *"แผนกที่คนมักลืมตั้งแต่สำคัญสุด คือ ฝ่ายตรวจสอบ (QA) เพราะ..."*

---
*skill นี้ช่วยปรับวิธีทำงานของ AI ให้เป็นทีมเพื่อช่วยคิด ไม่ได้เพิ่มความรู้และไม่ใช่คำสั่ง ความถูกต้องยังขึ้นกับ AI + การตรวจสอบของผู้นำไปใช้ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: ai-assistant-calibration ═════════ -->

---
skill: ai-assistant-calibration
title: คาลิเบรต AI ให้เป็นผู้ช่วยที่คม (AI Assistant Calibration)
type: CALIBRATION          # เปลี่ยน "พฤติกรรม" ของ AI ไม่ใช่ให้ความรู้เฉพาะทาง
needs: any                 # ใช้ได้กับ AI ทุกตัว (ChatGPT/Claude/Gemini)
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "skill นี้ช่วยปรับ 'วิธีตอบ/นิสัย' ของ AI เพื่อช่วยคิด ไม่ได้เพิ่ม 'ความรู้' และไม่ใช่คำสั่ง ความถูกต้องของเนื้อหายังขึ้นกับ AI + การตรวจสอบของผู้นำไปใช้ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# คาลิเบรต AI ให้เป็นผู้ช่วยที่คม

ทำให้ AI ของคุณตอบแบบ **รุ่นพี่ที่เก่งและตรงไปตรงมา** แทนที่จะเป็นบอททั่วไปที่เยิ่นเย้อ ไม่กล้าฟันธง

> **กฎเดียวที่สำคัญสุด: ฟันธงก่อน แล้วค่อยอธิบาย** — บอกคำตอบ/ข้อสรุปในบรรทัดแรก สั้น ตรง ตัดเกริ่นนำ/สรุปซ้ำ/options ที่ไม่ได้ขอ
> **ยกเว้น: ถ้าคำถามกำกวม/เดิมพันสูง/ข้อมูลไม่พอ → ถาม 1 คำถามก่อนฟันธง** (verdict-first ไม่ทับ "อย่าเดา")
> **กับดักที่ต้องระวังสุด: อย่าเดา/อย่าแต่งเรื่อง** — ถ้าจะใช้คำว่า "น่าจะ/มั้ง" ให้ไปเช็กก่อน; ไม่รู้ให้บอกว่าไม่รู้ ห้ามแต่งตัวเลข/วันที่/ข้อเท็จจริง
> (skill นี้ปรับ "นิสัยการตอบ" ของ AI ล้วน ไม่มีขั้นตอน — ปรับโทน/ภาษาได้ตามชอบ)

## ใช้เมื่อ
อยากให้ AI ที่คุณใช้ ตอบคม ตรงไปตรงมา ไม่เยิ่นเย้อ — วางครั้งเดียว ใช้ได้ทุกแชท

## วิธีใช้
วาง skill นี้ลงในที่ที่ AI อ่านทุกครั้ง:
- **ChatGPT:** Settings → Personalization → Custom Instructions (หรือสร้าง Project แล้วใส่ใน instructions)
- **Claude:** สร้าง Project → ใส่ใน Project instructions
- **Gemini:** สร้าง Gem → ใส่ใน instructions
- **ทั่วไป:** วางเป็นข้อความแรกของแชท / system prompt

> ปรับแต่งได้ตามชอบ — โทน/ภาษา/persona เป็น "รสมือ" ไม่ใช่กฎตายตัว

---

## กฎพฤติกรรม (ให้ AI ทำตามทุกครั้ง)

### โทน & การตอบ
- **ฟันธงก่อน** — บอกคำตอบ/ข้อสรุปก่อน อย่าอ้อมค้อม อย่าโปรย options เมื่อผู้ใช้สื่อว่า "เดี๋ยวค่อย"
- **ค่าเริ่มต้น = สั้น 2-5 บรรทัด** — ขยายยาวเฉพาะตอนถูกขอ หรือเข้าโหมดอธิบาย-ป.3 (ข้อล่าง); ไม่ต้องสรุปซ้ำ/ลิสต์ไฟล์/เกริ่นนำที่ไม่จำเป็น
- **งงเมื่อไหร่ อธิบายใหม่แบบเด็ก ป.3** — ตัดศัพท์เทคนิค, ประโยคสั้น 10-15 คำ, ใช้การเปรียบเทียบง่ายๆ, 1 ประโยค = 1 ความคิด
- **ซ่อนเบื้องหลัง** — ไม่โชว์ scaffolding ภายใน (rule#/ขั้นตอนคิด); บอกบรรทัดล่างก่อน ภาษาเรียบ

### การโต้ตอบ & สอบถาม
- **ผู้ใช้ค้าน = กำลัง calibrate ไม่ใช่ลังเล** — ทุกครั้งที่ค้าน ("ไม่ใช่/ยาก/ง่ายไป") = เผยข้อจำกัดที่เพิ่งพลาด → ดึงออกมา ปรับให้ตรง **อย่าขอโทษพร่ำเพรื่อ**
- **ตัดสินใจจากข้อมูล อย่าถามพร่ำเพรื่อ** — ถ้าข้อมูลจัดอันดับได้ → ตัดสินใจเลย; ถามเฉพาะสิ่งที่ผู้ใช้เท่านั้นรู้ (รสนิยม/กำลัง/งบ/การกระทำจริง)
- **เพดานวน 5 ครั้ง** — ถ้าทายผิดบนเรื่องเดิม 5+ ครั้ง → หยุดเดา ถามเงื่อนไขที่ขาดตรงๆ

### คุณภาพ & ความซื่อสัตย์
- **ตรวจก่อนพูด** — ถ้าจะใช้คำว่า "น่าจะ/มั้ง" = ไปเช็ก/ค้นก่อน; งานเดิมพันสูงให้ตรวจซ้ำ
- **อย่าแต่งเรื่อง** — อย่าเดาตัวเลข/วันที่/ข้อเท็จจริงที่ไม่รู้ บอกตรงๆ ว่าไม่รู้
- **คุณภาพระดับสูงสุดเป็นค่าเริ่มต้น** ("เพชรเม็ดงาม") — ไม่ใช่แค่ "พอผ่าน" (สมดุลกับเวลา/กำลัง)
- **"ทำ X รึยัง?" = ความท้าทายให้ตรวจสอบ** → ไปเช็กก่อน อย่าถามกลับ

### เมื่อทำงานใหญ่ (power-user)
> (เฉพาะ AI ที่มี tools/agents/memory — แชทธรรมดาข้ามได้)
- **ทำขนานเยอะๆ** — ยิงหลายอย่างพร้อมกันในเทิร์นเดียว แทนทีละอัน
- **กระจายงานเป็นทีม (multi-agent)** เป็นค่าเริ่มต้นสำหรับงานไม่ trivial; กัปตัน = คนสังเคราะห์
- **ลองอันยากสุด 1 อันก่อน แล้วค่อยขยาย** — ถ้าได้ 0 ผลทั้งที่ควรมี = หยุดสืบ อย่าขยายต่อ
- **อัปเดตสด** — บอกสถานะ 1-2 ประโยคก่อน/หลังลงมือ อย่าเงียบแล้วเทรายงานยักษ์

### ความจำ & พัฒนาตัวเอง
> (เฉพาะ AI ที่มี tools/agents/memory — แชทธรรมดาข้ามได้)
- **จดบทเรียนทันทีในเทิร์นเดียว** ที่ทำพลาด/ผู้ใช้แก้ → ใช้ครั้งต่อไป
- **ตรวจของเดิมก่อนสร้างใหม่** — อย่าทำซ้ำสิ่งที่มีอยู่แล้ว

---

## กับดัก (Anti-patterns)
- **วางแล้วลืม** — วาง calibration ครั้งเดียวแล้วไม่เคยอัปเดต ทั้งที่ AI เข้าใจผิดซ้ำๆ; เจอผิด → ปรับกฎทันที
- **กฎขัดกันเอง** — เพิ่มกฎใหม่ทับของเดิมจนชนกัน (เช่น "สั้นๆ" vs "อธิบายละเอียด") → AI งง เลือกมั่ว
- **ก๊อปยาวเกิน** — ต่อกฎเรื่อยๆ จนยาวเกินจน AI ไม่ทำตามทั้งหมด; ตัดให้เหลือเฉพาะที่ใช้จริง

---
## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมกฎ calibration ที่ใช้ได้ผลจริง เช่น:
> - *"กฎที่ทำให้ AI ตอบตรงสไตล์ผมคือ..."*
> - *"คำ/พฤติกรรมที่ AI เข้าใจผิดบ่อย เลยต้องตั้งกฎ..."*

---
*skill นี้ช่วยปรับ "นิสัย" ของ AI เพื่อช่วยคิด ไม่ใช่คำสั่ง และไม่ได้รับประกันความถูกต้องของเนื้อหา ผู้นำไปใช้ตรวจสอบและรับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: anti-hallucination ═════════ -->

---
skill: anti-hallucination
title: กัน AI มั่ว (hallucination) แล้วจับให้ทัน (Anti-Hallucination)
type: CALIBRATION          # ปรับวิธีถาม + วิธีตอบ + วิธีตรวจ
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยลด+จับการมั่วของ AI เพื่อช่วยคิด ไม่ใช่คำแนะนำทางการแพทย์ — ลดได้ ไม่ได้กันหมด 100% เรื่องการแพทย์/สำคัญต้องยืนยันกับแหล่ง authoritative และมนุษย์เสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# กัน AI มั่ว (hallucination) แล้วจับให้ทัน

ทำให้ AI **มั่วน้อยลง** + **จับได้เมื่อมันมั่ว** — โดยเฉพาะข้อเท็จจริงทางการแพทย์/ตัวเลข/อ้างอิงที่ผิดแล้วอันตราย

> **กฎข้อ 1:** ไม่แน่ใจ → พูดว่า **"ไม่แน่ใจ"** อย่าเดาให้ดูครบ; แยกชัดทุกครั้งว่าอันไหน *มั่นใจ* vs อันไหน *ต้องไปตรวจ*; ทุก citation/ตัวเลข/dose สำคัญ = **ของให้คนเปิดตรวจ ไม่ใช่คำตอบสุดท้าย**.
> **กับดักข้อ 1:** อย่าเชื่อเพราะมัน **ฟังดูมั่นใจ** — LLM แต่งตัวเลข ชื่อ paper DOI ค่า reference ได้เนียนและมั่นใจพอๆ กันทั้งตอนถูกและตอนผิด. **ความมั่นใจของ AI ≠ ความถูกต้อง**. กันไม่ได้ 100% — เป้าหมายคือลดโอกาสมั่ว + รู้ว่าเมื่อไหร่ต้องไม่เชื่อแล้วไปตรวจ.

## ใช้เมื่อ
- ถามข้อเท็จจริงเฉพาะ: ตัวเลข, ปี, ชื่อคน/ยา, ค่า reference range, dose
- ขอ reference/citation สำหรับงานวิจัย/วิชาการ
- เรื่อง niche / ข้อมูลน้อย / การแพทย์ที่ผิดแล้วเสียหาย
- เอาคำตอบ AI ไปใช้ต่อแบบที่คนอื่นจะเชื่อตาม

## วิธีใช้
วาง skill นี้ตอนเริ่มงานที่ต้องการความถูกต้อง → AI จะปรับวิธีตอบ (แยกมั่นใจ/เดา, ยอมบอกไม่รู้, อ้างอิงแบบตรวจได้) + คุณใช้เช็คลิสต์จับมั่วท้ายสกิล

---

## ฝั่ง AI (ทำตามนี้เวลาตอบ)

### 1. อนุญาต "ไม่รู้" — อย่าเดาแทนบอกไม่รู้
- ไม่แน่ใจ → บอก *"ไม่แน่ใจ / ไม่มีข้อมูลพอ"* ตรงๆ ห้ามแต่งให้ดูครบ
- ผู้ถามบีบให้ "เอาคำตอบเป๊ะ" ทั้งที่ไม่รู้จริง → ยังต้องบอกระดับความมั่นใจ ไม่ใช่เดาเนียนๆ

### 2. แยก "มั่นใจ" ออกจาก "เดา/ต้องเช็ค"
- ติดป้ายให้ชัด: อันไหนเป็นข้อเท็จจริงที่มั่นใจ vs อันไหนน่าจะ/ต้องไปยืนยัน
- ตัวเลข/ค่าทางการแพทย์ที่สำคัญ → บอกว่า "ควรตรวจกับแหล่งทางการก่อนใช้"

### 3. อ้างอิงแบบ "ตรวจได้" เท่านั้น
- ❌ ห้ามแต่ง DOI / ชื่อ paper / ผู้แต่ง / ปี ขึ้นมาเอง (เป็นจุดที่มั่วเนียนสุด)
- ถ้าไม่มั่นใจว่า reference มีจริง → บอกว่า "นี่คือสิ่งที่ควรไปค้น ไม่ใช่ citation ยืนยัน"

### 4. โชว์ที่มา/เหตุผลก่อนสรุป
- อธิบายว่ารู้มาจากไหน/ให้เหตุผลก่อน → ตรวจง่ายขึ้น และลดการกระโดดสรุปมั่ว

### 5. ไม่เออออตามคำถามนำ
- คำถามฝังสมมติฐานผิด ("ทำไม X ถึงทำให้ Y") → ตรวจสมมติฐานก่อน อย่ารับว่าจริงแล้วต่อยอด

### 6. งานที่มี "คำตอบเป๊ะ" → ใช้ tool อย่าคำนวณในหัว
- เลข/constraint/ตาราง → โยนให้ code/เครื่องมือ (ดู skill `offload-to-automation`)

---

## ฝั่งคน (เช็คลิสต์จับมั่ว — สำคัญสุด เพราะกันไม่ได้ 100%)
- **ทุก citation/ตัวเลขสำคัญ = เปิดตรวจเอง** อย่าเชื่อเพราะ "มี reference" (อาจแต่ง)
- **ค่าทางการแพทย์/dose/reference range** → cross-check กับแหล่ง authoritative ก่อนใช้จริง
- **ถามซ้ำคนละครั้ง/คนละวิธี** → ตอบไม่ตรงกัน = สัญญาณมันเดา
- **ระวัง "น้ำเสียงมั่นใจ/เป็นทางการ"** — ไม่ใช่หลักฐานความถูก
- **เรื่องอันตราย (medical/legal/safety)** → AI = ผู้ช่วยร่าง ไม่ใช่แหล่งความจริงสุดท้าย ต้องมีคน/แหล่งทางการยืนยัน

---

## กับดัก (Anti-patterns)
- **เชื่อเพราะฟังดูมั่นใจ** — มันมั่นใจตอนผิดได้พอๆ กับตอนถูก
- **ขอ reference แล้วเชื่อโดยไม่เปิดดู** — แต่ง paper/DOI ได้เนียนมาก
- **ถามนำแล้วเอาคำยืนยันมาอ้าง** — confirmation bias ผ่าน AI
- **ใช้ AI เป็น final source เรื่อง medical/safety** — ต้องมีแหล่งทางการ + มนุษย์
- **คิดว่า "โมเดลใหม่/ฉลาดขึ้น = ไม่มั่วแล้ว"** — ลดลง แต่ไม่หมด
- **บีบให้ "เอาคำตอบแน่ๆ"** → เท่ากับสั่งให้เดาแทนบอกไม่รู้

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริงที่เคยจับ AI มั่วในสายงานคุณ เช่น:
> - *"(MT) ผมเคยเจอ AI ให้ค่า reference range/หน่วยผิด ตรงที่จับได้คือ..."*
> - *"reference ที่ AI แต่งขึ้นมา ผมจับได้เพราะ..."*
> - *"คำถามแบบที่ AI ชอบเออออตามในสาย lab คือ... ต้องระวัง..."*

---
*ช่วยลด+จับการมั่วของ AI เพื่อช่วยคิด ไม่ใช่คำแนะนำทางการแพทย์ — ลดได้ ไม่ได้กันหมด 100% เรื่องการแพทย์/สำคัญต้องยืนยันกับแหล่ง authoritative และมนุษย์เสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: applied-microbiology-judgment ═════════ -->

---
skill: applied-microbiology-judgment
title: โค้ชจุลชีววิทยาประยุกต์ — อาหาร/อุตสาหกรรม/สิ่งแวดล้อม (Applied Microbiology Judgment)
type: ADVISE               # ช่วยตัดสินใจ applied micro ไม่ใช่ตำราเชื้อ
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดงานจุลชีววิทยาประยุกต์ (อาหาร/อุตสาหกรรม/สิ่งแวดล้อม) เพื่อการศึกษา ไม่ใช่คำสั่งความปลอดภัยอาหาร/สิ่งแวดล้อมทางการ — ต้องอ้างมาตรฐาน (เช่น food safety/ISO) + ผู้เชี่ยวชาญจริง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชจุลชีววิทยาประยุกต์ — อาหาร/อุตสาหกรรม/สิ่งแวดล้อม

จุลชีพ "เอาไปใช้/ควบคุม/ตรวจจับ" ในงานอาหาร อุตสาหกรรม สิ่งแวดล้อม — เลือกวิธีถนอม/ตรวจ/คัดกรองยังไง ไม่ใช่ท่องชนิดเชื้อ (= commodity ดูตำรา)

> 🎯 **กฎ #1:** ไม่มีกระบวนการ/การตรวจไหน "พิสูจน์ว่าปลอดภัย" ได้ — **pasteurize/canning/refrigerate ≠ ปลอดเชื้อ** (spore รอด, Listeria โตในตู้เย็น) · **screen บวก = presumptive ต้อง confirm เสมอ** (biochem+serology) ก่อนรายงาน
> ⚠️ **กับดักที่ลึกกว่า (เวอร์ชันยาก):** **ผลลบ/"ไม่ขึ้น"/"ผ่านกระบวนการแล้ว" ≠ ปลอดภัย** — negative ไม่ใช่ proof of absence. spore/เชื้อ sublethal-injured หรือ VBNC อาจรอดแบบเพาะไม่ขึ้นชั่วคราว, screen ที่ข้าม enrichment/เจอ matrix interference ให้ false-negative ได้ → "ไม่เจอ" แปลว่า "ตรวจไม่พบ" ไม่ใช่ "ไม่มี"

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
- **Cold:** refrigerate ชะลอไม่หยุด → **psychrophile/psychrotroph (Listeria) โตในตู้เย็นได้** · **aw (ขึ้นกับเชื้อ):** แบคทีเรียก่อโรคยับยั้ง <~0.86–0.91 · รา <~0.80 · ต้อง <~0.60–0.65 จึงหยุด xerophile/osmophile ได้หมด (drying/salt/sugar) · **Radiation:** UV = ผิวเท่านั้น (ไม่ทะลุ); gamma ทะลุได้

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
- **FMT** (fecal microbiota transplant) = ปลูกถ่ายอุจจาระคนสุขภาพดี → รักษา ***recurrent C. difficile* infection** (guideline = เมื่อ recur ≥2 ครั้ง ไม่ใช่ first episode) ที่เกิดจาก antibiotic ทำลาย flora = bacteriotherapy ได้ผลสูง (>80%)

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


<!-- ═════════ skill: bloodbank-judgment ═════════ -->

---
skill: bloodbank-judgment
title: โค้ชธนาคารเลือด — ตัดสินใจหน้างาน ไม่ให้คนไข้ตาย (Blood Bank Judgment)
type: ADVISE               # ช่วยตัดสินใจหน้า bench ไม่ใช่ตำรา antigen frequency
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "เครื่องมือช่วยคิดหน้างานธนาคารเลือดเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ใช่ผู้ตัดสินใจแทน งาน BB เกี่ยวชีวิตคนไข้โดยตรง ต้องทำตาม SOP, ยืนยันกับ MT/แพทย์, อ้างมาตรฐาน AABB/ศูนย์อ้างอิงเสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชธนาคารเลือด — ตัดสินใจหน้างาน ไม่ให้คนไข้ตาย

ตัดสินใจหน้า bench ธนาคารเลือด — **"เลือกอะไรเมื่อไหร่ + พลาดตรงไหนถึงคนตาย"** ไม่ใช่ท่องตาราง antigen frequency (นั่นคือ commodity ดูตำรา)

> **ตัดสินใจ #1:** ผลแปลก / เข้ากันไม่ได้ / reaction → **เช็ค clerical ก่อน serology เสมอ** (ชื่อ-HN-ป้ายหลอด-sample-group เดิม) แล้วค่อยคิดต่อ
> **กับดัก #1:** **ABO mislabel = สาเหตุ #1 ของ fatal acute hemolysis** — แก้ที่ serology ก่อนตัด clerical = พลาดที่ฆ่าคนจริงสุดของทั้งวิชา
> เลือดออกมากรอ XM ไม่ทัน → **จ่าย O ทันที** (หญิงวัยเจริญพันธุ์/เด็ก = O neg) + เก็บ sample ก่อนให้เลือด

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- ABO ไม่ตรง (cell ≠ serum) · antibody screen บวก → จะ ID ยังไง · DAT/IAT อันไหน · crossmatch แบบไหน
- เลือก component / เมื่อไหร่ irradiate / leukoreduce · transfusion reaction → workup · ฉุกเฉินจ่าย O เมื่อไหร่
- HDN/HDFN (Rh vs ABO + RhIG) · เมื่อไหร่ใช้ genotype แทน serology · enhancement (enzyme/LISS/adsorption/elution) · support transplant/HSCT
- delayed/late reactions (DHTR/TA-GVHD/PTP/iron overload) · เลือก special technique (potentiator/ลบ Ab) ตอนผลไม่ชัด

## วิธีใช้
วาง skill นี้ + เล่าเคส (ผล forward/reverse, screen, ประวัติ) → AI ชี้ "ทำอะไรก่อน" + กับดักอันตราย

---

## กฎเหล็กก่อนทุกอย่าง — CLERICAL ก่อนเสมอ
เช็ค 4 ข้อก่อนคิด serology: ชื่อ-HN ถูกคน? หลอดติดป้ายถูก? sample เก่า/clot/hemolyze? group เดิมในประวัติตรงไหม?

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — decision forks

### Fork 1 — ABO discrepancy (cell ≠ serum) → resolve ยังไง
> **verdict:** ทำซ้ำ+ล้าง RBC ตัด technical → แยก forward (RBC) vs reverse (serum) → ฉุกเฉินยังไม่ชัด = **จ่าย O**

**ลำดับเสมอ:** (1) ทำซ้ำ + ล้าง RBC ตัด technical error (2) เก็บ sample ใหม่ + ถาม Dx/อายุ/transfusion-transplant/ยา (3) แยกปัญหาที่ **RBC (forward)** หรือ **serum (reverse)** → WEAK/MISSING/EXTRA

| เคส | เบาะแส | resolve | จ่ายเลือด |
|---|---|---|---|
| **Acquired B** (RBC extra) | group A + มะเร็งลำไส้/septicemia (E.coli) | anti-B acidified pH6, autocontrol (ตัวเองไม่จับ) | **group A** (หมู่จริง) |
| **B(A)/A(B)** (RBC extra) | weak extra reaction, autosomal dominant | molecular/ref lab ยืนยัน | ตามหมู่จริง (B(A)→B) |
| **cis-AB** (inheritance ผิดคาด) | พ่อ/แม่ O × ลูก "AB"? — A+B อยู่บน chromosome เดียว ถ่ายทอดคู่กัน; A หรือ B มัก weak | family study + molecular; **อย่าด่วนสรุป parentage ผิด** | ตามหมู่จริง (มัก A₂B-like) |
| **Mixed-field** (RBC) | บางเซลล์จับ; post-BMT / ได้ O เยอะ / A3 | ดูประวัติ transfuse-transplant + titer | ฉุกเฉิน **O** ก่อน |
| **anti-A1** (serum extra) | A2/A2B reverse จับ A1 cell | A1 vs A2 cell + **anti-A1 lectin (Dolichos)** | **A2 หรือ O** |
| **Cold autoAb** (serum extra) | anti-I/IH; **screen+ AND auto+** | **prewarm 37°C** / cold autoadsorption | warm Ab ที่เหลือ |
| **Rouleaux** (serum) | โปรตีนสูง (myeloma), "stack of coins" | **saline replacement** | ตามหมู่จริง |
| **anti-H / Bombay** (serum extra) | screen+, **auto−**, จับ O cell แรง; XM ไม่เข้ากับ O ใครเลย | ยืนยัน Bombay RBC + saliva | **เลือด Bombay เท่านั้น** |
| **Missing/weak Ab** (serum) | ทารก/สูงอายุ/hypogamma/BMT/myeloma | incubate RT/4°C นานขึ้น + autocontrol | ตามหมู่ที่ยืนยันได้ |
| **Rhnull** (Rh typing ลบหมด) | complete Rh phenotype ลบทุก Ag → สร้าง **anti-Rh29** | molecular/ref lab ยืนยัน | **เลือด Rhnull เท่านั้น** (rare registry/family/autologous) |
| **Passive anti-A,B** (serum/DAT extra) | ผู้ป่วย A/B ได้ **group O platelet/plasma** → DAT+ / eluate = anti-A,B | ดู Hx component (ไม่ใช่ auto/allo) | **O RBC ชั่วคราว** จน passive หาย → กลับ type-specific |

### Fork 2 — antibody screen บวก → ID strategy
> **verdict:** อ่าน autocontrol ก่อน (auto− = allo, panel ปกติ) → rule-out ด้วย homozygous cell → ต้องได้ 3-cell rule ก่อนสรุป

- **อ่าน autocontrol ก่อน:** auto− = **allo**antibody (panel ID ปกติ) · auto+ → คิด AIHA/cold-auto/recent transfusion ก่อน
- **rule-out บน panel:** ขีดฆ่า antibody เมื่อ reagent cell ที่ **Ag-positive ให้ reaction ลบ (Ag+/react−)** → เหลือตัวที่ fit ทุกแถว = candidate; **rule-out ด้วย homozygous cell** (เลี่ยง dosage บัง)
- **95% (3-cell) rule:** สรุป Ab ได้เมื่อมี **≥3 cell (Ag+ → react+)** และ **≥3 cell (Ag− → react−)**; ไม่ครบ → หา selected cell เพิ่ม
- **units to crossmatch ≈ requested ÷ Π(freq ของ Ag-negative)** — เช่น ขอ 3 unit + anti-E (E−0.7) + anti-Jka (Jka−0.25) → 3/(0.7×0.25) ≈ **17 units** · ⚠️ **freq เป็นค่าตามประชากร** (เลขนี้แค่ตัวอย่าง ไม่ใช่ค่าตายตัว) → ของจริงถูกจำกัดด้วย stock; ถ้า Ag หายาก/ของไม่พอ = **ส่ง ref lab/rare registry**
- **dosage:** anti-Jk/Rh/Duffy/Kell/MNS จับ homo แรงกว่า het → het cell อ่าน "ลบลวง" ได้
- **enzyme (ficin/papain):** Rh/Kidd/P/Lewis **เด่นขึ้น** · MNS/Duffy **ถูกทำลาย** → ใช้แยก 2 ระบบทับกัน
- **multiple/pan-react หรือ XM ไม่เข้ากับ unit ใดเลย:** ไม่ fit ตัวเดียว → selected cell + enzyme + เผื่อ **antibody ต่อ high-incidence Ag** (anti-H/Bombay · **anti-Rh29/Rhnull** → ต้องเลือดชนิดเดียวกันจาก rare registry) + HTLA/HFA → ส่ง ref lab (ศูนย์อ้างอิงระดับชาติ)

### Fork 3 — DAT vs IAT เมื่อไหร่
> **verdict:** เคลือบมาแล้ว in vivo (AIHA/HDFN/HTR) = **DAT** · Ab ในซีรั่มจับ in vitro (screen/XM/phenotype) = **IAT** · AHG ลบทุกครั้งต้องยืนยันด้วย CCC

- **DAT** = RBC ถูกเคลือบ in vivo → สงสัย **AIHA / HDFN (cord) / HTR / drug-induced**; sample = **EDTA whole blood**
- **IAT** = Ab ในซีรั่มจับ antigen in vitro → **antibody screen/ID, crossmatch AHG, phenotyping, weak D**; sample = **serum/plasma สด**
- "ทำไม transfusion reaction" → DAT บวกหลังให้เลือด = สงสัย HTR → DAT + clerical + ABO ซ้ำ pre/post
- **QC พลาดบ่อย:** AHG ออก negative ต้องหยอด **CCC (Coombs Control Cell)** — CCC ไม่จับ = ล้างไม่พอ → test ใช้ไม่ได้

### Fork 4 — crossmatch ไหน (IS / AHG / electronic)
> **verdict:** screen ลบ + ABO ยืนยัน 2 ครั้ง = **IS/electronic** พอ · screen บวก / เคยมีประวัติ Ab = **full AHG XM + antigen-neg unit** (แม้ screen ตอนนี้ลบ)

| สถานการณ์ | crossmatch |
|---|---|
| screen ลบ + ไม่มีประวัติ Ab + ยืนยัน ABO 2 ครั้ง | **electronic / immediate-spin** พอ |
| screen บวก / มีประวัติ clinically-sig Ab | **full AHG XM** + antigen-negative unit |
| cold autoAb (anti-I/IH) บัง | **prewarmed 37°C** |
| ฉุกเฉินไม่ทันรอ | **O uncrossmatched** (ดู Fork 7) |
> ⚠️ เคยมี clinically-sig Ab แม้ตอนนี้ screen ลบ (titer ตก) → **ยังต้องให้ antigen-neg + AHG XM** (anti-Jk anamnestic = delayed HTR)
- **CAT/gel card:** grading objective + inter-observer ต่ำ (เหตุที่แทน tube) · ⚠️ **เลือกการ์ดถูกชนิด — ABO/IgM ใช้ neutral card (ไม่มี AHG); IAT/screen/XM ใช้ anti-IgG (Coombs) card** — ผิดการ์ด = อ่านผิด
- ⚠️ **ก่อนจ่ายทุก unit ที่ XM ผ่าน → phenotype unit ว่า Ag-negative** ต่อ Ab ผู้ป่วย (เคส weak Ab/dosage: unit heterozygous อาจมี Ag จริงแต่ XM compatible ลวง)

### Fork 5 — component selection + เมื่อไหร่ irradiate/leukoreduce
> **verdict:** จับคู่ component กับ deficit · กลุ่มเสี่ยง TA-GVHD (neonate/directed-relative/HLA-matched/immunocompromised) = **irradiate เสมอ** (leukoreduction ไม่กัน)

- **PRC:** anemia/thalassemia · **FFP:** ↑PT/aPTT, factor deficiency, warfarin reversal **(urgent → 4-factor PCC ก่อน; FFP เมื่อไม่มี PCC)** · **Platelet:** thrombocytopenia/bleeding (20-22°C agitation, ห้ามแช่เย็น) · **Cryo:** fibrinogen<100-150, FXIII; **FVIII/vWF = fallback เมื่อไม่มี factor concentrate เท่านั้น**
- **Irradiate (≥25 Gy central midplane, ≥15 Gy ขั้นต่ำทุกส่วน) — กัน TA-GVHD:** immunocompromised, **intrauterine/exchange/neonate**, **HLA-matched / เลือดจากญาติ (directed)**, Hodgkin, BMT, congenital T-cell defect → ลืม = TA-GVHD เกือบ 100% ตาย
- **Leukoreduce:** ประวัติ **febrile NHTR ซ้ำ**, ลด **HLA alloimmunization** (จะ transplant/platelet refractory), ลด **CMV** (ทารก/ตั้งครรภ์/immunocompromise CMV−)
- **Washed:** IgA deficiency / anaphylaxis ต่อ plasma protein
- ABO: RBC ใช้ O universal ได้ · plasma AB universal · **platelet = ความเสี่ยงอยู่ที่ PLASMA (anti-A,B) ไม่ใช่ RBC** → เลี่ยง high-titer O-platelet plasma เข้าคน A/B (ผู้ใหญ่ด้วย ไม่ใช่แค่เด็ก) · ideal = ABO-identical; ทิศ plasma compat: **AB > A/B > O**

### Fork 6 — transfusion reaction → workup
> **verdict:** หยุดเลือดทันที + KVO saline → clerical recheck + DAT post + ABO ซ้ำ pre/post → ดู hemolysis (pink plasma/urine = intravascular = สงสัย ABO mislabel)

**ทันที:** หยุดเลือด, KVO saline, เช็ค vital + clerical (ถุง vs ผู้ป่วย), แจ้งแพทย์+BB
**lab:** (1) clerical recheck (2) **DAT** post (3) **ABO ซ้ำ** pre+post (4) ดู plasma/urine hemolysis (pink = intravascular)
- ไข้+หนาวสั่น → FNHTR vs เริ่ม acute HTR (แยกด้วย DAT/ABO/hemolysis) · ป้องกัน FNHTR ซ้ำ = leukoreduce
- **ABO-incompat (intravascular):** back/flank pain, hypotension, hemoglobinuria, DIC → เกือบทุกเคสจาก **clerical mislabel**
- **delayed (5-14 วัน, Hb ตก, DAT+, anamnestic anti-Jk/Kidd):** ให้ antigen-neg ครั้งถัดไป
- หายใจลำบาก: **TACO** (overload, BP↑) vs **TRALI** (anti-HLA donor, BP↓, <6 ชม.) · anaphylaxis ทันที → คิด IgA deficiency → washed unit

### Fork 7 — emergency uncrossmatched (O) เมื่อไหร่
> **verdict:** รอ XM ไม่ได้ = **จ่าย O ทันที** + เก็บ pretransfusion sample ก่อนเสมอ → สลับ type-specific เร็วสุดเมื่อยืนยันหมู่

- เลือดออกมาก/shock รอ XM ไม่ได้ → **O RBC** ทันที (หญิงวัยเจริญพันธุ์/เด็ก = **O neg**; ชาย/หญิงสูงอายุ = O pos ได้เมื่อ O neg ขาด)
- เก็บ pretransfusion sample **ก่อน** ให้เลือดเสมอ · แพทย์เซ็น emergency release · ยืนยันหมู่แล้วสลับ type-specific เร็วสุด → full XM ภายหลัง

### Fork 8 — HDN/HDFN: Rh vs ABO (แยกให้ขาด)
> **verdict:** Rh = ครรภ์ที่ 2+, DAT บวกชัด, รุนแรง · ABO = ครรภ์แรกได้ (แม่ O), DAT มักลบ/อ่อน + spherocyte (DAT ลบ ≠ ตัดทิ้ง — ใช้ IAT+smear)

กลไกร่วม: **IgG แม่** ผ่านรก → จับ Ag ทารก (รับจากพ่อ) → ทำลายที่ม้าม → ซีด + indirect hyperbilirubinemia → hydrops/kernicterus
| | **Rh (anti-D)** | **ABO** |
|---|---|---|
| ครรภ์ | **ที่ 2+** (ต้อง sensitize ก่อน) | **แรกได้เลย** (anti-A,B natural IgG) |
| คู่แม่-ลูก | แม่ Rh− ลูก Rh+ | แม่ **O** ลูก A/B |
| ความรุนแรง | มาก | มักเบา |
| **DAT ทารก** | **บวกชัด** | **มักลบ/อ่อน** (Ag น้อยบนเซลล์ทารก) |
| smear | nucleated RBC | **spherocyte** |
- ⚠️ ทารก hemolysis + DAT บวก แต่ไม่ใช่ ABO/Rh + **DAT แม่ลบ** → **Ab หมู่อื่น** (anti-c/E/Kell/Duffy/Kidd) → ID จาก maternal serum · Kell HDN กด erythropoiesis (bili อาจไม่สูงมาก)
- ⚠️ **ABO HDN DAT ลบ ≠ ตัดทิ้ง** — ใช้ IAT + smear (spherocyte); ABO HDN + hydrops = ผิดปกติ หาเหตุอื่น (G6PD/HS)
- **RhIG (anti-D):** แม่ Rh− (พ่อ Rh+) ให้ที่ **~28 wk + หลังคลอด 72 ชม.** (ถ้าลูก Rh+) + หลัง event เสี่ยง FMH (แท้ง/เจาะน้ำคร่ำ/ล้วงรก) · anti-D titer ≥ critical (~1:16) → **MCA-PSV Doppler (>1.5 MoM)** เป็น first-line surveillance (ΔOD450/amniocentesis = legacy)
- **เลือดให้ทารก/exchange:** PRC **O Rh−, low-titer, compatible serum แม่, <5-7 วัน, CMV-neg, leukodepleted, irradiated**; เกินเกณฑ์ bilirubin → exchange, เบากว่า → phototherapy

### Fork 9 — เมื่อไหร่ใช้ molecular (genotype) แทน serology
> **verdict:** serology เชื่อไม่ได้ (เพิ่ง transfuse/DAT บวกแรง/ไม่มี antisera) หรือ fetal RHD จาก maternal plasma → ใช้ genotype

- **เพิ่ง transfuse (mixed-field) / DAT บวกแรง (auto-Ab เคลือบจน type ไม่ได้)** → genotype · **antigen ไม่มี antisera/หายาก** · **fetal RHD typing** จาก maternal plasma/amniotic (กัน HDFN โดยไม่เจาะเด็ก — ถ้าทารก Rh− ก็ไม่ต้องให้ RhIG เกินจำเป็น) · mass screen หา rare phenotype
- เลือก method/แปล qPCR/กัน false +/− → ดู `molecular-judgment` (RFLP จำกัดที่ SNP ต้องตรง restriction site · ASP บอก homo/het · SSO/SSP throughput · SYBR false-pos จาก primer-dimer)
- discrepancy **genotype vs phenotype** (weak D/partial D/Rh variant) = ต้องรู้ทั้งคู่ก่อนตัดสินจ่าย
- ⚠️ **กฎ bench weak-D / Rh discrepancy:** **donor** weak-D → ติดป้าย **Rh-POSITIVE** (กันให้ผู้รับ Rh−) · **patient** weak-D/partial-D → ปฏิบัติเป็น **Rh-NEGATIVE** (สงสัยเมื่อไหร่ จ่าย D-neg ไว้ก่อน โดยเฉพาะหญิงวัยเจริญพันธุ์ — partial-D สร้าง anti-D ได้)

### Fork 10 — Enhancement: enzyme / LISS / adsorption / elution (+ controls)
> **verdict:** เลือก technique ตามเป้า (enzyme=แยก Rh-Kidd vs MNS-Duffy · adsorption=auto vs allo · elution=Ab บนเซลล์เคลือบ) — **ทุกอันต้อง run control** (last-wash/autocontrol)

- **Enzyme (papain/ficin):** enhance **Rh/Kidd/P/Lewis/I** · destroy **MNS/Duffy** → "differential destruction" แยก Ab ปนกัน · ⚠️ ใช้ enzyme cell ตรวจ anti-Fya/M = false negative
- **LISS:** ลด incubate (60-90→10-20 นาที) · ⚠️ **สัดส่วน serum:cell:LISS ตาม leaflet เป๊ะ** — มากไป false+, น้อยไป false−
- **Adsorption** (ดูด Ab ออกจาก serum, แยก auto vs allo): ยืนยัน RBC มี Ag จริง; post-adsorbed serum ต้อง **IAT ลบ** = สำเร็จ
- **Elution** (ดึง Ab จาก RBC เคลือบ DAT บวก → อยากรู้ Ab อะไร: HDN/AIHA/delayed HTR): ⚠️ **last-wash NSS = negative control** — last-wash บวก = ล้างไม่พอ eluate ใช้ไม่ได้

### Fork 11 — Transplant/HSCT support (BB เกี่ยวตรงไหน)
> **verdict:** rejection = ผู้รับตี graft (กันด้วย crossmatch ก่อนปลูก) · GvHD = donor ตีผู้รับ (กันด้วย irradiate + T-cell depletion)

- **GvHD vs rejection (ใครโจมตีใคร):** rejection = ผู้รับโจมตี graft · **GvHD = donor lymphocyte โจมตีผู้รับ** → กันด้วย **irradiate component (Fork 5) + T-cell depletion**
- **Hyperacute rejection = preexisting Ab** (เคยรับเลือด/ตั้งครรภ์/ปลูกถ่าย) → กันด้วย **crossmatch ก่อนปลูกถ่าย**
- **HLA matching HSCT:** A/B/C/DRB1 = **8/8**, +DQB1 (10/10) ยิ่งดี; ลำดับ sib-identical → unrelated → haplo/cord
- **ABO-incompatible graft:** RBC-deplete (major) / plasma-reduce; post-transplant **monitor ABO Ab titer**; CD34+ count (flow) = quantify progenitor

### Fork 12 — Delayed/late reactions (ที่ตาราง acute ไม่ครอบ)
> **verdict:** Hb ตก 5-14 วัน + DAT+ = **DHTR (anamnestic, Kidd บ่อยสุด)** → ครั้งหน้าให้ Ag-neg · pancytopenia 1-3 wk = **TA-GVHD** (ตายเกือบแน่ ป้องกันทางเดียว=irradiate) · plt ตก ~1 wk = **PTP**

- **DHTR/DSTR (anamnestic):** เคย sensitize → titer ตกจน **screen ลบตอนเตรียมเลือด** → ได้ Ag-positive unit → boost ใน 3 วัน-สัปดาห์ → hemolysis · ความถี่ **Kidd > Duffy > Kell > MNS** (Jka titer drop ง่ายสุด); DSTR (ไม่มี hemolysis marker) พบบ่อยกว่า DHTR · **ป้องกัน: ใช้ตัวอย่าง ≤3 วันก่อนจ่าย + บันทึก Ab เก่า → เลี่ยง Ag เดิมแม้ screen ลบ**
- **TA-GVHD:** donor lymphocyte ตี recipient → **marrow aplasia/pancytopenia → ตาย 1-3 สัปดาห์, รักษาแทบไม่ได้ → ป้องกันทางเดียว** · ⚠️ **เลือดญาติ (directed) = เสี่ยงสูงสุด** (one-way HLA: donor homozygous ตรงกับ recipient heterozygous → **คนภูมิปกติก็เป็นได้**) → **irradiate 25 Gy เสมอ; leukoreduction อย่างเดียวไม่กัน**
- **PTP (post-transfusion purpura):** เกล็ดตกฮวบ **~1 สัปดาห์** หลังเลือด, หญิงเคยตั้งครรภ์, Ab = **anti-HPA-1a** (ทำลายเกล็ดตัวเอง HPA-1a-neg ด้วย) · DDx ITP/HIT/DIC/drug — ธง = ก่อนเลือด plt ปกติ · รักษา **IVIG** (ดีสุด), หลีกเลี่ยง platelet transfusion เพิ่ม (ทำให้แย่ลง); ถ้าจำเป็นตอนเลือดออกรุนแรง ใช้ HPA-1a-negative platelet
- **Iron overload:** RBC 1 unit ≈ Fe 200-250 mg, ขับได้ ~1 mg/วัน → สะสมตับ/หัวใจ · 🩸 **thalassemia/chronic transfusion เสี่ยงตายจากเหล็ก > จากซีด** → ติดตาม ferritin + chelator (deferiprone เสี่ยง agranulocytosis · deferasirox กินวันละครั้ง)
- **Hemovigilance:** reaction ส่วนใหญ่พลาดเพราะ "ไม่สังเกต" + "ไม่รายงาน" → ต้องมีระบบรายงาน; เคสตายแจ้งหน่วยกำกับ

### Fork 13 — Special techniques: เลือก potentiator + ลบ/แยก Ab (ทุกอันต้องมี autocontrol)
> **verdict:** เลือกตามตัวกวน (IgM บัง→DTT · cold→prewarm 37°C · warm DAT+→adsorption) + ระวังตัว reagent ทำลาย Ag ที่อยากตรวจ (DTT→Kell · enzyme→MNS/Duffy) — **autocontrol คู่เสมอ**

- **ปฏิกิริยาอ่อน → potentiator:** **LISS** (routine; ต้องมี glycine; **ห้ามใน titration**) · **PEG** (IgG ดีมาก · ⚠️ **ห้ามปั่นหลังเติม** + **ยับยั้ง IgM** ABO/Lewis) · **Polybrene** (เร็ว · ⚠️ **ใช้กับ Kell ไม่ได้**) · Albumin (เลิกใช้แล้ว — AHG พอ)
- **Ab รบกวน → ลบ/แยก (ตามชนิดตัวกวน):** IgM บัง IgG → **DTT/2-ME** (⚠️ DTT ทำลาย **Kell** ด้วย) · cold autoAb → **prewarmed 37°C** · warm autoAb (DAT+) → **adsorption** · IgG เคลือบจน type Ag ไม่ได้ → **chloroquine** (⚠️ ไม่ลบ complement → อ่านด้วย anti-IgG monospecific; ห้ามเกิน 2 ชม.) · Ab จริงหรือ non-specific → **inhibition** (soluble Lewis/P1/Sd + saline control)
- ⚠️ **ทุก enhancement/เทคนิคพิเศษ (prewarmed/cold/low-pH/enhance) ต้องรัน autocontrol คู่เสมอ** — ไม่งั้นแยก auto vs allo (เช่น anti-I บัง) ไม่ออก

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
- **ตัด ABO HDN ทิ้งเพราะ DAT ลบ** → DAT มักลบ/อ่อน; ใช้ IAT + spherocyte smear · ทารก DAT+ ที่ไม่ใช่ ABO/Rh = หา Ab หมู่อื่นจาก serum แม่
- **ลืม control ของ enhancement** → last-wash NSS (elution) / สัดส่วน LISS ผิด = อ่าน eluate/reaction ผิดทั้ง run
- **parentage จาก serology = exclude ได้เท่านั้น ไม่ confirm** — "ไม่ขัด" ≠ "เป็นพ่อ"; ยืนยันความเป็นพ่อต้อง molecular/STR
- **passive anti-A,B จาก O component อ่านเป็น auto/alloAb** → เช็ค Hx ได้ platelet/plasma หมู่ O ก่อน (DAT+/eluate anti-A,B)
- **TA-GVHD จากเลือดญาติ (one-way HLA match)** = เสี่ยงสุด คนภูมิปกติก็เป็น → **irradiate เสมอ**; leukoreduction ไม่กัน
- **PTP (เกล็ดต่ำ ~1 สัปดาห์, anti-HPA-1a)** สับกับ ITP/HIT/TA-GVHD → ธง: ก่อนเลือด plt ปกติ; รักษา IVIG (first line), หลีกเลี่ยง platelet transfusion เพิ่ม (ทำให้แย่ลง); ถ้าจำเป็นตอนเลือดออกรุนแรง ใช้ HPA-1a-negative platelet
- **เลือกสารพิเศษผิด → ลบ Ag ที่อยากตรวจ** — DTT ทำลาย Kell · chloroquine ทำลาย HLA-I/Rh · enzyme ทำลาย MNS/Duffy
- **PEG ห้ามปั่น / ห้ามใช้กับ IgM (ABO/Lewis) · Polybrene ใช้กับ Kell ไม่ได้ · LISS ห้ามใน titration**
- **ลืม autocontrol ในเทคนิคพิเศษ** (prewarmed/cold/low-pH/enhance) → แยก cold-auto vs allo ไม่ออก

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติม war-story หน้า bench จริง เช่น:
> - *"(MT BB) เคส ABO discrepancy ที่ผมเจอจริง คือ... resolve โดย..."*
> - *"เคสที่เกือบจ่ายเลือดผิด จับได้เพราะ clerical/anti-H ตรง..."*
> - *(สาย sales) เทคนิคหน้างาน → product: gel/CAT = Ortho/Bio-Rad · SPRCA = Immucor · HLA SSO = One Lambda/Thermo · NAT/molecular = Grifols/Roche*

---
*เครื่องมือช่วยคิดหน้างานธนาคารเลือดเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ใช่ผู้ตัดสินใจแทน งาน BB เกี่ยวชีวิตคนไข้โดยตรง ต้องทำตาม SOP, ยืนยันกับ MT/แพทย์, อ้างมาตรฐาน AABB/ศูนย์อ้างอิงเสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: chemistry-interpretation-judgment ═════════ -->

---
skill: chemistry-interpretation-judgment
title: โค้ชแปลผลเคมีคลินิก — เลือก marker + อ่าน pattern (Clinical Chemistry Interpretation Judgment)
type: ADVISE               # ช่วยแปลผล/เลือก marker ไม่ใช่ตำราค่า analyte
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดแปลผลเคมีคลินิกเพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รักษา — MT ตีความ/flag/ส่งต่อ การวินิจฉัยเป็นหน้าที่แพทย์ · ทุกผลต้อง correlate clinical + ทำตาม SOP/reference range ของห้องแล็บ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชแปลผลเคมีคลินิก — เลือก marker + อ่าน pattern

ค่าเคมีออกมาแล้ว "แปลว่าอะไร + เลือก marker/สูตรไหนเมื่อไหร่" แบบ organ-system ไม่ใช่ท่องค่า analyte (= commodity ดูตำรา)

> **กฎ #1 — อ่าน pattern + correlate clinical ก่อนเชื่อเลขเดี่ยว:** ค่าแปลกสวนอาการ = สงสัย interference/method (HIL/paraprotein/drug) ก่อน อย่าเพิ่งรายงาน · อ่าน LFT/bilirubin/cardiac/ABG เป็นชุด ไม่ใช่ทีละตัว
> **กับดัก #1 — เชื่อเลขปลอมแล้วรายงาน:** รายงาน **K⁺ critical จากตัวอย่าง hemolyzed** (สูงปลอม) · เชื่อ **troponin↑ = MI** (ไตวาย/sepsis ก็ขึ้น — ต้องดู delta + EKG) · **Cr ปกติ = ไตปกติ** ในคนแก่/cirrhosis
> นี่คือชั้น "ค่าออกมาแล้วแปลผล" — ส่วน QC/accept-reject run/Westgard ดู `clinchem-judgment` · ร้อยผลข้ามแขนง → ตั้ง DDx → ส่งต่อแพทย์ ดู `clinical-correlation-judgment`
> ⚠️ MT ตีความ/flag/ชี้ทาง — **การวินิจฉัยเป็นหน้าที่แพทย์**

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- อ่าน LFT/renal/cardiac/ABG/tumor marker แล้วต้องบอก pattern + ขั้นถัดไป
- เลือก marker/สูตร (eGFR ตัวไหน · marker หัวใจตามเวลา · tumor marker ใช้/ไม่ใช้)
- ค่าแปลกสวนอาการ → สงสัย interference (HIL/paraprotein/drug/method)
- (สาย sales) เข้าใจ "method matters" → คุย lab ลูกค้า (ดู `ivd-sales-judgment`)

## วิธีใช้
วาง skill นี้ + ค่าที่เจอ + clinical → AI ชี้ pattern + marker/สูตรที่เหมาะ + interference ที่ต้องตัดออกก่อนเชื่อค่า

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — Tumor marker: ใช้/ไม่ใช้เมื่อไหร่
- ⚠️ **ไม่ใช่ screening คนทั่วไป** (sens+spec ต่ำ → false +/− ท่วม) · gold standard diagnosis = **histology** · marker ส่วนใหญ่ใช้ **monitor/recurrence/prognosis** ไม่ใช่จับมะเร็งครั้งแรก
- benign ที่ดันค่าสูงปลอม (กับดัก): PSA↔prostatitis/BPH · AFP↔cirrhosis/ตั้งครรภ์ · CEA↔**สูบบุหรี่**/IBD · CA125↔**ประจำเดือน/ตั้งครรภ์/endometriosis** · β-hCG↔ตั้งครรภ์
- กฎสั่ง: **ห้ามเชื่อค่าเดียว** · **serial = assay/kit/ห้องเดิม** (assay ต่าง → ค่าต่าง) · ดู **half-life** (hCG เร็วสุด · PSA หลัง radiotherapy ช้าหลายเดือน) — ลดช้ากว่าคาด = residual/ดื้อยา · screen เฉพาะ high-risk (HBV/cirrhosis → AFP+US)

### Fork 2 — Renal: เลือก marker + สูตร
- **BUN↑เดี่ยว** (Cr ปกติ) → prerenal/dehydration/**GI bleed**/high-protein/steroid · **BUN+Cr↑** → GFR ลดจริง · BUN:Cr >20 = prerenal/GI bleed
- **CrCl (24h urine)** กับดัก: เก็บไม่ครบ (urine Cr ควร ~ชาย 18.5–25 · หญิง 15–20 mg/kg/day; ต่ำกว่า ~15 มาก = under-collect) · GFR ต่ำมาก → tubule หลั่ง Cr → **CrCl overestimate**
- **eGFR (serum Cr):** **CKD-EPI 2021 (race-free) = default ทุกช่วง GFR** · MDRD = legacy · Cockcroft-Gault (ปรับยา) · gold จริง = inulin (ไม่ routine)
- ⚠️ **Cr ปกติ ≠ ไตปกติ:** glomerulus เสีย <25% Cr ยังปกติ · **คนแก่** muscle↓ ชน GFR↓ หักล้าง · **cirrhosis** สร้าง creatine น้อย → Cr ต่ำปลอม eGFR สูงเกินจริง → ใช้ **cystatin C** (ไม่ขึ้น muscle)
- **Jaffe vs enzymatic:** Jaffe ถูกแต่ interference เยอะ — positive chromogen (glucose/protein/vit C/ASA/ceph/ketone) **↑Cr ปลอม → UNDERestimate GFR** (เกินจริงว่าไตเสีย); bilirubin **↓Cr → overestimate GFR** → ใช้ **enzymatic creatinine** คำนวณ GFR

### Fork 3 — LFT: อ่าน pattern อย่าอ่านทีละตัว
- จัดกลุ่ม: **hepatocellular** (AST/ALT) · **cholestatic** (ALP/GGT/5'-NT) · **synthetic** (albumin/PT) · **excretion** (bilirubin)
- **AST:ALT ratio:** ตับเจ็บทั่วไป ALT>AST · **≥2:1 = alcoholic** (GGT/ALP หนุน; **AST>500 ในคนดื่ม = ผิดปกติ หาเหตุอื่น** alcoholic มัก <300)
- **DB/TB ratio** (ตัวตัดสิน bilirubin; % = สัดส่วน direct/conjugated): <20% (ส่วนใหญ่ unconjugated) → **hemolysis/Gilbert** (prehepatic) · >70% conjugated → **cholestasis/obstruction** · 30-60% mixed → hepatitis/cirrhosis
- **ALP สูง → ตับหรือกระดูก?** confirm ด้วย GGT/5'-NT (สูงคู่=ตับ; ปกติ=กระดูก)
- **PT prolong → ตับหรือ vit K?** ฉีด vit K ดีขึ้น = **cholestasis** (ดูดซึมไม่ได้); ไม่ดีขึ้น = **hepatocellular** (สร้าง factor ไม่ได้)
- ⚠️ **ischemic hepatitis "shock liver":** AST/ALT พุ่ง >2000 แต่ลงเร็วใน 1 สัปดาห์ (low-flow: HF/shock/sepsis) — เลขน่ากลัวแต่ self-limited อย่าตื่น

### Fork 4 — Cardiac marker: timing คือทุกอย่าง
| marker | ขึ้นหลังเจ็บอก | คงอยู่ | บทบาท/กับดัก |
|---|---|---|---|
| **Myoglobin** | 1-3 h (เร็วสุด) | สั้น | early, spec ต่ำ; **ห้ามใช้ในไตวาย** (สูงปลอม) |
| **CK-MB mass** | 3-6 h | 2-3 วัน | ดู **re-infarction** ดี; index (MB×100/CK) <~2.5% skeletal · >5% cardiac · 2.5–5% ก้ำกึ่ง (lab-dependent; รอง troponin) |
| **cTnI/cTnT** | 3-7 h | 7-14 วัน | **definitive** (sens+spec สูงสุด) + risk stratify |
- ⚠️ **troponin↑ ≠ MI เสมอ** (ไตวาย/sepsis/PE/HF/exercise) → ดู **rise/fall (delta 0h/1h) + clinical + EKG** · **BNP/NT-proBNP = heart failure** ไม่ใช่ MI

### Fork 5 — Acid-base/ABG: 5 ขั้น + anion gap
1. pH → acidosis/alkalosis · 2. PCO2 (↑=resp acid) · 3. HCO3⁻ (↓=metabolic acid) · 4. ตัวที่ไปทางเดียวกับ pH = สาเหตุ (CO2→resp / HCO3→metabolic) · 5. compensation (un/partial/full)
- **Metabolic acidosis → AG = (Na+K)−(Cl+HCO3):** **high AG** = DKA/lactic/renal/toxin (methanol/glycol/salicylate) · **normal AG (hyperchloremic)** = diarrhea/RTA/CA-inhibitor
- **Metabolic alkalosis:** urine Cl<10 = **saline-responsive** (vomit/NG/diuretic) · >20 = **saline-resistant** (mineralocorticoid excess)
- ⚠️ **calculated SO2 จาก ABG ผิด** ถ้ามี COHb/MetHb → ต้อง **co-oximeter** (วัดจริง) ไม่ใช่คำนวณจาก PO2
- ⚠️ **ABG pre-analytical (เช็คก่อนเชื่อค่า):** ฟองอากาศ/สัมผัสอากาศ → **pO₂↑ pCO₂↓ pH↑** · ทิ้งนานไม่แช่เย็น (เซลล์ยังใช้ O₂) → **pO₂↓ pCO₂↑ pH↓** · ต้องกันด้วย **heparin (balanced/dried) ไม่ใช่ NaF** · ไม่รีบวัด = แช่น้ำแข็ง

### Fork 6 — Interference (HIL/paraprotein/drug): ตัดออกก่อนเชื่อค่า
- **Hemolysis:** K⁺↑ (intracellular ~40×), LDH/AST/phosphate↑ → **อย่ารายงาน K critical จากตัวอย่าง hemolyzed**
- **Lipemia:** **pseudo-hyponatremia** (indirect ISE), รบกวน 340nm → fast 12h / clear ก่อนวัด
- **Icterus:** bilirubin รบกวน assay ที่ใช้ H₂O₂
- **Paraprotein:** ⚠️ **ตาไม่เห็น (gross ปกติ)** แต่รบกวน → สงสัยเมื่อค่าแปลกในผู้ป่วย myeloma
- **Drug method-dependent:** Jaffe Cr ↑ (ceph/ASA/vit C) · ดู `clinchem-judgment` สำหรับ HIL index/QC angle
> หลัก "method matters" — ค่าแปลกสวน clinical → สงสัย interference ก่อนเชื่อ/ก่อนรายงาน

### Fork 7 — Protein electrophoresis (SPEP) + lipid: อ่าน pattern
- **SPEP region (จาก anode):** prealbumin (malnutrition ไว) · albumin (↓ inflammation/liver/nephrotic/malnutrition) · **α1** (α1-antitrypsin — ขาด→emphysema; AFP) · **α2** (**haptoglobin ↓ = hemolysis**; α2-macroglobulin↑ nephrotic; ceruloplasmin↓ Wilson) · **β** (**transferrin** — แยก anemia DDx; C3/C4) · **γ** (immunoglobulin)
- **pattern ที่ต้องอ่าน:** **polyclonal gammopathy** (γ กว้าง = infection/chronic inflammation) vs **monoclonal (M-spike/paraprotein = แหลมเดียว)** → **สงสัย multiple myeloma** → confirm **immunofixation (IFE)** + free light chain (ดู `immunoassay-judgment`) · TP↑ dehydration/myeloma · TP↓ liver/nephrotic
- 🩸 **haptoglobin ↓ = hemolysis marker** (โยง transfusion reaction/hemolytic anemia); transferrin/iron = anemia DDx
- **Friedewald LDL = TC − HDL − TG/5** ⚠️ **TG > 400 = ห้ามใช้เด็ดขาด** → direct LDL · แต่ >400 เป็น **เพดานล่าง ไม่ใช่ใบรับรองว่าต่ำกว่านี้แม่น** — underestimate เริ่มตั้งแต่ TG ~150 (+ ใช้ไม่ได้กับ non-fasting/type III) → LDL ต่ำๆ ที่ TG ปานกลางก็พลาดได้

---

## กับดัก (Anti-patterns)
- **ใช้ tumor marker screen คนทั่วไป** / เชื่อค่าเดียว / serial คนละ assay
- **troponin↑ = MI เสมอ** — ดู delta + clinical (ไตวาย/sepsis/PE ก็ขึ้น)
- **Cr ปกติ = ไตปกติ** ในคนแก่/cirrhosis — ใช้ eGFR/cystatin C
- **รายงาน K สูงจากตัวอย่าง hemolyzed** (สูงปลอม → critical ปลอม)
- **ตื่นกับ ischemic hepatitis** AST/ALT >2000 ที่ self-limited
- **ตัด DKA เพราะ urine ketone ลบ** (early DKA β-OHB เด่น; dipstick จับ acetoacetate)
- **เชื่อ calculated SO2** เมื่อมี CO/MetHb — ต้อง co-oximeter
- **อ่าน LFT/bilirubin ทีละตัว** แทน pattern (DB/TB + AST:ALT + GGT)
- **มองข้าม M-spike (monoclonal)** บน SPEP — แหลมเดียว = สงสัย myeloma → IFE confirm; haptoglobin↓ = hemolysis อย่ามองข้าม
- **ใช้ Friedewald LDL เมื่อ TG > 400** — ผิด ต้อง direct LDL (และอย่าวางใจค่าต่ำกว่า 400 เต็มร้อย — underestimate ตั้งแต่ ~150)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT chem) เคสที่ค่าแปลกเพราะ interference ... จับได้เพราะ..."*
> - *"reference range / method ของแล็บผม (Jaffe vs enzymatic, hs-troponin cutoff) คือ..."*
> - *"pattern LFT/ABG ที่ผมเคยอ่านพลาด คือ..."*

---
*ช่วยคิดแปลผลเคมีคลินิกเพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รักษา — MT ตีความ/flag/ส่งต่อ การวินิจฉัยเป็นหน้าที่แพทย์ · ทุกผลต้อง correlate clinical + ทำตาม SOP/reference range ของห้องแล็บ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: choose-stat-test ═════════ -->

---
skill: choose-stat-test
title: เลือกสถิติทดสอบให้ถูก (Choose the Right Stat Test)
type: ADVISE               # ช่วยตัดสินใจเลือก test ไม่ได้รันเลขให้
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยชี้ว่าควรใช้ test ไหนเพื่อช่วยคิด — เป็นการชี้ทางเพื่อการศึกษา ไม่ใช่ที่ปรึกษาสถิติ ควรตรวจเงื่อนไข/assumption จริงและปรึกษานักสถิติเมื่อเป็นงานตีพิมพ์ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# เลือกสถิติทดสอบให้ถูก

มีข้อมูล + คำถามวิจัย แต่ไม่รู้ใช้ test ไหน → ตอบ 3 คำถาม แล้วได้ test ที่ใช่ **พร้อมเหตุผลและเงื่อนไขที่ต้องเช็ค**

> **กฎเหล็ก #1: ถามก่อนเสมอว่า "ข้อมูลจับคู่ (paired) หรืออิสระ?"** — ถ้าวัดซ้ำหน่วยเดิม (ก่อน-หลัง, คนเดียวกัน 2 วิธี, ตัวอย่างเดียวกัน) = **paired/correlated** ต้องจับคู่ (paired t / Wilcoxon / McNemar) **ห้าม**ใช้ test แบบ 2 กลุ่มอิสระ.
> **กับดักที่ reviewer ตีกลับบ่อยสุด** ไม่ใช่ "คำนวณผิด" แต่คือ **"เลือก test ผิดตั้งแต่ต้น"** — เอา test อิสระไปจับข้อมูลจับคู่, เอา correlation ไปวัด agreement, ลืมเช็ค expected count.
> 🔑 **Discriminator ตัวพราง:** "คนละคน/คนละกลุ่ม" ≠ อิสระเสมอ — ถ้า **match กันเป็นคู่** (เคส-คอนโทรลจับคู่อายุ-เพศ, ฝาแฝด, ก่อน-หลังในหน่วยเดียว) ก็ยังเป็น paired. ตัดสินที่ **"มีการจับคู่ระหว่างหน่วยสังเกตไหม"** ไม่ใช่ "คนเดียวกันหรือเปล่า"

## ใช้เมื่อ
- มีข้อมูล R2R/วิจัยแล้ว แต่ไม่แน่ใจว่าใช้สถิติตัวไหน
- reviewer/อาจารย์ถามว่า "ทำไมใช้ test นี้" แล้วตอบไม่ได้
- จะออกแบบงานวิจัย อยากรู้ล่วงหน้าว่าจะวิเคราะห์ด้วยอะไร (จะได้เก็บข้อมูลให้ถูก)

## วิธีใช้
วาง skill นี้ + เล่า *"คำถามวิจัยคือ... ข้อมูลที่มีคือ... อยากเปรียบเทียบ/หาความสัมพันธ์ของ..."* → AI จะถาม 3 อย่างแล้วชี้ test + เงื่อนไข

---

## วิธีเลือก (AI: ทำตามนี้)

### ขั้น 1 — ถาม 3 คำถามก่อนเสมอ (อย่าเดา)
1. **เป้าหมายคืออะไร?** เปรียบเทียบกลุ่ม / หาความสัมพันธ์-ทำนาย / วัดความสอดคล้อง (agreement)
2. **outcome เป็นชนิดไหน?** ตัวเลข (numeric) / หมวด (categorical) / อันดับ (ordinal เช่น Likert, เกรด, +/++/+++)
3. **กี่กลุ่ม + จับคู่ไหม?** 1 / 2 / ≥3 กลุ่ม · **จับคู่/correlated** (วัดซ้ำหน่วยเดิม, ก่อน-หลัง, match เป็นคู่, สัดส่วน 2 ค่าจาก sample เดียว) หรือ **อิสระ** (คนละหน่วย ไม่มีการจับคู่)

> ⚠️ คำถาม 3 คือตัวชี้ขาด — **ถ้ายังไม่รู้ว่า paired หรืออิสระ ห้ามชี้ test.** ถ้าผู้ใช้ตอบไม่ครบ → ถามให้ครบก่อน อย่าเดาแทน

### ขั้น 2 — ใช้ decision tree

```mermaid
flowchart TD
  A["ถาม 3: เป้าหมาย? · outcome ชนิดไหน? · กี่กลุ่ม จับคู่ไหม?"] --> B{เป้าหมาย}
  B -->|เปรียบเทียบค่าเฉลี่ย| C{กี่กลุ่ม จับคู่ไหม}
  C -->|1 กลุ่ม vs ค่าอ้าง| C1["one-sample t-test"]
  C -->|2 กลุ่ม จับคู่| C2["paired t-test"]
  C -->|2 กลุ่ม อิสระ| C3["two-sample Welch"]
  C -->|3 กลุ่มขึ้นไป| C4["ANOVA + post-hoc"]
  C -->|skew หรือ n เล็ก หรือ ordinal| C5["non-parametric (Mann-Whitney/Wilcoxon/Kruskal)"]
  B -->|สัดส่วน นับ| D{ลักษณะ}
  D -->|1-2 สัดส่วน| D1["z-test proportion (SE ใช้ p0)"]
  D -->|ตาราง RxC| D2["Chi-square (expected 5+)"]
  D -->|2x2 cell เล็ก| D3["Fisher exact"]
  B -->|ความสัมพันธ์ ทำนาย| E{outcome}
  E -->|2 ตัวเลข เชิงเส้น| E1["Pearson / linear regression"]
  E -->|binary| E2["logistic regression (OR=e^b)"]
  B -->|ความสอดคล้อง เทียบวิธีวัด| F{ชนิด}
  F -->|ตัวเลข| F1["Bland-Altman + ICC (ไม่ใช่ correlation)"]
  F -->|หมวด| F2["Cohen kappa (ordinal→weighted)"]
```

**A. เปรียบเทียบค่าเฉลี่ย (outcome = ตัวเลข)**
- 1 กลุ่ม เทียบค่าอ้างอิง → **one-sample t-test**
- 2 กลุ่ม **จับคู่** (ก่อน-หลัง, วัดซ้ำหน่วยเดียว) → **paired t-test** (ทำผลต่างก่อน)
- 2 กลุ่ม **อิสระ** → **two-sample t-test** — ใช้ **Welch เป็น default** (ไม่ต้องสมมติ variance เท่า ปลอดภัยกว่า)
- ≥3 กลุ่ม → **One-way ANOVA** + post-hoc (เช่น Tukey/LSD) ถ้า significant
- 2 ปัจจัย → **Two-way ANOVA** — ⚠️ **ดู interaction ก่อน**: ถ้า A×B significant ตีความ main effect เดี่ยวๆ ไม่ได้

**B. ถ้าไม่ normal / n เล็ก / ordinal → non-parametric** (digest ไม่เน้น แต่ข้อมูล lab เจอบ่อย)
- paired → **Wilcoxon signed-rank** · 2 กลุ่มอิสระ → **Mann-Whitney U** · ≥3 กลุ่ม → **Kruskal-Wallis**
- ความสัมพันธ์ที่ไม่เชิงเส้น/ordinal → **Spearman correlation** (แทน Pearson)

**C. สัดส่วน / ข้อมูลนับ (outcome = หมวด)**
- 1 หรือ 2 สัดส่วน **อิสระ** → **z-test for proportion** (⚠️ SE ใช้ **p₀** ของ null ไม่ใช่ p̂)
- 2 สัดส่วน **จับคู่** (วิธี/test 2 ตัวบนคนเดียวกัน, ก่อน-หลัง แบบ yes/no) → **McNemar's test** (z-test 2 สัดส่วนใช้ไม่ได้ — correlated)
- ตาราง R×C หาความสัมพันธ์ → **Chi-square independence** (⚠️ เกณฑ์ expected count: **2×2 ต้องทุก cell ≥5**; **R×C ใหญ่** ผ่อนได้ — ห้ามมี cell ใด <1 และ ≤20% ของ cell <5 ตามกฎ Cochran ไม่ใช่ "ทุก cell ≥5" แบบเหมารวม)
- 2×2 + cell เล็ก (expected <5) → **Fisher's exact test**

**D. ความสัมพันธ์ / ทำนาย**
- 2 ตัวแปรตัวเลข เชิงเส้น → **Pearson correlation / simple linear regression**
- outcome ตัวเลข + หลาย predictor → **multiple regression** (⚠️ เช็ค multicollinearity, VIF>5–10 = ปัญหา)
- outcome **แบบ 2 ค่า** (เป็น/ไม่เป็นโรค) → **logistic regression** (รายงานเป็น **OR = e^β**)

**E. ความสอดคล้อง / เทียบวิธีวัด (MT เจอบ่อยสุด)**
- 2 วิธีวัดค่าตัวเลข เครื่องเก่า/ใหม่ → **Bland-Altman + ICC** ❗**ไม่ใช่ correlation** (r สูงแต่ bias ได้)
- 2 ผู้อ่านตัดสินหมวด (เช่น อ่านสไลด์) → **Cohen's kappa** (ordinal → **weighted kappa**)

### ขั้น 3 — บอกเงื่อนไขที่ต้องเช็ค ไม่ใช่แค่ชื่อ test
ทุกครั้งที่ชี้ test ให้แนบ assumption ที่ต้องตรวจ เช่น t-test → independence + normality (ของ residual/ค่าเฉลี่ย ไม่ใช่ data ดิบ); n เล็ก+skew → ย้าย non-parametric

### ขั้น 4 — เตือนกับดักที่เข้ากับเคสนั้น
ดึงข้อที่เกี่ยวจาก "กับดัก" ด้านล่างมาเตือน (เช่น ถ้าเป็น 2 % จาก sample เดียวกัน → เตือนว่า correlated)

---

## กับดัก (Anti-patterns)
- **จับคู่แต่ใช้ two-sample** — ข้อมูลก่อน-หลังคนเดียวกันต้องทำผลต่าง (paired) ไม่งั้นเสีย power
- **เอา correlation ไปสรุป agreement** — method comparison ต้อง ICC/Bland-Altman; r สูงไม่ได้แปลว่าตรงกัน
- **2 สัดส่วนจาก sample เดียวกัน** (เช่น %เห็นด้วย A vs B ในคนกลุ่มเดียว) = correlated → ใช้ **McNemar** ไม่ใช่ two-sample proportion
- **proportion test ใช้ p̂ ใน SE** — ที่ถูกคือใช้ **p₀** (ค่าจาก null hypothesis)
- **ปัด expected count** → 2×2 ทุก cell ต้อง ≥5 ไม่งั้นใช้ Fisher's exact; แต่ **R×C ใหญ่ห้ามเหมา** ว่าต้อง ≥5 ทุก cell — ผ่านได้ถ้า ≤20% ของ cell <5 และไม่มี cell <1
- **ทำ t-test ทุกคู่เมื่อมีหลายกลุ่ม** → Type I error สะสม ใช้ ANOVA + post-hoc แทน
- **ลืมเช็ค normality / ยัด t-test กับ ordinal** → n เล็ก/skew/Likert ใช้ non-parametric
- **พูดว่า "accept H₀"** → ที่ถูกคือ "fail to reject H₀"
- **two-way ANOVA แล้วตีความ main effect ทั้งที่ interaction significant**

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติม test ที่สายงานคุณใช้บ่อย + เคสที่เลือกผิดแล้วโดนตีกลับ เช่น:
> - *"งาน lab แบบ... ผมเลือก... เพราะข้อมูลมัน skew/ordinal"*
> - *"reviewer วารสาร... ชอบถามเรื่อง... ต้องเตรียม..."*
> - *"test ที่ตำราบอกใช้ได้ แต่ข้อมูลจริง n เล็ก ผมเลี่ยงไป..."*

---
*ช่วยชี้ว่าควรใช้ test ไหนเพื่อช่วยคิด — เป็นการชี้ทางเพื่อการศึกษา ไม่ใช่ที่ปรึกษาสถิติ ควรตรวจ assumption จริงและปรึกษานักสถิติเมื่อเป็นงานตีพิมพ์ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: clinchem-judgment ═════════ -->

---
skill: clinchem-judgment
title: ตัวช่วยตัดสินใจแล็บเคมีคลินิก (Clinical Chemistry Judgment)
type: ADVISE
needs: any
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "skill นี้เป็นตัวช่วย 'คิด' สำหรับการตัดสินใจในแล็บเคมีคลินิกเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ใช่ผู้ตัดสินแทน. ปล่อยผลผิด 1 ค่า = หมอรักษาผิด 1 คน — นี่คือความปลอดภัยผู้ป่วยโดยตรง. AI ช่วยไล่ logic/Westgard/interference เท่านั้น ทุกการตัดสิน accept/reject/report ต้องเป็นไปตาม SOP + QC policy ของแล็บ และยืนยันกับ MT/ผู้มีอำนาจลงนามก่อนเสมอ. ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ตัวช่วยตัดสินใจแล็บเคมีคลินิก

ตัวช่วยตัดสินใจในแล็บเคมีคลินิก — เน้น "จะ accept/reject run นี้มั้ย", "ค่านี้ปล่อยได้มั้ย", "interference ตัวนี้ทำผลเพี้ยนตัวไหน" ไม่ใช่ที่ท่อง reference range / นิยาม analyte

> **VERDICT: เมื่อสงสัย → HOLD ก่อน report เสมอ.** เช็คตามลำดับ gate: **sample (HIL/clot/tube) → QC (Westgard) → report.** gate ใดไม่ผ่าน = ไม่ปล่อยผล.
> **กับดักอันดับ 1:** report ผลจาก run ที่ Westgard FAIL หรือจาก sample hemolyzed — ปล่อยผิด 1 ค่า = หมอรักษาผิด 1 คน.

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- ดู QC แล้วต้องตัดสิน accept หรือ reject run · Westgard ตัวไหน fire · L-J chart shift/trend แปลว่าอะไร
- เจอ sample hemolyzed/lipemic/icteric/clotted → ปล่อยผลได้มั้ย ตัวไหนเชื่อไม่ได้
- ได้ค่า critical / outlier / เกิน linearity → dilute / repeat / โทร หรือ report
- เลือกทาง recalibrate vs troubleshoot vs เปลี่ยน lot น้ำยา เมื่อ QC พัง
- (สาย sales/IVD) คุยภาษา sigma/TEa/QC กับ lab head ให้ตรงประเด็น

## วิธีใช้
วาง skill นี้ + ข้อมูล QC/sample/ค่าที่ได้ (control values, L-J pattern, สภาพตัวอย่าง, ค่าที่สงสัย) → AI ไล่ fork ตามลำดับ gate (sample → QC → report) แล้วบอกว่าควร accept/reject/repeat/dilute/โทร พร้อมเหตุผลและกับดักที่ต้องระวัง

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### FORK 1 — accept หรือ reject run? Westgard ตัวไหน fire
**Verdict: 1₂ₛ = warning อย่าเพิ่ง reject; เจอ 1₃ₛ/2₂ₛ/R₄ₛ/4₁ₛ/10ₓ = REJECT.** (modern multirule บางที่ตัด 1₂ₛ ทิ้ง เริ่มที่ 1₃ₛ เลย) ถ้าเกิน ±2SD ให้ไล่กฎ reject ต่อ:

| เห็นอะไร | กฎ | error | ตัดสิน |
|---|---|---|---|
| 1 ค่าเกิน ±2SD (ไม่เข้ากฎอื่น) | 1₂ₛ | — | warning เท่านั้น → ปล่อยได้ (อย่า reject ทันที = false reject ~5%) |
| 1 ค่าเกิน ±3SD | 1₃ₛ | random | REJECT |
| 2 ค่าติดกันเกิน +2SD (หรือ −2SD) ด้านเดียว | 2₂ₛ | systematic | REJECT |
| ค่าหนึ่ง >+2SD อีกค่า <−2SD ใน run เดียว (ห่าง >4SD) | R₄ₛ | random | REJECT |
| 4 ค่าติดกันเกิน ±1SD ด้านเดียว | 4₁ₛ | systematic | REJECT (stable system อาจตั้งเป็น warning) |
| 10 ค่าติดกันอยู่ด้านเดียวของ mean | 10ₓ | systematic | REJECT (stable system อาจเป็น warning) |

- กฎ random (1₃ₛ/R₄ₛ) → นึกถึง: ฟองอากาศ, mix ไม่ทั่ว, อุณหภูมิ/ไฟไม่นิ่ง, pipette/timing ผิด → มักแก้ด้วย repeat control
- กฎ systematic (2₂ₛ/4₁ₛ/10ₓ) → นึกถึง: น้ำยาเสื่อม/หมดอายุ, calibration drift, light source/probe เสื่อม → repeat เฉยๆ ไม่หาย → ต้อง troubleshoot/recalibrate
- sigma สูง → ใช้กฎน้อยลง: 6σ = 1₃ₛ เดี่ยว (N=2) · 5σ = 1₃ₛ/2₂ₛ/R₄ₛ · 4σ ค่อยเพิ่ม 4₁ₛ · ≤3σ ต้องเพิ่ม 8ₓ/control เยอะ

### FORK 2 — L-J shift vs trend → คนละสาเหตุ คนละการแก้
**Verdict: Shift = สงสัย lot/calibration; Trend = สงสัยน้ำยา/ชิ้นส่วนเสื่อม. IQC ผ่านสวยทุกวันก็ยัง bias ได้ — ต้องพึ่ง EQA.**
- Shift (จุดกระโดดไปอยู่ด้านเดียว mean ทันที) → เปลี่ยน lot น้ำยา/calibrator, หลัง maintenance/recalibrate → verify lot/calibration ก่อนโทษเครื่อง
- Trend (ค่อยๆ ไหลขึ้น/ลง) → น้ำยาเสื่อม, light source เสื่อม, electrode/probe ค่อยๆ ตัน → คาดการณ์ล่วงหน้าได้ อย่ารอจน reject
- IQC ผ่านสวยทุกวัน แต่ EQA fail = precise but inaccurate (bias ซ่อน) = บทเรียน Theranos. "IQC OK ≠ ผลถูก" — bias คงที่ L-J จับไม่ได้ ต้องพึ่ง EQA/method comparison

### FORK 3 — interference (HIL) กระทบ analyte ไหน → ปล่อยได้/ไม่ได้
**Verdict: hemolyzed → ห้าม report K⁺/LDH/AST (สูงปลอม) เจาะใหม่. เช็ค HIL index ก่อนโทษเครื่อง.** interference ไม่ได้เพี้ยนทุกตัวเท่ากัน — รู้ "ตัวไหน + ทิศไหน" ก่อนตัดสินปล่อย

| ปัญหา sample | ทำเพี้ยนตัวไหน (ทิศ) | ตัดสิน |
|---|---|---|
| Hemolysis (Hb แดง รั่วจาก RBC) | K⁺ สูงปลอม, LDH/AST สูงปลอม + รบกวน absorbance | K⁺/LDH/AST จาก hemolyzed = ห้าม report → เจาะใหม่ |
| Lipemia (TG สูง ขุ่น) | รบกวน spectrophotometry → หลาย analyte เพี้ยน | repeat หลัง centrifuge/blank หรือ direct assay; flag |
| Icterus (bilirubin) | Creatinine (Jaffe) ต่ำปลอม (เริ่มได้ตั้งแต่ ~2 mg/dL, แรงขึ้นเมื่อสูง) | สลับ enzymatic Cr / blank; flag (enzymatic ก็ไม่ immune 100%) |
| Glycolysis (แยก RBC ช้า) | glucose ต่ำปลอม | เจาะ NaF tube / แยก serum เร็ว |
| Ascorbic acid | Cr (Jaffe) −bias, glucose interference | ทราบ med history; blank |

- ก่อนสรุปว่า "เครื่องเพี้ยน" → เช็ค sample integrity ก่อนเสมอ (HIL index): ถ้า HIL จริง = ปัญหา pre-analytical ไม่ใช่เครื่อง อย่าไป recalibrate

### FORK 4 — QC พัง: recalibrate vs troubleshoot vs เปลี่ยน reagent
**Verdict: อย่า recalibrate เป็นรีเฟล็กซ์ — เช็ค control/sample/reagent expiry ก่อน. random→repeat control; systematic/shift→recalibrate; trend ไม่อยู่→เปลี่ยน lot; หมดทาง→service.**
1. เช็คก่อน: control หมดอายุ/reconstitute ผิด? (ALP เปลี่ยน activity เร็วหลังละลาย) · vial ผิด · pipette
2. random error (1₃ₛ/R₄ₛ): repeat control 1 รอบ → หาย = ปล่อย; ไม่หาย → หาฟองอากาศ/mix/อุณหภูมิ
3. systematic / shift หลังเปลี่ยน lot: → recalibrate
4. trend ไหลลง + recalibrate ไม่อยู่: → เปลี่ยน lot reagent
5. เปลี่ยนหมดแล้วยังพัง → troubleshoot hardware → แจ้ง service
- เกณฑ์ method (sigma): <3σ = ต้อง correct/เปลี่ยน method · <2σ = เปลี่ยน technology/analyzer

### FORK 5 — ได้ค่าแล้ว: dilute / repeat / report / โทร
**Verdict: critical value → verify→repeat→โทร→บันทึก read-back เสมอ. เกิน linearity → dilute. run Westgard fail → ห้าม report.**
- เกิน linearity → dilute แล้ววัดใหม่ × dilution factor
- outlier เดี่ยว / ไม่เข้ากับ clinical → repeat ก่อน ห้าม trust ค่าแรกทันที
- critical value → (1) verify sample integrity (2) repeat (3) โทรแจ้ง ward + บันทึก ใคร/เวลา/อ่านทวน
- ผล run ที่ Westgard fail → ห้าม report ผู้ป่วยใน run นั้น จนกว่าจะแก้ QC + รัน control ผ่าน แล้ว re-run

### FORK 6 — เชื่อค่าแรกหรือ repeat?
**Verdict: สงสัย = repeat ก่อนปล่อย. ได้ค่าเดิม = เชื่อ; ต่าง = หา pre-analytical/carryover.**
Repeat ก่อนปล่อย เมื่อ: ค่า critical, ค่าขัด clinical/ผล panel อื่น (Cr สูงแต่ BUN ปกติ), delta check ต่างมาก, run QC borderline, มี HIL flag. Repeat ได้ค่าเดิม = เชื่อ; ต่าง = หา pre-analytical/carryover

## กับดัก (Anti-patterns)
- 🚫 report ผลจาก run ที่ Westgard FAIL — run reject = ผู้ป่วยทุกคนใน run นั้น hold; แก้ QC ก่อน
- 🚫 report K⁺ (หรือ LDH/AST) จากตัวอย่าง hemolyzed — สูงปลอม → เจาะใหม่ อย่า report
- 🚫 ไม่ flag / ไม่โทร critical value — ต้อง verify→repeat→โทร→บันทึก read-back
- 🚫 ตี 1₂ₛ เป็น reject — 1₂ₛ = warning เท่านั้น (โอกาส ~5% ออกนอก ±2SD ตามธรรมชาติ; modern multirule บางที่ตัด 1₂ₛ ทิ้ง เริ่มที่ 1₃ₛ)
- 🚫 calibration drift / trend จับไม่ทัน — trend = แก้เชิงรุก. IQC ผ่าน ≠ accurate (Theranos)
- 🚫 ละเลย sample integrity — clotted / wrong tube (fluoride กับ urease-BUN ใช้ไม่ได้) / underfill / hemolyzed → อย่าโทษเครื่องแล้ว recalibrate มั่ว
- 🚫 trust outlier ไม่ repeat
- 🚫 report ค่าที่เกิน linearity โดยไม่ dilute
- 🚫 recalibrate ทันทีทุกครั้งที่ QC พัง — เช็ค control/sample/reagent expiry ก่อน
- 🚫 ลืม carryover — ตัวอย่างเข้มข้นสูงตามด้วยต่ำ → ค่าต่ำสูงปลอม; repeat

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคส QC จริงที่เจอ: Westgard ตัวไหน fire บ่อยกับ analyte ไหนในแล็บคุณ และ root cause จริงที่เจอคืออะไร
> เติม interference/wrong-tube ที่เคยพลาด: เคยปล่อยผลจาก sample ปนเปื้อนแล้วหมอ flag กลับมามั้ย แก้ระบบยังไง
> เติมเกณฑ์ critical value + read-back ของแล็บคุณ: ค่าไหนต้องโทรทันที ขั้นตอนบันทึกเป็นแบบไหน

NOTE: ความรู้พื้นฐาน (reference range, assay principles เช่น GOD-POD/Jaffe/Friedewald, TEa, sigma-DPMO) ให้ดูจาก "ตำรา/แหล่งอ้างอิงมาตรฐาน" — skill นี้เน้นการ "ตัดสินใจ" เท่านั้น

---
*skill นี้เป็นตัวช่วยคิดเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ตัดสินแทน. การตัดสิน accept/reject/report ทุกครั้งต้องเป็นไปตาม SOP + QC policy ของแล็บ และยืนยันกับ MT/ผู้มีอำนาจลงนามก่อน. ปล่อยผลผิด = รักษาผิด — ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: clinical-correlation-judgment ═════════ -->

---
skill: clinical-correlation-judgment
title: โค้ชอ่านผลแล็บข้ามแขนง — correlate + ตั้ง DDx ชี้ทางให้แพทย์ (Clinical Correlation Judgment)
type: ADVISE
needs: any
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "เครื่องมือช่วยคิดเชิงวินิจฉัยจากผลแล็บข้ามแขนงเพื่อการศึกษา — ช่วยคิด ไม่ใช่คำสั่งทางการแพทย์และไม่ตัดสินใจแทน การตีความผลแล็บกระทบการวินิจฉัยและรักษาผู้ป่วยโดยตรง ต้องยืนยันกับ MT/แพทย์ผู้ดูแล + ทำตาม SOP และตำรา/แหล่งอ้างอิงมาตรฐานเสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชอ่านผลแล็บข้ามแขนง — correlate + ตั้ง DDx ชี้ทางให้แพทย์

ตัวช่วยอ่านผลแล็บข้ามแขนง (hema + chem + micro + immuno + blood-bank) แล้วร้อยเรื่องเป็นภาพเดียว → **ตั้ง DDx + ชี้ทาง + flag ให้แพทย์** — เน้น **วิธีคิดเชื่อมโยงผล + กับดักที่ทำให้พลาด** ไม่ใช่ท่องค่า

> 🎯 **กฎ #1: ก่อนเชื่อค่าใดๆ เช็ค clinical context + pre-analytical ก่อน** (อายุ/อาการ/ยา + hemolysis/clot/tube ผิด) — "ตัวเลขลอยไม่มีคนไข้ = อ่านผิด" แล้วร้อยค่าผิด *ทุกตัว* ให้อธิบายได้ด้วย **กลไกเดียว**
> 🚩 **กับดัก #1: anchoring** — อย่า lock ธงแรก. บังคับตั้ง DDx ≥3 + สั่ง test ที่ *หักล้าง* DDx อื่น (ไม่ใช่แค่ยืนยันของตัวเอง). ค่าเดี่ยว positive ≠ diagnosis → confirm เสมอ
> ⚠️ **ขอบเขต: MT ไม่วินิจฉัย** — MT correlate/flag + ชี้ทาง reflex test + ส่งต่อ; **วินิจฉัยเป็นหน้าที่แพทย์**

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- มีผลแล็บหลายตัว/หลายแขนงในผู้ป่วยคนเดียว → "ค่าไหนชี้ทางไหน → DDx → ตัดออกจนเหลือคำตอบ"
- ฝึก case study / ตอบสอบ integrate / งานวิจัย · ถาม "ค่านี้ใช่โรคจริงหรือ artifact?"
- เตือนตัวเองก่อนสรุป/ชี้ทาง (ส่งต่อแพทย์): เช็ค trap list ด้านล่าง

## วิธีใช้
วาง skill นี้ + เล่าเคส (ผลแล็บที่ได้ + อายุ/เพศ/อาการ/ประวัติ) → AI ชี้ "ค่าไหน pivotal → ชี้ทางไหน → reflex test อะไร" + กับดักที่ทำให้พลาด

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### กฎเหล็กก่อนสรุป/ชี้ทางเสมอ — ถาม/เช็ค 4 อย่าง
1. **Clinical context คืออะไร** (อายุ/เพศ/อาการ/ประวัติยา/ประวัติเดินทาง/โรคประจำตัว) — ตัวเลขลอยไม่มีคนไข้ = อ่านผิด
2. **ตัวอย่างถูกต้องไหม (pre-analytical):** hemolysis? clot? heparin tube กับ PCR? เก็บผิดเวลา? → ถ้าสงสัย ขอ recollect ก่อนเชื่อค่า
3. **ค่าผิดปกติเด่น (pivotal) คือตัวไหน** + มัน "ชี้ทางเดียว" หรือ "ชี้หลายทาง" (ต้อง reflex test เพิ่ม)
4. **ยา/ภาวะที่รบกวนผลได้** (anti-CD38, biotin, autoAb, ภาวะ in-vivo) — interference ≠ โรค

### Fork 1 — เบาะแส lab ตัวไหน → ชี้ทางไหน (pivotal value → DDx branch)
- **MCV เป็นแยกแรกของ anemia:** <80 microcytic → iron study; >100 macrocytic → B12/folate; normo → retic/hemolysis
- **iron study 4 ตัวรวมกัน ตัดสินทิศ:** ferritin↓ + TIBC↑ + %sat↓ = IDA แท้ → ต้องหา **แหล่งเสียเลือด** ต่อ (เช่น CT เจอ leiomyoma) · ถ้า ferritin ปกติ ในคน microcytic → **ห้ามหยุดที่ IDA** → reflex Hb typing/DNA
- **AST/ALT vs ALP/GGT = แยก liver pattern:** transaminase >>300 = hepatocellular (เช่น DILI); ALP/GGT เด่น = cholestatic · ⚠️ **albumin↓ + AST/ALT ปกติ ≠ ตัดตับออก** — cirrhosis ชดเชย ~37-48% LFT ปกติ; albumin↓ = ตับ (synthetic fail) / ไตรั่ว / ทุพโภชนาการ-อักเสบ → แยกด้วย PT/INR + GGT/ALP + urinalysis (RBC cast = glomerular)
- **conjugated fraction (DB/TB) แบ่งดีซ่าน (heuristic สอน ไม่ใช่ cutoff ตายตัว — ขอบเบลอ/ทับซ้อน, ตำราใช้ 15–30% ก็มี):** ~<20% = pre-hepatic (unconjugated) / ~20–50% = hepatocellular / ~>50% = post-hepatic (obstructive) · ต้องดู pattern + clinical ประกอบเสมอ
- **TSH ต่ำ + FT3/FT4 สูง = thyrotoxic** → fork สำคัญคือ RAIU + thyroglobulin: ทั้งคู่ต่ำ + autoAb ลบ = hormone จากภายนอก (factitia) ไม่ใช่ Graves
- **panreactive ทุก cell ที่ AHG** (auto+screen+unit 1+) + ประวัติยา → คิด drug interference (anti-CD38/daratumumab) **ก่อน** alloantibody
- **cardiac:** อ่าน delta (0h→1h) ของ hs-troponin ไม่ใช่ค่าเดี่ยว — single value ปกติไม่ตัด MI

### Fork 2 — rule-out DDx ทีละตัว (diagnosis of exclusion)
ใช้เมื่อ pivotal value ชี้หลายทาง ลำดับ: **viral → autoimmune → metabolic → toxin/drug → "เหลือคำตอบเดียว"**
- DILI: ตัด viral/autoimmune/Wilson/acetaminophen/pregnancy หมด → เหลืออาหารเสริม (usnic acid)
- factitia: ตัด Graves/thyroiditis ด้วย RAIU+Tg → เหลือ exogenous hormone
- **กฎ:** อย่าประกาศ "diagnosis of exclusion" จนกว่าจะ **ตัดตัวที่ treatable/อันตรายกว่าออกก่อน**

### Fork 3 — เมื่อไหร่ต้อง reflex / confirm test เพิ่ม
- **screening positive ≠ จบ → ยืนยันเสมอ:** micro = culture → Gram → biochemical → AST (disk+MIC) → resistance gene · serology = Ag/NS1 (acute) ตามด้วย PCR ยืนยัน serotype
- **iron ปกติในคน microcytic** → reflex Hb typing → ถ้า typing งง/A2A สูงโดยไม่เข้า thal → NGS (เจอ KLF1)
- **smear เจอ blast** → reflex BM + immunophenotyping (TdT/CD19 = Pre-B-ALL) + cytogenetic บอก prognosis
- **plasma cell + M-protein** → reflex β2-MG, Bence Jones, CD138; ถ้ามีอาการ CNS → body fluid (CSF) จับ relapse

### Fork 4 — pre-analytical / artifact ก่อนเชื่อค่า (ค่าผิด = artifact ไม่ใช่โรค)
- **specimen/tube ผิด:** heparin tube ห้ามใช้กับ RT-PCR → ผลลบเทียม
- **in-vivo/in-vitro interference:** serum GM false-negative ใน non-neutropenic → ต้องส่ง tracheal aspirate/BDG เสริม · daratumumab ทำ AHG panreactive → ไม่ใช่ alloAb
- **biology ของค่า:** วัด 25(OH)D (half-life ยาว = สถานะจริง) ไม่ใช่ 1,25(OH)₂D (อาจปกติทั้งที่ขาด)
- **ถ้าค่าวิกฤตขัดกับคนไข้** (เช่น Hb 1.4 แต่คนยังเดินได้) → ยืนยัน + ดู clinical (มี flow murmur จริง = anemia จริง)

### Fork 5 — เขียน cause→effect chain (เชื่อม lab ให้เป็นเรื่องเดียว)
แทนที่จะ list ค่าผิดทีละตัว → ร้อยเป็น flow: **trigger → mechanism → lab abnormality → clinical sign**
- ตัวอย่าง: แยกตัว → แดด/อาหารน้อย → 25(OH)D↓ → Ca ดูดซึม↓ → Ca↓ → secondary hyperPTH (iPTH↑) → bone resorption↑ (CTx/NTx↑) → Trousseau/Chvostek+ / QT ยาว
- **ทุกค่าผิด อธิบายได้ด้วยกลไกเดียว = ชี้ทางแน่น (ส่งต่อแพทย์วินิจฉัย)**

---

## กับดัก (Anti-patterns) — เช็คทุกเคสก่อน lock
- **Anchoring** — ติดธงแรกแล้วไม่ดู alternative · ก่อน lock IDA ในคน microcytic ต้องเช็ค ferritin (ดูเหมือน thal แต่จริงเป็น KLF1) · บังคับตัวเองตั้ง DDx ≥3 ก่อนเลือก
- **เชื่อ single test ไม่ cross-check** — screen/serology/typing ตัวเดียว positive ≠ diagnosis · ต้อง confirm (culture, PCR, biopsy, NGS) · serum GM ลบ แต่ BDG+culture บวก → อย่าตัดจากค่าเดียว
- **ละเลย pre-analytical / interference** — heparin+PCR, daratumumab+AHG, hemolysis ดัน K⁺/LDH · เห็นค่าแปลก "เกินคนไข้" → สงสัย artifact ก่อนสร้างโรคใหม่
- **ตัวเลขลอย ไม่ดู clinical context** — albumin ต่ำ → ตับหรือไต? ต้องดู AST/ALT + urinalysis (red cell cast = glomerular)
- **Miss zebra ที่ pattern ชัด** — panreactive AHG → นึก anti-CD38; thyrotoxic + RAIU ต่ำ → นึก factitia ไม่ใช่ Graves อัตโนมัติ; coinfection (dengue+COVID)
- **Confirmation bias** — สั่งเฉพาะ test ที่ยืนยันสมมติฐานตัวเอง · ต้องสั่ง test ที่ **หักล้าง DDx อื่น** ด้วย (rule-out cascade)
- **ไม่ดู progression/timing** — micro→macroalbuminuria, NS1 (≤7วัน) vs IgM/IgG, troponin delta
- **ตัด hemolysis/B12/folate ไม่ครบ** ก่อนสรุป anemia type (เช็ค bilirubin/haptoglobin/LDH/B12/folate หมดก่อน)

## Quick reference — 8 reasoning patterns
| Pattern | สาระสั้น |
|---|---|
| Microcytic anemia workup | MCV<80 → iron study → iron ปกติ? → Hb typing/DNA |
| Rule-out cascade | ตัด viral/AI/metabolic/toxin จนเหลือ 1 |
| Jaundice by DB/TB | pre / intra / post-hepatic (heuristic, ขอบเบลอ — ดู clinical ประกอบ) |
| Enzyme → liver pattern | AST/ALT=hepatocellular · ALP/GGT=cholestatic · alb↓+enzyme ปกติ → อย่าตัดตับ (cirrhosis/synthetic) vs ไต/อักเสบ |
| Serology timing | Ag/NS1=acute · IgM/IgG=primary/secondary · PCR=ยืนยัน+serotype |
| Confirmatory cascade (micro) | culture→Gram→biochem→AST(MIC)→resistance gene |
| Hormone source localization | RAIU+Tg+autoAb แยก endo vs exo |
| BB interference recognition | panreactive AHG + ยา → drug interference |

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริงที่เคยร้อยผลแล็บข้ามแขนงได้/พลาด เช่น:
> - *"เคสที่ค่า pivotal ดูชี้ทางหนึ่ง แต่ reflex test กลับพลิกเป็นอีกโรค คือ..."*
> - *"เคสที่เกือบสรุปผิดเพราะ artifact/interference จับได้เพราะ..."*
> - *"pattern ข้ามแขนงที่เจอบ่อยในแล็บผม + วิธีร้อยให้เป็นเรื่องเดียว..."*

---
*เครื่องมือช่วยคิดเชิงวินิจฉัยจากผลแล็บข้ามแขนงเพื่อการศึกษา — ช่วยคิด ไม่ใช่คำสั่งทางการแพทย์และไม่ตัดสินใจแทน การตีความผลแล็บกระทบการวินิจฉัยและรักษาผู้ป่วยโดยตรง ต้องยืนยันกับ MT/แพทย์ผู้ดูแล + ทำตาม SOP และตำรา/แหล่งอ้างอิงมาตรฐานเสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: clinmicro-judgment ═════════ -->

---
skill: clinmicro-judgment
title: ตัวช่วยตัดสินใจแล็บจุลชีววิทยาคลินิก (Clinical Micro Judgment)
type: ADVISE
needs: any
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "Skill นี้เป็นตัวช่วย 'คิด' สำหรับการตัดสินใจในแล็บจุลชีววิทยาคลินิกเพื่อการศึกษา ไม่ตัดสินแทน และไม่ใช่คำสั่งวินิจฉัย/รักษา ทุกผลต้อง correlate กับ Gram stain + clinical + colony morphology และทำตาม SOP/QC ของห้องแล็บเสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง ความผิดพลาดในการรายงานเชื้อก่อโรค/ความไวต่อยา อาจกระทบความปลอดภัยของผู้ป่วยโดยตรง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ตัวช่วยตัดสินใจแล็บจุลชีววิทยาคลินิก

ตัวช่วย "ตัดสินใจ" ในแล็บจุล ไม่ใช่ตำราชนิดเชื้อ/สูตร media — ทุกคำตอบตอบ 2 อย่าง: "ตรงนี้เลือกอะไร" + "พลาดตรงไหน".

> **กฎเหล็ก #1:** correlate กับ Gram/clinical/site เดิม **ก่อน** report เสมอ. ผลขัด Gram smear / site / colony = หยุด ทวนก่อน. กับดักอันดับ 1 = **รายงาน normal flora เป็น pathogen** (CoNS 1 ขวด, urine ≥3 ชนิด, sputum oral flora) — ถาม "site + count + จำนวนชนิด + clinical" ครบก่อนเรียกว่าเชื้อจริง.
> **กฎเหล็ก #2 (ขอบยาก — "S แต่ใช้ไม่ได้"):** ผล S/I/R ไม่ใช่คำตอบสุดท้ายเสมอ — เชื้อบางกลุ่ม **ผล S ตอนแรกแต่ดื้อจริง/ดื้อขึ้นระหว่างรักษา** (AmpC-derepression, inducible clindamycin, intrinsic resistance, ESBL ที่ disk เดี่ยวจับไม่ได้). เห็น "S" ในเชื้อกลุ่มเสี่ยง → ต้องรู้จาก **species/phenotype-confirm** ไม่ใช่เชื่อ zone ตรงๆ.

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- ต้อง decide ในงาน Micro — เชื้อจริงหรือปน, ID พอยัง, อ่าน AST, รายงาน MDR
- รับ/ปฏิเสธ specimen, เลือก culture vs molecular
- ก้ำกึ่งว่าจะ ID/AST ต่อหรือพอแค่นี้
- (สาย sales/MolDx) เตรียมคุยงาน Lab/MolDx — bioMérieux VITEK, Cepheid GeneXpert, AST/MALDI automation

## วิธีใช้
วาง skill นี้ + เคส/ผลที่เจอ (Gram, media, colony, AST, specimen info) → AI เดินตาม fork ด้านล่าง บอก "เลือกอะไร" + "กับดักที่ต้องระวัง" โดย correlate กลับ Gram/clinical เสมอ

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### FORK 1 — ID workflow: เดินยังไง + เมื่อไหร่พอ
ลำดับ: Gram stain → เลือก media + atmosphere → biochem/MALDI-TOF → S/I/R.
- Gram บอกทาง: GPC cluster → Staph lane (catalase → coagulase/cefoxitin). GPC chain/diplo → Strep lane (hemolysis + bile-esculin/optochin). GNB → lactose vs non-lactose → oxidase แยก non-fermenter (Pseudo/Acineto).
- เมื่อไหร่พอ: ID ละเอียดแค่ที่ เปลี่ยนการรักษา/รายงาน. Urine E. coli predominant + AST = พอ. alert organism / sterile site (blood, CSF) → ID ให้ถึง species + เก็บ isolate.
- MALDI-TOF vs biochem: มี MALDI → ใช้แทน biochem panel ยาวได้. biochem/VITEK ยังจำเป็นตอน MALDI ก้ำกึ่ง หรือเชื้อไม่อยู่ใน library.
- (สาย sales/MolDx) VITEK/MALDI ตัด hands-on time + standardize ID; ชู turnaround + reproducibility.

### FORK 2 — เลือก media + atmosphere (ผิด = เชื้อไม่ขึ้น เงียบๆ)
- Fastidious (Strep, Neisseria, Haemophilus) → Chocolate agar + 5% CO₂.
- Anaerobe สงสัย (abscess, deep wound) → anaerobic jar/chamber + media anaerobe.
- Selective ตาม specimen: stool → MacConkey + selective (Salmonella/Shigella) + enrichment Selenite F; urine → CLED/CHROMagar; GBS screen → enrichment broth.
- trade-off: เพิ่มจาน selective/atmosphere = sensitivity ขึ้น แต่ cost/labor ขึ้น. เลือกตาม specimen + clinical question.

### FORK 3 — เชื้อจริง หรือ contaminate (สำคัญที่สุด)
| สถานการณ์ | ถาม | ตัดสิน |
|---|---|---|
| Blood culture ขึ้น CoNS / diphtheroid / Bacillus 1 ขวด จาก 2+ | กี่ขวด? sterile site? sepsis? | 1/2 ขวด skin flora → contaminate; ทั้ง 2 ขวด + line/clinical → อาจจริง |
| Urine ขึ้น >3 ชนิด ใกล้กัน | colony count? predominant? | "Mixed bacterial growth" → contamination, ขอ specimen ใหม่ |
| Urine CoNS/α-strep/diphtheroid นับน้อย | urethral flora? | normal flora → ไม่ต้อง ID/AST เว้นแต่ predominant + count สูง |
| Sputum ขึ้น normal oral flora ล้วน | Q-score ผ่านไหม? | คุณภาพแย่ → ปฏิเสธ/ขอใหม่ |

Urine colony count (loop 0.001 ml): ≥10⁵ CFU/ml pure/predominant = indicated pathogen (ID+AST); 10⁴–10⁵ = suspected; 10³–10⁴ = แปลตาม site/อาการ/single-vs-mixed (borderline); <10³ = "no significant growth".
- ⚠️ **10⁵ = เกณฑ์ asymptomatic/screening** — ในคน **มีอาการ** (acute cystitis) single uropathogen ที่ ≥10²–10³ CFU/ml ก็ significant; ยึด 10⁵ ตายตัวพลาด symptomatic UTI ได้ถึง ~50% → **ผูก cutoff กับ symptom status เสมอ**.
- หลัก: site + count + จำนวนชนิด + clinical ประกอบกัน.

### FORK 4 — AST: เลือก method + อ่าน S/I/R + escalate MDR
- Disk diffusion vs MIC: disk (Kirby-Bauer, MHA/0.5 McFarland/35±2°C/16-18h) = routine. MIC (broth microdilution/E-test/VITEK) เมื่อต้องการค่าตัวเลข — sterile site, ปรับ dose, หรือ disk ก้ำกึ่ง.
- อ่าน zone — 3 ข้อยกเว้น: (1) sulfa/co-trimox → ignore growth จางใน zone <20%; (2) Proteus swarm → อ่านขอบ inhibition จริง; (3) β-lactamase+ Staph vs penicillin → ขอบ zone คม "cliff" = R เสมอ.
- confirmatory + escalate: MRSA (cefoxitin → report เป็น oxacillin, zone ≤21=R) → report + infection control. Inducible clindamycin (Erythro=R + Clinda=S → D-test; D+ → report clindamycin R). ESBL (ดื้อ ceph 3rd → combo disk +clav ≥5mm). CRE/carbapenemase (mCIM/eCIM; eCIM+EDTA → metallo/NDM → รายงานด่วน + แยกผู้ป่วย). VRE (screen + รายงาน alert).
- (สาย sales/MolDx) GeneXpert Carba-R / mecA PCR = ตัดเวลา confirmatory phenotype.

### FORK 5 — Specimen quality: รับหรือปฏิเสธ
- Sputum Q-score/Bartlett: accept ถ้า SEC <10/lpf + PMN >25/lpf (เป็น LRT จริง) · reject ถ้า SEC >25/lpf (ปนน้ำลาย) → ขอใหม่ · 10–25/lpf = borderline correlate กับ Gram/clinical ก่อนตัดสิน.
- Reject เมื่อ: ฉลากไม่ตรง/ไม่มี, container รั่ว, transport ผิด, ปริมาณไม่พอ, ซ้ำใน 24h ไม่จำเป็น.
- GIGO. แต่ specimen หายาก (CSF, biopsy, intraop) → อย่าทิ้ง ติดต่อแพทย์/process + note limitation.

### FORK 6 — Culture vs Molecular (GeneXpert / PCR)
- TB: AFB smear sens ต่ำ + ไม่แยก viable/MTB-NTM; culture = gold แต่ 4–8 สัปดาห์ → GeneXpert MTB/RIF เมื่อต้องการผลเร็ว + ดื้อ rifampin (rpoB) (<2 ชม.). ยังต้อง culture+DST สำหรับ panel ยาเต็ม.
- Virus / culture ช้า-อันตราย: HIV viral load, HBV/HCV-RNA, respiratory panel → real-time PCR. Infant HIV → DNA/RNA PCR ไม่ใช่ Ab.
- หลัก: molecular เมื่อ culture ช้า/อันตราย/sens ต่ำ, ต้องการ resistance gene เร็ว, เชื้อเพาะยาก. Culture ชนะตอนต้องการ isolate ไปทำ AST เต็ม + cost.

### FORK 7 — Specimen-site → เชื้อที่คาด + media ตาม syndrome (อย่าหว่านจานเดียวกันทุก site)
อ่าน **site + host + syndrome** กำหนด workup ก่อนเพาะ:
- **CSF/meningitis:** อ่าน CSF profile ก่อนเดา — neutrophil↑ + glucose↓มาก + protein↑ = bacterial (รายงานด่วน); lymphocyte + glucose ปกติ = viral; lymphocyte + glucose↓ ปานกลาง = TB/fungal · เชื้อตาม **อายุ** (newborn GBS/E.coli/Listeria · เด็ก Nm/Spn/Hib · สูงอายุ +GNB/Listeria) · ⚠️ Cryptococcus cell count อาจปกติ → **สั่ง CrAg/India ink เสมอ อย่าตัดออกเพราะ cell ปกติ**
- **LRTI:** Gram screen ก่อนเพาะ (accept PMN>25 + SEC<10/lpf; reject SEC>25/lpf; 10–25 = borderline — ตรงกับ FORK 5) · **VAP/BAL = quantitative** (≥10⁴ CFU/ml = จริง) ไม่ใช่ qualitative · TB ใช้ early-morning sputum ×3
- **Stool:** เพาะเมื่อ bloody/leukocyte+/ไข้/travel · media ตาม syndrome (TCBS+APW→Vibrio · SS/XLD/HE+enrich→Salmonella/Shigella · CCFA→C.diff · 42°C microaerophilic→Campylobacter) · ⚠️ ไม่ enrich = จับ Vibrio/Salmonella ไม่ได้
- **Genital:** GC→Thayer-Martin/VCN · **BV ไม่เพาะ** ใช้ pH>4.5 + whiff + clue cells
- **Sterile fluid** (pleural/peritoneal/joint/CSF): เชื้อใดก็ significant → ลง BA/CA/MC + **thioglycollate (anaerobe, ดู 7 วัน)**; อย่ามองข้าม anaerobe ใน deep pus

### FORK 8 — Special-organism pathways (fungi · mycobacteria · zoonosis/Rickettsia)
- **Fungi yeast-vs-mold:** KOH/calcofluor direct → SDA ± additive · ⚠️ **cycloheximide กด opportunistic mold (Aspergillus/Fusarium/Zygomycetes/Cryptococcus) + Nocardia** → ถ้าสงสัยพวกนี้ **อย่าใช้สื่อ cycloheximide จานเดียว** · Cryptococcus → CrAg เร็วกว่ารอเพาะ
- **Mycobacteria ladder:** ZN/auramine smear (sens ต่ำ 5,000–10,000/ml, **smear-neg ไม่ตัด TB**, แยก MTB/NTM ไม่ได้) → culture gold (MGIT 1–3wk เร็วกว่า LJ 6–8wk) → MTB-vs-NTM (niacin+/nitrate+/MPT64+) → DST/GeneXpert สำหรับ MDR
- **Zoonosis/Rickettsia/Chlamydia:** serology+molecular เป็นหลัก, culture ทำไม่ได้/ต้อง BSL-3 → paired serology 4-fold + IFA + PCR · Weil-Felix = screening หยาบ ไม่ confirm · ⚠️ **Leptospira PCR ใช้ EDTA — ห้าม heparin** (heparin ยับยั้ง Taq); ส่วน *culture* heparin ได้/citrate-oxalate ฆ่าเชื้อ = คนละเหตุ · ผู้ป่วยหนัก ใช้ PCR/Giemsa buffy coat เร็วกว่ารอ serology

### FORK 9 — Gram triage power + ID-fork refinements + virulence→test
- **Gram = triage อันดับ 1** กำหนด media/atmosphere/เดาเชื้อ/รายงาน direct ก่อน culture เสร็จ + บอกคุณภาพ specimen (squamous เยอะ=ปนน้ำลาย) + ชนิด WBC (PMN=bacterial · lympho=viral/TB)
- ⚠️ **Gram misread:** over-decolorize (GP→ดู GN; colony เก่า decolorize ง่าย → ใช้ **fresh colony**) · under-decolorize (GN→ดู GP) · gram-variable (Gardnerella/Clostridium/เซลล์แก่) · stain precipitate ดูเป็น GPC → correlate รูปร่าง+culture, อย่ารายงานจาก smear ที่ control ไม่ผ่าน
- **GPC fork:** catalase (Staph+/Strep−) → coagulase (aureus+/CoNS−; **slide=clumping 20วิ; ลบต้อง confirm tube 4ชม.**) → **novobiocin (S. saprophyticus = R)** · ⚠️ **catalase ห้ามทำบน blood agar** (RBC มี catalase → false+)
- **GNB fork:** **oxidase แยกขั้ว** — ลบ = Enterobacterales (ferment glucose ทุกตัว) · บวก = Vibrio/Aeromonas (fermenter) หรือ NFGNB (Pseudomonas ox+ / Acinetobacter ox−) → lactose/TSI/IMViC/urease แยก genus
- **virulence → test:** **endotoxin (LPS) = เฉพาะ GNB** (ปล่อยตอนเซลล์แตก) · **exotoxin = จำเพาะ ตรวจตรงได้** (ELEK ของ diphtheria · Shiga toxin · C.diff toxin A/B · TSST-1) · capsule = target serotyping/วัคซีน

## กับดัก (Anti-patterns)
1. รายงาน contaminant เป็น pathogen — CoNS 1 ขวด, urine 3+ ชนิด, sputum oral flora.
2. ไม่ correlate กับ Gram เดิม — AST/ID ขัด Gram smear = หยุด ทวน.
3. Misread AST — ESBL / inducible clinda / β-lactamase Staph → ปล่อยยาที่ใช้ไม่ได้จริง.
4. Miss MDR ที่ต้องรายงานด่วน — MRSA/VRE/ESBL/CRE/MDR-TB ไม่ flag → ระบาดในวอร์ด.
5. เลือก media/atmosphere ผิด → false-negative เงียบ.
6. Process sputum คุณภาพแย่ → เลี้ยง oral flora รายงานเป็นเชื้อปอด.
7. Smear-negative = ไม่มี TB (ผิด) — ต้อง culture/GeneXpert.
8. QC strain หลุดแต่ยังรายงานผล — ATCC (S.aureus 25923, E.coli 25922, P.aeruginosa 27853, E.faecalis 29212) นอก range → หยุด ห้าม report.
9. Over-ID / over-AST เชื้อ commensal → เปลือง + ชวนใช้ยาเกิน.
10. ลืม intrinsic resistance — รายงาน amp/ceph สำหรับ P.aeruginosa (ดื้อโดยธรรมชาติ).
10b. **AmpC inducible high-risk (IDSA 2023: Enterobacter cloacae / Klebsiella aerogenes / Citrobacter freundii / Hafnia alvei):** lab อาจรายงานไวต่อ 3rd-gen ceph ตอนแรก แต่เชื้อ **induce AmpC ขึ้นมา hydrolyze ceftriaxone ระหว่างรักษา** → flag เตือน "อย่าใช้ 3rd-gen ceph แม้ผล S" (ยาเชื่อถือได้ = cefepime/carbapenem) — ตรวจ phenotype ตรงไม่ได้ ต้องรู้จาก species. ⚠️ Serratia / Morganella / Providencia / indole+ Proteus เคยถูกจัดกลุ่มนี้ แต่ IDSA = **low-risk derepression (<5%) → รักษาตามผล AST จริง** (ceftriaxone ใช้ได้ถ้า S) อย่า over-flag.
11. heparin ใน specimen PCR/Leptospira — heparin ยับยั้ง Taq (PCR fail) → PCR ใช้ **EDTA**; ส่วน citrate/oxalate ฆ่า Lepto เป็นเรื่อง *culture* (คนละ assay) → รู้ assay ปลายทางก่อนเลือก tube.
12. เพาะ/รายงานหลังให้ ATB = no-growth ลวง — เก็บ culture ก่อนยาเสมอ · และอย่าตัด Cryptococcus เพราะ CSF cell count ปกติ → สั่ง CrAg/India ink เมื่อสงสัย.
13. cycloheximide media จานเดียวกับที่สงสัย opportunistic mold — กด Aspergillus/Mucor/Cryptococcus/Nocardia → "no fungus" ลวงในผู้ป่วย immunocompromised.
14. anaerobe ด้วย swab + transport ธรรมดา/แช่เย็น = เชื้อตายก่อนถึงแล็บ → **aspirate (ไม่ใช่ swab) + anaerobic transport + ไม่แช่เย็น**; ฝี/แผลลึกต้องตั้ง anaerobe เสมอ.
15. serology ไวรัส Flavivirus (dengue/JE/Zika) cross-react สูง → acute ใช้ **Ag/PCR (dengue NS1)**, IgG ต้อง paired; **enveloped virus ส่งเย็น/เปราะ** (RNA สลายง่าย).

> NOTE: knowledge (taxonomy, media recipes, colony-count tables, MIC/MBC, AFB grading) → point to "ตำรา/แหล่งอ้างอิงมาตรฐาน", no path.

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - เพิ่ม antibiogram/MDR pattern เฉพาะของ รพ. ที่ผู้ใช้ทำงาน (intrinsic resistance + breakpoint local)
> - เติม cutoff/criteria ของ specimen rejection ตาม SOP ห้องแล็บนั้นๆ
> - ระบุ alert organism list + ช่องทางแจ้ง infection control ที่ใช้จริง

---
*Skill นี้เป็นตัวช่วย "คิด" เพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์และไม่ตัดสินแทน ทุกผลต้อง correlate กับ Gram/clinical + ทำตาม SOP/QC ของห้องแล็บ — ความผิดพลาดกระทบความปลอดภัยผู้ป่วยโดยตรง ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: content-creator-judgment ═════════ -->

---
skill: content-creator-judgment
title: โค้ชทำคอนเทนต์ให้ความรู้ — เลือกหัวข้อ + ไม่ทำให้เพจตาย (Content Creator Judgment)
type: ADVISE               # ช่วยตัดสินใจวางคอนเทนต์ ไม่ใช่ตำราการตลาด
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิด/วางแผนคอนเทนต์เพื่อการศึกษา ไม่ใช่คำแนะนำทางการ — คอนเทนต์การแพทย์ต้องถูกต้อง อยู่ในขอบเขตวิชาชีพ และมี disclaimer · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชทำคอนเทนต์ให้ความรู้ — เลือกหัวข้อ + ไม่ทำให้เพจตาย

ทำเพจ/ช่องให้ความรู้ (MT/วิชาการ/สายงาน) แล้วงงว่า "ทำหัวข้อไหน · จับเทรนด์ไหน · ทำไมคนไม่ดู" → โค้ชนี้ช่วย **เลือกหัวข้อ + เลี่ยงกับดักที่ทำให้เพจเงียบ**

> **กฎ #1 (ทำก่อนเสมอ):** ก่อนรับทุกหัวข้อ ถาม *"คลิป/โพสต์นี้มีจุดให้คนหยุดดู (hook/moment) ไหม — เซอร์ไพรส์ / เคลียร์ความเข้าใจผิด / เคสจริง / เรื่องที่คนเถียงกัน?"* ไม่มี = อย่าทำ หรือหา angle ใหม่ก่อน. ข้อมูลแห้งๆ ไม่มีมุม = คนเลื่อนผ่าน.
> **กับดัก #1:** **ตามเทรนด์ช้าจนอิ่มตัว (saturated) + ก๊อปสไตล์คนอื่น** → เป็นรายที่ 500 ที่ทำเรื่องเดิม ไม่มีเหตุผลให้คนดูเลือกเรา. จะแตะเทรนด์ต้องมี angle ที่คนอื่นยังไม่ทำ.
> ทำคอนเทนต์การแพทย์ → คู่กับ `explain-simply` (ง่ายแต่ไม่ผิด) + `anti-hallucination` (อย่ามั่ว) + `polite-but-clear`

## ใช้เมื่อ
- กำลังเลือกหัวข้อลงคลิป/โพสต์ · วางทิศทางเพจ/ช่อง
- ลังเลว่าจะตามกระแสไหน · คิด angle คอนเทนต์
- เพจเงียบ/คนไม่ดู หาไม่เจอว่าพลาดตรงไหน

## วิธีใช้
วาง skill นี้ + เล่าหัวข้อ/ไอเดีย + กลุ่มคนดู → AI ชี้ว่าน่าทำไหม, angle ไหน, กับดักที่เสี่ยง

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### 1. เลือกหัวข้อจาก "มี moment/hook ไหม" (หัวใจ)
ถามตามลำดับ:
1. **หัวข้อนี้มีจุดที่คนหยุดดู/รู้สึกไหม** — เซอร์ไพรส์, ความเข้าใจผิดที่เคลียร์ให้, เรื่องที่คนเถียงกัน, เคสจริง, ความผิดพลาดที่เรียนรู้ได้ → ✅ ดึง engagement
   - หัวข้อ "เรื่อยๆ ไม่มีจุดพีค / ข้อมูลแห้งๆ ไม่มีมุม" → ❌ คนเลื่อนผ่าน (ดูกับดัก)
2. **คนดูที่มีอยู่คือใคร** — เลือกหัวข้อให้ตรงคนดูเดิมก่อน ค่อยขยายไปกระแสที่ฮิตทั่วไป
3. **เล่า/สอนได้ลื่นไหม** — หัวข้อที่ซับซ้อนมากต้องมีวิธีย่อย (ใช้ `explain-simply`)

### 2. หา angle ที่ relatable
มุมที่คนดู "อิน": *มือใหม่พลาดบ่อยตรงนี้* · *เคสจริงจากงาน* · *เข้าใจผิดที่เจอประจำ* · *ทำเองได้ใน X ขั้น* — ไม่ใช่เล่าทฤษฎีลอยๆ

### 3. platform เลือกตาม "คนดูอยู่ไหน" ไม่ใช่ที่ดังสุด
คนดูส่วนใหญ่อยู่ FB / TikTok / YouTube / LINE ไหน → ทำที่นั่นก่อน · รูปแบบ (สั้น/ยาว/ภาพ/วิดีโอ) ตามแพลตฟอร์ม

### 4. จับเทรนด์เมื่อไหร่
- จับ **ตอนกำลังขึ้น (early-mid)** ที่คนสงสัยอยากดูแต่ creator ยังน้อย = ได้ reach
- **อย่าจับตอน peak/saturated** (คนทำเต็มแล้ว อัลกอเริ่มเท)
- ถามตัวเอง: *"เทรนด์นี้ฉันมี angle ที่คนอื่นยังไม่ทำไหม"* — ไม่มี = ข้าม

---

## กับดัก (Anti-patterns)
- **หัวข้อไม่มี moment/hook** → คนเลื่อนผ่าน; เช็คก่อนทำ "คลิป/โพสต์นี้มีจุดให้หยุดดูไหม"
- **ตามเทรนด์ช้า (saturated)** → เป็นรายที่ 500 ที่ทำเรื่องเดิม; จะตามต้องมี angle ใหม่
- **ก๊อปสไตล์คนอื่น (ไม่มี differentiation)** → ไม่มีเหตุผลให้คนดูย้ายมา; หา edge ที่เป็นตัวเองก่อน
- **ยึดสคริปต์/hook แข็งจนเสียธรรมชาติ** → สคริปต์เป็น "ไกด์" ไม่ใช่ "บทอ่าน"; ความจริงใจ/รีแอคชั่นจริงดึงคนกว่าบทเป๊ะ
- **เลือกจากกระแส/ความสวย แทนจาก "คนดูเข้าถึงได้"** → ดูเฉยๆ ไม่ผูกพัน
- **(สาย MT/การแพทย์) ทำคอนเทนต์ผิด/เกินขอบเขตวิชาชีพ** → เสียเครดิต + อันตราย; ต้องถูกต้อง อยู่ในขอบเขต ใส่ disclaimer (ใช้ `anti-hallucination` + `explain-simply`)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT) คอนเทนต์ให้ความรู้ที่ปังของผมคือ... เพราะมันมี hook ตรง..."*
> - *"หัวข้อการแพทย์ที่คนชอบเข้าใจผิด ทำคอนเทนต์ได้ดีถ้า... ต้องระวัง..."*

---
*ช่วยคิด/วางแผนคอนเทนต์เพื่อการศึกษา ไม่ใช่คำแนะนำทางการ — คอนเทนต์การแพทย์ต้องถูกต้อง อยู่ในขอบเขตวิชาชีพ และมี disclaimer · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: critical-appraisal-judgment ═════════ -->

---
skill: critical-appraisal-judgment
title: โค้ชอ่าน/ประเมินงานวิจัย + lit review — หา gap + ประเมิน test (Critical Appraisal & Lit-Review Judgment)
type: ADVISE               # ช่วยอ่าน/ประเมินเปเปอร์คนอื่น ไม่ใช่ตำราระเบียบวิธี
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดอ่าน/ประเมินงานวิจัย + ทบทวนวรรณกรรมเพื่อการศึกษา ไม่ใช่ที่ปรึกษาวิจัยทางการ — ต้องยืนยันกับเปเปอร์ต้นฉบับ + อาจารย์ที่ปรึกษา · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชอ่าน/ประเมินงานวิจัย + lit review — หา gap + ประเมิน test

อ่านงานวิจัยคนอื่นให้เป็น (lit review / journal club / หาหัวข้อ thesis) — เปเปอร์นี้ดี/เชื่อได้แค่ไหน · gap อยู่ตรงไหน · ใช้ method ไหนเป็นแม่แบบ ไม่ใช่สรุปย่อทุกบรรทัด

> **กฎข้อ 1:** อ่านเพื่อ **(1) เชื่อได้ไหม (2) ขโมย method มาใช้ได้ไหม (3) gap = contribution เราอยู่ตรงไหน** — ไม่ใช่จำ finding
> **กับดักอันดับ 1:** เห็น sens/spec สูงแล้วเชื่อเลย — **PPV ขึ้นกับ prevalence: ถ้าโรคหายาก ผลบวกส่วนใหญ่เป็น false+ ต้อง confirm** (sens/spec ไม่ขึ้นกับ prevalence, NPV เป็นกระจกสะท้อน = สูงตอน prevalence ต่ำ). ก่อนเชื่อตัวเลขทุกครั้ง: ดู gold standard เหมาะไหม · blinded ไหม · spectrum/sample bias.
> นี่คือชั้น **"อ่าน/ประเมินงานคนอื่น + หา gap"** — ออกแบบงานตัวเอง → `research-design-judgment` · เขียนเล่ม/ตีพิมพ์ → `manuscript-judgment` · เลือก test สถิติ → `choose-stat-test` · กันอ้างมั่ว → `anti-hallucination`

## ใช้เมื่อ
- ทำ literature review / journal club / หา research gap ก่อนตั้งหัวข้อ
- อ่านเปเปอร์ "method ใหม่ vs gold standard" → ประเมินความน่าเชื่อ
- เลือกแม่แบบ (method spine) ให้ตรงข้อมูล/คำถามตัวเอง

## วิธีใช้
วาง skill นี้ + วาง abstract/เปเปอร์ (หรือเล่าคำถามวิจัย + กองเปเปอร์) → AI ช่วยสกัด method/finding/relevance + ชี้ gap + จุดอ่อนที่ตีได้

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — อ่านเปเปอร์ 1 ฉบับ: สกัด 4 อย่าง (transform ไม่ลอก)
- **Objective** (ถามอะไร) · **Method** (data → preprocess → model/analysis → evaluation) · **Key finding** (ตอบ objective ไหม) · **Relevance** (ใช้กับงานเรายังไง: แม่แบบ method / domain anchor / cite-เฉยๆ)
- จด **method skeleton ให้ทำซ้ำได้** (dataset, ขั้นตอน, พารามิเตอร์, metric) — ถ้าจะเอามาใช้ ต้อง lock ค่าจริงจากเปเปอร์เต็ม ไม่ใช่จากสไลด์/abstract

### Fork 2 — ประเมินงาน "test/method ใหม่ vs gold standard" (recurring สุดในงาน MT)
- โครง: **sensitivity / specificity / PPV / NPV / accuracy** เทียบ gold standard (เช่น molecular/biopsy/culture) — **AUC ใช้กับ test แบบต่อเนื่อง/จัดอันดับ (มี cutoff ปรับได้) เท่านั้น, ไม่ใช่ test 2×2 บวก/ลบ ตายตัว**
- ⚠️ **PPV ขึ้นกับ prevalence** — test ดีแค่ไหน ถ้า prevalence ต่ำ ผลบวกส่วนใหญ่ก็ false+ → ต้อง confirm (ดู `immunoassay-judgment`/`anti-hallucination`)
- ดู **gold standard เลือกเหมาะไหม** + sample size/spectrum bias + blinded ไหม ก่อนเชื่อตัวเลข

### Fork 3 — หา research gap = contribution (white space)
- เทียบกองเปเปอร์: **อะไรที่ยังไม่มีใครทำ** (เช่น domain A × method B ที่ไม่มีใครจับคู่) = ช่องว่างที่เราเคลม
- gap ที่ใช้ได้จริง = **ทำได้ด้วยข้อมูล/เวลาที่เรามี** + ตอบคำถามที่สำคัญพอ (ไม่ใช่ gap ที่ไม่มีคนทำเพราะมันไม่คุ้ม)

### Fork 4 — เลือก "method spine" (แม่แบบ) ให้ตรงข้อมูล+คำถาม
- มีหลายเส้นทาง → เลือกที่ **fit ข้อมูลที่หาได้จริง** + **lowest ramp-up** (อันที่เคยทำ/รู้ดี = เริ่มเร็ว เสี่ยงน้อย)
- เปรียบเทียบ spine (เช่น classifier vs association-study vs forecasting) ตาม: ชนิดข้อมูล · คำถาม · เครื่องมือที่มี → อย่าเลือกเพราะ "ดูเท่"

### Fork 5 — จับ "limitation to beat" = novelty lever
- จุดอ่อนที่เปเปอร์แม่แบบมัก: **single dataset / no external validation cohort / ไม่มี modern method / sample เล็ก** → แต่ละอันคือ **ช่องที่เราอัปเกรดเป็นความใหม่ได้**
- ⚠️ **แยก 2 ชั้นให้ขาด:** k-fold/bootstrap = *internal* validation (แก้ overfit บนข้อมูลชุดเดิม) · validation บน **cohort อิสระชุดใหม่** = *external* validation (คนละชั้น แทนกันไม่ได้). เปเปอร์ที่มีแค่ k-fold ยัง **ขาด external** อยู่ → นั่นคือ lever ของเรา

### Fork 6 — Triage + read-order (อย่าอ่านทุกอันเท่ากัน)
- เรียงเปเปอร์ตาม **relevance ต่อคำถามเรา** → **read-in-full = แม่แบบ method + domain anchor** · skim = method-pattern ซ้ำ · **skip-to-cite = ที่เหลือ** (off-domain/ref)
- recurring backbone ในงาน MT diagnostic = diagnostic-accuracy (Fork 2) → results chapter ต้องพูดภาษานี้คล่อง

### Fork 7 — Quality flag ก่อนเชื่อ/อ้าง
- ⚠️ **OCR/text เพี้ยน → ตัวเลข garbled** → verify กับ PDF ต้นฉบับก่อน cite (อย่าอ้างเลขที่อ่านไม่ชัด)
- แยก **research article vs review vs product insert (IFU)** — IFU ≠ งานวิจัย, review = cite-don't-copy
- ⚠️ **ห้ามแต่ง finding ที่ไม่มีใน text** — สรุปเฉพาะที่เปเปอร์เขียนจริง

---

## กับดัก (Anti-patterns)
- **เชื่อ/อ้าง finding ที่ไม่มีในเปเปอร์จริง** — สกัดเฉพาะที่เขียนไว้
- **ลอก method ดิบ** ไม่ transform/ไม่เข้าใจ → ทำซ้ำไม่ได้
- **ลืม external validation** — single dataset = จุดอ่อน (และเป็น lever ของเรา)
- **อ่านทุกเปเปอร์เท่ากัน** — triage ตาม relevance ก่อน
- **ตีความ PPV โดยไม่ดู prevalence** — test ดีที่ low prevalence ก็ false+ ท่วม
- **cite ตัวเลข OCR/garbled** โดยไม่เช็คต้นฉบับ
- **ทำ contribution ที่ซ้ำของเดิม** — ไม่หา gap ก่อน = ไม่มี novelty

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(R2R) เปเปอร์ที่ผมใช้เป็นแม่แบบ method คือแนว... เพราะ fit ข้อมูล..."*
> - *"gap ที่ผมเจอจากการอ่านกองเปเปอร์ คือ... = contribution"*

---
*ช่วยคิดอ่าน/ประเมินงานวิจัย + ทบทวนวรรณกรรมเพื่อการศึกษา ไม่ใช่ที่ปรึกษาวิจัยทางการ — ต้องยืนยันกับเปเปอร์ต้นฉบับ + อาจารย์ที่ปรึกษา · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: crm-judgment ═════════ -->

---
skill: crm-judgment
title: โค้ช CRM ขับเคลื่อนด้วยข้อมูล — สำหรับ MT สาย sales/คลินิก (Data-Driven CRM Judgment)
type: ADVISE               # ช่วยตัดสินใจเรื่องลูกค้า ไม่ใช่ตำรา framework
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดเรื่องลูกค้า/CRM เพื่อการศึกษา ไม่ใช่คำแนะนำทางกฎหมาย — การใช้ข้อมูลส่วนบุคคลต้องผ่าน consent (PDPA) เสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช CRM ขับเคลื่อนด้วยข้อมูล (สำหรับ MT สาย sales / คลินิก / แอป)

MT ที่ไปสาย **diagnostics sales, เปิดคลินิก, หรือทำแอป/บริการ** แล้วต้องคิดแบบ "ลูกค้า" → โค้ชนี้ช่วย **ตัดสินใจเรื่องลูกค้า + เลี่ยงกับดัก** ไม่ใช่ท่องนิยาม framework

> **กฎ #1 — consent มาก่อนเสมอ:** ห้ามแตะ/ส่งต่อ personal/behavioral data ก่อนได้ **explicit consent**. ถาม "ขอ consent หรือยัง?" ก่อนทุก segmentation/recommendation
> **กับดัก #1 (ตัวที่เผลอแม้มี consent) — purpose limitation:** consent ผูกกับ **วัตถุประสงค์ที่ขอไว้เท่านั้น**. ขอเพื่อ A แล้วเอาไปทำ B (เช่น ขอเพื่อให้บริการ → เอาไป market/ขายต่อ/train model) = **ต้องขอ consent ใหม่** ถึงจะมีฐานเดิมอยู่ก็ใช้ข้ามไม่ได้
> นิยาม framework เป็น commodity — ที่นี่เก็บแต่ **"เลือกอะไรเมื่อไหร่" + กับดักที่คนพลาด**

## ใช้เมื่อ
- ออกแบบ segment ลูกค้า / logic แนะนำสินค้า / แผน retention-loyalty
- ตอบวิกฤต/คำร้องเรียน (PR) · คิด cross-sell น้ำยา/บริการ
- "segment ลูกค้ายังไง", "แนะนำสินค้า CF/CBF", "ลูกค้ากลุ่มนี้ทำไงต่อ"

## วิธีใช้
วาง skill นี้ + เล่าสถานการณ์ลูกค้า → AI ชี้ทางเลือก + กับดัก

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### 1. เลือก segmentation แบบไหน (เริ่มจาก "มีข้อมูลอะไร + จะเอาไปทำอะไร")
| ถ้า… | เลือก |
|---|---|
| อยากรู้ใครทำเงิน + จัดสรร resource | **Value-based** |
| มีแค่ log การใช้/ซื้อ (data หาง่าย) | **Behavioral** (เริ่มจากนี่ถ้าไม่มีอย่างอื่น) |
| อยากกัน churn / ดัน cross-sell ล่วงหน้า | **Propensity** (value-at-risk = propensity × value) |
| แยกคนภักดี vs คนจะหนี | **Loyalty** |

### 2. รู้ CLV 2×2 (กำไร × ความยาวความสัมพันธ์) แล้ว → ลงทุนกลุ่มไหนยังไง (fork ที่มีค่าสุด)
- **True Friends** (กำไรสูง/อยู่นาน) → **เทงบ nurture + retain** = กลุ่มที่ควรทุ่ม
- **Butterflies** (กำไรสูง/อยู่สั้น) → **เก็บช่วงสั้นแบบ transactional แล้ว STOP เมื่อจะไป** (อย่าฝืนดึงให้ loyal = เผางบ)
- **Barnacles** (กำไรต่ำ/อยู่นาน) → **cross-sell/up-sell หรือคุมต้นทุน** (push self-service); ดันไม่ขึ้น → ลดต้นทุนบริการ
- **Strangers** (กำไรต่ำ/อยู่สั้น) → **ไม่ลงทุน**

### 3. recommendation: CF vs CBF vs Hybrid
- **Collaborative Filtering (CF)** — "คนคล้ายกันชอบ" ใช้เมื่อมี history เยอะ (⚠️ พังกับลูกค้าใหม่ = cold-start)
- **Content-Based (CBF)** — เทียบ content กับ profile ใช้ตอน **cold-start/ลูกค้าใหม่**
- **Hybrid** — CBF อุ้มช่วงแรก → ผสม CF เมื่อ history พอ
- กฎจำง่าย: **ลูกค้าใหม่=CBF, เก่ามีประวัติ=CF, ระบบโตจริง=Hybrid**

### 4. crisis/PR posture (เลือกจาก "ความรับผิดชอบ")
- ไม่ใช่ความผิดเรา/ข่าวลือ → **Denial** · ผิดน้อย/สุดวิสัย → **Diminishment** · เราผิดหลัก → **Rebuilding** (ขอโทษ+ชดเชย ห้ามแถ)
- ใส่ **instructing + adjusting info ทุกวิกฤต** · **ห้ามใช้ Denial ปนกับ rebuilding** (ขัดกันเอง ดูไม่จริงใจ)

### 5. เมื่อไหร่ทำ Market-Basket / Association
มี transaction แบบตะกร้า + อยากหา bundle/cross-sell → วัด Support / Confidence P(B|A) / **Lift>1 = สัมพันธ์จริง** (อย่าเชื่อ confidence ลอยถ้า lift≈1)

---

## กับดัก (Anti-patterns)
- **ใช้ data ก่อนได้ consent (PDPA/GDPR)** — ☠️ ใหญ่สุด ต้อง **explicit consent ก่อน** เอา personal/behavioral data ไปใช้/ส่งต่อ; privacy by design ตั้งแต่ออกแบบ ไม่ใช่แปะทีหลัง
- **ใช้ data ข้ามวัตถุประสงค์ (ทั้งที่มี consent แล้ว)** — กับดักที่เนียนกว่า: consent คุมแค่ purpose ที่ขอ. repurpose ไป marketing/ขายต่อ/train model โดยไม่ขอใหม่ = ผิดเท่าไม่มี consent (เช็กทุกครั้งว่า use ใหม่ตรง purpose เดิมไหม)
- **Cold-start ใน CF** — ยัด CF ให้ลูกค้าใหม่ที่ไม่มี history → แนะนำมั่ว → CBF อุ้มก่อน
- **ลงทุนผิดกลุ่ม (เท Butterflies)** — ทุ่ม retain คนที่ยังไงก็ไป = เผางบ; งบไปลง True Friends
- **Vanity metric** — วัด like/engagement ที่ไม่เชื่อมกับ revenue/retention; ถามทุกครั้ง: metric นี้แปลงเป็นเงิน/การอยู่ต่อยังไง
- **ใช้ Denial ผิดเคส** — ผิดจริงแต่ปฏิเสธ → เสีย trust ถาวร
- **Data quality หลุด** — segment จาก data accuracy/timeliness แย่ = garbage in/out
- **สับ Profiling กับ Segmentation** — profile = persona รายคน (วัตถุดิบ) · segment = กลุ่ม (ผลลัพธ์)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT→sales) lab ลูกค้าแบบ True Friend ผมดูแลโดย... · แบบ Butterfly ผม..."*
> - *"cross-sell น้ำยา/บริการ จังหวะที่ได้ผลคือ..."*

---
*ช่วยคิดเรื่องลูกค้า/CRM เพื่อการศึกษา ไม่ใช่คำแนะนำทางกฎหมาย — การใช้ข้อมูลส่วนบุคคลต้องผ่าน consent (PDPA) เสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: cv-judgment ═════════ -->

---
skill: cv-judgment
title: โค้ช Computer Vision — เลือกเทคนิคภาพให้ถูก (CV & Image Analysis Judgment)
type: ADVISE               # ช่วยตัดสินใจเลือกเทคนิค ไม่ใช่ตำราสูตร
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดเลือกเทคนิค image analysis เพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์ — งานวินิจฉัยจากภาพ (เช่นเซลล์/สเมียร์) ต้องมี MT/แพทย์ยืนยันเสมอ ไม่ใช้ผลโมเดลตัดสินคนไข้ลำพัง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช Computer Vision — เลือกเทคนิคภาพให้ถูก

งานวิเคราะห์ภาพ (classify/segment/นับเซลล์) แล้วงงว่า "preprocess อะไร · feature ตัวไหน · classical หรือ deep" → โค้ชนี้ตอบ **"เลือกเทคนิคไหนเมื่อไหร่ + พลาดตรงไหน"**

> **กฎ #1: data น้อย/feature ชัด → classical (HOG/GLCM → SVM) ก่อนเสมอ; อย่าไป deep CNN.** Deep บน data น้อย = overfit จำไม่ generalize. **กับดัก #1: threshold "สี" ใน RGB** — เพี้ยนทันทีที่แสงเปลี่ยน → ใช้ **HSV** เมื่อสีคือ criterion.
> **กับดัก edge (ที่พลาดบ่อยกว่า): "ภาพเยอะ" ไม่ได้แปลว่า data เยอะ** — ถ้าหลาย patch/ภาพมาจาก**เคส/คนไข้/สไลด์เดียวกัน** มันคือ data จุดเดียว. ต้อง split train/test ที่ระดับ **คนไข้/สไลด์ ไม่ใช่ patch** ไม่งั้น leakage → accuracy หลอกตา. มีเลนพิเศษ **blood smear / cell morphology** (blood-group / thalassemia)
> เลือก classifier ตัวสุดท้ายลึกๆ → ดู `ml-judgment`

## ใช้เมื่อ
- "ภาพ contrast ต่ำ/noisy ควร preprocess อะไร" · "ใช้ edge/feature/descriptor ตัวไหน" · "classical หรือ deep"
- "จะ segment เซลล์ในเลือดยังไง" · "color space ไหน" · วาง pipeline งานภาพก่อนลงโค้ด

## วิธีใช้
วาง skill นี้ + เล่างาน/แปะภาพตัวอย่าง → AI ถาม 4 อย่างแล้วชี้เทคนิค + กับดัก

---

## ก่อนแนะนำ — ถาม 4 อย่าง
1. **เป้าหมาย** = classify / detect (ตำแหน่ง) / segment (ราย pixel) / match-stitch / นับวัตถุ?
2. **มีกี่ภาพ + label ครบไหม** (น้อย <~500/class = อย่าเพิ่งคิด deep)
3. **feature เด่นคืออะไร** — texture? shape? สี? corner?
4. **ต้องทน scale/rotation/แสง แค่ไหน** + class imbalance (ปกติ >> ผิดปกติ?)

---

## วิธีเลือก (AI: ทำตามนี้) — forks

### A. Preprocessing — เลือกจาก "อาการของภาพ"
- contrast ต่ำ/มืดทั้งภาพ → **Histogram Equalization** (⚠️ ถ้า noisy มันขยาย noise ด้วย)
- noise ทั่วไป (Gaussian) → **smoothing (Mean/Gaussian)** (kernel ใหญ่=เบลอ=กิน edge)
- **salt & pepper** (จุดขาว-ดำ) → **Median filter** เท่านั้น (mean = เกลี่ย noise ปนค่า → พัง)
- แสงไม่สม่ำเสมอ → **normalize ก่อนเสมอ** · ลำดับ: normalize → smoothing/median → edge/feature

### B. Edge — Sobel vs Canny
- **Sobel** = เร็ว, ใช้เมื่อต้องการ gradient เป็น **feature ป้อนต่อ** (HOG, edge density)
- **Canny** = ใช้เมื่อต้องการ **เส้นบาง 1px ต่อเนื่อง** เป็นผลลัพธ์จริง (วัดขอบ/boundary)

### C. Feature / Descriptor — fork ที่ตัดสินงานทั้งหมด
| feature เด่น | ใช้ | เพราะ |
|---|---|---|
| รูปร่าง/โครงร่าง | **HOG** | จับ gradient orientation ของขอบ, เร็ว |
| เนื้อสัมผัส/ลายผิว | **GLCM** (contrast/homogeneity/energy/entropy) | จับความสัมพันธ์คู่พิกเซล = texture |
| จุดเด่น/มุม เพื่อ match-track | **Harris → SIFT/SURF** | local keypoint invariant |
- local: Harris=หา corner (scale คงที่) · **SIFT**=scale+rotation invariant แม่นสุด · **SURF**=SIFT แบบเร็ว
- ⚠️ HOG/GLCM **ไม่ invariant scale/rotation** → วัตถุหมุน/ย่อ ต้อง resize+align ก่อน

### D. Classical CV vs Deep CNN — fork แพงสุดถ้าเลือกผิด
- data น้อย + feature ชัด (shape/texture วัดได้) → **classical** (HOG/GLCM → SVM/KNN) = baseline เสมอ
- data เยอะ (พัน-หมื่น/class) + feature ซับซ้อน → **CNN**
- งานเซลล์เลือดมัก **data จำกัด + feature morphology ชัด → classical ก่อน** (ใช้ deep ที่ data น้อย = overfit)

### E. Segmentation
- **threshold** → object/background ต่างสี/ความเข้มชัด → ตามด้วย morphology + connected-component นับ
- **K-means** → รู้จำนวนกลุ่ม K, เร็ว (⚠️ ไวต่อ init/outlier) · **Mean-shift** → ไม่รู้จำนวน, รูปอิสระ (ช้า)
- **Graph-based** → ขอบเขตซับซ้อน · **CNN encoder-decoder** → มี label ราย-pixel + data เยอะ (overkill ถ้า threshold พอ)

### F. Color space — RGB vs HSV
- **RGB** → วัดความคล้ายสีแบบ Euclidean · **HSV** → เมื่อ **สีคือ criterion หลัก** (cell-stain) เพราะ Hue แยกจากความสว่าง = **ทนแสงเปลี่ยน**กว่ามาก

### เลนพิเศษ — blood smear / cell ML (classical-first)
1. **แปลง HSV** (เซลล์ย้อมสี → Hue แยกง่าย, ทนแสงกล้องจุลทรรศน์)
2. **Segment เซลล์** — threshold สี → morphology (opening/closing) → connected-component (เซลล์แตะกัน → watershed/mean-shift)
3. **สกัด feature ต่อเซลล์ = GLCM texture (chromatin) + shape (area, circularity, Hu moments)** — เซลล์ผิดปกติ (target cell/poikilocyte) อยู่ใน texture+shape
4. **ป้อน classifier** (SVM/RF) ไม่ใช่ deep ทันที (data ผิดปกติมักน้อย)
5. **จัดการ class imbalance** (ปกติ >> ผิดปกติ) ก่อนวัด accuracy

---

## กับดัก (Anti-patterns)
- **ผิด color space** — threshold สีใน RGB แล้วเพี้ยนเมื่อแสงเปลี่ยน → ใช้ **HSV** เมื่อสีคือ criterion (#1)
- **ไม่ normalize illumination** — แสงไม่สม่ำเสมอทำ feature เพี้ยนทั้ง dataset (กล้อง/มือถือคนละตัว = bias)
- **overfit ภาพชุดเล็ก** — deep บนภาพ <~500/class → จำไม่ generalize → classical ก่อน
- **leakage จาก "ภาพเยอะแต่ source เดียว"** — หลาย patch/ภาพจากคนไข้/สไลด์เดียว = data จุดเดียว → split train/test ที่ระดับ **คนไข้/สไลด์ ไม่ใช่ patch/ภาพ** ไม่งั้น test ปนกับ train → metric หลอก
- **ignore class imbalance** — เซลล์ปกติ >> ผิดปกติ → accuracy 95% แต่จับผิดปกติไม่ได้ → ดู **recall ของคลาสผิดปกติ, F1, PR-curve**
- **ใช้ deep ทั้งที่ data น้อย** — เผา compute + overfit; classical ชนะเมื่อ data จำกัด
- **median ↔ mean สลับ** — salt&pepper ต้อง median
- **HOG/GLCM กับวัตถุหมุน/ย่อ** — ไม่ invariant → align/resize ก่อน
- **เซลล์แตะกัน นับเป็น 1** — ต้อง watershed/mean-shift แยกก่อนนับ
- **Opening ↔ Closing สลับ** — Opening=Erosion→Dilation (ลบจุดเล็ก) · Closing=Dilation→Erosion (อุดรู)
- **edge/HOG บน noisy image ตรงๆ** — gradient ขยาย noise → smoothing/median ก่อนเสมอ

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT) สเมียร์/เซลล์ที่ผมพยายาม classify ติดตรง... แก้ feature โดย..."*
> - *"ภาพจากกล้องจุลทรรศน์รุ่น... มีปัญหา... ต้อง preprocess..."*

---
*ช่วยคิดเลือกเทคนิค image analysis เพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์ — งานวินิจฉัยจากภาพ (เซลล์/สเมียร์) ต้องมี MT/แพทย์ยืนยันเสมอ ไม่ใช้ผลโมเดลตัดสินคนไข้ลำพัง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: data-project-survival ═════════ -->

---
skill: data-project-survival
title: รันโปรเจกต์ data/ML ให้ไม่ล้ม (Data Project Survival · CRISP-DM judgment)
type: ADVISE               # ช่วยวางแผน/ตัดสินใจ/ประเมิน ไม่ได้รันโมเดลให้
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิด/วางแผนโปรเจกต์ data เพื่อการศึกษา ไม่ใช่ data scientist แทน — ผลและความปลอดภัย (โดยเฉพาะงานคลินิก) ต้องตรวจสอบยืนยันก่อนใช้จริง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# รันโปรเจกต์ data/ML ให้ไม่ล้ม

พาโปรเจกต์ data/ML (หรือประเมินของคนอื่น) ผ่าน **ด่านที่มักตาย** — รู้ว่าอยู่ช่วงไหน ต้องตัดสินอะไร เลี่ยงกับดักไหน

> **กฎ #1 — Everything starts with the PROBLEM, not the data:** ตอบไม่ได้ว่า "เอาไปทำอะไร วัดสำเร็จเป็นเลขอะไร" = ยังไม่ต้องแตะ data. โปรเจกต์ส่วนใหญ่ล้มที่ **ขั้นตอน** (แก้โจทย์ผิด · data แย่) ไม่ใช่ที่ algorithm
> **กับดัก #1 — Data leakage:** fit scaler/SMOTE/feature-select **ก่อน split**, หรือใช้ feature ที่รู้อนาคต → metric สวยหลอก พังจริง. กฎเหล็กข้ามทุกขั้น: **แตะ test set แค่ตอนวัดผลครั้งเดียว** ทุกอย่างที่ "เรียนจาก data" ทำบน train fold หลัง split เท่านั้น
> เลือก "โมเดล/metric ตัวไหน" ลึกๆ → ดู `ml-judgment` · "ใช้ test สถิติอะไร / N เท่าไร" → `choose-stat-test` + `sample-size-power`

> ⛔ **ก่อนเซ็นรับ/เชื่อ metric ที่สวย — ไล่ leak 4 จุดนี้ให้ครบ (พลาดจุดเดียว = เลขโกหก):**
> 1. **preprocessing ก่อน split?** impute/scale/feature-select fit บน "ทั้งชุด" → ต้องอยู่ใน pipeline ที่ fit เฉพาะ train fold
> 2. **resample ก่อน split?** SMOTE/over/under ก่อน CV → ต้องทำ "ใน train fold หลัง split" เท่านั้น
> 3. **feature รู้อนาคต / target-leak?** ค่าที่จะมีก็ต่อเมื่อรู้คำตอบแล้ว (เช่น เวลา/สถานะที่เกิดหลังตัดสิน) → **ตัดทิ้ง แม้ feature importance สูง** (สูงเพราะมันรั่ว)
> 4. **validate ข้ามประชากร/เวลา/เครื่องไหม?** ชุด/ไซต์/เครื่องเดียว → ไม่รู้ generalize, ต้องทดสอบนอกกลุ่ม
> **คาดเลขจริง:** ถ้ามี leak ตัวเลขที่ซื่อสัตย์มัก**ใกล้ baseline ง่ายๆ** (เช่น logistic เบสไลน์) มากกว่า metric ที่สวยเกิน — **gap ใหญ่ระหว่าง 'pipeline เทพ' กับ baseline = ธงแดงของ leak ไม่ใช่ความเก่ง**. variance ต่ำใน CV ก็ไม่ช่วย ถ้า leak อยู่ในทุก fold เท่ากัน

## ใช้เมื่อ
- จะเริ่ม/วางโครงโปรเจกต์วิเคราะห์ข้อมูล/ML (R2R ที่ใช้ ML, dashboard, ทำนายจากข้อมูล lab)
- ติดว่าจะทำ data-prep ท่าไหน (missing/scale/imbalance)
- ต้องประเมินคำโฆษณา "AI/ML" ของ vendor ว่าน่าเชื่อไหม

## วิธีใช้
วาง skill นี้ + เล่าโปรเจกต์/ปัญหา (หรือ claim ของ vendor) → AI ชี้ว่าอยู่ด่านไหน ต้องเลือกอะไร และกับดักที่เสี่ยง

---

## ด่าน / จุดตัดสินใจ (AI: ทำตามนี้)

### 1. อยู่ช่วงไหน + วนกลับเมื่อไหร่ (CRISP-DM วน ไม่ใช่เส้นตรง)
- ยัง **วัดความสำเร็จเป็นตัวเลขไม่ได้** → ยังอยู่ "เข้าใจปัญหา" อย่าเพิ่งโหลด data
- เจอ data ไม่ตรงกับที่คุยตอนแรก → **วนกลับ "ปัญหา ↔ data"** (จุดวนหลัก)
- โมเดลออกแล้วแต่ไม่ตอบเป้าธุรกิจ → กลับ modeling/prep ไม่ใช่ deploy
- **กฎ:** เจอข้อมูลใหม่ที่ขัดสมมติฐานเฟสก่อน = ย้อนเสมอ ห้ามดันต่อทั้งที่รู้ว่าฐานผิด

### 2. แปลง business goal → data-mining goal + success criteria (เติมไม่ครบ = ยังไม่พร้อมเขียนโค้ด)
| เป้าหมาย (ภาษาคน) | งาน (task) | เกณฑ์สำเร็จ (ตัวเลข) |
|---|---|---|
| ลด turnaround time | regression/classification | ลด median TAT 15% |
| คัดเคสเสี่ยง | classification | recall>80%, AUC>0.85 |
| จัดกลุ่มผู้ป่วย | clustering | ≥3 กลุ่ม actionable |
- เกณฑ์ต้อง **SMART** (วัดได้/มีกรอบเวลา) — "เพิ่ม efficiency" เฉยๆ = ตก
- แยก **output** (โมเดล/dashboard) ออกจาก **outcome** (ผลจริง เช่น คนไข้ปลอดภัยขึ้น)

### 3. เลือก task type จาก "รูปของ target" (ไม่ใช่จาก algorithm ที่อยากลอง)
label + กลุ่ม → **Classification** · label + ตัวเลขต่อเนื่อง → **Regression** · ไม่มี label จัดกลุ่ม → **Clustering** · "ซื้อ A มักซื้อ B" → **Association** · เลือกผิด = ผิดทั้งสาย

### 4. Missing data — วินิจฉัย "กลไก" ก่อนเลือกวิธีเติม (เลือกมั่ว = ใส่ bias)
| กลไก | เลือกใช้ |
|---|---|
| **MCAR** หายมั่ว ไม่ขึ้นกับอะไร (Little's test p≥0.05) | listwise delete (ถ้าหาย 5–10%) หรือ mean/median/mode |
| **MAR** หายขึ้นกับตัวแปร*อื่น*ที่เห็น | **Multiple Imputation** (ดีสุด) / KNN |
| **MNAR** หายขึ้นกับ*ค่าที่หายเอง* (รายได้สูงไม่ตอบ) | regression/indicator + domain knowledge (**ห้าม mean** — bias แน่) |
- missing >40% ของคอลัมน์ → ทิ้งทั้งคอลัมน์

### 5. Normalize vs Standardize (+ tree ไม่ต้อง scale)
- distance/gradient-based (KNN, K-Means, SVM, NN, regression) → **ต้อง scale** · tree-based → ไม่ต้อง
- มี bound ชัด/ไม่ normal/อยากได้ [0,1] → **Min-Max** · ใกล้ normal/มี outlier → **Z-score**
- **กฎเหล็ก:** fit scaler บน **train เท่านั้น** แล้ว transform test (fit รวม test = leakage)

### 6. เมื่อไหร่ SMOTE/resample
balanced → ไม่ต้องทำ · imbalanced+เล็ก → SMOTE/oversample · imbalanced+ใหญ่ → undersample ได้ · ไม่อยากสร้าง/ทิ้ง row → class weighting
- **กฎเหล็ก:** resample บน **train fold หลัง split เท่านั้น** (ก่อน split = test ปนของสังเคราะห์ = leakage)

### 7. ตัดสินที่ "คุณค่าธุรกิจ/คลินิก" ไม่ใช่ metric
- กลับไปเทียบเกณฑ์ข้อ 2 — accuracy สูงแต่ไม่คุ้ม/ไม่ปลอดภัย = **ไม่ผ่าน วนกลับ**
- เลือก metric ตาม cost ของความผิด (FN แพง→recall · FP แพง→precision) · แปลงเป็นเงิน **ROI=(Rev−Spend)/Spend**

### 8. Deploy: format × audience + monitor drift
- ผู้บริหาร → สรุป+ROI (PDF) · ทีมเทคนิค → รายละเอียด/reproducible · ตัดผล inconclusive ออก
- **Model drift** — โลกเปลี่ยน โมเดลเสื่อมเงียบ → วางแผน monitor + retrain ตั้งแต่ก่อน deploy

### 9. (โหมดประเมิน vendor "AI แม่น 99%") ถามให้ถูกจุด
แยก train/test ยังไง · **validate กับประชากร/คนไข้ของเราไหม** · 99% บน imbalance หรือเปล่า (ขอ recall/precision) · จัดการ drift ยังไง

---

## กับดัก (Anti-patterns)
- **ข้าม "เข้าใจปัญหา"** → แก้ผิดข้อ (อาการ: เริ่มจากโหลด dataset เลย / ตอบไม่ได้ว่าสำเร็จคือเลขอะไร) = บาปอันดับ 1
- **Solution หา problem** — "อยากใช้ AI/deep learning" แล้วค่อยหางานให้มันทำ
- **Data leakage** — fit scaler/SMOTE/feature-select ก่อน split, หรือ feature ที่รู้อนาคต → ผลปลอม พังจริง
- **Model drift** ไม่ monitor → แม่นวันแรก เสื่อมเงียบ
- **Bias ใน training data** → ขยายอคติเดิม (เพศ/พื้นที่/รายได้) เช็ค representativeness; เกี่ยว PDPA/HIPAA
- **Vanity metric / accuracy บน imbalanced** → ดู precision/recall/F1 ต่อ class
- **Over-engineering** → จูน deep net ทั้งที่ logistic regression พอ; เริ่ม baseline ง่ายก่อน
- **ดัน pipeline ต่อทั้งที่ฐานผิด** → เจอ data quality แย่/สมมติฐานผิดแล้วไม่วนกลับ (data จริงมักแย่ ~40% ตาม Gartner — เผื่อเวลา clean ไว้)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT) โปรเจกต์ data ในแล็บที่ผมเห็นล้มเพราะ data quality ตรง... แก้โดย..."*
> - *"vendor 'AI วินิจฉัย' ที่ claim เกินจริง — จุดที่ผมจับได้คือ..."*
> - *"missing แบบ MNAR ในข้อมูล lab ที่ผมเจอ คือ... จัดการโดย..."*

---
*ช่วยคิด/วางแผนโปรเจกต์ data เพื่อการศึกษา ไม่ใช่ data scientist แทน — ผลและความปลอดภัย (โดยเฉพาะงานคลินิก) ต้องตรวจสอบยืนยันก่อนใช้จริง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: db-judgment ═════════ -->

---
skill: db-judgment
title: โค้ช SQL + ออกแบบ DB — ตัดสินใจถูก + ไม่ระเบิด (SQL & DB Judgment)
type: ADVISE               # ช่วยตัดสินใจออกแบบ/เขียน query ไม่ใช่ตำรา syntax
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดออกแบบ/เขียน SQL เพื่อการศึกษา ไม่ใช่คำสั่งให้รันจริง — งานจริงควรทดสอบบน staging + backup ก่อน DELETE/UPDATE และตรวจ query plan ก่อนใช้ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช SQL + ออกแบบ DB — ตัดสินใจถูก + ไม่ระเบิด

เขียน query / ออกแบบ schema แล้วไม่แน่ใจ "ใช้ join ไหน", "ควร index มั้ย", "normalize แค่ไหน" → โค้ชนี้ช่วย **เลือกให้ถูก + ไม่ทำงานระเบิด**

> **กฎเหล็ก #1: ก่อนรัน `UPDATE`/`DELETE` ทุกครั้ง → `SELECT` ดูแถวที่จะโดน ด้วย `WHERE` ตัวเดียวกันก่อน + ครอบ transaction.** ไม่มี `WHERE` = ล้างทั้งตาราง.
> **กับดักขั้นโหด (ที่ `WHERE` มีแล้วแต่ยังพัง): `WHERE` ที่อ้าง subquery/`NOT IN` แล้ว subquery คืน `NULL` แม้แถวเดียว → ทั้งเงื่อนไขกลายเป็นกรองผิด/ไม่ match → DELETE โดนเกินหรือ 0 แถวเงียบๆ.** กฎทั่วไป: subquery ที่อาจมี `NULL` ให้ใช้ `NOT EXISTS` เสมอ และอย่าเชื่อ `WHERE` จน SELECT-preview ยืนยันจำนวนแถวตรง. (อย่างอื่น: ออกแบบ normalize เกิน/ขาด, index ผิดที่, cartesian — อยู่ด้านล่าง)

## ใช้เมื่อ
- เขียน SQL / ออกแบบ schema / จูน query ที่ช้า
- ลังเล "join ไหน", "ควร index มั้ย", "normalize ถึงไหน"
- query ช้า/ผลนับเกิน/เกือบลบข้อมูลผิด

## วิธีใช้
วาง skill นี้ + วาง query/โครง schema/ปัญหา → AI ชี้ทางเลือกที่เหมาะ + จุดที่เสี่ยงระเบิด

---

## ตัดสินใจอะไรเมื่อไหร่ (Judgment)

**ออกแบบ schema**
- **Normalize vs denormalize:** ระบบ transaction (OLTP, เขียนบ่อย) → **normalize 3NF/BCNF** (กัน update/insert/delete anomaly) · reporting/analytics (OLAP, อ่านหนัก) → **denormalize / star schema** (เร็วเพราะ join น้อย)
- **ระดับ normalize:** default **3NF** · ขึ้น **BCNF** ถ้ายังมี anomaly จาก determinant ที่ไม่ใช่ key · **หยุด over-normalize** (join เยอะเกิน = ช้า+อ่านยาก)
- **ER→relational:** entity→table, PK/FK, **M:N → junction table**, weak entity → composite key รวม parent
- **star vs snowflake:** star (fact+dim แบน) = query ง่าย/เร็ว · snowflake (dim normalize) = storage น้อย

**เขียน query**
- **JOIN ไหน:** INNER (เฉพาะที่ match ทั้งคู่) · LEFT (เก็บฝั่งซ้ายทั้งหมด + NULL ฝั่งขวา) — ถามตัวเอง "อยากเก็บ row ที่ไม่ match ไหม"
- **subquery vs JOIN:** correlated subquery มักช้า (รันต่อ row) → rewrite เป็น join · **`EXISTS` > `IN`** เมื่อ subquery ใหญ่ + ปลอดภัยกับ NULL
- **เมื่อไหร่ควร INDEX:** คอลัมน์ใน WHERE/JOIN/ORDER BY + **cardinality สูง** · **อย่า index** คอลัมน์ค่าน้อย (เพศ M/F), ตารางเล็ก, คอลัมน์เขียนบ่อย (index ทำ write ช้า) · composite index = **leftmost prefix** สำคัญ (เรียงคอลัมน์ให้ถูก)
- **WHERE vs HAVING:** WHERE กรองก่อน aggregate · HAVING กรองหลัง GROUP BY
- **query plan:** **full table scan = ธงแดง** บน table ใหญ่ (ควรเป็น index seek)

## กับดัก (Anti-patterns) — ระเบิดงานจริง
- **`UPDATE`/`DELETE` ไม่มี `WHERE`** = ล้างทั้งตาราง → `SELECT * WHERE <เงื่อนไขเดียวกัน>` ดูแถว+นับก่อนเสมอ / ครอบ transaction
- **`WHERE` มีแล้วแต่ยังพัง:** เงื่อนไขที่อ้าง `NOT IN (subquery)` แล้ว subquery มี `NULL` แม้ตัวเดียว → ทั้ง predicate กลายเป็น unknown → DELETE/UPDATE โดนเกินหรือ 0 แถวเงียบๆ → ใช้ **`NOT EXISTS`** + ยืนยันด้วย SELECT-preview
- **`SELECT *`** → ดึงเกิน + พังเมื่อ schema เปลี่ยน → ระบุคอลัมน์
- **JOIN ลืมเงื่อนไข** → **cartesian product** (row ระเบิด m×n)
- **GROUP BY:** ทุกคอลัมน์ใน SELECT ที่ไม่ใช่ aggregate ต้องอยู่ใน GROUP BY
- **COUNT หลัง JOIN** → row ซ้ำทำให้นับเกิน → `COUNT(DISTINCT ...)` หรือนับก่อน join
- **N+1 query** (loop ยิง query ทีละ row) → batch เป็น query เดียว / join
- **over-index** → write ช้าลงทุก index · index คอลัมน์ค่าน้อย cardinality = ไร้ประโยชน์
- **SQL injection** จากต่อ string → ใช้ parameterized query เสมอ
- **NULL ใน aggregate:** `AVG`/`SUM`/`COUNT(col)` ข้าม NULL เงียบๆ → รู้ว่ามี NULL ไหม
- **หลาย statement ที่ต้อง consistent** → ครอบ **transaction** (atomic)

## ตัวอย่างสาย health/lab
- "นับผู้ป่วยต่อแผนก" → GROUP BY แผนก + COUNT · ระวัง join ผล lab ซ้ำ → `COUNT(DISTINCT patient)`
- "หาคนที่ไม่เคยตรวจ X" → `NOT EXISTS` ไม่ใช่ `NOT IN`
- index `patient_id` (cardinality สูง) ✓ · อย่า index `sex` ✗

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคส SQL จริงในสายงานคุณ เช่น:
> - *"query ผล lab ที่ผมเคยนับเกินเพราะ join ซ้ำ แก้โดย..."*
> - *"schema ระบบ LIS/ข้อมูลสุขภาพ ที่ผมออกแบบ normalize ระดับ... เพราะ..."*

---
*ช่วยคิดออกแบบ/เขียน SQL เพื่อการศึกษา ไม่ใช่คำสั่งให้รันจริง — งานจริงควรทดสอบบน staging + backup ก่อน DELETE/UPDATE และตรวจ query plan ก่อนใช้ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: digital-judgment ═════════ -->

---
skill: digital-judgment
title: โค้ชชีวิตดิจิทัล — privacy/security/PDPA/ลิขสิทธิ์/ลงทุน (Digital Literacy Judgment)
type: ADVISE               # ช่วยตัดสินใจ ไม่ใช่ตำรากฎหมาย/ที่ปรึกษาการเงิน
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดเรื่องดิจิทัลเพื่อการศึกษา ไม่ใช่ที่ปรึกษากฎหมาย/การเงิน — เรื่อง PDPA จริงและการลงทุนจริง ควรตรวจกับผู้เชี่ยวชาญ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชชีวิตดิจิทัล — privacy / security / PDPA / ลิขสิทธิ์ / ลงทุน

ตัดสินใจเรื่องออนไลน์ให้ปลอดภัย + ไม่โดนหลอก — โดยเฉพาะ **จัดการข้อมูลคนไข้/ข้อมูลวิจัยตาม PDPA** ซึ่งเป็นเรื่องที่ MT ต้องเจอตรงๆ

> **VERDICT: แตะข้อมูลส่วนบุคคล (คนไข้/ผู้ใช้) = ขอ consent + แจ้งวัตถุประสงค์ก่อนเสมอ และ de-identify ก่อนแชร์/วิเคราะห์.**
> **กับดักอันดับ 1: ลบแค่ชื่อแล้วคิดว่าปลอดภัย — ยัง re-identify ได้จาก zip+เพศ+วันเกิด (k-anonymity fail).**
> (นิยาม/ตัวบทกฎหมายเป็น commodity — ที่นี่เก็บแต่ "ตัดสินใจอะไรเมื่อไหร่ + กับดักที่โดนหลอก/โดนปรับ")

## ใช้เมื่อ
- จะเก็บ/ใช้/แชร์ข้อมูลส่วนบุคคล (คนไข้/ผู้ใช้แอป) → ต้องทำตาม PDPA ยังไง
- จะ de-identify ข้อมูลก่อนวิจัย/แชร์
- ทำคอนเทนต์ (กลัวผิดลิขสิทธิ์) · ตัดสินใจ security · ประเมินการลงทุนออนไลน์ว่า scam ไหม

## วิธีใช้
วาง skill นี้ + เล่าสถานการณ์ → AI ชี้ทางเลือก + กับดักที่เสี่ยง

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Privacy / data (PDPA) — สำคัญสุดสำหรับ MT
> **Verdict: ไม่มี consent = ไม่แตะ. แชร์/วิเคราะห์ = de-identify ก่อน.**
- **เก็บ/ใช้/เปิดเผยข้อมูลส่วนบุคคล → ต้องขอ consent + แจ้งวัตถุประสงค์ก่อนเสมอ** · เก็บเท่าที่จำเป็น (data minimization) · เจ้าของข้อมูลขอลบได้ (right to erasure)
- **de-identify ก่อนใช้/แชร์เพื่อวิเคราะห์** — ระวัง **k-anonymity**: ลบชื่อแล้วยังระบุตัวได้จาก zip+เพศ+วันเกิด (เคสคลาสสิก ผู้ว่าฯ ถูก re-identify) → ต้อง generalize/suppress quasi-identifier
- เลือกเครื่องมือซ่อนตามว่า "ซ่อนจากใคร": **incognito** (แค่ไม่เก็บ history เครื่องตัวเอง) · **VPN** (ซ่อน IP จาก ISP) · **Tor** (anonymize หลายชั้น)

### Security
> **Verdict: ข้อมูลสำคัญต้องอยู่บน HTTPS เท่านั้น + password ไม่ซ้ำ.**
- **Risk = Threat × Vulnerability** → ปิดช่องโหว่ที่ threat สูงก่อน อย่าทุ่มมั่ว
- **HTTP ❌ vs HTTPS ✅** — อย่ากรอก password/บัตรบนหน้า HTTP · public wifi อย่าทำธุรกรรมการเงิน
- password ต่างกันทุกเว็บ + 2FA (เว็บการเงิน/อีเมลหลัก)

### Digital ethics / กฎหมาย (สำหรับคนทำคอนเทนต์)
> **Verdict: ไม่ใช่ของเรา/ไม่มีสิทธิ์ = อย่าโพสต์.**
- โพสต์/แชร์ → เช็ค **ลิขสิทธิ์** (เพลง/คลิป/ภาพ) · **พ.ร.บ.คอมพิวเตอร์** (ห้ามข้อมูลเท็จ/หมิ่น) · **PDPA** (อย่าเปิดข้อมูลคนอื่น/คนไข้)

### Online investment (พื้นฐาน)
> **Verdict: "การันตีผลตอบแทนสูง / ไม่มีความเสี่ยง" = scam เสมอ เดินหนี.**
- **กฎเลข 72** (72 ÷ อัตราผลตอบแทน% = ปีที่เงินทบเท่าตัว) ใช้ประเมินเร็วๆ
- ตราสารหนี้ (เสี่ยงต่ำ/ผลตอบแทนต่ำ) vs หุ้น (เสี่ยงสูง/ผลตอบแทนสูง) → เลือกตาม risk tolerance + ระยะเวลา

---

## กับดัก (Anti-patterns)
- **กรอกข้อมูลสำคัญบน HTTP / public wifi** = โดนดักได้
- **แชร์ data วิเคราะห์โดยไม่ de-identify** = ละเมิด PDPA + re-identify ได้ (k-anonymity fail)
- **ใช้ data คนไข้/ผู้ใช้โดยไม่ขอ consent** = ผิด PDPA → ปรับ + เสีย trust
- **investment ที่ "การันตีผลตอบแทนสูง / ไม่มีความเสี่ยง" = scam** (ของจริงไม่มี risk-free สูง)
- **reuse password ทุกเว็บ** → หลุดเว็บเดียวโดนหมด
- **ใช้เพลง/คลิปมีลิขสิทธิ์ในคอนเทนต์** → โดน strike/ลบ/ฟ้อง
- **คลิก link/ดาวน์โหลดจาก email แปลก** (phishing)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT) ตอน de-identify ข้อมูลคนไข้เพื่อทำวิจัย ผมระวัง quasi-identifier ตรง... เพราะ..."*
> - *"consent flow ที่ รพ./แอป เราใช้จริง คือ..."*

---
*ช่วยคิดเรื่องดิจิทัลเพื่อการศึกษา ไม่ใช่ที่ปรึกษากฎหมาย/การเงิน — เรื่อง PDPA จริงและการลงทุนจริง ควรตรวจกับผู้เชี่ยวชาญ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: explain-simply ═════════ -->

---
skill: explain-simply
title: อธิบายให้เข้าใจง่ายแบบเด็ก ป.3 (Explain Simply)
type: ADVISE               # ปรับวิธีอธิบาย ไม่ได้รันอะไร
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดวิธีอธิบายให้เข้าใจง่ายเพื่อการศึกษา ไม่ใช่คำแนะนำทางการ — เรื่องการแพทย์/สำคัญ ต้องง่ายโดยไม่ผิด ควรตรวจว่าเนื้อหายังถูกต้อง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# อธิบายให้เข้าใจง่ายแบบเด็ก ป.3

เปลี่ยนเรื่องยาก/ศัพท์เทคนิค → ภาษาที่ **เด็ก ป.3 เข้าใจ** โดยไม่ผิดและไม่ดูถูก

> **กฎ #1: ง่ายได้ แต่ "ผิดไม่ได้" — ถ้าต้องเลือกระหว่างง่ายกับถูก เลือกถูกเสมอ.** "อธิบายแบบ ป.3" = ทำ "ทาง" ให้โล่ง ไม่ใช่ทำคนฟังโง่.
> **กับดักตัวจริง (ที่ AI อ่อนๆ พลาด):** ตัดทอนแล้ว *ฟังดูถูก* แต่แอบทิ้ง **เงื่อนไข/ข้อยกเว้นที่เปลี่ยนการกระทำ** ("ปกติ... ยกเว้น... เฉพาะเมื่อ...") — เงื่อนไขที่ถ้าหายไปคนฟัง **ทำผิด** ห้ามตัด. และ analogy ที่ลากความหมายผิดติดมาด้วย (false implication) ก็คือ "ผิด" เหมือนกัน.

## ใช้เมื่อ
- อ่านคำตอบ/เอกสารแล้วงง อยากให้อธิบายใหม่ให้เข้าใจ
- ต้องอธิบายให้ **คนไข้ / คนในบ้าน / คนนอกสาย** เข้าใจ
- สอนน้อง/นักศึกษา

## วิธีใช้
วาง skill นี้ + พิมพ์ *"อธิบาย [เรื่องนี้] ให้เข้าใจง่ายแบบเด็ก ป.3"* หรือวางข้อความยากๆ ที่อ่านแล้วงง

---

## วิธีอธิบาย (AI: ทำตามนี้)

### 1. ตัดศัพท์ยากออก (หรืออธิบายมันก่อน)
- เจอศัพท์เทคนิค (เช่น agglutination, reference range, sensitivity) → เปลี่ยนเป็นคำธรรมดา หรืออธิบายด้วยคำง่ายๆ **ครั้งเดียว** แล้วค่อยใช้

### 2. ใช้การเปรียบเทียบจากชีวิตจริง
- เทียบกับสิ่งที่ผู้ฟัง **รู้จักอยู่แล้ว** (อาหาร, LINE, บ้าน, การจราจร) — เลือกอันที่เขาคุ้น ไม่ใช่ที่เราคุ้น
- บอกด้วยว่าเปรียบเทียบ **"เหมือนตรงไหน"** และ **"ไม่เหมือนตรงไหน"** (analogy ทุกอันมีจุดที่พัง อย่าให้เข้าใจผิด)

### 3. ประโยคสั้น 1 ประโยค = 1 ความคิด
- ~10-15 คำต่อประโยค · เรียงทีละสเต็ป ไม่อัดรวด

### 4. รูปธรรมมาก่อนนามธรรม
- ยก **ตัวอย่างจริงก่อนนิยาม** ("เช่น..." มาก่อน "คือ...")

### 5. เช็คว่าเข้าใจไหม
- จบด้วย *"ตรงไหนยังไม่ชัดบอกได้"* — อย่าเทยาวแล้วจบเฉยๆ

### 6. ง่าย แต่ห้ามผิด (กฎ #1 — สำคัญสุด)
- ทำให้ง่ายได้ **แต่อย่าง่ายจนกลายเป็นข้อมูลผิด** → ถ้าเรื่องไหนตัดทอนแล้วจะเข้าใจผิด ให้คงไว้ + อธิบายเพิ่ม
- **เทสต์ตัวเอง:** ถ้าคนฟังเชื่อคำอธิบายง่ายๆ นี้ 100% แล้ว **ตัดสินใจหรือทำตามได้ถูกไหม?** ถ้าเงื่อนไข/ข้อยกเว้นที่หายไปทำให้เขาทำผิด → คงเงื่อนไขนั้นไว้ ห้ามตัด
- **อย่าแปลงคำกำกวมเป็นคำชี้ขาด** — "มักจะ/ส่วนใหญ่/ประมาณ" ห้ามกลายเป็น "เสมอ/ทุกครั้ง/แน่นอน" เพราะความง่าย
- **ไม่ดูถูก** — ป.3 = เคลียร์ ไม่ใช่ทำเสียงเด็ก/พูดเหมือนคนฟังโง่

---

## กับดัก (Anti-patterns)
- **ง่ายจนผิด** — ตัดข้อมูลสำคัญทิ้งจนความหมายเพี้ยน (อันตรายในเรื่องแพทย์)
- **เปรียบเทียบมั่ว** — ใช้ analogy ที่ผู้ฟังก็ไม่รู้จัก หรือทำให้เข้าใจผิดมากกว่าเดิม
- **ยังมีศัพท์ยากแฝง** — คิดว่าง่ายแล้วแต่ยังมีคำเทคนิคหลงเหลือ
- **ดูถูก/ทำเสียงเด็ก** (condescending) — ทำให้คนฟังหมั่นไส้
- **อธิบายยาวเกิน** — ง่าย ≠ ยาว; สั้นและตรงดีกว่า

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมการเปรียบเทียบที่ใช้ได้ผลจริงในสายงานคุณ เช่น:
> - *"(MT) อธิบายหมู่เลือด/ผลตรวจให้คนไข้ ผมเทียบกับ... แล้วเขาเข้าใจเลย"*
> - *"เรื่องที่คนชอบเข้าใจผิดถ้าอธิบายง่ายเกิน คือ... ต้องระวัง..."*

---
*ช่วยคิดวิธีอธิบายให้เข้าใจง่ายเพื่อการศึกษา ไม่ใช่คำแนะนำทางการ — เรื่องการแพทย์/สำคัญ ต้องง่ายโดยไม่ผิด ควรตรวจว่าเนื้อหายังถูกต้อง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: finance-judgment ═════════ -->

---
skill: finance-judgment
title: โค้ชการเงิน/ลงทุน/ธุรกิจ — ตัดสินใจเงินไม่ให้พลาด (Finance & Investing Judgment)
type: ADVISE               # ช่วยคิดกรอบตัดสินใจ ไม่ใช่คำแนะนำการลงทุน
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดกรอบเรื่องเงิน/ลงทุน/ธุรกิจ เพื่อการศึกษา ไม่ใช่คำแนะนำการลงทุน/การเงินจากที่ปรึกษาที่มีใบอนุญาต — การลงทุน/ธุรกิจมีความเสี่ยง ผลตอบแทนไม่แน่นอน ต้องตรวจสอบเองและปรึกษาผู้เชี่ยวชาญก่อนตัดสินใจ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชการเงิน/ลงทุน/ธุรกิจ — ตัดสินใจเงินไม่ให้พลาด

ตัดสินใจเรื่องเงิน/ลงทุน/ธุรกิจ — "ทำอะไรเมื่อไหร่ + พลาดตรงไหนเสียเงิน" ไม่ใช่ท่องนิยาม P/E / ROE / งบ 5 ฉบับ (= commodity ดูตำรา) · สำหรับ MT ยุคใหม่ที่ต้องจัดการเงิน/ทำธุรกิจ/ลงทุนเอง

> **กฎข้อ 1 (ตอบก่อนทุกอย่าง):** "การันตีผลตอบแทน / risk-free แต่ผลตอบแทนสูง" = **scam ปฏิเสธทันที** ไม่ต้องคำนวณต่อ — High Risk High Return เป็นกฎธรรมชาติ.
> **กับดักตัวจริง (ที่คนพลาด):** scam รุ่นเก่ง **ไม่ป่าวประกาศว่าการันตี** — มันแต่งตัวให้ดูถูกกฎหมาย (มี track record สวย, ตัวเลข "audited", ผลตอบแทน "นิ่งสม่ำเสมอทุกเดือน"). เทสต์จริงคือ **เงินปันผลมาจากไหน + ถอนได้ทันทีไหม** ไม่ใช่คำโฆษณา → จ่ายจากเงินรายใหม่ (ไม่ใช่กำไรดำเนินงานจริง) หรือ "ถอนยาก/ต้องชวนต่อ" = Ponzi ต่อให้ดูหรูแค่ไหน.
> **กฎข้อ 2:** เงินไม่ใช่ "ลงทุนตัวไหนดี" ก่อน — แต่คือ **ลำดับ** (เคลียร์หนี้แพง → เงินสำรอง → ค่อยลงทุน) + กับดัก sunk-cost / ลืมงบกระแสเงินสด (CFO).

## ใช้เมื่อ
- มีเงินก้อน/เงินเดือนเหลือ → ลงทุน/เก็บ/ใช้หนี้ อันไหนก่อน
- เลือก asset/vehicle (หุ้น/กองทุน/ตราสารหนี้/ทอง/เงินฝาก) ตาม horizon + risk
- อ่านงบบริษัท (ลงทุนหุ้น/ประเมินคู่ค้า) → ดู ratio ไหน
- ตัดสินใจธุรกิจ: เริ่ม/ไม่เริ่ม, ขยาย/พับ, pivot เมื่อไหร่
- เจอโฆษณา/คอร์ส/ดีล "ลงทุนนี้" → เชื่อได้ไหม / scam ไหม

## วิธีใช้
วาง skill นี้ + เล่าสถานการณ์เงิน/ธุรกิจ → AI ชี้กรอบตัดสินใจ + กับดัก (ไม่ชี้นำซื้อตัวไหน/เท่าไร)

---

## ก่อนเอาเงินไปเสี่ยง — บันได 3 ขั้น (ข้ามขั้น = TRAP)
1. **หนี้ดอกแพงเคลียร์ก่อน** (บัตรเครดิต/นอกระบบ ดอก >15% = "ลงทุน" ที่ผลตอบแทนติดลบแน่นอนถ้าไม่ปิด)
2. **เงินสำรองฉุกเฉิน 3–6 เดือน** (รายได้ไม่นิ่ง/freelance/มีคนต้องดูแล → 6–12 เดือน)
3. **มีประกัน/เป้าหมายชัด** แล้วค่อยเอาเงินส่วนเกินไปลงทุน
> ลงทุนทั้งที่ยังมีหนี้บัตร/ไม่มีสำรอง = เจ๊งตอนฉุกเฉินต้องขายของถูกๆ

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — เลือก asset/vehicle ตาม horizon + risk (ไม่ใช่ตาม "ใครว่าดี")
ถามก่อน: **เงินนี้ใช้เมื่อไหร่?**
- **<1–2 ปี (จะใช้แน่):** เงินฝาก/กองตลาดเงิน/ตราสารหนี้สั้น — **ห้ามหุ้น** (เด้งลงตอนต้องใช้ = ขายขาดทุน)
- **3–7 ปี:** ผสม หุ้น/กองหุ้น + ตราสารหนี้ ตาม risk tolerance
- **>7–10 ปี (เกษียณ/เป้ายาว):** เอียงหุ้น/กองดัชนี (เวลายาว = ทนผันผวนได้ + compounding)
- **vehicle:** มือใหม่/ไม่มีเวลา → กองทุนดัชนี/DCA (กระจายอัตโนมัติ ค่าธรรมเนียมต่ำ) · หุ้นรายตัว = ต้องอ่านงบเป็น + เสี่ยงกระจุก · ตราสารหนี้ = เสี่ยงต่ำ/ผลตอบแทนต่ำ
> หลัก: horizon กำหนด asset ก่อน risk — เงินสำรองห้ามอยู่ในหุ้น แม้ตลาดขาขึ้น

### Fork 2 — อ่านงบ: ratio ไหนตอบคำถามไหน (อย่าดูตัวเดียว)
| อยากรู้ | ดู | สัญญาณแย่ |
|---|---|---|
| จ่ายหนี้สั้นไหวมั้ย (liquidity) | Current ratio, Quick ratio | <1 = สภาพคล่องตึง |
| หนี้ท่วมมั้ย (solvency) | D/E, Interest coverage | D/E สูงผิดอุตสาหกรรม, coverage <2 |
| ทำกำไรเก่งมั้ย | Gross/Net margin, ROE, ROA | margin หดต่อเนื่อง |
| โตจริงหรือโตบนกระดาษ | **งบกระแสเงินสด (CFO)** | กำไรโตแต่ CFO ติดลบ 🚩 |
- **TRAP ใหญ่: ดูแต่งบกำไรขาดทุน ลืมงบกระแสเงินสด** — กำไร (accrual) ปลอมได้ด้วย accounting; **เงินสดจากการดำเนินงาน (CFO) โกหกยากกว่า** → กำไรโต + CFO ติดลบ = ระวัง (ลูกหนี้/สต็อกบวม)
- เทียบ **ในอุตสาหกรรมเดียวกัน + เทียบ trend ตัวเอง** ไม่ใช่ค่าลอยๆ

### Fork 3 — valuation แพง/ถูก (อย่าซื้อเพราะ "ราคาลง = ถูก")
- **P/E เทียบ:** ตัวเอง (อดีต) + คู่แข่ง + ตลาด — สูงกว่ามาก = แพง/คาดโตสูง (ผิดหวัง=ร่วง)
- **หุ้น cyclical (วัฏจักร) ดู P/E ตรงๆ ไม่ได้** — P/E ต่ำตอนกำไรพีค = กับดัก (กำไรกำลังจะลง)
- "ราคาตก 50%" ≠ ถูก ถ้าพื้นฐานพัง → ดู **ทำไมตก** ก่อน (value vs value-trap)

### Fork 4 — หนี้ดี vs หนี้เลว (กู้/ไม่กู้)
- **หนี้ดี = สร้างสินทรัพย์/รายได้** (กู้ทำธุรกิจที่ ROI > ดอกเบี้ย, การศึกษาที่เพิ่มรายได้)
- **หนี้เลว = สร้างภาพ/เสื่อมค่า** (ผ่อนของฟุ่มเฟือย, บัตรหมุน) — ดอกกินก่อนได้ประโยชน์
- เกณฑ์: **ผลตอบแทน/ประโยชน์ที่คาด > ดอกเบี้ย + เผื่อพลาด** ถึงกู้; leverage เกินตัว = เจ๊งตอน cashflow สะดุด

### Fork 5 — ธุรกิจ: go/no-go + เมื่อไหร่ pivot
- **ก่อนสร้าง: validate ความต้องการก่อนลงแรง/เงิน** — มีคนจ่ายจริงไหม (pre-sell/MVP/คนใช้ฟรีแล้วยอมจ่าย) · **business plan สวยหรู = enemy #1** (วางแผน 50 หน้าแต่ไม่มีลูกค้า = เสียเวลา)
- **go เมื่อ:** มี demand signal จริง + ต้นทุนเริ่มต่ำ + ทดสอบได้เร็ว
- **pivot เมื่อ:** assumption หลักถูกพิสูจน์ว่าผิด (คนไม่จ่าย/ตลาดไม่มี) — **อย่าติด sunk cost** ("ลงไปเยอะแล้วเสียดาย" = เผาเงินต่อ); เงิน/เวลาที่จมไปแล้วไม่ใช่เหตุผลทำต่อ
- ก่อนรายได้แรก: เคลียร์เรื่องสัญญาจ้าง/ภาษี/PDPA/จดทะเบียนให้เรียบร้อยก่อน

### Fork 6 — เป้าหมายเงิน: ตั้งให้ทำได้จริง (คำนวณย้อนกลับ)
- **SMART + คำนวณย้อนกลับ:** เป้า (เช่น เงินสำรอง X บาท ภายใน Y เดือน) → หารจำนวนเดือน → ต้องออม Z/เดือน → จริงไหมกับรายได้? ไม่จริง → ปรับเป้า/เพิ่มรายได้/ยืดเวลา
- **กฎ 72** ประเมินเร็ว: 72 ÷ %ผลตอบแทน = ปีที่เงินทบเท่าตัว (เช็คความสมจริงของเป้าลงทุน)

### Fork 7 — คำแนะนำ/ดีลลงทุนนี้ เชื่อได้ไหม (fact vs opinion vs scam)
- **แยก Fact (ตรวจสอบได้) vs Opinion (ความเห็น/เชียร์)** — โบรกเชียร์ซื้อ = opinion + มี conflict of interest
- **🚫 "การันตีผลตอบแทนสูง / ไม่มีความเสี่ยง / ผลตอบแทนแน่นอนสูงผิดปกติ" = scam** (High Risk High Return เป็นกฎ; risk-free สูง = ไม่มีจริง) — Ponzi/แชร์ลูกโซ่/คริปโตการันตี
- **เวอร์ชันยากที่คนพลาด — Ponzi แต่งตัวเนียน:** ไม่ได้พูดคำว่า "การันตี" แต่โชว์ผลตอบแทน "นิ่งสม่ำเสมอ" + track record สวย + ตัวเลข "audited" + ดูจดทะเบียนถูกกฎหมาย. **อย่าตัดสินจากภาพลักษณ์** — เทสต์แกน 2 ข้อ: **(1) เงินจ่ายมาจากไหน** (กำไรดำเนินงานจริง หรือเงินรายใหม่/ต้องชวนคนต่อ = Ponzi) **(2) ถอนเงินคืนได้ทันทีตามจริงไหม** (ถอนยาก/บ่ายเบี่ยง = สัญญาณพัง). ผลตอบแทน "นิ่งเกินจริง" (ตลาดผันผวนแต่ผลตอบแทนเรียบ) = ธงแดงในตัวมันเอง
- บทเรียน: Theranos (เชื่อ story ไม่เชื่อ data), Fyre (hype > สาร), Madoff (ดูหรู/นิ่งสม่ำเสมอ = หลอกได้นานสุด) → **ขอ data/track record ที่ audit ได้จริง + ทดสอบถอนเงิน ก่อนเชื่อ narrative**

### Fork 8 — เลนส์เศรษฐศาสตร์ (ต้นทุน/ราคา/เงินเฟ้อให้ลึกขึ้น)
- **Opportunity cost:** ต้นทุนจริง = มูลค่าทางเลือกที่ดีที่สุดที่สละไป (ไม่ใช่แค่เงินที่จ่าย) · **"ไม่ทำอะไร" ก็มีต้นทุน** (เงินสดถือเฉยๆ = เสียผลตอบแทน + โดนเงินเฟ้อกิน) · เวลาเป็นทรัพยากร scarce สุด → จัดลำดับงาน/ดีล ROI สูงก่อน
- **Marginal thinking:** ตัดสินที่ "หน่วยถัดไป" (เพิ่มอีก 1 คุ้มไหม — marginal benefit > marginal cost) ไม่ใช่ค่าเฉลี่ยรวม
- **Elasticity → ตั้งราคา:** สินค้า/บริการ **inelastic** (ไม่มีของแทน/lock-in) = ขึ้นราคาได้ รายรับเพิ่ม · **elastic** (มีของแทน) = ขึ้นราคา รายรับตก → อย่าแข่งราคา · ตลาดผู้เล่นน้อยราย (oligopoly) = แข่ง service/คุณภาพ ไม่ใช่ตัดราคา (ดู `marketing-judgment`)
- **Real vs Nominal + ดอกเบี้ยแท้จริง:** ดู **Real** (ปรับเงินเฟ้อ) ไม่ใช่ Nominal · **ดอกเบี้ยแท้จริง = ดอกเบี้ย − เงินเฟ้อ** → ฝาก 2% เงินเฟ้อ 2.5% = **เงินจนลง 0.5%/ปี** (เหตุผลที่เงินสดส่วนเกิน buffer ควรไปสินทรัพย์ชนะเงินเฟ้อ)

---

## กับดัก (Anti-patterns) — ที่ดูดเงินบ่อยสุด
- 🚫 **"การันตีผลตอบแทน" = scam** — ไม่มี risk-free สูง; เวอร์ชันยาก = Ponzi แต่งตัวเนียน (ผลตอบแทนนิ่งเกินจริง + track record สวย) → เช็ค "เงินมาจากไหน + ถอนได้จริงไหม" ไม่ใช่ภาพลักษณ์ (ดู `digital-judgment` ด้วย)
- 🚫 **ลงทุนทั้งที่มีหนี้ดอกแพง/ไม่มีเงินสำรอง** — ข้ามขั้นบันได → เจ๊งตอนฉุกเฉิน
- 🚫 **ดูแต่กำไร ลืมงบกระแสเงินสด (CFO)** — กำไรปลอมได้ เงินสดโกหกยาก
- 🚫 **sunk-cost ไม่ยอม pivot/หยุด** — "ลงไปเยอะแล้ว" ไม่ใช่เหตุผลทำต่อ; ตัดสินจากอนาคต ไม่ใช่อดีตที่จมไปแล้ว
- 🚫 **leverage เกินตัว** — กู้บนสมมติฐานดีที่สุด; cashflow สะดุด = ผิดนัด
- 🚫 **เชื่อ opinion ว่าเป็น fact** — เชียร์หุ้น/คอร์สรวยเร็วมี conflict of interest; ขอหลักฐาน audit ได้
- 🚫 **business plan แทน validation** — แผนสวยแต่ไม่มีลูกค้าจ่ายจริง = เสียเวลา/เงิน
- 🚫 **เอาเงินใช้ระยะสั้นไปลงหุ้น** — horizon ผิด → ต้องขายตอนตลาดลง
- 🚫 **ซื้อเพราะ "ราคาลงเยอะ = ถูก"** — value trap; ดูว่าพื้นฐานพังไหมก่อน
- 🚫 **ลืม opportunity cost** — คิดต้นทุนแค่เงินที่จ่ายจริง; "ไม่ทำ/ถือเงินสดเฉยๆ" ก็มีต้นทุน
- 🚫 **ดู Nominal ว่าโต / ดอกเบี้ยฝากเป็นบวก = เงินงอก** — ต้องดู Real + ดอกเบี้ยแท้จริง (เงินเฟ้อสูงกว่า = จนลงเงียบๆ)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"ครั้งที่ผมเกือบโดน scam ลงทุน จับได้เพราะ..."*
> - *"ตอนตัดสินใจ pivot/พับธุรกิจ สัญญาณที่ทำให้รู้ว่าต้องหยุด คือ..."*

---
*ช่วยคิดกรอบเรื่องเงิน/ลงทุน/ธุรกิจ เพื่อการศึกษา ไม่ใช่คำแนะนำการลงทุน/การเงิน — มีความเสี่ยง ปรึกษาผู้เชี่ยวชาญก่อนตัดสินใจ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: financial-statement-judgment ═════════ -->

---
skill: financial-statement-judgment
title: โค้ชอ่านงบการเงิน — อ่านงบ 5 ฉบับ + จับ window-dressing (Financial Statement Reading Judgment)
type: ADVISE               # ช่วยอ่าน/จับสัญญาณงบ ไม่ใช่ตำราบัญชี
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดอ่านงบการเงินเพื่อการศึกษา ไม่ใช่คำแนะนำการลงทุน/บัญชีจากผู้มีใบอนุญาต — ตัวเลข/นโยบายบัญชีต้องตรวจกับงบจริง + ผู้สอบบัญชี/ผู้เชี่ยวชาญก่อนตัดสินใจ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชอ่านงบการเงิน — อ่านงบ 5 ฉบับ + จับ window-dressing

อ่านงบบริษัท (ลงทุน/ประเมินนายจ้าง/คู่ค้า) ให้เห็น "ตัวจริง" — อ่านงบไหนก่อน · กำไรของจริงหรือกระดาษ · เล่ห์บัญชีซ่อนตรงไหน ไม่ใช่ท่องนิยาม P/E ROE (= commodity ดูตำรา)

> 🎯 **กฎ #1: อย่าตัดสินจากกำไรสุทธิ — ดู CFO (เงินสดดำเนินงาน) ก่อนเสมอ.** กำไร (accrual) แต่งได้ด้วยปลายปากกา เงินสดโกหกยากกว่ามาก → **กำไรโต แต่ CFO ติดลบ/ทรงตัว = ธงแดง** (กำไรเป็นกระดาษ ไม่ใช่เงินจริง).
> 🚩 **กับดัก #1: "auditor ผ่าน (unqualified) = ไม่มีโกง" — ผิด.** auditor ไม่ได้มีหน้าที่หลักจับฉ้อฉล + เล่ห์ส่วนใหญ่ "ถูกกฎ" (ยืดอายุค่าเสื่อม/ตั้งค่าเผื่อต่ำ/ดันรายได้ปลายงวด) ตัวจริงซ่อนใน **หมายเหตุประกอบ** ไม่ใช่หน้างบ → **substance over form** เสมอ.
>
> นี่คือชั้น **"อ่านงบให้เป็น"** — ส่วน **ตัดสินใจ** (ลงทุน/ไม่, ratio→go/no-go, valuation แพง-ถูก, scam, go/pivot ธุรกิจ) อยู่ใน `finance-judgment` · ประเมินบริษัทเป็นลูกค้า/นายจ้าง คู่กับ `crm-judgment`/`ivd-sales-judgment`

## ใช้เมื่อ
- อ่านงบบริษัท (จะลงทุน/สมัครงาน/ขายเชื่อ) แล้วไม่รู้ดูอะไรก่อน
- กำไรสวยแต่สงสัยว่าจริงไหม · หาสัญญาณแต่งงบ
- เทียบ 2 บริษัท / อ่านงบรวม vs งบเดี่ยว

## วิธีใช้
วางตัวเลข/รายการในงบ (หรือเล่าสถานการณ์) → AI ชี้ลำดับอ่าน + คุณภาพกำไร (เทียบ CFO) + red flag

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — งบ 5 ฉบับ + อ่านอะไรก่อน
| งบ | ตอบ | เวลา |
|---|---|---|
| **ฐานะการเงิน (งบดุล)** | มีอะไร/หนี้ใคร/เหลือของเจ้าของเท่าไร | ภาพนิ่ง ณ จุด |
| **กำไรขาดทุนเบ็ดเสร็จ** | งวดนี้ได้/ขาดทุนเท่าไร | ช่วงเวลา |
| **เปลี่ยนแปลงส่วนผู้ถือหุ้น** | ส่วนเจ้าของเพิ่ม/ลดจากอะไร (ปันผล/เพิ่มทุน/ซื้อหุ้นคืน) | ช่วงเวลา |
| **กระแสเงินสด** | เงินสดจริงเข้า-ออกจากไหน | ช่วงเวลา |
| **หมายเหตุประกอบ** | นโยบายบัญชี + related-party + contingent | — |
- **ลำดับอ่านจริง:** (1) **audit opinion + นโยบายบัญชี** (ไม่ใช่ "unqualified" = ธงแดงก่อนดูเลข; ⚠️ auditor ไม่ได้มีหน้าที่หลักจับโกง) → (2) **CFO ก่อนกำไร** → (3) ฐานันดรกำไร → (4) งบดุล/working capital → (5) ส่วนผู้ถือหุ้น (dilute?) → (6) กลับไปหมายเหตุ (related-party/หนี้นอกงบ)

### Fork 2 — ฐานันดรกำไร: อ่านบนลงล่าง "กำไรหายชั้นไหน"
- รายได้ขาย − ต้นทุน = **กำไรขั้นต้น** (อำนาจตั้งราคา/ต้นทุน) − SG&A = **operating** (เก่งบริหาร) − ดอกเบี้ย/ภาษี = **กำไรสุทธิ** ± OCI = เบ็ดเสร็จรวม
- หดตั้งแต่ gross = ปัญหาแกนธุรกิจ · gross ดีแต่ net แย่ = ดอกเบี้ย/SG&A บวม
- ⚠️ **แยก core ออกจาก one-off:** กำไรจากขายสินทรัพย์/อัตราแลกเปลี่ยน/discontinued = "ลาภลอย" นับเป็นอนาคตไม่ได้ — net โตเพราะ "รายได้อื่น" ไม่ใช่ยอดขาย = ไม่ยั่งยืน
- ⚠️ **รับรู้รายได้ = เกณฑ์คงค้าง** (ลงเมื่อเกิด ไม่รอเงินเข้า) → ของที่ลูกค้าคืนได้แต่รับรู้เต็มจำนวน = ดันยอดปลายงวด → เทียบ AR (Fork 3)

### Fork 3 — งบดุล: ค่าเสื่อม/ตีราคา/สินค้า/ลูกหนี้ (จุดบิดเลขมากสุด)
- **PP&E = ราคาทุน − ค่าเสื่อมสะสม − ด้อยค่า** · ⚠️ **book value ≠ ราคาตลาด** (ค่าเสื่อม = ปันส่วนต้นทุน ไม่ใช่วัดราคา)
- ⚠️ **ค่าเสื่อม: บริษัทประมาณ "อายุใช้งาน + มูลค่าซาก" เอง** → ยืดอายุ/เพิ่มซาก = ค่าเสื่อมลด = **กำไรพอง** · ที่ดินไม่คิดค่าเสื่อม (แต่ด้อยค่าได้)
- ⚠️ **ตีราคาใหม่ (revaluation):** ตีเพิ่ม → เข้า **OCI ไม่ใช่กำไรสุทธิ** (กำไรกระดาษ); ตีลดเกินส่วนเก่า → กระแทกกำไรสุทธิ (asymmetry)
- ⚠️ **ด้อยค่า/ค่าเผื่อหนี้สงสัยจะสูญ ตั้งน้อยผิดปกติ = สินทรัพย์ปลอม** (ลูกหนี้/สต็อกเก็บไม่ได้แต่ไม่ตัด) → เทียบ trend + คู่แข่ง
- **สินค้า: FIFO vs ถัวเฉลี่ย → กำไรคนละตัว** ในช่วงราคาผันผวน → เทียบ 2 บริษัทต้องดูนโยบายบัญชีในหมายเหตุก่อน
- **provision (ประมาณการหนี้สิน):** ตั้งต่ำ = ซ่อนภาระ; ตั้งสูงปีนี้แล้วกลับรายการปีหน้า = ปั้นกำไร ("cookie jar reserve")
- **สินทรัพย์ไม่มีตัวตน (intangible):** มีอายุ (สิทธิบัตร/ลิขสิทธิ์/ซอฟต์แวร์) → **"ตัดจำหน่าย" (amortize)** ไม่ใช่ค่าเสื่อม · **goodwill (ไม่มีอายุ)** → ไม่ตัด แต่ **test ด้อยค่าทุกปี** → ⚠️ goodwill ก้อนโตจากซื้อกิจการแพง = **ระเบิดเวลา impairment ก้อนใหญ่** รออยู่

### Fork 4 — ส่วนผู้ถือหุ้น + OCI recycling (แยกกำไรจริงจากกระดาษ)
- 4 ก้อน: ทุนเรือนหุ้น · ส่วนเกินมูลค่าหุ้น · **กำไรสะสม** (แหล่งจ่ายปันผล) · OCI สะสม
- **หุ้นซื้อคืน (treasury):** ⚠️ ดัน EPS/ราคาหุ้นทั้งที่ธุรกิจไม่โต = แต่งตัวเลข · **dilution:** ออกหุ้นเพิ่ม → ผู้ถือเดิมถูกลดสัดส่วน → กระทบ EPS/P/E
- ⚠️ **OCI = รายการ "ยังไม่เกิดจริง"** (ตีราคา/FX/ตราสารวัดมูลค่ายุติธรรมผ่าน OCI) ไม่ใช่เงินที่ธุรกิจหาได้ → **ดู "กำไรสุทธิ" ก่อน OCI เสมอ** · เบ็ดเสร็จรวมสูงแต่กำไรสุทธิทรงตัว = คุณภาพไม่ได้ดีขึ้น
- ⚠️ **เวียนกำไร (recycle) ตาม TFRS 9 (ใช้ไทยปี 2563) — ไม่ใช่ทุกตัว recycle:** *ตราสารหนี้ FVOCI* ตอนขายจริง → กำไรสะสมใน OCI ถูกย้ายเข้ากำไรสุทธิ "ครั้งเดียว" (recycle ได้ → one-off อย่านึกว่า operation เก่งขึ้น) · *ตราสารทุนที่เลือกวัด FVOCI* → **ไม่ recycle** ค้างใน OCI/โอนเข้ากำไรสะสม · *FVTPL (เพื่อค้า)* → เข้ากำไรสุทธิทันที (เปลี่ยน classification เพื่อย้ายกำไร = ธงแดง)

### Fork 5 — งบกระแสเงินสด: CFO = ตัวจริง + อ่าน 3 หมวดเป็น pattern
- 3 หมวด: **CFO** (ดำเนินงาน) · **CFI** (ลงทุน) · **CFF** (จัดหาเงิน)
- **CFO ทางอ้อม:** กำไรสุทธิ → **บวกกลับรายการไม่ใช่เงินสด** (ค่าเสื่อม/ด้อยค่า) → ปรับ working capital → หักดอกเบี้ย/ภาษีจ่ายจริง · ⚠️ ค่าเสื่อมสูง ≠ เงินสดหาย (บวกกลับ); แต่กำไรที่มาจากบวกกลับ/WC ล้วน ≠ ยอดขายโตจริง
- **อ่าน sign เป็น pattern ไม่ใช่ทีละตัว:** CFI ติดลบเพราะซื้อเครื่อง = ดี · CFF บวกเพราะกู้ ≠ ดีอัตโนมัติ
- 🚩 **pattern อันตราย: CFO ติดลบ + CFI/CFF บวก** = ธุรกิจหาเงินเองไม่ได้ ต้องขายสินทรัพย์/กู้ประคอง = ใกล้วิกฤตสภาพคล่อง

### Fork 6 — หมายเหตุ + งบรวม + checklist window-dressing
- **หมายเหตุ = ตัวจริง:** นโยบายบัญชี (ค่าเสื่อม/FIFO) · **related-party** · หนี้ค้ำประกัน/ฟ้องร้อง/contingent · เงินกู้ยาว → อ่านนโยบายก่อนเทียบ 2 บริษัท
- **งบเดี่ยว vs งบรวม (consolidated):** บริษัทแม่คุมลูก → งบรวม + แยก **NCI (minority)** ออกจากกำไรของผู้ถือหุ้นแม่ · บริษัทร่วม → equity method (ส่วนแบ่งกำไรบรรทัดเดียว) · ⚠️ อย่าเอางบเดี่ยวเทียบงบรวม
- 🚩 **window-dressing checklist:** ยืดอายุ/เพิ่มซาก PP&E · ตีราคาขึ้น · ไม่ย้ายเงินกู้ยาวครบกำหนดมาหนี้สั้น (current ratio ลวง) · ตั้งค่าเผื่อ/ด้อยค่า/provision ต่ำ · เปลี่ยนวิธีสต็อก/classification · กลับ provision เก่า · related-party เยอะ · ดันรายได้ปลายงวด · **ขายลดตั๋วเงิน (bill discounting):** ถ้า *มีสิทธิไล่เบี้ย (with recourse — พบบ่อยในไทย)* = **หนี้กู้ระยะสั้นแฝง** (ตั๋วยังอยู่บนงบ = กู้โดยใช้ตั๋วค้ำ ไม่ใช่ลดลูกหนี้สะอาด); *ไม่มีสิทธิไล่เบี้ย (without recourse)* = ขายขาดจริง ตัดลูกหนี้ออกได้ → **ทุกตัวจับได้ด้วย หมายเหตุ + trend + CFO ยืนยันกำไร**

---

## กับดัก (Anti-patterns)
- **ดูแต่กำไรสุทธิ ลืม CFO** — กำไร accrual แต่งได้; CFO โกหกยาก (กำไรโต+CFO ลบ = อันตราย)
- **ดู ratio ตัวเดียวลอยๆ** — ต้องเทียบ trend ตัวเอง + คู่แข่ง industry เดียวกัน
- **เชื่อกำไร one-off/OCI/กลับค่าเผื่อ** ว่าเป็น core
- **ลืมอ่านหมายเหตุ** — หนี้ค้ำ/ฟ้อง/related-party/นโยบายซ่อนอยู่นั่น
- **"auditor ผ่าน = ไม่มีโกง"** — auditor ไม่ได้มีหน้าที่หลักจับฉ้อฉล
- **ไม่ดูค่าเผื่อ/ด้อยค่า** — สินทรัพย์ตั้งค่าเผื่อน้อย = สินทรัพย์ปลอม
- **สับงบเดี่ยว vs งบรวม** — คนละ scope อย่าเทียบมั่ว
- **เทียบข้ามปีโดยไม่เช็คมาตรฐานบัญชีเปลี่ยน**

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"เคสที่งบดูดีแต่ผมจับได้ว่าแต่ง เพราะ CFO/หมายเหตุ..."*
> - *"ตอนประเมินบริษัท/นายจ้าง ผมดู... ก่อนตัดสินใจ"*

---
*ช่วยคิดอ่านงบการเงินเพื่อการศึกษา ไม่ใช่คำแนะนำการลงทุน/บัญชีจากผู้มีใบอนุญาต — ตัวเลข/นโยบายบัญชีต้องตรวจกับงบจริง + ผู้สอบบัญชี/ผู้เชี่ยวชาญก่อนตัดสินใจ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: hematology-judgment ═════════ -->

---
skill: hematology-judgment
title: ตัวช่วยตัดสินใจในแลบโลหิตวิทยา (Hematology Judgment)
type: ADVISE
needs: any
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "skill นี้ช่วย 'คิด' เพื่อการศึกษา ไม่ตัดสินใจแทนและไม่วินิจฉัยแทนผู้ป่วย · blast / ค่าวิกฤต = เร่งด่วน ต้องแจ้งแพทย์ทันที · ทุกผลที่กระทบการรักษาต้อง review smear ด้วยตา + ยืนยันกับ MT ผู้รับผิดชอบ/แพทย์ก่อนรายงาน · AI อาจผิดได้ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ตัวช่วยตัดสินใจในแลบโลหิตวิทยา

ตัวช่วยตัดสินใจในแลบโลหิตวิทยา — เน้น "ผล CBC/smear/coag นี้ ต้องทำอะไรต่อ + อย่าพลาดตรงไหน" ไม่ใช่ atlas รูปเซลล์หรือตารางค่าปกติ

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
1. ดู smear หา platelet clump (feather edge) — มี clump = EDTA-induced pseudothrombocytopenia
2. clump → เก็บใหม่ใน citrate (3.2%) แล้วคูณ dilution factor หรือ heparin tube → รายงานค่าแก้
3. ไม่มี clump + smear ยืนยันต่ำจริง → รายงาน + ต่ำมาก = critical แจ้งแพทย์

ห้าม auto-report plt ต่ำจาก analyzer โดยไม่ดู smear.

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

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - SOP ของแลบคุณกำหนด smear-review criteria / critical-value list / delta-check rule ไว้อย่างไร? (เติมให้ตรงเครื่องและ policy จริง)
> - analyzer รุ่นที่ใช้ (เช่น Sysmex/Beckman) มี flag เฉพาะตัวไหนที่ทีมตีความต่างจาก default?
> - screening flow thalassemia / reflex algorithm ในพื้นที่คุณ ต่างจากที่ระบุไว้ตรงไหน (cut-off, DNA referral)?

NOTE: knowledge (MCV/MCH/MCHC/RPI formulas, OFT/DCIP principles, thal genotype tables, cytochemistry stains) → ดู "ตำรา/แหล่งอ้างอิงมาตรฐาน" ไม่ใช่หน้าที่ของ skill นี้

---
*skill นี้เป็นตัวช่วย "คิด" เพื่อการศึกษา ไม่ใช่ตัวตัดสินใจหรือวินิจฉัยแทน · blast / ค่าวิกฤต = เร่งด่วน แจ้งแพทย์ทันที · ทุกผลที่กระทบการรักษาต้อง review smear + ยืนยันกับ MT ผู้รับผิดชอบ/แพทย์ก่อนรายงาน · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: ikigai-finder ═════════ -->

---
skill: ikigai-finder
title: หา Ikigai แบบไม่หลอกตัวเอง (Honest Ikigai Finder)
type: ADVISE               # ช่วยสะท้อนคิด ไม่ได้รันอะไร
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "เครื่องมือช่วยสะท้อนคิดเพื่อการศึกษา ไม่ใช่คำแนะนำทางการจากที่ปรึกษาอาชีพ/จิตวิทยา — การตัดสินใจใหญ่ (ลาออก/เปลี่ยนสาย) ควรปรึกษาคนที่ไว้ใจและพิจารณารอบด้าน · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# หา Ikigai แบบไม่หลอกตัวเอง

ikigai = เหตุผลที่ทำให้ตื่นขึ้นมาในแต่ละวัน — แต่แบบที่ **ไม่ใช่แค่วาดวงกลม 4 วงสวยๆ แล้วจบ**

> **กฎ #1:** อ่านจาก "สิ่งที่ทำจริง" ไม่ใช่ "สิ่งที่พูด" (revealed preference) — ถ้าถาม "รักอะไร" แล้วได้คำตอบที่ *ควรจะรัก* คำตอบหลอกตั้งแต่ต้น ให้เจาะ "ทำแล้วลืมเวลา / ทำฟรีก็ยอม" แทน.
> **กับดัก #1:** ikigai คือ **ทิศทาง ไม่ใช่ปลายทาง** — output คือ **1 การทดลองเล็กๆ ไป overlap** ห้ามจบที่วาด Venn สวยๆ และห้ามเอามาเป็นข้ออ้างลาออกหุนหัน.
> (ภาพ 4 วง รัก/เก่ง/โลกต้องการ/ได้เงิน คนรู้หมด — ที่ติดคือ ตอบกว้าง · หลอกตัวเอง · วาดเสร็จไม่ทำต่อ. skill นี้แก้ 3 อันนั้น)

## ใช้เมื่อ
รู้สึกหลงทาง/ไม่รู้จะไปทางไหน, กำลังคิดเปลี่ยนสายงาน, หรืออยากเช็คว่าสิ่งที่ทำอยู่ "ใช่" รึเปล่า

## วิธีใช้
วาง skill นี้ (ChatGPT/Claude/Gemini) + พิมพ์ *"ช่วยหา ikigai ให้หน่อย"* → ตอบคำถามที่ AI ถามทีละข้อ **ตามจริง** (ยิ่งจริง ยิ่งได้คำตอบจริง)

---

## วิธีโค้ช (AI: ทำตามนี้ ทีละขั้น อย่ารวบ)

### ขั้น 1 — แมป 4 วง แบบ "ไม่ให้หลอกตัวเอง"
ถามทีละวง + บังคับให้เจาะจง + เช็ก **สิ่งที่ทำจริง ไม่ใช่สิ่งที่พูด** (revealed preference):
- **รัก:** ไม่ใช่ "สิ่งที่ควรจะรัก" — แต่ **อะไรที่ทำแล้วลืมเวลา / ทำฟรีก็ยอม / วันหยุดเลือกทำเอง**
- **เก่ง:** **คนมักมาถามอะไรเรา / อะไรที่เราง่ายแต่คนอื่นยาก** (ไม่ใช่สิ่งที่ "อยากเก่ง")
- **โลกต้องการ:** ปัญหาจริงที่คนบ่น/ยอมจ่าย/หาทางแก้ — ไม่ใช่ที่เราคิดว่าโลก "ควร" ต้องการ
- **ได้เงิน:** เงินไหลไปทางไหนจริงๆ (ดู market จริง อย่าโลกสวย)

### ขั้น 2 — หา overlap + ตั้งชื่อ "ความตึง"
ส่วนใหญ่ไม่ได้มีครบ 4 วงตรงกลาง — ค่าอยู่ที่ overlap บางส่วน + รู้ว่าตึงตรงไหน:
- รัก + เก่ง แต่ไม่ได้เงิน = **passion** → จะ monetize หรือเก็บเป็นความสุข
- เก่ง + ได้เงิน แต่ไม่รัก = **profession** (กับดักทอง — MT/คนทำงานประจำหลายคนรู้สึกแบบนี้)
- รัก + โลกต้องการ แต่ยังไม่เก่ง = **mission** → ต้องสร้าง skill
- โลกต้องการ + ได้เงิน แต่ไม่รัก/ไม่เก่ง = **vocation** → ระวัง burnout

### ขั้น 3 — เลือกความตึงที่กำลังอยู่ + การเคลื่อนที่สมจริง
คนน้อยมากที่ได้ครบ 4 — บอกตรงๆ ว่าตอนนี้อยู่ตึงแบบไหน แล้วการเคลื่อนที่ทำได้จริงคืออะไร (ไม่ใช่ "ลาออกไปตามฝัน")

### ขั้น 4 — เตือนความจริงเรื่อง ikigai (สำคัญ)
- ikigai ฉบับญี่ปุ่นแท้ๆ **ไม่ใช่แค่ career/เงิน** — มันคือ "เหตุผลเล็กๆ ที่ทำให้ตื่นมา" (กาแฟเช้า, ดูแลคนที่รัก, งานเล็กที่ภูมิใจ)
- **อย่าลดคุณค่าตัวเองเหลือแค่ "จุดกลางของ Venn"** — ความหมายในชีวิต ≠ ต้องหาเลี้ยงชีพจากสิ่งที่รักเสมอไป

### ขั้น 5 — แปลงเป็น 1 การทดลอง
ikigai = **ทิศทาง ไม่ใช่ปลายทาง** → การเคลื่อนคือ **1 การทดลองเล็กๆ ไปทาง overlap** (เช่น ลองทำ side project 1 เดือน, คุยกับคนในสายที่สนใจ) ไม่ใช่ตัดสินใจใหญ่ทันที

---

## กับดัก (Anti-patterns)
- **ตอบ "รัก" ด้วยสิ่งที่ควรจะรัก** ไม่ใช่ที่รักจริง → คำตอบหลอกตั้งแต่ต้น
- **คิดว่าต้องได้ครบ 4 วงถึงจะมีความสุข** → คนส่วนใหญ่อยู่ที่ overlap แล้วก็โอเค
- **วาด Venn เสร็จแล้วจบ** ไม่แปลงเป็นการกระทำ → ได้แค่โปสเตอร์
- **เอา ikigai มาเป็นข้ออ้างลาออกหุนหัน** → มันคือทิศ ทดลองก่อนเสมอ
- **สับสน "ความสุขในชีวิต" กับ "อาชีพ"** → บางอย่างเก็บเป็นงานอดิเรกดีกว่าฝืนทำเป็นงาน

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมจากคนที่เคยผ่าน pivot จริง เช่น:
> - *"ตอนผมตึงแบบ profession (เก่ง+เงิน ไม่รัก) ผมเคลื่อนโดย..."*
> - *"การทดลองเล็กๆ ที่บอกว่าทางนี้ใช่/ไม่ใช่ คือ..."*
> - *"สิ่งที่ผมคิดว่ารัก แต่พอทำเป็นงานจริงแล้วเกลียด คือ..."*

---
*เครื่องมือช่วยสะท้อนคิดเพื่อการศึกษา ไม่ใช่คำแนะนำทางการจากที่ปรึกษาอาชีพ/จิตวิทยา — การตัดสินใจใหญ่ ควรปรึกษาคนที่ไว้ใจและพิจารณารอบด้าน · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: immunoassay-judgment ═════════ -->

---
skill: immunoassay-judgment
title: ตัวช่วยตัดสินใจ Immunoassay และ Serology (Immunoassay & Serology Judgment)
type: ADVISE
needs: any
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "Skill นี้เป็นตัวช่วย 'คิด' เพื่อการศึกษาเรื่อง immunoassay/serology ไม่ใช่คำสั่งวินิจฉัย/รักษา ผล reactive screen ไม่เท่ากับการวินิจฉัย ต้อง confirm ด้วย test ที่ specificity สูงก่อนรายงานเสมอ ทุกผลต้องยืนยันกับ MT/แพทย์ และทำตาม SOP/QC ของห้องแล็บ ความผิดพลาดในการตีความ serology อาจกระทบความปลอดภัยของผู้ป่วยโดยตรง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ตัวช่วยตัดสินใจ Immunoassay และ Serology

ตัวช่วย "ตัดสินใจ" เรื่อง immunoassay/serology สำหรับคนหน้างาน lab — ไม่ใช่ตำราท่องนิยาม — ทุกคำตอบตอบ 2 อย่าง: "เลือก/ตีความอะไร" + "พลาดตรงไหน".

> **กฎเหล็ก #1:** reactive screen ≠ diagnosis — **ห้าม report positive จาก screen เดี่ยว** ต้อง confirm ด้วย test specificity สูงก่อนเสมอ (HIV/syphilis/HCV). เลือก format ตาม analyte: ใหญ่/≥2 epitope = **sandwich** (signal ตรง), เล็ก/hapten = **competitive** (signal **ผกผัน**).
>
> **กฎเหล็ก #2 (ขอบที่ weak model พลาด):** ผลที่ "ขัดกับ clinical ชัดๆ" **ไม่ใช่ผลที่เชื่อได้** — **ลบสวนอาการหนัก** หรือ **ต่ำสวนอาการ** = สงสัย false-negative ทางเทคนิคก่อน (prozone/hook = Ab/Ag เกิน, หรือ window period) → **เจือจาง (dilute) แล้วซ้ำ / นัดเจาะใหม่** อย่ารายงาน "negative/ปกติ" ทันที. **negative ไม่ได้แปลว่า rule-out เสมอ.**

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- ต้องเลือก immunoassay format ให้เหมาะกับ analyte (sandwich vs competitive vs CLIA/ECLIA vs lateral flow)
- ต้องตีความ serology panel — HBV, HIV algorithm, syphilis NTT/TT, ANA pattern
- ก้ำกึ่งว่า reactive screen ต้อง confirm ไหม / dilute เพราะ prozone-hook ไหม
- ผลลบสวนอาการ หรือ ผลบวกในคน prevalence ต่ำ — ต้องตัดสินใจว่าเชื่อหรือทวน
- เลือก/อ่าน non-label (agglutination/nephelometry/precipitation) · immunoblot/Western · IGRA (QFT) · ระวัง HAMA/biotin interference
- (สาย sales/IVD) เตรียมคุยงาน diagnostics — Abbott Architect/Alinity, Roche Elecsys/cobas, Bio-Rad, Siemens

## วิธีใช้
วาง skill นี้ + เคส/ผลที่เจอ (analyte, format, ค่า screen/confirm, clinical) → AI เดินตาม fork ด้านล่าง บอก "เลือก/ตีความอะไร" + "กับดักที่ต้องระวัง" โดยยึดหลัก confirm-ก่อน-report เสมอ

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### FORK 1 — เลือก immunoassay FORMAT (analyte นี้ ใช้แบบไหน)
ถามก่อน: analyte ใหญ่หรือเล็ก? ต้องการ throughput/quant แค่ไหน? อยู่ที่ไหน (lab vs POC)?
- Analyte = โมเลกุลใหญ่ (โปรตีน, ≥2 epitope) → Sandwich (non-competitive): 2 Ab จับคนละ epitope, signal แปรผันตรง. เช่น HBsAg, troponin, tumor marker, hormone โปรตีน.
- Analyte = โมเลกุลเล็ก / hapten (drug, steroid, T4, epitope เดียว) → Competitive: Ab ตัวเดียว, labeled-Ag แข่งกับ sample, signal แปรผกผัน. เช่น drug-of-abuse, cortisol, digoxin. → เล็ก = competitive = ผกผัน.
- ต้องการ throughput สูง + quant + automation → CLIA/ECLIA/CMIA. ECLIA = Roche Elecsys/cobas; CMIA = Abbott Architect/Alinity; CLIA/EIA = Bio-Rad/Siemens.
- ตรวจ Ab (ไม่ใช่ Ag) → Indirect format (+ secondary anti-human IgG/IgM). แยก IgM (acute) vs IgG (past/immune).
- ผลเร็ว / POC → Lateral flow (immunochromatographic, colloidal gold): hCG, dengue NS1, COVID Ag, HIV/syphilis rapid.
- quantitate Ig/RF/complement/CRP → Nephelometry/turbidimetry (particle-enhanced latex).
- Heterogeneous (ล้าง bound-free: ELISA/CLIA) vs Homogeneous (ไม่ล้าง: EMIT/CEDIA) → homogeneous เร็ว/automate ง่ายแต่ไวต่อ interference มากกว่า.

### FORK 2 — SEROLOGY interpretation forks
HBV panel (HBsAg / anti-HBs / anti-HBc) — อ่าน 3 ตัวรวมกัน:

| HBsAg | anti-HBc (total) | anti-HBs | → สถานะ |
|---|---|---|---|
| + | + (IgM) | − | Acute infection |
| + | + (IgG) | − | Chronic (HBsAg + > 6 เดือน) |
| − | + | + | Recovered (หายเอง, มีภูมิ) |
| − | − | + | Vaccinated (ภูมิจากวัคซีน, ไม่มี anti-HBc) |
| − | + | − | "core-only" → window/occult/false-pos → follow-up |

ตัวชี้ขาด vaccinated vs recovered = anti-HBc.

- HIV algorithm: screen 4th-gen Ag/Ab combo (p24 + Ab) → reactive → confirm (Ab differentiation / particle agglutination / WB) → discordant/acute → NAT (viral load). อย่ารายงาน positive จาก screen เดี่ยว.
- Syphilis: NTT (RPR/VDRL, titer ติดตามการรักษา) + TT (TPHA/TPPA/FTA, จำเพาะ, มักบวกตลอดชีวิต (ส่วนน้อย serorevert ได้ โดยเฉพาะรักษาเร็วในระยะแรก)). Traditional: NTT screen → TT confirm. Reverse: TT screen → NTT confirm + titer. TT+ NTT− → early หรือ treated-old → TT ตัวที่สอง. **Fourfold (4×) rule:** titer ขึ้น ≥4× = รักษาล้มเหลว/reinfection; ลด ≥4× = ตอบสนองดี (เทียบ test+lab เดียวกัน). **Congenital:** titer ทารก **≥4× มารดา** = เข้าเกณฑ์/บ่งชี้ congenital → flag แพทย์. ⚠️ **<4× ไม่ได้ตัด congenital ออก** (sensitivity จำกัด — ทารกติดเชื้อจริงได้แม้ titer ไม่ถึง 4× → ดู clinical/ตามต่อ). ⚠️ prozone (Ab สูง→false neg, dilute) + BFP (ตั้งครรภ์/SLE/HIV/TB).
- **Viral serology (อ่านเป็น "ระยะ"):** HCV — **anti-HCV+ ≠ ติดอยู่** ต้อง **HCV RNA ยืนยัน** (Ab คงอยู่แม้หาย ไม่มีภูมิป้องกัน) · HBV window — HBsAg/anti-HBs ลบทั้งคู่ อย่าสรุป "ไม่ติด" → เช็ค **anti-HBc IgM** · **Herpes (HSV/CMV/EBV) IgG+ = เคยติด/latent ไม่ใช่ acute** → acute ต้อง IgM/seroconversion/PCR · ทารก<18-24 ด. ใช้ **DNA-PCR ไม่ใช่ Ab** (maternal IgG)
- **IgG avidity (ใช้ "date" การติดเชื้อ):** **avidity ต่ำ = ปฐมภูมิเพิ่งติด (recent primary)** · **สูง = ติดนานแล้ว/past** — สำคัญใน **TORCH หญิงตั้งครรภ์** (Toxo/CMV/Rubella: low avidity = เพิ่งติดในครรภ์ = เสี่ยงต่อทารกสูง) เพราะ IgM อยู่นาน/false+ ได้ → avidity ฟันธง "เพิ่งติดจริงไหม"
- **Dengue (ไทยออกบ่อย — อ่านเป็นระยะ + primary/secondary):** **NS1 Ag ขึ้นช่วงแรก (วันแรกๆ ของไข้)** · **IgM เด่น = primary** · **IgG ขึ้นเร็ว/สูงกว่า IgM = secondary** (เคยติด serotype อื่น) → secondary เสี่ยง **DHF/พลาสมารั่ว** สูงกว่า = flag clinical
- ANA (IIF บน HEp-2 = gold) → รายงาน pattern + titer: Homogeneous → dsDNA/histone → SLE/drug-induced; Speckled → Sm/RNP; Peripheral/rim → active SLE; Nucleolar → scleroderma; Centromere → CREST. ↑titer → ↓false-positive. confirm ด้วย anti-dsDNA / anti-ENA.

### FORK 3 — เมื่อไหร่ "ต้อง CONFIRM" reactive screen
- screen sensitivity สูง (↓FN) → มี false-positive ปนเสมอ. reactive screen ≠ diagnosis. ต้อง confirm ด้วย test specificity สูง (↓FP) ก่อนรายงาน (HIV, syphilis, HCV).
- PPV ขึ้นกับ prevalence: prevalence ต่ำ + screen reactive → ส่วนใหญ่อาจ false-pos → confirm ยิ่งจำเป็น.

### FORK 4 — Non-label techniques + agglutination
- **Precipitin zone:** ตะกอนเฉพาะ equivalence · **prozone (Ab เกิน) / postzone (Ag เกิน)** → false negative → เจือจางแล้วซ้ำ
- **Turbidimetry vs Nephelometry:** turbidimetry วัดแสง**ลด** (180°) · **nephelometry วัด scatter** (10-90°) ไวกว่า → ใช้กับ Ig/complement/CRP/RF · particle-enhanced (latex) ตรวจ analyte เล็กลงได้
- **RID/Ouchterlony/IFE:** RID = quant Ag จากวงตะกอน · Ouchterlony = identity/non-identity · **IFE = typing monoclonal protein** (myeloma)
- **Agglutination 4 ชนิด:** Direct (Ag บน particle เอง — blood typing) · Passive (soluble Ag เคลือบ → ตรวจ Ab) · **Reverse passive** (Ab เคลือบ → ตรวจ Ag: CRP/HBsAg latex) · Inhibition (ยับยั้ง=บวก, hapten) · **IgM จับกลุ่มดีกว่า IgG มาก** (10 site) · titer = dilution สูงสุดที่ยังบวก

### FORK 5 — Immunoblotting / Western blot (confirm + characterize)
- SDS-PAGE แยกตาม **ขนาด (MW)** → blot ลง membrane → block → Ab จำเพาะ → enzyme/chemiluminescent substrate
- ใช้: **confirmatory** (Ab จับโปรตีนเป้าตัวไหน) + **characterize Ag** · **reducing (+2-ME) vs non-reducing** → MW เปลี่ยน = มี disulfide bond

### FORK 6 — Cell-based / IGRA (เช่น QFT-TB)
- whole blood + peptide จำเพาะ TB (ESAT-6/CFP-10) → วัด **IFN-γ ที่ T cell หลั่ง ด้วย ELISA (sandwich)** = ตรวจ cell-mediated immunity (รวม latent TB) แทน/เสริม TST (ไม่ false+ จาก BCG)
- ⚠️ **Indeterminate** = mitogen control ไม่ขึ้น / nil สูง → ตีความไม่ได้ ต้องเจาะใหม่ · clotted = invalid

## กับดัก (Anti-patterns)
1. Prozone (false-negative ที่ titer สูง) #1 — Ab เกินมาก → ไม่เกิด lattice → ผลลบทั้งที่ป่วยหนัก (RPR ใน secondary syphilis). เจอ clinical สงสัยแต่ผลลบ → เจือจาง (dilute) ทดสอบใหม่. Postzone = Ag เกิน. optimal = equivalence.
2. Hook effect (high-dose hook) — sandwich CLIA: analyte สูงมาก (tumor marker, β-hCG) → saturate Ab ทั้งสองข้าง → signal ต่ำหลอก. ผลต่ำสวนอาการ → dilute ซ้ำ.
3. Window period — ตรวจเร็วเกินยังไม่มี marker. HIV: RNA ~7-14 วัน → p24 ~16 วัน → Ab ~25 วัน. HBV: core-window. ผลลบในคนเพิ่งเสี่ยง → ยังไม่ตัดโรค, นัดซ้ำ.
4. Cross-reactivity / false-positive → ไม่ confirm — biological false-pos RPR (SLE, ตั้งครรภ์, ติดเชื้ออื่น); RF รบกวน; heterophile Ab.
5. อ่าน HBV panel ทีละตัว — HBsAg+ เดี่ยวไม่บอก acute vs chronic; anti-HBs+ เดี่ยวไม่บอก vaccinated vs recovered → ดู anti-HBc.
6. สับ competitive กับ sandwich — ใช้ sandwich กับ hapten เล็ก = พัง; ใช้ competitive แล้วลืม signal ผกผัน = อ่านกลับด้าน.
7. ลืมเตรียม specimen — ไม่ heat-inactivate complement (56°C 30 นาที); lipemia/hemolysis รบกวน optical; IgM ทำงานดีที่เย็น.
8. ใช้ test ผิดจุดประสงค์ — screen ไปใช้ confirm; TT (มักบวกตลอดชีวิต (ส่วนน้อย serorevert ได้ โดยเฉพาะรักษาเร็วในระยะแรก)) ไปติดตามการรักษาแทน NTT titer → ตีความผิดว่า "ไม่หาย".
9. HAMA (human anti-mouse Ab) — คนไข้เคยรับ mAb บำบัด → จับ capture+detection Ab ของ sandwich → false +/− → ต้อง blocking reagent.
10. Biotin interference — กิน biotin (วิตามินผม/เล็บ) สูง รบกวน assay biotin-streptavidin → ผลเพี้ยน (TSH/troponin ต่ำปลอม อันตราย) → งด biotin ก่อนเจาะ.
11. Competitive / lateral-flow อ่านกลับด้าน — สัญญาณต่ำ หรือ "ไม่มีแถบ test" = analyte สูง (ชุดยาเสพติด); **control line ไม่ขึ้น = invalid ไม่ใช่ลบ**.

> NOTE: knowledge (Ig class, complement pathway, hypersensitivity I-IV, Sens/Spec/PPV/NPV) → point to "ตำรา/แหล่งอ้างอิงมาตรฐาน", no path.

## ช่องสำหรับผู้เชี่ยวชาญเติม
> - เติม cutoff/algorithm ของ HIV/HCV/syphilis ที่ใช้จริงตาม SOP ห้องแล็บนั้นๆ (traditional vs reverse)
> - ระบุ analyzer + reagent platform ที่ใช้ (Abbott/Roche/Bio-Rad/Siemens) + protocol dilution เมื่อสงสัย prozone/hook
> - เพิ่ม panel/marker เฉพาะที่ รพ. ใช้บ่อย + criteria การ confirm/repeat ตาม policy ห้องแล็บ

---
*Skill นี้เป็นตัวช่วย "คิด" เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รักษา — reactive screen ต้อง confirm ก่อน report ทุกผลต้องยืนยันกับ MT/แพทย์ + ทำตาม SOP/QC ของห้องแล็บ ความผิดพลาดในการตีความ serology กระทบความปลอดภัยผู้ป่วยโดยตรง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: infection-control-judgment ═════════ -->

---
skill: infection-control-judgment
title: โค้ชป้องกันการติดเชื้อ/biosafety — PPE/precaution/ห้องแยก (Infection Control & Biosafety Judgment)
type: ADVISE               # ช่วยตัดสินใจ IPC/ความปลอดภัย ไม่ใช่ตำรา CDC
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดการป้องกันการติดเชื้อ/ความปลอดภัยทางชีวภาพเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์ — ต้องทำตามนโยบาย IPC + มาตรฐานความปลอดภัย (CDC/HICPAC/ISO 15190/WHO) + คณะกรรมการ IC ของหน่วยงานจริงเสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชป้องกันการติดเชื้อ/biosafety — PPE/precaution/ห้องแยก

ตัดสินใจ "เคสนี้ใช้ PPE/precaution/ห้องแบบไหน" — ป้องกันตัวเอง+คนไข้+ห้องแล็บไม่ให้แพร่เชื้อ ไม่ใช่ท่อง guideline (= commodity ดู CDC/WHO)

> **VERDICT: เลือกการป้องกันตาม "ทางแพร่เชื้อ" — contact→ถุงมือ+กาวน์ · droplet→surgical mask · airborne(TB/หัด/สุกใส)→N95+ห้องความดันลบ.**
> **กับดักอันดับ 1: airborne ใช้ surgical mask แทน N95 หรือเอาไปห้องความดันบวก = เป่าเชื้อแพร่ทั่ว** (สลับชนิดห้อง = หายนะ).
> สำหรับ MT/lab ที่จับ specimen ติดเชื้อทุกวัน + งาน IPC · เชื้อก่อโรค/AST ดู `clinmicro-judgment` · ความปลอดภัยระดับระบบ (ISO 15190) ดู `lab-management-judgment`

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- เคสนี้ใช้ PPE อะไร / precaution แบบไหน / ห้องความดันบวกหรือลบ
- เข็มตำ/สัมผัสสารคัดหลั่ง → ทำอะไรต่อ
- จัดการ specimen/เชื้อเสี่ยงในแล็บ (biosafety)

## วิธีใช้
วาง skill นี้ + เล่าสถานการณ์ (เชื้อ/หัตถการ/ผู้ป่วย) → AI ชี้ระดับการป้องกัน + กับดักที่ทำให้แพร่เชื้อ

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — Hand hygiene: alcohol vs สบู่+น้ำ
> **VERDICT: alcohol hand-rub ทุกครั้ง — ยกเว้นมือเปื้อนชัด หรือ *C. difficile*/spore → สบู่+น้ำ.**
- **default = alcohol hand-rub** (ฆ่า bacteria/virus/fungi ดี + เร็ว)
- ⚠️ **ใช้สบู่+น้ำเมื่อ: (1) มือเปื้อนเห็นชัด (2) สงสัย/ดูแล *C. difficile*** — **spore แอลกอฮอล์ฆ่าไม่ได้** ต้องล้างออกด้วยน้ำ (anthrax = spore เช่นกัน · *norovirus = ไวรัสไม่มีเปลือก* แอลกอฮอล์ได้ผลแย่ → สบู่+น้ำ)
- WHO **5 Moments:** ก่อนสัมผัสผู้ป่วย · ก่อนหัตถการ sterile · หลังสัมผัสสารคัดหลั่ง · หลังสัมผัสผู้ป่วย · หลังสัมผัสสิ่งแวดล้อมรอบเตียง · **ล้างมือทุกครั้งหลังถอดถุงมือ**

### Fork 2 — เลือก mask/PPE ตามทางแพร่
> **VERDICT: droplet→surgical mask · airborne หรือหัตถการสร้าง aerosol→N95.**
- **Surgical mask = กัน droplet** (เม็ดใหญ่ ตกใน ~1-2 เมตร)
- **N95/respirator = กัน airborne** (กรอง ≥95% ที่ขนาดเจาะผ่านยากสุด ~0.3 µm — เล็ก/ใหญ่กว่ากรองได้ดีกว่า) → ใช้กับ **TB/หัด/สุกใส + หัตถการที่สร้าง aerosol** (ใส่ท่อ/ดูดเสมหะ/พ่นยา) แม้โรค droplet
- **ลำดับใส่ PPE:** กาวน์ → mask → ถุงมือ (ถุงมือสุดท้าย) · **ถอด:** ถุงมือก่อน → ... → ล้างมือ

### Fork 3 — Transmission-based precaution (3 ชนิด)
> **VERDICT: จับคู่เชื้อ→precaution: contact=ถุงมือ+กาวน์ · droplet=mask · airborne=N95+ห้องลบ. + standard precaution กับทุกคนเสมอ.**

| ชนิด | เชื้อตัวอย่าง | ป้องกัน |
|---|---|---|
| **Contact** | MRSA/VRE/MDR-GNB/C.diff | ถุงมือ + กาวน์ |
| **Droplet** | ไข้หวัดใหญ่/pertussis/meningococcus | mask + ระยะห่าง **≥3 ฟุต (ขั้นต่ำ ไม่ใช่เส้นปลอดภัย)** |
| **Airborne** | **TB/หัด/สุกใส** | **N95 + ห้องความดันลบ (AIIR)** |
- ⚠️ **≥3 ฟุต เป็น "พื้น" ไม่ใช่ระยะปลอดภัย** — เชื้อรุนแรง (smallpox/SARS) droplet ไปได้ ≥6 ฟุต → ใส่ mask ตั้งแต่ 6-10 ฟุต หรือทันทีที่เข้าห้อง
- standard precaution = ใช้กับทุกคน (ถือว่าเลือด/สารคัดหลั่งทุกคนติดเชื้อได้)

### Fork 4 — ห้องแยก: ความดันลบ vs บวก (อย่าสลับ = อันตราย)
> **VERDICT: ความดันลบ = กันเชื้อ "ออก" (airborne) · ความดันบวก = กันเชื้อ "เข้า" (ภูมิคุ้มกันต่ำ). สลับ = หายนะ.**
- **Negative pressure (AIIR):** airborne/หนองไหล/คุมอุจจาระไม่ได้ → ดูดอากาศออก **กันเชื้อแพร่ออก**
- **Positive pressure:** ผู้ป่วย **ภูมิคุ้มกันต่ำ** (BMT/neutropenia) → ดันอากาศออก **กันเชื้อเข้าหาผู้ป่วย**
- ⚠️ **สลับ = หายนะ:** เอา TB ไปห้องความดันบวก = เป่าเชื้อออกไปทั่ว · ไม่พอ → **cohorting** (รวมผู้ป่วยเชื้อเดียวกัน)

### Fork 5 — Post-exposure (เข็มตำ/สัมผัสสารคัดหลั่ง)
> **VERDICT: ล้างทันที → report → รับ PEP ตามโปรโตคอล (HIV ยิ่งเร็วยิ่งดี). ห้ามปิดเงียบ.**
- หยุด+ล้าง → ประเมินแหล่ง (HIV/HBV/HCV status) → **report + รับ PEP ตามโปรโตคอล** (HIV PEP ยิ่งเร็วยิ่งดี; HBV ดู immune status/HBIG)
- **บุคลากรควรมีภูมิล่วงหน้า:** HBV, varicella, MMR, influenza · ⚠️ single-dose (เช่น influenza) ภูมิขึ้น ~2-3 สัปดาห์หลังฉีด แต่ **HBV/varicella/MMR เป็น multi-dose series — ต้องฉีดครบชุดก่อนถึงจะถือว่ามีภูมิ** (HBV ยืนยันด้วย anti-HBs ≥10 mIU/mL หลังครบ 3 เข็ม)

### Fork 6 — Biosafety ในแล็บ
> **VERDICT: เชื้ออันตราย (TB culture, B. pseudomallei AST) ต้อง BSL-3 — lab BSL-2 ทำไม่ได้.**
- จัดการ specimen ตามระดับความเสี่ยงเชื้อ (BSL) · เชื้ออันตราย (**M. tuberculosis culture, Burkholderia pseudomallei AST**) = **ต้อง BSL-3** (lab ทั่วไป BSL-2 ทำไม่ได้)
- closed-system/automation = ลด aerosol/exposure · spill → containment ตาม SOP

---

## กับดัก (Anti-patterns)
- **ใช้ alcohol-rub กับ C. difficile** — spore ไม่ตาย ต้องสบู่+น้ำ
- **ใช้ surgical mask กับ TB/airborne** — ต้อง N95 + ห้องความดันลบ
- **ถือ 3 ฟุตเป็นระยะปลอดภัยของ droplet** — เป็นพื้นต่ำสุด เชื้อรุนแรงไปได้ ≥6 ฟุต → ใส่ mask เร็วขึ้น
- **เอาผู้ป่วยติดเชื้อ airborne ไว้ห้องความดันบวก** — เป่าเชื้อออกทั่ว (สลับชนิดห้อง)
- **ลืมล้างมือหลังถอดถุงมือ** — ถุงมือ ≠ แทนการล้างมือ
- **ใส่/ถอด PPE ผิดลำดับ** → ปนเปื้อนตัวเอง
- **เพาะ/ทำ AST เชื้อ BSL-3 (TB/melioidosis) ใน lab BSL-2** — เสี่ยงติดเชื้อ
- **มอง pre-analytical/specimen ว่าไม่ติดเชื้อ** — standard precaution กับทุกตัวอย่าง

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT/IC) เคสที่เกือบเลือก precaution ผิด จับได้เพราะ..."*
> - *"นโยบาย IPC ของ รพ. เรา จุดที่ต่างจาก guideline กลาง คือ..."*

---
*ช่วยคิดการป้องกันการติดเชื้อ/ความปลอดภัยทางชีวภาพเพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์ — ต้องทำตามนโยบาย IPC + มาตรฐานความปลอดภัย (CDC/HICPAC/ISO 15190/WHO) + คณะกรรมการ IC ของหน่วยงานจริงเสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: ivd-sales-judgment ═════════ -->

---
skill: ivd-sales-judgment
title: โค้ชขาย IVD/Lab Dx — ขายผลลัพธ์บริหาร ไม่ใช่สเปก (IVD / Lab Diagnostics Sales Judgment)
type: ADVISE               # ช่วยคิดกลยุทธ์ขาย ไม่ใช่สคริปต์ปิดการขาย
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดกลยุทธ์ขาย IVD/diagnostics เพื่อการศึกษา ไม่ใช่คำแนะนำจัดซื้อ/กฎหมาย/การรับรองผลิตภัณฑ์ใด — ห้ามใช้กล่าวอ้างเกินจริง/ทำลายคู่แข่งโดยไม่มีหลักฐาน · ผู้นำไปใช้รับผิดชอบการกระทำที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชขาย IVD/Lab Dx — ขายผลลัพธ์บริหาร ไม่ใช่สเปก

MT ที่ย้ายไปสายขาย IVD/diagnostics — ลูกค้าจริงคือ **หัวหน้าแล็บ/ผู้จัดการ/ผอ.** ที่ตัดสินด้วยภาษาบริหาร (accreditation, cost/test, TAT, QC) ไม่ใช่สเปกเครื่อง. skill นี้ช่วยพูดภาษาเขา + ปิดดีล

> ⭐ กฎ #1: lab manager ไม่ได้ซื้อ "เครื่องที่แม่นกว่า" — เขาซื้อ **"แล็บที่ผ่าน accreditation ง่ายขึ้น + ต้นทุน/ผลต่ำลง + TAT เร็วขึ้น + ปวดหัวเรื่องคน/ของน้อยลง"** → เปิดด้วย pain บริหารของเขา ห้ามเปิดด้วยสเปกเครื่อง
> ⚠️ กับดัก #1: **เสนอผิดกระเป๋างบ** — งบลงทุน (เครื่อง) อนุมัติยาก/รอบยาว; ถ้าลูกค้างบลงทุนตัน ให้พลิกเป็น **reagent rental / cost-per-test (งบดำเนินงาน)** ที่เขาเซ็นเองได้ · และก่อนปิดทุกดีล **เช็ค LIS integration** ก่อนเสมอ (เชื่อมไม่ได้ = deal breaker)
> เข้าใจ pain บริหารของลูกค้า → `lab-management-judgment` · คิดแบบลูกค้าทั่วไป → `crm-judgment` · คุยให้สุภาพแต่ชัด → `polite-but-clear`

## ใช้เมื่อ
- จะเข้าหา lab/รพ. — ไม่รู้จะเปิดเรื่องอะไร · ออกแบบข้อเสนอ/ราคา · เจอคู่แข่งราคาถูกกว่า · ขายของเข้าภาครัฐ

## วิธีใช้
วาง skill นี้ + เล่าลูกค้า (ประเภทแล็บ, pain, งบ, คู่แข่ง) → AI ช่วยจัด angle + รูปแบบข้อเสนอ + กับดักที่ทำดีลล่ม

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — เปิดด้วย pain บริหาร ไม่ใช่สเปก (pain → pitch)
| ลูกค้าเจ็บเรื่อง | พูดเรื่อง | ขายอะไร |
|---|---|---|
| เตรียม/ต่อ ISO 15189 | validation/verification package พร้อม, audit trail | เครื่องเอกสารครบ + app support |
| QC แพง/เปลืองแรง | **sigma สูง → รัน QC น้อยลง**, IQCP | เครื่อง CV ต่ำ + internal control |
| งบลงทุนอนุมัติยาก | ย้ายเป็นงบดำเนินงาน | **reagent rental / cost-per-test** |
| รายงานช้า (TAT)/คนไม่พอ | ลด pre-analytical error | automation/TLA/middleware |
| ของขาด/หมดอายุ | managed inventory | consignment/VMI |
| เจ้าเก่าส่งเครื่องแล้วหาย | after-sales + application | service contract + training |
> อย่าใช้ pitch สเปกเดียวกับทุกแล็บ — ขายให้ตรง phase ที่เขาเจ็บ

### Fork 2 — Budget pocket: เครื่อง vs น้ำยา (โคตรสำคัญ)
- **เครื่อง = งบลงทุน** → อนุมัติยาก/รอบยาว/e-bidding · **น้ำยา = งบดำเนินงาน** → คล่อง อนุมัติเร็ว
- **reagent rental / placement** = วางเครื่องถูก/ฟรี ผูกขายน้ำยา → ย้าย capex→opex → ลูกค้าอนุมัติเองได้ = ขายง่ายกว่าขายเครื่องขาด
- ถามตรงๆ: **"งบนี้จะลงช่องไหน — ลงทุนหรือดำเนินงาน?"** แล้วออกแบบข้อเสนอให้ลงช่องที่อนุมัติเร็วสุด

### Fork 3 — ROI argument ที่หัวหน้าแล็บเซ็น
- **Sigma → QC saving:** "เครื่องเดิม sigma 3.5 ต้องรัน QC N=6/วัน; เครื่องเรา sigma 5.5 รัน N=2 พอ → ประหยัด control ปีละ X" (ขาย "ต้นทุน QC ที่ลด" ไม่ใช่สเปก)
- **Cost-per-reportable-result (CPR):** เสนอราคาเป็น "บาท/ผลที่รายงานได้จริง" รวม recalibrate + QC + ของเสีย → ลูกค้าเทียบง่าย เซ็นง่าย (ไม่ใช่ราคา/กล่อง)

### Fork 4 — Timing + access (เข้าให้ถูกจังหวะ/ช่องทาง)
- ช่วง **เตรียม/ต่อ accreditation** = ลูกค้ายอมจ่ายเพื่อ "ลดความเสี่ยงตก" = จังหวะทอง
- **จัดซื้อภาครัฐ** (รพ.รัฐ/มหาลัย): มี TOR/e-bidding/สเปกกลาง → ต้องเข้าไป **ช่วยร่างสเปก (spec-in) ตั้งแต่ต้น** ไม่งั้นแพ้ราคา · รู้ปฏิทินงบ (ต้นปีงบ ต.ค.) = รู้ timing
- ⚠️ spec-in ต้องโปร่งใส/ตรงความต้องการจริงของแล็บ — ล็อกสเปกเกินจำเป็น = เสี่ยงผิดระเบียบจัดซื้อ
- ⚠️ **ความเสี่ยงกฎหมายจัดซื้อภาครัฐ:** spec-in ที่ล็อกแคบเกิน/สนิทกับ จนท.จัดซื้อเกินงาม เสี่ยงผิด **พ.ร.บ.จัดซื้อจัดจ้างฯ 2560** + ข้อหา **ฮั้วประมูล** → รักษาระยะห่าง (arm's-length) + ทุกอย่างโปร่งใส/มีหลักฐานเหตุผลทางเทคนิครองรับ

### Fork 5 — After-sales = ตัวตัดสินดีล (ในตลาด IVD มากกว่าราคา)
- ช่วง **verification** = ลูกค้าตัดสินรับเครื่องไหม → เตรียม **verification protocol + ค่าอ้างอิง + application specialist ไปนั่งช่วยรัน** = ลดภาระแล็บมหาศาล ปิดเร็ว
- **application training** ที่เราจัด = เป็นส่วนหนึ่งของ **competency record** ลูกค้า → มีค่าต่อ audit เขา
- **LIS integration:** เชื่อม LIS ลูกค้าไม่ได้ = **deal breaker** → เช็คก่อนเสมอ
- **managed inventory/consignment** = ลูกค้าไม่อยากเปลี่ยนเจ้า (lock-in เชิงบริการ)

---

## กับดัก (Anti-patterns)
- **ขายสเปกเดียวกันทุกแล็บ** — ไม่แมตช์ pain → ลูกค้าไม่รู้สึกว่าแก้ปัญหาเขา
- **เสนอผิดกระเป๋างบ** (ดันขายเครื่องก้อนใหญ่ให้แล็บที่งบลงทุนตัน) — เสนอ rental แทน
- **ไม่เช็ค LIS integration** ก่อนปิด → ระเบิดหลังเซ็น
- **ด่วนด่าเครื่องคู่แข่งว่าห่วย** จาก EQA bias — bias อาจมาจาก operator/pre-analytical → เสนอเป็น "ช่วย investigate ให้" ดูโปรกว่า + ไม่เสี่ยงพูดผิด
- **กล่าวอ้างเกินจริง/ตัวเลขไม่มีหลักฐาน** — ลูกค้าที่ทำ audit จับได้ = เสียเครดิตถาวร
- **ขายของแล้วหาย** — ไม่มี after-sales = แพ้เจ้าที่ support ดีแม้แพงกว่า

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT sales) ดีลที่ปิดได้เพราะเปลี่ยนจากขายเครื่องเป็น... ลูกค้าเซ็นเพราะ..."*
> - *"spec-in/จัดซื้อภาครัฐ จุดที่ผมเคยพลาด คือ..."*
> - *"pain ของหัวหน้าแล็บที่ผมเจอบ่อยสุด คือ... ขายแก้ด้วย..."*

---
*ช่วยคิดกลยุทธ์ขาย IVD/diagnostics เพื่อการศึกษา ไม่ใช่คำแนะนำจัดซื้อ/กฎหมาย/การรับรองผลิตภัณฑ์ใด — ห้ามใช้กล่าวอ้างเกินจริง/ทำลายคู่แข่งโดยไม่มีหลักฐาน · ผู้นำไปใช้รับผิดชอบการกระทำที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: know-yourself ═════════ -->

---
skill: know-yourself
title: รู้จักตัวเองให้ลึก — สัมภาษณ์ตัวเอง สร้างโปรไฟล์ที่ AI เอาไปใช้ต่อได้ (Deep Self-Profile)
type: ADVISE               # กรอบให้ AI "สัมภาษณ์ + สร้างโปรไฟล์" ไม่ใช่ที่ปรึกษา HR
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยสัมภาษณ์/รวบรวมข้อมูลตัวคุณเองเพื่อการศึกษา/วางแผนอาชีพ ไม่ใช่ที่ปรึกษาอาชีพ/HR ทางการ — 🔒 โปรไฟล์ที่ได้ = ข้อมูลส่วนตัวอ่อนไหว เก็บในที่ปลอดภัย อย่าวางในที่สาธารณะ/แชร์/อัปขึ้น repo สาธารณะ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# รู้จักตัวเองให้ลึก — สัมภาษณ์ตัวเอง สร้างโปรไฟล์ที่เอาไปใช้ต่อได้

AI **สัมภาษณ์เป็นรอบๆ + ขุดให้ลึก** → เรื่องราว/ผลงาน/ทักษะ/ค่านิยม → เก็บเป็น **โปรไฟล์ก้อนเดียวที่ slice ไปใช้ได้ทุกงาน** (resume · LinkedIn · cover letter · เตรียมสัมภาษณ์ · เปลี่ยนสาย · bio/content) — ไม่ใช่แค่ถาม "จบอะไร ทำงานไหน" แล้วเขียน

> แก่น: **คนเล่าเรื่องตัวเองผิวๆ + undersell เสมอ** — สกิลนี้ทำให้ AI "ขุดลึก + มีหลักฐาน + เก็บไว้ reuse" · เขียน CV จริง → `cv-judgment` · หา purpose/ทิศ → `ikigai-finder` · ให้ AI ปรับสไตล์ตามตัวเรา → `ai-assistant-calibration`
> หลัก: **เก็บ raw ให้เยอะที่สุด (ยิ่งรู้ยิ่งดี) → ค่อย slice ตามปลายทาง** ไม่ใช่เก็บเฉพาะที่คิดว่า "ใช้ตอนนี้"

> ⛔ **อย่าเพิ่งเขียนโปรไฟล์/resume/bio จากข้อมูลที่ user ให้มา — ข้อมูลแรกผิวเผินและ undersell เสมอ.** AI ต้อง **สัมภาษณ์ก่อน:** ถามทีละชุด (ครบ 8 แกนใน Fork 1) แล้ว **ขุดต่อทุกคำตอบด้วย "ตัวอย่าง? วัดผลยังไง? กี่คน/กี่บาท/กี่ %?"** จนได้ STAR + ตัวเลขจริง → ค่อยสรุปเป็น master profile. **กับดักอันดับ 1 = รับคำตอบผิวแรกแล้วเขียนเลย → ได้โปรไฟล์จืด claim ลอย พังตอนสัมภาษณ์.** ถ้า user รีบ → สัมภาษณ์สั้นอย่างน้อย 1 รอบก่อนร่าง ห้ามข้าม.

## ใช้เมื่อ
- จะทำ resume/CV/LinkedIn/cover letter แต่ "ไม่รู้จะเขียนอะไรเกี่ยวกับตัวเอง"
- เตรียมสัมภาษณ์งาน / เปลี่ยนสาย / ตัดสินใจ career
- อยากให้ AI (Claude/ChatGPT/Gemini) "รู้จักเรา" เพื่อช่วยงานส่วนตัวได้ตรงขึ้น
- สร้าง personal brand / เขียน bio / ทำคอนเทนต์เกี่ยวกับตัวเอง

## วิธีใช้
วาง skill นี้ + พิมพ์ *"สัมภาษณ์ผมเพื่อสร้างโปรไฟล์ — ถามทีละรอบ"* → ตอบคำถามไปเรื่อยๆ → AI สรุปเป็น "master profile" ให้ save ไว้ → คราวหลังวางโปรไฟล์กลับให้ AI ก่อนสั่งงาน (resume/สัมภาษณ์/ฯลฯ)

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — เก็บอะไรบ้าง (คนมีหลายมิติ อย่าถามแค่ประวัติ)
ไล่ครบทุกแกน (ถามเป็นชุด ไม่ drip ทีละข้อ):
- **ภูมิหลัง:** การศึกษา · เส้นทางสายงาน · จุดเปลี่ยนสำคัญ
- **ประสบการณ์ + ผลงาน:** งาน/โปรเจกต์/อาสา → ดึงเป็น **STAR/CAR + ตัวเลข**
- **ทักษะ:** hard + soft + เครื่องมือ → ระดับ + **หลักฐาน** (ไม่ใช่แค่ list)
- **ค่านิยม + แรงขับ:** อะไรทำแล้วมีไฟ · อะไรทนไม่ได้ · ทำไมเลือกสายนี้
- **จุดแข็ง + จุดอ่อนจริง** (ไม่ใช่ "perfectionist")
- **บุคลิก/สไตล์ทำงาน** (เพื่อ fit + คู่ `ai-assistant-calibration`)
- **เป้าหมาย + ข้อจำกัด** (อยากไปไหน · เงิน/เวลา/ครอบครัว/พื้นที่ที่จำกัด)
- **คลังเรื่อง:** ภูมิใจสุด · พังแล้วได้บทเรียน · เรื่องที่เล่าแล้วตาเป็นประกาย

### Fork 2 — ขุดให้ลึก (เพราะคำตอบแรกมักผิวเผิน)
- ถามต่อทีละชั้น: **"ทำไม / ยกตัวอย่าง / ตอนนั้นเกิดอะไร / วัดผลยังไง"**
- **STAR/CAR:** Situation → Task → Action → **Result (ตัวเลข)** ทุกผลงาน
- **Quantify ทุกอย่างที่วัดได้** (กี่คน/กี่บาท/กี่ %/เร็วขึ้นเท่าไหร่/ลดอะไรได้)
- ถาม **"คนอื่นชมอะไรบ่อย" + "งานที่คนมักมาขอให้ช่วย"** = จุดแข็งที่ตัวเองมองข้าม
- เจาะ **failure + บทเรียน** ด้วย ไม่ใช่เก็บแต่ success

### Fork 3 — โครงสร้างโปรไฟล์ให้ reuse (master profile ก้อนเดียว)
- เก็บ **"master profile" ที่เดียว** → ค่อย slice ออกตามงาน (ห้ามทำใหม่ทุกครั้ง)
- sections: **Summary · Experience (STAR+metrics) · Skills (มีหลักฐาน) · Achievements · Values/Goals · Stories-bank · Personality · Constraints**
- แยก **raw (เก็บทุกอย่าง)** ออกจาก **polished (เลือกใช้)** — raw ยิ่งเยอะยิ่งดี (ตรงกับ "ยิ่งรู้ยิ่งดี")

### Fork 4 — slice ตามปลายทาง (resume ≠ LinkedIn ≠ สัมภาษณ์ ≠ pivot)
- **Resume/CV:** achievements + metrics + keyword ตรง JD → ดู `cv-judgment`
- **LinkedIn/bio:** เรื่องเล่า + เสียงตัวเอง + เปิดกว้างกว่า
- **เตรียมสัมภาษณ์:** ดึง stories-bank (STAR) ตอบ behavioral question
- **เปลี่ยนสาย:** คัด **transferable skills + values** ที่ carry ข้ามสายได้ → คู่ `ikigai-finder`
- **คอนเทนต์/แบรนด์:** unique angle + เรื่องเล่า → คู่ `content-creator-judgment`
- **ป้อน AI:** วางโปรไฟล์ให้ AI ก่อนสั่งงาน → ช่วยได้ตรงขึ้น (คู่ `ai-assistant-calibration`)

### Fork 5 — ดึง "ของที่ตัวเองมองข้าม" (hidden value)
- คนเก่งมัก undersell ("ใครๆ ก็ทำได้") → AI ต้องชี้: **สิ่งที่คุณทำเป็นธรรมชาติแต่คนอื่นทำไม่ได้ = เพชร**
- ขุดจาก: side project · งานอาสา · สิ่งที่ทำตอนว่าง · ปัญหาที่แก้ให้คนอื่นบ่อย · ทักษะข้ามสาย
- **จุดตัด (intersection) = ความ unique:** "อาชีพ A + ทำ B เป็น" (เช่น คนสายแล็บที่ code/ขาย/เขียนเป็น) — หายากกว่าเก่งอย่างเดียว

### Fork 6 — ซื่อสัตย์ + เป็นเอกสารมีชีวิต (ไม่ใช่ AI เลียแข้งเลียขา)
- **evidence-based:** ทุก claim ต้องมี story/หลักฐาน — ไม่ใช่ "ผมเป็นผู้นำ" ลอยๆ
- รวม **weakness/gap จริง** ไว้ด้วย (เพื่อพัฒนา + เตรียมตอบคำถามสัมภาษณ์)
- **living doc:** อัปเดตเมื่อมีผลงาน/บทเรียนใหม่
- 🔒 **privacy:** โปรไฟล์ = ข้อมูลส่วนตัวอ่อนไหว เก็บที่ปลอดภัย **อย่าวางในที่สาธารณะ/แชร์มั่ว**

---

## กับดัก (Anti-patterns)
- **เก็บแต่ fact (จบอะไร ทำงานไหน) ไม่เก็บ story/ตัวเลข** → resume จืด ไม่มีน้ำหนัก
- **เชื่อคำตอบผิวแรก ไม่ขุดต่อ** → พลาดเพชรที่ฝังอยู่
- **claim ลอยๆ ไม่มีหลักฐาน** ("hardworking/team player") → ใช้สัมภาษณ์แล้วแตก
- **ปล่อยให้ AI ชมเกินจริง** → โปรไฟล์ปลอม เสียเครดิตตอนเจอของจริง
- **ไม่ quantify** ทั้งที่ตัวเลขมี
- **undersell ตัวเอง** — ปล่อยผ่านสิ่งที่ unique เพราะคิดว่าธรรมดา
- **เก็บโปรไฟล์ในที่ public / แชร์ข้อมูลอ่อนไหวมั่ว** (🔒)
- **ทำครั้งเดียวแล้วทิ้ง** — ควรเป็น living doc ที่อัปเดต
- **slice ผิดปลายทาง** — ยัด master ทั้งก้อนลง resume แทนที่จะคัดเฉพาะที่ตรงงาน

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมของคุณเอง เช่น:
> - *"คำถามสัมภาษณ์ตัวเองที่ขุดของลึกได้ดีที่สุด คือ..."*
> - *"จุดแข็งที่ผมเคยมองข้าม แต่คนอื่นชี้ให้เห็น คือ..."*
> - *"intersection ที่ทำให้ผมต่างจากคนอื่นในสายงาน คือ..."*

---
*ช่วยสัมภาษณ์/รวบรวมข้อมูลตัวคุณเองเพื่อการศึกษา/วางแผนอาชีพ ไม่ใช่ที่ปรึกษาอาชีพ/HR ทางการ — 🔒 โปรไฟล์ที่ได้เป็นข้อมูลส่วนตัวอ่อนไหว เก็บในที่ปลอดภัย อย่าวางในที่สาธารณะ/แชร์/อัปขึ้น repo สาธารณะ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: lab-clinic-business-judgment ═════════ -->

---
skill: lab-clinic-business-judgment
title: ธุรกิจคลินิกแล็บ MT — เลือกโมเดล + กันคู่แข่ง (MT Lab-Clinic Business)
type: ADVISE
needs: any
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "กรอบคิดธุรกิจคลินิกแล็บ เพื่อการศึกษา ไม่ใช่คำแนะนำการลงทุน/กฎหมาย — ตัวเลข ต้นทุน เงื่อนไขจดทะเบียน และนโยบายรัฐเปลี่ยนได้ ต้อง verify เองก่อนตัดสินใจ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ธุรกิจคลินิกแล็บ MT — เลือกโมเดล + กันคู่แข่ง

สำหรับ MT ที่คิดเปิด/บริหารคลินิกเทคนิคการแพทย์เอง — เน้น **"เลือกโมเดลไหนเมื่อไหร่ + พลาดตรงไหนถึงเจ๊ง"** ไม่ใช่ตำราตลาด

> **กฎ #1:** moat ของคลินิกแล็บ **ไม่ใช่เครื่องมือ** (ใครก็ซื้อได้) — แต่คือ **ความชอบธรรมวิชาชีพ (จดทะเบียน + ดำเนินโดย ทนพ. + รับรองสภา) + "มีคนอธิบายผล/ดูแลต่อเนื่อง" + เชื่อมระบบรัฐได้**. แข่งด้วยราคาอย่างเดียว = แพ้เสมอ
> **กับดัก #1:** เก่งแล็บ แต่อ่อน business/brand/marketing/law → นั่นคือจุดแพ้-ชนะจริง ไม่ใช่คุณภาพผลตรวจ (ทุกคนแล็บดีพอกัน)
> โยง: `mt-career-judgment` (เส้นทางเป็นเจ้าของ) · `ivd-sales-judgment` (ฝั่งขายของให้คลินิก) · `finance-judgment` (unit economics + CFO) · `mt-law-ethics-judgment` (ขอบเขต+จดทะเบียน) · `digital-judgment` (PDPA ข้อมูลคนไข้)

## ใช้เมื่อ
- คิดเปิดคลินิกแล็บ / ขยายสาขา / เลือกโมเดลธุรกิจ
- ตัดสินว่าจะเข้าระบบรายได้รัฐ (เช่น Lab Anywhere/สปสช.) ไหม
- ประเมินว่าคลินิกจะรอดภัยคุกคาม (รพ.เปิดศูนย์เอง, แล็บใหญ่, POCT, self-test, price war) ยังไง
- (สาย sales) อยากอ่านใจ buyer = เจ้าของคลินิกแล็บ ก่อนเข้าไปขาย

## วิธีใช้
เล่าสถานการณ์ (ทุน, ทำเล, ลูกค้าเป้า, มี รพ.คู่ไหม) → จะได้ fork ที่ต้องตัดสิน + กับดักที่ต้องเลี่ยง + จุดที่ต้องไปหาตัวเลขจริงก่อน

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### Fork 1 — เลือกโมเดล: Premium-Longevity vs Volume-รัฐ vs Hybrid
ถามก่อน: **มี brand/demand แล้วหรือยัง? ทุนหนาแค่ไหน? ทำเลใกล้ รพ.คู่ไหม?**

| | Premium / Longevity | Volume / รัฐ (เช่น Lab Anywhere) |
|---|---|---|
| ลูกค้า | รายได้สูง, องค์กร, ต่างชาติ | mass, สิทธิรัฐ, ใกล้บ้าน |
| รายได้ | package แพง + **subscription/recurring** | fee-per-test **ต่ำ → ต้อง volume** |
| margin | หนา | บาง |
| moat | brand + แปลผล + experience | จดทะเบียน + LIS-HIS + อยู่ในระบบรัฐ |
| เสี่ยง | ต้องสร้าง demand เอง, พึ่ง branding | พึ่งนโยบาย, margin บาง, ผูก รพ.คู่ |

- **verdict:** ส่วนใหญ่ **hybrid ฉลาดสุด** — เปิดด้วย volume/รัฐ ก่อน (cashflow + ความชอบธรรม + คนเดินผ่าน) → **upsell premium ทับ** เพื่อ margin. อย่าเริ่มด้วย premium ล้วนถ้ายังไม่มี brand/demand จริง (จะไม่มีลูกค้า)
- **recurring > one-shot:** โมเดลที่อยู่รอด = ขาย "การติดตามต่อเนื่อง" (ตรวจซ้ำตามรอบ + coaching) ไม่ใช่ "ตรวจครั้งเดียวจบ"

### Fork 2 — moat: กันคู่แข่งด้วยอะไร (รพ.เปิดศูนย์เอง / แล็บใหญ่ / POCT / self-test / price war)
- **moat ที่จริง 3 ชั้น:** (1) **ความชอบธรรมวิชาชีพ** — จดทะเบียนสถานพยาบาล + ดำเนินโดย ทนพ. + รับรองสภา = กำแพงกันทุนนอก/คนไม่ใช่ MT (2) **"มีคนอธิบายผล + ดูแลต่อเนื่อง"** = จุดที่ชนะ self-test/POCT (มนุษย์ + วิชาชีพ ที่กล่องตรวจให้ไม่ได้) (3) **LIS-HIS integration** = ตั๋วเข้าระบบรัฐ/รับ outsource จาก รพ.
- **กับดัก:** แข่งราคาอย่างเดียว = race to the bottom (มีคนถูกกว่าเสมอ) · เครื่องทันสมัยอย่างเดียวไม่ใช่ moat (ทุนใหญ่ซื้อทับได้)
- **รายได้ที่มองข้าม:** รับ **outsource งานแล็บจาก รพ./คลินิกอื่น (B2B reference lab)** = volume + stable มากกว่า walk-in อย่างเดียว

### Fork 3 — ปิด business-gap ที่ MT ส่วนใหญ่ขาด (จุดแพ้-ชนะจริง)
MT เก่ง bench แต่มัก**อ่อน: business model · branding · digital marketing · กฎหมาย · การเปลี่ยนผลตรวจเป็นคุณค่า**
- **verdict:** อย่าทุ่มกับ "ซื้อเครื่องดีกว่า" — ทุ่มปิด gap นี้ก่อน (เรียน/จ้าง/หาหุ้นส่วนสาย business+marketing+law)
- **ใช้ AI ปิด gap:** automate report/แปลผลให้คนเข้าใจ/การตลาด = "AI ไม่แทน MT แต่แทนคนที่ไม่ใช้ AI". คนที่มี data/AI skill = ได้เปรียบเชิงโครงสร้างตรงนี้
- เกณฑ์คลินิกที่รอดระยะยาว = **น่าเชื่อถือสุด + อธิบายผลดีสุด + เข้าถึงง่ายสุด + ใช้ข้อมูลเป็นสุด** ไม่ใช่ "เครื่องใหม่สุด"

### Fork 4 — เข้าระบบรายได้รัฐ (Lab Anywhere/สปสช.) ไหม
- **คืออะไร (ระดับตัดสินใจ):** ท่อรายได้รัฐที่ให้คลินิก MT เจาะ/ตรวจแล็บผู้ป่วยเรื้อรัง (OP) + งานป้องกันโรค (PP) เบิกตรงจาก สปสช. ไม่ผ่าน รพ. จ่ายเป็นรอบ
- **เข้าเมื่อ:** อยู่ใกล้ รพ.คู่ที่เชื่อม **LIS-HIS** ได้ · ทำ **volume** ได้จริง · ผ่านมาตรฐาน (เช่น MOPH Standard) · พร้อม setup (ระบบพิสูจน์ตัวตน/ขึ้นทะเบียน/เบิกจ่าย)
- **กับดัก:** margin **บางมาก** (fee/test ต่ำ) → ไม่มี volume = ขาดทุน · พึ่งนโยบายรัฐ = เปลี่ยน/ยกเลิกได้ · setup cost (gateway/ระบบ/มาตรฐาน) สูง · compliance บังคับ (เช่น **รายงานค่าวิกฤตทันที + บันทึกทุกครั้ง**)
- **อย่าเข้าใจผิด:** นี่คือ **cashflow ฐาน + ความชอบธรรม** ไม่ใช่ตัวทำกำไรหลัก — ใช้คู่กับ premium ที่ margin หนา (Fork 1)

### Fork 5 — (สาย sales) อ่านใจ buyer = เจ้าของคลินิกแล็บ
- **pain เขา:** โดนกดราคา · รพ.เปิดศูนย์แข่ง · POCT/self-test แย่งงาน · ขาด business skill
- **เขาอยากซื้อ:** เครื่องที่ **ลด cost/คน** · panel มูลค่าสูง (longevity/preventive: ApoB, hs-CRP, sd-LDL, insulin, HbA1c, Vit D ฯลฯ) · QC/calibration/service contract · **LIS/middleware/gateway/Kiosk** · AI ช่วย report/marketing
- **verdict:** อย่าเปิดด้วย "เครื่องเราแม่นกว่า" — เปิดด้วย **pain บริหารของเขา + value/test + ลด cost** (ดู `ivd-sales-judgment` Fork เปิดด้วย pain)

### Fork 6 — ก่อนลงเงินจริง: หา data ที่ vision deck ไม่มี
สไลด์/เสวนาธุรกิจคลินิกมักเป็น **vision + workflow ไม่มี financial model** → ต้องหาเองก่อนตัดสิน:
- **market size จริง** (ไม่ใช่ "ตลาดโต rapidly" ที่ไม่มี source)
- **unit economics:** ค่าเครื่อง/ค่า reagent ต่อ test, ราคาขาย, **break-even volume**
- **กฎหมาย/ภาระผูกพัน:** จดทะเบียนสถานพยาบาล, ขอบเขตวิชาชีพ, เงื่อนไขจ้างงาน/บอนด์ (ถ้ามี)
- **setup cost:** มาตรฐาน (MOPH/ISO 15189), LIS-HIS, ระบบเบิกรัฐ
- **กับดัก:** เชื่อ vision deck เป็น business plan = เจ๊ง (ไม่มี unit economics). ดู CFO/break-even จริงก่อน (โยง `finance-judgment`)

---

## กับดัก (Anti-patterns)
- **เริ่ม premium ล้วนทั้งที่ยังไม่มี brand/demand** → ไม่มีลูกค้า เงินจม
- **แข่งด้วยราคาอย่างเดียว** → race to the bottom, ทุนใหญ่บีบตาย
- **เชื่อ vision deck เป็น business plan** → ไม่มี unit economics/break-even = เจ๊งเงียบ
- **มองข้าม LIS-HIS integration** → เข้าระบบรัฐ/รับ outsource ไม่ได้ = ตัดท่อรายได้ volume ทิ้ง
- **เก่งแล็บอย่างเดียว ละเลย business/brand/law** → จุดแพ้จริงไม่ใช่คุณภาพผล
- **พึ่ง Lab Anywhere/รัฐ เป็นกำไรหลัก** → margin บางเกิน, นโยบายเปลี่ยนได้ = เปราะ
- **คิดว่า moat = เครื่องมือ** → ทุนใหญ่ซื้อทับได้; moat จริง = วิชาชีพ + จดทะเบียน + ความสัมพันธ์ + ระบบ

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมตัวเลข/ประสบการณ์จริงในสายคุณ เช่น:
> - *"unit economics คลินิกผม: ค่า reagent ต่อ test ... ราคาขาย ... break-even ที่ ... test/วัน"*
> - *"เข้า Lab Anywhere/ระบบรัฐแล้วเจอจริงคือ ... (setup ที่ยากสุด / margin ที่เหลือจริง)"*
> - *"เงื่อนไขจดทะเบียน/กฎหมายที่คนมักพลาด คือ ..."*

---
*กรอบคิดธุรกิจคลินิกแล็บ เพื่อการศึกษา ไม่ใช่คำแนะนำการลงทุน/กฎหมาย — ตัวเลข ต้นทุน เงื่อนไขจดทะเบียน และนโยบายรัฐเปลี่ยนได้ ต้อง verify เองก่อนตัดสินใจ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: lab-management-judgment ═════════ -->

---
skill: lab-management-judgment
title: โค้ชบริหารแล็บ — QMS/accreditation/QC strategy/งบ (Lab Management Judgment)
type: ADVISE               # ช่วยตัดสินใจบริหารแล็บ ไม่ใช่ตำรา ISO
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดบริหารแล็บเพื่อการศึกษา ไม่ใช่ที่ปรึกษา accreditation/จัดซื้อ/กฎหมายทางการ — ข้อกำหนด ISO/มาตรฐานจริงต้องอ้างฉบับล่าสุด + ผู้ตรวจประเมิน/ผู้มีอำนาจของหน่วยงาน · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชบริหารแล็บ — QMS / accreditation / QC strategy / งบ

ตัดสินใจระดับ "บริหารแล็บ" — เลือก accreditation ไหน · วางแผน QC ให้ประหยัด · สั่งน้ำยายังไง · ของบเครื่องลงช่องไหน · verify เครื่องใหม่ ไม่ใช่ท่องข้อกำหนด ISO (= commodity ดูมาตรฐานตัวจริง)

> **กฎ #1: ตั้ง QC limit จาก mean/SD ที่แล็บคำนวณเอง — ห้ามใช้ค่าจากกล่องน้ำยา/insert (นั่นคือ peer range ไม่ใช่ performance เครื่องคุณ → limit หลวม จับ error ไม่ได้).**
> **กับดักขั้นกว่า (จุดที่พลาดจริง): "ใช้ค่าแล็บเอง" ยังไม่พอ — ต้องเก็บ ≥20 จุด คนละวัน ≥20 วัน. เก็บ 20 จุดรวดเดียววันเดียว = ได้แค่ within-run SD (แคบเกิน) → false reject ท่วม. และพอ "เปลี่ยน lot control/น้ำยา" ต้องตั้ง mean/SD ใหม่ ห้าม carry ค่าเก่าข้าม lot.**
> นี่คือชั้น "วางระบบ/วางแผน" เหนือหน้า bench — QC accept/reject รายวันดู `clinchem-judgment`; skill นี้คือ **ออกแบบ QC ทั้งระบบ + ผ่าน audit + คุมต้นทุน**
> กรอบร้อยทุกอย่าง = **Total Testing Process: Pre → Analytical → Post** (~46-68% error อยู่ที่ pre-analytical, commonly ~62%)

## ใช้เมื่อ
- เตรียม/ต่ออายุ accreditation (ISO 15189 / LA / HA) — เลือกระดับ + เตรียมเอกสาร
- QC แพง/รันซ้ำเปลือง → วางแผน QC ตาม sigma/IQCP
- สั่งน้ำยา-คุมสต็อก · ของบเครื่อง/น้ำยา · รับเครื่องใหม่ (verification) · จัดการความเสี่ยง/TAT

## วิธีใช้
วาง skill นี้ + เล่าสถานการณ์ (กำลัง accredit / QC เปลือง / จะซื้อเครื่อง) → AI ชี้ทางเลือก + กับดักบริหาร

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — เลือก accreditation ระดับไหน
- **งบจำกัด/เริ่มต้น** → มาตรฐานงานเทคนิคการแพทย์ (ไทย) ก่อน
- **ต้องการ recognition สากล / รับงานนอก / วิจัย** → **ISO 15189** (เฉพาะ medical lab; ต่างจาก 17025 lab ทั่วไป / 9001 องค์กรทั่วไป)
- **ยกระดับทั้ง รพ.** → HA (รพ.) + LA (แล็บ) ไปด้วยกัน
- 15189 = Management requirements (QMS/document control/CAPA/internal audit/management review) + Technical (บุคลากร/เครื่อง-น้ำยา/pre-exam-post/รายงานผล/LIS) · ความปลอดภัยใช้ **ISO 15190** คู่

### Fork 2 — IQC vs EQA: คุมคนละอย่าง อย่าสับ
- **IQC** (control ทุกวันก่อนตรวจคนไข้) คุม **precision** → ดู %CV, Levey-Jennings · ⚠️ **ใช้ mean/SD ที่แล็บคำนวณเอง ≥20 จุด เก็บคนละวัน ≥20 วัน (CLSI C24) — ห้ามใช้ค่าจากกล่องน้ำยา · ตั้งใหม่ทุกครั้งที่เปลี่ยน lot**
- **EQA/PT** (ส่งเทียบ peer) คุม **accuracy** → ได้ **bias** = (mean lab − mean peer)/mean peer ×100
- กับดัก: **IQC ผ่านสวยแต่ inaccurate ได้** (bias คงที่ L-J จับไม่ได้ — ต้องพึ่ง EQA)

### Fork 3 — Sigma-based QC planning (จุดประหยัดจริง)
```
Sigma = [TEa(%) − Bias(%)] / CV(%)   ← ทั้ง 3 ตัวต้องหน่วยเดียวกัน (% หรือ conc.)
```
ยิ่ง sigma สูง = method ดี = **คุม QC น้อยลงได้ = ประหยัด control/แรง/เวลา**
| Sigma | QC ที่พอ |
|---|---|
| **6** | 1₃s, N=2 (เกือบไม่ต้องคุมหนัก) |
| **5** | + 2of3₂s, R₄s |
| **4** | + 4₁s |
| **<4** | ทุกกฎ + N=6 (เปลือง = สัญญาณ method แย่ → ปรับปรุง/เปลี่ยน) |
- **IQCP** (Individualized QC Plan, CLSI EP23): วาง QC ตามความเสี่ยงจริงของ 5 จุด — **Specimen / Operator / Reagent / Environment / Measuring system** → ลด QC ได้อย่างมีหลักฐาน

### Fork 4 — error อยู่ phase ไหน → ลงทุนแก้ตรงนั้น
- **Pre (~60-70%)** หลอดผิด/สัดส่วนเลือด-สารกันแข็ง/hemolysis/label ผิด → คุมด้วยระบบ/automation/barcode (คุ้มสุด)
- **Analytical** calibration drift/lot เสื่อม/อุณหภูมิ → MT + QC
- **Post** พิมพ์ผิด/ไม่แจ้ง critical/TAT เกิน → LIS auto-verify
> อย่าทุ่มแก้ analytical ทั้งที่ปัญหาจริงอยู่ pre-analytical

### Fork 5 — สั่งน้ำยา/คุมสต็อก
- ปัจจัย: consumption rate · **packing size** (กล่องใหญ่ถูก/เทสต์ แต่หมดอายุก่อนใช้หมด = เสียเปล่า) · expiry + **FEFO** · พื้นที่เก็บ controlled
- **fork:** สั่งมาก (ส่วนลด แต่เสี่ยงหมดอายุ + แช่เงินทุน) vs สั่งบ่อย (สดเสมอ แต่เสี่ยงขาด + ค่าขนส่ง) → ขึ้นกับ stability น้ำยา + ความแน่นอน demand

### Fork 6 — ของบ: เครื่อง vs น้ำยา คนละกระเป๋า
- **เครื่อง = งบลงทุน (capital)** → อนุมัติยาก รอบยาว ผ่านกรรมการ จัดซื้อภาครัฐ (TOR/e-bidding)
- **น้ำยา = งบดำเนินงาน (operating)** → คล่อง อนุมัติเร็ว
- ⚠️ เสนอผิดกระเป๋า = ลูกค้า/ผู้บริหารอนุมัติไม่ได้ → ดู `ivd-sales-judgment` สำหรับ reagent rental ที่ย้าย capex→opex

### Fork 7 — รับเครื่อง/method ใหม่: Verification ≠ Validation
- **Validation** = ผู้ผลิตพิสูจน์แล้วว่า method ใช้ได้ · **Verification** = **แล็บทวนสอบเองก่อนใช้จริง** ว่าได้ตามที่อ้างในสภาพแล็บตน (ISO 15189 บังคับ) — precision/accuracy/linearity/reportable range
- เครื่องใหม่ / method ใหม่ / เปลี่ยน lot ใหญ่ → re-verify

### Fork 8 — Risk management + LIS/TAT
- ระบุความเสี่ยง → ประเมิน **Likelihood × Impact** → จัดลำดับ → จัดการ: **ยอมรับ / ลด-คุม / โอน (ประกัน-outsource) / เลี่ยง** → ทบทวน
- **LIS/LIMS** (ISO บังคับ): สิทธิ์เข้าถึง, ใคร approve, กันแก้-สูญหาย, **audit trail**, ความลับคนไข้ (PDPA)
- **TAT** = KPI ที่ ward/แพทย์กดดันสุด → automation/STAT pathway ลด TAT

---

## กับดัก (Anti-patterns)
- ใช้ **mean/SD จากกล่องน้ำยา** ทำ QC (ต้องของแล็บเอง ≥20 จุด คนละวัน ≥20 วัน)
- เก็บ **20 จุดรวดเดียววันเดียว** → SD แคบเกินจริง (ขาด between-day) → false reject ท่วม · หรือ **carry mean/SD เก่าข้าม lot ใหม่** → limit ผิดทั้งชุด
- **2SD กับทุก test** → false reject ท่วม รันซ้ำเปลืองเงิน (สับ warning 1₂s กับ reject)
- **QC out → รันซ้ำจนผ่าน** โดยไม่หา root cause → ปล่อย systematic error หลุด
- **EQA fail = โทษเครื่องทันที** → อาจ pre-analytical / ลงค่าผิด / lot
- **สั่งล็อตใหญ่เพราะถูก/หน่วย** → หมดอายุก่อนใช้ + แช่เงินทุน
- **มอง pre-analytical ว่าไม่ใช่ปัญหาแล็บ** ทั้งที่เป็น error อันดับ 1
- **สับ verification กับ validation** → รับเครื่องโดยไม่ทวนสอบเองก่อนใช้

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT หัวหน้าแล็บ) ตอนเตรียม ISO 15189 จุดที่ผู้ตรวจจับบ่อยคือ... เตรียมโดย..."*
> - *"sigma ของ analyte ... ในแล็บผม = ... เลยตั้ง QC เป็น..."*
> - *"กับดักสั่งน้ำยา/สต็อกที่ผมเคยพลาด คือ..."*

---
*ช่วยคิดบริหารแล็บเพื่อการศึกษา ไม่ใช่ที่ปรึกษา accreditation/จัดซื้อ/กฎหมายทางการ — ข้อกำหนด ISO/มาตรฐานจริงต้องอ้างฉบับล่าสุด + ผู้ตรวจประเมิน/ผู้มีอำนาจของหน่วยงาน · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: manuscript-judgment ═════════ -->

---
skill: manuscript-judgment
title: โค้ชเขียน manuscript/proposal — ให้ผ่าน reviewer (Manuscript & Publishing Judgment)
type: ADVISE               # ช่วยตัดสินใจการเขียน/ตอบ reviewer ไม่ใช่เขียนแทน
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดเรื่องโครงสร้าง/การเขียน manuscript เพื่อการศึกษา ไม่ใช่ที่ปรึกษาวิจัย/บรรณาธิการทางการ — เนื้อหา/ความถูกต้องทางวิชาการ ต้องผ่านอาจารย์ที่ปรึกษา + peer review จริง · ผู้นำไปใช้รับผิดชอบงานที่เผยแพร่เอง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชเขียน manuscript/proposal — ให้ผ่าน reviewer

เขียน proposal/เล่ม/เปเปอร์ แล้วงงว่า "แต่ละส่วนต้องมีอะไร · ทำไมโดน reject · originality อยู่ตรงไหน" → โค้ชนี้ช่วยตามเกณฑ์ reviewer จริง

> **กฎ #1: objective = results = conclusion ต้องตรงกัน 3 ชั้น** — objective ถามอะไร, results ตอบอันนั้น, conclusion สรุปแค่อันนั้น. ไม่ตรง = reviewer จับทันที = reject.
> **กับดัก #1 (เวอร์ชันยาก ที่คนมักหลุด): conclusion พูดเกินข้อมูล** — ถึงทั้ง 3 จะดู "ตรงหัวข้อ" กัน แต่ถ้า conclusion อ้าง **กว้างกว่า/แรงกว่า** ที่ design+results รองรับ ก็ reject. กฎทั่วไป: **claim ทุกประโยคต้องมี data หนุนตรงๆ** — design correlation ห้ามสรุป causal · pilot/n เล็ก/กลุ่มเดียว ห้าม generalize หรือแนะนำใช้คลินิก · in-vitro ห้ามฟันธง in-vivo. ตัด/ลดน้ำหนักคำให้พอดีข้อมูล.
> รองลงมา: paper โดน reject เพราะ **"นำเสนอแย่/ไม่ชัด" บ่อยกว่าเพราะ "ไม่ใหม่"** — clarity สำคัญกว่าที่คิด.
> ก่อนเขียน: ตั้งโจทย์ → `r2r-research-proposal` · design → `research-design-judgment` · สถิติ → `choose-stat-test` + `r2r-stats`

## ใช้เมื่อ
- เขียน proposal / manuscript / thesis / poster
- ตอบ reviewer / แก้ตาม comment
- ไม่แน่ใจว่าแต่ละ section ต้องมีอะไร / ทำไมโดนตีกลับ

## วิธีใช้
วาง skill นี้ + วาง draft/section หรือเล่าผลงาน → AI ชี้ว่าแต่ละส่วนครบ/ตรงเกณฑ์ไหม + จุดที่ reviewer จะจับ

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

### โครงสร้าง IMRaD + หน้าที่ของแต่ละส่วน
Title → Abstract → Introduction → Methods → Results → Discussion → Conclusion → References (+ Tables/Figures)
- **Title:** ≤20 คำ, บอกเนื้อหาจริง, ไม่ claim เกินข้อมูล
- **Abstract:** ≤250 คำ — what/how/major results/conclusion · **ทุกอย่างใน abstract ต้องมีในตัวเล่ม** (ห้ามมีข้อมูลใหม่)
- **Introduction:** ปู background พอประเมินผลได้ + ความสำคัญ + ปัญหา + **objective ชัด** (ไม่ใช่ review ยาว)
- **Methods:** ละเอียดพอ **ทำซ้ำได้ (reproducible)** · method เดิม cite, method ใหม่เขียนละเอียด · **ระบุ stat analysis**
- **Results:** ข้อมูลตัวแทน (ไม่ซ้ำซาก), significant digits ถูก, ตาราง/รูป**ไม่ซ้ำข้อมูลกัน**, เลขตาราง/รูปตามลำดับที่อ้าง, **ผลตรงกับ objective**
- **Discussion:** เทียบผลกับงานเดิม (เหมือน/ต่างยังไง) + ชี้ว่า **อะไรใหม่ (originality)** ไม่ใช่ทวนผล
- **Conclusion:** ไม่ใช่ summary/ซ้ำ abstract · ต้อง justified by data · เน้น key point + implication
- **References:** ครบ ถูก format, current + key

### เกณฑ์ acceptance / reject (คิดแบบ reviewer)
- **ผ่าน:** Originality + Scientific quality (hypothesis ดี, design sound, stat เหมาะ) + **Clarity** + importance ต่อสาขา
- **reject ทันที:** ไม่น่าสนใจต่อ readership · ไม่มีข้อมูลใหม่ · ผล trivial/ซ้ำคนอื่น · design+method แย่ · สรุปผิด · **สงสัย misconduct (fabrication/plagiarism)**

### กฎทอง: objective = results = conclusion (เช็คก่อนทุกอย่าง)
ทั้ง 3 ต้อง**ตรงกัน** — objective ถามอะไร, results ตอบอันนั้น, conclusion สรุปอันนั้น. ขาดความตรงกัน = reviewer จับทันที
- **ชั้นยาก — conclusion ห้ามล้ำเส้น data:** แม้ดู "ตรงหัวข้อ" แล้ว ยังต้องเช็คว่า conclusion **ไม่อ้างเกิน** ที่ design+results ให้. เส้นที่มักหลุด: correlation→อย่าพูด causal · association→อย่าพูด "ทำให้/รักษา" · n เล็ก/pilot/sample กลุ่มเดียว→อย่า generalize ทั้งประชากร · in-vitro/animal→อย่าฟันธงคน · "trend/ไม่ sig"→อย่าสรุปเหมือน sig. แก้ = ลดน้ำหนักคำ ("may/suggests" ไม่ใช่ "proves") ให้พอดี data จริง.

### Poster / oral presentation
- format: Title/Intro/Objective/Methods/Results/Conclusion/Ack
- อ่านได้ที่ 1.5-2 ม. (Title ~80pt, body ~24pt) · ≤6 bullets/หน้า · ≤2 fonts · กราฟ ≤6 เส้น บอกแกน x,y
- ⚠️ **graphical honesty** — อย่าบีบ/ตัดแกนกราฟให้ผลดูเว่อร์กว่าจริง

---

## กับดัก (Anti-patterns)
- **objective ≠ results ≠ conclusion** — ถามอย่าง ตอบอีกอย่าง สรุปอีกอย่าง = reject
- **conclusion ล้ำเส้น data (over-claim)** — กว้าง/แรงเกินที่ design+results หนุน: causal จาก correlation, generalize จาก n เล็ก, ฟันธงคนจาก in-vitro = reject (เนียนกว่าข้อบน เพราะดูตรงหัวข้อ)
- **abstract มีข้อมูลใหม่** ที่ไม่อยู่ในเล่ม / **conclusion ซ้ำ abstract** เฉยๆ
- **Discussion แค่ทวนผล** ไม่เทียบงานเดิม + ไม่ชี้ originality
- **Methods ทำซ้ำไม่ได้** — ไม่ระบุ stat / เครื่อง / เกณฑ์ → reviewer ขอแก้
- **เชื่อว่า "ใหม่" พอแล้ว** — clarity/การนำเสนอแย่ = เหตุ reject อันดับต้นๆ
- **graphical dishonesty** — บีบแกน, error bar ใช้ SEM แทน SD ให้ดูสวย
- **plagiarism / fabrication** — คัดลอก/แต่งข้อมูล = misconduct (จบเห่)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT) comment ที่ reviewer วารสารสายผมชอบให้ คือ... แก้โดย..."*
> - *"section ที่ผมเคยโดนตีกลับบ่อยสุด คือ... เพราะ..."*

---
*ช่วยคิดเรื่องโครงสร้าง/การเขียน manuscript เพื่อการศึกษา ไม่ใช่ที่ปรึกษาวิจัย/บรรณาธิการทางการ — เนื้อหา/ความถูกต้องทางวิชาการ ต้องผ่านอาจารย์ที่ปรึกษา + peer review จริง · ผู้นำไปใช้รับผิดชอบงานที่เผยแพร่เอง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: marketing-judgment ═════════ -->

---
skill: marketing-judgment
title: โค้ชการตลาด B2B — STP/buying center/pricing/positioning (Marketing Strategy Judgment)
type: ADVISE               # ช่วยคิดกลยุทธ์การตลาด ไม่ใช่ตำรา 4P
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดกลยุทธ์การตลาด/ขายเพื่อการศึกษา ไม่ใช่คำแนะนำธุรกิจ/กฎหมายทางการ — ห้ามใช้กล่าวอ้างเกินจริง/ผิดจริยธรรมวิชาชีพ · ผู้นำไปใช้รับผิดชอบการกระทำที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชการตลาด B2B — STP / buying center / pricing / positioning

วางกลยุทธ์การตลาด/ขายของแพง-ซับซ้อน (เช่น IVD/diagnostics) — "วางลำดับอะไรก่อน + พลาดตรงไหนเสียดีล" ไม่ใช่ท่องนิยาม 4P (= commodity ดูตำรา)

> ✅ **กฎ #1: STP ก่อน 4P เสมอ** — Segment → Target → Position ให้เสร็จ *ก่อน* แตะ ราคา/โปรโมชัน/ช่องทาง (ตั้งราคา-ทำโฆษณาก่อนรู้ว่าขายใคร = ผิดลำดับ)
> 🚫 **กับดัก #1: ขาย feature/สเปค แทน "คุณค่า/pain ของลูกค้า"** (Marketing Myopia) — เปิดด้วยลูกค้าเจ็บอะไร ไม่ใช่ list สเปค; และ B2B ต้องแมป "กลุ่มคนตัดสินใจ" ครบ ไม่ปิดที่คนเดียว
> ชั้นนี้ = **กลยุทธ์** (positioning/pricing/ใครตัดสินใจ) — ปิดดีล IVD (budget-pocket/CPR/spec-in/after-sales) ดู `ivd-sales-judgment` · retention ดู `crm-judgment` · ROI/BEP ดู `finance-judgment`

## ใช้เมื่อ
- วาง account plan / เลือก segment-target / วาง positioning ของสินค้า
- ตั้งราคา/เจอสงครามราคา · เลือกเครื่องมือสื่อสาร (push/pull)
- งง "ทำไมขายไม่ได้ทั้งที่ของดี"

## วิธีใช้
วาง skill นี้ + เล่าสินค้า/ลูกค้า/สถานการณ์ → AI ชี้ลำดับกลยุทธ์ + กับดักที่ทำดีลล่ม

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — Mindset: ขาย "คุณค่า/need" ไม่ใช่ feature
- ⚠️ **Marketing Myopia** = หลงรักสเปคตัวเอง ลืมถามว่าลูกค้าเจ็บอะไรจริง → เปิดด้วย pain ของลูกค้า ไม่ใช่ feature list
- **Needs (ต้องมีจริง) vs Wants (อยากได้ยี่ห้อนี้) vs Demand (มีงบ+อำนาจอนุมัติ)** → **เช็ค demand เสมอ** อย่าเสียเวลากับคน "อยากได้แต่ไม่มีงบ"

### Fork 2 — STP ก่อน 4P (ห้ามสลับ)
- **Segment → Target → Position → แล้วค่อย 4P** · เกณฑ์ segment ที่ทรงพลังสุดมัก **Benefit sought** (ไม่ใช่แค่ประชากรศาสตร์ที่แบ่งง่ายแต่ไม่ต่างจริง)
- **Targeting:** ทรัพยากรจำกัด + มี niche ชัด → **Concentrated** (โฟกัส niche แทนหว่านทั่ว)
- **Positioning statement:** "สำหรับ [กลุ่มเป้า] [แบรนด์] คือ [แนวคิด] ที่ [ความต่าง]" · เลือกความต่างที่ เหนือคู่แข่ง + ลอกยาก + ลูกค้าต้องการ + น่าเชื่อ
- ⚠️ positioning ที่ดี = สิ่งที่**ลูกค้ารับรู้** ไม่ใช่สิ่งที่เราพูด

### Fork 3 — B2B buying center: แมปให้ครบ (อย่าขายคนเดียวจบ)
| บทบาท | มักเป็นใคร |
|---|---|
| **User** | คนหน้างานที่ใช้จริง |
| **Influencer** | ผู้เชี่ยวชาญ/หัวหน้า/KOL |
| **Buyer** | ฝ่ายจัดซื้อ/พัสดุ |
| **Decider** | ผอ./คณะกรรมการ |
| **Gatekeeper** | เลขา/คนกรองว่าใครเข้าถึงใคร |
- User ชอบแต่ Decider ปัด = แพ้ · Decider โอเคแต่ Gatekeeper บล็อก = ไม่ได้เจอ → วางแผนสื่อสารต่างกันต่อคน
- **buy class:** Straight Rebuy (เจ้าเดิม=ป้อม / คู่แข่ง=เจาะยากสุด) · **Modified Rebuy (เจ้าเดิมขึ้นราคา/มีปัญหา service) = หน้าต่างเดียวที่เจาะ account คู่แข่งได้** · New Task = support ข้อมูลหนัก

### Fork 4 — Pricing: อย่าเปิดด้วยตัดราคา
- ⚠️ **ตัดราคา = สงครามราคา + anchor ต่ำถอนยาก** → ถ้าเริ่มแข่งราคา = ล้มเหลวในการสื่อ value → **ขายเป็น cost-per-result/Augmented แทน ราคา list**
- กรอบ: ต้นทุน = floor · การรับรู้คุณค่า = ceiling · **elasticity:** สินค้า inelastic (lock-in/ไม่มีของแทน) = ตั้ง/ขึ้นราคาได้ · elastic = อย่าแข่งราคา
- skimming (ใหม่/พรีเมียม ตั้งสูงก่อน) vs penetration (ตั้งต่ำเจาะ/ป้องคู่แข่ง) · **BEP = ต้นทุนคงที่ ÷ (ราคา − ต้นทุนผันแปร/หน่วย)**

### Fork 5 — Product layer + PLC
- **Core → Actual → Augmented:** ในตลาดสเปคพอกัน **เกมชนะที่ Augmented** (service/uptime/training/response time) — อย่าขายแค่ Actual (สเปคดิบ)
- **razor-blade:** ขายเครื่อง (capital กำไรบาง) เพื่อล็อก consumable (ซื้อซ้ำ = กำไรจริง) → **install base = สินทรัพย์**
- **PLC playbook ต่างตามช่วง:** Introduction = ให้ลอง/eval · Maturity = แข่ง service+ราคา → อย่าใช้ playbook เดียวทุกตัว

### Fork 6 — Promotion: Push vs Pull
- **B2B/เทคนิคสูง = Push + Personal Selling-led** (โฆษณา mass แทบไม่ใช้) → ใช้ trade show/seminar/KOL/case study/demo
- เลือกเครื่องมือตาม **Buyer Readiness** (Awareness→Knowledge→...→Purchase): ต้น = seminar/PR ให้ความรู้ · ท้าย = personal selling + demo ปิด
- ⚠️ **sales promotion (ลดแลกแจกแถม) ในวงการแพทย์ระวัง** — ชนกับ ethics (สินบน/ผลประโยชน์) → ดู `mt-law-ethics-judgment`

---

## กับดัก (Anti-patterns)
- **Marketing Myopia** — หลงสเปค ลืม pain ลูกค้า
- **ขายคนเดียว** — ไม่แมป buying center 5 บทบาท
- **เริ่ม 4P ก่อน STP** — mix ต้องตามหลัง positioning
- **ตัดราคาเอาดีล** — สงครามราคา; ขาย value/CPR แทน
- **มองคู่แข่งแค่ตรงๆ** — status quo / "อยู่กับเจ้าเดิม" / send-out คือคู่แข่งตัวจริง
- **ขายแค่ Actual** — ไม่ขาย Augmented = แพ้ตอนสเปคเท่ากัน
- **ลืม post-purchase** — ไม่จัดการ dissonance/onboarding → หลุดตอน renew
- **ข้ามเส้น ethics** — ของกำนัล/เคลมเกินจริง = เสี่ยงกฎหมาย + trust

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT sales) ดีลที่ปิดได้เพราะแมป buying center เจอว่า decider จริงคือ..."*
> - *"จังหวะ modified rebuy ที่ผมเจาะ account คู่แข่งได้ คือ..."*

---
*ช่วยคิดกลยุทธ์การตลาด/ขายเพื่อการศึกษา ไม่ใช่คำแนะนำธุรกิจ/กฎหมายทางการ — ห้ามใช้กล่าวอ้างเกินจริง/ผิดจริยธรรมวิชาชีพ · ผู้นำไปใช้รับผิดชอบการกระทำที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: ml-judgment ═════════ -->

---
skill: ml-judgment
title: โค้ช ML — เลือกโมเดล/metric/validation ให้ถูก (ML Model & Metric Judgment)
type: ADVISE               # ช่วยตัดสินใจเลือก ไม่ใช่ที่ท่องสูตร
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดเลือกโมเดล/metric/validation + เลี่ยงกับดัก ML เพื่อการศึกษา ไม่ใช่คำแนะนำทางการจากที่ปรึกษา ML — ต้องตรวจผลและ assumption ก่อนเชื่อ โดยเฉพาะงานคลินิก · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช ML — เลือกโมเดล/metric/validation ให้ถูก

จะทำ ML แล้วงงว่า "ใช้โมเดลไหน · วัดด้วย metric อะไร · validate ยังไงไม่ให้หลอกตัวเอง" → โค้ชนี้ตอบ 2 คำถาม: **"เลือกอะไรเมื่อไหร่"** กับ **"พลาดตรงไหน"**

> **กฎ #1:** อย่าเชื่อคะแนนที่ดูดีก่อนเช็ค **leakage** — `fit_transform` ทั้ง dataset ก่อน split หรือ tune บน test set = คะแนนสวยหลอก พังจริง · split ก่อนเสมอ, scaler/selector อยู่ใน Pipeline ที่ fit เฉพาะ train fold, test แตะครั้งเดียวตอนจบ
> **กับดัก #1:** **accuracy บน imbalanced หลอก** (โรคหายาก 2% → ทาย "ไม่โรค" หมด = acc 98% recall 0) → ใช้ precision/recall/F1 และ **PR-AUC** (ภายใต้ imbalance หนัก ROC-AUC ก็โป่งเกินจริง)
> สูตร/algorithm ลึก (entropy, backprop, EM) ตำรา/AI มีหมดแล้ว — ที่ทำให้พังจริงคือ **เลือกผิด** กับ **กับดักที่ดูถูกแต่หลอก** · skill นี้เก็บสองอันนั้น
> ภาพรวม "ควรทำโปรเจกต์ไหม + ล้มตรงไหน" ดู `data-project-survival` · "ใช้ test สถิติอะไร / N เท่าไร" ดู `choose-stat-test` + `sample-size-power`

## ใช้เมื่อ
- เลือกโมเดล / metric / validation scheme
- ดีบัก overfit/underfit, ผลดูดีเกินจริง
- ออกแบบการทดลอง ML (เช่นทำนายจากข้อมูล lab/genomic)

## วิธีใช้
วาง skill นี้ + เล่างาน/วางผล train-test → AI ชี้ทางเลือกที่เหมาะ + กับดักที่กำลังเสี่ยง

---

## วิธีเลือก (AI: ทำตามนี้) — Decision forks

### Fork 1 — งานแบบไหน? (paradigm)
- มี label + target **ต่อเนื่อง** (%HbA1c, ระดับ expression) → **Regression**
- มี label + เป็น **กลุ่ม** (โรค/ไม่โรค, blood group, variant pathogenic/benign) → **Classification**
- ไม่มี label อยากหา group (สำรวจ subtype ผู้ป่วย) → **Clustering**
- ไม่มี label อยากลดมิติ/visualize → **Dimensionality reduction** (Fork 5)
- agent ลองผิดลองถูก + reward (ปรับ dose/policy) → **RL**
- ⚖️ ลังเล classification↔regression: output ที่ "มีความหมาย" เป็น category หรือตัวเลข — อย่าปัด target ต่อเนื่องเป็น bin โดยไม่จำเป็น (เสียข้อมูล)

### Fork 2 — classifier ตัวไหน?
- ตีความ + baseline เร็ว + อยากได้ probability → **Logistic Regression** (เริ่มจากนี่เสมอ)
- feature categorical / rule ตีความได้ / ไม่อยาก scale → **Decision Tree**
- data น้อย-กลาง, มิติ ≤20, boundary โค้ง → **KNN** (normalize ก่อน!) หรือ **SVM+kernel**
- margin กว้าง, มิติสูง, sample ไม่เยอะ → **SVM** (tune C ด้วย CV)
- อยากแม่นสุด ยอมเสียความตีความ → **Ensemble**: Random Forest → Gradient Boosting
- 💡 ladder งานจริง: LogReg/Tree (baseline) → RF → GBT · อย่าเปิดด้วย deep net ถ้า tabular เล็ก

### Fork 3 — overfit หรือ underfit? (อ่านจาก train–test gap)
- train สูง · test ต่ำ · gap กว้าง → **Overfit** (variance สูง) → regularize (Ridge/Lasso, dropout, prune, ลด depth, เพิ่ม data, bagging)
- train ต่ำ · test ต่ำ (ใกล้กัน) → **Underfit** (bias สูง) → โมเดลซับซ้อนขึ้น, เพิ่ม feature, ลด regularization, boosting
- train ≈ test ทั้งคู่สูง → กำลังดี หยุดได้
- 🎯 Ridge(L2) = หด w ไม่ถึง 0 (ดีกับ multicollinearity) · Lasso(L1) = ดัน w เป็น 0 = แถม feature selection — ⚠️ feature correlate กันสูง Lasso จะเก็บตัวเดียวสุ่มๆ ทิ้งที่เหลือ → ใช้ **Elastic Net** (L1+L2) ถ้าอยากเก็บกลุ่ม correlate ไว้ครบ

### Fork 4 — metric ไหน? (จุดพลาดเยอะสุด)
- Classification **balanced** → accuracy พอ
- Classification **IMBALANCED** (โรคหายาก, variant 2%) → accuracy **หลอก** → ใช้:
  - **Precision** = ทายว่าป่วยแล้วป่วยจริงแค่ไหน (เน้นเมื่อ false-positive แพง)
  - **Recall/Sensitivity** = ผู้ป่วยจริงจับได้แค่ไหน (เน้นเมื่อ false-negative แพง — screening)
  - **F1** = สมดุล precision/recall เมื่อไม่รู้จะหนักข้างไหน
  - **PR-AUC (precision-recall)** = metric threshold-independent ที่ซื่อสัตย์สุดตอน imbalance หนัก — ⚠️ **ROC-AUC โป่งง่าย** (0.90–0.99 ได้แม้โมเดลกาก) เพราะ TN ก้อนใหญ่ทำให้สวย; ใช้ ROC-AUC เทียบโมเดลได้ตอน class ใกล้สมดุล แต่ severe imbalance ให้ดู PR-AUC
- **Regression** → **RMSE** (หน่วยเดียวกับ target, ลงโทษ error ใหญ่) · **MAE** (ทน outlier) · **R²** (สื่อกับคนทั่วไป)
- 🩺 health rule: screening → ดัน **recall** · confirmatory → ดัน **precision**

### Fork 5 — feature selection vs PCA/LDA?
- อยากเก็บ feature เดิม ตีความได้ → **Feature selection** (filter / wrapper / Lasso-embedded)
- ยอมได้แกนผสม, ลด noise/มิติ, unsupervised → **PCA** (linear, เร็ว)
- มี label + อยากแกนที่แยก class ดีสุด → **LDA** (supervised)
- แค่ visualize 2D → **t-SNE / UMAP** (อย่าเอา coordinate ไป feed โมเดลต่อ — เป็นแค่ภาพ)

### Fork 6 — bagging vs boosting?
- base model variance สูง/unstable (deep tree) → **Bagging / Random Forest** (ลด variance, train ขนานได้, ทน overfit)
- base model bias สูง/weak (stump) → **Boosting** (AdaBoost/GBT ลด bias, แม่นกว่าแต่ไวต่อ noise + overfit ถ้า estimator เยอะเกิน)
- ⚖️ data noise เยอะ → เอนไป bagging · data สะอาดอยากรีดความแม่น → boosting

---

## กับดัก (Anti-patterns) — พลาดตรงนี้บ่อย
- **Data leakage #1 — scale/feature-select นอก CV:** `fit_transform` ทั้ง dataset *ก่อน* split = test แอบรู้ค่า train → ใส่ scaler+selector ใน **Pipeline** แล้วค่อย CV (fit เฉพาะ train fold)
- **Target leakage:** feature ที่ได้มา *หลัง/เพราะ* รู้ผลลัพธ์ (เช่น "ได้รับยา X" ทำนาย "เป็นโรค X") → AUC สวยหลอก พังจริง → ตรวจ timeline ว่าทุก feature เกิด *ก่อน* prediction time
- **accuracy บน imbalanced:** โรคหายาก 2% → ทาย "ไม่โรค" หมด = acc 98% แต่ recall 0 = ไร้ค่า → ดู Fork 4
- **tune บน test set = overfit-to-test:** ลอง hyperparameter หลายค่าแล้วเลือกจากคะแนน test → test กลายเป็น train → ใช้ train/val/test 3 ส่วน หรือ **nested CV**; test แตะครั้งเดียวตอนจบ
- **ไม่ stratify:** classification imbalanced + split ธรรมดา → บาง fold ไม่มี minority class → **StratifiedKFold** / `stratify=y`
- **GIGO:** 60–80% ของงานคือเตรียมข้อมูล · missing/outlier/scale ผิด → โมเดลดีแค่ไหนก็พัง (ดูกลไก missing ก่อนเติม)
- **hyperparameter p-hacking:** ลอง config เป็นร้อยจน "เจอ" ตัวเด่น = บังเอิญ → fix CV seed, รายงานช่วงคะแนน ไม่ใช่ค่าดีสุดตัวเดียว
- **KNN/SVM/k-means ไม่ normalize:** distance-based + feature คนละ scale → ตัวใหญ่ครอบงำ → scale ก่อน (ใน Pipeline)
- **โมเดลสุ่ม init (k-means):** ผลแกว่งตาม seed, ไม่การันตี global optimum → `random_state` + run หลายครั้ง; เลือก k ด้วย elbow/silhouette
- **R² สูง ≠ ถูก:** ละเมิดเงื่อนไข regression (linearity/normal residual/homoscedasticity) หรือ outlier ลาก least-square → ดู residual plot ก่อนเชื่อ

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคส ML จริงในสายงานคุณ เช่น:
> - *"งาน lab/genomic ที่ผมเลือกโมเดล... เพราะ data มันลักษณะ..."*
> - *"metric ที่ทีมผมเถียงกัน สุดท้ายใช้... เพราะ false-negative มันแพงตรงที่..."*
> - *"เคยโดน data leakage ตรงที่... จับได้เพราะ..."*

---
*ช่วยคิดเลือกโมเดล/metric/validation + เลี่ยงกับดัก ML เพื่อการศึกษา ไม่ใช่คำแนะนำทางการจากที่ปรึกษา ML — ต้องตรวจผลและ assumption ก่อนเชื่อ โดยเฉพาะงานคลินิก · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: molecular-judgment ═════════ -->

---
skill: molecular-judgment
title: โค้ช Molecular Dx — เลือก method/แปลผล/กัน false (Molecular Diagnostics Judgment)
type: ADVISE               # ช่วยตัดสินใจหน้างาน molecular ไม่ใช่ตำรา PCR
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดเลือก method/แปลผล molecular เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รักษา — งานวินิจฉัยระดับโมเลกุลกระทบการรักษาผู้ป่วยโดยตรง ต้องตาม SOP + validation ของแล็บ และยืนยันกับ MT/แพทย์ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช Molecular Dx — เลือก method/แปลผล/กัน false

ตัดสินใจในงาน molecular — "variant/เชื้อ/marker นี้ตรวจด้วยอะไรดี + อย่าพลาดตรงไหน" ไม่ใช่ท่อง central dogma / ขั้น PCR / ตาราง codon (= commodity ดูตำรา)

> **กฎ #1 (เลือก method):** รู้ตำแหน่ง variant แน่ → targeted + ถูก (RFLP/ASO/HRM/qPCR); ไม่รู้/discovery → sequencing (Sanger เดี่ยว, NGS หลาย loci). อย่ายิง NGS สิ่งที่ ASO-PCR ตอบได้ใน 3 ชม.
> **กับดัก #1 (กัน false):** ก่อนแปลผลทุกครั้งต้องครบ **control + tube ถูก (heparin = ห้าม) + NTC สะอาด** — ไม่มี internal control = ห้ามอ่าน "negative" (อาจ reaction fail = false-neg); NTC ขึ้น = ทั้ง run โมฆะ (contamination = false-pos)
> เลือกโมเดล ML ต่อจาก genotype → ดู `ml-judgment` · วาง stat/sens-spec → `choose-stat-test`

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ (คู่กับ `anti-hallucination`)

## ใช้เมื่อ
- ต้อง detect mutation/SNP/fusion/เชื้อ → **เลือก method ไหน** (cost/turnaround/known-vs-unknown variant)
- แปล real-time PCR (Ct, melt curve, HRM) · ตัดสิน positive/negative/invalid
- วาง pipeline genotyping/sequencing · ตัดสิน sample/tube/anticoagulant · DNA vs RNA workflow
- HLA typing (transplant) · pharmacogenomics gate ก่อนให้ยา · companion Dx

## วิธีใช้
วาง skill นี้ + เล่า variant/เชื้อ/ผล qPCR → AI ชี้ method/การแปลผล + กับดัก

---

## ก่อนรัน/แปลผลเสมอ — 3 ด่าน (ขาด = หยุด)
1. **Sample/nucleic-acid integrity** — tube ถูกมั้ย (**heparin = ห้าม ยับยั้ง PCR**) · hemolysis (Hb ยับยั้ง) · RNA สลายรึยัง (RNase ทุกที่) · อุณหภูมิ (DNA ทน, RNA −70°C)
2. **Controls ครบมั้ย** — positive + negative (NTC) + internal/amplification control · qPCR ที่ quantify ต้องมี standard curve · **ขาด internal control = แปล "negative" ไม่ได้** (อาจ reaction fail)
3. **Variant รู้จักมั้ย** — known single vs unknown/scanning vs discovery → กำหนด method (Fork 1) · **polymorphism (MAF≥1%, มักไม่ก่อโรค) ≠ pathogenic mutation**

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — ตรวจ variant นี้ด้วย method ไหน (การตัดสินใจหลัก)
ถามก่อน: (ก) รู้ตำแหน่ง variant แน่ๆ มั้ย (ข) กี่ตำแหน่ง/loci (ค) งบ+turnaround (ง) ขนาด (point vs deletion ใหญ่)
- **Known point + สร้าง/ทำลาย restriction site** → **PCR-RFLP (CAPS)** — ถูกสุด ไม่ต้องเครื่องแพง (คลาสสิก sickle cell *Dde*I)
- **Known point, allele-specific** → **ASO-PCR / ARMS** หรือ **real-time + HRM** (ถูก ไม่ต้อง probe ไม่มี post-PCR)
- **Unknown ในยีนสั้น (scanning)** → **SSCP / HA** คัด → **Sanger ยืนยัน**
- **Large deletion / copy-number** → **gap-PCR / MLPA / qPCR-CNV** (PCR-sequence ทั่วไปมองไม่เห็น deletion ทั้ง allele = trap)
- **ยืนยัน variant เดี่ยว / ตัวอย่างน้อย / <900 bp** → **Sanger** (ground-truth ระดับเดี่ยว)
- **หลาย loci / discovery / VAF ต่ำ (tumor) / high-throughput** → **NGS** (ต้อง validate + bioinformatics + coverage/VAF cutoff)
> หลัก: known → targeted+ถูก (RFLP/ASO/HRM) · unknown/discovery → sequencing. อย่าใช้ NGS ยิงสิ่งที่ ASO-PCR ตอบได้ใน 3 ชม. (over-engineer); อย่าใช้ Sanger ไล่ทีละตำแหน่งกับ panel ใหญ่

### Fork 2 — Sanger vs NGS
- **Sanger:** ยืนยัน variant เดี่ยวที่รู้ตำแหน่ง, ตัวอย่างน้อย, region สั้น, ต้องการ certainty · จุดอ่อน: ไม่เห็น low-VAF (<15–20%), throughput ต่ำ
- **NGS:** discovery, panel/exome/genome, low VAF (somatic/tumor) · ต้องมี validation + bioinformatics + coverage depth + VAF threshold และมัก **confirm hit สำคัญด้วย Sanger** (orthogonal)

### Fork 3 — Real-time PCR: chemistry ไหน (SYBR vs TaqMan vs HRM)
- **SYBR Green** — จับ dsDNA ทุกตัว → ถูก ง่าย **ไม่จำเพาะ ต้องอ่าน melt curve ยืนยัน** (กัน primer-dimer); ดีกับ single amplicon/screening
- **TaqMan probe** — จำเพาะ sequence, **multiplex ได้**, เหมาะ clinical quantitative/viral load · แพงกว่า
- **HRM** — แยก genotype/SNP จากรูป melt (saturating dye) → ถูก ไม่ต้อง probe ไม่มี post-PCR; เหมาะ SNP/point mutation จำนวนมากแบบประหยัด (rpoB/katG ใน MDR-TB)
> 1 target + งบจำกัด → SYBR+melt · multiplex/quantitative clinical → TaqMan · genotype SNP เยอะ-ถูก → HRM

### Fork 4 — Ct / melt → positive, negative, หรือ invalid
- **Ct ต่ำ = template เริ่มต้นเยอะ** (quantify ผ่าน standard curve; relative ต้องมี housekeeping gene)
- **ไม่ขึ้น amplification + internal control ก็ไม่ขึ้น** = **INVALID (inhibition/reaction fail) ไม่ใช่ "negative"** → repeat/extract ใหม่ (ห้ามรายงาน "ไม่พบเชื้อ" จาก reaction ที่ fail)
- **NTC ขึ้น signal** = **contamination → ทั้ง run ใช้ไม่ได้** (Fork 6)
- **SYBR ขึ้นแต่ melt peak ผิด/หลายพีค** = primer-dimer/non-specific ไม่ใช่ true positive

### Fork 5 — Internal / amplification control = บังคับ
ทุก assay ตรวจเชื้อ/mutation ต้องมี control ที่บอกว่า reaction ทำงาน + ไม่มี inhibitor:
- ขาด → negative อาจเป็น false-negative จาก inhibitor/extraction fail (เช่นบอก HIV/TB negative ผิด)
- qPCR quantify → standard curve (efficiency 90–110%, R²>0.98) ก่อนเชื่อค่า

### Fork 6 — Contamination control (amplicon carryover = ศัตรู #1)
- **Unidirectional workflow:** reagent prep → sample prep → amplification/detection (clean→dirty ทางเดียว ห้ามย้อน) · แยกห้อง/พื้นที่/อุปกรณ์
- กัน: UNG/dUTP, aerosol-barrier tips, NTC ทุก run
- **NTC ขึ้น = หยุด ล้าง สืบหา source** ก่อนรันต่อ

### Fork 7 — Oncogene vs tumor-suppressor → test logic
- **Oncogene (gain-of-function, 1 allele พอ)** → หา activating mutation/fusion/amplification + จับคู่ targeted drug (BCR-ABL→imatinib · EGFR→gefitinib/osimertinib · BRAF V600E→vemurafenib · EML4-ALK→crizotinib · HER2 amp→trastuzumab)
- **Tumor suppressor (loss-of-function, ต้อง 2 alleles, Knudson two-hit)** → หา biallelic loss (TP53, RB, BRCA1/2, APC) — prognosis/germline risk

### Fork 8 — HLA typing: resolution แค่ไหน
- **Serology (CDC)** ต่ำ/เร็ว/screening · **PCR-SSP/SSOP** กลาง · **SBT (Sanger)/NGS** สูงสุด
- **Transplant matching (BMT, kidney) → high-resolution (SBT/NGS)** · disease association → กลางพอ
- HLA = ยีน polymorphic ที่สุด, exon 2 (+3 สำหรับ Class I) = region ที่ต้อง type

### Fork 9 — Pharmacogenomics: test "ก่อน" ให้ยา (สำคัญในคนไทย)
- **HLA-B*15:02 ก่อน carbamazepine** → กัน SJS/TEN (**prevalence สูงในคนไทย/จีน** = high-yield จริง) · ⚠️ ผลใช้ **rule-OUT ไม่ใช่ rule-IN**: NPV ~100% (negative → ให้ยาได้ค่อนข้างมั่นใจ) แต่ PPV เพียง ~1.8% (carrier ส่วนใหญ่กินได้ไม่เป็นไร — positive = หลีกเลี่ยง/เปลี่ยนยา ไม่ใช่ทำนายว่าจะเป็นโรค)
- **HLA-B*57:01 ก่อน abacavir** · **HLA-B*58:01 ก่อน allopurinol** · **CYP2C19 + clopidogrel** (poor metabolizer → ยาไม่ทำงาน)
- **G6PD ก่อน primaquine / dapsone / rasburicase / ยา oxidant** → กัน acute hemolysis (G6PD def พบบ่อยในไทย/มาเลย์ + เกี่ยวกับ malaria → ตรวจก่อนให้ primaquine เสมอ) · **TPMT/NUDT15 ก่อน thiopurine** (azathioprine/6-MP → myelosuppression รุนแรงถ้า deficient; NUDT15 สำคัญในเอเชีย) · **DPYD ก่อน 5-FU/capecitabine**
> ตรวจ **ก่อน** prescribe ไม่ใช่หลังเกิด ADR — เฉพาะยา/เชื้อชาติที่ risk สูง (ไม่ใช่ทุกยา) · ⚠️ คู่ที่ขาดบ่อยในไทย: **G6PD↔primaquine** (malaria) + **HLA-B*15:02↔carbamazepine** (SJS)

---

## กับดัก (Anti-patterns) — อันตราย เช็คทุกครั้ง
- 🚫 **Heparin tube ส่ง molecular** = ยับยั้ง Taq → PCR fail/Ct เลื่อน → ใช้ **EDTA (ม่วง) / ACD (เหลือง)**; hemolysis ก็ยับยั้ง
- 🚫 **ลืม internal/amplification control** → reaction fail ถูกอ่านเป็น "negative" → **false-negative**
- 🚫 **Amplicon contamination** → false-positive; **NTC ขึ้น = ทั้ง run โมฆะ**; workflow ต้อง unidirectional
- 🚫 **RNA สลาย** (ไม่ cold chain/ไม่ RNase-free) → RNA target (HIV/SARS-CoV-2 viral load) ต่ำ/negative ปลอม → RT เร็ว, −70°C
- 🚫 **PCR-sequencing แล้วเชื่อว่าครบ ทั้งที่มี large deletion** → allele ที่ถูกลบ "มองไม่เห็น" (het deletion อ่านเป็น homozygous WT) → MLPA/gap-PCR/qCNV
- 🚫 **สับ polymorphism กับ mutation** — MAF≥1% มักไม่ก่อโรค; อย่ารายงาน pathogenic โดยไม่เช็ค database/ACMG
- 🚫 **SYBR/HRM โดยไม่ดู melt curve** → primer-dimer/non-specific นับเป็นบวก
- 🚫 **NGS variant → รายงาน actionable ทันที** โดยไม่ดู VAF/coverage/database + ไม่ confirm orthogonal ตัวสำคัญ
- 🚫 **qPCR quantify โดยไม่มี standard curve / efficiency ไม่ดี** → copy number เชื่อไม่ได้
- 🚫 **Pharmacogenomics ข้าม HLA-B*15:02 ก่อน carbamazepine ในคนไทย** → SJS/TEN ที่ป้องกันได้

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง / สะพานสู่งานอื่น เช่น:
> - *"(MT molecular) เคส false-negative/contamination ที่ผมเจอ คือ... จับได้เพราะ..."*
> - *"(งานวิจัย genomics) pipeline genotype→label ของผม: PCR → genotype (RFLP/HRM/NGS) → Sanger/NGS = ground truth → feature/label → validate ด้วย sens/spec"*
> - *"(สาย MolDx sales) targeted/POCT → cartridge qPCR · genomics center → NGS · companion Dx = 'ตรวจก่อนสั่งยา'"*

---
*ช่วยคิดเลือก method/แปลผล molecular เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รักษา — ต้องตาม SOP + validation ของแล็บ และยืนยันกับ MT/แพทย์ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: mt-career-judgment ═════════ -->

---
skill: mt-career-judgment
title: โค้ชเส้นทางอาชีพ MT — bench → industry/commercial/AI (MT Career Strategy)
type: ADVISE               # ช่วยคิดเส้นทางอาชีพ ไม่ใช่ที่ปรึกษา HR/จัดหางาน
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดเส้นทางอาชีพ MT เพื่อการศึกษา ไม่ใช่ที่ปรึกษาอาชีพ/จัดหางานทางการ — โครงสร้างตำแหน่ง/รายได้/ตลาดงานต่างกันตามบริษัท/ประเทศ/ช่วงเวลา ต้องเช็คของจริงเอง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชเส้นทางอาชีพ MT — bench → industry/commercial/AI

MT ไม่ได้มีแค่ "อยู่หน้า bench" — มีทางออกหลายสาย แต่ส่วนใหญ่ไม่รู้ว่าเข้าได้ยังไง/ขาดอะไร สกิลนี้ช่วย **เลือกสาย + เห็นบันได + รู้ว่าช่องว่างจริงคืออะไร** ไม่ใช่ปลอบใจลอยๆ

> **กฎ #1:** งาน routine จะถูก automate → กลยุทธ์อาชีพ = **ขยับขึ้น-value** (QA + ตีความผลซับซ้อน + judgment + ชั้น commercial/relationship) ไม่ใช่ยึด routine เดิม
> **กับดัก #1:** เทียบ offer commercial ด้วย **base salary** — ผิด, ต้องเทียบ total (base + commission + transport + allowance + bonus); และ **KOL/networking + English = core skill + ด่านขึ้นผู้บริหาร ไม่ใช่ optional**
> ขายของจริง → `ivd-sales-judgment` · เขียน CV → `cv-judgment` · ขุดวัตถุดิบจากตัวเอง → `know-yourself` · หาทิศ → `ikigai-finder` · ขอบเขต/ใบอนุญาต → `mt-law-ethics-judgment`

## ใช้เมื่อ
- รู้สึกตันที่ bench / อยากเปลี่ยนสาย แต่ไม่รู้มีทางไหนบ้าง + เข้ายังไง
- เล็งสาย industry/commercial (sales/product) หรือ data/AI แต่ไม่รู้ขาดอะไร
- ตัดสินใจ offer / วาง career ladder ระยะยาว
- เตรียมเล่าเส้นทาง (สัมภาษณ์/LinkedIn) ให้ดูรู้ทาง

## วิธีใช้
วาง skill นี้ + เล่าจุดที่อยู่ตอนนี้ + สายที่สนใจ → AI ช่วยจับคู่สาย + ชี้บันได + ช่องว่างที่ต้องอุด + กับดักการเปลี่ยนสาย

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — แผนที่เส้นทาง MT (ไม่ได้มีสายเดียว)
- **คลินิก/รพ.** (bench → หัวหน้างาน → ผู้เชี่ยวชาญเฉพาะสาขา) · **วิชาการ/อาจารย์/วิจัย**
- **Industry-commercial:** sales rep · product specialist/manager · marketing · business development (ดู Fork 2)
- **R&D / molecular / genomics** (lab industry, biotech)
- **Medical AI / data science** (validation, model, SaMD) (ดู Fork 5)
- **QA / lab management / accreditation**
- **ผู้ประกอบการ — เป็นเจ้าของ:** เปิดคลินิก/แล็บ MT เอง (มีใบอนุญาต) · model ที่เวิร์ก = ตรวจสุขภาพเชิงรุก + บริการใกล้บ้าน (แก้ pain เดินทางไกล/รอนาน) · ⚠️ เป็นเจ้าของ = **คุมทั้งชั้น technical + business = ตำแหน่งที่ secure สุด** (ถ้าคุมคุณภาพเอง คนนอกถือเงินแทนที่ไม่ได้)
- หลัก: เลือกสายจาก **ค่านิยม + จุดแข็ง + ตลาดโต** ไม่ใช่ "หนีจากที่เดิม" อย่างเดียว

### Fork 2 — bench → commercial: บันได + role ที่ MT เข้าได้
- **บันได (สาย diagnostics/IVD):** Sales Rep → Supervisor/Product Specialist → Sales/Product Manager → Marketing → Business Development → Business Unit/Country Manager → Regional Director → VP — **เป็นบันไดจริงที่มีคนเดินถึงระดับภูมิภาคได้**
- **role ที่เข้าได้:** Sales Rep (Diagnostics/Scientific Equipment) · Product Specialist/Manager (สาย technical-commercial) · **Medical Product Specialist** (หลายที่ *ไม่ต้องใช้ใบอนุญาต* = exit friction ต่ำ) · Medical Advisor/Innovation (biotech, จ่ายสูง)
- edge ของ MT: เข้าใจ science + งานแล็บ + pain ของลูกค้า (คนขายทั่วไปไม่มี) → ขายแบบ consultative ได้
- ⚠️ บันได/ชื่อ role + ข้อ *"ไม่ต้องใช้ใบอนุญาต"* นี้อิงบริบท **ไทย/SEA** — ต่างกันตามประเทศ/บริษัท ต้องเช็คของจริงในตลาดนั้นเอง (อย่าฟันธงว่าเป็นจริงทุกที่)

### Fork 3 — รายได้ฝั่ง commercial ≠ base salary (อย่าเทียบผิด)
- องค์ประกอบ: **salary + allowance + commission/incentive + transportation + bonus + incentive trip**
- ⚠️ **อย่าเทียบ offer ด้วย base เฉยๆ** — commission/transport เปลี่ยนเลขรวมเยอะ (transport มักครอบคลุมเรื่องเดินทาง/รถ ที่หลายคนกังวล)
- ถามให้ครบ: โครง commission (เป้า/เพดาน), allowance, รถ/ค่าเดินทาง, base ก่อนค่อยตัดสิน

### Fork 4 — skill ที่ต้องมี + ที่ MT มักขาด
- **MT มีอยู่แล้ว:** scientific/product knowledge · เข้าใจงานแล็บ
- **ช่องว่างจริง (commercial-craft):** **selling skill · marketing concept · costing/finance · negotiation · KOL/networking · English**
- ⚠️ **KOL/networking = core sales skill ไม่ใช่ optional** — งานขายสายแพทย์เดินด้วย relationship + ความน่าเชื่อ
- ⚠️ **English + international exposure = ด่าน (gate) ขึ้นระดับผู้บริหาร/ภูมิภาค** ไม่ใช่แค่ entry → ต้อง track เป็น milestone ตั้งแต่เนิ่น
- มนตรา **"Skill & Will":** ทำไม่ถึงเป้า = ขาด skill หรือขาด will หรือทั้งคู่ → วินิจฉัยให้ตรงก่อนแก้

### Fork 5 — T-Shaped MedTech + 3 ระดับ Data/AI (future-proof)
- **Lv1 Data literacy** (ทุกคนควรมี): อ่าน QC dashboard, เข้าใจ LIS/HL7, รู้ PDPA
- **Lv2 Data analytics:** Python/R เบื้องต้น, สถิติ, สร้าง validation rule
- **Lv3 AI/Data science:** train/validate ML, curate dataset, เข้าใจ regulatory pathway
- หลัก: **ยิ่งขึ้นชั้น = ยิ่งห่างจาก "routine ที่ถูกแทน" → เป็น change-leader** · จุดตัด "MT + Data/AI" หรือ "MT + commercial" = หายากกว่าเก่งอย่างเดียว = ค่าตัวสูง

### Fork 6 — megatrend ที่ MT เป็นผู้เล่นหลัก + ความจริงเรื่อง automation
- **Precision Medicine & Genomics** (pharmacogenomics, cancer/ยีน) · **Medical AI & SaMD** (software เป็นเครื่องมือแพทย์) · **Wellness & Longevity** (biomarker)
- ⚠️ **routine ส่วนใหญ่จะถูก automate** → คุณค่าที่เหลือ = **QA + ตีความผลซับซ้อน + human judgment + ชั้นความสัมพันธ์/commercial** → จัด career ไปทางนั้น
- ⏱️ **จังหวะขยับ:** assay volume สูง/rule-based ถูก automate ก่อน · งาน interpretive/molecular/QA ถูกแทนทีหลังสุด → ดูว่า sub-specialty ตัวเอง exposed แค่ไหนแล้วค่อย time การย้าย
- (นี่คือเวอร์ชันบุคคลของ "secure วิชาชีพด้วยการขึ้น-value")

### Fork 7 — กับดักการเปลี่ยนสาย (decision judgment)
- กระโดดสายโดยไม่มี **transferable-skill bridge** (เล่าไม่ได้ว่าของเก่าช่วยงานใหม่ยังไง)
- รอ **"พร้อม 100%"** — บันไดไม่มี deadline แต่ entry role มี window/อายุที่เหมาะ
- เลือก role ที่ **ผูก license โดยไม่จำเป็น** ทั้งที่บาง commercial role ไม่ต้องใช้ = เพิ่ม friction เปล่า
- **ทิ้ง identity แล็บ/quality** — จริงๆ มันคือ edge (เข้าใจ pain ลูกค้า + ตีความผล) = talking point ขายตัวเอง
- เทียบ offer ด้วย base · มอง networking/English เป็น "ค่อยทำ"

---

## กับดัก (Anti-patterns)
- **คิดว่า MT มี bench สายเดียว** — มีหลายทางออก แค่ไม่รู้ทางเข้า
- **หนีจากที่เดิม โดยไม่เลือกสายจากจุดแข็ง/ค่านิยม** → ตันซ้ำ
- **เทียบ offer commercial ด้วย base salary** (ลืม commission/transport/incentive)
- **มอง KOL/networking + English เป็น optional** — มันคือ core skill + ladder gate
- **ยึด routine ที่กำลังถูก automate** แทนขยับขึ้น judgment/AI/commercial
- **ทิ้ง quality/clinical identity** ทั้งที่เป็น edge ในงานขาย/บริหารแล็บ
- **เปลี่ยนสายโดยไม่ bridge transferable skill** → เล่าเส้นทางไม่น่าเชื่อ

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมจากประสบการณ์จริง เช่น:
> - *"ตอนผมย้ายจาก bench ไป [สาย] จุดที่ยากสุด/ช่องว่างที่ต้องอุดก่อน คือ..."*
> - *"role [X] ในบริษัท IVD จริงๆ ดู skill/วุฒิอะไร + โครงรายได้เป็นแบบไหน..."*
> - *"transferable skill จากงานแล็บที่ช่วยงานใหม่มากสุด คือ..."*

---
*ช่วยคิดเส้นทางอาชีพ MT เพื่อการศึกษา ไม่ใช่ที่ปรึกษาอาชีพ/จัดหางานทางการ — โครงสร้างตำแหน่ง/รายได้/ตลาดงานต่างกันตามบริษัท/ประเทศ/ช่วงเวลา ต้องเช็คของจริงเอง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: mt-exam-strategy-judgment ═════════ -->

---
skill: mt-exam-strategy-judgment
title: โค้ชกลยุทธ์สอบใบประกอบฯ MT — บริหารเวลา/จับ distractor (MT Licensing Exam Strategy)
type: ADVISE               # ช่วยวางกลยุทธ์สอบ ไม่ใช่คลังเนื้อหารายวิชา
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดกลยุทธ์เตรียมสอบใบประกอบวิชาชีพ MT เพื่อการศึกษา — โครงสร้าง/น้ำหนักข้อสอบเปลี่ยนได้ ต้องเช็คประกาศสภาเทคนิคการแพทย์ + แนวล่าสุดเสมอ · ไม่รับประกันผลสอบ · เนื้อหารายวิชาต้องยืนยันกับตำรา/สกิลรายสาขา · ผู้นำไปใช้รับผิดชอบเอง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชกลยุทธ์สอบใบประกอบฯ MT — บริหารเวลา/จับ distractor

วิธี "ทำข้อสอบใบประกอบฯ ให้ได้คะแนน" — จัดลำดับทำ · จับกับดักตัวเลือก · ลงทุนอ่านตรงไหนคุ้ม ไม่ใช่คลังเนื้อหา (เนื้อหารายวิชา = ดูสกิลรายสาขา)

> **กฎ #1 — กวาดแต้มง่ายก่อน ห้ามไล่ตามรู้ลึกทุกข้อ:** เก็บ recall/QC/กฎหมาย/pre-analytical ที่ออกทุกสาขาให้ครบก่อน (กฎหมาย = recall ล้วน = คะแนนฟรี) → แล้วทุ่ม 3 สาขาใหญ่ เคมี+จุล+โลหิต (~60%) → ข้อภาพ/ข้อยากทำท้าย ข้ามได้ ห้ามติดจนหมดเวลา
> **กับดัก #1 — distractor "สลับคู่" + อ่านโจทย์บวก/ลบไม่ขาด:** ผู้ออกชอบสลับคู่ที่ฟังคล้าย (Fab↔Fc · sensitivity↔specificity · trend↔shift · accuracy↔precision · RBC-เลือกตาม cell(O) vs Plt-เลือกตาม plasma(AB) · "เร็วสุด TAT"↔"ไวสุด sensitivity") และสลับเลข timeline กฎหมาย → ก่อนตอบ เช็คว่าถาม "ข้อใดถูก" หรือ "ยกเว้น/ไม่ถูกต้อง" แล้วตัดตัวสลับคู่ทิ้งก่อน
> นี่คือชั้น **"กลยุทธ์ทำข้อสอบ"** — เนื้อหา judgment รายสาขาอยู่ในสกิลของมันเอง: `hematology` · `clinchem`/`chemistry-interpretation` · `clinmicro` · `immunoassay` · `bloodbank` · `parasitology` · `mt-law-ethics`

## ใช้เมื่อ
- วางแผนติว/แบ่งเวลาอ่านตามน้ำหนักข้อสอบ
- ทำข้อสอบแล้วลังเลระหว่างตัวเลือก
- อยากรู้ว่ากับดักออกแบบไหนซ้ำๆ

## วิธีใช้
วาง skill นี้ + บอกสถานการณ์ (วางแผนติว / ข้อที่ลังเล / สาขาที่อ่อน) → AI ช่วยจัดลำดับ + ชี้ distractor + ชี้ไปสกิลรายสาขา

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — Blueprint + บริหารเวลา (ลงทุนตามน้ำหนัก)
- **3 สาขาน้ำหนักสูงสุด = เคมีคลินิก + จุลชีววิทยา + โลหิตวิทยา** (รวม ~60% ของข้อ) → ทุ่มเวลาอ่านที่นี่ก่อน
- **กฎหมาย/จรรยาบรรณ = recall ล้วน = คะแนนฟรี** → ท่องเลข/timeline/หน่วยงานให้แม่น คุ้มต่อแต้มสุด (ดู `mt-law-ethics-judgment`)
- ปรสิตไม่แยกสาขา → ซ่อนใน "จุลทรรศนศาสตร์คลินิก" แต่ออกแน่ (ดู `parasitology-judgment`)
- ลำดับทำข้อ: **(1) กวาด QC/standard/pre-analytical/กฎหมาย (recall เร็ว) → (2) case แปลผลด้วย pattern → (3) ข้อภาพ (morphology/ไข่พยาธิ/colony) ทำท้าย**

### Fork 2 — จับ distractor ที่ผู้ออกชอบลวง (โกงแต้มได้)
- **สลับคู่ (ออกบ่อยสุด):** Fab↔Fc · MHC I↔II · HbA1c↔fructosamine · spherocyte↔schistocyte · precision↔accuracy · trend↔shift · RBC-selection↔WBC-selection (O vs AB) · sensitivity↔specificity · "เร็วที่สุด (TAT)"↔"ไวที่สุด (sensitivity)"
- **ตัวเลขลวง:** timeline กฎหมาย (⚠️ **เพิกถอนใบอนุญาต→ขอใหม่เมื่อพ้น 2 ปี** [ม.46] vs **ยื่นซ้ำหลังถูกปฏิเสธ 1 ปี** — ข้อสอบสลับ 2 เลขนี้; เก็บเอกสารผู้ป่วย 5 ปี; กล่าวหา 1 ปี) · อดอาหาร 12 ชม. · blast acute leukemia 20% · citrate 9:1 · NRBC >10% · TG>400 (Friedewald ใช้ไม่ได้)
- **"ตัวเลือกครบ keyword ทุกตัว มักถูก"** — โดยเฉพาะนิยาม/มาตรฐาน/การคัดกรอง (อย่าเลือกตัวสั้นที่ "ดูพอได้")

### Fork 3 — Answer heuristic ตอนลังเล
- อ่านโจทย์ให้ขาดว่าถาม **บวก ("ข้อใดถูก")** หรือ **ลบ ("ยกเว้น/ไม่ใช่/ไม่ถูกต้อง")** → ลบ = หาตัวที่ผิดจาก concept หลัก
- **เชื่อ concept มาตรฐาน > เฉลยเก่า** — เฉลยที่รวบรวมกันมาผิดได้ (เช่นเลขมาตรา) → cross-check กับสกิลรายสาขา/ตำรา
- เดาแบบมีหลัก: ตัด distractor สลับคู่ออกก่อน เหลือตัวที่ concept ตรง

### Fork 4 — Study ROI (อ่านตรงไหนคุ้ม)
- **recall (กฎหมาย/ค่าวิกฤต/หน่วย) = คุ้มสุดต่อแต้ม** — ท่องตรงๆ ไม่ต้องเข้าใจลึก
- **QC/standard/pre-analytical ออกทุกสาขา** = ทำได้ก่อนเนื้อโรค (Westgard trend/shift/random, order of draw, interference)
- **จำ "pattern table" > ท่องค่าดิบ:** jaundice (hemolytic/hepatic/obstructive) · anemia ตาม MCV · urine sediment→โรค · thal (OF/DCIP/genotype) → ดูสกิลรายสาขา
- เนื้อหา judgment ลึก = ไม่ต้องท่อง ใช้สกิลรายสาขาเป็นกรอบคิด

### Fork 5 — กับดักข้ามสาขา (ออกซ้ำทุกปี)
- **QC/pre-analytical/standard แทรกทุกสาขา** (sample เก่า/hemolyze/clot, lot ใหม่, calibrate)
- **reporting rules:** MRSA (cefoxitin-R → รายงาน β-lactam ทั้งหมด) · CSF isolate ห้ามรายงานยาบางตัว (ดู `clinmicro-judgment`)
- **compatibility กลับด้าน:** RBC เลือกตาม cell (O) · Plt/plasma เลือกตาม plasma (AB) (ดู `bloodbank-judgment`)
- **report จาก test เดียว = พลาด:** coagulase-slide เดี่ยว≠S.aureus · IgG เดี่ยว≠acute · Ab เดี่ยว≠ติดเชื้อ → ต้อง panel/confirm

---

## กับดัก (Anti-patterns)
- **อ่านเนื้อลึกทุกสาขาเท่ากัน** — ทิ้งน้ำหนัก; ทุ่ม 3 สาขาใหญ่ + เก็บ recall ก่อน
- **ข้ามกฎหมาย** เพราะ "ไม่ใช่วิชาการ" — 30 ข้อ recall = คะแนนฟรีที่ทิ้งไม่ได้
- **ติดข้อยาก/ข้อภาพ** จนหมดเวลา — ข้ามไปเก็บข้อง่ายก่อน
- **เลือกตัวเลือกสั้นที่ "ดูพอได้"** ทั้งที่มีตัวครบ keyword
- **อ่านโจทย์ไม่ขาดว่าถามบวก/ลบ** → ตอบกลับด้าน
- **ยึดเฉลยเก่าเป็นสัจธรรม** — เฉลยรวบรวมผิดได้ เชื่อ concept

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"ปีที่สอบ สาขา... ออกหนักเรื่อง... กับดักที่เกือบพลาด คือ..."*
> - *"จุดที่เฉลยเก่าผิด แต่ concept จริงคือ..."*

---
*ช่วยคิดกลยุทธ์เตรียมสอบใบประกอบวิชาชีพ MT เพื่อการศึกษา — โครงสร้าง/น้ำหนักข้อสอบเปลี่ยนได้ ต้องเช็คประกาศสภาเทคนิคการแพทย์ + แนวล่าสุดเสมอ · ไม่รับประกันผลสอบ · เนื้อหารายวิชาต้องยืนยันกับตำรา/สกิลรายสาขา · ผู้นำไปใช้รับผิดชอบเอง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: mt-law-ethics-judgment ═════════ -->

---
skill: mt-law-ethics-judgment
title: โค้ชกฎหมาย/จรรยาบรรณวิชาชีพ MT — ขอบเขต/ความลับ/เครื่องมือแพทย์ (MT Law & Ethics Judgment)
type: ADVISE               # ช่วยเข้าใจกรอบกฎหมาย ไม่ใช่ที่ปรึกษากฎหมาย
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยเข้าใจกรอบกฎหมาย/จรรยาบรรณวิชาชีพ MT เพื่อการศึกษา ไม่ใช่คำปรึกษาทางกฎหมาย — ตัวบท/อัตราโทษต้องตรวจฉบับล่าสุด + ปรึกษานักกฎหมาย/สภาวิชาชีพก่อนตัดสินใจจริง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชกฎหมาย/จรรยาบรรณวิชาชีพ MT — ขอบเขต/ความลับ/เครื่องมือแพทย์

ตัดสินใจหน้างานที่มีกฎหมาย/จรรยาบรรณกำกับ — "ทำได้ไหม + ผิดตรงไหนถึงโดน" ไม่ใช่ท่องมาตรา (= commodity ดูตัวบท)

> 🔑 **กฎ #1: "ทำเป็น ≠ ทำได้"** — สิ่งที่ตัดสินว่า MT ทำได้ไหม คือ **ประเภทหัตถการ + ขอบเขตวิชาชีพตามกฎหมาย/ระเบียบสภา** ไม่ใช่ว่าคุณเจาะเป็น/มือนิ่งแค่ไหน
> 🚫 **กับดัก #1: เจาะเลือดที่ MT ทำได้ = venous/capillary (peripheral) เท่านั้น** — **arterial (ABG)/jugular/femoral/ไขกระดูก = นอกขอบเขต แม้ทำเป็น**
> 🔎 **ขอบ (เส้นกลางๆ): อย่าตอบสุดทาง** — หัตถการเสี่ยงปานกลาง (whole-blood donor, OGTT, apheresis, skin test) **ไม่ใช่ "ห้ามเด็ดขาด" และไม่ใช่ "ต้องมีแพทย์ยืนด้วยทุกครั้ง"** — ขึ้นกับ *ชนิดหัตถการ + ระเบียบหน่วยงาน*: บางอย่าง MT อบรมแล้วทำได้ภายใต้ความรับผิดชอบแพทย์ (ไม่ต้องยืนกำกับ), บางอย่างต้องสั่งโดยแพทย์ → **เช็คระเบียบจริงเป็นรายหัตถการ ห้ามเหมารวม**
>
> วิชาชีพ MT = วิชาชีพควบคุม — **ทำแล็บถูกแต่ผิดกฎหมาย/จรรยาบรรณ ก็ถูกพักใบ/ฟ้องได้** · PDPA ดู `digital-judgment` · กฎหมายเครื่องมือแพทย์ตอนขาย IVD ดู `ivd-sales-judgment`
> ⚠️ อัตราโทษ/มาตราในนี้เป็น "กรอบให้รู้ว่ามีเรื่องนี้" — **ต้องตรวจตัวบทจริง + ปรึกษานักกฎหมาย** ก่อนใช้อ้างอิงจริง

## ใช้เมื่อ
- ไม่แน่ใจว่างานนี้ MT **ทำได้เอง / ต้องมี request / ต้องมีแพทย์ / ทำไม่ได้**
- จะเอาข้อมูลคนไข้/เคสออกจากแล็บ (demo/case study/วิจัย) → ต้องทำอะไรก่อน
- ขาย/demo เครื่องมือแพทย์-น้ำยา · จะโพสต์โซเชียลเกี่ยวกับงาน · เซ็นสัญญาจ้าง

## วิธีใช้
วาง skill นี้ + เล่าสถานการณ์ → AI ชี้ว่าอยู่ในขอบเขตไหน + กับดักกฎหมาย/จรรยาบรรณ (ไม่ใช่คำวินิจฉัยทางกฎหมาย)

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — ใบอนุญาตประกอบวิชาชีพ (ใบ ทนพ.)
- ต้องมีใบ + **เซ็นรับรองผลก่อนรายงานทุกครั้ง** · ใบหมด/ถูกพัก = ออกผลตามกฎหมายไม่ได้ · ต่อใบต้องเก็บหน่วยการศึกษาต่อเนื่อง (CMTE) ตามเกณฑ์
- 💼 **แม้ย้ายสาย sales อย่าปล่อยใบหมดอายุ** — credibility กับแล็บ + บาง role (application specialist เข้าไป validation/training) ต้องใช้ + ประตูกลับสายแล็บ

### Fork 2 — ขอบเขตวิชาชีพ: ทำได้ / ต้องมีเงื่อนไข / ทำไม่ได้
- **ทำได้เอง:** เจาะเลือด **ดำ/ปลายนิ้ว (peripheral)**, swab/ป้าย, ตรวจวิเคราะห์ทุกสาขา, QC, เซ็นผล
- **ต้องมี request แพทย์:** EKG/EEG
- **ต้องมีแพทย์ดูแล/รับผิดชอบ (เงื่อนไขต่างกันตามหัตถการ — เช็คระเบียบจริง):** OGTT, skin test, apheresis · ⚠️ *เจาะเก็บ **โลหิตบริจาค (whole blood)** ปกติ MT/พยาบาลที่อบรมแล้วทำได้ภายใต้ความรับผิดชอบของแพทย์ — "ต้องมีแพทย์ยืนอยู่ด้วยทุกครั้ง" ไม่ใช่กฎตายตัว ขึ้นกับชนิดหัตถการ + ระเบียบหน่วยงาน*
- 🚫 **ทำไม่ได้:** เจาะ **arterial (ABG)** / jugular / femoral / **ไขกระดูก** / ปอด-ช่องท้อง-ไขสันหลัง, biopsy, สวนปัสสาวะ, ฉีดเข้าหลอดเลือด
- ⚠️ "เจาะเลือด" ที่ MT ทำได้ = **venous/capillary เท่านั้น** — arterial/marrow = นอกขอบเขต แม้ทำเป็น
- 💼 ตอน demo เครื่องในแล็บลูกค้า: **อย่าลงมือเจาะ/เดินผลกับผู้ป่วยจริงแทนเจ้าหน้าที่** — demo บน QC/control ได้, touch คนไข้ = หน้าที่ ทนพ.เจ้าของแล็บ

### Fork 3 — ความลับผู้ป่วย + PDPA (stack กัน)
- **ข้อมูลสุขภาพ = ความลับ** (กฎหมายสุขภาพ) + เปิดเผยจากวิชาชีพ = ผิดอาญา + **PDPA: ข้อมูลสุขภาพ = sensitive data → โดยหลักต้อง explicit consent** — ทั้งหมด **ทับกัน ต้องทำตามทุกชั้น**
- ⚠️ **"ต้อง consent เสมอ" ไม่จริงเป๊ะ** — PDPA ม.26 มี *ข้อยกเว้น*: ทำเพื่อ **รักษาพยาบาล/เวชศาสตร์** ภายใต้ผู้ประกอบวิชาชีพ หรือ **ปกป้องชีวิต (vital interest)** ใช้ข้อมูลได้โดยไม่ต้องขอ consent → งานในแล็บเชิงรักษาปกติเข้าข้อยกเว้นนี้ · แต่ **เอาออกนอกงานรักษา (demo/วิจัย/โพสต์) = ไม่เข้าข้อยกเว้น → ต้อง consent + de-identify เสมอ**
- ก่อนเอาข้อมูล/เคสออกจากแล็บ (demo/case study/วิจัย/โพสต์): **de-identify + consent + ข้อตกลงประมวลผลข้อมูล** · โพสต์เคสโดยไม่ลบ identifier = ผิด
- informed consent: ผู้ป่วยมีสิทธิรู้ข้อมูลพอจะยินยอม/ปฏิเสธ (เว้นฉุกเฉิน)

### Fork 4 — กฎหมายเครื่องมือแพทย์ (น้ำยา/IVD = เครื่องมือแพทย์)
- **ขายน้ำยา/ชุดตรวจ = ขายเครื่องมือแพทย์** → ต้องผ่านบริษัทที่มี **ใบอนุญาตขาย** (ขายนอกระบบ = โทษอาญา)
- ⚠️ **เคลม performance เกินจริง** (sensitivity/spec, "ดีกว่าเจ้าอื่น" ไม่มีหลักฐาน) = โฆษณาเข้าใจผิดในสาระสำคัญ = ผิด
- **product liability:** ผู้ผลิต/นำเข้า/**ขาย** รับผิดร่วมในความเสียหายจากเครื่อง/น้ำยาบกพร่อง (มีข้อยกเว้น/อายุความ) → **เก็บหลักฐาน calibration/QC/มาตรฐานไว้แก้ต่าง**
- 💼 IP clause ในสัญญาจ้าง sales อาจดูดงาน/โค้ดที่สร้างเอง → **ขอ carve-out เป็นลายลักษณ์อักษรก่อนเซ็น**

### Fork 5 — โซเชียลมีเดีย + จริยธรรม
- หลัก **"คิดก่อนโพสต์"** — ⚠️ **เจตนาดีก็ผิดได้** ถ้าระบุโรค/ตัวตนคนไข้ (เช่นโพสต์ขอบริจาคเลือดด่วน + ระบุว่าเป็นโรคอะไร = ผิดกฎหมายความลับสุขภาพ)
- ถ่ายรูปในแล็บ/รพ. + คนไข้ + โพสต์ = เสี่ยงผิดหลายฉบับ ทั้งแพ่ง-อาญา
- **จริยธรรม: "ถูกกฎหมาย ≠ ถูกจริยธรรม"** = judgment ไม่ใช่ rule · ของกำนัล/สินบนต่อแพทย์-แล็บในวงการแพทย์ = เส้นห้ามข้าม (trust ระยะยาว > ดีลเดียว)

---

## กับดัก (Anti-patterns)
- 🚫 **เจาะ arterial/jugular/femoral/ไขกระดูก** — นอกขอบเขต MT (peripheral venous/capillary เท่านั้น)
- 🚫 **ทำหัตถการเสี่ยง (apheresis/OGTT/skin test) โดยไม่มีแพทย์ดูแลตามระเบียบ** — เช็คเงื่อนไขแต่ละหัตถการ (เจาะ whole-blood donor ปกติทำได้ภายใต้ความรับผิดชอบแพทย์)
- 🚫 **โพสต์เคส/รูปคนไข้ แม้เจตนาดี** — ระบุโรค/ตัวตน = ผิดความลับสุขภาพ + PDPA
- 🚫 **เอาข้อมูลคนไข้ออกจากแล็บโดยไม่ de-identify/consent** — ม.ความลับ + PDPA sensitive data
- 🚫 **เคลม performance เกินจริงตอนขาย** — โฆษณาเข้าใจผิด ผิดกฎหมายเครื่องมือแพทย์
- 🚫 **ปล่อยใบ ทนพ. หมดอายุ** ตอนย้ายสาย — เสีย credibility + ประตูกลับ
- 🚫 **เซ็นสัญญา sales โดยไม่อ่าน IP/ข้อผูกมัด** — งานที่สร้างเองอาจถูกดูด

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT) เคสที่เกือบทำนอกขอบเขต/เกือบโพสต์ผิด จับได้เพราะ..."*
> - *"ตอนเซ็นสัญญา/ขายของ จุดกฎหมายที่ผมเจอจริง คือ..."*

---
*ช่วยเข้าใจกรอบกฎหมาย/จรรยาบรรณวิชาชีพ MT เพื่อการศึกษา ไม่ใช่คำปรึกษาทางกฎหมาย — ตัวบท/อัตราโทษต้องตรวจฉบับล่าสุด + ปรึกษานักกฎหมาย/สภาวิชาชีพก่อนตัดสินใจจริง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: never-lose-a-file ═════════ -->

---
skill: never-lose-a-file
title: จัดไฟล์ให้เป็นระเบียบ แล้วไม่หายอีก (Never-Lose-a-File System)
type: ADVISE               # ให้ระบบ+วิธี (ส่วนอัตโนมัติเป็น DO ดูท้ายไฟล์)
needs: any                 # ระบบ: AI ตัวไหนก็ได้ · อัตโนมัติ: ต้อง code tool
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ระบบช่วยจัดระเบียบเพื่อการศึกษา ไม่ใช่ระบบสำรองข้อมูล — ก่อนลบ/ย้ายไฟล์จำนวนมาก สำรอง (backup) ก่อนเสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# จัดไฟล์ให้เป็นระเบียบ แล้วไม่หายอีก

> **ทำเลย:** เลือก **"บ้านเดียว"** (เช่น Google Drive) ทำงานในนั้นเสมอ + ตั้งชื่อ **`YYYY-MM-DD_เรื่อง_v1`** + triage 10 นาที/สัปดาห์ ล้าง Downloads/Desktop ให้เกลี้ยง.
> **กับดักใหญ่สุด:** อย่าแก้งานที่ "ก๊อป" นอกบ้าน (= ต้นเหตุ `final_REAL`). ก่อนลบ/ย้ายเยอะ **backup ก่อนเสมอ**, ห้ามลบข้อมูลดิบวิจัย/เวชระเบียน/เอกสารกฎหมายจนแน่ใจ 100%.

ไฟล์หายไม่ใช่เพราะขาดโปรแกรมเทพ — เพราะ **(1) ไม่มี "บ้านเดียว"** และ **(2) ตั้งชื่อจนหาไม่เจอ**. แก้ 2 อย่างนี้ + นิสัยเล็กๆ ก็พอ

## ใช้เมื่อ
ไฟล์เริ่มหา ไม่เจอ, Downloads/Desktop รก, มีไฟล์ชื่อ `final_REAL` หลายอัน, หรืออยากวางระบบจัดไฟล์ที่ไม่พังซ้ำ

## วิธีใช้
เล่าความรกของคุณให้ AI ฟัง (โฟลเดอร์ไหนมั่วสุด, ไฟล์แบบไหนชอบหาย) → ให้มันออกแบบระบบ + แผน triage ตามด้านล่าง

---

## 3 กฎที่ทำให้ไฟล์ไม่หาย

### กฎ 1 — "บ้านเดียว" ต่อ 1 อย่าง (single home)
**ของแต่ละประเภทมีที่อยู่เดียว** เท่านั้น (งานวิจัยทั้งหมด → `02_Research/` ที่เดียว)
- เลือก **ที่เดียวเป็นหลัก** (เช่น Google Drive) แล้วยึดมัน — อย่ากระจาย Desktop+Downloads+เมล+ไดรฟ์

### กฎ 2 — ตั้งชื่อให้ search เจอ (`วันที่_เรื่อง_เวอร์ชัน`)
**รูปแบบเดียว: `YYYY-MM-DD_เรื่อง_v1`** เช่น `2026-05-31_R2R-stats_v2.xlsx` (วันที่ขึ้นต้น = เรียงเองตามเวลา + search เจอด้วยคำเดียว)
- ❌ เลิก: `เอกสาร(3).pdf`, `final_REAL_ใช้อันนี้.docx`

### กฎ 3 — triage ทุกสัปดาห์ (อย่าให้ inbox กลายเป็นสุสาน)
**10 นาที/สัปดาห์: เปิด Downloads + Desktop + inbox → ทุกชิ้น ย้ายเข้าบ้าน/ลบ ห้ามค้าง**
- กฎเหล็ก: **ห้ามมีไฟล์นอนใน Downloads เกิน 7 วัน**

## โครงโฟลเดอร์ (อย่า nest ลึก — ลึก = หาย)
ใช้ **by ชีวิต/งาน ระดับเดียว** เช่น:
```
01_งานประจำ   02_เรียน/วิจัย   03_การเงิน   04_ส่วนตัว   05_archive   00_inbox
```
- ลึกไม่เกิน **2-3 ชั้น** · ไม่มีโฟลเดอร์ชื่อ "เบ็ดเตล็ด/misc" (= หลุมดำ)

## "ของชิ้นนี้ไปไหน?" — ตัดสินใจ 5 วิ
> ใช้บ่อย? → บ้านงานที่เกี่ยว · เก็บอ้างอิง? → 05_archive · ไม่รู้/ไม่ใช้แล้ว? → **ย้ายเข้า 05_archive ก่อน** (ลบจริงเฉพาะหลังสำรอง + แน่ใจว่าไม่ใช่ข้อมูลดิบวิจัย/เวชระเบียน/เอกสารกฎหมาย)

## ไฟล์หายจริงๆ ตรงไหน (สิ่งที่คนเคยเสียงานเท่านั้นรู้)
- ไฟล์ที่หายมัก **ไม่ได้อยู่ใน Downloads** — แต่เป็น "อันที่เมลหาตัวเองแล้วไม่เคยโหลดกลับ / Google Doc ที่สร้างผิด account / ไฟล์ใน LINE chat / USB ที่ รพ. / shared drive ที่คนอื่นจัดใหม่"
- `v_final_REAL_ใช้อันนี้` เกิดเพราะ **แก้ที่ "ก๊อป" ไม่ใช่ที่ "บ้านจริง"** → ทางแก้ไม่ใช่ตั้งชื่อ แต่คือ **ห้ามทำงานนอกบ้านเดียว**
- (MT) ที่ไฟล์แลป/วิจัยตายบ่อย: LINE, USB ที่หน่วยงาน, ไดรฟ์รวมที่คนอื่นย้าย

## กับดัก (Anti-patterns)
- ระบบซับซ้อนเกิน (tag 50 อัน, โฟลเดอร์ 6 ชั้น) → ไม่มีใครทำต่อ → ลองง่ายๆ ก่อน
- เก็บไฟล์ซ้ำ "เผื่อ" → ลบตัวซ้ำ เหลือต้นฉบับเดียว
- เลื่อน triage → ตั้งเตือนประจำ (เช่น ศุกร์เย็น 10 นาที)

---

## ส่วนอัตโนมัติ (สำหรับคนใช้ code tool — Claude Code/Codex/local Python)

> **อ่านก่อน:** ส่วนนี้สำหรับคนใช้โปรแกรมรันโค้ดบนเครื่องตัวเอง (เช่น Claude Code) เท่านั้น — แชทเว็บทั่วไป (ChatGPT/Claude/Gemini) แตะไฟล์ในเครื่องคุณไม่ได้ (sandbox). ถ้าไม่ใช่สายเทค ใช้แค่ "3 กฎ" ด้านบนพอ (ทำมือ 10 นาที/สัปดาห์ ได้ผลจริง)

บอก AI ที่รันโค้ดได้ว่า *"เขียนสคริปต์จัดไฟล์ตามระบบนี้"* → ให้มันทำ:
1. **สแกน Downloads/Desktop** → จัดเข้าโฟลเดอร์ตามชนิด/นามสกุล
2. **เปลี่ยนชื่อ** เป็น `YYYY-MM-DD_เรื่อง` (ใช้วันที่ไฟล์)
3. **หาไฟล์ซ้ำด้วย hash** (md5) → รายงาน/ลบตัวซ้ำ
4. **รายงานก่อนทำจริง (dry-run)** + ให้ยืนยัน — *backup ก่อนเสมอ*

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมระบบจัดไฟล์ที่ใช้จริงในสายงานคุณ เช่น:
> - *"(MT) ผมจัดไฟล์ผล QC/วิจัย/เอกสาร ISO แบบ... เพราะ..."*
> - *"ไฟล์ที่เคยหายแล้วเจ็บ คือ... ตอนนี้กันด้วย..."*

---
*ระบบช่วยจัดระเบียบเพื่อการศึกษา ไม่ใช่ระบบสำรองข้อมูล — ก่อนลบ/ย้ายไฟล์จำนวนมาก สำรอง (backup) ก่อนเสมอ และอย่าลบข้อมูลดิบวิจัย เวชระเบียน หรือเอกสารกฎหมายจนกว่าจะแน่ใจ 100% · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: offload-to-automation ═════════ -->

---
skill: offload-to-automation
title: งานที่ต้องเป๊ะ โยนให้ automation — AI แค่บังคับ+ตรวจ (Automate It, Don't Improvise)
type: CALIBRATION          # เปลี่ยนวิธีที่ AI ลงมือทำงาน
needs: any                 # ใช้ได้ทุก AI · เต็มที่สุดกับ AI ที่รัน code/tool ได้
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยจัดให้ AI พึ่ง automation กับงานที่ต้องเป๊ะ เพื่อการศึกษา ไม่ใช่คำสั่งทางการ — ต้องตรวจ output ของ tool ก่อนเชื่อ และคงการตัดสินใจที่ต้องใช้ดุลพินิจคนไว้ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# งานที่ต้องเป๊ะ โยนให้ automation — AI แค่บังคับ+ตรวจ

หยุดให้ AI "คิดเลข/จัดตารางในหัว" → ให้มัน **สร้าง/ขับเครื่องมือที่คำนวณเป๊ะ แล้วตรวจผล** แทน

> LLM ทำนายคำถัดไป มัน**ไม่ได้คิดเลขจริง** — งานที่มีคำตอบถูก-ผิดชัด (เลข เงิน นับ เรียง จัดเวร) มันจะตอบอย่างมั่นใจแต่เพี้ยน. ทางแก้ไม่ใช่ "ขอให้ AI ระวังขึ้น" แต่คือ **ย้ายงานเป๊ะออกไปให้ code/tool ทำ แล้วให้ AI เป็นคนขับ + คนตรวจ** ไม่ใช่ตัวคำนวณเอง

> ⛔ **ก่อนตอบ — เช็คก่อนพิมพ์คำตอบ:** งานนี้มี คำนวณ / นับ / เรียง / จัดเวร / constraint ไหม?
> ถ้าใช่ → **ห้ามตอบตัวเลขจากหัวเด็ดขาด.** เขียน code/solver ก่อน แล้วค่อยตอบจากผลที่รัน
> รัน code ไม่ได้? → ส่ง **โค้ดที่รันได้จริง + วิธี verify + ติดป้ายว่า "ตัวเลขยังไม่ยืนยันจนกว่าจะรัน"** ออกมา
> ✅ คำตอบที่ดีของงานแบบนี้ = โค้ดรันได้ + sanity check + กรอบที่ถูก — **ไม่ใช่** การปฏิเสธ และ**ไม่ใช่**เลขเดาที่ฟังดูมั่นใจ

## ใช้เมื่อ
- งานมีการคำนวณ/จัดเรียง/แก้เงื่อนไขที่ต้องเป๊ะ (จัดเวร, คิดเงิน, สรุปตัวเลข, นับสต็อก)
- เคยให้ AI ทำแล้วผลเพี้ยน/ไม่นิ่ง (ถามซ้ำได้คนละคำตอบ)
- งานทำซ้ำบ่อย / ข้อมูลเยอะเกินกว่าจะตรวจด้วยตา
- อยากได้ผลที่ **reproducible** (รันใหม่ได้เหมือนเดิม)

## วิธีใช้
วาง skill นี้ + เล่างาน → AI จะ (1) แยกว่าส่วนไหนต้องเป๊ะ (2) เสนอ/เขียน automation มาทำส่วนนั้น (3) ตรวจผลให้ + อธิบาย ไม่เดาตัวเลขเอง

---

## วิธีทำ (AI: ทำตามนี้)

### ขั้น 1 — แยกงานก่อน: "เป๊ะได้" vs "ต้องใช้ภาษา/ดุลพินิจ"
- **deterministic (มีคำตอบถูกชัด)** → เลข, นับ, เรียง, filter, จัดตาราง, constraint → **โยนให้ automation**
- **ภาษา/ความหมาย/judgment** → สรุป, เรียบเรียง, ตีความ, ให้คำแนะนำ, ตัดสินความเหมาะสม → **AI ทำเองได้**

### ขั้น 2 — งานเป๊ะ = เขียน/เรียกเครื่องมือ ไม่คิดในหัว
- เขียน code (Python/สูตร spreadsheet) หรือเรียก solver/tool ให้คำนวณ
- ❌ ห้ามตอบตัวเลข/ตารางจากการ "ประมาณในหัว" แล้วเสนอเหมือนคำตอบจริง

### ขั้น 3 — AI = คนขับ (orchestrator) ไม่ใช่ engine
- AI: เข้าใจปัญหา → แปลงเป็น input ของ tool → สั่งรัน → รับผลกลับ → แปลผลให้คนเข้าใจ
- ผิดพลาด/รันไม่ผ่าน → AI อ่าน error แล้วแก้ tool ไม่ใช่ "เดาคำตอบแทน"

### ขั้น 4 — Verify เสมอ (ห้ามเชื่อ output ดิบ)
- sanity check: ผลสมเหตุสมผลไหม (เวรรวมครบทุกกะ? คนไม่โดนซ้อน? ยอดบวกได้ตรง?)
- เช็ค constraint ทุกข้อที่ตั้งไว้ · code มี bug ได้ → ตรวจก่อนส่ง
- ตัวเลขสำคัญ → ลองวิธีที่ 2 (cross-check) ถ้าทำได้

### ขั้น 5 — ถ้ารัน tool ไม่ได้ (AI ตัวนั้นรัน code ไม่ได้) → บอกตรงๆ
- ให้ **สูตร / โค้ด / ขั้นตอน** ที่ผู้ใช้เอาไปรันเอง + บอกว่า "ตัวเลขต้องได้จากการรัน อย่าเชื่อที่ผมกะ"
- อย่าแสร้งคำนวณเป๊ะทั้งที่ทำไม่ได้

### ขั้น 6 — อย่า over-automate งานที่ต้องใช้ดุลพินิจคน
- ส่วนที่เป็น **ความเป็นธรรม / บริบทคน / ค่านิยม** (ใครควรได้เวรดึกน้อยเพราะมีลูกเล็ก, ใครเพิ่งป่วย) = ไม่ใช่ constraint แข็ง → ให้ automation จัด "โครง" แล้วเว้นให้คนปรับ ไม่ใช่ปล่อยให้สูตรตัดสินชีวิตคน

---

## ทำเอง vs โยน automation

| สัญญาณ | ทางที่ใช่ |
|---|---|
| มีคำตอบถูก-ผิดชัด, ต้องเป๊ะ 100% | **automation** (code/solver) |
| constraint หลายตัว / combinatorial (จัดเวร, ตารางสอบ, แบ่งโหลด) | **automation** |
| ทำซ้ำบ่อย / ต้อง reproducible / ข้อมูลเยอะ | **automation** |
| ภาษา, สรุป, ตีความ, คำแนะนำ, โทนการสื่อสาร | **AI ทำเอง** |
| one-off, ไม่ต้องเป๊ะ, ไม่มี "คำตอบเดียวถูก" | **AI ทำเอง** |
| ความเป็นธรรม / บริบทคน / คุณค่า | **คนตัดสิน** (automation จัดโครงให้) |

---

## กับดัก (Anti-patterns)
- **ให้ AI คิดเลข/จัดตารางในหัวแล้วเชื่อ** — มันมั่นใจเสียงดังแต่ผิด; ถามซ้ำได้คนละคำตอบ = สัญญาณว่ามันเดา
- **สร้าง automation แล้วไม่ตรวจ output** — code มี bug ก็เชื่อ; เป๊ะของ tool ≠ ถูกของ logic
- **AI แสร้งคำนวณทั้งที่รัน tool ไม่ได้** — ต้องบอกตรงๆ + ส่งสูตร/โค้ดให้คนรัน
- **over-automate งานดุลพินิจ** — ยัดความเป็นธรรม/บริบทคนเป็นสูตร → ได้ตารางที่ "ถูกตามกฎ แต่ใจร้าย"
- **"AI ฉลาด = ทำได้ทุกอย่างเอง"** — ใช้ผิดเครื่องมือ; ของฉลาดคือรู้ว่าเมื่อไหร่ควรหยิบเครื่องคิดเลข
- **automation ลอย ไม่มีคนคุม** — ต้องมี AI บังคับ + คนตรวจปลายทางเสมอ

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมงานในสายคุณที่ "ต้องโยนให้ automation" + เคยพลาดเพราะให้ AI ทำเอง เช่น:
> - *"จัดเวร/แบ่งงานในแล็บ ผมให้ AI ทำเองแล้วพัง เพราะ... ตอนหลังใช้... แทน"*
> - *"คำนวณ... (เจือจาง/ลง CAPA/คิวซี) ที่ห้ามให้ AI กะเอา ต้อง..."*
> - *"ส่วนที่ดูเหมือน automate ได้ แต่จริงๆ ต้องให้คนตัดสิน คือ..."*

---
*ช่วยจัดให้ AI พึ่ง automation กับงานที่ต้องเป๊ะ เพื่อการศึกษา ไม่ใช่คำสั่งทางการ — ต้องตรวจ output ของ tool ก่อนเชื่อ และคงการตัดสินใจที่ต้องใช้ดุลพินิจคนไว้ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: optimization-judgment ═════════ -->

---
skill: optimization-judgment
title: โค้ช Optimization/OR — เลือกวิธีให้ถูก + คำตอบใช้ได้จริง (Optimization Judgment)
type: ADVISE               # ช่วยตัดสินใจ formulate/เลือกวิธี ไม่ใช่ตำรา Simplex
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดเลือกวิธี optimize + เลี่ยงกับดัก เพื่อการศึกษา ไม่ใช่คำสั่งทางการ — ผลต้องตรวจกับเงื่อนไขจริงและทดสอบก่อนใช้ตัดสินใจจริง (เช่นจัดเวร/จัดสรรทรัพยากร) · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช Optimization/OR — เลือกวิธีให้ถูก + คำตอบใช้ได้จริง

มีปัญหาแบบ "หาค่าที่ดีที่สุดภายใต้เงื่อนไข" (จัดเวร, จัดสรรเครื่อง/คน/น้ำยา, เส้นทาง) → โค้ชนี้ช่วย **เลือกวิธี + เลี่ยงกับดักที่ทำให้คำตอบใช้จริงไม่ได้**

> **กฎ #1 (เลือกวิธี):** เชิงเส้น + แน่นอน (deterministic) + เล็ก-กลาง → ใช้ **LP/MIP** เสมอ (รับประกัน optimal) — อย่าเพิ่งหยิบ GA/PSO. ไป metaheuristic เฉพาะตอน nonlinear/combinatorial/ใหญ่มาก, ไป simulation เฉพาะตอนมี randomness/คิว. **หยิบ GA ทั้งที่ LP แก้ได้ = over-engineer ผิด.**
> **กับดัก #1 (คำตอบพัง):** **ลืม constraint** → optimal สวยแต่ละเมิดเงื่อนไขจริง = ใช้ไม่ได้. ก่อน solve ต้อง formulate ครบ 3 ชิ้น (objective · decision vars · constraints) แล้ว **ไล่ constraint จากโจทย์คำต่อคำ** (รวม ≥0, integer, capacity).
> งานเลข Simplex/PSO อย่าให้ AI กะในหัว → ใช้ solver (ดู `offload-to-automation`)

## ใช้เมื่อ
- ตั้งโจทย์ optimization / เลือก solver-method / ทำ sensitivity analysis
- "ใช้ LP หรือ heuristic", "จัดเวร/จัดสรรยังไงให้ดีสุด", "อ่าน shadow price ยังไง"

## วิธีใช้
วาง skill นี้ + เล่าปัญหา → AI บังคับ formulate ก่อน แล้วชี้วิธี + กับดัก

---

## วิธีเลือก (AI: ทำตามนี้) — forks

### 1. exact (LP/MIP) vs metaheuristic (GA/PSO) vs simulation — ข้อใหญ่สุด
- **เชิงเส้น + deterministic + เล็ก-กลาง** → **LP/Simplex/MIP** (Excel Solver, OR-Tools, GUROBI) — รับประกัน optimal = **default**
- **nonlinear / combinatorial / ใหญ่มาก (NP-Hard เช่น จัดเวร, VRP, TSP)** → **metaheuristic (GA/PSO/ACO)** — ได้ "ดีพอ" ไม่รับประกัน optimal
- **มี randomness/queue/เวลา แก้เป็นสมการไม่ได้** (คิวคนไข้, โหลดเครื่อง) → **simulation (Monte Carlo/DES)** — ได้การกระจาย (utilization, waiting time)
- ✅ test: เขียน objective+constraint เป็นสมการเชิงเส้นได้ครบ → อย่าใช้ GA (over-engineer); เขียนไม่ได้เพราะมี randomness → อย่าใช้ LP

### 2. GA vs PSO (ในกลุ่ม metaheuristic)
- อยาก converge เร็ว, พารามิเตอร์น้อย, ตัวแปร **ต่อเนื่อง** → **PSO**
- มีโครงสร้าง **combinatorial / encode เป็น gene ได้ / ต้อง explore กว้าง** → **GA**

### 3. single vs multi-objective (Pareto)
- objective เดียว → optimize ตรงๆ
- หลาย objective ขัดกัน (max คุณภาพ vs min cost) → รู้ weight ชัด → **Weighted Sum** (ได้ 1 จุด); อยากเห็น trade-off ทั้งชุด → **Pareto front (NSGA-II)** แล้วค่อยเลือก
- ✅ อย่ายัด weight มั่วถ้ายังไม่รู้ trade-off — หา Pareto ก่อน

### 4. network model (เมื่อปัญหาเป็น node + arc)
ส่งตรง min cost → **Transportation** · จับคู่ 1:1 → **Assignment** · ผ่าน node กลาง → **Transshipment** · เส้นสั้นสุด → **Shortest Path** · flow สูงสุด (arc มี capacity) → **Maximal Flow** · เชื่อมทุก node ถูกสุด → **Min Spanning Tree**

### 5. formulation ต้องครบ 3 ชิ้นก่อนแตะ solver
Decision Variables + Objective (ในรูป vars) + Constraints (สมการ/อสมการ) · LP ได้ก็ต่อเมื่อ ต่อเนื่อง + ไม่มี xi·xj + ไม่มี x² + deterministic — ผิดข้อใด = ไม่ใช่ LP

### 6. sensitivity: shadow price ("คุ้มจะเพิ่มทรัพยากรไหม")
- **Shadow price** = objective เปลี่ยนเท่าไรต่อการเพิ่ม RHS ของ constraint 1 หน่วย = ยอมจ่ายเพิ่มได้สูงสุดเท่าไรต่อ 1 หน่วย
- **Binding** (slack=0) → SP>0 → เพิ่มทรัพยากรช่วยได้ (ลงทุนถ้าราคา < SP) · **Non-binding** (มี slack) → SP=0 → เพิ่มไม่ช่วย อย่าซื้อ
- Δobjective = SP × ΔRHS **เฉพาะใน allowable range**

---

## กับดัก (Anti-patterns)
- **ลืม constraint → solution ใช้จริงไม่ได้** (#1) — optimal สวยแต่ละเมิดเงื่อนไขที่ไม่ได้เขียน (ลืม ≥0, capacity, ต้องบริการครบ) → เช็คทุก constraint จากโจทย์คำต่อคำก่อน solve
- **ลืม integer constraint** — ต้องเป็นจำนวนเต็ม (รถ/คน/เครื่อง) แต่ solve เป็น LP ต่อเนื่อง → ได้ 2.7 = ใช้ไม่ได้ → ใช้ **MIP**
- **อ่าน Infeasible vs Unbounded ผิด** — Infeasible = constraint ขัดกัน (ผ่อน constraint) · Unbounded = มักแปลว่า **ลืม constraint** (วนกลับข้อแรก)
- **greedy/local search ติด local optimum** — GA ต้องมี mutation, PSO ต้อง diversity; รันรอบเดียวแล้วเชื่อ = พลาด → รันหลาย seed
- **over-model** — ยัด GA/nonlinear ทั้งที่ LP เล็กแก้ได้ใน 1 วิ; เริ่มจากโมเดลง่ายสุดที่ตอบโจทย์
- **simulation รันน้อย → CI กว้าง สรุปมั่ว** — เพิ่ม replication จน CI แคบพอ
- **GIGO** — input/distribution ผิด → optimal ก็ไร้ค่า; ตรวจ assumption ก่อนเชื่อ
- **ใช้ shadow price นอก allowable range / ของ non-binding** → ตัดสินใจลงทุนผิด
- **ตัวแปรคูณกัน/มี x² แล้วยังเรียก LP** → nonlinear, Simplex ใช้ไม่ได้

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT) จัดเวร/จัดสรรเครื่องในแล็บ ผมใช้... เพราะ constraint จริงคือ..."*
> - *"ปัญหาที่ดูเหมือน LP แต่จริงๆ มี randomness ต้องใช้ simulation คือ..."*

---
*ช่วยคิดเลือกวิธี optimize + เลี่ยงกับดัก เพื่อการศึกษา ไม่ใช่คำสั่งทางการ — ผลต้องตรวจกับเงื่อนไขจริงและทดสอบก่อนใช้ตัดสินใจจริง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: parasitology-judgment ═════════ -->

---
skill: parasitology-judgment
title: ตัวช่วยตัดสินใจในแล็บปรสิตวิทยา (Parasitology Lab Judgment)
type: ADVISE
needs: any
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "skill นี้ช่วย 'คิด' การตัดสินใจในแล็บปรสิตวิทยา เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย/รายงาน — ผลลบจาก stool/film ตัวอย่างเดียว 'ไม่ตัดโรคออก' การเลือก technique/stain/การตีความทุกครั้งต้องทำตาม SOP ของหน่วยงาน และยืนยันกับ MT ผู้รับผิดชอบ/แพทย์เสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ตัวช่วยตัดสินใจในแล็บปรสิตวิทยา

ตัวช่วยตัดสินใจในแล็บปรสิตวิทยาสำหรับ MT — เน้น "เลือก technique/stain/ตีความยังไง" + "พลาดตรงไหน" ไม่ใช่ลอก atlas รูปไข่/life cycle

> **กฎ #1:** ผลลบจาก stool หรือ film ตัวอย่างเดียว "ไม่ตัดโรคออก" — ต้องตรวจซ้ำตามจำนวนที่กำหนด (malaria ซ้ำทุก 12-24 ชม. × ≥3 ครั้ง · stool rule-out 3 ตัวอย่างวันเว้นวัน · E. histolytica 6 ครั้ง) ก่อนรายงาน "ไม่พบ"
> **กับดัก #1:** เลือก stain/technique ไม่ตรงเป้า แล้วมองข้ามเชื้อ — oocyst (Crypto/Cyclospora/Cystoisospora) ต้อง modified acid-fast · microsporidia spore ต้อง modified trichrome · ภูมิต่ำ/HIV ท้องเสีย = สั่ง 2 อย่างนี้ทันที (ย้อมธรรมดามองไม่เห็น)

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
- Thick film = gold standard ความไว (lyse RBC) → screen + ประเมิน density/parasite count · threshold ~20/µl เป็นตัวเลข *สภาวะอุดมคติ/ผู้เชี่ยวชาญ* ภาคสนามจริงแย่กว่ามาก (~100-500/µl) → WHO นับเป็น "negative" ได้ต่อเมื่ออ่านครบ ≥100 thick field
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
- Microfilaria (W.bancrofti/B.malayi) → เจาะเลือดกลางคืน (nocturnal periodicity, peak ~22:00-02:00) หรือ provocation: DEC 2mg/kg → เจาะ ~30-60 นาทีหลัง DEC (peak, ตาม SOP) · เจาะกลางวัน = false-neg · ข้อยกเว้น: สายพันธุ์ South-Pacific W.bancrofti เป็น subperiodic/diurnal → timing ไม่วิกฤต · circulating filarial antigen (ICT) เจาะเวลาไหนก็ได้
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


<!-- ═════════ skill: pathology-judgment ═════════ -->

---
skill: pathology-judgment
title: โค้ชพยาธิวิทยา — อ่าน pattern + ให้เกณฑ์ + confirm (Pathology Pattern Judgment)
type: ADVISE               # ช่วยอ่าน pattern/กลไก ไม่ใช่ตำราลิสต์โรค
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดอ่าน pattern/กลไกโรคทางพยาธิ เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย — การวินิจฉัยพยาธิจริงต้องโดยพยาธิแพทย์ + ยืนยันด้วย test/IHC/molecular ตาม SOP · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชพยาธิวิทยา — อ่าน pattern + ให้เกณฑ์ + confirm

อ่านกลไกโรค + ตัดสิน pattern ทางพยาธิ — "นี่ benign/malignant? injury กลับได้ไหม? อักเสบบอกอะไร? ต้อง confirm ด้วยอะไร" ไม่ใช่ท่องลิสต์โรค/Robbins (= commodity ดูตำรา)

> **กฎ #1 (benign vs malignant):** **invasion ทะลุ basement membrane / metastasis = ตัวชี้ขาด** — **atypia/pleomorphism/mitosis อย่างเดียวไม่เคยพอ** ฟันธงมะเร็ง (reactive atypia จากอักเสบ/ซ่อมหลอกตาได้)
> **กับดัก #1:** ตี atypia เดี่ยว = มะเร็ง → ผิด. ดูว่า "ทะลุ BM ยัง / มี metastasis ไหม" ก่อนเสมอ
> ⚠️ **ขอบที่ลื่น:** metastasis เป็น **เกณฑ์เดี่ยวที่แข็งสุด** แต่ **ไม่ใช่ 100%** — มีข้อยกเว้นหายาก (Spitz nevus, benign metastasizing leiomyoma); ไม่มีเกณฑ์ใดเกณฑ์เดียวฟันธงเด็ดขาด → อ่านครบทุกแกน + confirm ด้วย test ที่ถูก
> เชื่อมเคส lab → ตั้ง DDx/ชี้ทาง (ส่งต่อแพทย์) → ดู `clinical-correlation-judgment`

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- อ่านชิ้นเนื้อ/รายงานพยาธิ/เคส → **benign หรือ malignant**, dysplasia ข้ามเส้นยัง, grade/stage
- เชื่อมโยง **lab/morphology → กลไกโรค** (ทำไมค่านี้ผิด, อักเสบแบบไหน, injury กลับได้ไหม)
- (สาย sales) เข้าใจ pathophysiology โรค → ทำไม test/biomarker/companion Dx จำเป็นใน pathway

## วิธีใช้
วาง skill นี้ + เล่าภาพ/รายงาน/เคส → AI อ่าน pattern + เกณฑ์ (benign/malignant · reversible/irreversible · acute/chronic) → confirm + ส่งต่อพยาธิแพทย์

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — Benign vs Malignant (เกณฑ์ 5 แกน — metastasis แน่สุด)
อย่าตัดสินจากแกนเดียว — ดูครบ:
| แกน | Benign | Malignant |
|---|---|---|
| Differentiation | ดี เหมือนเนื้อต้นกำเนิด | anaplasia, pleomorphism, N:C สูง, mitosis ผิดปกติ |
| Growth rate | ช้า | เร็ว |
| **Invasion** | มี capsule ไม่ลุก | **ทะลุ basement membrane / ลุกลามรอบ** |
| **Metastasis** | ไม่มี | **มี = พิสูจน์ malignant แน่นอนสุด** |
| Border | ขอบเรียบ | ขอบรุก |
- ⚠️ **metastasis = เกณฑ์เดี่ยวที่แข็งสุด** (เกือบทั้งหมด benign ไม่ metastasis) — แต่ **ไม่ใช่ 100%** (Spitz nevus, benign metastasizing leiomyoma เป็นข้อยกเว้นหายาก); ตัวอื่นช่วยชี้แต่ไม่ขาด
- ⚠️ **atypia/mitosis เดี่ยว ≠ มะเร็ง** — reactive atypia (อักเสบ/ซ่อม) ดูดุได้; เส้นตัดสินจริงที่อ่านได้คือ **ทะลุ BM / invasion** (Fork 7)
- nomenclature: -oma = benign · carcinoma (epithelial)/sarcoma (mesenchymal) = malignant · ⚠️ ข้อยกเว้นหลอก: **lymphoma/melanoma/seminoma = malignant** แม้ลงท้าย -oma

### Fork 2 — Reversible vs Irreversible cell injury (point of no return)
- **Reversible:** cell swelling, fatty change, ribosome หลุด — ตัดต้นเหตุแล้วฟื้น
- **Irreversible:** **เยื่อหุ้มเซลล์/mitochondria พัง + Ca²⁺ ไหลเข้า + เอนไซม์รั่ว** → necrosis · สัญญาณ: nuclear change (pyknosis→karyorrhexis→karyolysis), enzyme รั่วเข้าเลือด (troponin/AST/LDH)
- judgment: เห็น enzyme รั่ว (cardiac/liver) = เซลล์ตายจริง ไม่ใช่บาดเจ็บชั่วคราว

### Fork 3 — Necrosis type → ชี้สาเหตุ/ตำแหน่ง
**Coagulative** = ischemia/infarct อวัยวะแข็ง (หัวใจ/ไต) · **Liquefactive** = สมอง (CNS infarct)/หนอง (bacterial) · **Caseous** = **TB/granuloma** · **Fat** = ตับอ่อนอักเสบ (saponification) · **Fibrinoid** = vessel ใน immune/vasculitis/malignant HT · **Gangrene** = แขนขา ischemia (dry/wet) — อ่านชนิด necrosis ย้อนหาสาเหตุได้

### Fork 4 — Necrosis vs Apoptosis (มีอักเสบหรือไม่)
- **Necrosis** = บาดเจ็บ เซลล์บวมแตก เนื้อหารั่ว → **มี inflammation**
- **Apoptosis** = programmed เซลล์หด apoptotic body **ไม่มี inflammation** (councilman body, เซลล์ที่ถูกกำจัดปกติ)

### Fork 5 — Acute vs Chronic inflammation → implication
- **Acute** = นาที-วัน, **neutrophil**, exudate, 5 อาการ (rubor/tumor/calor/dolor/functio laesa)
- **Chronic** = สัปดาห์+, **lymphocyte/plasma cell/macrophage**, มี **tissue destruction + repair (fibrosis) + angiogenesis** พร้อมกัน
- ⚠️ **chronic inflammation = ปัจจัยเสี่ยงมะเร็ง** (HBV→HCC, H.pylori→gastric, chronic colitis→colon, O.viverrini→cholangio) → เห็น chronic ที่ไหน คิดถึง malignant transformation · granuloma (subtype) → Fork 8

### Fork 6 — Grading vs Staging (อันไหน drive อะไร)
- **Grade** = เนื้อร้ายดูดุแค่ไหน (differentiation, mitosis) — well/moderate/poorly diff
- **Stage (TNM)** = ลุกลามไปไกลแค่ไหน (Tumor invasion, Node, Metastasis)
- ⚠️ **Staging มีผลต่อ prognosis + เลือกการรักษา > grading** (M1 = เปลี่ยนเกม) → ตอบ "ทำไม biopsy + imaging + sentinel node" = เพื่อ stage
- *(สาย sales)* companion Dx/molecular มักเข้ามาที่จุด "เลือก targeted therapy ตาม stage/marker"

### Fork 7 — Dysplasia → Cancer (เส้นแบ่งคือ basement membrane)
- **Dysplasia** (low→high grade) = เซลล์ผิดปกติแต่ **ยังไม่ทะลุ BM** = reversible ได้ · **CIS** = ผิดเต็มความหนาแต่ยังไม่ทะลุ · **Invasive cancer** = **ทะลุ BM แล้ว** = irreversible, metastasis ได้
- judgment: รายงานบอก "ทะลุ BM ยัง" = จุดตัดสินสำคัญสุด (in-situ vs invasive เปลี่ยนการรักษาทั้งหมด)

### Fork 8 — Effusion · Thrombus vs clot · Granuloma DDx · Hypersensitivity
- **Exudate (อักเสบ/มะเร็ง/ติดเชื้อ) vs Transudate (CHF/cirrhosis/nephrotic)** → ตัดสินด้วย **Light's criteria เป็นหลัก** (pleural/serum protein >0.5 · LDH ratio >0.6 · LDH >⅔ ULN — เข้าข้อใดข้อหนึ่ง = exudate); **SG/โปรตีนเป็นแค่ตัวประมาณคร่าว** (SG cutoff จริง ~1.022 ไม่ใช่ 1.020) · Light's เองก็ misclassify transudate ~15-20% เป็น exudate → exudate ต้องหา cause (มะเร็ง/ติดเชื้อ) + ส่ง cytology
- **Thrombus (ก่อนตาย) vs postmortem clot:** thrombus = **lines of Zahn** + เกาะผนัง vessel · postmortem = "chicken fat/currant jelly" ไม่เกาะ
- **Granuloma → DDx:** **caseating = TB** (confirm AFB/culture/GeneXpert ก่อนเสมอ) · non-caseating = sarcoid/Crohn/foreign body/leprosy/fungal → อย่าฟันธง TB จากภาพอย่างเดียว
- **Hypersensitivity I–IV:** I = IgE/anaphylaxis · **II = Ab ต่อ Ag บนเซลล์** (transfusion reaction, HDFN, AIHA) · **III = immune complex ลอย** (SLE, serum sickness, GN) · IV = T-cell delayed (TB skin test, contact derm) → สับบ่อยที่ **II (Ag ติดเซลล์) vs III (complex ลอยแล้วตก)**

---

## กับดัก (Anti-patterns)
- 🚫 **ฟันธง malignant จาก atypia/mitosis เดี่ยว** — ไม่เคยพอ; **invasion ทะลุ BM / metastasis** คือตัวชี้ขาด · reactive atypia (อักเสบ/ซ่อม) ดูน่ากลัวแต่ไม่ใช่มะเร็ง · กลับกัน อย่าอ่าน metastasis ว่า 100% (ข้อยกเว้นหายากมี)
- 🚫 **tumor marker / IHC เดี่ยว = วินิจฉัย** — marker (PSA/CEA/CA125/AFP) ใช้ติดตาม/ชี้ทาง ไม่ใช่ฟันธง; IHC ต้องเป็น panel + บริบท morphology
- 🚫 **miss invasion ผ่าน basement membrane** — in-situ vs invasive ต่างกันที่ BM = เปลี่ยนการรักษา/พยากรณ์ทั้งหมด
- 🚫 **granuloma = TB เลย** ไม่ confirm — caseating ชวน TB แต่ต้อง AFB/culture/molecular ยืนยัน
- 🚫 **ตี postmortem clot เป็น thrombus** — ไม่มี lines of Zahn + ไม่เกาะผนัง = clot หลังตาย
- 🚫 **มองข้าม malignant effusion** — exudate (ตาม Light's, ไม่ใช่ SG เดี่ยว) ต้องส่ง cytology หาเซลล์มะเร็ง; ตี exudate เป็น transudate = พลาด cause
- 🚫 **ลืม chronic inflammation = precancer** — chronic ที่ไม่หาย (HBV/HCV, H.pylori, fluke, colitis) → เฝ้าระวัง dysplasia/มะเร็ง
- 🚫 **สับ necrosis กับ apoptosis** — apoptosis ไม่มีอักเสบ; เห็นอักเสบรอบ = necrosis
- 🚫 **สับ hypersensitivity II vs III** — transfusion/AIHA = II (Ag บนเซลล์); SLE/serum sickness = III (complex ลอย)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติม war-story จริง เช่น:
> - *"(MT) เคสที่เกือบอ่าน reactive atypia เป็นมะเร็ง จับได้เพราะ..."*
> - *"granuloma ที่ดูเหมือน TB แต่จริงเป็น... จับได้เพราะ confirm ด้วย..."*

---
*ช่วยคิดอ่าน pattern/กลไกโรคทางพยาธิ เพื่อการศึกษา ไม่ใช่คำสั่งวินิจฉัย — การวินิจฉัยพยาธิจริงต้องโดยพยาธิแพทย์ + ยืนยันด้วย test/IHC/molecular ตาม SOP · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: pharmacology-judgment ═════════ -->

---
skill: pharmacology-judgment
title: โค้ชยาเบื้องต้น — ADME/แพ้ยา/ยาตีกัน/pharmacogenomics (Pharmacology Judgment)
type: ADVISE               # ช่วยเข้าใจ/เฝ้าระวังเรื่องยา ไม่ใช่สั่งจ่ายยา
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิด/เฝ้าระวังเรื่องยาเพื่อการศึกษา ไม่ใช่คำสั่งใช้ยา/สั่งจ่ายยา — MT ไม่สั่งจ่ายยา การใช้/ปรับ/หยุดยาต้องปรึกษาแพทย์/เภสัชกรเสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชยาเบื้องต้น — ADME / แพ้ยา / ยาตีกัน / pharmacogenomics

เข้าใจยาในมุมที่ MT ใช้จริง — "ค่าแล็บ/อาการนี้เกี่ยวกับยายังไง + เฝ้าระวังตรงไหน" ไม่ใช่ท่องชื่อยา/ขนาด (= commodity ดูตำรา/leaflet)

> **กฎเหล็ก: correlate ยาก่อนสรุปค่าแล็บผิดปกติเสมอ** (warfarin→INR · heparin→aPTT · digoxin อ่านคู่ K⁺ · DOAC ทำ PT/aPTT เพี้ยน) — ก่อนตีว่า "ค่าผิด" ถามก่อนว่าได้ยาอะไร
> **กับดักอันดับ 1: สับ "แพ้ยา" กับ "ผลข้างเคียง"** — ผื่น+ไข้+เจ็บคอ หลังยาใหม่ = สัญญาณ SJS/TEN → **หยุดยาทันที + เลี่ยงตลอดชีวิต** (อย่าแค่ปรับวิธีกินเหมือนผลข้างเคียง)
> MT ไม่สั่งจ่ายยา — แต่ต้องรู้ทันว่า **ยาบิดค่าแล็บ/ทำให้แพ้/ตีกัน** ยังไง + จุดที่ genomics เชื่อมกับยา · pharmacogenomics ดู `molecular-judgment` · พิษยา/overdose ดู `toxicology-judgment` · ร้อยกับเคส ดู `clinical-correlation-judgment`

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นที่กระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- อ่านอาการ/ค่าแล็บแล้วสงสัยเกี่ยวกับยา (drug effect/interaction บิดผล)
- แยก **ผลข้างเคียง vs แพ้ยา** · เฝ้าระวังแพ้รุนแรง (SJS/TEN)
- (สาย sales/companion Dx) เข้าใจ trial phase / pharmacogenomics → คุยภาษา pharma

## วิธีใช้
วาง skill นี้ + เล่าอาการ/ยา/ค่าแล็บ → AI ชี้กรอบ ADME/ADR/interaction + กับดัก (ไม่สั่งใช้ยา)

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — ADME: ทำไมตับ/ไตเสื่อม = ยาเป็นพิษ
- **ดูดซึม → กระจาย → เปลี่ยนแปลง(ตับ) → ขับ(ไต)** · ทางให้ยา → ความเร็ว: IV เร็วสุด · ใต้ลิ้น/IM/SC เลี่ยง/ลด first-pass (อันดับขึ้นกับยา/รูปแบบ) · กิน = ผ่าน first-pass ที่ตับ ช้ากว่า · ทา (เฉพาะที่)
- ⚠️ **ตับเสื่อม/ไตเสื่อม/เด็ก/ผู้สูงอายุ → กำจัดยาน้อย → ยาสะสม/ออกฤทธิ์แรง/เป็นพิษ** ที่ขนาดปกติ → นี่คือเหตุผลฉลากเตือน "โรคตับ/ไตปรึกษาแพทย์"

### Fork 2 — แพ้ยา (allergy) vs ผลข้างเคียง (side effect) — แยกให้ขาด
| | ผลข้างเคียง | แพ้ยา (hypersensitivity) |
|---|---|---|
| กลไก | ฤทธิ์ยาเองที่ขนาดปกติ | ภูมิคุ้มกันตอบสนอง |
| ใครเป็น | **คาดเดาได้ ทุกคน** | **คาดเดาไม่ได้ บางคน** |
| จัดการ | ปรับวิธีกิน มักไม่หยุดยา | **หยุดยาทันที** + เลี่ยงตัว/กลุ่มเดิมตลอดชีวิต |
- ⚠️ **SJS/TEN (ผิวลอกทั้งตัว, ถึงตาย):** สัญญาณหลังเริ่มยาใหม่ = **ผื่น + ไข้ + เจ็บคอ + ปวดเมื่อย** → **หยุดยาทันที + ถ่ายรูปผื่น + เอายาพร้อมฉลากไปหาหมอ** · ยาเสี่ยง: allopurinol, carbamazepine/phenytoin (กันชัก), ซัลฟา (co-trimoxazole), NSAIDs, ยาวัณโรค, nevirapine
- มีประวัติแพ้ → จำชื่อยา + พกบัตรแพ้ยา + แจ้งทุกครั้ง

### Fork 3 — ยาตีกัน (drug interaction) — ยา-ยา / ยา-อาหาร / ยา-โรค
- หลัก: **ใช้ยาน้อยชนิดที่สุด** (interaction เกิดเมื่อ >1 ตัว)
- **CYP450 enzyme (กลไกที่มองข้ามบ่อย):** inducer (rifampicin/ยากันชัก/บุหรี่) → เร่ง metabolism → ยาตัวอื่นออกฤทธิ์**ลด** · inhibitor (ketoconazole/erythromycin/น้ำเกรปฟรุต) → ยาค้าง → **toxic** · + ยาแย่ง plasma-protein binding (warfarin โดน displace → free สูง)
- **ยา-อาหาร:** ⚠️ tetracycline + นม/ธาตุเหล็ก → ไม่ดูดซึม (กินห่าง 2 ชม.) · พาราเซตามอล + แอลกอฮอล์ → พิษตับ · warfarin + วิตามิน K → ยาไม่ได้ผล
- **ยา-โรค (ห้ามคู่):** โรคกระเพาะ ✗ NSAIDs · **ธาลัสซีเมีย ✗ ยาเสริมธาตุเหล็ก** · โรคตับ ✗ พาราเซตามอลขนาดสูง
- 🩸 ค่าแล็บที่ยาบิด: warfarin→INR · ยาหลายตัว→LFT/renal · → correlate ยาเสมอก่อนสรุปค่าผิดปกติ

### Fork 4 — ใช้ยาให้ถูก + รูปแบบยาที่ห้ามหัก/บด
- "ถูก 6 ถูก": คน/โรค/ทาง/วิธี/ขนาด/เวลา · NSAIDs/แอสไพริน/สเตียรอยด์ = **หลังอาหารทันที** (ระคายกระเพาะ)
- ⚠️ **ห้ามหัก/บด:** Enteric-coated (EC) + ออกฤทธิ์นาน (MR/CR/SR/XR/ER) → หัก/บด = ได้ยาโด๊สสูงทีเดียว อันตราย
- **ลืมกินยา:** กินเมื่อนึกได้; ใกล้มื้อถัดไป → ข้ามไป **ห้ามกิน 2 เท่า** (อันตรายกับยากันชัก/หัวใจ) — **ยกเว้นยาคุมลืมต้องกิน 2 เม็ด**
- **ยาฆ่าเชื้อ → ครบคอร์สแม้หายแล้ว** (หยุดเอง = ดื้อยา)

### Fork 5 — OTC tiers + "มี อย. ≠ ปลอดภัย"
- **ยาสามัญประจำบ้าน** (ร้านชำได้) vs **ยาอันตราย** (ปฏิชีวนะ/NSAIDs/ยาคุม = ร้านยามีเภสัช) vs **ยาควบคุมพิเศษ** (สเตียรอยด์เม็ด/ยาสิว vit-A = แพทย์สั่ง)
- ⚠️ **"มี อย." = ได้รับอนุญาตขายเท่านั้น ≠ มีสรรพคุณ/ปลอดภัยจริง** (อาหารเสริมหลอกขายใช้ช่องนี้)
- **ORS ≠ เกลือแร่นักกีฬา** (สัดส่วนต่างกัน)

### Fork 6 — Pharmacogenomics + AEFI (จุดเชื่อม genomics + เฝ้าระวังวัคซีน)
- **pharmacogenomics:** ตรวจยีน (เช่น HLA) **ทำนายเสี่ยง SJS/TEN ก่อนให้ยา** = สะพาน MT genomics ↔ ยา (companion Dx/precision medicine)
- **clinical trial 4 phase + placebo** = เหตุผลที่ "ยา ≠ อาหารเสริม" (อาหารเสริมไม่มีกลุ่มเปรียบเทียบ)
- ⚠️ **AEFI: "เกิดหลังฉีดวัคซีน ≠ เกิดจากวัคซีน"** — 5 สาเหตุ (ปฏิกิริยาจริง / error การเก็บ-ฉีด / ความกลัว(เป็นลม) / เหตุร่วมบังเอิญ / ไม่ทราบ) → ต้องสอบสวน

### Fork 7 — TDM (therapeutic drug monitoring): จุดที่ยา↔แล็บมาเจอ
- **TDM เมื่อ:** **TI (therapeutic index) แคบ** + มี therapeutic range ชัด + conc↔response ตรง + เดา dose ยาก/เสี่ยงพิษ · ยา TI แคบ: **digoxin, phenytoin, warfarin, theophylline, aminoglycoside, vancomycin, lithium, carbamazepine**
- **จังหวะเจาะ:** ที่ **steady state (~4-5 t½)** หลัง absorption/distribution เสร็จ · **efficacy → เจาะ trough** (ก่อน dose ถัดไป) · **toxicity → เจาะ peak** · ⚠️ **aminoglycoside เจาะทั้ง peak (ฆ่าเชื้อ) + trough (กัน nephro/ototoxic)** — นี่คือกฎของ **conc-dependent** (aminoglycoside)
- ⚠️ **vancomycin ไม่เข้ากฎ peak/trough นี้:** conc-**independent** → guideline ตั้งแต่ปี 2020 เปลี่ยนเป็น **AUC/MIC 400–600** (เลิก trough-only) → อย่าเอา logic peak=efficacy/trough=toxicity ของ aminoglycoside มาใช้กับ vanco
- ⚠️ **digoxin + hypokalemia → พิษแรงขึ้น** → อ่าน K⁺ คู่กับ digoxin level เสมอ · **zero-order kinetics** (phenytoin/ethanol/aspirin สูง): เพิ่ม dose นิด → conc พุ่ง toxic (ไม่เป็นเส้นตรง)

### Fork 8 — ยา anticoagulant ↔ coag test (อย่าสลับ)
- **Heparin → monitor aPTT** (กระตุ้น antithrombin III; antidote = protamine; ออกฤทธิ์ **in vitro ได้** → เป็น tube anticoagulant ได้) · ⚠️ **HIT (heparin-induced thrombocytopenia)**
- **Warfarin → monitor PT/INR** (ยับยั้ง factor II/VII/IX/X + protein C/S; antidote = vit K; **in vivo เท่านั้น**; ผ่านรก ห้ามตั้งครรภ์)
- ⚠️ **DOAC (dabigatran/rivaroxaban/apixaban) ทำ PT/aPTT เพี้ยนแบบไม่สะท้อนระดับยาจริง** → อย่าแปล coag "ปกติ/ผิดปกติ" โดยไม่รู้ว่าได้ DOAC · ไม่ต้อง routine monitor
- 🩸 ก่อนตีความ PT/aPTT **ต้องรู้ว่าคนไข้ได้ anticoagulant อะไร**

---

## กับดัก (Anti-patterns)
- **สับผลข้างเคียงกับแพ้ยา** — แพ้ = หยุดทันที + เลี่ยงตลอดชีวิต; เมินผื่น+ไข้+เจ็บคอ = พลาด SJS/TEN
- **หัก/บด ยา EC หรือ SR/XR** — ได้โด๊สสูงทีเดียว
- **ลืมยาแล้วกิน 2 เท่า** — อันตราย (ยกเว้นยาคุม)
- **กินยาฆ่าเชื้อจนหายแล้วหยุด** — ดื้อยา
- **ไม่ correlate ยาก่อนสรุปค่าแล็บผิดปกติ** — warfarin/ยาหลายตัวบิดค่า
- **ยา TI แคบไม่ TDM / เจาะผิดจังหวะ** (ไม่ steady state, peak↔trough สลับ) — digoxin/phenytoin/aminoglycoside; **digoxin + K⁺ ต่ำ = พิษแรง** (อ่าน K คู่)
- **สลับ heparin↔aPTT กับ warfarin↔PT/INR**; DOAC ทำ PT/aPTT เพี้ยน — อย่าตีว่า "ไม่มียา"
- **"มี อย. = ปลอดภัย/ได้ผล"** — แค่ได้รับอนุญาตขาย
- **"เกิดหลังฉีดวัคซีน = วัคซีนทำ"** — อาจเป็นเหตุร่วมบังเอิญ ต้องสอบสวน
- **ให้ธาตุเหล็กในธาลัสซีเมีย** — ห้ามคู่

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT) เคสที่ค่าแล็บผิดเพราะยา... จับได้เพราะถาม med history"*
> - *"เคสแพ้ยา/SJS ที่เจอ + สัญญาณที่ทำให้ catch ได้ทัน"*

---
*ช่วยคิด/เฝ้าระวังเรื่องยาเพื่อการศึกษา ไม่ใช่คำสั่งใช้ยา/สั่งจ่ายยา — MT ไม่สั่งจ่ายยา การใช้/ปรับ/หยุดยาต้องปรึกษาแพทย์/เภสัชกรเสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: photography-judgment ═════════ -->

---
skill: photography-judgment
title: โค้ชถ่ายภาพ/วิดีโอ + photomicrography (Photography & Lab Documentation Judgment)
type: ADVISE               # ช่วยตัดสินใจการถ่าย ไม่ใช่ตำรากล้อง
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดการถ่ายภาพ/วิดีโอ + ถ่ายงานแล็บ เพื่อการศึกษา · การถ่ายภาพคนไข้/สิ่งส่งตรวจต้องเคารพความลับ/consent ตามกฎหมาย (ดู mt-law-ethics-judgment) · ผู้นำไปใช้รับผิดชอบการนำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชถ่ายภาพ/วิดีโอ + photomicrography

ถ่ายภาพ/วิดีโอให้ "สื่อสารได้" — เลือกตั้งค่า/จัดองค์ประกอบให้ตรงสิ่งที่อยากสื่อ + ถ่ายงานแล็บ (สไลด์/colony/gel) ให้คม-สีตรง ไม่ใช่ท่องสเปคกล้อง (= commodity)

> **กฎ #1: ตั้งโจทย์ก่อนยกกล้อง** — "จะสื่ออะไร?" → ค่อยเลือกชัดตื้น/ลึก + ระยะ + มุม. ปรับ exposure ตัวนึงต้องชดเชยอีกตัว (aperture↔shutter↔ISO).
> **กับดักที่ฆ่าภาพมากสุด: WB ผิดแหล่งแสง → สีเพี้ยนทั้งภาพ** (กับสไลด์แล็บ = อ่าน morphology ผิด) — ปรับ "ขาว" ให้ขาวจริงทุกครั้ง, แล็บถ่าย RAW เผื่อแก้.
>
> 2 ปลายทาง: **content/วิชวล** (thumbnail/clip/พรีเซนต์) + **lab documentation** (photomicrography = หลักฐาน QC, สอน, present เคส, demo) · เลือกหัวข้อคอนเทนต์ดู `content-creator-judgment` · วิเคราะห์ภาพด้วย ML ดู `cv-judgment`

## ใช้เมื่อ
- ตั้งกล้อง/มือถือ แล้วไม่รู้ปรับอะไร (ภาพมืด/ไหว/ฉากหลังรก)
- อยากได้ภาพเล่าเรื่อง/thumbnail เด่น
- ถ่ายสไลด์/colony/gel ใต้กล้องให้คม-สีตรงสำหรับ documentation/portfolio
- วางช็อต/ตัดต่อวิดีโอ

## วิธีใช้
วาง skill นี้ + บอกว่าจะถ่ายอะไร/สื่ออะไร → AI ชี้การตั้งค่า + องค์ประกอบ + กับดัก

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — Exposure triangle: ปรับ 1 ตัว ชดเชยอีกตัว
| ตัว | คุม | trade-off |
|---|---|---|
| **Aperture (F)** | แสง + ระยะชัด | F น้อย=รูกว้าง=แสงเยอะ=**ชัดตื้น** · F มาก=**ชัดลึก** |
| **Shutter** | เวลารับแสง + จับ/เบลอ | ช้า=แสงเยอะ/เบลอ · เร็ว=หยุดนิ่ง · ⚠️ <1/50 มือเปล่า=ไหว |
| **ISO** | ความไวแสง | ต่ำ=เนียน · สูง=ถ่ายที่มืดได้ แต่ **noise** |
- ⚠️ **ISO ต่ำสุดเท่าที่แสงให้** (กัน noise) · ที่มืด: ดัน ISO ยอม noise ดีกว่าภาพไหว (ถ้าไม่มีขาตั้ง)
- โหมด: A/Av (คุม DOF) · S/Tv (คุมการเคลื่อนไหว) · M (manual)

### Fork 2 — DOF เพื่อสื่อความหมาย
- **ชัดตื้น** (F น้อย + เลนส์ tele + ฉากหลังไกล) → เน้น subject ตัดฉากรก → portrait/ดอกไม้/thumbnail · **bokeh** = ฉากหลังเบลอเป็นวง
- **ชัดลึก** (F มาก + เลนส์ wide) → เก็บรายละเอียดหมด → วิว/สถาปัตย์/หมู่
- 🔬 **lab: ชัดลึกพอให้เห็น morphology** ของเซลล์/เชื้อทั้ง field

### Fork 3 — Composition: จัดวางให้ตาไปถูกที่
- **Rule of Thirds:** วางจุดเด่นที่ 4 จุดตัด (ไม่ใช่กลางภาพเป๊ะ) · เส้นขอบฟ้า 3:1 หรือ 1:3 (อย่า 1:1)
- **สีจิตวิทยา:** ร้อน (แดง/ส้ม=เร้า พุ่งออก) vs เย็น (ฟ้า/เขียว=สงบ ถอย) → เลือกวรรณะหลัก + สีตรงข้ามเป็นจุดเน้นเล็ก
- **เล่าเรื่อง = 3 ระยะ** (ใกล้/กลาง/ไกล) + ถ่ายซ้ำมุมเดิม 2-3 ช็อตเลือกดีสุด

### Fork 4 — White Balance + วัดแสง
- **WB:** ปรับ "ขาว" ให้ขาวจริงตามแหล่งแสง (Kelvin: ต่ำ=ฟ้าเย็น, สูง=ส้มร้อน) — ⚠️ ตั้งผิด = สีเพี้ยน
- **วัดแสง:** เฉลี่ยหนักกลาง (ทั่วไป) · **Spot 2-3%** (ย้อนแสง/วัตถุเล็ก/แม่นสุด) · เช็ค **histogram** (เอียงซ้าย=มืด, ขวา=สว่าง → ดันกลาง)

### Fork 5 — Photomicrography / lab documentation (MT)
- **Spot meter เฉพาะ field** · **WB ตรงกับแหล่งแสงกล้อง** (ไม่งั้นสีสไลด์เพี้ยน) · **ขาตั้ง/รีโมท/shutter** ลดสั่น · **RAW** เพื่อแก้สีทีหลัง · ชัดลึกพอเห็น morphology
- กล้องที่ใช้: ธรรมดา/fluorescence/phase-contrast/polarized → ปรับ exposure ตามชนิด
- ⚠️ ถ่ายสไลด์/เคสคนไข้ = **เคารพความลับ/consent** (ดู `mt-law-ethics-judgment`) — de-identify ก่อนเผยแพร่

### Fork 6 — Video grammar (ถ้าทำคลิป)
- **Shot sizes:** ELS→LS→MS→MCU→CU→ECU (ไกล→ใกล้) · **มุม:** high=ดูอ่อนแอ, low=ดูมีพลัง
- **Movement:** Dolly (เลื่อนเข้า-ออก ให้มิติลึกกว่า zoom) · Pan/Tilt
- **Montage:** ช็อต A + B = ความหมาย C (จัดลำดับคุมอารมณ์คนดู) · **Storyboard:** Intro→Suspense→Crisis→Climax→Conclusion
- Tech: ขั้นต่ำ Full HD (1920×1080) · 16:9 · 24/25/30 fps — **4K/60fps ถ้าทำ content จริง** (มาตรฐานทั่วไปแล้ว)

---

## กับดัก (Anti-patterns)
- **ยกกล้องก่อนตั้งโจทย์** — ตั้งก่อนว่าจะสื่ออะไร → ค่อยเลือกชัดลึก/ตื้น/ระยะ/มุม
- **shutter ช้า มือเปล่า** (<1/50) → ภาพไหว — ใช้ขาตั้ง/ดัน ISO/เพิ่มแสง
- **ISO สูงเกินจำเป็น** → noise; ต่ำสุดเท่าที่แสงให้
- **WB ผิดแหล่งแสง** → สีเพี้ยน (สำคัญมากกับสไลด์แล็บ)
- **วางจุดเด่นกลางภาพเป๊ะทุกครั้ง** → ใช้ rule of thirds
- **ถ่ายระยะเดียว** → เล่าเรื่องไม่ครบ; เก็บ 3 ระยะ
- **ถ่ายเคส/คนไข้แล้วเผยแพร่โดยไม่ de-identify/consent** — ผิดความลับ (ดู mt-law-ethics)
- **เก็บกล้องในที่ชื้น** → ราเลนส์ (แก้ไม่ได้); ตู้กันชื้น 40-45%RH

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(content) preset ที่ผมใช้ถ่าย thumbnail/B-roll คือ... เพราะ..."*
> - *"(lab) ตอนถ่ายสไลด์/gel จุดที่สีเพี้ยน/เบลอบ่อย แก้โดย..."*

---
*ช่วยคิดการถ่ายภาพ/วิดีโอ + ถ่ายงานแล็บ เพื่อการศึกษา · การถ่ายภาพคนไข้/สิ่งส่งตรวจต้องเคารพความลับ/consent ตามกฎหมาย (ดู mt-law-ethics-judgment) · ผู้นำไปใช้รับผิดชอบการนำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: polite-but-clear ═════════ -->

---
skill: polite-but-clear
title: พูดให้สุภาพแต่ยังตรง (Polite but Clear)
type: ADVISE               # ช่วยเรียบเรียงถ้อยคำ ไม่ได้รันอะไร
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยปรับถ้อยคำให้สุภาพขึ้น เพื่อการศึกษา ไม่ใช่คำแนะนำทางการ — ควรอ่านทวนก่อนส่งทุกครั้ง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# พูดให้สุภาพแต่ยังตรง

เปลี่ยนข้อความที่ **ห้วน / แรง / ขวางหู** → สุภาพ น่าอ่าน **แต่ยังได้ใจความ** (ไม่ใช่อ้อมจนไม่รู้จะให้ทำอะไร)

> **กฎเดียวที่ต้องจำ:** ทำให้สุภาพได้ แต่ห้ามทำ "ใจความ/สิ่งที่อยากให้ผู้รับทำ" หายไป — เสร็จแล้วผู้รับต้องยัง **รู้ว่าต้องทำอะไร** อยู่.
> **กับดักอันดับ 1:** สุภาพจนอ้อม ไม่มีใครจับได้ว่าจะให้ทำอะไร = แย่กว่าห้วน. สุภาพ ≠ อ้อม. เคสยากสุดคือต้อง "พูดสิ่งไม่ดี" (ปฏิเสธ / ตักเตือน / แย้งหัวหน้า / ตอบคนโกรธ) — ตรงนี้ให้ชัด + เคารพ ไม่ใช่หายไปกับความนุ่ม
> ⛔ **ข้อยกเว้นเด็ดขาด — เรื่องความปลอดภัย/ด่วน/เสี่ยงชีวิต** (ห้ามให้เลือด, หยุดยา, ค่าวิกฤต, อันตราย): **ห้ามลดความแรงของคำสั่ง/คำเตือน** แม้จะดูห้วน. คำสั่งความปลอดภัย ≠ ทางเลือกของผู้รับ — "**ห้าม X**" ห้ามแปลงเป็น "อาจเสี่ยงถ้า X" หรือ "แล้วแต่ท่านพิจารณา". สุภาพได้ที่ **น้ำเสียง** เท่านั้น ไม่ใช่ที่ **ความเด็ดขาดของ action**

## ใช้เมื่อ
- จะส่งข้อความ/อีเมล/LINE แล้วกลัวห้วนหรือแรงไป
- ต้องปฏิเสธ, ตักเตือน, แจ้งปัญหากับผู้ใหญ่/หัวหน้า/แพทย์
- ตอบ complaint หรือสถานการณ์ตึงๆ
- เขียนภาษาราชการ/ทางการ

## วิธีใช้
วาง skill นี้ + วางข้อความที่อยากส่ง → *"ช่วยปรับให้สุภาพแต่ยังได้ใจความ ผู้รับคือ [ใคร/ตำแหน่ง] สถานการณ์คือ [...]"*

---

## วิธีปรับ (AI: ทำตามนี้)

### ขั้น 1 — รักษา "ใจความ" ไว้ก่อน อย่าทำหาย
- จับให้ได้ว่าข้อความนี้ต้องการสื่ออะไร/อยากให้ผู้รับทำอะไรจริงๆ → **ห้ามทำให้ความหมายหายตอนทำให้สุภาพ**
- สุภาพ ≠ อ้อมจนจับใจความไม่ได้

### ขั้น 2 — ดูว่าใครคือผู้รับ แล้วปรับระดับภาษา
- **หัวหน้า/ผู้ใหญ่/แพทย์** → สุภาพสูง ให้เกียรติ ใช้ "ขออนุญาต/เสนอ" ไม่ใช่ "สั่ง"
- **เพื่อนร่วมงาน** → เป็นกันเองแต่เคารพ
- **ผู้ป่วย/ประชาชน** → ชัด เข้าใจง่าย อบอุ่น
- **ราชการ/ทางการ** → รูปแบบทางการ ตรงประเด็น

### ขั้น 3 — เทคนิคทำให้นุ่มโดยไม่เสียใจความ
- ใช้ **คำขอ/คำเสนอ แทนคำสั่ง** ("รบกวน...", "อยากขอ...", "พอจะ...ได้ไหม" แทน "ทำ...")
- เริ่มด้วย **รับรู้/ขอบคุณ** ก่อนเข้าเรื่องยาก
- **พูดจากมุมเรา (I-message)** ไม่ชี้นิ้ว ("ผมกังวลว่า..." แทน "คุณทำผิด")
- ปฏิเสธ = **ขอบคุณ + เหตุผลสั้น + ทางเลือก/ทางออก**

### ขั้น 4 — เคสยาก (พูดสิ่งไม่ดี)
- **ตักเตือน:** ชี้ที่ **พฤติกรรม ไม่ใช่ตัวคน** + เสนอทางแก้ (ไม่ใช่แค่ตำหนิ)
- **แย้งหัวหน้า:** เห็นด้วยส่วนที่เห็นด้วยก่อน + เสนอเป็น "อีกมุม" ("อาจมีอีกมุมที่...") ไม่ใช่ "ผิดแล้ว"
- **ปฏิเสธ:** ชัดเจน + เคารพ **ไม่ต้องขอโทษเกินจำเป็น**
- **ตอบคนโกรธ:** รับรู้อารมณ์เขาก่อน + ไม่สวนกลับ + โฟกัสทางแก้

### ขั้น 5 — เช็คก่อนส่ง (สำคัญ)
อ่านในมุมผู้รับ 2 คำถาม:
1. รู้สึก **ถูกเคารพ** ไหม?
2. ยัง **เข้าใจสิ่งที่เราต้องการ** ไหม? — ถ้าข้อ 2 หาย = สุภาพเกินไป ต้องเติมใจความกลับ

---

## กับดัก (Anti-patterns)
- **สุภาพจนจับใจความไม่ได้** — อ้อมจนผู้รับไม่รู้ว่าจะให้ทำอะไร
- **ขอโทษพร่ำเพรื่อ** จนดูไม่มั่นใจ/ไม่มีจุดยืน
- **"สุภาพ" แบบประชด/แดกดัน** — แย่กว่าพูดตรงๆ
- **ได้ความสุภาพ แต่ใจความเพี้ยน** — รักษาเนื้อหาให้ตรงเสมอ

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริงในสายงานคุณ เช่น:
> - *"(MT) แจ้งแพทย์เรื่องผลผิดปกติ/ขอ reject sample ยังไงให้สุภาพแต่ชัด..."*
> - *"ประโยคที่ใช้แล้วได้ผลตอนต้องแย้งหัวหน้า คือ..."*

---
*ช่วยปรับถ้อยคำให้สุภาพขึ้น เพื่อการศึกษา ไม่ใช่คำแนะนำทางการ — ควรอ่านทวนก่อนส่งทุกครั้ง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: progress-tracker ═════════ -->

---
skill: progress-tracker
title: ติดตามความคืบหน้าแบบเห็นภาพ — วางคู่สกิลไหนก็ได้ (Visual Progress Tracker)
type: CALIBRATION          # เปลี่ยนวิธีที่ AI "แสดงงาน" วางคู่กับสกิลอื่น
needs: any                 # ใช้ได้ทุก AI · richer ถ้า AI render Mermaid/artifact ได้
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยให้ AI แสดงความคืบหน้าเป็นภาพ เพื่อการศึกษา/ติดตามงาน — visual บอก 'ทำอะไรไป' แต่ไม่รับประกันว่าเนื้อหาถูก ตรวจผลจริงเสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ติดตามความคืบหน้าแบบเห็นภาพ — วางคู่สกิลไหนก็ได้

วางคู่กับสกิลอื่น → AI จะโชว์ **"ทำอะไรไปแล้ว · อยู่ขั้นไหน · เลือกกิ่งไหน"** เป็นภาพทุก turn ไม่ใช่กำแพงตัวหนังสือ

> **กฎ #1: ติ๊ก ✅ เฉพาะขั้นที่ทำจริงและเห็นผลจริงแล้วเท่านั้น** — progress panel สะท้อน "ของที่ verify แล้ว" ไม่ใช่ "ที่ตั้งใจจะทำ/พิมพ์ว่าทำ". **กับดักใหญ่สุด = โชว์ progress สวยแต่ไม่ได้ทำงานจริง (ละคร)**, และกับดักที่เนียนกว่า = ติ๊ก ✅ ทั้งที่แค่ *สั่ง/ลองทำ* แต่ยังไม่เห็นผลลัพธ์ (เช่น เขียนว่า "รัน test เสร็จ" ทั้งที่ยังไม่เห็น output). ยังไม่เห็นผล = ▶️ ไม่ใช่ ✅. คนอยากเห็น **"ตอนนี้ถึงไหนจริงๆ"** มากกว่า reasoning ยาวๆ — AI **emit แผงนี้เอง**ทุก turn (checklist ได้ทุก AI · สวยขึ้นถ้าวาด Mermaid/artifact ได้)

## ใช้เมื่อ
- วางคู่สกิลที่มีหลายขั้น/แตกกิ่ง (bloodbank, choose-stat-test, data-project-survival, r2r flow ฯลฯ) แล้วอยากเห็น progress
- งานยาวหลาย step อยากรู้ว่า AI ทำถึงไหน + เหลืออะไร

## วิธีใช้
วาง skill นี้ **พร้อมกับ** สกิลหลักที่จะใช้ → บอกงาน → AI จะแสดง "แผงความคืบหน้า" ทุก turn

---

## วิธีทำ (AI: ทำตามนี้)
ทุก turn ที่ทำงานตามสกิลหลัก แสดง **แผงความคืบหน้า** (ก่อนหรือหลังเนื้อหาหลัก):

### 1. Checklist สด (ทำได้ทุก AI — default ขั้นต่ำ)
- list ขั้นของงาน + สถานะ: **✅ เสร็จ · ▶️ กำลังทำ · ⬜ ยังไม่ถึง · ⏭️ ข้าม (ไม่เกี่ยว + บอกเหตุผล)**
- บอกชัด **"ตอนนี้อยู่ขั้น X / Y"** + **decision/กิ่งที่เลือกไปแล้ว** (เช่น "เลือกทาง two-sample Welch เพราะ 2 กลุ่มอิสระ")
- ตัวอย่าง:
  ```
  📊 ความคืบหน้า (3/5)
  ✅ ถาม 3 คำถาม → เปรียบเทียบค่าเฉลี่ย, 2 กลุ่ม, อิสระ
  ✅ เช็คเงื่อนไข normality
  ▶️ เลือก test: two-sample Welch
  ⬜ บอก assumption ที่ต้องตรวจ
  ⬜ เตือนกับดักที่เกี่ยว
  ```

### 2. ถ้า AI render Mermaid ได้ (เช่น Claude) → วาด flowchart + ไฮไลต์เส้นทาง
- วาด decision tree ของสกิลหลัก แล้ว **ไฮไลต์ node ที่เดินผ่าน/เลือก** (เช่น ใส่ style สีเข้ม) → เห็น "เดินมาทางไหน" ทันที
- ถ้า AI วาดไม่ได้ (โชว์เป็น code) → **ข้าม ใช้ checklist พอ** (อย่าดันให้รก)

### 3. ถ้า AI ทำ artifact/canvas ได้ → mini-dashboard ที่อัปเดตได้
- แผงเดียวอัปเดตทุก turn (ขั้น/กิ่ง/ผลลัพธ์ย่อย) แทนพิมพ์ใหม่ทุกครั้ง

### 4. สรุปท้ายงาน
- checklist เต็ม (ทุกขั้น) + ผลลัพธ์ + **ขั้นที่ข้ามและเหตุผล** + "ขั้นต่อไปถ้าจะทำต่อ"

> หลัก: โชว์ **"ทำอะไรไป + อยู่ไหน + จะไปไหนต่อ"** ไม่ใช่เท reasoning ดิบยาวๆ

---

## กับดัก (Anti-patterns)
- **โชว์ progress สวยแต่ไม่ได้ทำงานจริง** (ละคร) → ต้อง track งานที่ทำจริง ติ๊ก ✅ เฉพาะที่เสร็จจริง
- **ติ๊ก ✅ ขั้นที่แค่สั่ง/ลองทำ แต่ยังไม่เห็นผลลัพธ์** (กับดักเนียน) → "เริ่มทำ" หรือ "สั่งให้ทำ" ≠ "เสร็จ". ยังไม่เห็น output/ยืนยันผล = ▶️ เสมอ; เลื่อนเป็น ✅ ก็ต่อเมื่อเห็นผลจริงแล้ว
- **checklist ไม่อัปเดต** → ต้องอัปทุก turn ไม่งั้นไร้ประโยชน์
- **ยัด visual จนรกกว่าเดิม** → สั้น กระชับ พอเห็นภาพ (5-7 ขั้นกำลังดี อย่าซอย 30 ขั้น)
- **ดันวาด Mermaid ทั้งที่ AI render ไม่ได้** → กลายเป็น code block เฝือ → fallback checklist
- **track แต่ลืมเนื้องาน** → progress panel = เสริม ไม่ใช่แทนคำตอบจริง

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมรูปแบบ tracker ที่ใช้ได้ผลในสายงานคุณ เช่น:
> - *"(MT) ตอนไล่ ABO discrepancy ผมอยากเห็น checklist แบบ... เพราะ..."*
> - *"งานหลาย step ที่ tracker ช่วยจริง คือ..."*

---
*ช่วยให้ AI แสดงความคืบหน้าเป็นภาพ เพื่อการศึกษา/ติดตามงาน — visual บอก "ทำอะไรไป" แต่ไม่รับประกันว่าเนื้อหาถูก ตรวจผลจริงเสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: python-coach ═════════ -->

---
skill: python-coach
title: โค้ช Python — เลือกถูก + ไม่ตกหลุม (Python Judgment & Gotchas)
type: ADVISE               # ช่วยตัดสินใจ/ดีบัก ไม่ใช่ตำรา syntax
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิด+จับกับดัก Python ระดับเริ่ม→กลาง เพื่อการศึกษา — ไม่ใช่ตำรา syntax หรือคำสั่งทางการ ควรทดสอบโค้ดจริงและตรวจผลก่อนนำไปใช้ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช Python — เลือกถูก + ไม่ตกหลุม

เขียน/ดีบัก Python แล้วงงว่า "ใช้อะไรดี" หรือ "ทำไมพัง" → โค้ชนี้ช่วย **เลือกเครื่องมือให้ถูก + โทษบั๊กให้ถูกจุด**

> **กฎข้อ 1 (จำให้ขึ้นใจ): method ที่แก้ของ in-place คืน `None` ไม่ใช่ค่าที่แก้แล้ว.** `.sort()`/`.reverse()`/`.append()`/`.update()`/`.extend()` → คืน `None` ทั้งหมด. ดังนั้น **ห้ามเอาผลของมันไป assign หรือ chain ต่อ** — `x = lst.sort()` ทำให้ `x` เป็น None เงียบๆ, `lst.append(y).append(z)` พังทันที. อยากได้ค่าที่แก้แล้ว: เรียก method (มันแก้ตัวแปรเดิมให้) **แล้วใช้ตัวแปรเดิม** หรือใช้ฟังก์ชันที่ "คืนค่าใหม่" เช่น `sorted(lst)`, `reversed(lst)`, `lst + [y]`.
> **ตัวแยกง่ายๆ:** ชื่อเป็นกริยาแก้ของ (sort/append/update/reverse) → in-place คืน None · ชื่อบอกผลลัพธ์ (sorted/reversed) → คืนค่าใหม่ เอาไป assign ได้.
>
> Google/AI มี syntax ให้หมดแล้ว — ส่วนที่ทำให้พลาดจริงคือ (1) เลือก data structure/วิธีผิด (2) ตกกับดักที่ "ดูถูกแต่พัง" (in-place คืน None, loop variable ค้าง, mutable default). skill นี้เก็บสองอันนั้น ไม่ใช่ตำรา

## ใช้เมื่อ
- เขียน/ดีบัก Python (เรียน, coursework, งาน data)
- ลังเล "ใช้ list หรือ dict ดี", "loop หรือ comprehension"
- code พัง/ผลเพี้ยน หาไม่เจอว่าผิดตรงไหน

## วิธีใช้
วาง skill นี้ + วางโค้ด/พิมพ์ปัญหา → AI ชี้ตัวเลือกที่เหมาะ + จุดที่เสี่ยงตกหลุม

---

## เลือกอะไรเมื่อไหร่ (Judgment)
- **data structure:** เรียงลำดับ+ซ้ำได้ → **list** · lookup ด้วย key O(1) → **dict** · unique + เช็คสมาชิก O(1) → **set** · ค่าคงที่/immutable/เป็น key → **tuple** · (เก็บคำไม่ซ้ำ → `set` เร็วกว่า `if x not in list` ซึ่งเป็น O(n²))
- **loop vs comprehension:** แปลง/กรองง่ายๆ → comprehension · มี side-effect/ซับซ้อน/หลายขั้น → for loop (อ่านง่ายกว่า)
- **string ต่อกันใน loop:** ใช้ `"".join(parts)` ไม่ใช่ `s += x` (O(n²))
- **อ่านไฟล์:** `for line in fh:` (streaming, ไฟล์ใหญ่) vs `.readlines()` (โหลดทั้งหมดเข้า RAM)
- **pure python vs pandas (DS):** ตาราง/คำนวณทั้งคอลัมน์ → pandas (vectorize) · ข้อมูลเล็ก/stream/logic ซับซ้อน → python · **อย่า loop ทีละ row ใน DataFrame** (ใช้ vectorized op)
- **เทียบค่า:** `==` (ค่าเท่า) · `is` (วัตถุตัวเดียวกัน) → ใช้ `is` เฉพาะกับ `None`

## กับดัก (Anti-patterns) — เช็คก่อนโทษที่อื่น
- **method แก้ของ in-place คืน `None`** — ทั้งตระกูล `.sort()` `.reverse()` `.append()` `.extend()` `.update()` `.add()` → `x = lst.sort()` ได้ None เงียบๆ, chain `lst.append(a).sort()` พัง (`'NoneType' has no attribute`). อยากได้ค่า: ใช้ตัวแปรเดิมหลังเรียก หรือใช้ `sorted()`/`reversed()`/`lst+[a]` ที่คืนค่าใหม่ *(กับดักอันดับ 1 ของมือใหม่)*
- **loop variable ค้างหลัง loop:** จบ `for line in fh:` แล้ว `line` = บรรทัดสุดท้าย → `print(line)` พิมพ์ตัวสุดท้ายไม่ใช่ผลรวม *(บั๊กคลาสสิกตอนวนอ่านไฟล์แล้วนับคำ)*
- **mutable default arg:** `def f(x=[])` → list แชร์ข้าม call ทุกครั้ง → ใช้ `x=None` แล้ว `if x is None: x=[]`
- **copy vs reference:** `b = a` (list/dict) = ชี้ก้อนเดียวกัน แก้ b กระทบ a → `b = a.copy()` / `list(a)`
- **แก้ list ขณะวนมัน** → ข้าม/พัง → วน copy หรือสร้าง list ใหม่
- **`input()` คืน str เสมอ** → ต้อง `int()`/`float()` ก่อนคำนวณ
- **`/` คือ float division, `//` คือ integer** · float ไม่แม่น (`0.1+0.2≠0.3`) → เทียบด้วย `math.isclose`
- **`split()` ไม่มี arg** = ตัดทุก whitespace + ทิ้งช่องว่าง · `split(' ')` = ได้ string ว่างถ้าเว้นซ้อน
- **`.get(k)` vs `d[k]`** — `d[k]` KeyError ถ้าไม่มี key; ใช้ `.get(k, default)` กันพัง
- **tab ปน space** → IndentationError (ตั้ง editor เป็น space 4)
- **`NaN` ใน pandas** = เงียบๆ ทำผลเพี้ยน → `.isna().sum()` เช็คก่อน · chained assignment warning → ใช้ `.loc`

## ดีบักให้ถูกจุด
- อ่าน traceback **จากล่างขึ้นบน** (บรรทัดล่างสุด = error จริง) · บั๊กมักอยู่จุดที่ "มั่นใจว่าถูก" ไม่ใช่จุดที่ error โผล่
- reproduce ให้ได้ก่อน → `print`/`breakpoint()` ค่าตัวแปรตรงจุดสงสัย → แก้ทีละอย่าง

## สะพานสู่ Data Science
`pd.read_csv` · vectorize อย่า loop row · `.loc[row, col]`/`.iloc` · `df.groupby().agg()` · merge = SQL join · จัดการ NaN ก่อนคำนวณ

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมกับดัก Python ที่เคยกัดในงานจริงสายคุณ เช่น:
> - *"ตอนทำงาน data lab ผมเคยพลาดเพราะ... (เช่น NaN/float/encoding) แก้โดย..."*
> - *"โครงสร้างข้อมูลที่ผมเลือกผิดบ่อย คือ... ที่ถูกควรใช้..."*

---
*ช่วยคิด+จับกับดัก Python ระดับเริ่ม→กลาง เพื่อการศึกษา — ไม่ใช่ตำรา syntax หรือคำสั่งทางการ ควรทดสอบโค้ดจริงและตรวจผลก่อนนำไปใช้ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: r2r-research-proposal ═════════ -->

---
skill: r2r-research-proposal
title: ผู้ช่วยปั้นโจทย์วิจัย R2R (R2R Proposal Builder)
type: ADVISE               # ช่วยคิด/โค้ช ไม่ได้รันอะไร
needs: any                 # ใช้ได้ทุก AI — แต่หา gap จะดีขึ้นมากถ้าใช้ AI ที่ค้นเปเปอร์ได้ (ChatGPT search / Gemini / PubMed)
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "เป็นผู้ช่วยร่างข้อเสนอเพื่อการศึกษา/ช่วยคิด ไม่ใช่ที่ปรึกษาวิจัย/EC ทางการ — methodology และจริยธรรม ต้องผ่านอาจารย์ที่ปรึกษา + คณะกรรมการจริยธรรม (EC) จริงเสมอ ก่อนเก็บข้อมูลหรือตีพิมพ์ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ผู้ช่วยปั้นโจทย์วิจัย R2R

สำหรับ MT รพช. ที่ **คิดโจทย์ R2R ไม่ออก / กลัวซ้ำคนอื่น / กลัวโดนอาจารย์แก้ยับ** — ช่วยปั้นตั้งแต่ "ปัญหาหน้างาน" จนเป็นข้อเสนอที่ตั้งเรื่องได้

> **กฎข้อ 1:** R2R ไม่ใช่การค้นพบระดับโนเบล — มันคือ **"แก้ปัญหาหน้างานในแลปเรา แล้ววัดผลให้เป็นระบบ"** อย่าฝืนทำให้เป็นนวัตกรรม; เจอว่าซ้ำ **ห้ามทิ้งโจทย์** ต่อยอดจาก limitation/บริบทเราได้เสมอ
> **กับดักร้ายแรงสุด:** **ลืมขอ EC ก่อนเก็บข้อมูล = งานเสียทั้งงาน** (เก็บไปก่อนแล้วค่อยขอ → ตีพิมพ์ไม่ได้) — วาง EC ไว้ใน timeline ตั้งแต่วันแรก
> skill นี้พาคิดทีละขั้น: ปัญหา → คำถาม → หา gap → จับ objective ให้ตรง method → กัน EC ดอง

## ใช้เมื่อ
มีปัญหา/ความหงุดหงิดในงาน routine แต่ยังไม่รู้จะทำเป็นวิจัยยังไง หรือคิดหัวข้อได้แล้วแต่กลัวซ้ำ/กลัว methodology ไม่แน่น

## วิธีใช้
1. เปิด AI (ChatGPT/Claude/Gemini) — ถ้าใช้ตัวที่ **ค้นเว็บ/เปเปอร์ได้** (ChatGPT search, Gemini) จะช่วยขั้น "หา gap" ได้ดีกว่ามาก
2. วาง skill นี้ + พิมพ์: *"ใช้ skill นี้ช่วยปั้นโจทย์ R2R ปัญหาที่เจอในแลปคือ: [เล่าปัญหา]"*
3. ตอบคำถามที่ AI ถามไปทีละข้อ — **คุณคือคนที่รู้ปัญหาหน้างาน AI แค่ช่วยจัดให้เป็นระบบ**

> ⚠️ ขั้นตอนหา gap: AI ช่วย **คิดคำค้น + ชี้ทาง** ได้ แต่ **คุณต้องไปเปิด review/เปเปอร์จริงเอง** — อย่าเชื่อว่า "ไม่มีใครทำ" เพราะ AI บอกลอยๆ

---

## วิธีโค้ช (AI: ทำตามลำดับนี้ ทีละขั้น อย่ารวบ)

### ขั้น 1 — เปลี่ยนปัญหาหน้างาน → คำถามวิจัย
- ถาม MT: *งาน routine ไหนที่ช้า/พลาดบ่อย/สิ้นเปลือง/ไม่มั่นใจผล?* (เช่น TAT นาน, reject เยอะ, 2 เครื่องผลไม่ตรง, QC หลุดบ่อย)
- ช่วยแปลงเป็นคำถามที่ **วัดได้**: ใคร/อะไร/เทียบกับอะไร/วัดด้วยตัวเลขอะไร
- ย้ำ: **R2R = แก้ปัญหาแล้ววัดผล ไม่ต้องค้นพบสิ่งใหม่ของโลก**

### ขั้น 2 — หา gap + เช็คซ้ำ (จุดที่ MT กลัวที่สุด)
- ช่วยคิด **คำค้น** (ไทย+อังกฤษ, ใส่ MeSH/synonym) แล้วสั่งให้ MT ไปหา review/เปเปอร์
- **ถ้าเจอว่าซ้ำ → ห้ามทิ้งโจทย์!** ต่อยอดได้ 3 ทาง:
  1. ทำในบริบทตัวเอง — **รพช./เครื่องที่เรามี/ประชากรต่าง** (ความต่างเชิงบริบท = contribution ของ R2R)
  2. หยิบ **"limitation / ข้อเสนอแนะเพื่อการวิจัยต่อไป"** ของงานเดิมมาทำต่อ
  3. เปลี่ยนมุม — ตัวแปร/ช่วงเวลา/วิธีวัดที่งานเดิมไม่ได้ทำ
- อธิบาย MT ว่า "ทำในบริบทเราเอง" **ไม่ใช่การลอก** — เป็นการ replicate/extend ที่ยอมรับได้

### ขั้น 3 — จับ objective ↔ methodology ให้ตรงกัน
- ให้ MT เขียน objective เป็นข้อๆ → **ทุกข้อ ต้องมี method ที่ตอบได้** (ถ้า objective ไหนไม่มี method = ตัดทิ้งหรือเพิ่ม method)
- รัน **checklist นี้** แล้วบอกผลตรงๆ:
  - [ ] research question **คม** (เจาะจง วัดได้ ไม่กว้างลอย)?
  - [ ] research gap **ชัด** (บอกได้ว่า "ที่ผ่านมาขาดอะไร เราเติมอะไร")?
  - [ ] method **ตอบ objective ครบทุกข้อ**?
  - [ ] design พอดีกับทรัพยากร รพช. (คน/เครื่อง/เวลา/งบ) ไม่เกินตัว?
- นี่คือด่านที่ผู้ทรงคุณวุฒิ/อาจารย์ชอบแก้ยับ — ทำให้แน่นตั้งแต่ตอนนี้

### ขั้น 4 — reframe ความคาดหวังให้พอดี
- เตือน MT: **R2R / CQI / case report เพียงพอ** สำหรับขอชำนาญการในหลายบริบท — ไม่ต้องเป็นองค์ความรู้ใหม่ระดับโลก
- ช่วยเลือก design **ให้พอดีทรัพยากร**: descriptive / before-after / cross-sectional / method comparison มักพอ อย่าฝืนทำ RCT ถ้าทำไม่ไหว
- ถ้า MT (หรือต้นสังกัด) คาดหวัง "ต้องเป็นนวัตกรรม" → ช่วยปรับความคาดหวังให้ตรงกับสิ่งที่ R2R ควรเป็น

### ขั้น 5 — เตือน Ethics (EC) ตั้งแต่ต้น (อย่ารอจนจบ!)
- ถาม: *ใช้ข้อมูล/ตัวอย่างผู้ป่วยไหม?* — **ถ้าใช่ (แม้แค่ leftover specimen / เวชระเบียน) ต้องขอ EC**
- เตือน timeline จริง: EC + อาจต้องผ่าน **สสจ. ใช้เวลา ~2–8 สัปดาห์** (บางที่ดองนานกว่า)
- **ต้องได้อนุมัติ "ก่อน" เก็บข้อมูล** — เก็บไปก่อนแล้วลืมขอ = **ตีพิมพ์ไม่ได้** (วารสารถามหา EC number)
- สั่งให้ MT วาง EC ไว้ใน timeline ตั้งแต่วันแรก ไม่ใช่ค่อยคิดตอนจะเขียนตีพิมพ์

---

## กับดัก (Anti-patterns)
- **โจทย์กว้างเกิน** ("คุณภาพแลป") — ตั้งเรื่องไม่ได้ ต้องเจาะให้แคบ-วัดได้
- **เจอว่าซ้ำแล้วทิ้งทันที** — เสียโจทย์ดีไปเปล่าๆ ต่อยอดจาก limitation/บริบทได้เสมอ
- **objective กับ method ไม่ตรงกัน** — เขียน objective สวยแต่ไม่มี method ตอบ = โดนแก้ยับแน่
- **คาดหวังว่าต้องเป็นนวัตกรรม** — ขัดขาตัวเอง ทำไม่จบ R2R ควรพอดีบริบท
- **ลืม EC / ขอทีหลัง** — กับดักร้ายแรงที่สุด เก็บข้อมูลก่อนขอ = งานเสียทั้งงาน
- **เชื่อ AI ว่า "ไม่มีใครทำ"** — AI หลอนได้ ต้องไปเช็คเปเปอร์จริงเอง

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติม war-story/วิจารณญาณจริงจากคนที่เคยผ่านมา เช่น:
> - *"โจทย์แบบนี้ผู้ทรงตีกลับเพราะ... ผมแก้โดย..."*
> - *"EC ที่ รพ./สสจ. เรา จริงๆ ใช้เวลา... เตรียมเอกสาร... ต้องระวัง..."*
> - *"งานซ้ำแบบนี้ ผมเคยต่อยอดด้วยมุม... แล้วผ่านฉลุย"*
> - *"design ที่ดูดีในตำราแต่ทำจริงใน รพช. ไม่ได้เพราะ..."*

*(— ส่วนนี้แหละที่ทำให้ skill เป็น "มรดก" ไม่ใช่แค่ตำรา)*

---

*เป็นผู้ช่วยร่างข้อเสนอเพื่อการศึกษา/ช่วยคิด ไม่ใช่ที่ปรึกษาวิจัย/EC ทางการ — methodology และจริยธรรม ต้องผ่านอาจารย์ที่ปรึกษา + คณะกรรมการจริยธรรม (EC) จริงเสมอ ก่อนเก็บข้อมูลหรือตีพิมพ์ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: r2r-stats ═════════ -->

---
skill: r2r-stats
title: ผู้ช่วยสถิติงานวิจัย MT (R2R Stats Buddy)
type: DO                    # ต้องรันคำนวณจริง
needs: code-interpreter     # AI ที่รัน Python ได้จริง — ChatGPT Plus / Claude Pro / Gemini Advanced
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "เครื่องมือช่วยเลือก/รัน/แปลผลสถิติเพื่อการศึกษา — ไม่ใช่ที่ปรึกษาสถิติทางการ ควรตรวจสอบความเหมาะสมและการแปลผลกับนักสถิติ/ผู้เชี่ยวชาญก่อนนำไปใช้/ตีพิมพ์/ตัดสินทางคลินิก · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ผู้ช่วยสถิติงานวิจัย MT (R2R Stats Buddy)

สำหรับ MT ที่ทำ R2R/งานวิจัยแล้ว **ติดสถิติ** — ไม่รู้ใช้ test ไหน รันยังไง แปลผลยังไง ตอบ reviewer ยังไง

> ⚠️ **กฎเหล็ก #1: เลือก test ก่อนดู p-value เสมอ — ห้ามเปลี่ยน test ทีหลังเพราะ p ไม่ผ่าน (= p-hacking) และอย่าเชื่อตัวเลขที่ AI ไม่ได้รันโค้ดโชว์**
> ⚠️ **กับดักที่ #1: ข้อมูลจับคู่ (ก่อน-หลังคนเดียวกัน / 2 วิธีวัด sample เดียวกัน) ต้องใช้ paired test (paired t / Wilcoxon signed-rank / McNemar) — ตัวเลขเป็น "2 คอลัมน์" เหมือนกันหมด ดูจาก design ไม่ใช่จากหน้าตาข้อมูล ใช้ unpaired ทั้งที่ข้อมูล paired = ผิดบ่อยสุดและทำให้ผลเพี้ยน**

## ใช้เมื่อ
มีข้อมูล (Excel/CSV) + คำถามวิจัย แต่ไม่มั่นใจเรื่องสถิติ

## วิธีใช้ (ไม่ต้องเขียนโค้ดเอง แต่ต้องใช้ AI ที่รันโค้ดเป็น)
1. เปิด AI ที่ **"รัน Python ได้จริง"** — ChatGPT Plus (กดคลิป 📎 อัปไฟล์), Claude Pro, หรือ Gemini Advanced
2. อัปโหลด **ไฟล์นี้ + ไฟล์ข้อมูล**
3. พิมพ์: *"ใช้ skill นี้ช่วยวิเคราะห์ คำถามวิจัยคือ: [เขียนคำถาม]"*

> ⚠️ **ถ้า AI ตอบตัวเลขโดยไม่โชว์ว่ารันโค้ด = อย่าเชื่อ** — สั่งให้รันโค้ดจริงแล้วโชว์โค้ด+ผลลัพธ์

---

## วิธีเลือก test (decision guide)

> 💡 อยากได้ decision-tree เลือก test แบบละเอียด → ใช้ `choose-stat-test` ก่อน · ที่นี่ย่อพอใช้ + เน้น **รัน/แปลผล**

**ก่อนเลือก: ดูก่อนว่าตัวแปรหลักเป็นแบบไหน** — ต่อเนื่อง (เช่น ค่า Hb, TAT นาที) หรือ หมวดหมู่ (เช่น ผ่าน/ไม่ผ่าน, หมู่เลือด)

> (ถ้าไม่รู้จัก test พวกนี้ ไม่เป็นไร — แค่อัปโหลด + บอกคำถามวิจัย แล้ว AI เลือกให้)

| คำถาม | ข้อมูลต่อเนื่อง | ข้อมูลหมวดหมู่ |
|---|---|---|
| เทียบ **2 กลุ่มอิสระ** (เช่น เครื่อง A vs B) | t-test (ถ้า normal; ใช้ **Welch's t-test** ถ้า variance ไม่เท่ากัน) / **Mann-Whitney U** (ถ้าไม่ normal) | Chi-square; ใช้ **Fisher's exact** เมื่อ **มี expected cell < 1 หรือ > 20% ของ cell มี expected < 5** (ตาราง 2×2 เกณฑ์ "expected < 5" พอใช้ได้ แต่ตารางใหญ่ cell เดียว < 5 ไม่บังคับ Fisher) |
| เทียบ **ก่อน-หลัง / จับคู่** (paired) | paired t-test / **Wilcoxon signed-rank** | McNemar |
| เทียบ **≥3 กลุ่ม** | One-way ANOVA + post-hoc / **Kruskal-Wallis** | Chi-square + **pairwise + multiple-testing correction** (Bonferroni/FDR); Fisher's exact ถ้า expected น้อย |
| **ความสัมพันธ์** 2 ตัวแปรต่อเนื่อง | Pearson (normal) / **Spearman** (ไม่ normal) | — |
| **ทำนาย / คุม confounder** | Linear/Logistic regression | — |
| **2 วิธีวัดตรงกันมั้ย** (method comparison — MT เจอบ่อย!) | **Bland-Altman + ICC** (agreement ต่อเนื่อง) + Passing-Bablok / Deming regression | **Cohen's kappa** (categorical); ใช้ **weighted kappa สำหรับ ordinal** (unweighted ประเมิน ordinal ต่ำเกินจริง) |

> **เลือก parametric vs non-parametric ตัดสินจาก Q-Q plot + ชนิดข้อมูล ไม่ใช่แค่ n < 30** — ถ้าข้อมูลเบ้/ไม่ normal → เอนไปทาง **non-parametric** (Mann-Whitney/Wilcoxon/Spearman/Kruskal-Wallis); แต่ที่ n เล็ก non-parametric ก็ **underpowered** เหมือนกัน อย่าคิดว่าปลอดภัยเสมอ

---

## คำสั่งให้ AI ทำ (AI: ทำตามลำดับนี้)
1. **สำรวจข้อมูล** — ชนิดตัวแปร, n แต่ละกลุ่ม, missing, outlier
2. **เช็ค assumption** — normality (Shapiro-Wilk + histogram/Q-Q), equal variance (Levene) → บอกผล; **ถ้า variance ไม่เท่ากัน ใช้ Welch's t-test อย่า default เป็น Student's t**
3. **เลือก test ตาม guide ข้างบน + บอกเหตุผลที่เลือก** (เป็นภาษาคน) — **เลือก test ก่อนดู p-value เสมอ ห้ามเปลี่ยน test ทีหลังเพราะ p ไม่ผ่าน (= p-hacking)**
4. **รัน** แล้วรายงาน: test ที่ใช้, test statistic, **p-value**, **effect size** (Cohen's d สำหรับ parametric / rank-biserial หรือ r = Z/√N สำหรับ non-parametric / OR สำหรับ logistic), 95% CI
5. **ทำกราฟที่เหมาะ** (box plot/scatter/Bland-Altman) ใส่ label+หน่วยครบ
6. **เขียนผลแบบ paper-ready** 1 ย่อหน้า (รูปแบบ "X กลุ่ม A (mean±SD) เทียบ B ... ; test, p = ...")
7. **เตือน assumption ที่ละเมิด + ข้อจำกัด**
8. **รายงานทุก test ที่รัน ไม่ใช่เฉพาะที่ significant** — บอกจำนวน comparison ทั้งหมด + การ correct
9. **(บังคับ) พิมพ์ท้ายผลทุกครั้ง:** *"⚠️ ผลนี้เป็น decision-support — ตรวจ assumption + ความเหมาะสมกับนักสถิติ/ผู้เชี่ยวชาญ ก่อนตีพิมพ์หรือใช้ตัดสินทางคลินิก"*

---

## กับดัก (Anti-patterns)
- **p < 0.05 ≠ สำคัญทางคลินิก** → ดู effect size + ช่วงค่าจริงเสมอ
- **p-hacking** → เลือก test ก่อนดู p; ห้ามเปลี่ยน test เพราะ p ไม่ผ่าน; รายงานทุก test ที่รัน ไม่ใช่เฉพาะที่ significant
- **multiple testing** (เทียบหลายคู่/หลายตัวแปร) → ต้อง correct (Bonferroni/FDR) ไม่งั้น false positive
- **n น้อย** → อย่าเชื่อ normality test, ใช้ non-parametric, ระวัง underpowered
- **correlation ≠ causation**
- **% / สัดส่วน ที่ n ฐานต่าง** → อย่าเทียบตรงๆ
- **paired vs unpaired ตัดสินจาก design ไม่ใช่หน้าตาข้อมูล** — ถ้าแต่ละแถวคือ "หน่วยเดียวกันวัด 2 ที" (ก่อน-หลัง / 2 วิธีวัด sample เดียว / ตา 2 ข้างคนเดียว) = paired (paired t / Wilcoxon signed-rank / McNemar); ใช้ unpaired ทั้งที่ข้อมูล paired = ผิดบ่อยสุด
- **method comparison ≠ การ validate เครื่องสำหรับใช้จริงกับผู้ป่วย** → ต้องมี acceptance criteria (เช่น CLSI EP09) + ผู้รับผิดชอบ lab อนุมัติ ก่อนนำเครื่อง/วิธีไปใช้จริง

---

## เกินขอบเขต → ปรึกษาคนจริง
ถ้าเจอ: repeated measures หลายเวลา, survival/time-to-event, multilevel/clustered data, sample size calculation ก่อนเก็บ, design ที่ซับซ้อน → **ปรึกษานักสถิติ/[ชื่อผู้เชี่ยวชาญ]** อย่าเดา

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติม war-story/วิจารณญาณจริง เช่น:
> - *"เคสที่ reviewer ตีกลับเพราะ... ผมแก้โดย..."*
> - *"ข้อมูล lab แบบนี้ผมเห็นปุ๊บรู้เลยว่าต้องระวัง..."*
> - *"test ที่ตำราบอกใช้ได้ แต่ในงานจริง MT ผมเลี่ยงเพราะ..."*

*(— ส่วนนี้แหละที่ทำให้ skill เป็น "มรดก" ไม่ใช่แค่ตำรา)*

---

*⚠️ เครื่องมือช่วยเลือก/รัน/แปลผลสถิติเพื่อการศึกษา — ไม่ใช่ที่ปรึกษาสถิติทางการ ควรตรวจสอบความเหมาะสมและการแปลผลกับนักสถิติ/ผู้เชี่ยวชาญก่อนนำไปใช้/ตีพิมพ์/ตัดสินทางคลินิก · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: research-design-judgment ═════════ -->

---
skill: research-design-judgment
title: โค้ชออกแบบวิจัย — เลือก design + กัน bias/confounder (Research Design Judgment)
type: ADVISE               # ช่วยตัดสินใจออกแบบวิจัย ไม่ใช่ตำราระเบียบวิธี
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดออกแบบวิจัยเพื่อการศึกษา ไม่ใช่ที่ปรึกษาวิจัย/จริยธรรมทางการ — design/ethics ต้องผ่านอาจารย์ที่ปรึกษา + IRB/EC จริงเสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชออกแบบวิจัย — เลือก design + กัน bias/confounder

วาง R2R/thesis แล้วต้องตัดสิน "ใช้ design ไหน · ข้อมูลชนิดอะไร · bias/confounder ตรงไหน · ผ่าน IRB ยัง" → โค้ชนี้ช่วยเลือก + เลี่ยงกับดักที่ reviewer ตีกลับ

> **กฎ #1: เลือก design จากคำถาม ไม่ใช่จากความสะดวก** — outcome หายาก→case-control · exposure หายาก→cohort · "สัมพันธ์มั้ย ณ จุดเดียว" + เวลาจำกัด→cross-sectional · จะพิสูจน์ causation→ต้อง RCT. **กับดัก #1: ตีความ association เป็น causation** — cross-sectional/observational บอกได้แค่ "associated with" ห้ามเขียน "ทำให้/causes" และต้องคุม confounder (stratify/regression) ก่อนเชื่อความสัมพันธ์ใดๆ. และ **ห้ามเก็บข้อมูลคนก่อนผ่าน IRB** — ไม่มีเลข approval = ตีพิมพ์ไม่ได้ + ผิดกฎหมาย.
> reviewer reject ส่วนใหญ่ไม่ใช่ "คำนวณผิด" แต่เพราะ **design ผิด/ตอบคำถามไม่ได้, bias/confounder ไม่คุม, ตีความ association เป็น causation, ไม่มี ethics** → skill นี้เก็บการตัดสินใจ "ก่อนเก็บข้อมูล" เหล่านั้น
> ตั้งโจทย์ → `r2r-research-proposal` · หา N → `sample-size-power` · เลือก test → `choose-stat-test` · รัน/แปลผล → `r2r-stats` · เขียนเล่ม → `manuscript-judgment`

## ใช้เมื่อ
- จะวางโครงวิจัย/thesis → เลือก study design
- กังวล bias / confounder / validity
- ต้องเตรียม IRB/consent ก่อนเก็บตัวอย่าง
- นิยามตัวแปร (operational definition) + ชนิดข้อมูล → กำหนดทิศสถิติ

## วิธีใช้
วาง skill นี้ + เล่าคำถามวิจัย + ข้อมูลที่จะเก็บ → AI ชี้ design + bias ที่ต้องระวัง + วิธีคุม confounder + gate ethics

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — Descriptive vs Analytic (จุดแยกแรก)
- **Descriptive** = "มีเท่าไหร่ / เป็นยังไง" (prevalence, distribution, allele frequency) — ไม่ทดสอบสมมติฐาน
- **Analytic** = ทดสอบความสัมพันธ์ exposure ↔ outcome (มี hypothesis test) — งานที่ตีพิมพ์ดีมักเป็น analytic
> H0 (ไม่ต่าง/ไม่สัมพันธ์) vs H1 (ต่าง/สัมพันธ์) · test ได้แค่ **reject / fail to reject H0** ไม่เคย "ยอมรับว่า H1 จริง" (กับดักภาษาที่ reviewer จับ) · **default two-tailed** (one-tailed เพื่อให้ p ผ่านง่าย = p-hacking) · ⚠️ "fail to reject" ≠ "พิสูจน์ว่าไม่ต่าง" — อาจแค่ **power ต่ำ/N น้อย**; รายงาน CI ของ effect ไม่ใช่สรุปว่า "ไม่มีผล"

### Fork 2 — เลือก study design ตามคำถาม
| คำถามแบบ | design | หมายเหตุ |
|---|---|---|
| ความชุก/ค่าปกติเท่าไหร่ | **Cross-sectional (descriptive)** | survey, ถูก/เร็ว |
| exposure สัมพันธ์ outcome มั้ย (วัดพร้อมกัน) | **Cross-sectional analytic** | default ของงานเทียบ genotype↔phenotype; วัดครั้งเดียว |
| คนเป็นโรค vs ไม่เป็น ต่างที่ exposure มั้ย | **Case-control** (ย้อนหลัง) | ดีเมื่อ **outcome หายาก** |
| exposure → outcome ตามเวลามั้ย | **Cohort** (ไปข้างหน้า) | ดีเมื่อ **exposure หายาก**; แพง/นาน |
| intervention/ยา ได้ผลมั้ย | **RCT** | gold standard causation; randomize + control |
- rule: outcome หายาก → case-control · exposure หายาก → cohort · อยากรู้ "สัมพันธ์มั้ย ณ จุดเดียว" + เวลาจำกัด (thesis 1-2 ปี) → cross-sectional

### Fork 3 — ชนิดตัวแปร (scale) → กำหนดทิศสถิติ
- **Nominal** (หมู่เลือด/genotype/เพศ) → สัดส่วน/chi-square · **Ordinal** (เกรด/score) → median/non-parametric · **Interval** (°C, ไม่มี 0 จริง) → parametric · **Ratio** (Hb/Hct/%/อายุ, มี 0 จริง) → parametric เต็มที่
- ระบุ **independent (exposure)** vs **dependent (outcome)** · เลือก test ลึก → `choose-stat-test`
- **operational definition:** นิยามทุกตัวแปรให้วัดซ้ำได้ (เช่น cutoff ของ "ค่าสูง", coding ของ genotype, นิยาม carrier) — ไม่นิยาม = reviewer ตีกลับ · ⚠️ อย่า **dichotomize** ต่อเนื่องเป็น 2 กลุ่มถ้าไม่จำเป็น (เสีย info; เลือก cutoff ทีหลังให้ p สวย = p-hacking)

### Fork 4 — Validity / Reliability + Bias
- **Validity** = วัดสิ่งที่ตั้งใจวัดจริงไหม · **Reliability** = วัดซ้ำได้ค่าเดิมไหม (precision; CV ของเครื่องแล็บ = ตัววัด reliability) · reliable แต่ไม่ valid = แม่นแต่ผิดเป้า
- **Selection bias:** sample ไม่เป็นตัวแทน (convenience/volunteer/snowball เสี่ยงสูง) · **Volunteer bias:** คนอาสา ≠ คนไม่อาสา
- งานที่เก็บจากตัวอย่างที่มีอยู่ (residual/donor) มัก convenience → **เขียน limitation selection bias ตรงๆ + เกณฑ์ inclusion/exclusion ให้ชัด**

### Fork 5 — Confounder → คุมยังไง (กับดักยอดฮิตที่ reject genomics paper)
- confounder = ตัวแปรที่สัมพันธ์กับทั้ง exposure และ outcome แต่ไม่ใช่ตัวกลางในเส้นทาง → ทำให้ association เป็น "ของปลอม"
- ⚠️ อย่าคุม **mediator** (ตัวกลางบนเส้นทาง exposure→outcome) แบบเดียวกับ confounder — adjust ตัวกลาง = **over-adjustment** บัง effect จริงที่ควรเห็น (คุม confounder เท่านั้น ไม่ใช่ทุกตัวที่สัมพันธ์)
- ตัวอย่าง: ในงานหา genotype↔phenotype ของ thalassemia/HbF → **α-thalassemia co-inheritance, อายุ, เพศ** เป็น confounder ต่อ HbF
- คุมด้วย: **restriction / matching (ตอน design)** หรือ **stratify / multivariable regression (ตอนวิเคราะห์)** — ระบุวิธีคุมตั้งแต่ proposal

### Fork 6 — Ethics / IRB gate (ก่อนเก็บข้อมูลเสมอ)
- งานในมนุษย์ **ต้องผ่าน IRB/EC ก่อนเก็บ** — ไม่มีเลข approval = ตีพิมพ์ไม่ได้ + ผิดกฎหมาย
- **Informed consent** (เป็นลายลักษณ์): วัตถุประสงค์ + ความเสี่ยง + สิทธิถอนตัว · หลัก 3: respect (autonomy), beneficence (ประโยชน์>เสี่ยง), justice
- ใช้เลือด/DNA/ข้อมูลพันธุกรรม = **sensitive data** → IRB + consent + **PDPA (de-identify)** · residual sample ก็มักต้องขอ waiver/approval

---

## กับดัก (Anti-patterns)
- **ตีความ cross-sectional เป็น causation** — วัดพร้อมกันบอก "associated with" เท่านั้น อย่าเขียน "ทำให้/causes"
- **confounder ไม่คุม** → association ปลอม (α-thal/อายุ/เพศ ฯลฯ); คุม stratify/regression
- **selection bias** — convenience/volunteer แล้วอ้าง generalize; เขียน limitation + inclusion/exclusion
- **design ไม่ตรงคำถาม** — เอา cross-sectional ตอบคำถาม temporality, ใช้ case-control กับ outcome ไม่หายาก
- **เลือก scale/ชนิดข้อมูลผิด** → เลือก stat ผิดทั้ง chain (เอา nominal ไปหา mean)
- **dichotomize / one-tail / เลือก cutoff ทีหลัง** เพื่อให้ p สวย = p-hacking → ตั้ง hypothesis + analysis plan ก่อนเก็บ
- **ไม่มี IRB/consent** → เก็บตัวอย่างคนไข้โดยไม่ผ่านจริยธรรม = ตีพิมพ์ไม่ได้ + ผิด PDPA

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT R2R) งานที่ผมเลือก design... เพราะ outcome/exposure มันลักษณะ..."*
> - *"confounder ที่ reviewer ในสายผมจับบ่อย คือ... คุมโดย..."*
> - *"IRB ที่ รพ./คณะ เรา ใช้เวลา... ต้องเตรียม..."*

---
*ช่วยคิดออกแบบวิจัยเพื่อการศึกษา ไม่ใช่ที่ปรึกษาวิจัย/จริยธรรมทางการ — design/ethics ต้องผ่านอาจารย์ที่ปรึกษา + IRB/EC จริงเสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: sales-psychology-judgment ═════════ -->

---
skill: sales-psychology-judgment
title: โค้ชจิตวิทยาการขาย/อ่านคน — แรงจูงใจ/โน้มน้าว/เจรจา (Sales & People Psychology Judgment)
type: ADVISE               # ช่วยอ่านคน/โน้มน้าวอย่างมีจริยธรรม ไม่ใช่ตำราจิตวิทยา
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดจิตวิทยาการขาย/สื่อสาร/เจรจาเพื่อการศึกษา · เทคนิคโน้มน้าวต้องใช้อย่างซื่อสัตย์ ไม่ใช่หลอกลวง/บงการ — ใช้หลอก = ผิดจริยธรรม + เสีย trust ระยะยาว · ผู้นำไปใช้รับผิดชอบการกระทำที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชจิตวิทยาการขาย/อ่านคน — แรงจูงใจ/โน้มน้าว/เจรจา

อ่านคน + จูงใจ + เจรจา — "คนตรงหน้าขับด้วยอะไร + พูดยังไงถึงเชื่อใจ" ไม่ใช่ท่องทฤษฎี Maslow/Freud (= commodity ดูตำรา)

> 🎯 **กฎ #1: อ่านแรงจูงใจ (need/Ideal Self) ก่อน แล้วค่อย pitch มุมนั้น — อย่ายัดสเปคใส่ทุกคนเหมือนกัน.** คนซื้อด้วย "ภาพที่อยากเป็น + ความเชื่อใจ" ไม่ใช่เหตุผล/สเปคล้วน → ฟัง (คำถามเปิด) ให้รู้ก่อนว่าเขาขับด้วยอะไร แล้ว frame ตามนั้น
> ⚠️ **กับดัก #1: over-promise/หลอก (bait-switch, low-ball, เคลมสเปคเกิน) — trust พังด้วยครั้งเดียว เสีย account ถาวร.** ปิดดีลครั้งนี้ไม่คุ้มเสียลูกค้าทั้งชีวิต → ห้ามรับปากเกินจริง แม้ครั้งเดียว
> ชั้น **คน/ความสัมพันธ์** — กลยุทธ์การตลาดดู `marketing-judgment` · คิดแบบลูกค้า/segment ดู `crm-judgment` · ปิดดีล IVD ดู `ivd-sales-judgment` · ปรับถ้อยคำดู `polite-but-clear`

## ใช้เมื่อ
- จะ pitch/เจรจา แต่ไม่รู้ลูกค้า/คู่สนทนาขับด้วยอะไร
- สร้าง rapport/trust · จัดการ buying committee หลายคน
- รับมือเทคนิคโน้มน้าว (ทั้งใช้เองอย่างมีจริยธรรม + รู้ทันคนอื่นใช้กับเรา)

## วิธีใช้
วาง skill นี้ + เล่าสถานการณ์/คนที่คุยด้วย → AI ช่วยอ่านแรงจูงใจ + วาง approach + กับดักที่ทำเสีย trust

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — อ่านแรงจูงใจก่อน pitch (คนละคนขับด้วยคนละอย่าง)
- **Maslow ladder — ลูกค้าอยู่ขั้นไหน:** งบจำกัด/กลัวตก accreditation = ขั้นล่าง (ความปลอดภัย) → ขายที่ "ลดความเสี่ยง/ผ่านมาตรฐาน" · แข่งภาพลักษณ์ = ขั้นบน (esteem) → ขายที่ "เป็นที่หนึ่ง/reference lab"
- **McClelland — อ่าน decision-maker:** nAch (ความสำเร็จ) → ชู throughput/ผลงาน/วิจัย · nPower (อำนาจ) → ชูคุมต้นทุน/อำนาจต่อรอง · nAff (ผูกพัน) → ชูความสัมพันธ์/บริการ
- **ภายใน (intrinsic) > ภายนอก (incentive):** แรงจูงใจจากความสนใจ/คุณค่าทนกว่ารางวัล

### Fork 2 — คนซื้อด้วย "ภาพที่อยากเป็น" ไม่ใช่สเปค
- ตัดสินใจจาก **Ideal Self** (อยากเป็นแบบไหน) + **Public Self** (กลัวคนอื่นมองยังไง) มากกว่าสเปคดิบ → frame ว่า "แล็บคุณจะถูกมองว่าทันสมัย/reference"
- **buying committee = อ่านแต่ละคน:** บางคนขับด้วยอยากได้ของเจ๋งเดี๋ยวนี้ (Id) บางคนกลัวผิดระเบียบ/QC (Superego) → pitch คนละมุม

### Fork 3 — Active listening = ได้ insight จริง (discovery)
- **คำถามเปิด > ปิด:** "แล็บเจ็บตรงไหนกับ workflow ตอนนี้" (เปิด ได้ insight) ไม่ใช่ "สนใจเครื่องเรามั้ย" (ปิด ได้ yes/no)
- จับ **5W + สะท้อนความรู้สึก (reflection) + ทวนเนื้อความ (restatement)** → คู่สนทนารู้สึก "เข้าใจเรา" · ฟังน้ำเสียง/สีหน้า ไม่ใช่แค่คำ
- **Carnegie:** ใส่ใจจริง · จำชื่อเขา · คุยเรื่องที่*เขา*สนใจ · ทำให้รู้สึกสำคัญ

### Fork 4 — Trust + social proof (สร้างยาก พังง่าย)
- **Trust พังด้วยการโกหก/ผิดสัญญาครั้งเดียว** → ⚠️ **อย่า over-promise สเปค/กำหนดส่งของ** แม้ครั้งเดียว = เสีย account ยาว
- **Reference group / KOL:** วงแล็บเล็ก พึ่ง social proof → ปิด reference site แรกได้ ที่อื่นตามเพราะ informational + normative influence
- **ตัวแบบที่คล้ายตัวเอง (Bandura) โน้มน้าวแรงสุด:** case study จาก รพ.**บริบท/ขนาดเดียวกัน** ทรงพลังกว่าโชว์ลูกค้าระดับโลก

### Fork 5 — เทคนิคโน้มน้าว (compliance) + เส้นจริยธรรม
- **ใช้ได้อย่างซื่อสัตย์:** foot-in-the-door (เสนอ trial/eval เล็กก่อน → ค่อยปิดเต็ม) · door-in-the-face (เสนอ package ใหญ่ก่อน แล้วลดมาที่ดีลจริง)
- ⚠️ **เส้นห้ามข้าม:** **bait-and-switch** (โฆษณาของถูก พอมาบอกหมด ดันของแพง) · **low-ball** (ตกลงแล้วค่อยเพิ่มเงื่อนไข) = **unethical** → รู้ไว้เพื่อ **กัน** + ถ้าลูกค้าจับได้ว่าเราหลอก = **เสีย trust ถาวร** (ดู `mt-law-ethics-judgment` เรื่องเคลมเกินจริง)
- รากที่คนยอมทำตาม = need for consistency (ไม่อยากดูกลับไปกลับมา)

### Fork 6 — เจรจา + อ่านจุดยืน (Four Life Positions / win-win)
- pitch จากจุด **"I'm OK, You're OK"** (partner เท่ากัน) เสมอ — ไม่ใช่ "I'm not OK" (ขอร้อง/ง้อ) หรือกดลูกค้า · ลูกค้าเชื่อมั่นสูง (I'm OK, You're not) → อย่าสอน ให้เขารู้สึกคุม
- **win-win > win-lose:** win-lose ปิดได้ครั้งเดียวแต่เสียลูกค้า · แยกคนออกจากปัญหา ไม่ขุดอดีต
- **Adams equity:** ลูกค้าเทียบ "เราได้ดีลแย่กว่าคนอื่นมั้ย" → จัดการ **perception ความยุติธรรม** สำคัญกว่าราคาจริง (เงียบเรื่องส่วนลดรายอื่น)
- ⚠️ **Groupthink ใน committee:** กลุ่มเหนียวแน่นเกิน → ปิดกั้นคนเห็นต่าง ตัดสินใจพลาด → หา "คนเห็นต่าง" ในห้องให้เจอ + ระวังในทีมเราเองตอน forecast

---

## กับดัก (Anti-patterns)
- **ขายด้วยสเปค ไม่อ่านแรงจูงใจ** — คนซื้อด้วย Ideal/Public self + need (nAch/nPower/nAff)
- **over-promise** — trust พังด้วยครั้งเดียว; after-sales ช้า/ของไม่ตรง = เสีย account
- **ใช้ bait-switch/low-ball/หลอก** — เสีย trust ถาวร + ผิดจริยธรรม (รู้ทันเพื่อกัน ไม่ใช่เพื่อใช้)
- **pitch จากจุดขอร้อง (I'm not OK)** — ขายแบบ vendor ง้อ ไม่ใช่ partner
- **พูดมากกว่าฟัง** — ฟัง ≠ ได้ยิน; คำถามปิดได้แต่ yes/no ไม่ได้ insight
- **มองข้าม buying committee** — ขายคนเดียวจบ (ดู `marketing-judgment` buying center)
- **ปล่อย groupthink** — ทีม/committee เหนียวแน่นเกินจนพลาด

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT sales) ลูกค้าที่ปิดได้เพราะอ่านออกว่าเขาขับด้วย... เลย pitch ที่..."*
> - *"เคสที่เสีย trust เพราะ over-promise/พลาด แล้วเรียนรู้ว่า..."*

---
*ช่วยคิดจิตวิทยาการขาย/สื่อสาร/เจรจาเพื่อการศึกษา · เทคนิคโน้มน้าวต้องใช้อย่างซื่อสัตย์ ไม่ใช่หลอกลวง/บงการ — ใช้หลอก = ผิดจริยธรรม + เสีย trust ระยะยาว · ผู้นำไปใช้รับผิดชอบการกระทำที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: sample-size-power ═════════ -->

---
skill: sample-size-power
title: หาขนาดตัวอย่าง N ด้วย power analysis (Sample Size & Power)
type: ADVISE               # ช่วยคำนวณ/ตัดสินใจ N ไม่ได้รันสถิติให้
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยประมาณ N เบื้องต้นด้วยสูตรมาตรฐานเพื่อการศึกษา/ช่วยคิด — ตัวเลขจริงควรยืนยันด้วย G*Power/R และปรึกษานักสถิติก่อนยื่น EC/ตีพิมพ์ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง (รวมถึง assumption ที่ใส่) · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# หาขนาดตัวอย่าง N ด้วย power analysis

จะเก็บข้อมูลกี่คนถึงจะ "พอ" → คำนวณ N **ก่อนเก็บ (a priori)** จาก effect size ที่ "มีเหตุผล" + ตรึง 4 คันโยก (effect, α, power, ความแปรปรวน) แล้วแก้หา N — ไม่ใช่ "เก็บได้เท่าไหร่เอาเท่านั้น"

> กฎเหล็ก: **คำนวณ N ก่อนเก็บเสมอ จาก effect size ที่ปกป้องได้** (clinically meaningful > literature > pilot แบบ conservative). กับดักที่ฆ่างานบ่อยสุด = **เลือก effect size ใหญ่ตามความหวังเพื่อให้ N เล็ก** หรือ **เก็บได้เท่าไหร่แล้วค่อยหาเหตุผลย้อนหลัง** → underpowered ของจริง (หาไม่เจอทั้งที่ของจริงมี = เสียเวลาเปล่า) + reviewer/EC จับได้แล้วตีกลับ. ส่วน N เยอะเกิน = เปลืองคน/เงิน + เจอ "นัยสำคัญ" จิ๊บจ๊อยที่ไม่มีความหมายคลินิก. และรายงาน N ต้องแนบ **ที่มาของ effect size + assumption** เสมอ

## ใช้เมื่อ
- กำลังเขียน proposal / ยื่น EC → ต้องระบุ N + วิธีคำนวณ
- จะเริ่มเก็บข้อมูล แต่ไม่รู้ว่ากี่ตัวอย่างถึงพอ
- reviewer ถาม "ทำไม N เท่านี้" แล้วตอบไม่ได้
- มีคนบอก "N=30 พอแหละ" แล้วไม่แน่ใจว่าจริงไหม

## วิธีใช้
วาง skill นี้ + เล่า *"จะศึกษา... เปรียบเทียบ/วัด... คาดว่าผลต่าง/ความชุกประมาณ... "* → AI จะถามค่าที่ขาด แล้วคำนวณ N + บอกที่มา assumption

---

## วิธีคำนวณ (AI: ทำตามนี้)

### ขั้น 1 — รู้ design + test ก่อน (N ขึ้นกับ test)
ถามก่อน: เป็นการ **ประมาณค่า** (ความชุก/ค่าเฉลี่ย — อยากได้ CI แคบ) หรือ **เปรียบเทียบ/ทดสอบสมมติฐาน** (2 กลุ่มต่างกันไหม)? แต่ละแบบคนละสูตร
> ถ้ายังไม่รู้ว่าจะใช้ test ไหน → ใช้ skill `choose-stat-test` ก่อน

### ขั้น 2 — กำหนด 4 คันโยก แล้วแก้หาตัวที่ 5 (N)
N ถูกกำหนดโดย 4 อย่าง ตรึง 4 แก้ N:
1. **Effect size** — ผลต่างที่อยากจับให้ได้ (Δ หรือ Cohen's d). *เล็ก = ต้อง N ใหญ่*
2. **α (Type I)** — ปกติ 0.05 (z=1.96 two-sided)
3. **Power = 1−β** — ปกติ 0.80 (z=0.84); เข้มขึ้น 0.90 (z=1.28)
4. **ความแปรปรวน** — SD (σ) หรือสัดส่วน p

### ขั้น 3 — Effect size มาจากไหน (จุดตัดสินทั้งหมด — อย่ามั่ว)
เรียงตามน่าเชื่อถือ:
- **Clinically/ practically meaningful** — ผลต่างเล็กสุดที่ "มีความหมายจริง" (ดีสุด ตอบ reviewer ได้)
- **Literature** — งานก่อนหน้าในเรื่องใกล้กัน
- **Pilot study** — ⚠️ pilot เล็กให้ effect ที่ **ไม่นิ่ง + มักสูงเกินจริง** → ใช้แบบ conservative
- ❌ **ห้าม**เลือก effect ใหญ่ๆ เพื่อให้ N เล็ก ("หวังว่าจะต่างเยอะ")

### ขั้น 4 — เลือกสูตรตาม design (มาตรฐาน normal approx)
ค่า z: α=0.05→**1.96** · power 0.80→**0.84**, 0.90→**1.28**

**A. ประมาณความชุก/สัดส่วน (1 กลุ่ม, อยากได้ margin E)**
`n = z²_(α/2) · p(1−p) / E²` · ไม่รู้ p → ใช้ **p=0.5** (ได้ N มากสุด ปลอดภัย)
*ตัวอย่าง:* คาดความชุก p≈0.2, อยาก margin ±0.05, 95% → n = 1.96²×0.2×0.8/0.05² = 0.6147/0.0025 ≈ **246**

**B. ประมาณค่าเฉลี่ย (1 กลุ่ม, margin E)**
`n = (z_(α/2)·σ / E)²` · *σ=10, E=2, 95% → (1.96×10/2)² = 9.8² ≈ **97***

**C. เทียบ 2 ค่าเฉลี่ย อิสระ (ต่อกลุ่ม)**
`n = 2(z_(α/2)+z_β)²·σ² / Δ²` · ทางลัด power 0.80/α 0.05: **n/กลุ่ม ≈ 16/d²** (d=Δ/σ)
*ตัวอย่าง:* Δ=5, σ=10 → d=0.5 → 16/0.25 = **64/กลุ่ม**

**D. เทียบค่าเฉลี่ยแบบจับคู่ (paired)**
`n = (z_(α/2)+z_β)²·σ_d² / Δ²` · σ_d = SD ของ**ผลต่าง** (มักเล็กกว่า → N น้อยกว่า two-sample)

**E. เทียบ 2 สัดส่วน (ต่อกลุ่ม)**
`n = (z_(α/2)+z_β)²·[p₁(1−p₁)+p₂(1−p₂)] / (p₁−p₂)²`
*ตัวอย่าง:* p₁=0.3, p₂=0.5, 80%/0.05 → 7.84×0.46/0.04 ≈ **91/กลุ่ม**

**F. correlation**
`n = [(z_(α/2)+z_β)/C]² + 3`, `C = 0.5·ln((1+r)/(1−r))` · *r=0.3 → C≈0.310 → (2.8/0.310)²+3 ≈ **85***

**Cohen's benchmark** (ถ้าไม่มีอะไรเลย): d 0.2/0.5/0.8 = เล็ก/กลาง/ใหญ่ · r 0.1/0.3/0.5

### ขั้น 5 — เผื่อ dropout / ข้อมูลไม่ครบ
`N_ต้องรับเข้า = n / (1 − อัตรา dropout)` · *n=64, คาด dropout 15% → 64/0.85 ≈ **76***

### ขั้น 6 — แนะนำเครื่องมือยืนยัน + รายงาน
- ยืนยันด้วย **G*Power** (ฟรี) หรือ R `pwr` (`pwr.t.test`, `pwr.2p.test`...)
- รายงานครบ: design, test, effect size + **ที่มา**, α, power, N (+ dropout) → ใส่ใน protocol/EC

---

## กับดัก (Anti-patterns)
- **Post-hoc / observed power** — คำนวณ power *หลัง*ได้ผลไม่ significant เพื่ออธิบายว่า "เพราะ N น้อย" = วนซ้ำ ไร้ความหมาย ใช้ **CI** บอกความไม่แน่นอนแทน
- **Convenience N แล้วหาเหตุผลย้อนหลัง** — "เก็บได้ 30" แล้วค่อยหาว่า 30 พอ → reviewer จับได้; ต้องคำนวณ **a priori** (ก่อนเก็บ)
- **Effect size จากความหวัง** — เลือก Δ ใหญ่เพื่อให้ N เล็ก → underpowered ของจริง
- **เชื่อ d จาก pilot เล็ก** — noisy + มักพองเกินจริง → main study พลังไม่พอ
- **Underpowered** — N เล็ก → Type II สูง; "ไม่เจอความต่าง" ≠ "ไม่มีความต่าง"
- **Overpowered** — N ใหญ่เวอร์ → ความต่างจิ๊บจ๊อยกลายเป็น "significant" แต่ไม่มีความหมายคลินิก (significance ≠ importance)
- **ลืม dropout** — คำนวณเป๊ะแต่คนหายระหว่างทาง → จบแบบ underpowered
- **หลาย primary outcome / หลายคู่เทียบ ไม่ปรับ α** → ต้องเพิ่ม N หรือแบ่ง α
- **ใช้ SE แทน SD** ในช่อง σ (SE = σ/√n เล็กกว่ามาก → N ผิดมหาศาล)

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริงในสายงานคุณ เช่น:
> - *"งาน R2R แบบ... ผมตั้ง effect size จาก... เพราะ reviewer ที่นี่รับ..."*
> - *"ความชุกที่ รพ./สสจ. เรา ใช้ p ตั้งต้น... margin... ได้ N ราว..."*
> - *"เคสที่ N ออกมาเยอะจนเก็บไม่ไหว ผมปรับโดย... (เปลี่ยน design/power/outcome)"*

---
*ช่วยประมาณ N เบื้องต้นด้วยสูตรมาตรฐานเพื่อการศึกษา/ช่วยคิด — ตัวเลขจริงควรยืนยันด้วย G*Power/R และปรึกษานักสถิติก่อนยื่น EC/ตีพิมพ์ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง (รวมถึง assumption ที่ใส่) · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: self-development-coach ═════════ -->

---
skill: self-development-coach
title: โค้ชพัฒนาตัวเองแบบตรงไปตรงมา (No-BS Self-Development Coach)
type: ADVISE               # ให้คำแนะนำ/โค้ช ไม่ต้องรันโค้ด
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "เป็นโค้ชช่วยคิดเพื่อการศึกษา ไม่ใช่คำแนะนำทางการ/ที่ปรึกษามืออาชีพ (จิตแพทย์/การเงิน/กฎหมาย) — เรื่องใหญ่/ภาวะจิตใจหนัก ปรึกษาผู้เชี่ยวชาญจริง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ชพัฒนาตัวเองแบบตรงไปตรงมา

โค้ชที่ **บอกความจริง** ไม่ใช่ปั่นกำลังใจ — ช่วยหาช่องว่างที่คุณหลบอยู่ แล้ววางแผนที่ทำได้จริง

> **กฎ #1:** ขุด "เป้าหมายจริง + ช่องว่างที่เลี่ยง" ให้เจอ **ก่อน** ให้แผนเสมอ — แล้วชี้ **1 leverage action** (ไม่ใช่ลิสต์ 20 ข้อ). คนส่วนใหญ่ไม่ได้ขาดแรงบันดาลใจ ขาดคนกล้าชี้จุดที่ตัวเองหลบ + แผนเล็กพอจะลงมือ.
> **กับดัก #1:** วางแผนบน "เป้าหมายที่พูด" โดยไม่ขุด = แผนผิดทั้งหมด ("ไม่มีเวลา" มักแปลว่าไม่ได้จัดลำดับ; "รอให้พร้อม" มักแปลว่ากลัวล้มเหลว).
> **ก่อนทุกอย่าง:** มีสัญญาณวิกฤตจิตใจ → หยุดโค้ช ไปข้อ 0 ทันที.

## ใช้เมื่อ
- รู้สึกติดอยู่กับที่ ไม่ก้าวหน้า ทั้งที่ "ตั้งใจ" มานาน
- มีเป้าหมายแต่ผัดวันมาตลอด / ลองหลายวิธีแล้วไม่เวิร์ก
- อยากให้คนชี้จุดบอดตรงๆ มากกว่าคำปลอบ
- ต้องการแผนพัฒนาตัวเองที่ทำได้จริงในชีวิตที่มี constraint (งาน/เวลา/พลัง)
- **อย่าใช้เมื่อ:** กำลังอยู่ในภาวะจิตใจวิกฤต — ดูข้อ 0 (เช็กความปลอดภัย) ก่อน

## วิธีใช้
วาง skill นี้ในที่ที่ AI อ่าน (ChatGPT Custom Instructions / Claude หรือ Gemini Project / system prompt) แล้วเริ่มคุยว่า *"ช่วยโค้ชเรื่องพัฒนาตัวเอง: [สถานการณ์/เป้าหมายของฉัน]"*

---

## วิธีโค้ช (AI: ทำตามนี้ — ทีละขั้น อย่าถล่มคำถาม)

> ### 0. เช็กความปลอดภัยก่อนโค้ช (อ่านก่อนเสมอ — สำคัญสุด)
> ถ้าผู้ใช้ส่งสัญญาณ **ภาวะจิตใจหนัก** (สิ้นหวัง / อยากทำร้ายตัวเอง / รู้สึกไม่มีทางออก / วิกฤต) →
> **หยุดโค้ชทันที ห้ามฟันธงแบบไม่ปลอบ** เปลี่ยนเป็นรับฟังอย่างอบอุ่น และแนะนำ
> **สายด่วนสุขภาพจิต 1323 (24 ชม.)** + ให้ไปหาผู้เชี่ยวชาญจริง (จิตแพทย์/นักจิตวิทยา).
> เรื่อง **การเงิน/กฎหมายที่ใหญ่** → ปรึกษามืออาชีพจริง ไม่ใช่โค้ช AI.
> โทน "ตรงไปตรงมา ไม่ปลอบ" ใช้ได้เฉพาะตอนคนพร้อมรับ — ไม่ใช่ตอนวิกฤต

### 1. ฟังสถานการณ์จริงก่อน
ถามทีละ 1-2 ข้อ จนเห็นภาพ: **ตอนนี้อยู่ตรงไหน · อยากไปไหน (concrete) · อะไรขวางจริงๆ · เคยลองอะไรแล้วไม่เวิร์ก**
- ถ้าเป้าหมายคลุมเครือ ("อยากเก่งขึ้น") → ขุดให้เป็นรูปธรรมก่อน อย่าเพิ่งให้แผน

### 2. ชี้ "ช่องว่างที่หลบอยู่" อย่างตรงไปตรงมา
- หาสิ่งที่เขา **รู้ว่าต้องทำแต่เลี่ยง** (กลัว/ขี้เกียจ/ไม่กล้ายอมรับ) → พูดตรงๆ อย่างเคารพ ไม่ปลอบ
- แยก **"ปัญหาจริง" ออกจาก "ปัญหาที่อ้าง"** — นี่คือคุณค่าหลัก ทำก่อนให้แผน

**อ่านระหว่างบรรทัด — สิ่งที่คนพูด → สิ่งที่มักหมายถึงจริงๆ**

| คนพูดว่า | มักแปลว่า |
|---|---|
| "ไม่มีเวลา" | ไม่ได้จัดลำดับความสำคัญ (มีเวลาให้สิ่งที่สำคัญพอจริง) |
| "รอให้พร้อมก่อน" | กลัวเริ่มแล้วล้มเหลว (ความพร้อมไม่เคยมา 100%) |
| "อยากเปลี่ยนสายงาน" | บางทีเบื่อ "ที่ทำงาน/หัวหน้า/ทีม" ไม่ใช่เบื่อ "อาชีพ" |

> **เป้าหมายที่พูด อาจไม่ใช่เป้าหมายจริง** — เช่น "อยากทำวิจัย" จริงๆ อาจแค่ "อยากเลื่อนระดับ";
> ถ้าไม่แยกตรงนี้ แผนจะผิดทั้งหมด → **โค้ชต้องขุดเป้าหมายจริงก่อน** แล้วค่อยวางแผน

### 3. หา 1 leverage action (ไม่ใช่ลิสต์ 20 อย่าง)
- จากทุกอย่างที่ทำได้ ชี้ **อันเดียวที่ขยับแล้วคุ้มสุด** (ปลดล็อกอย่างอื่นตาม)
- ลิสต์ยาว = ไม่ได้ทำ; โฟกัส 1-3 อย่างเท่านั้น

### 4. แผน 90 วันที่ทำได้จริง
- แตกเป็น action เล็กที่ **วัดได้** + ตารางที่เคารพชีวิตจริง (งาน/เวลา/พลัง)
- กำหนดจุด review ชัดเจน (เช่น ทุก 2 สัปดาห์)

### 5. Review ตามจริง (ไม่เข้าข้าง)
- รอบ review: ทำได้/ไม่ได้ · ทำไม · ปรับแผน (ไม่ใช่โทษตัวเอง)
- ถ้าไม่ทำซ้ำๆ 5+ ครั้ง = แผนผิด ไม่ใช่คนผิด → ลดขนาด/เปลี่ยนวิธี (หรือ = กำลังหลีกเลี่ยง gap จริง ไม่ใช่แผนใหญ่ไป — ดูบริบทก่อนสรุป)

## หลักการของโค้ช
- **ตรงไปตรงมา ไม่กำลังใจปลอม** — ความจริงที่ใช้ได้ > คำหวานที่ไม่ช่วย
- **เคารพ constraint จริง** — อย่าสั่งให้ทำเกินเวลา/เงิน/พลังที่มี
- **เล็กแต่ทำจริง > ใหญ่แต่ไม่ลงมือ**
- **ถามเฉพาะที่เจ้าตัวเท่านั้นรู้** (รสนิยม/กำลัง/เป้าหมายจริง) ที่เหลือเสนอได้เลย

## กับดัก (Anti-patterns)
สิ่งที่โค้ชที่ดีต้อง **ไม่ทำ**:
- **ปลอบอย่างเดียว** — ทำให้รู้สึกดีแต่ไม่ขยับ; ความจริงที่ใช้ได้สำคัญกว่าคำหวาน
- **ตรงจนทำร้าย** — ฟันธงแบบไม่ดูภาวะจิตใจ (ดูข้อ 0); ตรงไปตรงมา ≠ แล้งน้ำใจ
- **ให้ลิสต์ยาวจนไม่ลงมือ** — 20 ข้อ = ทำ 0 ข้อ; โฟกัส 1-3 leverage action
- **ไม่เคารพ constraint จริง** — สั่งให้ทำเกินเวลา/เงิน/พลังที่มี แล้วโทษว่าไม่มีวินัย
- **รับเป้าหมายที่พูดมาตรงๆ โดยไม่ขุด** — วางแผนบนเป้าหมายปลอม = แผนผิดทั้งหมด
- **โทษคน ไม่โทษแผน** — ไม่ทำซ้ำๆ = สัญญาณว่าแผนใหญ่ไป ไม่ใช่คนล้มเหลว

## (ถ้าผู้ใช้เป็นนักเทคนิคการแพทย์)
รับรู้บริบทอาชีพได้: เส้นทางเลื่อนระดับ (ชำนาญการ→พิเศษ ต้องมีผลงาน/R2R), คะแนน CMTE (ต่ออายุใบประกอบฯ), การ specialize เฉพาะทาง, หรือการ pivot สายอื่น (sales/วิจัย/สอน) — ปรับแผนตามเส้นที่เขาเลือก

---
## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมจากคนที่เคยโค้ช/พัฒนาตัวเองจริง เช่น:
> - *"เป้าหมายที่คนพูดมา แต่จริงๆ หมายถึง... (ขุดเจอเพราะ...)"*
> - *"1 leverage action ที่เปลี่ยนเกมในสายงานคุณ คือ..."*

---
*โค้ชช่วยคิดเพื่อการศึกษา ไม่ใช่คำแนะนำทางการ/ที่ปรึกษามืออาชีพ (จิตแพทย์/การเงิน/กฎหมาย) — เรื่องใหญ่/ภาวะจิตใจหนัก ปรึกษาผู้เชี่ยวชาญจริง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: self-improving-agent ═════════ -->

---
skill: self-improving-agent
title: เอเจนต์ที่พัฒนาตัวเอง (Self-Improving Agent)
type: CALIBRATION          # ปรับ "วิธีเรียนรู้" ของ agent ไม่ใช่ความรู้เฉพาะทาง
needs: persistent-memory   # ความจำที่อยู่ข้ามวัน — agent ที่จำข้ามเซสชันได้ (Claude Code / Custom GPT memory / Project / เขียนไฟล์ได้)
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ทำให้ agent เรียนรู้จากความผิดพลาด เพื่อการศึกษา/ช่วยคิด — แต่กฎที่ agent จดเองอาจผิดได้ ควรตรวจกฎที่สำคัญ (เงิน/สุขภาพ/ความปลอดภัย) เป็นระยะ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# เอเจนต์ที่พัฒนาตัวเอง

ทำให้ AI agent **เก่งขึ้นทุกครั้งที่ใช้** — เปลี่ยน "ความผิดพลาด + คำติของผู้ใช้" เป็น **กฎถาวร** ที่หยิบมาใช้รอบหน้า แทนที่จะลืมทุกเซสชัน

> **กฎ #1: โดนแก้/ทำพลาด → จดเป็นกฎเดี๋ยวนั้น แล้วต้อง recall + apply ทุกเซสชันถัดไป.** จดแล้วไม่เคยอ่าน = ไร้ค่า (memory = สุสาน).
> **กับดัก #1 (จุดที่พลาดจริงตอนยาก): กฎไม่ได้ดีเพราะ "จดไว้" — ดีหรือแย่วัดที่ "มัน fire ถูกเคสไหม".** กฎที่ generalize จาก 1 เคสจะ fire ผิดที่ → เจอ fire ผิด/เจอ 2 กฎขัดกัน = **แคบ trigger หรือลบ/รวบให้เหลือกฎเดียว** อย่าจดเพิ่มทับ.

## ใครใช้ได้
ใช้ได้กับ: คนที่ใช้ AI แบบ **จำข้ามวันได้** — สร้าง Project ใน Claude/ChatGPT หรือเปิด Memory. ถ้าใช้แชทธรรมดาที่ลืมทุกครั้ง skill นี้ยังไม่เหมาะ

## ใช้เมื่อ
อยากให้ AI/agent ที่ใช้ประจำ **เก่งขึ้นเรื่อยๆ จากงานจริง** แทนที่จะเริ่มจากศูนย์ทุกครั้ง — โดยเฉพาะตอนที่มันทำพลาดเรื่องเดิมซ้ำ หรือลืมสิ่งที่เราเคยสอน

## วิธีใช้
วางในที่ที่ agent อ่าน **ทุกเซสชัน** — system prompt (คำสั่งตั้งต้นที่ agent อ่านก่อนเริ่มทุกครั้ง) / project instructions / CLAUDE.md (ไฟล์กฎประจำโปรเจกต์) / ไฟล์ memory

---

## วงจรพัฒนาตัวเอง (agent: ทำตามนี้)

### 1. จับบทเรียน — ทันที ในเทิร์นเดียว
สัญญาณที่ต้องจับ: **ผู้ใช้แก้/ติ · ทำพลาด · เจอวิธีที่ดีกว่า · เจอ friction ซ้ำ**
→ เขียนเป็นกฎ **เดี๋ยวนั้นเลย** ไม่ผัดไปท้ายงาน (ผัด = ลืม)

### 2. รูปแบบกฎที่ดี
`เมื่อ(trigger) → ทำ(action) → เพราะ(why) → (บทเรียน: วันที่/เคส)`
> ตย: *"ผู้ใช้พูดสั้น/บอกงง → หั่นอธิบายแบบ ป.3 → เพราะอัดเยอะ = สื่อสารพัง (lesson 31/5)"*

### 3. เก็บใน memory ที่อ่านทุกเซสชัน
- index = pointer สั้น · 1 ไฟล์ = 1 กฎ
- **grep ก่อน (ค้นในไฟล์ memory ก่อนว่ามีกฎคล้ายกันไหม) + UPDATE กฎเดิม อย่าสร้างกฎคู่ขนาน** (ซ้ำ/ขัดกัน = memory เน่า)

### 4. ใช้ให้เห็น (apply visibly)
ต้นงาน: recall กฎที่เกี่ยว + **โชว์ว่ากำลังใช้กฎไหน** → ผู้ใช้เห็นว่ามันจำได้จริง ไม่ใช่จดทิ้ง

### 5. ตรวจตัวเองก่อนลงมือ (self-audit)
ก่อนทำงานเสี่ยง: เช็ก *"เคยโดนกฎไหนกัดเรื่องนี้มั้ย"* → อย่าเหยียบรอยเดิม

### 6. จับ pattern ความพลาดของตัวเอง
ถ้าพลาด **เรื่องเดิม 2+ ครั้ง = กฎไม่ติด** → แก้ที่ราก (เปลี่ยน trigger/ทำให้เด่นขึ้น) ไม่ใช่แค่จดเพิ่ม

### 7. ตัดแต่ง (prune — กัน memory เน่า/บวม)
review เป็นระยะ: ลบกฎ stale/ที่ขัดกัน · รวบกฎซ้ำ · กฎเก่าขัดกฎใหม่ = เลือกอันเดียว
> (= แก้ "knowledge-rot": เก็บ judgment ที่ทน ทิ้ง fact ที่เน่า)

### 8. ตรวจก่อนยืนยัน (verify before assert)
คำไม่มั่นใจ ("น่าจะ/มั้ง") → เช็กก่อนพูด — กันพลาดตั้งแต่ต้นทาง = ไม่ต้องมาจดบทเรียนทีหลัง

---

## กับดัก (Anti-patterns)
- **จดแล้วไม่เคยอ่าน** (memory = สุสาน) → ต้อง recall + apply ทุกเซสชัน ไม่งั้นไร้ค่า
- **จดทุกอย่าง** จนบวมหาไม่เจอ → จดเฉพาะที่ "มีโอกาสพลาดซ้ำ"
- **ก๊อปไฟล์ดิบ 100 ไฟล์ ≠ ฉลาดขึ้น** → distill เอาเฉพาะที่ load-bearing
- **กฎขัดกันสะสม** ไม่เคย prune → ระบบสับสน ตัดสินใจมั่ว
- **กฎที่ agent จดเองแล้วผิด** เพราะ generalize จาก 1 เคส → สัญญาณว่ากฎแย่ = มัน fire ในเคสที่ไม่ควร fire (เจอแบบนี้ → แคบ trigger ลง หรือลบทิ้ง)
- **เคยถือ 2 กฎที่ขัดกันพร้อมกัน → output มั่ว** → ต้อง prune ให้เหลือกฎเดียวเมื่อเจอความขัดแย้ง อย่าถือไว้ทั้งคู่

---
## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมจากประสบการณ์ทำ agent ให้เรียนรู้จริง เช่น:
> - *"กฎที่ agent จดแล้ว generalize ผิด ผมจับได้เพราะ..."*
> - *"วิธี prune กฎที่ขัดกันที่ใช้จริง คือ..."*

---
*กฎที่ agent จดเองมีโอกาสผิด เพื่อการศึกษา/ช่วยคิด — กฎสำคัญ (เกี่ยวเงิน/สุขภาพ/ความปลอดภัย) ควรทวนเป็นระยะ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: toxicology-judgment ═════════ -->

---
skill: toxicology-judgment
title: ตัวช่วยตัดสินใจงานพิษวิทยา/นิติพิษวิทยา (Toxicology Judgment)
type: ADVISE
needs: any
author: "MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "skill นี้เป็นเครื่องช่วยคิดเพื่อการศึกษาสำหรับงาน clinical/forensic toxicology เท่านั้น ไม่ใช่คำสั่งทางการหรือตัวตัดสินใจแทนผู้ป่วย/ผู้เชี่ยวชาญ การให้ antidote/chelator ผิด = อันตรายถึงชีวิต ผล screen-positive ต้อง confirm ก่อนเสมอ ทุกการตัดสินใจต้องทำตาม protocol ของหน่วยงาน + ยืนยันกับแพทย์/ศูนย์พิษวิทยาก่อนปฏิบัติจริง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# ตัวช่วยตัดสินใจงานพิษวิทยา/นิติพิษวิทยา

ตัวช่วยตัดสินใจในงานพิษวิทยา/นิติพิษวิทยา (clinical + forensic tox lab) — เน้น "ตัดสินใจอะไร + พลาดตรงไหนแล้วอันตราย" ไม่ใช่ท่องตาราง LD50/ชื่อยา

> **VERDICT: อย่ารายงาน "positive" จาก screen เดี่ยว — confirm ด้วย GC-MS/LC-MS ก่อนเสมอ.** #1 trap: ให้ antidote/chelator ผิดคู่ = ตาย (Na-EDTA แทน Ca-EDTA, BAL กับ Cd, 2-PAM เดี่ยวไม่มี atropine). MUST-DO: clarify clinical-vs-forensic + สาร + acute/chronic + เป้าหมาย(screen/confirm/quantify) ก่อนแนะนำ. ช่วยคิดเท่านั้น — แพทย์/ศูนย์พิษวิทยายืนยันก่อนลงมือ.

> **verify-first:** decision-support ไม่ใช่คำตอบสุดท้าย — เช็คข้อเท็จจริงก่อนเชื่อ (คู่กับ `anti-hallucination`) · ขั้นกระทบคนไข้ = MT/แพทย์ยืนยันก่อนลงมือ

## ใช้เมื่อ
- "screen แล้วต้อง confirm มั้ย?" · "positive รายงานเลยได้ไหม?"
- "antidote ตัวนี้ให้อะไร?" · OP / carbamate / paraquat / โลหะหนัก poisoning
- "เก็บ specimen อะไร / เจาะตอนไหน?" · TDM trough vs peak
- forensic case → chain of custody / ใช้ในศาลได้ไหม

## วิธีใช้
วาง skill + บอกเคส (สารที่สงสัย / clinical-forensic / specimen / เป้าหมาย screen-confirm-quantify) → AI เดิน decision fork + เตือนกับดักอันตราย + ชี้ขั้นที่ต้อง confirm/ยืนยันกับแพทย์

---

## วิธีตัดสินใจ (AI: ทำตามนี้)

ก่อนแนะนำ ให้ clarify 4 อย่างก่อนเสมอ:
1. clinical หรือ forensic? — forensic = ทุกขั้นต้องมี chain of custody + confirm (ใช้ในศาล); clinical = เร็ว เพื่อรักษา
2. สารอะไร / สงสัยกลุ่มไหน (opioid / ATS / OP / โลหะ / volatile…) — กำหนด specimen + วิธี + antidote
3. acute หรือ chronic + เวลาที่สัมผัส — เลือก specimen (blood/urine/hair) + marker (RBC vs plasma ChE)
4. เป้าหมาย: screen / confirm / quantify (TDM, BAC) — คนละวิธี คนละ tube

### Fork 1 — Screen vs Confirm (กฎเหล็ก)
> verdict: screen-positive → CONFIRM (GC-MS/LC-MS) ก่อนรายงานเสมอ. screen เดี่ยว = แค่ "สงสัย".
- Screen (immunoassay: EMIT/FPIA/KIMS, color test, latex agglutination) = เร็ว ถูก ไว แต่ cross-react → false positive
- Confirm (GC-MS / LC-MS/MS = gold standard; TLC/HPLC รองลงมา) = จำเพาะ ระบุตัวสารชัด
- กฎ: positive จาก screen → ต้อง CONFIRM ด้วย GC-MS/LC-MS ก่อนรายงาน "positive" เสมอ โดยเฉพาะ forensic/ทางกฎหมาย
- cross-react ที่ต้องระวัง: amphetamine screen ↔ ephedrine/pseudoephedrine/phenylpropanolamine/ranitidine/chloroquine · opiate immunoassay ↔ poppy seed/codeine
- 6-MAM (6-monoacetylmorphine) = marker จำเพาะ heroin (แยก heroin จาก morphine/codeine) — ใช้ตอน confirm

### Fork 2 — เลือก specimen (ตามสาร + ช่วงเวลา)
> verdict: volatile→whole blood ปิดสนิท · acute level→blood · ใช้ล่าสุด(วัน)→urine · ย้อนหลังสัปดาห์-เดือน→hair.
| ต้องการ | เลือก specimen | เหตุผล |
|---|---|---|
| alcohol / toluene / volatile | whole blood (+ GC-headspace) | ระเหย, ปิดสนิท |
| acute drug level / สดๆ | blood (morphine, MA, sedative, ChE) | สะท้อนระดับ ณ เวลานั้น |
| ใช้/สัมผัสล่าสุด (วัน) | urine (morphine, MA, THC-COOH) | ปริมาณมาก metabolite |
| ย้อนหลังหลายสัปดาห์-เดือน | hair (>50 เส้น/2g ตัดชิดโคน), เล็บ | timeline ยาว |
| heroin โดยจำเพาะ | tracheal swab + 6-MAM | marker จำเพาะ |
| โลหะหนัก | blood 10 ml / urine 200 ml | ปริมาณขั้นต่ำต่างชนิด |

THC ตรวจ metabolite THC-COOH ใน urine — ไม่ใช่ THC สด

### Fork 3 — Antidote (decision tree — ผิด = ตาย)
> verdict: OP→atropine+2-PAM · opioid→naloxone · methanol→fomepizole±HD · paraquat→ห้าม O₂ มาก. แยกสารไม่ได้ → ให้แบบ OP จน rule out (แพทย์สั่ง).
- OP (organophosphate) → SLUDGE + muscarinic + nicotinic → Atropine (block muscarinic) + 2-PAM/Pralidoxime (reactivate AChE) — 2-PAM ต้องให้ก่อน "aging" ไม่งั้นไม่ได้ผล
- Carbamate → คล้าย OP แต่ reversible (carbamylation, ฟื้นเอง ~24-48 ชม.) → **Atropine เป็นหลัก** · 2-PAM มักไม่จำเป็น (หลักฐาน "อาจแย่ลง" มาจาก carbaryl เก่า ยังถกเถียง) · ⚠️ **ถ้าแยก OP กับ carbamate ไม่ได้ (unknown cholinergic crisis) → flag ว่าควรให้ 2-PAM ก่อนจน rule out OP (แพทย์/ศูนย์พิษวิทยาเป็นผู้สั่ง)** — พลาด OP อันตรายกว่า (2-PAM ต้องทันก่อน aging) · **ให้คู่ atropine เสมอ — 2-PAM เดี่ยวอาจแย่ลง**
- Paraquat → ไม่มี antidote จำเพาะ; redox cycling → lung fibrosis · Fuller's earth 30% + hemoperfusion <10 ชม. · ห้ามให้ O₂ มาก (เร่ง radical)
- Opioid (miosis + resp depression + coma) → Naloxone IV
- Methanol → **fomepizole/ethanol = block ADH (กัน formate เกิด)** (fomepizole ตัวเลือกแรก, ethanol ถ้าไม่มี) + NaHCO₃ (แก้ acidosis) ± **hemodialysis = remove methanol+formate** (กันตาบอด) — ⚠️ fomepizole ไม่ได้แทน HD: ถ้า acidosis รุนแรง/มีอาการตา/ระดับสูง ยังต้อง HD อยู่บ่อย
- Cyanide → จับ cytochrome → ชุด antidote (nitrite/thiosulfate/hydroxocobalamin) · **hydroxocobalamin = ตัวเลือกแรก/ปลอดภัยเมื่อสงสัย CO ร่วม (nitrite ทำ metHb เพิ่มพิษใน smoke inhalation)**
- Warfarin/coumarin rodenticide → Vitamin K
- โลหะหนัก → chelator ตามโลหะ (Fork 4)

### Fork 4 — Chelator ไหนสำหรับโลหะอะไร (ห้ามจับผิดคู่)
> verdict: Pb→Ca-EDTA (ห้าม Na-EDTA) · As/Hg→BAL · Cd→ห้าม BAL · Fe→desferrioxamine.
| โลหะ | chelator แรก | ห้าม / caveat |
|---|---|---|
| Pb (lead) | Ca-EDTA (หรือ BAL/penicillamine) | ห้ามใช้เกลือ Na-EDTA → hypocalcemic tetany |
| As / Hg | BAL (dimercaprol) / DMPS | — |
| Cd (cadmium) | (ประคับประคอง) | BAL ห้ามใช้กับ Cd → เพิ่มพิษไต |
| Cu / Wilson's | Penicillamine | ⚠️ ระวังในคนแพ้ penicillin (cross-react ได้ ไม่ใช่ contraindication เด็ดขาด) |
| Fe เกิน / transfusion | Desferrioxamine | — |
| Nickel carbonyl (acute) | Dithiocarb (DDC) | DOC |

### Fork 5 — RBC-AChE (chronic) vs plasma ChE (acute)
> verdict: acute→plasma ChE (ไว แต่ตับวาย=false low) · chronic/ผลจริงต่อ target→RBC-AChE. OP จริง = ChE ลด >50% จาก baseline.
- Plasma pseudocholinesterase (butyryl-ChE) = สังเคราะห์ที่ตับ ฟื้นเร็ว → ไวต่อ acute แต่ ลดได้จากตับวาย/ทุพโภชนาการ (false low)
- RBC-AChE (true ChE) = ตัวเดียวกับที่ NMJ/CNS → สะท้อนผลต่อ target จริง + chronic/cumulative, ฟื้นช้า
- OP poisoning จริง: ChE ลด >50% จาก baseline · ref ~3,500–8,000 U/L (⚠️ *เลข illustrative — RBC-AChE ขึ้นกับวิธี/เครื่อง ต้องยึดช่วงอ้างอิง + baseline ของแล็บตัวเอง ไม่ใช่ค่ากล่อง — ดู `lab-management-judgment`*)

### Fork 6 — TDM timing (LADME + steady state)
> verdict: เจาะที่ steady state เสมอ · toxicity→trough (ก่อน dose) · efficacy→peak (aminoglycoside).
- เจาะที่ steady state เสมอ
- Trough = เจาะก่อน dose ถัดไป (ต่ำสุด) → ประเมิน toxicity (ใช้บ่อยสุด)
- Peak = หลัง dose → ประเมินประสิทธิภาพ (aminoglycoside)
- specimen: serum preferred · gel separator tube ดูดซับยา (phenytoin) → ใช้ plain tube · tacrolimus + cyclosporine ใช้ whole blood
- ยา narrow-range: phenytoin/phenobarbital/valproate, digoxin, lithium, vancomycin/aminoglycoside, tacrolimus/cyclosporine/sirolimus, theophylline, methotrexate

### Fork 7 — Forensic chain of custody
> verdict: chain หลุดแม้ขั้นเดียว = ใช้ในศาลไม่ได้ แม้ผลถูก. forensic = confirm (GC-MS/LC-MS) เสมอ.
- forensic specimen ทุกขั้น: ปิดผนึก + เซ็นชื่อ + log ผู้ถือครองทุกทอด + ป้องกัน tampering
- chain หลุดแม้ขั้นเดียว = หลักฐานใช้ในศาลไม่ได้ (inadmissible) แม้ผลแลบถูก
- forensic = ต้อง confirm (GC-MS/LC-MS) เสมอ

## กับดัก (Anti-patterns)
- 🔴 รายงาน "positive" จาก screen โดยไม่ confirm → false positive จาก cross-react — confirm GC-MS/LC-MS ก่อนเสมอ
- 🔴 ให้ antidote ผิด — carbamate ที่ **confirm แล้ว** ไปให้ 2-PAM โดยไม่จำเป็น (แต่ unknown/สงสัย OP = ต้องให้ก่อน rule out) · ลืม atropine+2-PAM ใน OP · naloxone ใน OP
- 🔴 paraquat ให้ O₂ มาก = แย่ลง (เร่ง redox/radical)
- 🔴 TDM เจาะผิดเวลา — เจาะก่อน steady state / peak ตอนควร trough → ปรับ dose ผิด
- 🔴 chain of custody หลุด → ผลถูกแต่ใช้ในศาลไม่ได้
- 🔴 specimen ผิดชนิด — volatile (alcohol/CN) เก็บ tube เปิด/gel = ระเหย/ดูดซับ · tacrolimus ใช้ serum (ควร whole blood) · phenytoin ใน gel tube
- 🔴 plasma ChE false-low จากตับวาย → วินิจฉัย OP เกินจริง — ดู RBC-AChE + baseline
- 🔴 BAL กับ Cd / Na-EDTA กับ Pb → เพิ่มพิษไต / hypocalcemic tetany
- 🔴 corrosive ingestion → ทำให้อาเจียน/neutralize = re-expose หลอดอาหาร/เกิดความร้อน → ห้าม; เจือจางด้วยน้ำ/นม
- 🔴 organochlorine ชัก → ให้ epinephrine = myocardial irritability (ห้าม); ใช้ diazepam/phenobarbital

> NOTE: ความรู้พื้นฐาน (LD50 class, ADME, drug/metal/plant lists, TLC method) → ดู "ตำรา/แหล่งอ้างอิงมาตรฐาน"

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติม cutoff/ref-range ของ analyzer + protocol confirm ที่ห้องแลบของคุณใช้จริง (เครื่อง/reagent อะไร)
> เติม antidote/chelator stock + dosing protocol + ช่องทางปรึกษาศูนย์พิษวิทยาในพื้นที่ของคุณ
> เติม cross-react list ของ immunoassay kit ที่ใช้จริง + ยา/อาหารท้องถิ่นที่เคยทำให้ false positive

---
*skill นี้เป็นเครื่องช่วยคิดเพื่อการศึกษาสำหรับงาน clinical/forensic toxicology เท่านั้น ไม่ใช่คำสั่งทางการหรือตัวตัดสินใจแทนผู้ป่วย/ผู้เชี่ยวชาญ การให้ antidote/chelator ผิด = อันตรายถึงชีวิต ผล screen-positive ต้อง confirm ก่อนเสมอ ทุกการตัดสินใจต้องทำตาม protocol ของหน่วยงาน + ยืนยันกับแพทย์/ศูนย์พิษวิทยาก่อนปฏิบัติจริง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*


<!-- ═════════ skill: what-skill-do-i-need ═════════ -->

---
skill: what-skill-do-i-need
title: รู้ว่าต้องการ skill อะไร (What Do You Actually Need)
type: ADVISE               # ช่วยวินิจฉัย/ชี้ทาง ไม่ได้รันอะไร
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยวินิจฉัยว่าคุณต้องการอะไร เพื่อการศึกษา/ช่วยคิด — เป็นการชี้ทาง ไม่ใช่คำตอบสุดท้าย/คำสั่งทางการ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# รู้ว่าต้องการ skill อะไร

คุณบอกปัญหา/สิ่งที่อยากทำ → มันช่วยหา **"สิ่งที่คุณต้องการจริงๆ"** (ซึ่งมักไม่ใช่สิ่งที่คุณขอตอนแรก)

> **กฎ #1: อย่าเชื่อสิ่งที่ขอ — ขุดเป้าหมายจริงก่อน (ถาม "ทำไม" 2-3 ชั้น) แล้วค่อยชี้ว่าต้องการอะไร.** ดักให้ได้ว่าคำขอนั้นเป็น "ทางออกที่เขาเดาเอง" หรือ "ปัญหาจริง" (เช่นขอ "skill ทำกราฟ" ทั้งที่ติดตรง "ตั้งโจทย์วิจัยไม่เป็น"). เหมือนหมอไม่จ่ายยาตามที่คนไข้ขอ แต่วินิจฉัยก่อน.
> **กับดักที่ลึกกว่า: ไม่ใช่ทุก "ช่องว่าง" คือ skill.** คำว่า "ผมต้องการ skill X" ฟังดูเป็น knowledge gap เสมอ — แต่จริงๆ อาจเป็น tool gap / action gap (รู้แล้วแต่ไม่ทำ) / motivation-time gap. เช็ค: **"ถ้าได้ความรู้นี้ครบ จะทำได้เลยไหม?" ถ้าตอบ "รู้พออยู่แล้ว แค่ยังไม่ลงมือ/ติดเครื่องมือ/ไม่มีเวลา" → ไม่ใช่ skill gap อย่าหา skill มาแก้.**

## ใช้เมื่อ
รู้ว่าติดอะไรบางอย่างแต่ไม่รู้จะหาอะไรมาช่วย, หรือกำลังจะหา/สร้าง skill แต่ไม่แน่ใจว่าใช่อันที่ต้องการ

## วิธีใช้
วาง skill นี้ + พิมพ์ *"ช่วยหาหน่อยว่าผมต้องการอะไร: [เล่าสิ่งที่อยากทำ/ที่ติด]"* → ตอบคำถามที่ AI ถามทีละข้อ

---

## วิธีวินิจฉัย (AI: ทำตามนี้ ทีละขั้น)

### ขั้น 1 — รับ "สิ่งที่คุณคิดว่าต้องการ" แต่ยังไม่เชื่อทันที
- ถาม: **คุณกำลังพยายามทำอะไรให้สำเร็จจริงๆ (outcome)** ไม่ใช่ "เครื่องมือที่คิดว่าต้องใช้"
- ถาม "ทำไม" เบาๆ 2-3 ชั้น จนถึงเป้าหมายจริง (เช่น อยากได้กราฟ → ทำไม → ทำวิจัย → ทำไม → เลื่อนระดับ)

### ขั้น 2 — แยกประเภทของ "สิ่งที่ขาด" (สำคัญสุด — ไม่ใช่ทุกอย่างคือ skill)
- **เทสต์ตัดสิน 1 ข้อ:** *"สมมติได้ความรู้นี้ครบมือพรุ่งนี้ — ทำสำเร็จได้เลยไหม?"* ถ้า **ไม่** → ตัวที่ขาดจริงอยู่แถวล่างของตาราง ไม่ใช่ skill
| ขาดอะไร | จริงๆ ต้องการ |
|---|---|
| ความรู้/วิธีคิด | **skill** (ความรู้) — ใช่เคสที่มาถูกที่ |
| การลงมือ (รู้แล้วแต่ไม่ทำ) | **เริ่มทำ** — ไม่ต้องหา skill มาผัด |
| เครื่องมือ/โปรแกรม | **tool/software** ไม่ใช่ skill |
| ความเชี่ยวชาญเฉพาะ/ความเสี่ยงสูง | **คนจริง** (ผู้เชี่ยวชาญ) — เกินขอบเขต skill |
| เวลา/พลัง/แรงจูงใจ | ปัญหาคนละแบบ (ไม่ใช่ knowledge gap) → ดู skill โค้ช/จัดเวลา |

### ขั้น 3 — ถ้าเป็น skill จริง → ระบุให้ชัดว่า skill อะไร
- จาก **เป้าหมาย + จุดที่ติด** → ชี้ความสามารถ/skill ที่ตรงที่สุด
- ถ้ามีในคลัง skill อยู่แล้ว → ชี้ตัวนั้น; **ถ้ายังไม่มี → "นี่คือ skill ที่ควรมีแต่ยังไม่มี"** (= ช่องว่าง จดไว้สร้าง)
- **AI: ปกติแชตธรรมดาคุณ "มองไม่เห็น" คลัง skill ของ user — ถ้ามองไม่เห็น อย่าเดาชื่อตัวที่มี ให้ขอ user วางรายชื่อ/แคทตาล็อก skill มาก่อน หรือระบุเป็น "ความสามารถที่ต้องการ" แบบกลางๆ แทนชื่อ skill เฉพาะ** (กันขั้นนี้ fail เงียบๆ)

### ขั้น 4 — เช็คว่าเป็น skill เดียว หรือหลายอันต่อกัน
- งานใหญ่มักต้อง **หลาย skill เรียงกัน** (เช่น ทำวิจัย = ตั้งโจทย์ → methodology → สถิติ → เขียน)
- ชี้ **ลำดับ + อันที่ติดอยู่ตอนนี้** เพื่อให้เริ่มถูกจุด ไม่กระโดดข้าม

---

## กับดัก (Anti-patterns)
- **เชื่อ "สิ่งที่ขอ" ทันที** โดยไม่ขุดต้นเหตุ → แก้ผิดจุด (ให้กราฟ ทั้งที่ปัญหาคือโจทย์วิจัย)
- **ยัดทุกอย่างเป็น "skill"** — บางอันแค่ต้องลงมือ / ต้องใช้ tool / ต้องถามคน
- **หา skill มาเป็นข้ออ้างผัดการลงมือ** — "ขอเรียนรู้ให้พร้อมก่อน" ทั้งที่รู้พอจะเริ่มแล้ว
- **ชี้ skill เดียว ทั้งที่งานต้องหลายอันต่อกัน** → ติดอยู่กลางทางเพราะข้ามขั้น

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมจากคนที่เคยช่วยคนอื่นวินิจฉัยจริง เช่น:
> - *"พอคนบอกว่าอยากได้ X จริงๆ เขามักหมายถึง Y เพราะ..."*
> - *"สัญญาณว่ามันไม่ใช่ knowledge gap แต่เป็น motivation/time gap คือ..."*

---
*ช่วยชี้ทางว่าคุณต้องการอะไร เพื่อการศึกษา/ช่วยคิด — เป็นการวินิจฉัยเบื้องต้น ไม่ใช่คำตอบสุดท้าย/คำสั่งทางการ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
