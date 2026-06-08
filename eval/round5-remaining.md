# Round 5 — spot-A/B of the remaining 26 post-eval skills

> Companion to [`round4-new-skills.md`](round4-new-skills.md). Round 4 screened the 8
> v0.6.0 skills; this screens the **other 26** added after the eval-53 (the v0.4.0 +
> v0.5.0 waves, plus `lab-clinic-business-judgment` and `ab-test-judgment` from v0.3.0).
> **With this, every one of the 87 skills has now had at least a weak-model A/B screen.**

Same harness and same caveats as round 4: each skill's own #1 anti-pattern → a tempting
scenario; a **weak model (Claude Haiku)** answers **without** then **with** the skill;
trap-avoidance compared. It is a **lighter screen** than rounds 1–3 (self-derived traps,
single pass, assessed not blind-judged) — read it as a *safety check*, not a grade.

## Result — 26 skills · ~24 tie · ~2 marginally better · **0 regression**

| batch | skills | outcome |
|---|---|---|
| AI/prompt | prompt-optimizer · verification-panel · write-a-skill · token-budget · ai-coding-guardrails | 5 tie |
| research | literature-review · deep-research · source-credibility · pubmed-search · market-research | 4 tie · 1 better (lit-review: cold wavered "half-ok", skill firmly required PICO/criteria-first) |
| code/data | data-science-workflow · ml-engineering-workflow · tdd · debugging · grill-my-plan | 5 tie |
| comms/career | humanize-ai-writing · writing · report-up · interactive-course · pomodoro-focus | 5 tie |
| business/meta | dx-company-brief · lead-intelligence · incident-postmortem · time-blocking · lab-clinic-business · ab-test | 5 tie · 1 marginally better (time-blocking) |

**0 regression** — in every pair the with-skill answer was at least as trap-avoiding as
the cold answer. Loading a skill never made the weak model worse.

## The honest read (same as round 4, now at library scale)

Even **cold**, the weak model avoided almost every #1 trap — including non-obvious ones
it had no business knowing offhand:
- `write-a-skill`: cold correctly said "normal ranges = knowledge, not judgment"
- `lab-clinic-business`: cold correctly said "the moat isn't the equipment"
- `incident-postmortem`: cold correctly went for the system root cause, not "retrain the person"

So the outcome is ties. The skill's measurable contribution was **specificity and a forcing
function** — the exact scoring weights (lead-intelligence), the exact CAPA questions, the
noise-floor number (ab-test), PICO + 2-pass screening (lit-review). That is the documented
value: **consistency rails + non-expert scaffolding**, not boosting a model that already
carries the textbook.

## Library-wide status

| | skills | dangerous regression |
|---|---|---|
| rounds 1–3 (full harness, blind-judged) | 53 | 0 |
| round 4 (screen) | 8 | 0 |
| round 5 (screen) | 26 | 0 |
| **total** | **87** | **0** |

## The limitation that still stands

**Claude Haiku ≠ a real junior MT.** It carries broad textbook knowledge a first-week MT
or a nurse running POCT may not. These screens prove the skills are **safe to load**; they
do **not** prove the rescue value the skills are built for. The test that would: put the
[triage router](../prompts/triage.md) in front of real junior MTs and measure. Until then,
the honest claim is *"no skill is dangerous; value is real but audience-specific and not
yet proven at scale on humans."*
