# Changelog

Notable changes to the MT Score UP! skills hub. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/). Every skill is `status: draft` —
content เรียบเรียงจากองค์ความรู้มาตรฐาน, ยังไม่ผ่าน formal clinical peer-review.

## [Unreleased] — T-shaped MT expansion (waves 1–3)

### Added
- **`urinalysis-judgment`** (#56) — UA + body-fluid (CSF/serous/synovial) microscopy: strip↔micro↔clinical
  correlate, `nitrite-neg ≠ no UTI`, cast/crystal significant-vs-artifact, gout vs pseudogout under polarized
  light. Closes a core lab-bench coverage gap (clinical microscopy had no standalone skill).
- **`preanalytical-judgment`** (#57) — pre-analytical/phlebotomy = error #1 of the lab (~60–70%): order of
  draw, tube/ratio, HIL → which analyte breaks, timing/tourniquet/IV-line, `rerun ≠ recollect`,
  wrong-blood-in-tube. Consolidates guidance that was scattered across 11 files.
- **`build-a-dashboard`** (#58) — first **T-shaped MT** skill: MT builds their own dashboard (TAT/QC/workload)
  — question-before-chart, tool choice (Sheets/Looker/Power BI/Streamlit), non-deceptive charts (median TAT),
  and a PDPA-first trap (no patient HN/row-level data on cloud). Reframes dev judgment for non-coder MTs.
- **`docs/EXPANSION-PLAN.md`** — full no-omission manifest mapping every tier of source skills (dev/design/
  data/business/productivity/AI/process) → MT-reframed repo skills, organised into 9 tracks + build waves.

### Added — wave 2 (MT++ T-shaped core, 58 → 64)
- **`automate-lab-tasks`** (#59) — when repetitive lab work is worth automating (ROI) + how not to fail
  silently (validate/alert/idempotent/human-in-loop). Reframes `offload-to-automation` + `python-coach`.
- **`clean-messy-data`** (#60) — clean lab/research data before analysis: look-at-raw-first, keep raw + log,
  ordering (structural→values→missing→dup), date hell, regex-vs-AI, blank≠0. From `data-project-survival` + `regex-vs-llm-structured-text`.
- **`vibe-coding-safely`** (#61) — let AI write code without it breaking/leaking, for non-coders:
  "runs ≠ correct", known-answer verify, never paste PHI/keys, don't run commands you don't understand.
  From `python-coach` + `python-testing` + `error-handling` + `safety-guard` + `e2e-testing`.
- **`ship-a-small-app`** (#62) — build a small team tool (calculator/form/mini-dashboard): smallest-thing-first,
  no-code/low-code first, auth+PDPA from the start, verify clinical formulas. From `deployment-patterns` + `fastapi-patterns` + `docker-patterns`.
- **`spreadsheet-judgment`** (#63) — use Excel/Sheets right + prevent silent error: stop autoconvert wrecking
  IDs/dates/genes, tidy data, VLOOKUP-exact/STDEV.S-vs-P, data validation, median TAT, when to move to a DB.
- **`mt-databases`** (#64) — where to store data (Sheets/Access/SQL/REDCap) by size×users×relationships +
  non-DBA design (1 entity/table, unique id, backup, conditional DELETE). From `db-judgment` + `postgres-patterns` + `database-migrations`.
- Manifest closed to **97/97** source skills (added `mle-workflow`, `python-testing`, `scientific-pkg-gget`)
  with a completeness ledger in `docs/EXPANSION-PLAN.md`.

### Added — wave 3 (stats/research + remaining lab gaps, 64 → 72)
- **`method-validation-stats`** (#65) — MT-specific stats the general stat skills don't cover: method comparison
  (Bland-Altman + Passing-Bablok/Deming, *not* r/paired-t), reference interval (CLSI EP28, n≥120),
  diagnostic accuracy (PPV depends on prevalence), precision/CV/sigma, kappa. From `mt-stats-helper`.
- **`pubmed-search`** (#66) — literature search: PICO→MeSH+synonym+Boolean, smart filters, "not found ≠ doesn't
  exist", verify PMIDs (AI fabricates citations). From `scientific-db-pubmed-database`.
- **`source-credibility`** (#67) — how much to trust a source: screen predatory journals, evidence hierarchy,
  COI/retraction, "high IF / peer-reviewed ≠ correct". From `scientific-thinking-scholar-evaluation`.
- **`deep-research`** (#68) — multi-source research: triangulate ≥2–3 independent sources, cross-check,
  synthesise with confidence levels, cite + verify, guard confirmation bias. From `deep-research`.
- **`gget-genomics`** (#69) — pull gene/variant/structure via gget (Ensembl/NCBI/UniProt/AlphaFold);
  genome-build trap (hg19↔hg38), presence ≠ pathogenic (classify by ACMG), PHI. From `scientific-pkg-gget`.
- **`poct-judgment`** (#70) — point-of-care testing = lab outside the lab (ISO 15189:2022): when POCT vs central,
  QC + operator competency + connectivity, interference (Hct), confirm/report critical values. Net-new.
- **`flow-cytometry-judgment`** (#71) — gate correctly (singlet/viable/CD45-SSC), read pattern not single
  marker, leukemia/lymphoma/PNH/CD4/MRD, correlate morphology. Net-new (closes the last bench gap).
- **`deploy-ml-safely`** (#72) — take a trained model to real use ("accurate in training ≠ usable"):
  external validation, data drift + monitoring, fallback/reject option, human-in-the-loop for clinical use,
  versioning + IRB. From `mle-workflow` + `ml-judgment`. Ties to the user's smear-classifier thesis.

### Notes
- `skills/INDEX.md`, `dist/all-skills.md`, `prompts/triage.md` regenerated via `scripts/build_triage.py`
  (72 skills, no drift). README + skills/README counts bumped 55 → 72.
- Every MT++ skill ties its #1 trap to **patient-data safety (PDPA)** + verify-against-source — the line
  generic dev guidance omits but MTs cannot. Lab-bench coverage now complete (UA/body-fluid · pre-analytical
  · POCT · flow added to the original 14 clinical skills).

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
