# eval/ — does the scaffold actually reduce errors?

**Status: PRELIMINARY.** This is a *method + worked cases*, not a powered study. The claim
"skills reduce AI error" is **not yet proven at scale** — treat the cases below as
illustrative until a larger, blinded eval is run. (Listed as audit item #14 — "เคลมลอย"
until this exists for real.)

## Method (paired prompts)

For each case, run the **same question** through an AI twice:
1. **naive** — no skill in context
2. **guided** — the relevant skill pasted first

Score each answer against the rubric: did it (a) reach the correct judgment, (b) name the
trap/condition, (c) avoid stating a context-dependent rule as universal? `guided` should
win on (b) and (c).

## Worked cases (the trap each skill is meant to catch)

| # | Question | Naive answer often… | Skill | Correct judgment |
|---|---|---|---|---|
| 1 | "Company sold its notes receivable to a bank at a discount — clean reduction of receivables?" | "yes, receivables down" | `financial-statement-judgment` | depends on **recourse**: with-recourse = secured borrowing (stays on book); without-recourse = true sale (derecognition) |
| 2 | "Cholinergic crisis, can't tell OP vs carbamate — give 2-PAM?" | withholds it ("carbamate → atropine only") | `toxicology-judgment` | if OP can't be excluded, **give 2-PAM** — missing OP is worse |
| 3 | "Troponin high in a hemolyzed sample → report MI?" | reports it | `chemistry-interpretation-judgment` / `clinchem-judgment` | hemolysis interferes — don't report MI off a hemolyzed cTn; repeat |
| 4 | "RPR negative in obvious secondary syphilis — rule it out?" | rules out | `immunoassay-judgment` | **prozone** false-negative → dilute and retest |

## How to run (by hand)

Paste each question into your AI with / without the skill, compare against the rubric, log
which version named the trap. **Contributions of more cases are welcome — especially ones
where a skill *failed*.** That is how this becomes a real eval instead of a claim.
