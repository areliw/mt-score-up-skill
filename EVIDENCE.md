# Evidence — how the guides are tested

> ⚠️ **For learning and study only — not for clinical use.** These guides help an AI assistant
> *think through* lab and work decisions. They are not diagnosis or treatment instructions and
> carry no guarantee of accuracy. Real patient work follows your lab's SOP and a licensed
> medical technologist or physician.

This repo holds **96 Thai-language guides** ("skills") that teach AI assistants how to reason
through medical-lab and workplace questions. Every number below is recomputed from the repo's
own files by [`scripts/evidence_counts.py`](scripts/evidence_counts.py) (counts as of 2026-10-21).

## The test

1. A trap question is written for the guide (in current runs, by Claude Opus).
2. A weak model (Claude Haiku) answers it twice: **with** the guide and **without** it.
3. Claude Opus scores both answers **blind**, without knowing which is which. Δ = score with − score without.
4. In repeated runs, a difference only counts if it is larger than that run's own noise (Δ ≥ 2·SE).

Method and rules: [`eval/AB-GATE.md`](eval/AB-GATE.md) · harness: [`eval/harness/ab-x3.js`](eval/harness/ab-x3.js)

## Results — latest A/B per guide

| Result | Guides |
|---|---:|
| Scored higher **with** the guide | 53 |
| No clear difference | 33 |
| Scored **lower** with the guide | 10 |
| **Total tested** | **96 / 96** |

44 results come from repeated runs (×3 or ×5), 51 from the early rounds, and 1 is a manual
run that does not count toward promotion. Raw rows: [`eval/_ab_slim.json`](eval/_ab_slim.json).

## Status — what "semi-stable" and "draft" mean

| Status | Meaning | Guides |
|---|---|---:|
| `semi-stable` | Passed: AI review + a full A/B whose result is not negative, **and** the text has not changed since that test (CI checks a hash of the guide body). | **21** |
| `draft` | Not passed yet, or edited after its last test so the old result no longer applies. Use with care. | 75 |
| `stable` | Signed review by a licensed MT or domain expert. | 0 |

- Of the 21 `semi-stable` guides, 15 scored higher with the guide and 6 tied. A tie passes because
  the guide did no harm; it does not prove the guide helps.
- All 10 guides that scored lower are kept at `draft`.
- All 21 lab-bench (🩸) guides are `draft`; none of them is promoted yet.

## Limits

- The judge is an AI model, not a human expert.
- Questions are constructed scenarios, not patient outcomes.
- One trap per guide cannot cover everything the guide says.

More: [`eval/METHOD.md`](eval/METHOD.md) ("Threats to validity").

## Re-check it yourself

```bash
python scripts/evidence_counts.py
python scripts/check_maturity_gate.py
```
