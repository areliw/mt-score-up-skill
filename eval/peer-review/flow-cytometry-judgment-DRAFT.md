# MT peer-review record — flow-cytometry-judgment (DRAFT)

> **DRAFT — awaiting MT SIGN.** AI pre-screen complete ([`../peer-review-clinical-2026-06-10.md`](../peer-review-clinical-2026-06-10.md));
> full-tier helpfulness A/B Δ+3.67 (round 6, [`../round6-probe.md`](../round6-probe.md)). This file
> is ready for a licensed MT in flow/hematology to review and sign. **Do not promote to `stable`
> until SIGN block is checked.**

---

- **skill:** `flow-cytometry-judgment`
- **content-hash reviewed:** `642e425b0df6` *(sha256 of body after frontmatter — verify before signing)*
- **reviewer:** *(empty — MT to fill: name + credential, no hospital/PII)*
- **date:** *(empty — YYYY-MM-DD at sign)*

## Scope reviewed

Reviewer confirms the file covers **MT decision-support for flow cytometry** (gating order,
viability/doublet exclusion, FMO vs isotype, compensation pitfalls, correlate
morphology/clinical/genetics) and **does not** substitute for pathologist/MD diagnosis.

| section | reviewed? | notes |
|---|---|---|
| Frontmatter + disclaimer | ☐ | scope: ADVISE, draft, verify-first |
| `## ใช้เมื่อ` / `## วิธีใช้` | ☐ | |
| Fork 1 — gating strategy (time → scatter → singlet → viable/dump → CD45/SSC) | ☐ | |
| Fork 2 — panel design | ☐ | |
| Fork 3 — pattern not single marker | ☐ | |
| Fork 4 — apps (leukemia, CD4, PNH, MRD, subsets) | ☐ | PNH lineage-specific + transfusion caveat |
| Fork 5 — correlate | ☐ | no diagnosis from flow alone |
| `## กับดัก` (#1–#8) | ☐ | especially #1 dead/doublet/debris, #2 over-comp, #3 FMO |
| `## ช่องสำหรับผู้เชี่ยวชาญเติม` | ☐ | |

## Claims checked

*(AI pre-screen 2026-06-10 — MT re-verify against current lab SOP/editions before SIGN.)*

| claim / area | pre-screen verdict | MT check | edition / source used |
|---|---|---|---|
| FMO = primary gating control; isotype legacy, not interchangeable | FIXED (was misleading pair) | ☐ | Maecker & Trotter 2006; ICCS |
| Gating order: time/stability → scatter → singlet → viable+dump → CD45/SSC | FIXED (added time/dump) | ☐ | EuroFlow/OMIP practice |
| Over-compensation → false **negative** (MRD risk) | FIXED | ☐ | |
| PNH: FLAER + ≥2 GPI markers per **WBC** lineage; RBC/transfusion caveats | FIXED | ☐ | ICCS PNH consensus 2018 |
| Blast CD45-dim; plasma cell may fall outside CD45/SSC gate | present | ☐ | |
| MRD requires adequate event count | present | ☐ | |
| No diagnosis from flow alone — correlate smear/genetics/MD | present | ☐ | |

**MT findings:** *(empty — errors, overstatements, missing landmines)*

## Forks verified

Walk each fork against **real bench workflow** (not textbook only):

| fork | real-world fit OK? | traps aligned? | MT notes |
|---|---|---|---|
| 1 — gating order | ☐ | ☐ | |
| 2 — panel design | ☐ | ☐ | |
| 3 — pattern reading | ☐ | ☐ | |
| 4 — clinical apps (PNH/MRD/CD4/…) | ☐ | ☐ | |
| 5 — correlate | ☐ | ☐ | |

## Checklist (from template)

- [ ] **Correctness** — no factual error; claims match current standards (cite editions used)
- [ ] **Scope** — stays inside MT scope; no diagnose/prescribe overreach; gray-zones flagged
- [ ] **Traps** — documented `## กับดัก` are real junior landmines; none missing/wrong
- [ ] **Real-world fit** — matches bench/field decision flow
- [ ] **Currency** — standards/figures are latest published edition used in your lab
- [ ] **Safety** — nothing that could harm a patient if a junior follows literally

## Verdict

- [ ] **SIGN** — content endorsed at hash `642e425b0df6` → eligible for L7 `peer-reviewed` / discuss `stable`
- [ ] **REVISE** — fix findings, re-review at new hash
- [ ] **REJECT** — not ready

**Reviewer signature / handle:** *(empty)*

**Second reviewer (clinical skills — prefer ≥2 SIGN):** *(empty)*
