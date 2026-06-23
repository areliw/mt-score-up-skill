# Adapter: Claude Code Workflow

> **Tier:** `full` · **Method:** `x3` / `x5` · **Scoring:** [`../python/protocol.py`](../python/protocol.py)

## When to use

You are in **Claude Code** with Workflow primitives (`agent`, `pipeline`, `parallel`).
This is the original round6 path — unchanged for backward compatibility.

## Invocation

```javascript
Workflow({
  scriptPath: 'eval/harness/ab-x3.js',
  args: [
    {
      skill: 'foo-judgment',
      file: 'skills/foo-judgment.md',
      focus: "the skill's own #1 anti-pattern",
    },
  ],
})
```

Batch with configurable reps:

```javascript
Workflow({
  scriptPath: 'eval/harness/ab-x3.js',
  args: {
    targets: [/* … */],
    reps: 5,  // act-grade before promote/cut/rewrite
  },
})
```

Or pass targets from [`../backfill-screen-only.json`](../backfill-screen-only.json)
→ `workflow.args`.

## What the adapter does

| Phase | Model | Notes |
|---|---|---|
| Generate trap | Opus | Reads skill via Read tool |
| Answer without / with | Haiku × N | Parallel per rep |
| Blind judge | Opus | A/B order swapped by `(target_index + rep) % 2` |

Returns `{ n, reps, rows: [{ skill, delta, kind, se, … }] }`.

## After the run

Workflow scripts **cannot write files**. Manually:

1. Copy each row into `eval/_ab_slim.json` **or** re-run the same skill via Python CLI with
   `--append-slim` (preferred for append automation).
2. Set `"tier": "full"`, `"method": "x3"` or `"x5"`, `"run": "wf_<id>"`.
3. `python scripts/build_ab_coverage.py` → commit `ab-coverage.json`.

Checklist: [`../../ANTI-BIAS-PROTOCOL.md`](../../ANTI-BIAS-PROTOCOL.md) §6

## Protocol source of truth

Prompt wording and scoring rules: [`../PROTOCOL.md`](../PROTOCOL.md)  
Implementation: [`../ab-x3.js`](../ab-x3.js) (orchestration) + [`../python/protocol.py`](../python/protocol.py) (scoring tests)

If Python and JS disagree, **fix JS or Python to match PROTOCOL** and extend
`tests/test_ab_protocol.py`.

## Alternative

Same protocol without Workflow:

```bash
python scripts/ab_harness.py --skill foo-judgment --reps 3 --append-slim
```

See [`../README.md`](../README.md).
