---
skill: cv-judgment
title: โค้ช Computer Vision — เลือกเทคนิคภาพให้ถูก (CV & Image Analysis Judgment)
type: ADVISE               # ช่วยตัดสินใจเลือกเทคนิค ไม่ใช่ตำราสูตร
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
reviewed: 2026-06-01
status: draft
disclaimer: "ช่วยเลือกเทคนิค image analysis + เลี่ยงกับดัก — งานวินิจฉัยจากภาพ (เช่นเซลล์/สเมียร์) ต้องมี MT/แพทย์ยืนยันเสมอ ไม่ใช้ผลโมเดลตัดสินคนไข้ลำพัง"
---

# โค้ช Computer Vision — เลือกเทคนิคภาพให้ถูก

งานวิเคราะห์ภาพ (classify/segment/นับเซลล์) แล้วงงว่า "preprocess อะไร · feature ตัวไหน · classical หรือ deep" → โค้ชนี้ตอบ **"เลือกเทคนิคไหนเมื่อไหร่ + พลาดตรงไหน"**

> สูตร convolution/filter ตำรามีหมด — ส่วนที่ทำให้พังคือ **เลือกผิดจากนิสัยเดิม** (เช่น threshold สีใน RGB, ใช้ deep ทั้งที่ data น้อย). มีเลนพิเศษสำหรับ **blood smear / cell morphology** (สาย blood-group / thalassemia)
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
- **overfit ภาพชุดเล็ก** — deep บนภาพ <~500/class → จำไม่ generalize; แยก train/test ระดับ **ภาพ/คนไข้** ไม่ใช่ patch (leakage)
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
*ช่วยเลือกเทคนิค image analysis + เลี่ยงกับดัก — งานวินิจฉัยจากภาพ (เซลล์/สเมียร์) ต้องมี MT/แพทย์ยืนยันเสมอ ไม่ใช้ผลโมเดลตัดสินคนไข้ลำพัง*
