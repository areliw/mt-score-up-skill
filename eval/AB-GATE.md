# AB-GATE (P4) — make the benchmark continuous, not a one-time sweep

> Decided 2026-06-18 (`STRATEGY-2026-06.md`, P4). A reliable ×3 scoreboard of all 94 skills
> ≈ ~34M tokens — not worth a one-time sweep. Instead the moat is enforced **on the margin**:
> every skill that lands must have an A/B record, and quality is checked at add/edit + promotion.

## Two halves (by design)

| half | what | where | cost |
|---|---|---|---|
| **deterministic gate** | every changed skill must have a Δ entry in `eval/_ab_slim.json` | GitHub Actions `ab-gate.yml` → `scripts/ab_gate_check.py` | free, no API key |
| **the actual A/B** | ×3 blind-judge (Opus gen → Haiku answer ×3 with/without → Opus blind judge) | Claude Code Workflow → `eval/harness/ab-x3.js` | model tokens (run by maintainer) |

The AI half stays in Claude Code (managed model access, no secret to manage); CI only enforces
that the evidence exists. CI is **advisory** — the repo's branch protection has
`required_status_checks=null`, so a red check is a visible signal, not a hard block.

## The ritual (when you add or edit a skill's judgment)

1. Run the harness on the changed skill(s):
   ```
   Workflow({ scriptPath: 'eval/harness/ab-x3.js', args: [
     { skill: 'foo-judgment', file: 'skills/foo-judgment.md',
       focus: "the specific new landmine, or \"the skill's own #1 anti-pattern\"" }
   ]})
   ```
2. Read the Δ. **Decision rules:**
   - **Δ ≥ 1.4** (vs floor) and weak-model-without unsafe → the skill *rescues*. Ship.
   - **regression** = `mean(with)` UNSAFE (≤2.5) while `mean(without)` was safe (≥3) → **rewrite** the
     skill (per `IMPROVE-PLAYBOOK.md`) until it clears, then re-run.
   - **tie / style-cost** (both safe, Δ≈0) → not a failure; the trap may be intuitive to a weak
     model or the scenario didn't stress the skill's real value. Keep, or test a harder scenario.
3. **Always ×3.** Never act on a single pass — it is noise (a single pass gave `blood-donor`
   a false −3 that ×3 flipped to +1.33: `2026-06-18-p1-probe-results.md`).
4. **Append the Δ row to `eval/_ab_slim.json`** (the harness returns JSON; Workflow scripts can't
   write files, so paste it in). The gate reads only this structured file — a mention of a skill
   name in prose does **not** count as a record (that subtlety was a real bug, caught on 2026-06-18).

## Coverage status (gate audit, 2026-06-18)
**55 / 94** skills have a Δ entry in `_ab_slim.json` (53 legacy single-pass + 5 this-session ×3;
2 of those newly inserted). **39** lack one — the 34 screen-only skills (`coverage-gap.md`) +
recent additions. They are the backfill queue, and the gate flags any of them the moment it is
edited — by design: an edited skill should carry a current Δ. (Legacy 53 are single-pass →
re-confirm with ×3 when promoting to `stable`, P3.)

## Hardening to a fully-automatic gate (optional, later)
To run the A/B *inside* CI and hard-block: add `ANTHROPIC_API_KEY` as a repo secret, port
`ab-x3.js` to a standalone API script, and enable branch-protection required-checks for `ab-gate`.
Trade-off: real API $ per PR + A/B is stochastic near the floor (flaky) — keep the floor lenient
or run ×5. The current design avoids both by keeping the run in Claude Code.


## How many reps per arm? (3 screen · 5 act · borderline → fresh trap)
Scores are 0–5 with high weak-model variance (SD ~1.0/arm), so Δ carries real noise:
`SE(Δ) ≈ √(2/n)` → n=3 → 0.82 · n=5 → 0.63 · n=10 → 0.45.
- **3 = screen (default):** detects a clear rescue (Δ≥1.4 ≈ 1.7·SE) and sorts it from ties — cheap, wide.
- **5 = act:** required before any **cut / rewrite / promote** (Δ≥1.4 ≈ 2.2·SE).
- **borderline / negative (|Δ| < ~1.5):** reps alone can't settle it — re-run with a **fresh trap**
  (scenario-luck is a *separate* variance source from rep noise) or call it a **tie**.

Proven the hard way (2026-06-18): single-pass → blood-donor false −3 (real +1.33); ×3 → histotech
false −1.17 (×5 + fresh trap → +1.1). **Never act below 5 reps; never trust one trap on a borderline.**
Maps to the ladder: L5 `proven` = 3-run, **L6 `replicated` = a 2nd axis** (fresh trap / judge / model) —
this session is the evidence you must reach L6 before acting, not stop at L5.

Run act-grade: `Workflow({scriptPath:'eval/harness/ab-x3.js', args:{targets:[...], reps:5}})`.
