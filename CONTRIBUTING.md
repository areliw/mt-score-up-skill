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
- ❌ เนื้อหา verbatim ที่ copy จากตำรา/มาตรฐานมีลิขสิทธิ์ (CLSI/ISO/AABB/บทความ/ข้อสอบ) — สรุปเป็น judgment ภาษาตัวเองได้ แต่ห้ามลอกข้อความ/ตาราง/ข้อสอบมาตรงๆ

ถ้าไม่แน่ใจ → consult MT head / QC manager ของโรงพยาบาลคุณก่อน submit

## 📝 วิธี submit — เลือกทางที่สะดวก

> **ไม่ต้องมี GitHub ก็ส่งได้** และ **ไม่ต้องเขียนให้สวย** — แค่บอก "เลือกอะไรเมื่อไหร่ +
> กับดักที่คนพลาด" มา เดี๋ยว maintainer + AI เรียบเรียงเป็น skill ให้ (พร้อม credit ชื่อคุณ)

### 🟢 ไม่มี GitHub — สำหรับ MT หน้างาน ⭐

1. *(ไม่บังคับ แต่ช่วยมาก)* ร่างให้เนียนก่อนด้วย **AI** — แปะ [prompt ตัวช่วย](#-ตัวช่วยร่างด้วย-ai)
   ลง ChatGPT / Claude / Gemini แล้วเล่าปัญหา → ได้ proposal พร้อมส่ง + มันเตือนให้ลบข้อมูลคนไข้ก่อน
2. ส่งทาง **Google Form** (เร็วสุด · ไม่ต้อง login): 👉 **[ส่งความรู้เข้าคลัง](FORM_URL)**
   <!-- maintainer: แทน FORM_URL (ตรงนี้ + ในส่วน "ติดต่อ") ด้วยลิงก์ Google Form จริง -->
3. maintainer → triage → AI แปลงเป็น skill → ขึ้นคลัง

ส่งได้ทั้ง **ข้อความ / เสียง / รูปโน้ตมือ** — ขอแค่วิจารณญาณ ไม่ต้องจัดรูปแบบเอง

### ⚙️ มี GitHub — สำหรับ dev

- **PR (preferred):** fork → `git checkout -b add-<topic>` → commit (ใส่ `Co-Authored-By` ถ้า AI ช่วย) → Pull Request → review ~3-7 วัน
- **Issue (ไม่ต้อง fork):** เปิด GitHub Issue → เล่าเคส/แปะเนื้อหา · Title `[CONTRIB] <topic> - <ชื่อย่อ>`

## 🤖 ตัวช่วยร่างด้วย AI

แปะข้อความนี้ลง AI ตัวไหนก็ได้ แล้วเติมในวงเล็บ — ได้ skill proposal พร้อมส่ง:

```
ผมเป็น MT อยากแชร์วิจารณญาณหน้างานเข้าคลัง "MT Score UP! skills" ช่วยเรียบเรียงเป็น skill proposal:
- เรื่อง/หัวข้อ: [...]
- สถานการณ์ที่ต้องตัดสินใจหน้างาน: [...]
- ตัวเลือก & เลือกอันไหนเมื่อไหร่: [...]
- กับดักที่คนพลาดบ่อย (สิ่งที่ผู้เชี่ยวชาญรู้ มือใหม่ไม่รู้): [...]
จัดเป็นหัวข้อ: ใช้เมื่อ / วิธีตัดสินใจ (fork) / กับดัก — ภาษาไทย กระชับ verdict-first
และเตือนผมถ้ามีข้อมูลคนไข้/HN/ชื่อสถาบันที่ต้องลบออกก่อนส่ง
```

## ✅ Review criteria

PR จะถูก review ตาม:
- 🔒 Privacy compliance (ไม่มี identifying info)
- 📋 Structure ตาม ISO 15189:2022 (12 ส่วน) + Safety section อ้างอิง ISO 15190:2020
- 🗣️ ภาษาไทยทางการ + คำศัพท์ MT มาตรฐาน
- 🔍 Technical accuracy (verify อย่างน้อย 1 MT คนอื่น)
- 📚 References / sources ระบุ

## 🙏 Credit

Contributors จะถูก list ใน `CONTRIBUTORS.md` (สร้างเมื่อมี contributor คนแรก)

ใส่ในรูปแบบ: `[ชื่อ-นามสกุล] - [โรงพยาบาล/สังกัด] - [contribution]`

## 📞 ติดต่อ

- 📋 **ส่งความรู้ (ไม่ต้องมี GitHub):** [Google Form](FORM_URL)
- 🐙 **GitHub** Issues / Discussions: bug · คำถาม · feature
- (FB MT group link: TBD)

---

**Code of Conduct:** treat each other with respect. MT community ในไทยเล็ก — ทุกคนเจอกันสักวัน
