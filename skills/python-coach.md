---
skill: python-coach
title: โค้ช Python — เลือกถูก + ไม่ตกหลุม (Python Judgment & Gotchas)
type: ADVISE               # ช่วยตัดสินใจ/ดีบัก ไม่ใช่ตำรา syntax
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: stable
disclaimer: "ช่วยคิด+จับกับดัก Python ระดับเริ่ม→กลาง เพื่อการศึกษา — ไม่ใช่ตำรา syntax หรือคำสั่งทางการ ควรทดสอบโค้ดจริงและตรวจผลก่อนนำไปใช้ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช Python — เลือกถูก + ไม่ตกหลุม

เขียน/ดีบัก Python แล้วงงว่า "ใช้อะไรดี" หรือ "ทำไมพัง" → โค้ชนี้ช่วย **เลือกเครื่องมือให้ถูก + โทษบั๊กให้ถูกจุด**

> **กฎข้อ 1 (จำให้ขึ้นใจ): method ที่แก้ของ in-place คืน `None` ไม่ใช่ค่าที่แก้แล้ว.** `.sort()`/`.reverse()`/`.append()`/`.update()`/`.extend()` → คืน `None` ทั้งหมด. ดังนั้น **ห้ามเอาผลของมันไป assign หรือ chain ต่อ** — `x = lst.sort()` ทำให้ `x` เป็น None เงียบๆ, `lst.append(y).append(z)` พังทันที. อยากได้ค่าที่แก้แล้ว: เรียก method (มันแก้ตัวแปรเดิมให้) **แล้วใช้ตัวแปรเดิม** หรือใช้ฟังก์ชันที่ "คืนค่าใหม่" เช่น `sorted(lst)`, `reversed(lst)`, `lst + [y]`.
> **ตัวแยกง่ายๆ:** ชื่อเป็นกริยาแก้ของ (sort/append/update/reverse) → in-place คืน None · ชื่อบอกผลลัพธ์ (sorted/reversed) → คืนค่าใหม่ เอาไป assign ได้.
>
> Google/AI มี syntax ให้หมดแล้ว — ที่พลาดจริงคือ (1) เลือก data structure/วิธีผิด (2) ตกกับดักที่ "ดูถูกแต่พัง". skill นี้เก็บสองอันนั้น ไม่ใช่ตำรา

## ใช้เมื่อ
- เขียน/ดีบัก Python (เรียน, coursework, งาน data)
- ลังเล "ใช้ list หรือ dict ดี", "loop หรือ comprehension"
- code พัง/ผลเพี้ยน หาไม่เจอว่าผิดตรงไหน

## วิธีใช้
วาง skill นี้ + วางโค้ด/พิมพ์ปัญหา → AI ชี้ตัวเลือกที่เหมาะ + จุดที่เสี่ยงตกหลุม

---

## เลือกอะไรเมื่อไหร่ (Judgment)
- **data structure:** เรียงลำดับ+ซ้ำได้ → **list** · lookup ด้วย key O(1) → **dict** · unique + เช็คสมาชิก O(1) → **set** · ค่าคงที่/immutable/เป็น key → **tuple** · (เก็บคำไม่ซ้ำ → `set` เร็วกว่า `if x not in list` ซึ่งเป็น O(n²))
- **loop vs comprehension:** แปลง/กรองง่ายๆ → comprehension · มี side-effect/ซับซ้อน/หลายขั้น → for loop (อ่านง่ายกว่า)
- **string ต่อกันใน loop:** ใช้ `"".join(parts)` ไม่ใช่ `s += x` (O(n²))
- **อ่านไฟล์:** `for line in fh:` (streaming, ไฟล์ใหญ่) vs `.readlines()` (โหลดทั้งหมดเข้า RAM)
- **pure python vs pandas (DS):** ตาราง/คำนวณทั้งคอลัมน์ → pandas (vectorize) · ข้อมูลเล็ก/stream/logic ซับซ้อน → python · **อย่า loop ทีละ row ใน DataFrame** (ใช้ vectorized op)
- **เทียบค่า:** `==` (ค่าเท่า) · `is` (วัตถุตัวเดียวกัน) → ใช้ `is` เฉพาะกับ `None`

## กับดัก (Anti-patterns) — เช็คก่อนโทษที่อื่น
- **method แก้ของ in-place คืน `None`** — ทั้งตระกูล `.sort()` `.reverse()` `.append()` `.extend()` `.update()` `.add()` → `x = lst.sort()` ได้ None เงียบๆ, chain `lst.append(a).sort()` พัง (`'NoneType' has no attribute`). อยากได้ค่า: ใช้ตัวแปรเดิมหลังเรียก หรือใช้ `sorted()`/`reversed()`/`lst+[a]` ที่คืนค่าใหม่ *(กับดักอันดับ 1 ของมือใหม่)*
- **loop variable ค้างหลัง loop:** จบ `for line in fh:` แล้ว `line` = บรรทัดสุดท้าย → `print(line)` พิมพ์ตัวสุดท้ายไม่ใช่ผลรวม *(บั๊กคลาสสิกตอนวนอ่านไฟล์แล้วนับคำ)*
- **mutable default arg:** `def f(x=[])` → list แชร์ข้าม call ทุกครั้ง → ใช้ `x=None` แล้ว `if x is None: x=[]`
- **copy vs reference:** `b = a` (list/dict) = ชี้ก้อนเดียวกัน แก้ b กระทบ a → `b = a.copy()` / `list(a)`
- **แก้ list ขณะวนมัน** → ข้าม/พัง → วน copy หรือสร้าง list ใหม่
- **`input()` คืน str เสมอ** → ต้อง `int()`/`float()` ก่อนคำนวณ
- **`/` คือ float division, `//` คือ integer** · float ไม่แม่น (`0.1+0.2≠0.3`) → เทียบด้วย `math.isclose`
- **`split()` ไม่มี arg** = ตัดทุก whitespace + ทิ้งช่องว่าง · `split(' ')` = ได้ string ว่างถ้าเว้นซ้อน
- **`.get(k)` vs `d[k]`** — `d[k]` KeyError ถ้าไม่มี key; ใช้ `.get(k, default)` กันพัง
- **tab ปน space** → IndentationError (ตั้ง editor เป็น space 4)
- **`NaN` ใน pandas** = เงียบๆ ทำผลเพี้ยน → `.isna().sum()` เช็คก่อน · chained assignment warning → ใช้ `.loc`

## ดีบักให้ถูกจุด
- อ่าน traceback **จากล่างขึ้นบน** (บรรทัดล่างสุด = error จริง) · บั๊กมักอยู่จุดที่ "มั่นใจว่าถูก" ไม่ใช่จุดที่ error โผล่
- reproduce ให้ได้ก่อน → `print`/`breakpoint()` ค่าตัวแปรตรงจุดสงสัย → แก้ทีละอย่าง

## สะพานสู่ Data Science
`pd.read_csv` · vectorize อย่า loop row · `.loc[row, col]`/`.iloc` · `df.groupby().agg()` · merge = SQL join · จัดการ NaN ก่อนคำนวณ

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมกับดัก Python ที่เคยกัดในงานจริงสายคุณ เช่น:
> - *"ตอนทำงาน data lab ผมเคยพลาดเพราะ... (เช่น NaN/float/encoding) แก้โดย..."*
> - *"โครงสร้างข้อมูลที่ผมเลือกผิดบ่อย คือ... ที่ถูกควรใช้..."*

---
*ช่วยคิด+จับกับดัก Python ระดับเริ่ม→กลาง เพื่อการศึกษา — ไม่ใช่ตำรา syntax หรือคำสั่งทางการ ควรทดสอบโค้ดจริงและตรวจผลก่อนนำไปใช้ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
