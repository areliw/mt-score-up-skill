# Standards Reference — Verified Editions

> **Source of truth สำหรับ AI** เมื่อสร้าง WI — AI ต้องอ้าง edition ตามไฟล์นี้, **ไม่ใช่ knowledge cutoff ของ AI**
>
> ถ้า AI มี web_search → verify จาก iso.org / aabb.org / clsi.org ก่อน + cross-check ไฟล์นี้
> ถ้าไม่มี → ใช้ไฟล์นี้ + flag user ถ้า `last_verified` > 90 วันจากวันปัจจุบัน

---

## Last full verification

**Date:** 2026-06-01
**Method:** WebSearch via Claude Code agent
**Next scheduled recheck:** 2026-07-01 (30-day cadence — see Layer 3 in [README](README.md))

---

## Verified editions

### Primary (ใช้ใน WI ทุกฉบับ)

| Standard | Current edition | Published | Notes | Last verified |
|---|---|---|---|---|
| **ISO 15189** | `:2022` (4th ed) | 2022-12 | Replaces :2012. Risk-based thinking + ISO 22870 (POCT) merged in. | 2026-06-01 |
| **ISO 15190** | `:2020` | 2020 | Replaces :2003. ⚠️ **ISO/AWI 15190 in draft** (Nov 2025) — monitor | 2026-06-01 |
| **AABB Technical Manual** | `21st edition` | 2023 | Blood Bank — used in PRC/component prep WIs | 2026-05-27 |

### Secondary (ใช้ตามแผนก/ความเกี่ยวข้อง)

| Standard | Current edition | Published | Used in | Last verified |
|---|---|---|---|---|
| ISO/IEC 17025 | `:2017` | 2017 | General lab competence | ⏳ pending |
| ISO 9001 | `:2015` | 2015 | QMS framework | ⏳ pending |
| ISO 22367 | `:2020` | 2020 | Risk management (cited in 15189:2022) | ⏳ pending |
| ISO 35001 | `:2019` | 2019 | Biorisk management (cited in 15189:2022) | ⏳ pending |
| CLSI guidelines | (varies per doc) | — | Method-specific | ⏳ pending |

### Withdrawn / Merged

| Standard | Status | Replacement |
|---|---|---|
| ISO 22870 (POCT) | Withdrawn | Merged into ISO 15189:2022 |
| ISO 15189:2012 | Superseded | ISO 15189:2022 |
| ISO 15190:2003 | Superseded | ISO 15190:2020 |
| AABB Tech Manual 20th | Superseded | 21st edition (2023) |

---

## How AI must use this file

1. **ทุก session ก่อน generate WI** — อ่านไฟล์นี้ + อ้าง edition ตามนี้
2. **ถ้า AI มี web_search** → ตรวจ iso.org / aabb.org ก่อน → ถ้า diff กับไฟล์นี้ → **trust web** + เตือน user ว่า STANDARDS.md ต้อง update
3. **ถ้า `Last full verification` > 90 วันจากวันนี้** → AI ต้องเตือน user ใน output:
   > ⚠️ Standards reference last verified [DATE] — ผ่านมา [N] วัน แนะนำให้ verify เอง ที่ iso.org / aabb.org ก่อนใช้จริง
4. **ห้าม AI cite edition ที่ไม่อยู่ในไฟล์นี้** ยกเว้น web_search confirm ใน real-time

## How human contributor updates this file

1. WebSearch standard ที่จะ update → confirm current edition จาก iso.org/aabb.org
2. แก้ row + อัพเดต `Last verified` column
3. แก้ `Last full verification` ที่ top ของไฟล์
4. Commit: `chore: refresh STANDARDS.md (<standard> verified current as of <date>)`

## Automation (Layer 3 — active)

[GitHub Action workflow](.github/workflows/standards-recheck.yml) ตั้งให้ run **ทุกวันที่ 1 ของเดือน 09:00 ไทย** (02:00 UTC):

1. รัน [`scripts/recheck_standards.py`](scripts/recheck_standards.py) — fetch iso.org สำหรับ ISO 15189 / ISO 15190 → regex หา current edition
2. ถ้าพบ newer edition → update STANDARDS.md → auto-commit + push to main
3. ถ้า fetch/parse error → open GitHub issue ติด label `standards-recheck` `needs-attention`
4. ถ้าไม่มี diff → update เฉพาะ "Last full verification" + "Next scheduled" → commit

**User effort = 0** — ระบบ self-heal เมื่อ ISO ออก revision ใหม่ + เตือนเมื่อต้องดู

**Manual trigger** ได้ที่ GitHub repo → Actions tab → "Monthly standards recheck" → "Run workflow"

### Scope ของ Layer 3
- ✅ ISO 15189 (Edition + year)
- ✅ ISO 15190 (Edition + year)
- ⏳ AABB Technical Manual — pending (aabb.org ไม่มี stable URL pattern เหมือน iso.org → ใช้ Layer 1/2 อย่างเดียวก่อน)
- ⏳ ISO/IEC 17025, ISO 9001 — เพิ่มได้ใน `SOURCES` list ของ script
