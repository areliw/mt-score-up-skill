# Self-audit — T-shaped expansion clinical skills — 2026-06-08

> ✅ **RESOLVED 2026-06-08 (same day)** — adversarial clinical self-audit of the 5 new clinical/compliance
> skills from the T-shaped expansion, run **before** human peer-review (per `docs/how-we-audit.md`).
> All actionable findings fixed in this commit. Kept as a quality-process record.

**Method:** 5 parallel independent `healthcare-reviewer` agents — one per skill — each prompted to
*adversarially* hunt clinical/compliance errors (reversed direction, wrong cutoff, mis-stated mechanism,
dangerous shortcut, scope violation), calibrated against the prior 2026-06-03 audit's error class
(Bombay/anti-H, Jaffe-GFR direction). Every finding was then verified by the maintainer before fixing.

**Result:** 5 skills reviewed · **1 true clinical error** + a set of accuracy/completeness gaps · 2 skills
returned clean (`urinalysis`, `flow-cytometry` — sound, only minor precision nits). No false-positive padding.

---

## 🔴 True error (fixed)
**1. [HIGH] `preanalytical-judgment.md` Fork 1 — EDTA carryover Mg direction REVERSED**
Stated `EDTA carryover → ... Mg↑`. WRONG — EDTA **chelates** divalent cations, so contamination **lowers**
Mg (and Ca, and ALP via metalloenzyme inhibition): triad ↑K / ↓Ca / ↓Mg / ↓ALP. (The file's own
anti-pattern #3 already omitted Mg, so Fork 1 was internally inconsistent.) Note the genuine contrast,
now made explicit: **EDTA → Mg↓ (chelation)** vs **hemolysis → Mg↑ (intracellular leak)** — the Fork 3
hemolysis `Mg↑` was correct and was left unchanged.
→ **Fixed:** `K↑ Ca↓ Mg↓ ALP↓` + added the EDTA-vs-hemolysis contrast line.

## 🟠 Accuracy / completeness (fixed)
- **`poct-judgment`** — interference stated without direction/method. Added: **Hct high → glucose falsely
  LOW** (low Hct/anaemia → falsely high; dangerous in ICU/renal/neonate); **O₂ interferes only with
  glucose-oxidase** methods; **GDH-PQQ + maltose/icodextrin(PD)/galactose → falsely HIGH glucose → fatal
  insulin overdoses (FDA warning)**; AMR/reportable-range note. Tightened ISO claim (15189:2022 absorbed
  POCT; ISO 22870 withdrawn).
- **`flow-cytometry-judgment`** — **FMO is the gating control; isotype controls no longer recommended**
  (file had lumped "FMO/isotype"). Added blast-gate direction (**CD45-dim, low SSC**) and PNH nuance
  (**FLAER for WBC; RBC assessed with CD59**).
- **`phi-data-handling`** — added the load-bearing PDPA facts: **health/lab/genetic data = sensitive
  (§26)** needs explicit consent / medical-research exception (not §24 contract/legal-duty);
  **pseudonymized/key-coded ≠ anonymous** (still personal data); **breach → controller must notify PDPC
  within 72 h** + data subjects on high risk ("tell DPO = done" is wrong); small-cell **complementary
  suppression** (totals leak); fuller data-subject rights (§30–34).

## 🟡 Precision nits (fixed where cheap)
- **`urinalysis-judgment`** — clarified Ca-oxalate **dihydrate = envelope vs monohydrate = dumbbell/needle**
  (the monohydrate form is the one tied to ethylene-glycol AKI). Otherwise confirmed sound: MSU/CPPD
  birefringence signs correct, nitrite/LE logic correct, cast→disease map correct, Bence-Jones gap correct.

## ✅ Clean (no clinical errors)
- `urinalysis-judgment` and `flow-cytometry-judgment` — the reversible-logic landmines (birefringence sign,
  PNH markers, gating order, cast associations) were all stated correctly on first write.

> Status unchanged: these skills remain `status: draft` and still warrant **human MT peer-review** before
> promotion. This self-audit reduces — does not replace — that step.
