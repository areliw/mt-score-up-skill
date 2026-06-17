# External study — Ponytail (teardown แบบหมดทุกหยด + บทเรียนเข้า repo)

> ศึกษา [`DietrichGebert/ponytail`](https://github.com/DietrichGebert/ponytail) (21k★, MIT) —
> agent-skill บังคับ AI เขียนโค้ดน้อยสุด ("lazy senior dev: the best code is the code never written").
> **Verified จาก repo จริงทุกไฟล์ 2026-06-17/18** (eval · hooks · adapters · skills · tests). เป้า:
> สกัด *ทุก* technique/schema/number/caveat แล้ว **take/drop** เทียบ repo เรา.
>
> ⚠️ **คนละ distribution model:** Ponytail = plugin เสียบ *coding agent* (always-on rules) · เรา =
> **paste-in judgment skill** สำหรับ MT ไทย (on-demand, ส่วนใหญ่ไม่มี GitHub). อ่านแบบเลือกรับ.

---

## 1. โครงสร้าง + drift-guard จริง (แก้ความเข้าใจรอบแรก)
- **source of truth:** `skills/<name>/SKILL.md` (top-level) = แก่น · `AGENTS.md` = compact always-on derived · adapter ต่อ platform
- **drift-guard มีจริง (สำคัญ — เทียบ build_triage เรา):**
  - `scripts/check-rule-copies.js` = **CHECK-only gate** (เหมือน build_triage CI เรา): (1) **byte-compare** body ของ 5 adapter (`.cursor/.mdc` `.windsurf` `.clinerules` `.kiro` `.github/copilot-instructions.md`) กลับไป `AGENTS.md` หลัง normalize → ต่าง = exit 1 · (2) **invariant canary**: 13 วลีวิกฤต (เช่น `"ONE runnable check"`, `"input validation at trust boundaries"`) **ต้องมีทั้งใน SKILL.md และ AGENTS.md** → หาย = exit 1
  - `scripts/build-openclaw-skills.js` = **generator** เฉพาะ openclaw mirror (truncate description ≤160 ตัวอักษร)
  - → adapter 5 ตัว = static hand-maintained **แต่ถูก gate** ไม่ใช่ generated. invariant-canary = ของใหม่ที่เราไม่มี

## 2. EVAL harness (บทเรียนหนักสุด — ตรงกับ "ปรับแล้วต้องเทสต์โจทย์ยาก")
- **tool:** promptfoo (YAML: `providers` model+max_tokens/temp · `prompts` = JS export `(vars)=>[{role,content}]` · `defaultTest.assert` = JS files · `tests` = `{vars:{task}}`)
- **3 arms (ไม่ใช่ 2):** `baseline.js` (user msg เปล่า = null control) · **`caveman.js` = competing control** (skill อีกตัวที่แค่ "จงสั้น" — token-compression, 5 ระดับ) · `ponytail.js` (skill จริง). → ทดสอบ **"skill vs skill" ไม่ใช่แค่ "skill vs ไม่มี"** = แยกว่า lift มาจาก *judgment เฉพาะ* หรือแค่ "ตอบสั้น/พยายามขึ้น"
- **correctness gate (`correctness.js`):** spawn Python/Node subprocess รันโค้ด+assert (timeout 10s) → `{pass,score:0|1}`. email/debounce/CSV = **รันจริง** · React/FastAPI = **keyword/structural เท่านั้น** (ยอมรับว่า "verify plausible structure ไม่ใช่ full correctness")
- **`--selftest` ก่อนเผา API:** ทุก instrument มี `good` ref (ต้องผ่าน) + `bad` ref (ต้อง fail) → verify เครื่องมือวัดก่อนยิงจริง. **เราไม่มี — นี่คือกุญแจ**
- **gate-bug honesty:** `correctness-gate-fix.md` เล่าว่า **72/74 "failure" จริงๆ คือ bug ของ harness** (อ่าน unfenced code ไม่ได้ + เช็คของที่ prompt ไม่ได้ขอ) ไม่ใช่โมเดลพลาด → บทเรียน: harness โกหกได้ (ตรงกับ [[feedback_test_harness_can_lie]] เรา)
- **metrics:** LOC (นับ fenced block, ตัด comment/blank · measurement ไม่ gate) · cost (USD จริงจาก promptfoo telemetry) · latency · behavior gates (prose≥45 คำ / onecheck / hardware)
- **n:** median (ไม่ใช่ mean) ของ **10 reps** (cost re-verify 30) · robustness audit n=20-40
- **honesty ที่ต้องเลียนแบบ:** revise claim ลง (47-77%→42-75% หลัง 30-rep) · ระบุ scope (ดีเฉพาะ Claude; GPT แพงขึ้น 26-39%) · drop ~22/1350 transient + บอกตรงๆ · **ปฏิเสธ ship skill-text ที่ไม่ขยับ metric** ("cargo-cult Ponytail exists to prevent") · เตือน OpenAI auto-cache ทำ token telemetry เป็นศูนย์ (ต้อง vary seed token/rep)

## 3. การ "ทดสอบ skill file" (= roadmap W3 ของเรา ทองคำ)
- `behavior.test.js` — **assert รูปร่าง output ไม่ต้องใช้ API**: probe `hardware`/`explanation`/`onecheck` → `assert score==1` · probe ที่ไม่รู้จัก = "skipped" ไม่ fail
- `correctness.test.js` — **known-good vs known-bad**: ต่อ task มี output ถูก 1 + ผิดจงใจ 1 (validator always-true, CSV ฮาร์ดโค้ด, timer ไม่ cleanup) → assert ถูกผ่าน/ผิดถูกจับ
- `openclaw-skills.test.js` — build-integrity: generated==committed (ไม่ stale) · description≤160 · ends-with canonical
- `commands.test.js` — adapter completeness: ทุก command มีไฟล์ครบทุก platform

## 4. Skill craft (เทียบ forks+กับดัก เรา)
- **frontmatter เขา:** `name`/`description`/`license` เท่านั้น (เราข้อมูลรวยกว่า — เก็บของเรา) · **แต่บังคับ description ≤160 ตัวอักษร 1 บรรทัด** (เราไม่มี gate)
- **The Ladder** (6 ชั้น YAGNI) = forks เราบีบเป็น numbered "ลองนี่ก่อน แล้วค่อยนี่" — **ลำดับ = ตัว judgment** สแกนง่ายกว่า prose
- **intensity lite/full/ultra** = ปรับ "ความดุ" ของ AI → map clinical: lite=flag เฉยๆ · full=แนะนำ+hedge · ultra=ท้าสมมติฐานคนสั่ง → ให้ MT คุมระดับตามประสบการณ์
- **"when NOT / boundaries" block** = เขียน out-of-scope ในสกิลเอง ("Not lazy about: input validation, security, accessibility...") = **hedge-instinct เดียวกับ flag-only clinical เรา แต่ explicit** → เราควรมี `## ไม่ใช้เมื่อ`
- **กับดัก + upgrade-trigger:** เขา `[code] → skipped: X, add when Y` (บอกทั้งที่ข้าม + เงื่อนไขกลับมาใช้) · ของเราส่วนใหญ่แค่ "ระวัง X" → ควรเป็น **"ระวัง X — ข้ามได้เมื่อ [เงื่อนไข]"**
- **`ponytail:` inline marker** = ทิ้งร่องรอยจุดที่ลัด + ceiling/upgrade-path ใน output → analog: ให้ AI mark `[ยืนยันกับ SOP]` ตรง threshold ที่ hedge → ทำกฎ "hedge ทุกเลข" เป็นรูปธรรมที่ MT เห็น
- **worked example format:** task → without (N บรรทัด) → with (M บรรทัด) → เหตุผล 1 บรรทัด → `skipped: A,B — add when needed` · **quantified delta เด่น ("267→9 lines")** · raw model output verbatim → เราวัด Δ แต่ไม่เคย publish before/after ต่อสกิล

## 5. Command suite (เขาแยก 1 command = 1 output type)
| ponytail | ทำอะไร | analog เรา |
|---|---|---|
| `/ponytail-review` | สแกน diff หา over-engineering (ไม่แก้) | `/[skill]-audit` สแกน case write-up หา over-elaboration/fork ที่พลาด |
| `/ponytail-audit` | สแกนทั้ง repo → ranked simplify list | repo-wide หา judgment ซ้ำข้ามสกิล (≈ `check_duplicates.py`) |
| `/ponytail-debt` | harvest `ponytail:` marker → debt ledger | `/skill-debt` harvest `[ยืนยัน]`/`TODO`/draft-status → ledger รับผิดชอบ |
| `/ponytail-help` | capability card | `/skill-help` ต่อ cluster ลด onboarding friction |

## 6. Distribution / packaging (per-platform)
| platform | path | format/schema key |
|---|---|---|
| Claude Code | `.claude-plugin/plugin.json` | `name,version,description,author,interface{...},skills:"./skills/"` |
| Claude marketplace | `.claude-plugin/marketplace.json` | `$schema,name,owner,plugins[]{name,description,source,category}` |
| Codex | `.codex-plugin/plugin.json` | superset + `homepage,repository,license,keywords` |
| Gemini CLI | `gemini-extension.json` | `name,version,description,contextFileName:"AGENTS.md"` |
| Cursor | `.cursor/rules/*.mdc` | frontmatter `description/globs/alwaysApply` |
| Copilot/Windsurf/Cline/Kiro | `.github/copilot-instructions.md` / `.windsurf` / `.clinerules` / `.kiro/steering` | plain md (rule body) |
| slash cmd | `commands/*.toml` | `description=` · `prompt=` (`{{args}}`) |
| generic | `.agents/plugins/marketplace.json` | `name,source(git+branch),policy{installation,authentication}` |

## 7. Runtime / hooks (optional auto-load — เราเป็น paste-only)
- **`SessionStart` hook** (`matcher:"startup|resume|clear|compact"`, timeout 5s) → script อ่าน flag file `~/.claude/.ponytail-active` → cat skill section ที่ตรง mode → **print stdout** → Claude Code prepend เข้า system prompt (zero paste)
- **`UserPromptSubmit` hook** → parse `/ponytail lite|full|ultra|off` (+ natural "stop ponytail") → เขียน flag file (cross-process state)
- **dual `bash:`/`powershell:` key** ใน hooks.json (ไม่ branch OS ที่ caller) + fallback hardcoded ถ้าไฟล์หาย (ไม่ inject ว่างเงียบ) · env detect `COPILOT_PLUGIN_DATA`/`PLUGIN_DATA` → output คนละ schema ต่อ agent

---

## ADOPT backlog (รวมทุก agent · prioritized)
| P | action | ที่มา | model fit |
|---|---|---|---|
| **P0** | description ≤160 char gate + required-section-heading check + `dist/all-skills.md` stale check → `validate_repo.py` | openclaw-skills.test | ✅ ตรง |
| **P0** | **invariant-canary** ใน CI: 10-15 วลีวิกฤตต้องคงอยู่ในสกิลหลัก + triage → จับ silent editorial drift | check-rule-copies.js | ✅ ตรง |
| **P0** | `## ไม่ใช้เมื่อ` (out-of-scope explicit) เข้า template สกิล clinical | when-NOT block | ✅ safety |
| **P1** | **control arm ที่ 3 ใน A/B** (with / without / generic-careful) → delta-of-deltas (ที่ `ab-test-judgment` สอนเองแต่ harness ยังไม่ใช้) | caveman arm | ✅ ตรง |
| **P1** | **`--selftest`**: ทุก trap case มี gold(≥4)+known-bad(≤2) ref → รัน judge offline, abort ถ้า spread<2 | selftest+known-good/bad | ✅ ตรง |
| **P1** | **correctness/safety gate แยกจาก helpfulness 0-5**: binary "ชี้ fork ถูก? flag กับดัก? ไม่แนะนำอันตราย?" ต่อ fork | correctness.js split | ✅ = W3 |
| **P1** | median ≥10 reps (ไม่ใช่ 3) + report Δ min/max ต่อสกิล + log n-drop >5% = halt | n-discipline | ✅ ตรง |
| **P1** | กับดัก format → "ระวัง X — ข้ามได้เมื่อ [Y]" (upgrade-trigger) | skipped/add-when | ✅ craft |
| **P1** | published worked example ต่อสกิล (`skills/examples/` หรือ `examples/`) quantified before/after | examples/ | ✅ craft |
| **P2** | forks → numbered ladder ที่ "ลำดับ = judgment" + ✓-state verdict ตอนผ่านครบ | The Ladder | ✅ craft |
| **P2** | `commands/*.toml` slash commands (`/mt-triage` + per-skill) + `gemini-extension.json` (contextFileName:AGENTS.md) | toml + gemini-ext | ✅ low-effort win |
| **P2** | unit-test judgment: ต่อ fork มี MT-answer ถูก 1 + classic-wrong 1 → assert สกิลจับ wrong (no/low API ถ้า cache response) | correctness.test.js | ✅ = W3 gold |
| **P2** | `## ระดับ (lite/full/ultra)` table ในสกิลที่ความดุควรปรับตาม seniority | intensity | 🟠 บางสกิล |
| **P3** | optional Claude Code **auto-load hook** (SessionStart stdout-inject + flag-file + dual bash/ps1) — `/mt-skill <slug>` ไม่ต้อง paste (~40 บรรทัด) | hooks/ | 🟠 ถ้าขยายสู่ dev |
| **P3** | `/skill-debt` harvest `[ยืนยัน]`/TODO/draft → ledger | ponytail-debt | 🟠 nice |

## DROP (+เหตุผล)
- **adapter static rules หลาย IDE** (.cursor/.windsurf/.clinerules/.kiro) — เหมาะ always-on coding guardrail ไม่ใช่ paste-in on-demand · ยัด 90+ สกิลเป็น ambient rule = ท่วม context
- **OpenClaw build / .agents marketplace (git-install policy)** — surface ไม่ตรงกลุ่ม MT ไทย + auth complexity เกินจำเป็น
- **statusline ps1/sh · OpenCode/pi extension · `%APPDATA%` config · resolveSessionMode จาก history** — over-engineered สำหรับ paste-in v1
- **intensity modes แบบ behavior-injection ต่อเนื่อง** — เราตอบเป็นเคส ไม่ใช่ inject ทุก turn (แต่ table lite/full/ultra ในสกิล = เอา ดู P2)

## Convergence
Ponytail (21k★) ยืนยัน thesis เรา (แพ็กวิจารณญาณรุ่นพี่เป็นไฟล์พกพา) มีตลาดจริง · ใช้ AGENTS.md+skills เหมือนกัน · มี check-gate (เหมือน build_triage) + "boundaries/when-NOT" (เหมือน flag-only) · honesty bar (report failed fix, ปฏิเสธ ship text ไม่ work) = ethos เดียวกับ `eval/METHOD.md`. ต่างที่โดเมน + distribution. **บทเรียนหนักสุด = eval (control arm · selftest · correctness gate · n≥10)** + การ **unit-test skill file** (W3).
