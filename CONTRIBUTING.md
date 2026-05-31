# Contributing to MT Score UP — Skills Hub

ขอบคุณที่สนใจ contribute! โปรเจ็คนี้เป็น **community-driven open source** สำหรับ MT ไทย

## 🎯 สิ่งที่ contribute ได้

### 0. Skills (ใน `skills/`) — ต้องการมากสุด ⭐

แพ็ก **"วิจารณญาณ" ในสายงานคุณ** ให้ MT คนอื่นหยิบไปวางในแชต AI ใช้ได้ — ไม่ต้องเขียนเก่ง แค่รู้จริง

**ไม่ต้องเขียน skill เองก็ได้** — เล่าให้ฟังก็พอ:
- *"งานแบบนี้คนชอบทำพลาดตรง... ที่ถูกควร..."*
- *"เคสที่ reviewer/หัวหน้า/QC ตีกลับเพราะ... กับวิธีที่แก้คือ..."*
- *"เครื่องมือ/test/วิธี ที่ตำราบอกใช้ได้ แต่ของจริงต้องระวัง..."*

หัวใจของ skill = **judgment ไม่ใช่ knowledge** → เก็บ "เลือกอะไรเมื่อไหร่ + กับดักที่มือใหม่ไม่รู้" ตัดสิ่งที่ตำรา/AI รู้อยู่แล้วทิ้ง

**รูปแบบไฟล์** (ดูตัวอย่างใน `skills/`): frontmatter (`skill`/`title`/`type`/`needs`/`author`/`disclaimer`) → ใช้เมื่อ → วิธีใช้ → วิธีทำ → กับดัก → ช่องผู้เชี่ยวชาญเติม → disclaimer
- **type:** `ADVISE` (แนะนำ) · `DO` (รันจริง) · `CALIBRATION` (ปรับวิธีทำงาน AI)
- **PII:** ห้ามมีชื่อคน/โรงพยาบาล/รหัสวิชา/แหล่งเฉพาะ — generalize ก่อนเสมอ
- **voice:** ภาษากลาง (เป็นของสาธารณะที่คนอื่น copy ไปใช้)

### 1. WI examples (ใน `inbox/`)

WI ที่คุณเขียนเสร็จ + ผ่าน QC แล้ว → drop ที่ `inbox/` (flat folder, ไม่มี subfolder) → AI ใช้เป็น template

**ต้องลบข้อมูล identifying ก่อน submit:**
- ✅ ชื่อคนไข้, HN, MRN → ลบหรือใช้ `[ผู้ป่วย]` แทน
- ✅ ชื่อบุคลากรเฉพาะเจาะจง → ใช้ placeholder `[MT name]`, `[supervisor]`
- ✅ Hospital-specific เลขที่เอกสาร → ใช้ `[TBD]`
- ✅ Lot number specific → ลบหรือใช้ placeholder
- ✅ Date specific (ที่ correlate กับ patient) → ลบ

**ชื่อไฟล์อิสระ** — ไทย / อังกฤษ / ผสม (เช่น `PRC ตัวอย่าง B.md`, `abo-grouping.md`). AI scan content + classify ให้เอง ไม่ต้องคิด structure

### 2. Hospital templates (ใน `templates/`)

.docx template ที่มี header/footer/box ลายเซ็นของโรงพยาบาลคุณ
**ลบ logo เฉพาะ** ที่อาจ infringe trademark → ใช้ placeholder text แทน

### 3. Prompt improvements (ใน `prompts/`)

ถ้าคุณเจอ prompt ที่ทำให้ AI generate WI ดีขึ้น (โครงสร้างครบกว่า, ภาษาตรงกว่า, technical depth ลึกกว่า) → propose ใน `prompts/system.md`

**Format:** PR ที่ describe:
- ก่อนแก้: ผลลัพธ์เป็นอย่างไร
- หลังแก้: ผลลัพธ์ดีขึ้นยังไง
- Test case: prompt input ที่ใช้ test

### 4. Glossary terms (ใน `glossary.md` — TBD)

ศัพท์ MT ไทย ↔ English term ที่ AI ยังแปลผิด

### 5. Bug fix / typo

แค่ open PR เลย

## 🔒 Privacy + Ethics

โปรเจ็คนี้รับ contribute เฉพาะ:
- ✅ Generic procedures (ไม่ลิงค์ patient เฉพาะ)
- ✅ ลบ identifying info ทั้งหมดแล้ว
- ✅ ผ่านการอนุมัติจาก supervisor / QC manager ของคุณ (ถ้าเป็น proprietary SOP)

**ไม่รับ:**
- ❌ Patient records ทุกรูปแบบ
- ❌ Hospital trade secrets / proprietary intellectual property
- ❌ Document ที่ห้ามแชร์ตาม hospital policy

ถ้าไม่แน่ใจ → consult MT head / QC manager ของโรงพยาบาลคุณก่อน submit

## 📝 วิธี submit

### Method 1: GitHub PR (preferred)

1. Fork repo นี้
2. Clone → `git clone <your-fork>`
3. Branch: `git checkout -b add-<topic>`
4. แก้ไข + commit (ระบุ `Co-Authored-By` ถ้า AI ช่วย draft)
5. Push + open Pull Request
6. Maintainer review (~3-7 วัน)

### Method 2: Email (ถ้าไม่ใช้ GitHub)

ส่ง .md / .docx file มาที่: [email TBD]
Title: `[CONTRIB] <topic> - <ชื่อย่อ>`

## ✅ Review criteria

PR จะถูก review ตาม:
- 🔒 Privacy compliance (ไม่มี identifying info)
- 📋 Structure ตาม ISO 15189:2022 (12 ส่วน) + Safety section อ้างอิง ISO 15190:2020
- 🗣️ ภาษาไทยทางการ + คำศัพท์ MT มาตรฐาน
- 🔍 Technical accuracy (verify อย่างน้อย 1 MT คนอื่น)
- 📚 References / sources ระบุ

## 🙏 Credit

Contributors จะถูก list ใน [CONTRIBUTORS.md](./CONTRIBUTORS.md) (สร้างเมื่อมี contributor คนแรก)

ใส่ในรูปแบบ: `[ชื่อ-นามสกุล] - [โรงพยาบาล/สังกัด] - [contribution]`

## 📞 ติดต่อ

- GitHub Issues: bug report / feature request
- Discussions: คำถามทั่วไป
- (FB MT group link: TBD)

---

**Code of Conduct:** treat each other with respect. MT community ในไทยเล็ก — ทุกคนเจอกันสักวัน
