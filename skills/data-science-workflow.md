---
skill: data-science-workflow
title: เดินโปรเจกต์ Data Science ตาม CRISP-DM (Data Science Workflow)
type: ADVISE               # ช่วยนำทาง phase + ตัดสินใจ ไม่ได้รันโมเดลให้
needs: any                 # ใช้ได้ทุก AI · เต็มที่สุดกับ AI ที่รัน code/tool ได้
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-08
status: draft
disclaimer: "ช่วยวางลำดับงานและตัดสินใจในโปรเจกต์ data science ไม่ใช่คำแนะนำทางการแพทย์ — ผลโมเดล/การวิเคราะห์ต้อง validate ก่อนนำไปใช้กับคนไข้/งานจริงเสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# เดินโปรเจกต์ Data Science ตาม CRISP-DM

จะทำโปรเจกต์ data science แล้วงงว่า "ตอนนี้อยู่ตรงไหน · ทำอะไรต่อ · เมื่อไหร่ต้องวนกลับ" → โค้ชนี้เป็น **แผนที่ phase ทั้งโปรเจกต์** ตอบว่า **"อยู่ phase ไหนของ CRISP-DM"** กับ **"loop กลับเมื่อไหร่"** ไม่ใช่ที่ท่องนิยาม

> **กฎข้อ 1:** ห้ามข้าม **Business/Clinical Understanding** ไปจับ data/โมเดลก่อน — ถ้ายังตอบไม่ได้ว่า "ผลที่ใช้ได้จริงหน้าตายังไง ใครเอาไปใช้ ตัดสินใจอะไร" แปลว่ายังไม่พร้อมเข้า phase ถัดไป · เริ่มผิด phase = ได้ solution ที่ไม่มีปัญหารองรับ
> **กับดักข้อ 1:** **CRISP-DM ไม่ใช่เส้นตรงเดินครั้งเดียวจบ** — มันวนได้ทุกขั้น. เจอ data ไม่พอ / leakage / โมเดลตอบโจทย์ธุรกิจไม่ได้ ต้อง **ถอยกลับ phase ก่อน** ไม่ใช่ดันต่อทั้งที่ฐานพัง.
> นิยาม/สูตรแต่ละ phase ตำรา/AI มีหมดแล้ว — ที่ทำให้โปรเจกต์ล้มจริงคือ **รู้ผิดว่าอยู่ phase ไหน** กับ **ไม่ยอม loop กลับ** · skill นี้เก็บสองอันนั้น
> เลือกโมเดล/metric/validation ดู `ml-judgment` · กันโปรเจกต์ล้ม/ประเมิน vendor/scope ดู `data-project-survival` · งานซ้ำๆ ที่ควรให้ script/automation ทำดู `offload-to-automation`

## ใช้เมื่อ
- เริ่มโปรเจกต์ data science / วาง pipeline แล้วไม่รู้ลำดับงาน
- ติดอยู่กลางโปรเจกต์ ไม่แน่ใจว่าตอนนี้ควรทำอะไรต่อ หรือควรถอยกลับ
- จะแปลง "โจทย์ธุรกิจ/คลินิก" → "โจทย์ที่วัดได้สำหรับโมเดล"
- ต้องตัดสินใจช่วง data prep (เติม missing แบบไหน, scale ยังไง, encode ยังไง)
- โมเดลเสร็จแล้วแต่ไม่แน่ใจว่า "ดีพอใช้จริง" หรือยัง / deploy แล้วต้องเฝ้าอะไร

## วิธีใช้
วาง skill นี้ + เล่าว่าโปรเจกต์ทำอะไร อยู่ขั้นไหนแล้ว → AI จะระบุ phase ปัจจุบัน บอกสิ่งที่ต้องเคลียร์ก่อนข้ามไป phase ถัดไป และเตือนว่ากำลังเสี่ยงต้อง loop กลับตรงไหน

---

## รู้ว่าอยู่ phase ไหน (AI: ระบุ phase ก่อนแนะนำ) — 6 phase CRISP-DM

| Phase | คำถามหลักของ phase | เกณฑ์ "ผ่าน" ไป phase ถัดไป |
|---|---|---|
| 1. Business/Clinical Understanding | จะตัดสินใจอะไร ใครใช้ ผลที่ใช้ได้หน้าตายังไง | เขียน data-mining goal ที่ **วัดได้** ออกมาได้ |
| 2. Data Understanding | มี data อะไร คุณภาพแค่ไหน พอตอบโจทย์ไหม | รู้แหล่ง/ขนาด/คุณภาพ + เห็น missing/outlier เบื้องต้น |
| 3. Data Preparation | ทำความสะอาด/แปลง/รวม ให้พร้อม model | dataset สะอาด split แล้ว ไม่มี leakage |
| 4. Modeling | ลองวิธี/โมเดล + tune | มี baseline + โมเดลที่ดีกว่า baseline |
| 5. Evaluation | ดีพอ **ต่อธุรกิจ/คลินิก** จริงไหม | ผ่านเกณฑ์ที่ตั้งใน phase 1 ไม่ใช่แค่ metric สวย |
| 6. Deployment | ส่งมอบ + เฝ้าระวังหลังใช้จริง | มีแผน monitor drift + ช่องรับ feedback |

> ⚖️ ลังเลว่าอยู่ phase ไหน: ถามว่า "งานล่าสุดที่ทำเสร็จคืออะไร" แล้วเลื่อนลงทีละขั้น · ห้ามตอบ "phase 4 Modeling" ถ้ายังตอบ phase 1 ไม่ได้

## phase 1 — แปลง business goal → data-mining goal (จุดที่คนข้ามบ่อยสุด)
- business goal มักลอย ("ลดเคสพลาด", "คัดกรองเร็วขึ้น") → ต้องแปลงเป็นโจทย์โมเดลที่วัดได้
- ถามให้ครบ: **ใครใช้ผล · ตัดสินใจอะไรจากผล · ผิดพลาดแบบไหนแพงกว่า (FP vs FN) · เกณฑ์ "ดีพอใช้"**
- 🩺 ตัวอย่าง: "ช่วยคัดกรอง thalassemia carrier จาก CBC" → data-mining goal = classification (carrier/ไม่) ที่ **recall สูง** (พลาด carrier แพงกว่า false alarm) + บอก threshold ที่ยอมรับได้
- เขียน success ออกมาเป็นตัวเลข/เงื่อนไขก่อน อย่าเพิ่งแตะ data

## phase 2-3 — Data: เลือก prep ให้ตรงชนิดปัญหา (Decision forks)

### Fork A — ระบุ task type ก่อนเลือกวิธี (ทำก่อนทุกอย่าง)
- target ต่อเนื่อง (ระดับ Hb, ค่า lab) → **Regression** · target เป็นกลุ่ม (โรค/ไม่, blood group) → **Classification** · ไม่มี label หา group → **Clustering**
- ⚠️ ระบุ task ผิดตั้งแต่ต้น = เลือก metric/โมเดล/prep ผิดทั้งสาย → ดู `ml-judgment` Fork 1

### Fork B — missing แบบไหน → เติมยังไง (ดูกลไกก่อนเติม)
- **MCAR** (หายแบบสุ่มจริง) → ลบแถว/เติม mean-median ได้ ความ bias ต่ำ
- **MAR** (หายขึ้นกับตัวแปรอื่นที่มี) → เติมแบบมีเงื่อนไข (group-wise / model-based / KNN-impute)
- **MNAR** (หายเพราะค่าของมันเอง เช่นค่าสูงเกินจนไม่ถูกวัด) → ⚠️ เติมมั่วทำ bias หนัก → ต้องเข้าใจ domain / สร้าง flag "เคยหาย" / ปรึกษาคนรู้บริบท lab
- 💡 อย่าเติม missing **ก่อน** split → ค่าที่ใช้เติมต้องคำนวณจาก train เท่านั้น (ไม่งั้น leakage)

### Fork C — normalize vs standardize + encode
- **Standardize** (z-score, mean 0 sd 1) → ดีฟอลต์ตอนข้อมูลใกล้ normal / ใช้ distance-based (KNN, SVM, k-means, PCA)
- **Normalize** (min-max 0–1) → เมื่ออยากคุมช่วงค่าแน่ๆ / NN / ค่าไม่มี outlier หนัก (min-max ไวต่อ outlier)
- encode: ลำดับมีความหมาย (ระดับความรุนแรง) → ordinal · ไม่มีลำดับ (ชนิดเชื้อ, แผนก) → one-hot · cardinality สูงมาก → ระวัง one-hot บาน
- ⚠️ fit scaler/encoder บน **train fold เท่านั้น** แล้ว transform test (ใส่ใน Pipeline) — ดู `ml-judgment`

## phase 5 — Evaluation: เทียบ "คุณค่า" ไม่ใช่แค่ metric
- ผ่าน metric (F1/AUC) ≠ ผ่านโจทย์ธุรกิจ → ย้อนถาม phase 1: "ตัวเลขนี้แปลว่าเอาไปใช้ตัดสินใจได้จริงไหม"
- 🩺 recall 0.95 ดูดี แต่ถ้า precision ต่ำจน lab ต้อง confirm ตามเยอะเกินกำลัง = ใช้ไม่ได้จริง → คุยต้นทุน FP/FN กับคนใช้งาน
- เช็ค error เป็นกลุ่ม (subgroup) ไม่ใช่ค่าเฉลี่ยรวม — โมเดลอาจแม่นรวมแต่พังกับกลุ่มน้อย
- ตัดสิน go/no-go ที่นี่ ก่อนเสียแรง deploy

## เมื่อไหร่ต้อง loop กลับ (สัญญาณถอย)
- data ไม่พอ/คุณภาพแย่ตอน Modeling → ถอยไป **phase 2-3**
- เจอ **leakage** (คะแนนสวยผิดปกติ) → ถอยไป **phase 3** ซ่อม split/pipeline
- โมเดลผ่าน metric แต่ไม่ตอบโจทย์ → ถอยไป **phase 1** ทบทวน goal/metric
- หลัง deploy เจอ **concept drift** (ผลตกเมื่อข้อมูลจริงเปลี่ยน) → กลับเข้า loop ใหม่ retrain

---

## กับดัก (Anti-patterns) — พลาดตรงนี้บ่อย
- **ข้าม Business Understanding** → ได้โมเดลเท่ๆ ที่ไม่มีใครใช้ = "solution หาปัญหา" → ล็อก data-mining goal ที่วัดได้ก่อนแตะ data เสมอ
- **เริ่ม Modeling ก่อนเข้าใจ + ทำความสะอาด data** → garbage in garbage out · 60–80% ของงานคือ data prep ไม่ใช่ tune โมเดล
- **Data leakage** — เติม missing/scale/feature-select ทั้ง dataset ก่อน split, หรือใส่ feature ที่รู้ "หลัง" รู้ผลลัพธ์ → คะแนนหลอก พังจริง → split ก่อน, Pipeline fit เฉพาะ train, ตรวจ timeline ทุก feature
- **Vanity metric** — accuracy สูงบนข้อมูล imbalanced (โรคหายาก 2% → ทาย "ไม่โรค" หมดได้ acc 98% recall 0) → เลือก metric ตามต้นทุนคลินิก (ดู `ml-judgment`)
- **Over-engineering ก่อนมี baseline** — กระโดด deep net/ensemble หรูก่อน ทั้งที่ยังไม่มี baseline ง่ายๆ ไว้เทียบ → ทำ baseline เร็วก่อนเสมอ
- **เดินเส้นตรงไม่ยอม loop** — รู้ว่าฐานพัง (data ไม่พอ/leakage) แต่ดันต่อเพราะเสียดายแรง → ถอยกลับ phase ที่พังถูกกว่า
- **deploy แล้วทิ้ง** — ไม่เฝ้า drift, ไม่มีช่องรับ feedback → โมเดลค่อยๆ เพี้ยนเงียบๆ จนตัดสินใจผิด → วางแผน monitor ตั้งแต่ phase 6
- **biased training data** — data ที่เก็บมาไม่แทนประชากรจริง (เก็บจาก รพ.เดียว/กลุ่มเดียว) → โมเดลพังกับกลุ่มที่ไม่เคยเห็น → ตรวจตัวแทนของ data ตั้งแต่ phase 2

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริงในสายงานคุณ เช่น:
> - *"โปรเจกต์ที่ผมข้าม Business Understanding แล้วเจ๊ง คือ... รู้ตอน..."*
> - *"missing ในข้อมูล lab ของผมมักเป็น MNAR ตรงที่... ผมจัดการด้วย..."*
> - *"ตอนที่ผมต้อง loop กลับ phase เพราะ... สัญญาณที่จับได้คือ..."*

---
*ช่วยวางลำดับงานและตัดสินใจในโปรเจกต์ data science ไม่ใช่คำแนะนำทางการแพทย์ — ผลโมเดล/การวิเคราะห์ต้อง validate ก่อนนำไปใช้กับคนไข้/งานจริงเสมอ ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
