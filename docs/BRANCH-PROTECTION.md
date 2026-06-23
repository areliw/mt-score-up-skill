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

## Enable (maintainer, repo admin)

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
