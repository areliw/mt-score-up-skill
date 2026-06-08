# How we audit — QA ก่อน merge (clinical accuracy first)

> กระบวนการตรวจคุณภาพ skill ก่อนรวมเข้า `main` — เน้น **clinical accuracy** เพราะ skill งานแล็บ (🩸) ผิดแล้วกระทบคนไข้.
> เรียบเรียงจากแนวทาง adversarial review / multi-perspective verification / local-evidence audit.

## หลักการ
- **หา → ยืนยัน → พยายามหักล้าง** ทุก finding สำคัญ (อย่าเชื่อ finding รอบเดียว — ของที่ "ฟังดูถูก" อาจผิด)
- **หลายมุม ไม่ใช่หลายคนถามเหมือนกัน** — ตรวจคนละเลนส์ (correctness / patient-safety / scope-of-practice / reproducibility)
- **จัด tier ตามผลกระทบ** แล้วแก้ Tier-1 (clinical, กระทบคนไข้) ก่อนเสมอ

## ขั้นตอน
1. **Scope** — เปลี่ยนอะไรบ้าง (skill ใหม่/แก้เนื้อหา clinical/แก้ flow)
2. **Find (หลายเลนส์ขนาน)** — clinical accuracy · MT scope (ไม่ diagnose/prescribe) · PII/PHI · format/index drift · copyright
3. **Verify adversarially** — ทุก finding high/critical ให้ "พยายามหักล้าง" ก่อน ถ้าหักไม่ได้ = ของจริง
4. **Tier** — 🔴 Tier 1 = clinical error กระทบคนไข้ (แก้ทันที) · 🟠 Tier 2 = medium · 🟡 Tier 3 = polish
5. **Fix order** — Tier 1 → PII/public-integrity → code → docs → Tier 3
6. **Pin** — เพิ่ม regression note/test ที่กันไม่ให้ผิดเดิมกลับมา

## เกณฑ์ผ่าน (gate)
- ไม่มี diagnose/prescribe directive · มี `verify-first` guard ในทุก skill งานแล็บ
- ไม่มี PII/PHI หลุด (ชื่อ/HN/สถาบันเฉพาะ)
- frontmatter ครบ (`type`/`needs`/`disclaimer`) · disclaimer แบ่งระดับตามความเสี่ยง
- `python scripts/build_triage.py` แล้ว INDEX/dist/triage ไม่ drift

## อ้างอิงในรีโป
- precedent: 14-agent audit (`docs/audit-2026-06-03.md`) — จับ 4 clinical error ร้ายแรง แก้แล้ว
- skill ที่เกี่ยวข้องเชิงแนวคิด: `anti-hallucination`, `source-credibility`, `critical-appraisal-judgment`

> สำหรับเนื้อหา clinical: ผ่าน audit แล้วยัง `status: draft` จนกว่าจะมี **MT/ผู้เชี่ยวชาญ peer-review** — ดู `how-we-maintain.md`.
