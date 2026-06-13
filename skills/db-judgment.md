---
skill: db-judgment
title: โค้ช SQL + ออกแบบ DB — ตัดสินใจถูก + ไม่ระเบิด (SQL & DB Judgment)
type: ADVISE               # ช่วยตัดสินใจออกแบบ/เขียน query ไม่ใช่ตำรา syntax
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: semi-stable
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
- **UNION vs UNION ALL:** default **`UNION ALL`** (ต่อตรงๆ เร็ว) · ใช้ `UNION` (sort+dedup, แพง) เฉพาะเมื่อ "ต้องการตัดซ้ำจริง" — ส่วนมากไม่ต้อง
- **transaction isolation:** เขียนเงิน/สต็อก/ผล lab ที่ห้ามเพี้ยน → ดัน isolation สูง (Serializable/Repeatable Read) · รายงานอ่านอย่างเดียว → Read Committed พอ · transaction **ยิ่งสั้นยิ่งดี** (ถือ lock นาน = deadlock/คอขวด)
- **query plan:** **full table scan = ธงแดง** บน table ใหญ่ (ควรเป็น index seek)

## กับดัก (Anti-patterns) — ระเบิดงานจริง
- **`UPDATE`/`DELETE` ไม่มี `WHERE`** = ล้างทั้งตาราง → `SELECT * WHERE <เงื่อนไขเดียวกัน>` ดูแถว+นับก่อนเสมอ / ครอบ transaction
- **`WHERE` มีแล้วแต่ยังพัง:** `NOT IN (subquery)` แล้ว subquery มี `NULL` แม้ตัวเดียว → ทุกแถวถูกตัด (ตรงค่า=FALSE, ไม่ตรง=UNKNOWN เพราะ NULL) → query/DELETE/UPDATE คืน **0 แถวเงียบๆ** (ได้*น้อยไป* ไม่ใช่โดนเกิน) → ใช้ **`NOT EXISTS`** + ยืนยันด้วย SELECT-preview ใน transaction
- **`SELECT *`** → ดึงเกิน + พังเมื่อ schema เปลี่ยน → ระบุคอลัมน์
- **JOIN ลืมเงื่อนไข** → **cartesian product** (row ระเบิด m×n)
- **GROUP BY:** ทุกคอลัมน์ใน SELECT ที่ไม่ใช่ aggregate ต้องอยู่ใน GROUP BY
- **COUNT หลัง JOIN** → row ซ้ำทำให้นับเกิน → `COUNT(DISTINCT ...)` หรือนับก่อน join
- **N+1 query** (loop ยิง query ทีละ row) → batch เป็น query เดียว / join
- **over-index** → write ช้าลงทุก index · index คอลัมน์ค่าน้อย cardinality = ไร้ประโยชน์
- **SQL injection** จากต่อ string → ใช้ parameterized query เสมอ
- **NULL ใน aggregate:** `AVG`/`SUM`/`COUNT(col)` ข้าม NULL เงียบๆ → รู้ว่ามี NULL ไหม
- **`UNION` แทน `UNION ALL` โดยไม่ตั้งใจ** → เสีย cost sort+dedup ทุก query ทั้งที่ไม่มีซ้ำ → ใช้ `ALL` เป็น default
- **`OFFSET` ลึกๆ ช้า** → `LIMIT 20 OFFSET 100000` ยังต้องสแกน+ทิ้ง 100k แถว → ใช้ **keyset/seek pagination** (`WHERE id > last_id`) บนตารางใหญ่
- **หลาย statement ที่ต้อง consistent** → ครอบ **transaction** (atomic) · transaction สั้น, ห้ามถือ lock คร่อม I/O ภายนอก (เผลอ block ทั้งระบบ)

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
