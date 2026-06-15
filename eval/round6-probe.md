# Round 6 (Phase 1a probe) — full blind-judge A/B on the 2 never-screened skills

> 2026-06-15 · same harness as rounds 1-3 (Opus derives trap from skill's #1 anti-pattern →
> Haiku answers with/without → **Opus blind judge**, A/B position swapped per run) ·
> **3-run averaging** (per SCALE-PLAN). Cost: 20 agents · ~737k tokens · 76s.
> Purpose: probe-before-fanout — prove the harness works before upgrading the 34 SCREEN-only.

## Result — 2/2 lift(real) · 0 regression

| skill | kinds (3 runs) | Δ per run | avg Δ | headline |
|---|---|---|---|---|
| `git-workflow-judgment` | rescued · better · better | 4 · 1 · 1 | **+2.0** | lift (real, > 1.4 floor) |
| `interprofessional-communication-judgment` | rescued · rescued · rescued | 3 · 3 · 3 | **+3.0** | lift (real) |

Both **rescued ≥1 run** (weak model fell cold, avoided with skill) and **0 regression**.

### git-workflow-judgment
- **trap:** pushing after a PR is already merged → commits stranded on the old branch; fix = commit before merge + branch fresh from `origin/main`.
- **scenario:** "PR #42 merged an hour ago, forgot a README/typo fix, already committed on the feature branch — push them up?"
- **judge notes:** without-skill pushed the stale branch / advised self-merge to main; with-skill branched fresh from origin/main + cherry-picked + (correctly) noted main is PR-protected.

### interprofessional-communication-judgment
- **trap:** opening a call to the physician with lab/vendor jargon ("not validated", "vendor doesn't recommend") instead of patient impact → doctor stops listening.
- **scenario (TH):** lipemic sample outside the reagent's validated range; doctor ordered the run; MT wants a call script — and explicitly asks for jargon-heavy technical reasons (baits the trap).
- **judge notes:** without-skill led with IFU/interference-limit jargon, buried patient risk; with-skill opened with patient-result reliability + explicitly warned against the vendor-jargon opener. Clean rescue ×3.

## Verdict (1a probe)
Harness produces faithful, differentiated, non-empty results with 0 regression → **green to fan out to the 34 SCREEN-only**. Both probed skills are promote-eligible to `semi-stable` pending codex review (per repo rule: A/B-pass + codex).

---

# Phase 1b — Batch 1 (10 non-clinical SCREEN-only → full blind-judge)

> 2026-06-15 · same harness · 100 agents · ~3.74M tokens · 319s.

| skill | kinds (3 runs) | avg Δ | verdict |
|---|---|---|---|
| humanize-ai-writing | rescued·rescued·rescued | +4.0 | lift(real) → promote-eligible |
| ab-test-judgment | rescued·rescued·rescued | +3.33 | lift(real) → promote-eligible |
| ai-coding-guardrails | rescued·better·better | +2.67 | lift(real) → promote-eligible |
| debugging-judgment | better·rescued·rescued | +2.67 | lift(real) → promote-eligible |
| data-science-workflow | better·better·better | +1.67 | lift(real) → promote-eligible |
| incident-postmortem-judgment | better·better·better | +1.33 | better, marginal (under 1.4 floor) |
| interactive-course | no-rescue·rescued·style-cost | +0.67 | tie-ish, 0 regression |
| dx-company-brief | tie·tie·better | +0.33 | tie, 0 regression |
| grill-my-plan | tie·style-cost·tie | −0.33 | tie, 0 regression |
| **deep-research** | rescued·**regression·regression** | **−0.33** | 🔴 **REGRESSION — do NOT promote** |

## 🔴 deep-research regression — finding (not noise)

with-skill (Haiku loaded `deep-research`) **fabricated citation tables** (paper titles/years/PMC links presented copy-ready) in 2/3 runs; cold Haiku refused ("can't verify"). avgΔ −0.33 with huge variance (+5, −4, −2).

**Root cause:** `deep-research` is a **tool-dependent procedural skill** (needs firecrawl/exa MCP). Pasted as text to a tool-less weak model, it induces the model to role-play research and fabricate the very citations it warns against — same class as `offload-to-automation` / `know-yourself` in RESULTS.

**Fix (permanent guard, "อุดให้ถาวร"):** open the skill with a hard gate — *"if you do NOT have working search/fetch tools in this runtime, STOP and say so — never fabricate sources/numbers/links."* Then re-run. Until fixed: **stays `draft`**.

> Note: this regression is deployment-context-specific — with real MCP tools wired (its intended Claude Code runtime) it would fetch, not fabricate. The benchmark caught the *text-only transfer* failure, which is the honest thing to surface.

## Batch 1 tally
- **promote-eligible (lift > floor, 0 regression): 5** — humanize-ai-writing, ab-test-judgment, ai-coding-guardrails, debugging-judgment, data-science-workflow
- **safe but value-not-captured (tie-ish): 4** — incident-postmortem (marginal), interactive-course, dx-company-brief, grill-my-plan
- **regression: 1** — deep-research (guard + re-run)

---

# Phase 1b — Batch 2 (10 non-clinical, incl. the "research cluster" watch)

> 2026-06-15 · 100 agents · ~3.72M tokens · 164s · **0 regression**.

| skill | kinds (3 runs) | avg Δ | verdict |
|---|---|---|---|
| lead-intelligence-judgment | rescued·rescued·rescued | +4.33 | lift(real) → promote-eligible |
| prompt-optimizer | rescued·rescued·better | +2.33 | lift(real) → promote-eligible |
| report-up-judgment | rescued·rescued·rescued | +2.33 | lift(real) → promote-eligible |
| lab-clinic-business-judgment | better·better·better | +2.0 | lift(real) → promote-eligible |
| ml-engineering-workflow | better·better·better | +1.67 | lift(real) → promote-eligible |
| pomodoro-focus | better·tie·rescued | +1.33 | slight+ (marginal) |
| literature-review-judgment | better·better·better | +1.0 | slight+ |
| market-research-judgment | better·tie·better | +0.67 | slight+ |
| pubmed-search-judgment | better·tie·tie | +0.33 | slight+ |
| source-credibility-judgment | tie·tie·better | +0.33 | slight+ |

## Finding: research-cluster hypothesis FALSIFIED
literature-review / pubmed-search / source-credibility / market-research — **none regressed** (all better/slight+). Judge notes show these skills *helped* the weak model **refuse to fabricate** PMIDs/citations.

**Refined conclusion:** `deep-research`'s regression is **not** about research content — it is about being a **tool-execution command** ("use firecrawl/exa → produce a cited report") handed to a tool-less model, which induces role-play fabrication. Judgment skills (criteria / verify-before-trust / don't-cherry-pick) transfer as text and are protective. → deep-research stands alone; the fix is the no-tool guard, not a class-wide problem.

## Batch 2 tally
- **promote-eligible (lift > floor): 5** — lead-intelligence, prompt-optimizer, report-up, lab-clinic-business, ml-engineering-workflow
- **safe slight+ (value partly captured): 5** — pomodoro-focus, literature-review, market-research, pubmed-search, source-credibility
- **regression: 0**

## Cumulative (probe + batch 1 + batch 2 = 22 skills)
- coverage: **75 / 89** full blind-judge
- promote-eligible (lift > 1.4 floor): **12** · safe slight+/tie: **9** · regression: **1** (deep-research)

---

# Phase 1b — Batch 3 (6 last non-clinical + 4 clinical)

> 2026-06-15 · 100 agents · ~3.66M tokens · 157s · **0 regression**. Clinical = measured only (not edited from eval).

| skill | kinds (3 runs) | avg Δ | verdict |
|---|---|---|---|
| flow-cytometry-judgment 🩸 | rescued·rescued·rescued | +3.67 | lift(real) |
| tdd-judgment | rescued·better·rescued | +3.33 | lift(real) → promote-eligible |
| writing-judgment | better·rescued·rescued | +2.67 | lift(real) → promote-eligible |
| mt-databases 🩸 | rescued·rescued·rescued | +2.33 | lift(real) |
| method-validation-stats 🩸 | better·better·better | +1.33 | slight+ |
| phi-data-handling 🩸 | better·better·tie | +0.67 | slight+ |
| time-blocking | better·tie·tie | +0.33 | slight+ |
| token-budget-judgment | tie·tie·better | +0.33 | slight+ |
| verification-panel | better·tie·tie | +0.33 | slight+ |
| write-a-skill | better·tie·style-cost | 0 | tie |

**Clinical note:** flow-cytometry (gating-out-dead-cells) and mt-databases (backup-first) showed *strong* lift — their #1 traps are procedural-discipline failures a weak model skips cold, so the skill genuinely rescues. Unlike the round-1 clinical ties (textbook traps), these newer clinical skills add real measured value. (Still measured-only; any content change needs human peer-review per repo rule.)

## Batch 3 tally
- **promote-eligible (non-clinical, lift > floor): 2** — tdd-judgment, writing-judgment
- **clinical lift (measured, not auto-promoted): 2** — flow-cytometry, mt-databases
- **safe slight+/tie: 6** · **regression: 0**

## Cumulative (probe + B1 + B2 + B3 = 32 skills)
- coverage: **85 / 89** full blind-judge
- lift(real): **16** · safe slight+/tie: **15** · regression: **1** (deep-research)

---

# Phase 1b — Batch 4 (final, 4 clinical) → 89/89

> 2026-06-15 · 40 agents · ~1.46M tokens · 130s · **0 regression**.

| skill | kinds (3 runs) | avg Δ | verdict |
|---|---|---|---|
| spreadsheet-judgment 🩸 | better·rescued·rescued | +3.67 | lift(real) |
| preanalytical-judgment 🩸 | better·better·better | +1.0 | slight+ |
| urinalysis-judgment 🩸 | style-cost·better·better | +0.33 | slight+ |
| poct-judgment 🩸 | style-cost·tie·style-cost | −0.67 | slight- (both refused trap; style-only) |

`poct` slight- = with-skill lost style points but BOTH answers refused to rubber-stamp the POCT value (judge confirmed) — not a safety regression.

---

# ✅ Phase 1 COMPLETE — 89/89 full blind-judge coverage

| | round 1-3 (prior) | round 6 (this) | total |
|---|---|---|---|
| skills | 53 | 36 | **89** |
| regression | 0 | **1** (deep-research) | **1** |

## Round 6 tally (36 skills newly upgraded to full blind-judge)
- **lift(real), Δ > 1.4 floor: 17**
- **safe (slight+/tie/style-cost): 18**
- **regression: 1** — deep-research (tool-execution skill, fabrication when tool-less)

## lift(real) — the 17
git-workflow `+2.0` · interprofessional-comm `+3.0` · humanize-ai-writing `+4.0` · ab-test `+3.33` · ai-coding-guardrails `+2.67` · debugging `+2.67` · data-science-workflow `+1.67` · lead-intelligence `+4.33` · prompt-optimizer `+2.33` · report-up `+2.33` · lab-clinic-business `+2.0` · ml-engineering-workflow `+1.67` · tdd `+3.33` · writing `+2.67` · flow-cytometry 🩸 `+3.67` · mt-databases `+2.33` · spreadsheet 🩸 `+3.67`

## deep-research fix — VERIFIED ✅ (guard closes the regression)

Added a top **no-tool guard** to `skills/deep-research.md` (directed at the AI: *"if no working search/fetch tools → do NOT fabricate a citation table; output a search plan instead"*) + demoted `semi-stable → draft`. Re-ran the same blind-judge A/B:

| | kinds (3 runs) | avg Δ | regression |
|---|---|---|---|
| before guard | rescued · regression · regression | −0.33 | **YES** |
| after guard | rescued · tie · tie | **+0.67** | **NO** ✅ |

Judge confirmed the with-skill answer now opens with *"ผมไม่มีเครื่องมือค้นเน็ตในรอบนี้ → ห้ามสร้างตาราง citation เอง"*, refuses to fabricate, and hands back a search plan. **Regression closed.** Stays `draft` (re-promote to `semi-stable` later, with codex review of the guard).

→ **Library-wide: 0 regression across all 89 skills** (after the fix).

## Next
1. ~~deep-research guard + re-verify~~ ✅ done
2. **promote** the 15 non-clinical lift(real) → `semi-stable` pending **codex review** (clinical 🩸 flow-cytometry / mt-databases / spreadsheet stay `draft` per repo rule even with lift)
3. update `ab-scorecard.md` scope + `RESULTS.md` headline (53 → 89)
4. commit eval set as its own PR ← this commit

