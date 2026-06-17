# MT peer-review record — TEMPLATE

> Copy this to `eval/peer-review/<skill-slug>-<YYYY-MM-DD>.md` and fill it in.
> This captures the **L7 `peer-reviewed`** evidence in the maturity ladder
> (`docs/design/maturity-ladder.md`) — a licensed MT / domain expert signing off on the
> *content*. This is the human gate that AI review (codex) and the weak-model A/B **cannot**
> replace; clinical correctness rests here, not on the Haiku proxy.

---

- **skill:** `<skill-slug>`
- **content-hash reviewed:** `<sha256 of skills/<slug>.md at review time>`
  (record it so the level auto-drops if the skill is edited later — hash-currency rule)
- **reviewer:** `<name + credential, e.g. "ทนพ. X, สาขา Y, NN ปี">`
  *(anonymity OK — use a pseudonym or the "สมาชิกแห่งความมืด–องค์กรลับแห่งรัตติกาล" handle;
  do NOT publish hospital names / PII)*
- **date:** `<YYYY-MM-DD>`

## Checklist (mark each)
- [ ] **Correctness** — no factual error; claims match current standards (cite editions used)
- [ ] **Scope** — stays inside MT scope; no diagnose/prescribe overreach; gray-zones flagged
- [ ] **Traps** — the documented `## กับดัก` are the *real* landmines a junior hits; none missing/wrong
- [ ] **Real-world fit** — matches how the decision actually plays out on the bench / in the field
- [ ] **Currency** — standards/figures are the latest published edition
- [ ] **Safety** — nothing that could lead to patient harm if a junior follows it literally

## Findings
`<error / missing landmine / overstatement → fix applied, or flagged>`

## Verdict
- [ ] **SIGN** — content endorsed at this hash → eligible for L7 `peer-reviewed`
- [ ] **REVISE** — fix the findings, re-review
- [ ] **REJECT** — not ready

> Promotion to `stable`/L7 needs **≥1 SIGN from an MT in that domain** (clinical skills: prefer ≥2).
> Record the SIGN here; the maturity report / gate reads these records.
