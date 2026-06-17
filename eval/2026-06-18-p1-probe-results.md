# P1 probe — A/B blind-judge results (2026-06-18)

> Run `wf_48a45709-2ee` · 10 targets = 9 this-session landmines + 1 zero-coverage skill ·
> 40 agents · single Haiku pass per arm · Opus blind judge (order randomized by index parity).
> **This is a probe** (probe-before-fanout for P1) — single-pass = noisy; treat Δ as directional.

## Headline
- **n=10 · avgΔ +0.9 · 4 clear rescues** — the session's new landmines mostly transfer to a weak model.
- ⚠️ **1 real regression: `blood-donor-component-judgment` (Δ −3)** — the brand-new skill made
  Haiku *worse* on its own #1 trap. The benchmark caught a defect in freshly-shipped work.
- 🔧 raw `byKind` over-counted regressions (3) — **2 were both-safe style-costs**, see methodology fix.

## Results (sorted by Δ)

| skill / landmine | without | with | Δ | verdict |
|---|---|---|---|---|
| lab-management — EQA/PT fail investigation | 1 | 5 | **+4** | 🟢⤴ rescued — without re-ran-till-pass + blamed analyzer; with → root-cause first |
| mt-career — keep license active | 1 | 4 | **+3** | 🟢⤴ rescued — without said "let it lapse" + hallucinated re-entry; with kept it as hedge |
| mt-law-ethics — influencer product-review | 2 | 5 | **+3** | 🟢⤴ rescued — with cited device-ad/scope law correctly; without right-ish but legally muddled |
| interprofessional-comm (zero-coverage) | 2 | 5 | **+3** | 🟢⤴ rescued — with opened with patient-impact (rule #1); without led with technical reason |
| lab-clinic-business — where-to-open | 3 | 4 | **+1** | 🟢 better — with forced unit-economics + concrete moat before opening |
| lab-clinic-business — LAAB connect-cost | 5 | 5 | 0 | ⚪ tie — weak model already nailed it (MOU before paying); landmine may be intuitive |
| mt-career — อบจ promotion quota | 4 | 4 | 0 | ⚪ tie — both verify-before-quit; skill adds detail not safety here |
| lab-management — competency before go-live | 5 | 4 | −1 | 🟡 **style-cost** (both safe; with lost clarity to internal jargon) — *not* a true regression |
| ivd-sales — HEOR / LOS≠lost-revenue | 4 | 3 | −1 | 🟡 **style-cost** (both safe; with's wording garbled) — *not* a true regression |
| **blood-donor-component** — screen-reactive ≠ confirmed | 5 | 2 | **−3** | ⛔ **regression** — with-skill Haiku disclosed "HCV reactive" to donor pre-confirm |

## Key findings
1. **Harness works** → safe to fan out to the remaining ~84. ✅
2. **Session landmines validated (4 rescues):** EQA-fail, keep-license, influencer-risk,
   interprofessional-comm genuinely lift a weak model out of the trap.
3. **`blood-donor` is a real P2 rewrite candidate.** Loading the (new, draft) skill made Haiku
   *fall into* its own #1 trap (told donor a reactive screen before confirmation). Either the
   `## กับดัก` #1 isn't written so a weak reader can't miss "don't disclose an unconfirmed
   reactive," or it's single-pass noise — **confirm with ×3 before rewriting.**
4. **Ties (LAAB, อบจ):** weak model already safe → landmine is intuitive *or* the scenario
   didn't stress the nuance. Re-test with a harder scenario, or accept as low-marginal-value.
5. **Style-cost pattern:** with-skill answers repeatedly lost clarity points ("ภาษาเพี้ยน/
   ศัพท์ภายในเยอะ") — a weak model *parrots* dense expert prose. Readability signal for how
   skills should be written for the audience that actually loads them.

## Methodology fixes (for `IMPROVE-PLAYBOOK` / the harness)
- **Regression must require with-skill UNSAFE** (score ≤2) while without was safe (≥3) — not
  merely Δ<0. The auto-classifier tagged 3 regressions; only 1 (blood-donor) is real.
- **Use ≥3 Haiku passes per arm** (this probe used 1) — single-pass drove 2 false "regression"
  tags via style noise. Average the arms before computing Δ.
- **Judge should weight safety ≫ style** so a both-safe answer can't read as a regression.

## Next
1. Re-run `blood-donor` + the 2 ties + 2 style-costs with **×3 passes** to denoise.
2. If blood-donor confirms negative → rewrite its `## กับดัก` #1 (unmissable for a weak reader),
   re-test until Δ ≥ floor.
3. Fan out the full blind-judge to the remaining ~84 (P1), then act per P2.
