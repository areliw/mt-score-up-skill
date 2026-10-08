---
skill: cv-judgment
title: โค้ช Computer Vision — เลือกเทคนิคภาพให้ถูก (CV & Image Analysis Judgment)
type: ADVISE               # ช่วยตัดสินใจเลือกเทคนิค ไม่ใช่ตำราสูตร
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-10-08
status: draft
disclaimer: "ช่วยคิดเลือกเทคนิค image analysis เพื่อการศึกษา ไม่ใช่คำสั่งทางการแพทย์ — งานวินิจฉัยจากภาพ (เช่นเซลล์/สเมียร์) ต้องมี MT/แพทย์ยืนยันเสมอ ไม่ใช้ผลโมเดลตัดสินคนไข้ลำพัง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช Computer Vision — เลือกเทคนิคภาพให้ถูก

งานวิเคราะห์ภาพ (classify/segment/นับเซลล์) แล้วงงว่า "preprocess อะไร · feature ตัวไหน · classical หรือ deep" → โค้ชนี้ตอบ **"เลือกเทคนิคไหนเมื่อไหร่ + พลาดตรงไหน"**

> **กฎ #1: data น้อย/feature ชัด → classical (HOG/GLCM → SVM) ก่อนเสมอ; อย่าไป deep CNN.** Deep บน data น้อย = overfit จำไม่ generalize. **กับดัก #1: threshold "สี" ใน RGB** — เพี้ยนทันทีที่แสงเปลี่ยน → ใช้ **HSV** เมื่อสีคือ criterion.
> **กับดัก edge: "ภาพเยอะ" ≠ data เยอะ** — หลาย patch/ภาพจากคนไข้/สไลด์เดียว = data จุดเดียว → split train/test ที่ระดับ **คนไข้/สไลด์ ไม่ใช่ patch** ไม่งั้น leakage → accuracy หลอกตา.
> มีเลนพิเศษ **blood smear / cell morphology** ด้านล่าง · เลือก classifier ลึกๆ → ดู `ml-judgment`

## เครื่องมือ (รันก่อนคิดเลข)
เลขใน fork C/F + เลนเซลล์เลือด (HSV, GLCM, opening/closing) → **รันสคริปต์ก่อน แล้วค่อยใช้ judgment ข้างล่างเลือก/ตีความ** (อย่านับคู่ GLCM หรือเลือกสูตร hue ด้วยมือ) · รัน `--help` ก่อน ไม่ต้องอ่านซอร์ส · ไฟล์อยู่ใน `scripts/` ของโฟลเดอร์ skill (ใน repo: `skills/cv-judgment/scripts/`) · histogram/filter/Sobel/labeling ไม่อยู่ที่นี่ → `scripts/vision_calc.py` ของ `image-processing-judgment`
- `python scripts/cv_calc.py hsv @data/stain_two_lightings_rgb.txt --h-range 270 320 --s-min 0.2` — fork F + กับดัก #1: อ่านบรรทัด `branch` (M=r/g/b ใช้สูตรไหน; แถว M=r ต้อง mod 360) แล้วตาราง `vs pixel #1` (สีย้อมเดียวกันแสงต่าง = ระยะ RGB ~138 แต่ Δh = 0) · pixel เทา (M = m) ได้ h = 0 ตามนิยาม **ไม่ใช่สีแดง** → ใส่ `--s-min` · `--h-range 330 30` = ช่วงแดงที่วนผ่าน 0°
- `python scripts/cv_calc.py glcm @data/glcm_slide5_7x6.txt --dx 0 --dy 1 --symmetric` — fork C + เลนเซลล์ข้อ 3: อ่าน C → C_SYM → P = C/ΣC → ตารางพจน์ต่อช่อง → max prob / ASM (=Energy) / contrast / homogeneity / entropy / correlation · ตามสไลด์ GLCM: **x = แถว (ลง), y = คอลัมน์ (ขวา)** → `--dx 0 --dy 1` = เพื่อนบ้านทางขวา · `--angle 45` = ขวาบน (Haralick/MATLAB) ≠ skimage π/4 (ขวาล่าง) — สคริปต์พิมพ์คำสั่ง skimage ที่ตรงกันให้ · บรรทัดวงเล็บ `[skimage …]` = ค่าที่ไลบรารีตั้งชื่อเหมือนแต่สูตรต่าง (homogeneity ใช้ (i−j)², energy = √ASM, entropy ใช้ ln) · `--quantize 4` = 0–63/64–127/128–191/192–255 · `--given` = โจทย์ให้ GLCM มาแล้ว
- `python scripts/cv_calc.py morph @data/smear_mask_12x12.txt --op open` (เทียบ `--op close`) — เลนเซลล์ข้อ 2 + กับดัก Opening↔Closing: พิมพ์ภาพหลังแต่ละขั้น + พิกเซลที่หาย/เพิ่ม (opening ลบจุดเล็กและวงบาง · closing อุดรู เก็บจุดเล็กไว้) · dilation = แปะ SE ตามที่วาดบนทุกพิกเซล 1 · `--border zero` (นอกภาพ = 0 ตามสไลด์) ≠ `ignore` (ค่าเริ่มต้นของ skimage) ที่ขอบภาพ
- สคริปต์ = ตัวช่วยตรวจ ไม่ใช่ผู้ตัดสิน: ทุก output มีบรรทัด `ADVISORY` · ทดสอบแล้ว: `evals/test_cv_calc.py` (35 ข้อ ค่าคาดหวังจากสไลด์วิชา + Haralick 1973 Fig. 2 · must-fail control 12 ตัว: hue_without_mod_360, hue_branch_offsets_swapped, glcm_axes_swapped, glcm_offset_reversed, glcm_not_symmetrized, glcm_features_on_raw_counts, glcm_skimage_angle_map, homogeneity_squared_denominator, entropy_natural_log, opening_closing_swapped, dilation_touch_rule_mirrors_se, border_ignore_breaks_slide115)

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
- local: Harris = หา corner (rotation-invariant แต่ไม่ทน scale; ต้องการ scale+rotation → ใช้ SIFT) · **SIFT**=scale+rotation invariant แม่นสุด · **SURF**=SIFT แบบเร็ว
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
