# peer-review/ — human L7 gate for clinical `stable`

AI codex review + weak-model A/B **cannot** replace a licensed MT signing off on clinical
judgment content. Records here implement **L7 `peer-reviewed`** in
[`docs/design/maturity-ladder.md`](../../docs/design/maturity-ladder.md).

## Workflow

1. Copy [`TEMPLATE.md`](TEMPLATE.md) → `<skill-slug>-<YYYY-MM-DD>.md` (or use a `*-DRAFT.md`
   prepared by maintainers).
2. Reviewer records **content-hash** (body after frontmatter — same rule as
   `scripts/build_ab_coverage.py`) so edits after sign drop the evidence level.
3. Complete scope / claims / forks / checklist → **SIGN** or REVISE/REJECT.
4. Promotion to `stable` needs **≥1 SIGN from MT in domain** (clinical: prefer ≥2).

## Files

| file | status |
|---|---|
| [`TEMPLATE.md`](TEMPLATE.md) | blank template |
| [`flow-cytometry-judgment-DRAFT.md`](flow-cytometry-judgment-DRAFT.md) | **DRAFT** — round-6 Δ+3.67, AI pre-screen done; awaiting MT SIGN |

**AI pre-screen only (not SIGN):** [`../peer-review-clinical-2026-06-10.md`](../peer-review-clinical-2026-06-10.md)

## Path to first `stable` skill

Target pilot: **`flow-cytometry-judgment`** — strong measured lift, pre-screen fixes merged,
DRAFT peer-review record ready. After MT SIGN at current hash → maintainer may promote per
[`../../AGENTS.md`](../../AGENTS.md) + update `CHANGELOG.md`. No auto-promote from A/B alone.
