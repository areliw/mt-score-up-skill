# Skill-improvement playbook — how to lift a skill, and how to know if you actually did

Distilled from 3 A/B rounds + an improve loop + a controlled before/after experiment.
Two halves: **how to improve a skill**, and the harder half — **how to tell whether the
improvement was real or just noise.**

## Part 1 — The recipe (lift a weak/low skill toward tie-or-better)

Diagnose first — *why* is it low? Then apply the matching fix. (Evidence = where it worked in
our runs.)

| # | Fix | Apply when | Evidence it worked |
|---|---|---|---|
| 1 | **Lead with the verdict** — top = the #1 decision rule + #1 trap in one unmissable line a one-shot reader can act on | almost always | many tie→better (pathology, hematology, lab-mgmt) |
| 2 | **Procedural trigger** — `⛔ ถ้าเจอ [signal] → ทำ [action] ก่อนตอบ` at the very top | skill's value is an ACTION (use a tool, run a loop, check X first) | **know-yourself +3, offload +2** (no-rescue→lift) |
| 3 | **Negative constraint** — `ห้ามตอบแบบนี้: [the exact wrong pattern]`; generalize, don't overfit one phrase | the model drifts into a specific wrong move | polite-but-clear life-critical carve-out |
| 4 | **Tighten** — cut filler, every fork leads with its verdict, keep the answer sharp+short | scores fine on correctness but loses style points (the "style-cost" kind) | digital style→better, never-lose-a-file style→tie |
| 5 | **Correctness fold** — fix any dated/oversimplified claim against literature | any factual claim | bloodbank 15 Gy floor, clinchem multirule |

**The honest ceiling — don't fight it:**
- A **tie** is often because the scenario is *easy* (a weak model already gets it). You can't
  edit the skill to beat a baseline that's already at 5 — the lever is a **harder scenario**
  that reveals the skill's value, or accepting the value is in edge-cases/consistency.
- The noise floor is ~**1.4** points. Edits smaller than that are invisible to this A/B.

## Part 2 — How to know if an edit actually helped (the hard part)

**Use a controlled before/after, not a single re-run.** Same fixed scenario, change *only* the
skill (original vs edited), run N times each side, and — critically — **keep the without-skill
answer as a control.** The without-skill score must not depend on your edit, so if it moves,
that movement is your **noise estimate**.

Read it as a **delta-of-deltas**, never the raw with-score:
```
edge_before = with_before − without_before
edge_after  = with_after  − without_after
real effect = edge_after − edge_before      ← this is what your edit changed
```
If `with` rises but `without` rises by the same amount, your edit did **nothing measurable** —
you moved a whole noisy batch, not the skill.

## Worked example — `data-project-survival` (and why this matters)

We took a tie skill (a data-leakage sign-off scenario), added a sharp 4-point leakage checklist
+ an "expect the honest baseline number" rule, and ran the controlled experiment (N=3/side,
weak Haiku answerer):

| | with-skill | without (control) | edge |
|---|---|---|---|
| BEFORE (original) | 2.33 | 1.33 | **+1.00** |
| AFTER (+checklist) | 3.00 | 2.00 | **+1.00** |
| change | +0.67 | **+0.67** | **0.00** |

The with-score rose +0.67 — but the control rose **+0.67 too**, so the edit's real effect was
**zero**: the skill's edge stayed +1.00. Worse, the within-batch noise was brutal — the
with-score swung **1 → 4 on the identical scenario**, and this demo's "before" (2.33) didn't
even reproduce round 3's number for the same skill+scenario (4.0).

**The lesson (the most valuable finding of this whole eval arc):**
> At N=3 with a stochastic weak answerer, the measurement noise (±2–3) dwarfs any single edit's
> effect (<1). So **do NOT tune skills edit-by-edit with this A/B — you'd be chasing noise.**
> Instead:
> 1. **Judge each edit by expert review** — is it clearer, more complete, correct, scannable?
>    (The leakage checklist *is* a real improvement by that standard; we kept it on those
>    grounds, not on the A/B.)
> 2. **Use the A/B only at the library-aggregate level** — "do these skills help a weak model?"
>    (Yes: a stable ~+1 edge, 8 bulletproof, 0 dangerous regressions.) Not per-edit.
> 3. If you must measure a single edit, you need **N≈20+** or a stronger/more deterministic
>    answerer — otherwise accept review as the verdict.

The controlled design was the hero: it didn't make the number go up, it let us **see** that the
"+0.67 win" was noise — which is exactly what a single uncontrolled re-run would have hidden.
