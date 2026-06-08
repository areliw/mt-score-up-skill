# Round 4 — spot-A/B of the v0.6.0 skills (the 8 newest)

> The round-1 scorecard ran on the 53 skills that existed at eval time. This is a
> **lighter screen** of the 8 clinical/data skills added in v0.6.0 (urinalysis,
> preanalytical, poct, flow-cytometry, method-validation-stats, phi-data-handling,
> spreadsheet, mt-databases) — which had never been A/B'd. The point is a **safety
> screen** (does any new skill make a weak model *worse*?), not a graded scorecard.

## Method (and how it's weaker than round 1)

For each skill: its **own #1 anti-pattern** → a realistic trap scenario. A **weak model
(Claude Haiku)** answers the scenario twice — **WITHOUT** the skill, then **WITH** it
(reads the skill file first). Trap-avoidance compared.

**Caveats — this is not the full round-1 rigor:**
- traps were **self-derived** (not strong-model-derived), **single-pass** (no 2-run averaging),
  and **assessed, not blind-judged** by an independent model. Treat as a screen, not a grade.
- one scenario per skill — misses edge cases a fuller harness would hit.

## Result — 8/8 tie · 0 rescue · 0 regression

| skill | without-skill (Haiku cold) | with-skill | Δ |
|---|---|---|---|
| method-validation-stats | avoided (r≠agreement → Bland-Altman, bias, LOA) | avoided + PB/Deming, TEa, CLSI EP09 | tie |
| urinalysis | avoided (strip↔micro discordance, delay overgrowth, don't call UTI) | avoided + LE/nitrite reasons, "await culture" | tie |
| preanalytical | avoided (hemolysis→K↑ false, redraw not rerun) | avoided + Fork refs | tie |
| poct | avoided (QC mandatory, accuracy, liability) | avoided + ISO 15189:2022 POCT, Hct/O₂ interference | tie |
| flow-cytometry | avoided (doublet+viability artifact, redo gating) | avoided + exact gate order, FMO control, correlate smear | tie |
| phi-data-handling | avoided (quasi-identifiers re-identify, generalize/shift) | avoided + DPO/IRB, k<5 suppression | tie |
| spreadsheet | avoided (autoconvert corrupts, no-red≠ok, import-as-text) | avoided + undo, format-text-first | tie |
| mt-databases | avoided (device/human loss, backup 2 places, version) | avoided + don't-edit-raw, audit trail | tie |

## What this means (honestly)

- **0 regression** — the result that matters for safety: **no new skill made the weak model
  worse**. Loading any of the 8 was at least as good as not.
- **0 rescue** — even a weak model already avoids these #1 traps **cold**, because each #1
  anti-pattern is a *textbook* pitfall (r≠agreement, hemolysis→K, POCT-needs-QC,
  gating artifacts, quasi-identifiers, Excel autoconvert, backup). So: ties.
- The skill's contribution was **consistent polish** — the right standard (EP09, ISO 15189),
  the exact procedure (gate order, k-anonymity, redraw-don't-rerun), the governance step
  (DPO/IRB). That is the documented value of these skills: **consistency + a forcing
  function**, not rescuing a model that already knows.

## Limitation that points to the real validation

**Claude Haiku is "weak" but still carries broad textbook knowledge a *real junior MT*
might not have yet.** A genuine rescue likely appears with actual non-experts (a
first-week MT, a nurse running POCT) — which **only human testing can show**. This screen
confirms the skills are *safe* to load; it does not (and cannot) prove the rescue value
the skills are designed for. Put the triage in front of real junior MTs — that's the test
that counts.

*Reconfirms round-1's core finding: these skills lift a weak reasoner / non-expert and act
as consistency rails for everyone — they don't boost a model that already embodies the
judgment. No skill is dangerous; the value is audience-specific.*
