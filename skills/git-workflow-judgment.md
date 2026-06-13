---
skill: git-workflow-judgment
title: โค้ช Git workflow — branch/commit/merge/conflict ไม่ให้งานหาย (Git Workflow Judgment)
type: ADVISE
needs: any
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-11
status: stable
disclaimer: "ช่วยตัดสินใจ git workflow เพื่อการศึกษา ไม่ใช่คำสั่งทางการ — คำสั่ง destructive (reset --hard / push --force / rebase ที่ push แล้ว) ลบงานได้ ต้องเข้าใจผล + สำรองก่อนรันเสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช Git workflow — branch/commit/merge/conflict ไม่ให้งานหาย

ตัดสินใจหน้างาน git — **"branch ไหน · commit ยังไง · merge หรือ rebase · resolve conflict ยังไง · กู้งานที่หาย"** ไม่ใช่ท่อง git command (= commodity ดู man page)

> 🔑 **กฎ #1: `git diff` / `git log` คือความจริง — ไม่ใช่ "updated/done" ของ tool หรือความจำ.** ก่อนเชื่อว่า edit/commit ลงจริง **verify ด้วย git เสมอ** (edit อาจลง branch ผิด / โฟลเดอร์ที่ git ignore / sandbox → git มองไม่เห็น)
> 🚫 **กับดัก #1: push หลัง PR merge ไปแล้ว = commit orphan** (ค้างบน branch ไม่เข้า main) → commit *ทุกอย่างก่อน* merge; ถ้า merge ไปแล้วต้องแก้เพิ่ม = **branch ใหม่จาก `origin/main` เสมอ**
> ⚠️ destructive (reset --hard · push --force · rebase ที่ push แล้ว) = ทำลายประวัติ/งานคนอื่น → เข้าใจผล + สำรองก่อน

## ใช้เมื่อ
- จะ branch / commit / merge / resolve conflict / กู้งานที่ "หาย"
- main ถูก protect (PR-only) → จะลงงานยังไงให้ถูก
- edit/commit แล้ว "ไม่ติด" / ไม่แน่ใจว่าลงจริง
- generated file (bundle/lock/catalog) ชนตอน merge
- CI ขึ้น drift ทั้งที่ดูเหมือนถูก (cross-platform)

## วิธีใช้
วาง skill นี้ + เล่าสถานการณ์ (จะทำอะไร / error อะไร / repo state) → AI ชี้ลำดับที่ปลอดภัย + กับดักที่ทำงานหาย — ทุกขั้นที่ irreversible ให้ยืนยัน + verify ด้วย `git` ก่อน

---

## วิธีตัดสินใจ (AI: ทำตามนี้) — forks

### Fork 1 — ทำบน branch ไหน
- **main ถูก protect (require-PR):** ทุกการเปลี่ยน = **branch สดจาก `origin/main` → push → PR → ให้คน merge** (แม้ admin bypass ได้ ก็ควรผ่าน PR เพื่อ review + CI)
- **branch ใหม่ทุกงาน — อย่าทำต่อบน branch ที่ merge แล้ว** (stale → commit ใหม่บนนั้น = orphan ไม่เข้า main)
- **`git fetch origin main` ก่อนเสมอ** แล้ว `git switch -c <new> origin/main` (หรือ `git checkout -b` — *fail* ถ้าชื่อ branch มีอยู่แล้ว = กันเขียนทับ) → กัน divergence/conflict ทีหลัง · ⚠️ **อย่าใช้ `-B`/`git reset` กับ branch ใหม่** — `-B` *force-reset* branch ชื่อเดิมที่มีอยู่ทิ้งเงียบๆ (งานหาย) → สงวนไว้เฉพาะตอนตั้งใจ reset จริงๆ

### Fork 2 — Commit: atomic + message ที่ตามได้
- **1 commit = 1 เรื่องที่ revert อิสระได้** — อย่าผสม content + tooling + rename ในก้อนเดียว (revert/review ยาก)
- message: บรรทัดแรก imperative สั้น (`fix: …` / `feat: …`) + body บอก **ทำไม** ไม่ใช่ **อะไร** (diff บอก "อะไร" อยู่แล้ว)
- 🚫 **ห้าม commit:** secret/token · PII/ข้อมูลคนไข้ · ข้อมูลส่วนตัว/identity ลับ · ไฟล์ generated ที่ควร gitignore — **`git grep` คำลับก่อน commit ที่แตะ content เสมอ** (หลุดเข้า history แล้วลบยาก)

### Fork 3 — Merge vs Rebase + ลำดับ
- **merge commit:** เก็บประวัติจริง ไม่รื้อ → **default สำหรับ branch ที่ push/share แล้ว**
- **rebase:** ประวัติ linear → **เฉพาะ branch ส่วนตัวที่ยังไม่ push** (rebase branch ที่ push แล้ว = ต้อง force-push = พังของคนอื่น)
- **ลำดับสำคัญ:** จะล็อก/เปลี่ยน rule ที่กระทบ automation → **land การแก้ที่จำเป็นก่อน แล้วค่อยล็อก** (เช่น แปลง bot เป็น verify-only *ก่อน* เปิด require-PR ไม่งั้นบอท push ไม่ได้ CI แดง)

### Fork 4 — Resolve conflict (โดยเฉพาะ generated file)
- **generated file (bundle/lock/catalog) ชน → อย่าแก้มือ → regenerate** บน base ที่ merge แล้ว (deterministic + ถูกกว่าแก้เอง)
- 2 ฝั่งแก้ **คนละบรรทัด = git auto-merge** (ไม่ conflict) → conflict จริงเกิดตอนแก้ทับบรรทัดเดียวกัน
- pattern กู้เมื่อรู้ exact edit: `git checkout --theirs <file>` (ฝั่งไหนต้องเช็คก่อน — ❌ ไม่ใช่ merge-base) → **re-apply การแก้ของเราทับ** → แล้ว **verify `git diff <base>..HEAD -- <file>` ต้องเห็นเฉพาะการเปลี่ยนที่ตั้งใจ** ไม่มีของหาย
  - ⚠️ **`--ours`/`--theirs` หมายความสลับกันตาม operation:** ใน **merge** → `--ours`=branch ปัจจุบันของเรา, `--theirs`=branch ที่ merge เข้ามา (เช่น `origin/main`) · ใน **rebase** → *สลับกัน* (`--ours`=branch ที่ rebase ไปอยู่บน, `--theirs`=commit ของเราที่กำลัง replay) → **ยืนยันว่าจะเอาฝั่งไหนจาก context เสมอ + verify ด้วย `git diff` หลังทำ** (พลาดทิ้งผิดฝั่งง่ายมาก)

### Fork 5 — main ถูก protect: ใครแก้ได้ + flow
- require-PR + **ยกเว้น admin (`enforce_admins=false`):** owner push ตรงได้, คนอื่น/บอท ต้องผ่าน PR · personal repo ตั้ง "เฉพาะคนนี้ push" ไม่ได้ (เป็น org feature) — "เฉพาะ owner" มาจาก **sole-collaborator + rule นี้รวมกัน**
- ห้าม force-push + ห้ามลบ main (กันรื้อ/ลบประวัติ)
- ⚠️ **PR ที่แตะ `.github/workflows/*` = review เป็นพิเศษ** — merge แล้วมันรันด้วยสิทธิ์เขียนบน main (fork PR ปกติ token read-only แต่*หลัง merge*ไม่ล็อก)

### Fork 6 — "งานหาย" / commit ไม่ติด → กู้ยังไง
- เช็คก่อนตกใจ: อยู่ branch ไหน (`git branch --show-current`) · repo จริงหรือโฟลเดอร์ที่ถูก ignore (`git rev-parse --show-toplevel` + `git check-ignore <path>`)
- **edit หาย / `git status` ไม่โผล่** → edit ลง dir หรือ branch ผิด (เช่น sandbox/worktree ปลอมที่ git ignore) → ไปแก้ที่ repo จริง
- **commit หายหลัง reset/checkout** → `git reflog` หา SHA → `git checkout`/`cherry-pick` กลับ
- **stash หาย** → `git stash list`; ถ้าหลุด → `git fsck --unreachable | grep commit`

### Fork 7 — Line endings / cross-platform (CI drift หลอก)
- Windows `autocrlf=true` → checkout เป็น CRLF, commit เป็น LF · **generated file ที่ build บน Windows อาจต่างจาก Linux CI ไม่กี่บรรทัด** → CI รายงาน "drift" ทั้งที่ content ถูก
- แก้: **`.gitattributes`** (`* text=auto eol=lf` หรือเจาะจง generated file) + ให้ generator เขียน LF · **หรือ gate CI เฉพาะไฟล์ deterministic** (อย่า gate ไฟล์ bundle ใหญ่ที่ churn ข้าม platform)

## กับดัก (Anti-patterns)
- 🚫 เชื่อ "updated successfully"/ความจำ ไม่ verify `git diff` → edit ลงผิดที่/หายโดยไม่รู้
- 🚫 push หลัง PR merge → orphan commit (ค้างไม่เข้า main)
- 🚫 ทำงานต่อบน branch ที่ merge แล้ว → orphan/divergence
- 🚫 แก้ generated-file conflict ด้วยมือ → ควร regenerate
- 🚫 merge ก่อน CI เขียว → ปล่อยของพังเข้า main
- 🚫 commit generated bundle ที่ churn ข้าม platform แล้ว gate CI บนมัน → CI drift หลอกตลอด
- 🚫 force-push / reset --hard main → รื้อประวัติคนอื่น
- 🚫 commit secret/PII/ของลับเข้า public (grep ก่อน) — history ลบยาก
- 🚫 merge PR ที่แก้ workflow โดยไม่อ่าน → รันด้วยสิทธิ์เขียน
- 🚫 rebase branch ที่ push/share แล้ว → ต้อง force-push = พังของคนอื่น

> 🔗 คู่กับ [`ai-coding-guardrails`](./ai-coding-guardrails.md) (คุม AI ตอนแก้โค้ด) · [`offload-to-automation`](./offload-to-automation.md) (ให้ code/CI ทำงานเป๊ะ) · [`debugging-judgment`](./debugging-judgment.md)

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"ครั้งที่ commit/งานหาย แล้วกู้ด้วย `reflog`/`fsck` ยังไง"*
> - *"conflict generated-file ที่แก้แล้วเจ็บ — วิธีที่ใช้จริงคือ..."*
> - *"flow PR + protected main ของทีมผม จุดที่พลาดบ่อยคือ..."*

---
*ช่วยตัดสินใจ git workflow เพื่อการศึกษา ไม่ใช่คำสั่งทางการ — คำสั่ง destructive ลบงานได้ ต้องเข้าใจผล + สำรองก่อนรันเสมอ · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
