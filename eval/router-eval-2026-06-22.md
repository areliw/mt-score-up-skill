# Router-accuracy eval — baseline 2026-06-22

**คำถามที่วัด:** พอผู้ใช้พิมพ์ปัญหาด้วยภาษาคนจริง (ไม่ใช่ศัพท์) — ระบบ triage หยิบสกิล **ถูกตัว** ไหม? นี่คือพื้นผิวที่เดิมพัน "94 สกิล" ทั้งหมดวางอยู่ แต่ A/B เดิมทดสอบสกิลแบบ "ป้อนให้แล้ว" — ไม่เคยวัด routing.

## วิธี (harness: `eval/harness/router-eval.js`)
1. **GEN** — Opus อ่านสกิลเป้าหมาย → แต่งปัญหาที่ผู้ใช้จะพิมพ์จริง (ห้ามใช้คำในชื่อสกิล = กัน keyword-leak)
2. **ROUTE** — Haiku อ่าน `prompts/triage.md` (catalog) → เลือก 3 สกิลตรงสุด (blind ต่อ ground-truth)
3. **SCORE** — top1 = อันดับ 1 ตรง · top3 = อยู่ใน 3 อันดับ
4. **ADJUDICATE** — Opus ตัดสิน top3-miss: หลงทางจริง (hard) หรือ boundary คาบเกี่ยวที่ยังช่วยได้ (soft)
- **batched (chunk 10, sequential)** — กัน rate-limit/usage-limit ทำ run ล่ม (บทเรียน: ยิง 94 รวด → ตาย; batch → รอด)

## ผล baseline (n=94, errors=0)
| metric | ค่า |
|---|---|
| **top1 accuracy** | **0.798** (75/94) |
| **top3 accuracy** | **0.936** (88/94) |
| hard miss | **1** |
| soft miss (acceptable) | 5 |

→ **router แกนแข็ง** — top3 93.6%, hard miss แท้ตัวเดียว

## Hard miss (1) — แก้แล้ว
- `what-skill-do-i-need` → router เดิมเลือก `data-science-workflow` (adjudicator: "พาหลงทาง" — DS-workflow สมมติว่ามีโปรเจกต์ DS เดินอยู่แล้ว)
  - **โจทย์:** *"จะทำ R2R หาตัวช่วยสอนทำกราฟ/สถิติ แต่นั่งงงไม่รู้จะเริ่มตรงไหน ควรไปหัดอะไรก่อน"*
  - **ราก:** catalog ของ what-skill เป็น meta-นามธรรม ("หาสิ่งที่คุณต้องการจริงๆ") ไม่มี trigger ภาษาคน → router เห็นแต่ "กราฟ/สถิติ/R2R" เลยเทไป DS
  - **fix:** เติม trigger ลง tagline — "ไม่รู้จะเริ่มตรงไหน / ไม่รู้ควรหา-ใช้สกิลไหนก่อน (ขอตัวช่วยทำกราฟ/สถิติ ทั้งที่ติดที่ตั้งต้น)"
  - **verify (route โจทย์เดิมผ่าน catalog ใหม่):** → `research-design-judgment` (1) · choose-stat-test (2) · r2r-stats (3) — **เลิกส่งไป misleading DS-workflow** = hard miss resolved (research-design ช่วยผู้ใช้ได้จริง) · โจทย์นี้กำกวมโดยเนื้อแท้ (multi-valid) → **ไม่ over-tune บังคับ exact-match**
  - what-skill `semi-stable` → body เปลี่ยน → **re-A/B (Δ+1.8 rescued, judgment ไม่พัง) + re-anchor hash** (gate ผ่าน)

## Soft miss (5) — acceptable (boundary คาบเกี่ยว, top1 ไป sibling ที่ยังช่วยได้)
- chemistry-interpretation → preanalytical (hemolysis K — Fork คาบเกี่ยว)
- choose-stat-test → method-validation-stats (method comparison — ตรงเท่ากัน)
- data-science-workflow → data-project-survival (CRISP-DM พี่น้อง โหลดคู่)
- immunoassay → clinical-correlation (ผลขัด clinical → confirm — พาถูกการกระทำ)
- pharmacology → preanalytical (coag workup gateway)

## top1-miss แต่ top3-hit (13) — overlap cluster, ยอมรับได้ (catalog โชว์ 3 ตัว ผู้ใช้เห็นตัวถูก)
clinchem↔result-release · deep-research↔source-credibility · digital↔phi-data · interprof-comm↔clinchem · lab-management↔clinchem · market-research↔lab-clinic-business · marketing↔ivd-sales · offload↔optimization · pathology↔histotech · python-coach↔debugging · r2r-stats↔choose-stat-test · self-improving-agent↔ai-assistant-calibration · verification-panel↔anti-hallucination

→ ส่วนใหญ่เป็น **overlap ตั้งใจ** (boundary ใกล้กัน) ที่ check_duplicates เคยเตือน — top3 ยังจับได้ = ไม่ต้องแก้รายตัว (เสี่ยง over-tune แย่ง cluster เพื่อนบ้าน)

## บทเรียน method
- **partial run (21, 40) เคยชี้ `db-judgment` เป็น hard miss — แต่ baseline เต็มไม่ใช่** = scenario-luck (โจทย์รอบนั้นบังเอิญกำกวมกับ spreadsheet) → **รอ baseline เต็มก่อนแก้** กัน fix ของที่ไม่พัง
- synthetic-eval มี **gen-ambiguity** จริง (1 โจทย์ map หลายสกิลได้) → "hard miss" บางตัว = ความกำกวมของ eval ไม่ใช่ catalog พัง → adjudicator (Opus) ช่วยกรอง hard vs soft
