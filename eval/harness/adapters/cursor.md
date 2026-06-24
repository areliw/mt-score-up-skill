# Adapter: Cursor

Two modes — only **Mode A** counts for `semi-stable` promotion.

## Mode A — Python CLI (recommended, tier `full`)

Run in the Cursor integrated terminal from repo root:

```bash
pip install -r requirements-dev.txt
export ANTHROPIC_API_KEY=sk-…

# Dry-run — validates pipeline, no API key
python scripts/ab_harness.py --skill choose-stat-test --reps 1 --dry-run

# Live screen
python scripts/ab_harness.py --skill choose-stat-test --reps 3 --append-slim
```

Uses Haiku (weak answerer) + Opus (blind judge) via Anthropic API — same tier as
Claude Code Workflow. Checkpoints land in `eval/runs/<run_id>/results.json`.

**Tip:** Ask the Cursor agent to run the command above instead of improvising a manual
A/B in chat — avoids accidental tier `manual` evidence.

## Mode B — Agent loop in chat (tier `manual` only)

Follow the four phases in [`../PROTOCOL.md`](../PROTOCOL.md):

1. **Generate** — read skill, write one trap scenario (≤120 words Thai MT).
2. **Answer** — weak persona, without skill then with skill inline, ×3 reps.
3. **Judge** — blind, swap A/B order per rep, score 0–5.
4. **Score** — aggregate with [`../python/protocol.py`](../python/protocol.py) rules.

Record prose in `eval/manual-ab-<date>.md`. If you append `_ab_slim`, use:

```json
{
  "tier": "manual",
  "method": "manual-screen",
  "run": "manual-YYYY-MM-DD",
  "note": "same-session Cursor agent — NOT valid for semi-stable promotion"
}
```

**Do not** overwrite existing `tier: full` rows with manual runs.

## Comparison

| | Mode A (CLI) | Mode B (chat) |
|---|---|---|
| Tier | `full` | `manual` |
| Blind judge | separate Opus call | ⚠️ same session |
| Promote? | ✅ | ❌ |
| Cost | ~12 calls/skill @ reps=3 | chat tokens |

## References

- Harness overview: [`../README.md`](../README.md)  
- Anti-bias: [`../../ANTI-BIAS-PROTOCOL.md`](../../ANTI-BIAS-PROTOCOL.md)  
- Superseded manual example: [`../../manual-ab-2026-06-24.md`](../../manual-ab-2026-06-24.md)
