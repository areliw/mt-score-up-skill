# Strategy 2026-06 — turn the A/B benchmark into the repo's operating system

> Data-driven plan to make the library *defensibly* good, not just big.
> Builds on existing infra: `SCALE-PLAN.md`, `IMPROVE-PLAYBOOK.md`, `coverage-gap.md`,
> `ab-scorecard.md`, `peer-review-clinical-2026-06-10.md`. This file is the *why + priority order*.

## North-star recap
Democratize "รุ่นพี่ที่เก็บเคส/เตรียม landmine ให้รุ่นน้องไม่เคว้ง." The A/B benchmark
**is that north-star made measurable**: a *weak* model answers a trap derived from a skill's
own #1 anti-pattern, WITHOUT vs WITH the skill, blind-judged. `Δ = with − without` literally
asks *"does this skill keep a junior out of the trap?"*

## Data diagnosis (state @ 2026-06-18, main `8bc7bb9`)

| signal | number | reading |
|---|---|---|
| skills | **94** | — |
| status | **52 draft · 42 semi-stable · 0 stable** | top rung of the maturity ladder is empty |
| A/B coverage | **53 full blind-judge · 34 screen-only · ≥2 none** | "proven-to-help" moat covers ~**56%** |
| A/B result (n=53) | rescued 9 · better 16 · **tie 19 · style-cost 7** · no-rescue 2 · **regression 0** | ~half show no measurable lift on own worst-case; **0 made a weak model more dangerous** |
| freshest content | this session added blood-donor (#94) + many forks (LAAB · อบจ · HEOR · influencer · competency) | **newest landmines have 0 eval** |
| clinical core | hema/chem/micro/bloodbank = draft | highest-stakes skills are the least validated |

**Core problem:** the moat isn't "94 skills" (vanity count) — it's *"can prove, on demand,
that each skill helps."* That benchmark is **stale (53 of 94), incomplete, and one-shot.**

## Plan (ranked by leverage; each has a KPI)

### P1 — close the eval gap: a Δ score for all 94 (the scoreboard) ← START HERE
Upgrade 34 screen-only → full blind-judge, run the ≥2 zero-coverage, and **re-run every
skill this session edited** (new forks were never scored). Harness is reusable (Workflow).
Probe-before-fanout: 10-batch first, then fan out.
- **KPI:** 94/94 have a current Δ + kind.
- *In progress:* P1 probe launched 2026-06-18 (run `wf_48a45709-2ee`) — 10 targets =
  9 this-session landmines + 1 zero-coverage (interprofessional-communication).

### P2 — act on the scores (quality > count)
- **tie + commodity** (weak model already safe; AI knows it) → **cut or merge**. Shrinking
  where it doesn't help raises signal-to-noise — a junior shouldn't wade through noise.
- **no-rescue** (skill didn't transfer to a weak model) → **rewrite** per `IMPROVE-PLAYBOOK.md`
  until Δ clears floor (1.4).
- **regression** (0 today) → fix immediately if any new content introduces one.
- **KPI:** median Δ rises; 0 zero-lift skills left shipped.

### P3 — stand up the `stable` tier with real peer review
0 stable today; `peer-review-clinical-2026-06-10.md` already started the process. Take
high-lift + high-stakes (clinical core) skills → real MT peer review (crowdsource form +
contributors) → promote to `stable` with named-reviewer evidence.
- **KPI:** first N `stable` skills. This is the credibility moat (peer-validated, not just codex).

### P4 — wire the benchmark into CI (the durable moat)
Today eval is manual/periodic. Make it continuous: every skill add/edit auto-runs its A/B
screen, the scorecard regenerates, and **merge is blocked if Δ < floor or a regression
appears.** This turns the repo into a **self-validating** knowledge base, not a static doc dump.
- **KPI:** benchmark live + public + gating merges.
- *Note:* `dist/all-skills.md`/`INDEX.md` have OS-dependent byte output (Windows vs Linux
  runner) — gate the deterministic artifacts, not self-generated bundles (see
  `project_main_protected_bot_verify_only`).

### P5 (parallel) — close *real* coverage gaps, sourced from practitioners
Only ~2 genuine zero-coverage skills. Fill holes the data shows (`coverage-gap.md`), sourced
from real MT input (crowdsource form) over self-generation — real cases strengthen the moat.
- **KPI:** every high-frequency MT decision domain has a *proven* skill.

## Order of operations
P1 (scoreboard) → P2 (cut/improve) + P3 (promote) in parallel → P4 (make it continuous) →
P5 ongoing. **Everything downstream needs the scores first**, and the old scores are stale.
