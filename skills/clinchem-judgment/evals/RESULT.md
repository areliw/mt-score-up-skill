# A/B — clinchem-judgment v1 (judgment-only) vs v2 (+ westgard.py / qc_calc.py)

**Date:** 2026-10-08 · **Model under test:** Claude Haiku 4.5 subagents, both arms allowed to run Python
**Task:** 4 fresh IQC series (2 levels, 4–10 runs), judge the LATEST run with the full multirule (1-2s warning only, all rejection rules on).
Traps: Q1 2-2s across levels within one run · Q2 +2.5 then −2.5 SD in DIFFERENT runs (must NOT be R-4s) · Q3 4-1s with no value beyond 2SD · Q4 10x.
**Oracle:** hand-derived from the 505402 digest §2.3 rule table · **Grader:** deterministic, 12 points (decision 2 + exact rejection-rule set 1, per question)
**Grader controls:** oracle sheet 12/12 · trap sheet 3/12

## Attempt 1 — v2 card as first written

| arm | r1 | r2 | r3 | r4 | mean | sd |
|---|---|---|---|---|---|---|
| v1 | 9 | 9 | 6 | 6 | 7.50 | 1.73 |
| v2 | 12 | 12 | 6 | 12 | 10.50 | 3.00 |

Δ = +3.00 but 2·SE = 3.46 → **gate FAILED, no promotion.**
- v1 errors: Q1 missed 2-2s across levels (3/4 runs) · Q3/Q4 "latest value within 2SD → ACCEPT" (1/4) · Q2 called R-4s across runs (1/4).
- v2 error (1/4 runs): the model chose `--mode classic` itself, saw the tool's `NOTE: classic 1-2s gate skipped ['4-1s']` and still answered ACCEPT for Q3 and Q4.
- Root cause is the card wording, not the tool → fix: card now says the default mode `all` is the standard answer, other modes only when the task/SOP names them, and a classic-gate NOTE must never become a silent ACCEPT.

## Attempt 2 — v2.1 card (mode rule added), same v1 sheets as baseline

| arm | r1 | r2 | r3 | r4 | mean | sd | time |
|---|---|---|---|---|---|---|---|
| v1 | 9 | 9 | 6 | 6 | 7.50 | 1.73 | 102–147 s |
| v2.1 | 12 | 12 | 12 | 12 | 12.00 | 0.00 | 66–79 s |

Δ = +4.50 > 2·SE = 1.73 (floor 0.8) → **A/B gate PASSED.**
Clinical content: per the promotion gate, a lab QC decision skill is promoted only after the owner confirms →
recorded as `pending-owner` in VERSION.json; the ladder counts it as v3 once the owner flips it to `pass`.
