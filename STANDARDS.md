# Standards Reference — Verified Editions

> **Source of truth สำหรับ AI** เมื่อสร้าง WI — AI ต้องอ้าง edition ตามไฟล์นี้, **ไม่ใช่ knowledge cutoff ของ AI**
>
> ถ้า AI มี web_search → verify จาก iso.org / aabb.org / clsi.org ก่อน + cross-check ไฟล์นี้
> ถ้าไม่มี → ใช้ไฟล์นี้ + flag user ถ้า `last_verified` > 90 วันจากวันปัจจุบัน

---

## Last full verification

**Date:** 2026-06-03
**Method:** WebSearch via Claude Code agent
**Next scheduled recheck:** 2026-07-01 (30-day cadence — see "Automation (Layer 3 — active)" below + [scripts/README](scripts/README.md))

---

## Verified editions

### Primary (ใช้ใน WI ทุกฉบับ)

| Standard | Current edition | Published | Notes | Last verified |
|---|---|---|---|---|
| **ISO 15189** | `:2022` (4th ed) | 2022-12 | Replaces :2012. Risk-based thinking + ISO 22870 (POCT) merged in. | 2026-06-01 |
| **ISO 15190** | `:2020` | 2020 | Replaces :2003. ⚠️ **ISO/AWI 15190 in draft** (Nov 2025) — monitor | 2026-06-01 |
| **AABB Technical Manual** | `21st edition` | 2023 | Blood Bank — *เนื้อหาเทคนิค/วิธี* (PRC/component prep WIs) | 2026-06-03 |
| **AABB Standards (BB/TS)** | `35th edition` | 2026-04 (effective 1 Apr 2026) | Standards for Blood Banks & Transfusion Services — *ข้อกำหนด accreditation* (**คนละเล่มกับ Technical Manual**); รอบ 24 เดือน ถัดไป ~เม.ย. 2028 | 2026-06-03 |

### Secondary (ใช้ตามแผนก/ความเกี่ยวข้อง)

| Standard | Current edition | Published | Used in | Last verified |
|---|---|---|---|---|
| ISO/IEC 17025 | `:2017` | 2017 | General lab competence | ⏳ pending |
| ISO 9001 | `:2015` | 2015 | QMS framework | ⏳ pending |
| ISO 22367 | `:2026` | 2026-04 | Risk management (cited in 15189:2022) | verified 2026-06-07 (replaced :2020) |
| ISO 35001 | `:2019` | 2019 | Biorisk management (cited in 15189:2022) | ⏳ pending |
| CLSI guidelines | (varies per doc) | — | Method-specific | ⏳ pending |

### Withdrawn / Merged

| Standard | Status | Replacement |
|---|---|---|
| ISO 22870 (POCT) | Withdrawn | Merged into ISO 15189:2022 |
| ISO 15189:2012 | Superseded | ISO 15189:2022 |
| ISO 15190:2003 | Superseded | ISO 15190:2020 |
| ISO 22367:2020 | Superseded | ISO 22367:2026 (พ.ค. 2026) |
| AABB Tech Manual 20th | Superseded | 21st edition (2023) |
| AABB Standards 34th | Superseded | 35th edition (effective 1 Apr 2026) |

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
2. ถ้าพบ newer edition → STANDARDS.md ไม่ถูกแก้ → เปิด issue/PR ให้คนรีวิว/อัปเดตเอง (ไม่มี auto-commit/push)
3. ถ้า fetch/parse error → open GitHub issue ติด label `standards-recheck` `needs-attention`
4. ถ้าไม่มี diff → update เฉพาะ "Last full verification" + "Next scheduled" → commit (auto-commit เฉพาะกรณีนี้)

**User effort ต่ำ** — ระบบ auto-refresh วันที่เมื่อไม่มี diff + เปิด issue/PR เตือนเมื่อ ISO ออก revision ใหม่ (การ apply edition ใหม่เข้า STANDARDS.md ยังต้องให้คนรีวิว ไม่ apply เอง)

**Manual trigger** ได้ที่ GitHub repo → Actions tab → "Monthly standards recheck" → "Run workflow"

### Scope ของ Layer 3
- ✅ ISO 15189 (Edition + year)
- ✅ ISO 15190 (Edition + year)
- ⏳ AABB Technical Manual — pending (aabb.org ไม่มี stable URL pattern เหมือน iso.org → ใช้ Layer 1/2 อย่างเดียวก่อน)
- ⏳ ISO/IEC 17025, ISO 9001 — เพิ่มได้ใน `SOURCES` list ของ script
