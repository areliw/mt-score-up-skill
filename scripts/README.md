# scripts/ — what each script does (and which is canonical)

| script | role | status |
|---|---|---|
| `md_to_docx.py` | **Canonical scratch-build** — Markdown (+frontmatter) → DOCX with hospital banner + doc-control box, driven by per-hospital `profiles/<slug>.yaml` (content/layout split). No Word template needed. | ✅ canonical |
| `fill_with_docxtpl.py` | **Canonical template-fill** — fills a Word template *marked* with `{{ placeholders }}` (see `mark_template.py`): docxtpl render → body replace at anchor → native multilevel numbering + warning box + page footer. | ✅ canonical |
| `mark_template.py` | One-time helper: add `{{ placeholders }}` to a hospital's `.docx` so `fill_with_docxtpl.py` can fill it. | helper |
| `fill_template.py` | Basic template-fill (doc-control box via `paragraph.text`, no docxtpl/numbering). | ⚠️ deprecated → use `fill_with_docxtpl.py` |
| `recheck_standards.py` | CI: monthly check of current ISO editions on iso.org → refresh `STANDARDS.md` date stamps; flag a newer edition for human review (no silent edit). | ✅ (CI) |
| `replace_personnel.py` | Swap personnel names across a rendered WI `.docx` (body + header/footer + tables). Writes a `.bak` backup; supports `--dry-run`. | ✅ |
| `build_triage.py` | **Canonical catalog regen** — from skill frontmatter, rebuilds `prompts/triage.md` CATALOG, `skills/INDEX.md`, `dist/all-skills.md`. Run after **any** change under `skills/`. | ✅ canonical |
| `validate_repo.py` | CI: frontmatter keys, canonical sections, internal markdown links across all skills. | ✅ (CI) |
| `check_duplicates.py` | Advisory char-3gram Jaccard overlap report — flags merge/graft candidates (threshold 0.22). | advisory |
| `ab_gate_check.py` | PR gate: changed skills must have an entry in `eval/_ab_slim.json`. See [`eval/AB-GATE.md`](../eval/AB-GATE.md). | CI gate (advisory) |
| `check_maturity_gate.py` | PR gate: `status` must not out-rank evidence + body hash must match `eval/ab-coverage.json`. | CI gate (advisory) |
| `build_ab_coverage.py` | Maintainer: rebuild `eval/ab-coverage.json` maturity registry (body hashes + evidence flags). | maintainer |
| `maturity_report.py` | Advisory: claimed `status:` vs actual A/B evidence — surfaces over-claims without mutating files. | advisory |
| `create_contribution_form.gs` | Google Apps Script for the public contribution intake form. | helper (GAS) |

## Skill library pipeline

```bash
# After editing any skill:
python scripts/build_triage.py

# Before opening a PR:
python scripts/validate_repo.py
python scripts/check_duplicates.py          # advisory
python scripts/maturity_report.py           # advisory — check status vs evidence
python scripts/check_maturity_gate.py       # if you changed status or judgment body
python scripts/ab_gate_check.py           # if you changed skills (needs git diff context)
```

See also: [`eval/AB-GATE.md`](../eval/AB-GATE.md) · [`eval/METHOD.md`](../eval/METHOD.md) · [`docs/design/maturity-ladder.md`](../docs/design/maturity-ladder.md)

## Two document pipelines

- **No template → build from scratch:** `md_to_docx.py <in.md> <out.docx>`  (layout from `profiles/<slug>.yaml`)
- **Have a Word template → fill it:** `mark_template.py` (once) → `fill_with_docxtpl.py <marked.docx> <content.md> <out.docx>`

Rule of thumb (proven on real hospital templates): **if the user has a formatted template, fill it — don't rebuild from code.**

---

## `recheck_standards.py` — Layer 3 auto-refresh

ตรวจ current published edition ของ ISO 15189 / ISO 15190 จาก iso.org → refresh [`STANDARDS.md`](../STANDARDS.md) ที่ root

### Run locally

```bash
python scripts/recheck_standards.py            # clean run → refresh date stamps; a newer edition is flagged for review, NOT auto-applied
python scripts/recheck_standards.py --dry-run  # check only, don't write file
```

### Exit codes

| Code | ความหมาย | Action ของ GitHub Action |
|---|---|---|
| `0` | ทุก source confirm current — refresh date stamps ใน STANDARDS.md | commit date refresh (เฉพาะถ้าเปลี่ยน) |
| `1` | Error (fetch fail / pattern not matched) — **ไม่ refresh date** (กันเขียน "verified" ทั้งที่เช็คไม่สำเร็จ) | open issue + ping maintainer |
| `2` | พบ newer edition — **STANDARDS.md ไม่ถูกแก้** | **open issue/PR ให้คนรีวิว (ไม่ auto-push)** |

> ⚠️ ตั้งใจ: edition ใหม่ = หยุด + ให้คนตัดสิน (เลข clause/เนื้อหาอาจเปลี่ยน) ไม่เขียนทับเงียบๆ แล้วประทับ "verified"

### เมื่อ iso.org เปลี่ยน HTML

ถ้า exit code = 1 ติดต่อกัน — น่าจะ pattern เก่าไม่ match แล้ว แก้ที่ `SOURCES` list ใน script — เปิดหน้านั้นใน browser แล้ว update regex

### Schedule

Auto-run โดย `.github/workflows/standards-recheck.yml` ทุก **วันที่ 1 ของเดือน 09:00 ไทย**

Manual trigger ได้ที่ GitHub repo → Actions tab → "Monthly standards recheck" → "Run workflow"
