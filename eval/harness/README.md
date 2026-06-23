# Portable A/B Harness

> **Which path should I use?** Pick an adapter — they all implement
> [`PROTOCOL.md`](PROTOCOL.md). Scoring is centralized in
> [`python/protocol.py`](python/protocol.py) (tested; must stay in sync with `ab-x3.js`).

## Adapter comparison

| Adapter | Entry point | Tier | API key | Best for |
|---|---|---|---|---|
| **Python CLI** (recommended) | `python scripts/ab_harness.py …` | `full` | `ANTHROPIC_API_KEY` (local) | Cursor terminal, Codex shell, maintainer laptop |
| **Claude Code Workflow** | `Workflow({ scriptPath: 'eval/harness/ab-x3.js', … })` | `full` | Claude Code billing | Existing round6 workflow, batch in CC |
| **Cursor agent manual** | Follow PROTOCOL phases in chat | `manual` only | chat model | Exploratory triage — **not** promotion evidence |
| **Codex + Python CLI** | Same as Python CLI | `full` | Anthropic (phase 2a) | OpenAI Codex environments with shell |

## Quick start (Python — no Claude Code required)

```bash
pip install -r requirements-dev.txt
export ANTHROPIC_API_KEY=sk-…   # omit for --dry-run

# Single skill, dry-run (no API)
python scripts/ab_harness.py --skill choose-stat-test --reps 1 --dry-run

# Live screen (≈12 API calls/skill at reps=3)
python scripts/ab_harness.py --skill choose-stat-test --reps 3

# Batch from config + append scoreboard
python scripts/ab_harness.py --config eval/harness/backfill-screen-only.json --reps 3 --append-slim
```

Output:

- **Checkpoint:** `eval/runs/<run_id>/results.json`
- **Stdout:** summary table (Δ, kind, σ)
- **`--append-slim`:** appends full-tier rows to `eval/_ab_slim.json`

## Layout

```
eval/harness/
  PROTOCOL.md           # portable spec (prompts + scoring)
  prompts/*.txt         # shared prompt templates
  ab-x3.js              # Claude Code adapter (legacy, kept)
  python/
    protocol.py         # parse config, classify kind, SE/threshold
    anthropic_driver.py # Opus/Haiku API calls
    runner.py             # gen → answer → judge orchestration
    append_slim.py        # write _ab_slim rows
  adapters/
    claude-code.md
    cursor.md
    codex.md
scripts/ab_harness.py   # thin CLI
```

## Drift guard

- Any change to scoring in `ab-x3.js` **must** be ported to `protocol.py` and covered by
  `tests/test_ab_protocol.py`.
- Prompt strings live in `prompts/*.txt` — both JS (future) and Python read the same files
  where possible; today JS still inlines strings (pointer only in `ab-x3.js` header).

## CI note

There is **no** GitHub Actions workflow for live A/B (no `ANTHROPIC_API_KEY` in CI).
The deterministic gate (`ab-gate.yml`) only checks that `_ab_slim.json` has a row.

## See also

- [`../BACKFILL-RUNBOOK.md`](../BACKFILL-RUNBOOK.md) — when a skill lacks full-tier evidence  
- [`../ANTI-BIAS-PROTOCOL.md`](../ANTI-BIAS-PROTOCOL.md) — tier rules  
- [`../AB-GATE.md`](../AB-GATE.md) — PR gate + decision rules
