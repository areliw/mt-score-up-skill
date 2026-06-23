# METHOD — how we tried to find out if these skills are actually good

## The honest problem

A "judgment skill" here is a page of *when-to-choose-what* + *traps experts know*. The hard
part of validating it: **you can't ask a frontier model whether it's good** — a strong model
already embodies most of this judgment, so it answers the trap correctly with or without the
skill. Asking GPT-class models "is this skill helpful?" gives you a flattering null result.

So we triangulate with four layers, each attacking a different failure mode. None alone is
sufficient; together they're the most honest read we can give without a funded clinical RCT.

---

## Layer 1 — Correctness (adversarial audit)

**Question: is anything in here just wrong?** A skill that confidently states a wrong rule is
worse than no skill.

Two rounds of adversarial review (a strong model instructed to *attack* each clinical claim,
not agree with it) surfaced verified errors that were then fixed — e.g. a Bombay/anti-H case
routed through a prewarm row (a fatal-if-followed error), an inverted antibody rule-out, a
backwards Jaffe→GFR direction, "albumin↓ + normal LFT excludes liver." Record:
[`../docs/audit-2026-06-03.md`](../docs/audit-2026-06-03.md).

The point of writing these down: an eval that only reports wins is marketing. The audit is
the paper trail of the skills being *wrong* and getting fixed.

## Layer 1b — Literature cross-check

**Question: do the key claims hold up against authority?** For every clinical and methodology
skill, an agent pulls the 3 most *falsifiable* claims, WebSearches a real source
(AABB/ACOG/CLSI/CAP/guideline/peer-reviewed), and returns a verdict —
`supported | nuanced | contradicted | unverified` — with the citation. Results +
the precision fixes they triggered: [`literature-check.md`](literature-check.md).

This catches the subtler failure: a claim that's *directionally right but dated or
oversimplified* (e.g. "irradiate at 25 Gy" → should be "25 Gy central dose, ≥15 Gy minimum to
any portion"; "fetal-anemia surveillance with ΔOD450" → MCA-PSV Doppler now leads).

## Layer 2 — Helpfulness (trap-A/B on a weak model)

**Question: does loading the skill change what an answerer does, for the better?**

The design that makes this non-trivial:

1. **Ground truth from the skill itself.** A strong model reads each skill, takes its
   documented **#1 anti-pattern**, and writes a hard scenario engineered to bait exactly that
   trap. The skill's *own* worst case is the test — we don't get to pick a softball.
2. **A weak answerer (Claude Haiku).** Because a frontier model embodies the judgment already
   (no signal), we test on the audience the skill is actually for: a weaker model / a
   non-expert. Haiku answers the scenario **twice, independently** — once with no skill in
   context, once with the skill pasted first.
3. **A blind judge.** A different strong model scores both answers 0–5 on trap-avoidance
   **without being told which is which**, and reports which trap each did/didn't avoid.
4. **Effect = Δ (with − without)**, then classified by *what actually happened* (see below).

Full table: [`ab-scorecard.md`](ab-scorecard.md). Per-skill judge rationales: in the workflow
output.

**Evidence tiers (2026-06-24):** structured rows in `eval/_ab_slim.json` carry optional
`"tier": "full" | "manual" | "screen"`. Only **`full`** (Haiku+Opus blind harness) counts toward
`semi-stable`; same-session manual runs are **`manual`** — exploratory, not promotion-grade.
See [`ANTI-BIAS-PROTOCOL.md`](ANTI-BIAS-PROTOCOL.md).

### Why a raw "lift/neutral/backfire" tally isn't enough

A judge giving the with-skill answer one fewer style point when **both answers were clinically
correct** is not a safety problem — but it shows up as "backfire" in a naive count. So each
result is re-classified by the `trapAvoid` field into what it *means*:

| kind | what happened | reading |
|---|---|---|
| **rescued** | without fell in the trap, with avoided it | the skill worked |
| **better** | both avoided; with scored higher on quality | skill adds polish |
| **tie** | no meaningful difference | weak model already handled it |
| **style-cost** | **both correct**; with lost ≤1 style pt | not a safety issue |
| **no-rescue** | both fell in; skill didn't save a weak model | skill didn't transfer |
| **regression** | without was right, **skill caused the fall** | the dangerous case |

The `regression` row is the one that would actually condemn a skill. See RESULTS for the count.

### Layer 2 upgrade (2026-06-18) — control arm · selftest · split gates

Three refinements adapted from a teardown of `DietrichGebert/ponytail`'s benchmark harness
([study](../docs/design/study-ponytail.md)), proven on one discriminating trap
([probe](2026-06-18-harness-upgrade-probe.md)) and now the protocol for promote-grade runs:

1. **`--selftest` the judge before spending.** Each trap ships a pre-written *gold* answer
   (should score ≥4) and a *known-bad* answer (should score ≤2). Run the blind judge on these
   **first**; if the spread < 2 the instrument can't discriminate → fix the trap/judge before
   burning answerer runs. (Catches the failure mode where a flat result means "bad ruler", not
   "no effect" — cf. the textbook-trap ties where Haiku already knew the answer.)
2. **Third arm = control.** Add a *generic-careful* arm (a plain "answer carefully as a
   professional" system prompt, **no judgment scaffolding**) alongside baseline (null) and
   with-skill. Report **delta-of-deltas**: a skill must beat the control, not just the null —
   otherwise the "lift" may be *any* framing making the model try harder, not the specific
   judgment. (In the probe the control scored *below* baseline, so the skill's +3 was provably
   its domain judgment, not generic caution.)
3. **Split the score into axes.** Keep helpfulness 0–5, **plus** a binary **correctness/safety**
   gate (did it avoid the dangerous action?) **plus** a binary **specificity** gate (did it
   deliver the specific senior judgment the skill claims?). When a trap is "safe for every arm"
   (correctness all-pass), specificity is what still measures the skill — rescuing cases that
   a single helpfulness average would score as a tie.

**Mental model — run an eval like a gel/assay.** The three upgrades are really one thing an MT
already does on every run: a **control panel**. No one reports a gel where the positive control
didn't run or the negative lane lit up — an eval result without its controls is just as
untrustworthy.

| gel/assay lane | must… | eval-harness equivalent |
|---|---|---|
| **negative control** (no template) | stay blank | null/baseline arm + known-bad ref must score **low** — if a no-skill/bad answer scores high, the judge is contaminated (too lenient) |
| **positive control** (known +) | light up | gold ref must score **high** — if a known-good expert answer doesn't, the judge can't detect quality → run **invalid** |
| **blank / contamination check** | catch carryover | generic-careful control arm — isolates lift from *mere framing* (delta-of-deltas) |
| **ladder / size marker** | calibrate scale | **Δ ≥ 2·SE(Δ)** (SE from rep variance, floored 0.8 — not a flat 1.4) + the gold↔bad spread — defines how big a difference counts as real |
| **test lanes (×N)** | the unknowns | with-skill answers × median ≥10 reps on hard scenarios |

→ **discipline: an eval run whose control panel doesn't pass is discarded, not reported** —
exactly like a QC-fail run (cf. `clinchem-judgment`).

Discipline unchanged: hard cases per fork **and** anti-pattern, median ≥10 reps for promote
decisions, log/halt if answerer drop-rate > 5%.

## Layer 2b — Safety-eval (W3 scaffold)

**Question: if a junior followed this answer literally, would a patient be harmed?**
Helpfulness Δ can be strong while an answer still over-scopes, skips verification, or fails to
escalate — so clinical skills need a **second axis** mapped to four harm types:
`unsafe-confident-answer` · `scope-of-practice` · `missing-context` · `required-escalation`.

Rubric (0–5 per type, worst-axis min for pass), pilot plan for five clinical skills, and
illustrative safe vs unsafe pairs: [`SAFETY-EVAL.md`](SAFETY-EVAL.md). **Not yet in CI** — design
only until harness pilot runs.

**Human L7 gate (clinical `stable`):** MT peer-review records live in [`peer-review/`](peer-review/)
(template + `flow-cytometry-judgment-DRAFT.md` pilot). AI pre-screen ≠ SIGN — see
[`peer-review-clinical-2026-06-10.md`](peer-review-clinical-2026-06-10.md).

## Layer 3 — Measurable exemplar (Titanic, real code)

**Question: can we put a number on the judgment, not just a vote?** For `ml-judgment` we run
the same dataset/model/selector and flip only *where feature selection happens* (before vs
inside cross-validation). The leak fabricates **+0.031 ROC-AUC** of fake performance —
reproducible, in 60 lines. [`titanic/`](titanic/).

---

## Threats to validity (read before believing any single number)

- **One run, stochastic answerer.** Haiku varies; each scenario is a single draw. In an
  earlier n=3 probe `polite-but-clear` *backfired*; in the full run it *lifted +3*. Trust the
  **aggregate direction**, not any per-skill decimal.
- **The judge is an LLM.** Blind, but still a model scoring models. A human-rater pass would
  strengthen this.
- **"Weak" = Haiku specifically.** A different weak model or a human novice may respond
  differently. The claim is "skills can lift *a* weak reasoner," not "all of them."
- **Clinical `tie`s may hide value.** One scenario can't probe a skill's whole surface; a skill
  that ties on its headline trap may still help on edge cases not sampled here.
- **Not a clinical outcome study.** This measures *answer quality on constructed scenarios*,
  not patient outcomes. Nothing here licenses skipping the human-in-the-loop the skills
  themselves demand.

The goal was never to prove these are perfect — it was to find where they help, where they
don't, and where they could hurt, *honestly enough that the failures show up*. They did.


## Reps per arm (2026-06-18)
**3 = screen · 5 = act · borderline/negative → fresh trap (or tie).** Scores 0–5, SD~1.0/arm →
`SE(Δ)≈√(2/n)` (n=3→0.82, n=5→0.63). Single-pass and even ×3 produced false negatives this session
(blood-donor, histotech) that more reps + a fresh trap corrected. Never cut/rewrite/promote below
reps=5. Harness: `eval/harness/ab-x3.js` takes `{targets,reps}`. Details: `AB-GATE.md`.
