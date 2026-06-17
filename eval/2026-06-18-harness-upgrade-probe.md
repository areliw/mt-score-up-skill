# Harness upgrade probe — control arm · selftest · correctness/specificity gates

> 2026-06-18 · proof-run ของ 3 upgrade ที่สกัดจาก [Ponytail teardown](../docs/design/study-ponytail.md)
> เข้า Layer-2 A/B harness. **n=1 trap, 1 answerer (Haiku), 1 judge (Opus)** — พิสูจน์ *กลไก* ไม่ใช่
> ผลครอบคลุม. trap = `lab-management-judgment` Fork 9 (PT/EQA-fail investigation).

## โจทย์ (discriminating trap — เลือกตัว non-obvious)
"ได้ผล PT — analyte มี bias เทียบ all-method mean. ควร recalibrate เครื่องให้ตรง all-method mean
เพื่อให้รอบหน้าผ่านไหม?" · **กับดักเฉพาะ:** ต้องเช็ค **peer/method-group ถูกไหม** (เทียบผิดกลุ่ม = bias
ลวง) + **PT commutability** ก่อน — ไม่ใช่แค่ "อย่า recalibrate มั่ว" (ชั้นทั่วไปที่ AI-เปล่ารู้แล้ว)

## Upgrade #2 — `--selftest` (verify instrument ก่อนเผา)
Opus judge ตัดสิน gold vs known-bad ที่เขียนไว้ก่อน รัน 3-arm:
| ref | helpfulness | correctness |
|---|---|---|
| gold (สอบสวน peer-group/commutability ก่อน) | 5/5 | PASS |
| known-bad (recalibrate ตาม all-method mean เพื่อผ่าน) | 0/5 | FAIL |

**spread = 5 (≥ เกณฑ์ 2) → กรรมการแยกดี/แย่ได้ชัด → เขียวให้รันจริง.** ถ้า spread < 2 = instrument
เชื่อไม่ได้ ต้อง rework trap/judge ก่อน ไม่เผา API (บทเรียน Ponytail `--selftest` known-good/known-bad).

## Upgrade #1 — control arm (delta-of-deltas)
Haiku ตอบ 3 arm (blind judge, Opus):
| arm | helpfulness | correctness | specificity (ถึง peer-group/commutability?) |
|---|---|---|---|
| baseline (null prompt) | 3/5 | PASS | NO |
| **control (generic-careful, ไม่มี judgment)** | 2/5 | PASS | NO |
| **with-skill (Fork 9)** | **5/5** | PASS | **YES** |

- Δ(skill − baseline) = **+2** · Δ(skill − control) = **+3** · Δ(control − baseline) = **−1**
- **สิ่งที่ control arm เผย (2-arm เดิมมองไม่เห็น):** "สั่งให้รอบคอบ" เปล่าๆ **ไม่ช่วย** (−1, ในระดับ noise)
  → lift ของสกิล = **judgment เฉพาะ (peer-group/commutability) ไม่ใช่แค่ system-prompt ใดๆ ทำให้ระวังขึ้น**.
  ถ้าวัดแค่ skill vs baseline (+2) จะแยกไม่ออกว่า lift มาจากตัว judgment หรือแค่ "มี framing"

## Upgrade #3 — correctness gate แยกจาก helpfulness (+ specificity)
- **correctness (binary):** ทั้ง 3 arm = PASS (ไม่มีใครแนะนำ recalibrate มั่ว) → trap นี้ "ปลอดภัยทุก arm"
- แต่ **helpfulness 0-5 + specificity (binary)** จับความต่างได้: มีแค่ with-skill ที่ส่ง senior judgment จริง
- บทเรียน: **3 axis จับคนละอย่าง** — correctness กันอันตราย · helpfulness วัดคุณภาพรวม · specificity วัด
  "ส่ง judgment ที่สกิลอ้างว่าให้ไหม". เคสที่ correctness ผ่านหมด (อันตรายต่ำ) ยังวัดค่าสกิลได้ด้วย 2 axis หลัง
  → แก้ปัญหา "tie" ของ probe textbook รอบก่อน (donor/IPC) ที่ helpfulness อย่างเดียวแยกไม่ออก

## Verdict + caveat
กลไกทั้ง 3 ทำงานจริง บน trap ที่ discriminate. **caveat:** n=1, model เดียว, single draw — นี่คือ proof-of-
mechanism. ก่อนใช้ promote: รัน median ≥10 reps × ทุก fork+anti (full fan-out) ตาม `feedback_adjust_then_ab_test_hard_cases`.
