# Branch protection — required CI checks on `main`

`main` is PR-only. These GitHub Actions **job names** should be **required status checks**
so merges cannot bypass validation:

| Job name | Workflow | What it guards |
|----------|----------|----------------|
| `validate` | `validate-skills` | frontmatter + canonical sections + internal links |
| `check` | `check-triage-catalog` | `prompts/triage.md` catalog in sync with `skills/` |
| `maturity-gate` | `maturity-gate` | `status` ≤ evidence + hash-currency |
| `pytest` | `pytest` | script regression tests (W3) |

**Advisory (visible red, not required yet):** `ab-gate`, `smoke` (WI generator).

## Verify (any collaborator with `gh` auth)

```bash
python scripts/verify_branch_protection.py
```

Exit `0` when all four checks are required on `main`; exit `1` with instructions if not.

## Enable (maintainer, repo admin)

```bash
python scripts/verify_branch_protection.py --apply
```

Or manually:

```bash
gh api -X PUT repos/areliw/mt-score-up-skill/branches/main/protection \
  --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "checks": [
      {"context": "validate"},
      {"context": "check"},
      {"context": "maturity-gate"},
      {"context": "pytest"}
    ]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0
  },
  "restrictions": null
}
EOF
```

Verify: `gh api repos/areliw/mt-score-up-skill/branches/main/protection --jq '.required_status_checks'`

**Note:** Non-admin tokens often get HTTP 403/400 on the PUT — that is expected. A maintainer
must apply the rule in GitHub **Settings → Branches → Branch protection rules** using the
table above, then re-run `verify_branch_protection.py`.
