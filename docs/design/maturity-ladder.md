# Maturity Ladder — 10 ชั้น วัดผลได้ (strict)

> เปลี่ยนจาก 3 ชั้น (`draft`/`semi-stable`/`stable`) → **10 ชั้น** ที่แต่ละชั้น = **gate ที่วัดได้จริง**
> (มี artifact/เลข ไม่ใช่ความรู้สึก). ออกแบบ 2026-06-15.

## ทำไมต้องวัด "ในนี้" ไม่ใช่ "ตอนแจก"

**Exit-Voice (Hirschman):** user ที่ไม่พอใจของฟรี **ไม่บ่น (voice) — เขาเลิกใช้เงียบๆ (exit)**. แปลว่าพอแจก skill ออกไป **เราจะไม่มีวันได้สัญญาณกลับว่ามันดี/แย่**. ดังนั้นการวัดผลที่เชื่อได้มีทางเดียว = **วัดในรีโปก่อนแจก** ด้วย **weak-model A/B** — ใช้ Haiku เป็น **ตัวแทน junior MT / คนไม่มีรุ่นพี่** (audience จริงของ skill). เลข **Δ (lift) เทียบ noise floor + จำนวน regression** คือ "คะแนน" ที่แทนการวัดผลจริงข้างนอกที่ทำไม่ได้.

> สิ่งเดียวที่ชนะ proxy นี้ = **เทสกับคนจริง (L8)** — แต่แพง/ช้า จึงอยู่ชั้นสูง.

## 10 ชั้น (strict superset — ขึ้นชั้น N ต้องมีของ 0..N-1 ครบ)

| L | ชื่อ | gate ที่วัดได้ | วัดด้วย (artifact) |
|---|---|---|---|
| 0 | `draft` | ร่างแล้ว ยังไม่ verify / มี blocker | — |
| 1 | `structured` | ผ่าน schema + cross-link + canonical format | `validate_repo.py` exit 0 |
| 2 | `reviewed` | codex correctness ผ่าน, **0 MUST-FIX** | codex (gpt-5.5) verdict |
| 3 | `corroborated` | claim เชิงข้อเท็จจริง cross-check แล้ว **0 contradicted** (skill ไม่ factual = ผ่านอัตโนมัติ + ติดป้าย n/a) | `literature-check.md` / source links |
| 4 | `screened` | A/B light (1-run): **0 regression** บน weak model | round4/5 screen Δ |
| 5 | `proven` | A/B **full blind-judge** (3-run, blind, control): lift หรือ tie-ที่อธิบายได้ + **0 regression** · **hash ตรงเนื้อปัจจุบัน** | round6 scorecard (Δ/kind/hash) |
| 6 | `replicated` | A/B ซ้ำบน **แกนที่ 2** (2nd weak model / 2nd judge / scenario ชุดใหม่) → ผลไปทางเดียวกัน | A/B รอบ 2 (เครื่องคนละตัว) |
| 7 | `peer-reviewed` | ผู้เชี่ยวชาญ MT/สาขา ≥1 คน **เซ็นรับเนื้อหา** | reviewer record + ชื่อ |
| 8 | `field-tested` | เทสกับ **junior MT จริง** → rescue rate (มี vs ไม่มี skill) **> 0** | human A/B (n คน) |
| 9 | `canonical` | multi-expert + ใช้สนามจริง **≥6 เดือน 0 incident** + hash ยังตรง | consensus + longitudinal log |

ลำดับ: **correctness (L2) ก่อน helpfulness (L4-6)** — อย่าพิสูจน์ว่า skill *ผิด* "ช่วยคน".

## กฎเหล็ก: hash-currency (ทำให้ "แก้แล้วไม่ test" ซ่อนไม่ได้)

- ทุก evidence (codex/A/B/peer) บันทึก **content-hash ของ skill ตอนที่ผ่าน gate นั้น**.
- skill อยู่ที่ **ชั้นสูงสุดที่ hash ของหลักฐานยังตรงเนื้อปัจจุบัน**.
- **แก้เนื้อ → hash เปลี่ยน → หลักฐานที่ครอบเนื้อเก่า stale → ชั้นตกอัตโนมัติ** ลงไปที่ชั้นที่หลักฐานยังตรง จนกว่าจะ re-test ไต่กลับ.
- build_triage = gate: ถ้า `status` ในไฟล์ > ชั้นที่ evidence (hash-current) รองรับ → **CI แดง**.

## Re-baseline (ความจริงที่ ladder นี้เปิดโปง)

- ส่วนใหญ่จะหล่นจาก "semi-stable" เดิม — เพราะ semi-stable เก่า = "codex + A/B" ก้อนเดียว ไม่แยกว่า hash สด/ stale.
- **ตัวอย่าง:** 5 ตัวที่เพิ่ง hedge (interprof/humanize/ab-test/lead-intelligence/lab-clinic) → A/B เป็นของ **ก่อน** hedge → hash ไม่ตรง → ตกมา **L2 `reviewed`** (codex สด) **ไม่ใช่ L5 `proven`** จนกว่า re-A/B.
- clinical 🩸 ที่ยังไม่ peer-review → เพดาน **L5** (แตะ L7+ ไม่ได้จนมีคนเซ็น).

## Implementation plan
1. `eval/ab-coverage.json` — registry: `{skill, level, codex_hash, ab_round, ab_kind, ab_delta, ab_hash, lit, peer}` + คำนวณ hash ปัจจุบัน
2. re-baseline `status:` ทั้ง 89 ตาม evidence จริง (honest — หลายตัวหล่น)
3. `scripts/check_maturity_gate.py` wire เข้า build_triage CI (status ≤ evidence-level + hash-current)
4. แก้ CHANGELOG/README/spec ให้สะท้อน 10 ชั้น

## Implementation status (2026-06-18)
- ✅ **measurement keystone:** `scripts/maturity_report.py` — เทียบ `status:` vs หลักฐาน A/B จริง (advisory, ไม่ mutate). รันแล้ว: 94 skills · full-A/B **59** · screen-A/B 18 · NONE 17.
- ✅ **over-claim ที่ ladder ทำนายไว้ = จริง:** **11 ตัว `semi-stable` แต่ไม่มี A/B เลย** (debugging · interprofessional-communication · lead-intelligence · literature-review · pubmed-search · report-up · source-credibility · spreadsheet · tdd · token-budget · writing) → ควร re-baseline → L2 `reviewed` (ถ้า codex สด) จนกว่าจะ A/B. *ยังไม่ mutate — taxonomy call ของ maintainer (+ แก้ CHANGELOG/spec ตาม project_status_draft_intentional).*
- ✅ **L7 enabler:** `eval/peer-review/TEMPLATE.md` — ฟอร์ม MT peer-review (hash + checklist + verdict) ปลด human bottleneck สู่ `stable`.
- ✅ **continuous gate (P4):** `ab-gate.yml` + `ab_gate_check.py` (อ่าน `_ab_slim.json`) + harness `eval/harness/ab-x3.js`.
- ✅ **status≤evidence gate (item 3):** `scripts/check_maturity_gate.py` + `.github/workflows/maturity-gate.yml` — semi-stable⟹มี A/B, stable⟹มี signed peer-review; fire เฉพาะตอน over-claim จริง (แก้ draft ไม่ trip). advisory. building มันเองจับเพิ่มอีก 11 ตัว (screen-only) → ปรับ gate ให้ยอมรับ screen-A/B = L4 ตรงกับ re-baseline.
- ✅ **re-baseline status (item 2):** เสร็จ — PR #65 demote 11 → #70 earn-back 6 (Δ≥2·SE). semi-stable honest แล้ว.
- ⏳ **TODO ที่เหลือ:** hash-registry `ab-coverage.json` (item 1) + เก็บ test-time hash → **hash-currency อัตโนมัติ** (ตอนนี้ gate เช็คแค่ evidence-class ยังไม่เช็คว่า edit ทำ A/B stale).
