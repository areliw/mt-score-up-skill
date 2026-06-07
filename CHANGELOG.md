# Changelog

Notable changes to the MT Score UP! skills hub. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/). Every skill is `status: draft` —
content เรียบเรียงจากองค์ความรู้มาตรฐาน, ยังไม่ผ่าน formal clinical peer-review.

## [0.5.0] — 2026-06-08

### Added
- **+14 skills (65 → 79)** — port จากคลัง global `~/.claude/skills` ที่ใช้คู่ Life OS → reframe เป็นภาษาไทย/audience MT/วางในแชตได้ (ตัด Claude-Code/IDE-only + knowledge-only ออก):
  - 🔬 `source-credibility-judgment` · `pubmed-search-judgment`
  - 💻 `tdd-judgment` (merge tdd+python-testing) · `debugging-judgment` (merge debug-mantra+diagnose) · `ai-coding-guardrails` (karpathy)
  - 🤖 `token-budget-judgment`
  - 💬 `writing-judgment` · `report-up-judgment` (reframe management-talk → lab/รพ.)
  - 💼 `market-research-judgment` · `lead-intelligence-judgment` · `incident-postmortem-judgment` (reframe post-mortem → lab NC/CAPA)
  - 🧭 `pomodoro-focus` · `time-blocking` · `interactive-course`

### Changed
- README counts 65→79 (3 จุด) + `dist/all-skills.md` (~105K→~125K tokens) · build_triage regenerated INDEX/triage/bundle (79, in-sync) · eval honesty note: 26 ตัวยังไม่ A/B

### Notes
- ทั้ง 14 = non-clinical · `status: draft` · ยังไม่ผ่าน weak-model A/B
- ตัด ~30 ตัวจาก global ที่ off-mission (frontend/video/Claude-Code-meta เช่น overnight/handoff/ultracode, knowledge-only เช่น python-patterns) — ไม่เข้า audience MT
- merge ตัวซ้ำ: tdd+python-testing → `tdd-judgment` · debug-mantra+diagnose → `debugging-judgment`

## [0.4.0] — 2026-06-08

### Added
- **+10 skills (55 → 65)** — ชุด AI-usage / research / data / decision / sales ที่คลังยังขาด:
  - `prompt-optimizer` (#65) — วินิจฉัย+ซ่อม prompt: แก้สาเหตุที่ใช่ก่อน · few-shot · สเปก output · ไม่ยัดยาวเฟ้อ
  - `verification-panel` (#64) — ตั้งคณะตรวจ 3 มุม (Factual/Logic/Context) แบบ adversarial ก่อนเชื่อคำตอบ high-stakes
  - `write-a-skill` (#63) — แพ็กวิจารณญาณเป็น skill (judgment-not-knowledge test, type fork, PII, ส่งเข้า repo) — เป็นคู่มือ contributor ในตัว
  - `humanize-ai-writing` (#62) — เกลางานที่ AI ร่างให้เป็นคนเขียน ตัดสัญญาณ AI โดยคงความถูกต้อง/ศัพท์
  - `literature-review-judgment` (#61) — กระบวนการรีวิววรรณกรรม (search→screen→synthesize) เสริม `critical-appraisal-judgment` (อันนั้น = ประเมินเปเปอร์เดียว)
  - `deep-research` (#60) — ค้นเรื่องใดก็ได้ลึก หลายแหล่ง + cross-check ≥2 แหล่ง + cite ตรวจได้
  - `data-science-workflow` (#59) — CRISP-DM phase navigator (กัน leakage / vanity metric / skip Business)
  - `ml-engineering-workflow` (#58) — นำโมเดลขึ้นใช้จริง: reproducible train · shadow/A-B · monitor drift · rollback
  - `grill-my-plan` (#57) — ให้ AI ซักไซ้แผนแบบ adversarial ก่อน decision แก้ยาก
  - `dx-company-brief` (#56) — brief บริษัท diagnostics ก่อนสัมภาษณ์/ขาย (6-section + verify ตัวเลขตลาด)

### Changed
- README category tables + counts (55→65, 3 จุด) + `dist/all-skills.md` token estimate (~90K→~105K)
- `scripts/build_triage.py` regenerated INDEX / triage catalog / bundle (65 skills, in-sync)
- eval honesty note: ตัวที่เพิ่มหลัง eval-53 รวมเป็น 12 ตัวที่ยังไม่ A/B (ผ่าน design review)

### Notes
- ทั้ง 10 ตัว = non-clinical (AI/วิจัย/data/อาชีพ) → disclaimer ระดับเบาตามความเสี่ยง · `status: draft` · ยังไม่ผ่าน weak-model A/B (รอ round ถัดไป)

## [0.3.0] — 2026-06-07

### Added
- `ab-test-judgment` (#55) — general judgment for evaluating prompt/skill changes without chasing
  noise: credible design (own-worst-case + blind judge, no biased-judge), delta-of-deltas with a
  control, noise floor, review-vs-A/B, and scaling (test by risk×uncertainty, not count).
- `lab-clinic-business-judgment` (#54) — MT lab-clinic business: model choice (premium vs state-volume
  vs hybrid), the real moat (profession+registration+LIS-HIS), gov revenue, reading the buyer.
- `eval/IMPROVE-PLAYBOOK.md` — how to lift a skill + how to validate an edit via a controlled
  before/after (without-skill = noise control). Worked example: a per-edit A/B can't resolve a <1pt
  change against ±2–3 noise → judge edits by review, use the A/B only at library-aggregate level.
- `eval/round3/` — fixed-scenario, 2-run-averaged, harder-trap re-eval + recovery of all 53. Honest
  lift is *lower* than the noisy number (noise removed), with 0 dangerous regressions.

### Changed
- Critical "would-it-break-for-a-real-user" review over all 55 skills (**0 critical · 0 needs-work**)
  → fixed 8: `financial-statement` AFS→FVOCI (IFRS 9 currency); `bloodbank` ×5 clinical polish
  (platelet plasma-risk, Cryo-fallback, FFP→PCC, weak-D rule); `mt-career`, `ai-assistant-calibration`,
  `what-skill-do-i-need`, `photography`, `ivd-sales`, `self-development-coach`.
- Credits genericized — dropped specific institution names, kept the gratitude + non-endorsement note.
- Skill count 53 → 55.

## [0.2.0] — 2026-06-04

### Added — a real evaluation (`eval/`)
- **A/B scorecard ([`eval/ab-scorecard.md`](eval/ab-scorecard.md)):** all 53 skills, each tested on
  its *own* #1 anti-pattern, answered twice by a **weak** model (Haiku) with/without the skill,
  blind-judged 0–5. Result: **9 rescued · 16 better · 19 tie · 7 style-cost · 2 no-rescue · 0 regression.**
  No skill made a weak model's correct answer wrong.
- **Literature cross-check ([`eval/literature-check.md`](eval/literature-check.md)):** 66 clinical/method
  claims across 22 skills vs AABB/ACOG/CLSI/KDIGO/NKF-ASN/peer-review → **43 supported · 23 nuanced ·
  0 contradicted · 0 unverified**. Nuances are currency/precision upgrades, logged with sources.
- **Titanic exemplar ([`eval/titanic/`](eval/titanic/)):** `ml-judgment`'s leakage trap quantified —
  selecting features outside CV fabricates **+0.031 ROC-AUC** of fake performance (reproducible script).
- **[`eval/METHOD.md`](eval/METHOD.md) + [`eval/RESULTS.md`](eval/RESULTS.md):** the 4-layer design, the
  honest verdict, and the threats to validity. Key finding: skills lift a *weak* model / non-expert;
  a frontier model already embodies the judgment (so for it they're consistency rails, not boosts).

### Changed
- `bloodbank-judgment`: two literature-driven precision upgrades — irradiation stated as "≥25 Gy
  central, ≥15 Gy minimum to any portion" (was flat 25 Gy); fetal-anemia surveillance now leads with
  **MCA-PSV Doppler**, demoting ΔOD450/amniocentesis to legacy.
- Skill count 51 → 53 (`know-yourself`, `mt-career-judgment`).

### Known limitations (updated)
- The eval is **one run** of a weak-model A/B + literature check + a code exemplar — *not* a powered
  clinical-outcome study, and the judge is itself an LLM. Per-skill grades carry run-to-run variance
  (documented). 23 literature nuances are captured in `literature-check.md` but **not yet folded into
  every skill body** — open work. Still a *thinking aide*, not a source of truth.

## [0.1.0] — 2026-06-03

First tagged version, so MT can cite a fixed version in documents / audit trails.

### Skills (51)
- 🩸 **Lab bench:** bloodbank · hematology · clinchem · chemistry-interpretation · clinmicro · applied-microbiology · immunoassay · molecular · pathology · parasitology · toxicology · pharmacology · clinical-correlation · infection-control
- 🔬 **Research:** critical-appraisal · r2r-research-proposal · research-design · choose-stat-test · sample-size-power · r2r-stats · manuscript
- 🧭 **Life/career:** mt-law-ethics · mt-exam-strategy · finance · financial-statement · ikigai · self-development · digital
- 💼 **Lab-mgmt / IVD:** lab-management · ivd-sales · crm · marketing · sales-psychology
- 🤖 **AI-use** · 💬 **comms** · 💻 **code/data** · 🗂️ **files**

### Safety scaffolding
- Clinical skills carry an in-body `verify-first` guard: decision-support not the final answer; pair with `anti-hallucination`; patient-affecting steps need MT/physician confirmation.
- Risk-tiered disclaimers (heavy for patient-safety skills, light for utility) — by design, documented in README.
- `STANDARDS.md` source-of-truth: ISO 15189:2022 · ISO 15190:2020 · AABB Technical Manual 21st (2023) · AABB Standards 35th (effective 1 Apr 2026). Monthly auto-recheck (ISO) flags a newer edition for human review (no silent edit).

### Known limitations
- `eval/` is a preliminary paired-prompt harness — error-reduction claims **not yet proven at scale**.
- Not yet clinical-peer-reviewed; intended as a *thinking aide*, not a source of truth.
