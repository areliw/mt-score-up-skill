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
> **กับดัก #1:** **accuracy บน imbalanced หลอก** (โรคหายาก 2% → ทาย "ไม่โรค" หมด = acc 98% recall 0) → ใช้ precision/recall/F1 และ **PR-AUC** (ภายใต้ imbalance หนัก ROC-AUC สูงก็ยังหลอกได้ — PPV ร่วงตาม prevalence)
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
- 🎯 Ridge(L2) = หด w ไม่ถึง 0 (ดีกับ multicollinearity) · Lasso(L1) = ดัน w เป็น 0 = แถม feature selection — ⚠️ feature correlate กันสูง Lasso จะเก็บตัวเดียวทิ้งที่เหลือ (เลือกตาม data/path ไม่ใช่สุ่มแท้) → ถ้าอยากเก็บกลุ่ม correlated ใช้ **Elastic Net** (L1+L2)/Ridge

### Fork 4 — metric ไหน? (จุดพลาดเยอะสุด)
- Classification **balanced** → accuracy พอ
- Classification **IMBALANCED** (โรคหายาก, variant 2%) → accuracy **หลอก** → ใช้:
  - **Precision** = ทายว่าป่วยแล้วป่วยจริงแค่ไหน (เน้นเมื่อ false-positive แพง)
  - **Recall/Sensitivity** = ผู้ป่วยจริงจับได้แค่ไหน (เน้นเมื่อ false-negative แพง — screening)
  - **F1** = สมดุล precision/recall เมื่อไม่รู้จะหนักข้างไหน
  - **PR-AUC (precision-recall)** = ซื่อสัตย์สุดตอน imbalance หนัก เพราะไวต่อ performance บน **positive/minority class** — ⚠️ **ROC-AUC สูงไม่ได้แปลว่าใช้ได้จริงตอน imbalance**: AUC แทบไม่ขึ้นกับสัดส่วน class (ranking metric) แต่ค่า "สูง" อยู่ได้พร้อมกับ **precision/PPV ที่ร่วงเพราะ prevalence ต่ำ** → severe imbalance ดู **PR-AUC เป็นหลัก**, ROC-AUC อ่านประกอบได้ ไม่ใช่ตัวตัดสิน
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
