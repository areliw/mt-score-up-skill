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
