# Round 3 — the honest measurement (fixed set + averaged + harder)

Round 2 ended with a warning: a single A/B run is too noisy to trust. Round 3 fixes the
*measurement*, not the skills. Three changes, all aimed at telling the truth, not boosting a
number:

1. **Fixed scenario set** — each skill's hard scenario is derived ONCE and saved
   (`scenarios.json`). Same questions every future run → before/after becomes comparable.
2. **Harder scenarios** — "expert-level traps" (conflicting data, ambiguous history, a
   tempting-but-wrong shortcut) so a capable weak model can still fall in. More discriminating.
3. **Two runs, averaged** — each scenario is answered + judged twice and averaged, so a lucky
   spike in either direction cancels instead of counting as a "win."
4. **Text-tag judge** (no forced JSON schema) — fixes the StructuredOutput bug that silently
   dropped judges in round 2.

(We deliberately did **not** bias the judge toward our edit-style — that would manufacture
lift and make the number unpublishable. The rubric is substance-first, applied blind to both.)

## Result: the honest lift is *lower*, and that's the point

| | R1 (1 run) | R2 (1 run, fresh) | **R3 (2-run avg, fixed, harder)** |
|---|---|---|---|
| lift | 25 | 25 | **19** |
| neutral | 19 | 15 | **23** |
| backfire | 9 | 4 | **2** |
| judged | 53 | 44 | 44 |

Averaging pulled ~6 "lifts" back to neutral. They were **noise**, not signal. Chasing the 25
was chasing luck. The real, noise-reduced lift is ~19 — and the base is rock-solid:

- **0 regressions, 0 no-rescues** after averaging. The 2 "backfires" (`mt-career`,
  `optimization`) are both cases where **both answers were correct** and the with-skill answer
  merely lost style points — not a safety problem.
- **8 bulletproof lifts** — Δ≥1 *and* spread≤1 (identical verdict across both runs):
  `parasitology`, `self-development-coach`, `pharmacology`, `what-skill-do-i-need`,
  `sample-size-power`, `mt-law-ethics`, `anti-hallucination`, `ml-judgment`. These are the
  skills you can trust to lift a weak model every time.

## The noise number (the real finding)

**`avgSpread = 1.39`.** On the *identical* scenario, the two runs' scores differed by ~1.39
points (summed over both answers, ~0.7 per answer). One skill (`applied-microbiology`) swung
its without-skill score **5 → 1** on the same question. **The noise lives in the weak answerer
(Haiku), not the judge** — Haiku gives materially different answers to the same prompt. So:

> A delta must clear **~1.4** to be real signal. Any single-run A/B that reports per-skill
> deltas below that is reporting coin-flips. Averaging (or a stronger, more deterministic
> answerer) is mandatory, not optional.

## Tactic scorecard (what was asked vs what the data justified)

1. **Harder scenarios** — ✅ done; raised discrimination.
2. **Biased judge** — ❌ refused; it manufactures lift and destroys credibility (the one thing
   this eval is *for*). Used a substance-first blind rubric instead.
3. **Recover the unjudged** — ✅ switched judge to text tags (fixed the schema bug). But 9 of
   the *largest* skills still dropped — not the schema now, but agent failures when the full
   (long) skill text is stuffed into the 6-agents-per-skill structure. Cheap recovery path:
   re-run just those 9 with truncated skill text. They were all judged in R1 (mostly tie/style).
4. **Negative constraints** — the data says **don't sweep all 53**: with 0 real regressions,
   blanket "don't do X" rules would be a fix looking for a problem (and bloat). Applied
   surgically where the data pointed (the `polite-but-clear` life-critical carve-out in R2).

## Bottom line

The skills' honest value: **~8 bulletproof lifts + ~11 softer lifts, 0 dangerous regressions,
on harder scenarios** — for a weak model / non-expert. Frontier models still don't need them.
The biggest deliverable here isn't the 19; it's the **fixed scenario set + the 1.4 noise floor**,
which make every future before/after measurement trustworthy instead of a coin-flip.

## Update — all 53 recovered

The 9 dropped skills were re-run single-pass (3 agents each instead of 6 → fewer failure
points) and **all 9 came back**. So it was transient agent failure, not skill size. Combined
(44 two-run-averaged + 9 single-run):

**lift 26 · neutral 24 · backfire 3** — kinds: rescued 8 · better 18 · tie 24 · style 3 ·
**regression 0 · no-rescue 0** across all 53.

The headline win: **the two round-1 no-rescues both became lifts** — `know-yourself` +3 and
`offload-to-automation` +2. These were the skills whose value is *procedural* (dig for the
metrics before drafting; offload the calc to a tool), and the round-2 edits that added an
unmissable top trigger **demonstrably fixed exactly those two.** On genuinely hard clinical
scenarios the skills also rescue a weak model decisively — e.g. `clinchem` **+4**: without the
skill the weak model released an ICU K⁺ = 6.8 from a QC-failed run (a dangerous error); with
it, it held the whole batch.

(The 9 are single-run, so noisier than the averaged 44 — treat their deltas as provisional.)

*Artifacts: `scenarios.json` (the fixed 53-scenario set), `results.json` (per-skill scores;
the 44 carry both-run data + spread, the 9 are single-run).*
