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
