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
that the evidence exists. Required checks on `main`: see [`docs/BRANCH-PROTECTION.md`](../docs/BRANCH-PROTECTION.md).

## The ritual (when you add or edit a skill's judgment)

1. Run the harness on the changed skill(s):
   ```
   Workflow({ scriptPath: 'eval/harness/ab-x3.js', args: [
     { skill: 'foo-judgment', file: 'skills/foo-judgment.md',
       focus: "the specific new landmine, or \"the skill's own #1 anti-pattern\"" }
   ]})
   ```
2. Read the Δ. **Decision rules:**
   - **Δ ≥ 2·SE(Δ)** (harness computes SE from rep variance, floored 0.8 — *not* a flat 1.4) **and** without unsafe (≤2) **and** with safe (≥3) → *rescues*. Ship.
   - **regression** = `mean(with)` UNSAFE (≤2.5) while `mean(without)` was safe (≥3) → **rewrite** the
     skill (per `IMPROVE-PLAYBOOK.md`) until it clears, then re-run.
   - **tie / style-cost** (both safe, Δ≈0) → not a failure; the trap may be intuitive to a weak
     model or the scenario didn't stress the skill's real value. Keep, or test a harder scenario.
3. **Always ×3.** Never act on a single pass — it is noise (a single pass gave `blood-donor`
   a false −3 that ×3 flipped to +1.33: `2026-06-18-p1-probe-results.md`).
4. **Append the Δ row to `eval/_ab_slim.json`** (the harness returns JSON; Workflow scripts can't
   write files, so paste it in). The gate reads only this structured file — a mention of a skill
   name in prose does **not** count as a record (that subtlety was a real bug, caught on 2026-06-18).

## Coverage status (gate audit, 2026-06-24)
**76 / 94** skills have a Δ entry in `_ab_slim.json` from full blind-judge (round 1–3, round 6,
and session ×3/×5 runs). **18** have light screen only (`round4`/`round5`). **0** lack any
record after round-6 backfill of the last 6 NONE gaps (see `eval/round6-probe.md` Batch 1–4).

## Hardening to a fully-automatic gate (optional, later)
To run the A/B *inside* CI and hard-block: add `ANTHROPIC_API_KEY` as a repo secret, port
`ab-x3.js` to a standalone API script, and enable branch-protection required-checks for `ab-gate`.
Trade-off: real API $ per PR + A/B is stochastic near the floor (flaky) — keep the floor lenient
or run ×5. The current design avoids both by keeping the run in Claude Code.


## How many reps per arm? (3 screen · 5 act · borderline → fresh trap)
Scores are 0–5 with high weak-model variance (SD ~1.0/arm), so Δ carries real noise:
`SE(Δ) ≈ √(2/n)` → n=3 → 0.82 · n=5 → 0.63 · n=10 → 0.45.
- **3 = screen (default):** sorts clear rescues from ties — cheap, wide (a flat Δ=1.4 here is only ~1.7·SE = marginal).
- **5 = act:** required before **cut / rewrite / promote**. bar = **Δ ≥ 2·SE(Δ)** (≈1.26 at n=5); harness reports `se`/`sigma`/`threshold` so you don't eyeball a magic number.
- **borderline / negative (|Δ| < ~1.5):** reps alone can't settle it — re-run with a **fresh trap**
  (scenario-luck is a *separate* variance source from rep noise) or call it a **tie**.

Proven the hard way (2026-06-18): single-pass → blood-donor false −3 (real +1.33); ×3 → histotech
false −1.17 (×5 + fresh trap → +1.1). **Never act below 5 reps; never trust one trap on a borderline.**
Maps to the ladder: L5 `proven` = 3-run, **L6 `replicated` = a 2nd axis** (fresh trap / judge / model) —
this session is the evidence you must reach L6 before acting, not stop at L5.

Run act-grade: `Workflow({scriptPath:'eval/harness/ab-x3.js', args:{targets:[...], reps:5}})`.
