# Changelog

Notable changes to the MT Score UP! skills hub. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/). Every skill is `status: draft` —
content เรียบเรียงจากองค์ความรู้มาตรฐาน, ยังไม่ผ่าน formal clinical peer-review.

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
