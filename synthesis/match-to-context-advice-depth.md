---
thesis: match-to-context-advice-depth
title: ความลึกของคำแนะนำต้อง match สถานะคน ไม่ใช่ "เปิดทุกชั้นตลอด"
status: draft
signals: 4
confidence: medium
date: 2026-06-24
feeds: mt-career-judgment
---

# ความลึกของคำแนะนำต้อง match สถานะคน ไม่ใช่ "เปิดทุกชั้นตลอด"

> **หมายเหตุชนิด:** thesis นี้เป็น **system read** (เรื่อง *hub ควรส่งคำแนะนำยังไง*) — ต่างจาก
> [value-capture](value-capture-mt-labor-market.md) ที่เป็น **domain read** (เรื่อง *โลก MT เป็นยังไง*).
> synthesis/ เก็บ cross-signal read ที่ atom ไม่ถือ — ทั้งสองชนิด.

## Claim
คุณภาพคำแนะนำ **ไม่ได้**มาจาก "ใส่ judgment/structure/strategy ให้มากที่สุด" — มันมาจาก
**match ความลึกกับสถานะการตัดสินใจของคนถาม**. ชั้นความรู้ที่มากขึ้น (skill → synthesis → meta-rule)
ช่วยเมื่อคน *มีพื้นที่ไตร่ตรอง* แต่ **ทำร้าย**เมื่อคน *กำลัง panic หรือ ข้อมูลพอแล้วต้องฟันธง*
(= overload + ลังเลเกิน). "more ≠ better."

## หลักฐาน (cross-signal, 2026-06-24)
- **Ablation 3 เคส MT จริง (base vs +skill vs +skill+synthesis), judge blind วัด decision-usefulness:**
  - เคส**ไตร่ตรอง** — "ไม่บรรจุ 10 ปี" · "หัวหน้า toxic" → **+synthesis ชนะ** (structural reframe ปลดล็อกการตัดสินใจ)
  - เคส**เร่งด่วน/panic** — "จบใหม่ 8 เดือน เครียดกลัวไม่มีงาน" → **base ชนะ · +synthesis โหล่** (judge: ยัด value-capture strategy = เพิ่มภาระตัดสินใจคนกำลัง panic แทนจะลด)
- **Non-circular test ของ self-mirror rule (judge blind, decision-quality):** ช่วย strategy (SC 2/2) **แต่ control case "ข้อมูลพอควรฟันธง" → WITH HURTS (over-cautious)** = ชั้น meta ที่เพิ่ม "ความคิด" ทำร้ายเมื่อควร "ลงมือ"
- รูปแบบตรงกันทั้งสอง test: **depth ต้อง match context**

## นัย
- **ระดับ hub/router:** ก่อนยิงคำตอบเต็มชั้น → อ่าน **สถานะคนถาม** ก่อน: *panic/เร่งด่วน/ข้อมูลพอ = action คม สั้น ฟันธง* · *หลงทาง/strategy/มีเวลา = structural reframe + ทางเลือก*. triage ควรมี signal นี้ ไม่ใช่ "เปิดทุก skill+thesis เสมอ"
- **ต่อ self-mirror rule:** failure mode (over-caution) = match-to-context พังทิศ "ใส่ doubt ตอนควรกล้า" → scope-guard เวอร์ชันหน้าควรเป็น **context-detection** ไม่ใช่แค่ task-type
- **ต่อ `mt-career-judgment`:** เพิ่ม sensibility **"เจอคน panic → triage action ก่อน strategy"** (อาจเป็น meta-fork)

## คำถามเปิด
- detect สถานะคน (panic / confident / lost) จาก text เดียว ทำได้แม่นแค่ไหน?
- n เล็ก (4 signal) — อาจมีข้อยกเว้น (บางคน panic แต่ต้องการความจริงเชิงโครงสร้างเพื่อสงบ?)
- corroborate ต้องการ signal-set **อิสระ** (เคสจริงนอก ablation ชุดนี้ · A/B ที่ tag user-state)
