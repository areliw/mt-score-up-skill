# eval/ — does the scaffold actually reduce errors?

**Status: evaluated, not proven.** There is now a real, blinded, multi-layer evaluation here
(not just the four illustrative cases this folder started with). It found genuine value **and**
genuine limits — both are reported. It is still *one run of a weak-model A/B + a literature
cross-check + a code exemplar + two audit rounds*, **not** a powered clinical-outcome study.
Read the threats to validity before trusting any single number.

## Start here

| file | what it answers |
|---|---|
| [`METHOD.md`](METHOD.md) | how we tested it (4 layers) + threats to validity |
| [`RESULTS.md`](RESULTS.md) | **the honest verdict** — what helped, what didn't, what could hurt |
| [`ab-scorecard.md`](ab-scorecard.md) | all 53 skills graded: rescued / better / tie / style-cost / no-rescue / regression |
| [`literature-check.md`](literature-check.md) | 66 clinical/method claims vs AABB/ACOG/guidelines |
| [`titanic/`](titanic/) | a *measurable* exemplar: `ml-judgment` removes +0.031 AUC of fake performance |

## The headline (n=53 skills, each on its own worst-case trap, weak answerer, blind judge)

```
rescued  9   skill flipped a weak model's wrong answer to right   ← strongest evidence
better  16   both right, skill added quality
tie     19   no measured difference (mostly clinical — weak model already knew the textbook trap)
style    7   both answers CORRECT, skill lost ≤1 style point        ← not a safety issue
no-resc  2   both failed; skill didn't transfer (procedural skills)
regress  0   skill made a right answer wrong                         ← the dangerous case: none
```

Literature: **43 supported / 23 nuanced / 0 contradicted** (nuances are precision upgrades).
Titanic: **+0.031 AUC** of leak-fabricated performance, removed by doing selection inside CV.

**Read:** the skills lift a *weak* model or a *non-expert* (9 rescues, 0 regressions, a
measurable code save); a frontier model already embodies the judgment, so for it they're
consistency rails, not capability boosts. Full nuance in [`RESULTS.md`](RESULTS.md).

## Why a weak (Haiku) answerer?

Because a frontier model answers the trap correctly with or without the skill — asking it "is
this skill helpful?" returns a flattering null. The skills exist to help a *weaker* reasoner or
a non-expert, so we test on that audience. See [`METHOD.md`](METHOD.md#layer-2--helpfulness-trap-ab-on-a-weak-model).

## The original four worked cases (still valid, now part of a bigger picture)

| # | Question | Naive answer often… | Skill | Correct judgment |
|---|---|---|---|---|
| 1 | "Sold notes receivable to a bank at a discount — clean reduction of receivables?" | "yes, receivables down" | `financial-statement-judgment` | depends on **recourse**: with-recourse = secured borrowing (stays on book); without = true sale |
| 2 | "Cholinergic crisis, can't tell OP vs carbamate — give 2-PAM?" | withholds it | `toxicology-judgment` | if OP can't be excluded, **give 2-PAM** — missing OP is worse |
| 3 | "Troponin high in a hemolyzed sample → report MI?" | reports it | `chemistry-interpretation-judgment` | hemolysis interferes — don't report MI off a hemolyzed cTn; repeat |
| 4 | "RPR negative in obvious secondary syphilis — rule it out?" | rules out | `immunoassay-judgment` | **prozone** false-negative → dilute and retest |

## Contributions welcome — especially failures

The eval is credible *because* it has 2 no-rescues, 7 style-costs, and 23 literature nuances in
it. If you find a skill that's wrong, dated, or that makes an answer worse — open an issue with
the scenario. That's how this stays honest instead of becoming marketing.
