# AGENTS.md — MT Score UP! Skills Hub

> **Single source of truth for AI coding agents.** `CLAUDE.md` (Claude Code) and
> `GEMINI.md` (Gemini CLI) just `@`-import this file — **edit agent rules HERE only**,
> so the three never drift. Most agents (Codex, Cursor, Copilot, Gemini, Aider,
> Windsurf, Zed, Jules, Factory, VS Code) read `AGENTS.md` natively.

## What this repo is
Free, portable **judgment skills** for Thai Medical Technologists (MT) — one markdown
file per skill, pasted into any AI chat (Claude / ChatGPT / Gemini), no install.
The value is **"which to choose when + the traps a senior would warn you about"**,
**not** textbook knowledge the model already has. Public docs are **Thai-first**.

## Layout
- `skills/` — the skills (one `*.md` each) · `README.md` (human catalog) · `INDEX.md` (generated)
- `prompts/` — `triage.md` router (has a generated CATALOG block) · `skill-interview.md`
- `eval/` — empirical evaluation; start at `METHOD.md`
- `docs/` — `USING.md` · `design/roadmap.md` · `skill-registry-spec.md`
- `contributions/` — `INTAKE.md` (maintainer playbook: submission → skill)
- `scripts/` — `build_triage.py` · `validate_repo.py` · `check_duplicates.py`
- `dist/all-skills.md` — generated bundle of every skill

## Commands (run from repo root; Python 3, no external deps)
- **After ANY change under `skills/`:** `python scripts/build_triage.py` — regenerates
  `prompts/triage.md`, `skills/INDEX.md`, `dist/all-skills.md`. **Commit the regenerated
  files** or CI fails.
- `python scripts/validate_repo.py` — checks skill frontmatter + internal links.
- `python scripts/check_duplicates.py` — char-3gram overlap detector (advisory).

## Authoring a skill — judgment, not knowledge
- Keep **"เลือกอะไรเมื่อไหร่ + กับดักที่มือใหม่ไม่รู้"**; cut definitions/formulas the AI already knows.
- Structure: frontmatter (`skill`/`title`/`type`/`needs`/`author`/`disclaimer`) →
  `## ใช้เมื่อ` → `## วิธีใช้` → **forks** (decision trees) → **กับดัก** (anti-patterns)
  → `## ช่องสำหรับผู้เชี่ยวชาญเติม` → disclaimer.
- `type`: `ADVISE` · `DO` · `CALIBRATION` — `needs`: `any` · `code-interpreter` · `persistent-memory`.
- **PII-clean** (no patient/person/hospital names, HN, course codes); no verbatim copyrighted text.

## Discipline — do not skip
- New/edited skill → **adversarial AI review** (take/drop, never apply raw) →
  **empirical A/B test on HARD cases covering every fork + anti-pattern** → *only then*
  "done" / eligible to promote. A static review is **not** a test. See [`eval/METHOD.md`](eval/METHOD.md).
- **Clinical (🩸) skills = flag-only** when reviewing — wrong clinical content injects error.
  Hedge every number/threshold as a teaching illustration tied to SOP/standard/edition (verify).
- **Maturity ladder:** `draft` → `semi-stable` (AI review + stress-test) → `stable`
  (formal/clinical peer-review — none yet). Status change ⇒ update `CHANGELOG.md` too.
- **`main` is branch-protected (PR-only)** — open a PR, don't push to `main`.
- **Conventional commits, no emoji in the body**; end AI-assisted commits with `Co-Authored-By`.

## Where to go next
- Contributing (humans): [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Submission → skill (maintainer): [`contributions/INTAKE.md`](contributions/INTAKE.md)
- Strategy / focus / roadmap: [`docs/design/roadmap.md`](docs/design/roadmap.md)
- Evaluation method: [`eval/METHOD.md`](eval/METHOD.md)
- Standards & editions: [`STANDARDS.md`](STANDARDS.md)
- Conduct: [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) · Security / PII: [`SECURITY.md`](SECURITY.md)
