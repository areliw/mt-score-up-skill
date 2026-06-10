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
> ⚠️ **กับดักที่ #1: ข้อมูลจับคู่ (ก่อน-หลังคนเดียวกัน / 2 วิธีวัด sample เดียวกัน / ตา 2 ข้างคนเดียว) ต้องใช้ paired test (paired t / Wilcoxon signed-rank / McNemar) — ตัดสินจาก design ไม่ใช่หน้าตาข้อมูล (paired/unpaired เป็น "2 คอลัมน์" เหมือนกัน) ใช้ unpaired ทั้งที่ข้อมูล paired = ผิดบ่อยสุด ผลเพี้ยน**

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
- **paired vs unpaired ตัดสินจาก design ไม่ใช่หน้าตาข้อมูล** — ถ้าแต่ละแถวคือ "หน่วยเดียวกันวัด 2 ที" (ก่อน-หลัง / 2 วิธีวัด sample เดียว / ตา 2 ข้างคนเดียว) = paired (paired t / Wilcoxon signed-rank / McNemar)
- **method comparison ≠ การ validate เครื่องสำหรับใช้จริงกับผู้ป่วย** → ต้องมี acceptance criteria (เช่น CLSI EP09) + ผู้รับผิดชอบ lab อนุมัติ ก่อนนำเครื่อง/วิธีไปใช้จริง

---

## เกินขอบเขต → ปรึกษาคนจริง
ถ้าเจอ: repeated measures หลายเวลา, survival/time-to-event, multilevel/clustered data, sample size calculation ก่อนเก็บ, design ที่ซับซ้อน → **ปรึกษานักสถิติ** อย่าเดา

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติม war-story/วิจารณญาณจริง เช่น:
> - *"เคสที่ reviewer ตีกลับเพราะ... ผมแก้โดย..."*
> - *"ข้อมูล lab แบบนี้ผมเห็นปุ๊บรู้เลยว่าต้องระวัง..."*
> - *"test ที่ตำราบอกใช้ได้ แต่ในงานจริง MT ผมเลี่ยงเพราะ..."*

*(— ส่วนนี้แหละที่ทำให้ skill เป็น "มรดก" ไม่ใช่แค่ตำรา)*

---

*⚠️ เครื่องมือช่วยเลือก/รัน/แปลผลสถิติเพื่อการศึกษา — ไม่ใช่ที่ปรึกษาสถิติทางการ ควรตรวจสอบความเหมาะสมและการแปลผลกับนักสถิติ/ผู้เชี่ยวชาญก่อนนำไปใช้/ตีพิมพ์/ตัดสินทางคลินิก · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
