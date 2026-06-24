# AB-GATE (P4) — make the benchmark continuous, not a one-time sweep

> Decided 2026-06-18 (`STRATEGY-2026-06.md`, P4). A reliable ×3 scoreboard of all 94 skills
> ≈ ~34M tokens — not worth a one-time sweep. Instead the moat is enforced **on the margin**:
> every skill that lands must have an A/B record, and quality is checked at add/edit + promotion.

## Two halves (by design)

| half | what | where | cost |
|---|---|---|---|
| **deterministic gate** | every changed skill must have a Δ entry in `eval/_ab_slim.json` | GitHub Actions `ab-gate.yml` → `scripts/ab_gate_check.py` | free, no API key |
| **the actual A/B** | ×3 blind-judge (Opus gen → Haiku answer ×3 with/without → Opus blind judge) | **Primary:** `python scripts/ab_harness.py` · **Alt:** Claude Code → `eval/harness/ab-x3.js` · **Manual (tier manual only):** Cursor agent loop per `eval/harness/PROTOCOL.md` | model tokens (run by maintainer) |

The AI half stays in Claude Code (managed model access, no secret to manage); CI only enforces
that the evidence exists. Required checks on `main`: see [`docs/BRANCH-PROTECTION.md`](../docs/BRANCH-PROTECTION.md).

## The ritual (when you add or edit a skill's judgment)

1. Run the harness on the changed skill(s) — pick one path (`eval/harness/README.md`):
   ```bash
   # Primary (portable)
   python scripts/ab_harness.py --skill foo-judgment --reps 3
   ```
   ```javascript
   // Alternative (Claude Code Workflow)
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
   write files, so paste it in). Set **`"tier": "full"`** and `"method": "x3"` or `"x5"`.
   Manual same-session runs → **`"tier": "manual"`** only (see [`ANTI-BIAS-PROTOCOL.md`](ANTI-BIAS-PROTOCOL.md)).
   The gate reads only this structured file — a mention of a skill
   name in prose does **not** count as a record (that subtlety was a real bug, caught on 2026-06-18).

## Coverage status (gate audit, 2026-06-24)
**76 / 94** skills have a **full-tier** Δ in `_ab_slim.json` (round 1–3, round 6, session ×3/×5).
**18** have light screen only (`round4`/`round5`). Manual-tier rows (e.g. `manual-2026-06-24`) are
recorded for audit but **do not count** toward `semi-stable` — see [`ANTI-BIAS-PROTOCOL.md`](ANTI-BIAS-PROTOCOL.md).

### Evidence tiers in `_ab_slim.json`

| `tier` | source | counts for semi-stable? |
|---|---|---|
| `full` (default legacy) | `eval/harness/ab-x3.js` — Haiku answerer, Opus blind judge | ✅ |
| `manual` | same-session manual (`method` contains `manual`) | ❌ — PR gate warns |
| `screen` | rare structured screen row | ❌ — use round4/5 markdown instead |

`scripts/check_maturity_gate.py` requires **full-tier** `_ab_slim` (or round4/5 screen markdown) for
`semi-stable`. `scripts/ab_gate_check.py` still requires *some* row on changed skills but prints
**WARNING** when only `tier: manual` exists.

## Hardening to a fully-automatic gate (optional, later)
`scripts/ab_harness.py` already ports the protocol to the Anthropic API (local/maintainer only).
Running it **inside** CI would still require `ANTHROPIC_API_KEY` as a repo secret — intentionally
**not** wired (stochastic near the floor, API cost). The deterministic gate only checks that
`_ab_slim.json` has a row.


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
