# RESULTS — what the evaluation actually found

> One run, weak-model A/B + literature cross-check + a measurable code exemplar + two audit
> rounds. Not a powered clinical study. Read [`METHOD.md`](METHOD.md) for the design and the
> threats to validity. The numbers below are reported as they came back — including the parts
> that don't flatter the skills.

> ⚠️ **Superseded headline number — read [`round3/`](round3/) for the corrected one.** The
> single-run figures below (lift 25 = 9 rescued + 16 better) were re-measured in round 3 with a
> *fixed scenario set + 2-run averaging*. Averaging pulled ~6 "lifts" back to noise, giving the
> honest figure: **lift ~19, rescued 8, 0 regression, 0 no-rescue** on harder scenarios. The
> analysis below still holds *directionally*; for the headline trust round 3 + the **~1.4 noise
> floor** (a per-skill delta must clear ~1.4 to be real signal).

## TL;DR

- On each skill's **own worst-case trap**, given to a **weak** model (Haiku), blind-judged:
  **9 rescued · 16 better · 19 tie · 7 style-cost · 2 no-rescue · 0 regression** (n=53).
  <sub>(n=53 = the library **at eval time** (v0.2 era). The library is now **88** — the +34 added
  by v0.6.0 (v0.4.0–v0.6.0) plus the newest skill `git-workflow-judgment` (#88, added after) passed design
  review but have **not** had a weak-model A/B yet (35 total). See `CHANGELOG.md`.)</sub>
- **0 skills made a weak model more dangerous.** No skill turned a correct answer into a
  trap-fall. The 9 raw "backfires" are 7 *both-answers-correct* style-point losses + 2
  *both-failed* no-rescues.
- The skill's value is **real but audience-specific**: it lifts a weak reasoner / non-expert.
  A frontier model embodies the judgment already, so with/without is a wash for it (that's
  expected, and it's *why* the skills exist for everyone else).
- Concrete, measurable case: `ml-judgment` removes **+0.031 AUC of fake performance** on
  Titanic ([`titanic/`](titanic/)).

## Layer 1 — Correctness: errors existed, and were fixed

Two adversarial audit rounds found and corrected verified clinical errors (Bombay/anti-H
prewarm routing — fatal if followed; inverted antibody rule-out; backwards Jaffe→GFR; "low
albumin + normal LFT excludes liver"). This is the most important honesty signal in the whole
eval: the skills *were wrong in places*, an attacker-model found it, and it's logged in
[`../docs/audit-2026-06-03.md`](../docs/audit-2026-06-03.md). A scaffold that only ever reports
wins isn't being tested.

## Layer 1b — Literature: key claims hold up, with precision upgrades

Clinical/methodology skills were cross-checked claim-by-claim against AABB/ACOG/CLSI/guideline
/peer-reviewed sources ([`literature-check.md`](literature-check.md)).
**66 claims across 22 clinical/methodology skills: 43 supported · 23 nuanced · 0 contradicted ·
0 unverified.** Nothing came back flat-wrong, and nothing was an unverifiable hand-wave — but
23 nuances (a third of all claims) means the check wasn't a rubber-stamp. Every nuance is a
*currency/precision* upgrade, not a reversal. The bloodbank probe is representative: all three high-stakes claims (25 Gy irradiation for
TA-GVHD; RhIG timing + ~1:16 critical anti-D titer; mandatory Coombs control cells on a
negative AHG) were **supported**, with two *nuanced* precision fixes the literature triggered —
state irradiation as "25 Gy central, ≥15 Gy minimum to any portion," and lead fetal-anemia
surveillance with MCA-PSV Doppler (ΔOD450/amnio is now legacy). Pattern across the set: claims
are directionally sound; the corrections are about *currency and precision*, not reversals.

## Layer 2 — Helpfulness: the A/B, read honestly

Full table: [`ab-scorecard.md`](ab-scorecard.md). What the breakdown means:

**The 9 rescues — the strongest evidence.** Here the weak model *fell into the trap without the
skill and avoided it with the skill*. The biggest deltas:

| skill | with | without | Δ | the trap it rescued |
|---|---|---|---|---|
| `ivd-sales-judgment` | 5 | 1 | +4 | selling on "more accurate" instead of turnaround/COGS/reproducibility |
| `content-creator-judgment` | 4.5 | 1 | +3.5 | picking a topic for completeness over a scroll-stopping hook |
| `anti-hallucination` | 5 | 2 | +3 | trusting a confident, hyper-specific number + citation (the most seamless fabrication) |
| `mt-exam-strategy-judgment` | 5 | 2 | +3 | — |
| `polite-but-clear` | 5 | 2 | +3 | softening past the point of losing the actual message |
| `mt-career-judgment` | 5 | 2 | +3 | — |
| `r2r-research-proposal` | 4.5 | 2 | +2.5 | — |
| `parasitology-judgment` | 5 | 3 | +2 | — |

The lifts cluster on **judgment that's non-obvious** — sales framing, hook-vs-value, calibrated
skepticism, exam tactics. That's exactly where a page of distilled "choose X when Y" beats a
weak model's defaults.

**The 19 ties — mostly clinical, and that's informative.** `hematology`, `clinmicro`,
`pathology`, `immunoassay`, `applied-microbiology`, `lab-management`, `choose-stat-test`,
`finance`, `cv`, and others tied. For the clinical ones, the reason is benign: their headline
traps are *well-documented in training data*, so even a weak model often gets the textbook
answer on a single scenario. The skill's real edge for these is **consistency (forcing the
check every time)** and **edge cases** — neither of which one scenario can prove. A tie here is
"no measured harm, value not captured," not "useless."

**The 7 style-costs — both answers were correct.** `bloodbank`, `clinchem`, `toxicology`,
`infection-control`, `digital-judgment`, `never-lose-a-file`, `ai-agent-team` showed Δ−1, but
the blind judge recorded **both** versions avoiding the trap (clerical-first, refuse-to-report,
GC-MS-confirm, soap-and-water-for-C.diff). The with-skill answer just lost a style/length
point. **This is not a safety regression** — both answers were safe.

**The 2 no-rescues — the genuinely instructive failures.** `offload-to-automation` (Δ−2) and
`know-yourself` (Δ−1): in both, the weak model failed the trap with *and* without the skill.
The shared lesson is sharp — **both are skills whose value is procedural, not propositional.**
`offload-to-automation` says "hand the calculation to a solver instead of asserting in your
head"; a weak model reading that advice still asserts in its head, because *executing* it needs
the runtime to actually invoke a tool, not just the text. `know-yourself` is an interview loop;
given a one-shot input it can't run the loop. **Reading the judgment ≠ being able to perform
it** when the judgment is "use a tool" or "run a multi-turn process." That's a real design note
for the hub, not a defect in the advice.

**0 regressions.** The case that would actually condemn a skill — *without-skill was right and
the skill pushed the weak model into the trap* — happened **zero times**. Note the earlier n=3
probe had `polite-but-clear` backfiring (weak model over-softened and dropped a K⁺ 6.8 urgency);
that did **not** replicate in the full run (it lifted +3). The disagreement is the variance
warning made concrete — and the reason the conservative read is "0 regressions observed, but
soft skills given to weak models still deserve a don't-bury-the-urgent guard."

## Layer 3 — Titanic: a number, not a vote

Same data, same model, flip only where feature selection happens: the leak fabricates
**+0.031 ROC-AUC** (0.850 inflated vs 0.819 honest) that would vanish on real holdout. The
seductive path scores *higher*, which is the whole reason the skill has to exist. Details and
reproduction: [`titanic/`](titanic/).

## So — are the skills good?

Honestly: **good for the right user, on the right job, with the limits stated.**

- **Yes** for a weaker model or a non-expert: 9 clean rescues + 16 quality gains, 0 regressions,
  and a measurable +0.031-AUC save. That's a real, non-rigged signal.
- **Marginal** for frontier models: they already embody the judgment (ties), so loading a skill
  mostly costs context for little gain — use them as *checklists/consistency rails*, not
  capability boosts.
- **Known dead-zones:** procedural skills (`offload-to-automation`, `know-yourself`) don't
  transfer as one-shot text — they need the tool/loop wired up to deliver.
- **Still unproven:** real-world clinical outcomes, human-rater agreement, and stability across
  more runs. Those are the next layers, and they're listed as open in
  [`METHOD.md`](METHOD.md#threats-to-validity).

The skills are decision-support for a human/automation pipeline that keeps the expert in the
loop — which is exactly what every clinical skill's own footer already says. Nothing here
changes that contract; it just measures, with the failures left in, how much the support
actually helps and where it doesn't.
