# Scripts — Layer 3 Auto-Refresh

## `recheck_standards.py`

ตรวจ current published edition ของ ISO 15189 / ISO 15190 จาก iso.org → update [`STANDARDS.md`](../STANDARDS.md) ที่ root

### Run locally

```bash
python scripts/recheck_standards.py            # commits changes if newer edition found
python scripts/recheck_standards.py --dry-run  # check only, don't write file
```

### Exit codes

| Code | ความหมาย | Action ของ GitHub Action |
|---|---|---|
| `0` | ทุก source confirm current — file refreshed last_verified date | commit (เฉพาะถ้า date เปลี่ยน) |
| `1` | Error (fetch fail / pattern not matched) | open issue + ping maintainer |
| `2` | พบ newer edition | auto-commit + push to main |

### เมื่อ iso.org เปลี่ยน HTML

ถ้า exit code = 1 ติดต่อกัน — น่าจะ pattern เก่าไม่ match แล้ว. แก้ที่ `SOURCES` list ใน script — เปิดหน้านั้นใน browser แล้ว update regex

### Schedule

Auto-run โดย `.github/workflows/standards-recheck.yml` ทุก **วันที่ 1 ของเดือน 09:00 ไทย**

Manual trigger ได้ที่ GitHub repo → Actions tab → "Monthly standards recheck" → "Run workflow"
