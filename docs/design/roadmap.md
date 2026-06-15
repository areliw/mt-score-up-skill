# Roadmap — wave ที่จะทำ (draft 2026-06-15)

> **หลัก:** โลภเพื่อ MT — สกัด value ให้มากสุด **แต่ซื่อสัตย์** (ไม่ overclaim). ทุก wave fan-out ขนานได้ (overnight-style) · ทุกสกิลใหม่/แก้เนื้อ = **codex + PR** เสมอ · main protected = PR-only · verify-against-git ทุกครั้ง.
> ที่มา: gap-review + codex (2026-06-15) — infra ครบแล้ว, gap จริงอยู่ที่ content void + measurement + real-validation.

## ภาพรวม
| Wave | ชื่อ | ส่งมอบ | ขนาน | dependency |
|---|---|---|---|---|
| W0 | Quick wins | merge #45 · CITATION.cff · promote design drafts | 1 คน | — |
| W1 | Content voids 🔴 | 3 สกิลที่รุ่นน้องเคว้งจริง + 3 fork | ~5 agent | — (ทำได้เลย) |
| W2 | Measurement foundation | ladder 10-tier + credit + re-baseline 91 | 2-3 agent + integrate | — (ควรก่อน "ผลิตสกิลเยอะ" รอบหน้า) |
| W3 | Hardening | pytest scripts + safety-eval | ~3 agent | — |
| W4 | Moat + ทะลุเพดาน | senior-case + auto-invoke + real-validation | mixed | W2 (ใช้ ladder/credit) |
| W5 | Catalog-Steward | self-curation loop | capstone | **W2** |

**ลำดับแนะ:** W0 เดี๋ยวนี้ → W1 (value เร็วสุด) → W2 (ลงดิน honest) → W3 → W4 → W5

---

## W0 — Quick wins (~30 นาที, 1 คน)
- **merge #45** `receiving-review-judgment` (รออยู่)
- **`CITATION.cff`** — ให้ cite repo ได้ (ตรงธีม paper/credit)
- promote `maturity-ladder.md` + `contribution-credit.md` จาก untracked → tracked design doc

## W1 — Content voids 🔴 (north-star ตรงสุด · fan-out ~5)
verified ว่า "ไม่มีจริง" (ไม่ใช่ codex มั่ว):
| skill | โดเมน | gap-type |
|---|---|---|
| `histotech-cytology-judgment` | ตรึง/ย้อม/adequacy/artifact (*process* ไม่ใช่แปลผล) | 🔴 void |
| `blood-donor-component-judgment` | donor eligibility/apheresis/component-QC/hemovigilance | 🔴 void (bloodbank = ฝั่ง transfusion เท่านั้น) |
| `result-release-judgment` | delta-check เด้ง→ทำไง · autoverify exception · amended report · ปล่อย/ยับยั้ง/escalate | 🟠 scattered→consolidate |
| fork → `clinchem` | analyzer-down/on-call backup + STAT triage | 🟠 |
| fork → `lab-management` | EQA/PT failure investigation | 🟠 |
| fork → `infection-control` | chemical/occupational safety (formalin/spill/waste) | 🟠 |
- ⚠️ **clinical = flag-only verify เข้ม** (เนื้อผิด = ฉีด error) · แต่ละตัว codex-gate → PR · status `draft`

## W2 — Measurement foundation (credibility · "โลภต้องซื่อสัตย์")
- **maturity-ladder 10-tier** + gate-number ที่เคาะ: L5 ~20-30 paired answer · L6 +แกน 2 (~50-60 = เพดาน synthetic) · L7 ≥2-3 peer · L8 ≥25-35 junior/arm (จาก `sample-size-power`) · L9 ≥6 เดือน 0 incident + ≥2 published source/claim
- `eval/ab-coverage.json` registry + `scripts/check_maturity_gate.py` + wire CI (status ≤ evidence-level + hash-current)
- **re-baseline 91 จริง** → ส่วนใหญ่หล่น L2-5 (ยอมรับ: ยังไม่มีตัวแตะ L7)
- **contribution-credit**: `eval/contributions.json` + U-count (tier=U) + anti-gaming + render. identity opt-in · anon=U-only

## W3 — Hardening (gap เงียบ)
- **pytest** ครอบ 7 scripts (build_triage/validate_repo/check_duplicates — golden output + malformed fixture). "CI รัน ≠ logic ถูก"
- **safety-eval**: map 91 → `unsafe-confident-answer / scope-of-practice / missing-context / required-escalation` → A/B safety pass (เดิมวัดแค่ helpfulness Δ)

## W4 — Moat + ทะลุเพดาน synthetic (value จริงพิสูจน์)
- **senior-case embedding**: ฝังเคส de-identified (context→fork→action→outcome→ตัวเลือกผิดที่ดูถูก→escalation) เข้าสกิลหลัก = ทำให้เป็น "รุ่นพี่ที่เคยเจอ" จริง (ตรงกับ U)
- **auto-invocation**: gen platform adapter จาก registry + Thai-synonym/symptom trigger + routing precision/recall test (insight จาก `obra/superpowers`)
- 🔑 **real-validation outreach** — *ทางเดียวข้าม L6→L7+*: MT จริงเซ็น (L7) + junior MT ทดสอบ rescue-rate (L8). แพงแต่นี่คือที่ value พิสูจน์

## W5 — Catalog-Steward (capstone · self-curation)
ดู [`catalog-steward.md`](./catalog-steward.md) — loop auto-detect → propose lifecycle op → gate → apply. ทำให้คลัง "มีชีวิต ดูแลตัวเอง" โดยไม่กินตัวเอง. **ต้องมี W2 ก่อน** (ใช้ tier-signal + dedup + credit เป็น input)

---

## Discipline ที่ห้ามหลุด (ทุก wave)
- สกิลใหม่/แก้เนื้อ → **codex review (take/drop) → PR** · clinical = flag-only
- catalog แตะ skills/ → `build_triage.py` + commit catalog ก่อน push (ไม่งั้น CI แดง)
- **ห้าม `git add -A`** ตอนมี WIP ผู้ใช้ใน tree → stage pathspec เจาะจง
- verify เนื้อ commit ด้วย `git show <branch>:<file>` ไม่เชื่อ worktree
