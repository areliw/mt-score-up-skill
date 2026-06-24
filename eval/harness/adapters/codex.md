# Adapter: Codex (OpenAI)

## Phase 2a — Python CLI + Anthropic API (MVP)

Codex can run shell commands. Use the **same portable harness** as Cursor Mode A:

```bash
pip install -r requirements-dev.txt
export ANTHROPIC_API_KEY=sk-…
python scripts/ab_harness.py --skill choose-stat-test --reps 3 --append-slim
```

This produces **`tier: full`** evidence with `method: x3` and Haiku/Opus pairing defined in
[`../PROTOCOL.md`](../PROTOCOL.md).

Dry-run (no key):

```bash
python scripts/ab_harness.py --skill choose-stat-test --reps 1 --dry-run
```

## Phase 2b — Native OpenAI driver (optional, not shipped)

A future `openai_driver.py` could map:

| Role | Anthropic (current) | OpenAI (hypothetical) |
|---|---|---|
| Strong (gen + judge) | Opus | `gpt-4o` |
| Weak (answerer) | Haiku | `gpt-4o-mini` |

**Important:** Δ values are **not directly comparable across vendors**. Treat Anthropic and
OpenAI runs as separate benchmarks — use relative trends **within** one vendor only.
If implemented, use `"method": "x3-openai"` (distinct from `"x3"`).

## When to prefer Codex path

- No Claude Code Workflow available
- Batch automation from a Codex agent with terminal access
- Maintaining parity with Cursor/local Python runs

## References

- Protocol: [`../PROTOCOL.md`](../PROTOCOL.md)  
- CLI: [`../../../scripts/ab_harness.py`](../../../scripts/ab_harness.py)  
- Gate tiers: [`../../ANTI-BIAS-PROTOCOL.md`](../../ANTI-BIAS-PROTOCOL.md)
