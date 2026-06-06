# Round 2 — improve all skills, then re-run the A/B

We edited all 53 skills (lead-with-verdict + #1-trap-up-top + folded the 23 literature
nuances), then re-ran the same weak-model trap-A/B with **freshly derived scenarios**.

## Headline: the measurement is noisier than the improvement

| | Round 1 (original) | Round 2 (after edits) |
|---|---|---|
| lift | **25** | **25** |
| neutral | 19 | 15 |
| backfire | 9 | 4 |
| judged | 53 | 44 (9 judge-agents hit the StructuredOutput schema bug) |

`lift` is **identical (25)**. What moved is the *composition*: `rescued` 9→4, with many
`rescued→better` and `better→tie`. That is **not** "skills got worse" — it's that the
without-skill baseline rose this round (fresh, slightly easier scenarios + a stochastic weak
answerer), so the *gaps* shrank. The clearest proof: **`polite-but-clear` swung
rescued (+3) → regression (−2)** across runs with no change that would explain a real flip.

**Conclusion: a single A/B re-run can't prove an improvement.** The noise — fresh scenarios +
stochastic Haiku + an LLM judge — is larger than the edit's signal. To detect real movement
you'd need a **fixed scenario set** and **multiple runs averaged**, not one fresh-scenario run.
This was the variance caveat in `METHOD.md`, now demonstrated.

## What IS reliable (signal that survives the noise)

- **Style-cost recovery.** The skills told to "tighten + lead with verdict" recovered exactly
  as predicted: `digital-judgment` style→better, `never-lose-a-file` style→tie. The verbosity
  fix worked.
- **Literature nuances folded** (round 1, Layer 1b) are a **correctness** gain independent of
  the A/B — e.g. bloodbank now states "≥25 Gy central, ≥15 Gy floor" + MCA-PSV Doppler;
  clinchem notes the modern multirule drops 1₂ₛ + bilirubin interference starts ~2 mg/dL;
  hematology flags hereditary spherocytosis as a *true* high MCHC, not an artifact.
- **13 skills moved up** (mostly tie→better: pathology, hematology, lab-management, mt-law-ethics…).

## The 2 regressions (without-only) — handled honestly

- **`polite-but-clear`** (w2/wo4): the weak model softened a *transfusion refusal* until it
  handed the safety barrier back to the doctor as discretionary ("…แล้วแต่ท่านพิจารณา"). This
  is the repeated, scenario-stable failure of soft-skills + weak-model + life-critical message.
  **Fix applied:** a hard carve-out at the top — "เรื่องความปลอดภัย/ด่วน/เสี่ยงชีวิต: ห้ามลด
  ความแรงของคำสั่ง; 'ห้าม X' ห้ามแปลงเป็น 'แล้วแต่ท่านพิจารณา'."
- **`optimization-judgment`** (w1/wo5): a single −4 with a garbled low-score answer — most
  likely answerer/judge noise, not a real regression. Left as-is; flagged to re-check, not
  reverted on one noisy draw.

## Decision

Kept all improvements — they are principled (verdict-first), literature-current, and
format-verified (frontmatter/footer/headings clean across 53). The A/B noise argues for a
better *measurement* (fixed scenarios, repeated runs), not for reverting good edits. The one
genuine, repeatable safety pattern (`polite-but-clear` on life-critical messages) was hardened.

*9 skills (incl. `offload-to-automation`, `know-yourself`, and 5 clinical) went unjudged this
round due to the judge-schema bug, so their round-2 effect is unknown — a fixed-scenario re-run
without forcing schema on the judge would close that gap.*
