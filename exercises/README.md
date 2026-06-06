# แบบฝึก — ลองเองแล้วเทียบ

วิธีฝึก: อ่านโจทย์ → ถาม AI **ของคุณเองก่อน (ยังไม่วาง skill)** → แล้วค่อยวาง skill ที่ระบุ ถามซ้ำ → เทียบ. กับดักเฉลยอยู่ **ท้ายไฟล์** (อย่าเพิ่งแอบดู) โจทย์ทั้งหมดเป็นสถานการณ์สมมุติ

> โจทย์ชุดนี้คือชุดเดียวกับที่ใช้ทดสอบ skill จริง — เก็บไว้ที่ [`eval/round3/scenarios.json`](../eval/round3/scenarios.json) (มี 53 โจทย์)

---

### แบบฝึก 1 — `choose-stat-test`
นักวิจัยวัดค่าวิเคราะห์เดียวกันจากผู้ป่วย 30 คน ด้วยเครื่อง 2 เครื่อง (เครื่อง A กับ B) อยากรู้ว่า "ผลต่างกันไหม". เขาจะรัน two-sample t-test เทียบ 30 ค่าของ A กับ 30 ค่าของ B. ถูกไหม? ควรทำอะไร?

### แบบฝึก 2 — `immunoassay-judgment`
หญิงตั้งครรภ์ มีผื่นทั่วตัว ฝ่ามือฝ่าเท้า + แผลในปาก สงสัย secondary syphilis. แต่ผล RPR (non-treponemal) ออกมา **ลบ**. จะรายงาน "ไม่พบหลักฐานซิฟิลิส" เลยไหม?

### แบบฝึก 3 — `ml-judgment`
ทีมสร้างโมเดลทำนาย ได้ AUC 0.97 สวยมาก variance ต่ำทุก fold. เขา impute + standardize + SMOTE **ก่อน** แบ่ง train/test และมี feature ชื่อ `review_turnaround_minutes` (ติด top-3). จะ sign-off ให้ขึ้น production ไหม? คาดว่าเลขจริงเท่าไร?

### แบบฝึก 4 — `clinmicro-judgment`
ผู้ป่วย ICU มี central line ไข้สูง WBC พุ่ง. เจาะ hemoculture 2 ขวดจาก 2 ตำแหน่ง. **ขวดเดียว** ขึ้น coagulase-negative staph (CoNS), อีกขวด no growth. หมอเร่งให้รายงานเป็น CRBSI + เดิน vancomycin + ถอดสาย. คุณรายงานยังไง?

---
<details>
<summary><b>เฉลยกับดัก (กดเปิดหลังลองเอง)</b></summary>

1. **ผิด — ข้อมูล paired** (วัดผู้ป่วยคนเดียวกัน 2 เครื่อง) → ใช้ paired test บนผลต่างรายคน; และจริงๆ คำถาม "ตรงกันไหม" = method comparison → **Bland-Altman + ICC** ไม่ใช่ hypothesis test
2. **อย่าเพิ่งตัดออก — prozone** (Ab สูงมากจน lattice ไม่เกิด → ลบลวง) → **เจือจางแล้วทดสอบซ้ำ** ก่อนรายงาน
3. **อย่า sign-off — data leakage** (preprocess/SMOTE ก่อน split + `review_turnaround_minutes` = target leak) → ย้ายทุกอย่างเข้า CV fold, ตัด feature รั่ว, **คาดเลขจริงใกล้ baseline ~0.83 ไม่ใช่ 0.97**
4. **1/2 ขวด CoNS = น่าจะปนเปื้อน** ไม่ใช่ CRBSI (ต้อง ≥2 ขวด/sets บวก หรือดู differential time-to-positivity) → อย่าเพิ่งถอดสาย, เจาะซ้ำ, หาแหล่งติดเชื้อจริง

</details>

> อยากเข้าใจว่าทำไม skill ช่วยตรงนี้ → ดู [`examples/`](../examples) (before/after) + [`eval/`](../eval)
