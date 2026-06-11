# แผนปล่อยจริง — MT Score UP Skills Hub (Launch / Go-to-Market)

> เอกสารนี้คือ **playbook ปล่อยของ** ไม่ใช่ marketing copy — ใครหยิบไปกดตามได้เลย
> หลักคิดเดียวที่ถือทั้งหน้า: **แคบก่อน กว้างทีหลัง** เพราะของยัง `draft` ทั้ง 87 ตัว ยังไม่ผ่าน clinical peer-review — ปล่อยกว้างทันทีแล้วมี error คลินิกหลุด = เสีย credibility ทั้งโปรเจกต์ในครั้งเดียว แก้คืนยาก

## ทำไม "แคบก่อน" ถึงเป็นทางที่ถูก (ไม่ใช่ขี้กลัว)

เป้าของคลังนี้คือ **กองกลางที่ MT ทุกรุ่นช่วยกันลงขัน** — รุ่นใหม่/คนไม่มีรุ่นพี่ดีๆ จะได้ "ไม่เคว้ง ไม่โดนเจื๋อน". ของแบบนี้ value มาจาก **ความเชื่อใจ** ไม่ใช่ยอด download. ปล่อยกว้างทั้งที่ยังไม่มีคนตรวจ = เดิมพันความเชื่อใจทั้งหมดในรอบเดียว.

3 เหตุผลที่ soft-launch แคบก่อน:
1. **จับ clinical error ก่อน scale** — สกิลงานแล็บ (🩸) ผิดแล้วกระทบคนไข้. ให้เพื่อน MT 5-10 คนลองยิงเคสจริงก่อน เจอ error ตอนคน 8 คนเห็น ดีกว่าเจอตอนคน 800 คนเห็น
2. **ของยังเป็น draft โดยตั้งใจ** — `status: draft` ทั้งคลังคือเจตนา ไม่ใช่งานค้าง. การปล่อยแบบ draft + disclaimer ชัดเจน = **ซื่อสัตย์ ไม่ใช่มักง่าย**. แต่ "draft" ต้องมาคู่กับ "วงแคบที่เข้าใจว่ามันคือ draft" ไม่ใช่โยนให้คนทั่วไปที่อ่าน disclaimer ไม่ทัน
3. **4 สกิลคลินิกใหม่ยังรอ peer-review** — `urinalysis-judgment` · `preanalytical-judgment` · `poct-judgment` · `flow-cytometry-judgment` ผ่าน design review แล้วแต่ **ยังไม่มี MT คนที่สองตรวจ**. อย่าเอา 4 ตัวนี้ขึ้นหน้าโพสต์ public จนกว่าจะมีคนตรวจ (ดู checklist ข้อ 5)

> honest baseline ที่อ้างได้ (อย่าเป่าเกินนี้): eval บน **53 สกิล** (model อ่อน + กรรมการตาบอด) = rescued 9 · better 16 · tie 19 · **0 dangerous regression**. อีก 34 ตัวที่เพิ่มภายหลัง = design-review + spot-A/B screen เท่านั้น **ยังไม่ได้ full A/B**. สกิลช่วย model อ่อน/มือใหม่ — frontier model มักเสมอ (ตอบถูกเองอยู่แล้ว). ตัวเลขนี้ใช้พูดได้, เกินนี้ห้าม

---

## เฟส 1 → 2 → 3 (แคบ → กว้าง)

| เฟส | ใคร | จำนวน | ประตูผ่านไปเฟสถัดไป (gate) |
|---|---|---|---|
| **1 · Soft-launch** | เพื่อน MT ที่ไว้ใจได้ 5-10 คน (มีงานแล็บจริง) | 5-10 | ได้ feedback ≥5 คน · **0 clinical error ที่ยังไม่แก้** · มีอย่างน้อย 1 correction ที่ปิดจบ (พิสูจน์ว่า loop แก้ได้จริง) |
| **2 · Community** | เพจ Score UP + กลุ่ม MT ไทย (FB/Line) | 50-500 | contribution inflow เริ่มเข้า (issue/form ≥1) · correction rate ทรงตัว ไม่พุ่ง · 4 สกิลคลินิกใหม่ผ่าน peer-review |
| **3 · Public** | โพสต์เปิดกว้าง · pin · ชวน share ข้ามกลุ่ม | ไม่จำกัด | ของนิ่ง · funnel ทำงาน (form live, มี maintainer SOP) · CONTRIBUTORS.md มีชื่อจริง |

**กฎเหล็ก:** ห้ามข้ามเฟส. ถ้าเฟส 1 เจอ clinical error ที่ยังแก้ไม่จบ → **หยุด อย่าขึ้นเฟส 2**. gate ไม่ใช่พิธีกรรม — มันคือเบรกที่กันไม่ให้ error ขยายตัว.

### เฟส 1 ลงรายละเอียด — ขอ feedback ยังไงให้ได้ของจริง
- เลือกคนที่ **กล้าบอกว่าผิด** ไม่ใช่คนที่จะตอบ "ดีครับ" อย่างเดียว — feedback ที่มีค่าคือ "ตรงนี้มันไม่จริงหน้างาน"
- ให้แต่ละคน **1 สกิลในสายเขา + 1 เคสจริงของเขา** (เจาะ ไม่ใช่ให้อ่านทั้งคลัง) — bloodbank คนทำ BB, micro คนทำจุล
- ถามตรง 3 ข้อ: (1) มีอะไรผิด/ไม่ตรงหน้างานไหม (2) มีกับดักที่คลังยังไม่เก็บไหม (3) จะหยิบไปใช้จริงไหม เพราะอะไร
- เก็บทุก correction เป็น **issue/PR** ทันที — เฟส 1 คือที่ที่ loop "เจอผิด → แก้ → ปิด" ต้องพิสูจน์ว่าเดินได้

---

## ปล่อยช่องทางไหน + ลำดับ

| ลำดับ | ช่องทาง | เฟส | ทำอะไร |
|---|---|---|---|
| 1 | **DM/กลุ่มเล็กเพื่อน MT** | 1 | ส่ง raw URL สกิล + เคส ตรงตัว ขอ feedback |
| 2 | **เพจ Score UP (FB)** | 2 | โพสต์แนะนำคลัง · pin โพสต์ · ลิงก์ repo + triage.md |
| 3 | **กลุ่ม MT ไทย (FB)** | 2 | โพสต์ในกลุ่มที่ admin อนุญาต · เน้น "ฟรี ไม่ต้องติดตั้ง" + soul กองกลาง |
| 4 | **Line / community** | 2-3 | ช่องส่งความรู้แบบไม่มี GitHub (ชี้ไป Google Form) |
| 5 | **โพสต์เปิดกว้าง + ชวน share** | 3 | หลังของนิ่ง · ชวนคนช่วยกันลงขัน |

**โทนโพสต์ (บังคับ):** MT เป็นเจ้าของผลงาน AI เป็นแค่ปากกา · พูดว่า "ตัวช่วยคิด/decision-support" ไม่พูด "verified/แม่นยำ/รับรองทางคลินิก" · ใส่ disclaimer NOT FOR CLINICAL USE ทุกโพสต์ที่แตะสกิลแล็บ · เลี่ยง AI-tropes ("ในยุค AI...") เขียนเหมือนคนพูด.

**soul ที่ต้องสื่อในโพสต์:** นี่คือ **กองกลาง** ไม่ใช่รุ่นพี่สอนรุ่นน้องแบบบนลงล่าง — ทุกคนเป็นทั้งคนให้และคนรับ. ค่าพิเศษ = ดึงวิจารณญาณของ MT ที่กำลังเกษียณไว้ไม่ให้สูญ ("ห้องสมุดถูกเผาทั้งหลังเมื่อคนเก่งเกษียณ"). เป้า = MT รุ่นใหม่/คนไม่มีรุ่นพี่ดีๆ ไม่เคว้ง.

---

## ปล่อยอะไรก่อน — lab skills นำหน้า (crown jewels)

ลำดับการชู ไม่ใช่ลำดับการมีอยู่ — ทุกตัวมีในคลังแล้ว แต่ "ตัวที่เอาขึ้นหน้าโพสต์" ต้องเป็นของที่เงาวับสุดและตรงกลุ่มสุด:

1. **🩸 งานแล็บ (crown jewels) — นำหน้าเสมอ.** `bloodbank-judgment` (ลึกสุด 13 fork) · `hematology-judgment` · `clinchem-judgment` · `clinmicro-judgment`. นี่คือของที่ MT หน้างานเห็นแล้ว "อันนี้ใช้ได้จริง" — เป็นเหตุผลให้เขาเชื่อทั้งคลัง
   *(ยกเว้น 4 ตัวรอ peer-review — ดู checklist ข้อ 5 — ยังไม่ชูจนกว่าจะตรวจเสร็จ)*
2. **🔬 research / R2R** — `choose-stat-test` · `sample-size-power` · `r2r-research-proposal`. กลุ่มทำวิจัย/CQI/thesis ที่ไม่มีพื้นสถิติ
3. **🤖 ใช้ AI อย่างคม** — `anti-hallucination` · `what-skill-do-i-need` · `prompt-optimizer`. ดึงคนที่อยากใช้ AI เป็นเครื่องมือ
4. **🧭 ชีวิต/อาชีพ** — `mt-career-judgment` · `mt-exam-strategy-judgment`. ขยายฐานนอกงาน bench

> เหตุผล: lab skills คือจุดที่ judgment เข้มที่สุดและ "พิสูจน์ตัวเอง" ได้เร็วที่สุดต่อสายตา MT. ปล่อย career/AI นำหน้า = ดูเหมือน productivity tool ทั่วไป กลืนหาย. ปล่อย lab นำหน้า = ดูเหมือนของที่ "คนทำแล็บจริงเขียน" ซึ่งคือความจริง.

---

## ตารางต่อ platform (สรุปสั้น)

ฉบับเต็ม how-to ต่อ platform (ครบ 7 ช่องทาง) → [`docs/USING.md`](./USING.md) · ตั้ง Custom GPT/Project/Gem → [`setup-custom-gpt.md`](./setup-custom-gpt.md)

| Platform | โหมดที่เวิร์ค | ปล่อยอะไร | หมายเหตุ |
|---|---|---|---|
| **Claude (web/Project)** | ก๊อป · live-load · bundle | สกิลเดี่ยว + `dist/all-skills.md` (~133K) | context ใหญ่ รับ bundle ได้ · Project = จำ context |
| **ChatGPT (Custom GPT)** | ก๊อป · live-load (browse) | สกิลเดี่ยว · Custom GPT แนบไฟล์ | chat เปล่าฟรีไม่เหมาะ bundle ใหญ่ |
| **Gemini (Gem)** | ก๊อป · live-load · bundle | สกิลเดี่ยว + bundle | context ใหญ่ รับ bundle ได้ |
| **AI chat ทั่วไป / offline** | ก๊อปเนื้อไฟล์ (แช่แข็ง) | สกิลเดี่ยว | live-load ใช้ไม่ได้ถ้าดึง URL ไม่ได้ |

3 โหมดโหลด (ย่อ): **ก๊อป** = snapshot แช่แข็ง (เหมาะคลินิก/audit trail) · **live-load** ผ่าน raw URL = auto-sync ล่าสุด · **bundle** `dist/all-skills.md` = ทุกตัวไฟล์เดียว AI เลือกเอง (เฉพาะ context ใหญ่). รายละเอียด 3 โหมด + ตารางต่อ platform → [`docs/USING.md`](./USING.md).

---

## Metrics ที่ดู (ไม่ใช่ vanity)

วัด **สุขภาพของกองกลาง** ไม่ใช่ความดัง. 3 ตัวที่สำคัญจริง:

| metric | วัดอะไร | สัญญาณดี | vanity ที่ห้ามหลงวัด |
|---|---|---|---|
| **Adoption (ใช้จริง)** | คนหยิบสกิลไปใช้ในงานจริง | มีคนเล่าว่าใช้แล้วช่วยตัดสินใจเคสไหน · star/fork repo · ถามถึงสกิลเฉพาะ | ยอด view โพสต์ · reach |
| **Contribution inflow** | คนเริ่ม "ลงขัน" คืนกองกลาง | issue/form/PR เข้า · มีคนเสนอกับดักใหม่ · ผู้เกษียณส่งวิจารณญาณมา | ยอด like (ไม่ใช่การให้) |
| **Correction reports** | คนกล้าบอกว่าผิด = ระบบ self-heal | มี correction เข้ามาแล้ว **ปิดจบ** เร็ว · rate ทรงตัว | "0 correction" = อาจไม่มีใครกล้าบอก ไม่ใช่ของสมบูรณ์แบบ |

> อ่าน correction inflow แบบกลับหัว: **มี correction เข้ามา = ระบบทำงาน** (คนเชื่อใจพอจะบอกว่าผิด + loop แก้เดินได้). น่ากลัวกว่าคือ adoption สูงแต่ correction เป็นศูนย์ — แปลว่าคนใช้แต่ไม่กล้า/ไม่รู้วิธี feedback. ถ้าเจอแบบนั้น → ปัญหาอยู่ที่ feedback channel ไม่ใช่คุณภาพสกิล.

จุดที่ขาด feedback loop ปัจจุบัน (รู้ไว้): ผู้ใช้ที่อ่าน `dist/all-skills.md` รวม ยัง map ปัญหากลับไปสกิลตัวที่ผิดได้ยาก — ดู [`docs/FEEDBACK.md`](./FEEDBACK.md) หรือชี้เขาให้ระบุชื่อสกิลในหัว issue.

---

## Human-only launch checklist (เฉพาะ maintainer ทำได้)

สิ่งเหล่านี้ AI/CI ทำแทนไม่ได้ — ต้อง maintainer ลงมือเอง. ทำตามลำดับ:

- [x] **1 · เปิด Google Form (no-GitHub lane)** — ✅ live: [forms.gle/N7RsgZqrHkikgfKK6](https://forms.gle/N7RsgZqrHkikgfKK6)
  - เสียบลิงก์ครบทุกจุดแล้ว: CONTRIBUTING ×2 · README · FEEDBACK · CONTRIBUTORS · INTAKE · skill-interview · issue-template config
  - *เหตุผล:* ~80% ของกลุ่มเป้าหมาย (MT หน้างาน) ไม่มี GitHub — lane นี้ live แล้ว funnel ไม่ตันครึ่ง

- [ ] **2 · ตั้ง Custom GPT / Claude Project / Gemini Gem (ตัวอย่างพร้อมใช้)**
  - ทำตาม `docs/setup-custom-gpt.md` ต่อ platform — เอาไว้เป็น demo link ในโพสต์ ("กดใช้เลยไม่ต้อง setup")
  - ลดแรงเสียดทานคนลองครั้งแรกได้มากสุด

- [ ] **3 · ขอ clinical peer-review 4 สกิลใหม่** — `urinalysis-judgment` · `preanalytical-judgment` · `poct-judgment` · `flow-cytometry-judgment`
  - หา MT คนที่สองในสายนั้นตรวจ judgment + กับดัก (ไม่ใช่แค่ proofread)
  - **gate ของเฟส 2→3:** ยังไม่ผ่าน = ยังไม่ชู 4 ตัวนี้ขึ้นโพสต์ public (ในคลังอยู่ได้ แต่ติด draft ชัด)

- [ ] **4 · สร้าง CONTRIBUTORS.md เมื่อมี contributor คนแรก**
  - `CONTRIBUTING.md` สัญญาไว้ว่าจะ list ชื่อ — พอคนแรกส่งของ ต้องมีไฟล์ให้ลง credit (ฟอร์แมต: `[ชื่อ] - [สังกัด] - [contribution]`)

- [ ] **5 · โพสต์จริง (เรียงตามเฟส)**
  - เฟส 1: DM เพื่อน MT 5-10 คน + เคส
  - เฟส 2: เพจ Score UP → pin → กลุ่ม MT (ขออนุญาต admin)
  - เฟส 3: เปิดกว้าง + ชวน share
  - ทุกโพสต์: disclaimer ชัด · MT-เป็นเจ้าของ-AI-เป็นปากกา · soul กองกลาง · ไม่ overclaim

> เช็คก่อนโพสต์ทุกครั้ง: โพสต์นี้มีคำว่า "verified/รับรอง/แม่นยำพิสูจน์แล้ว" ไหม? → ถ้ามี ตัดออก. มี disclaimer NOT FOR CLINICAL USE ไหม (ถ้าแตะสกิลแล็บ)? → ถ้าไม่มี เติม. ฟังเหมือน MT เขียนหรือเหมือน AI เขียน? → ถ้าเหมือน AI เกลาใหม่.

---

## สรุปหนึ่งบรรทัด

ปล่อยแคบให้เพื่อน MT จับผิดก่อน → ขยายเข้าชุมชน → เปิดกว้างเมื่อของนิ่งและ funnel ทำงาน. **draft + disclaimer ชัด = ซื่อสัตย์**. กองกลางนี้โตด้วยความเชื่อใจ ไม่ใช่ยอด view — เก็บความเชื่อใจไว้ให้ดีตั้งแต่โพสต์แรก.

---
*เอกสารวางแผน — ปรับได้ตามหน้างานจริง · cross-link: [`README.md`](../README.md) · [`CONTRIBUTING.md`](../CONTRIBUTING.md) · [`docs/USING.md`](./USING.md) · [`docs/FEEDBACK.md`](./FEEDBACK.md) · [`docs/setup-custom-gpt.md`](./setup-custom-gpt.md) · [`eval/ab-scorecard.md`](../eval/ab-scorecard.md)*
