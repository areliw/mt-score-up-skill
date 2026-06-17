# External study — Ponytail (เทียบโครงสร้าง + บทเรียนเข้า repo)

> ศึกษา [`DietrichGebert/ponytail`](https://github.com/DietrichGebert/ponytail) (21k★, MIT) —
> agent-skill ที่บังคับ AI เขียนโค้ดให้น้อยสุด ("lazy senior dev: the best code is the code
> never written"). Verified จาก repo จริง 2026-06-17. เป้า: เทียบสถาปัตยกรรม skill / AGENTS.md /
> eval กับของเรา แล้ว **take/drop** — ไม่ใช่ลอกตาม.
>
> ⚠️ **คนละ distribution model:** Ponytail = plugin เสียบ *coding agent* (Claude Code/Cursor/Copilot…) ·
> เรา = **paste-in judgment skill** สำหรับ MT ไทย (ส่วนใหญ่ไม่มี GitHub). หลายอย่างของเขาเหมาะ model
> เขา ไม่ใช่ของเรา — อ่านบทเรียนแบบเลือกรับ.

## โครงสร้างเขา (verified)
- **hub-and-spoke:** `skills/*/SKILL.md` = แก่น · `AGENTS.md` = compact derived · adapter ต่อ platform
  (`.cursor/` `.windsurf/` `.clinerules/` `.github/copilot-instructions.md` `.kiro/` `.codex-plugin/`
  `.claude-plugin/` `.openclaw/` `.opencode/`) — **manual align ไม่มี build/sync** (เขายอมรับเองใน
  `docs/agent-portability.md`)
- **SKILL.md = Anthropic Agent Skills format:** frontmatter `name`/`description`/`homepage`/`license`
  + sections (the ladder 6 ชั้น / rules / intensity lite-full-ultra / **when NOT / boundaries**) ~1,100 คำ
  → **installable** (skill-capable host auto-load ได้)
- **`benchmarks/` = eval จริง:** 3 arms — baseline / **caveman (= "จงสั้น" prose-compression control)** /
  ponytail · metrics LOC + **cost (USD จริง)** + latency + **correctness gate (รันโค้ดจริง)** · promptfoo ·
  median 10 runs (cost re-verify 30) · robustness audit n=20-40 หา "constraint ทำโค้ดผิดไหม" ·
  **report failed fix 8 ครั้ง + ปฏิเสธ ship skill-text ที่ไม่ขยับ metric** ("adding skill text that
  doesn't work is the cargo-cult Ponytail exists to prevent")

## เทียบกับเรา
| มิติ | Ponytail | เรา (mt-score-up-skill) | verdict |
|---|---|---|---|
| source of truth | skills/ + AGENTS.md, adapter **manual** | AGENTS.md + `@import` + **generated catalog** (build_triage) | เรา drift-proof กว่าในส่วนที่ครอบ — แต่ครอบ 2 agent · เขา 13 (แลกกับ manual) |
| skill format | **SKILL.md (name+desc) = installable** | custom frontmatter = **paste-in เท่านั้น** | ⚠️ strategic gap → บทเรียน #3 |
| eval arms | 3 (มี **control**) | 2 (with/without) | 🔴 บทเรียน #1 |
| eval metrics | LOC + cost + latency + **correctness gate** | helpfulness 0–5 เท่านั้น | 🔴 บทเรียน #2 |
| eval runs | 10–40 | 3 | 🟢 บทเรียน #4 |
| honesty | report failed fix, ไม่ ship text ที่ไม่ work | `eval/METHOD.md` ethos เดียวกัน | ✅ ยืนยันมาถูกทาง |

## บทเรียน take → เข้า repo (prioritized)
1. 🔴 **เพิ่ม control arm ใน A/B** — เขาเทียบ baseline / caveman(แค่ "จงสั้น") / ponytail เพื่อพิสูจน์ว่า
   lift มาจาก *judgment เฉพาะ* ไม่ใช่แค่ "พยายามมากขึ้น/สั้นขึ้น". เรามีแค่ with/without → ควรเพิ่ม arm
   "generic-careful" แล้ววัด **delta-of-deltas** (ซึ่ง `ab-test-judgment` ของเราสอนไว้เอง แต่ harness ยังไม่ใช้).
   เคสที่ probe เพิ่งเจอ (textbook trap → tie) จะตีความชัดขึ้นเมื่อมี control
2. 🔴 **เพิ่ม correctness/safety gate แยกจาก helpfulness** — skill ที่ "ช่วย" แต่ output ผิด = แย่กว่าไม่มี.
   เขา gate ด้วย runnable check; ของเรา clinical → gate "ไม่แนะนำสิ่งอันตราย / ไม่เกินขอบเขต MT" เป็น
   pass/fail แยก (METHOD มี Layer-1 audit + Layer-1b lit-check แต่ยังไม่รวมเข้า A/B run ต่อเคส)
3. 🟠 **SKILL.md installability (strategic fork — บันทึกไว้ ยังไม่ทำ)** — สกิลเรา paste-in ไม่ใช่ installable
   Agent Skill. ถ้าอยากให้ skill-capable host auto-load ต้อง frontmatter `name`+`description` แบบ SKILL.md.
   **ไม่ทำตอนนี้** — paste-in = เจตนา low-friction สำหรับ MT ที่ไม่มี GitHub; แต่เก็บเป็นทางเลือกถ้าจะขยายสู่
   สาย dev/agent (อาจ dual-publish: frontmatter เราคงไว้ + เพิ่ม `name`/`description` ให้ SKILL.md-compatible)
4. 🟢 **เพิ่ม runs เมื่อ metric ตัดสิน promote** — n=3 ของเรา light (METHOD ยอมรับ); metric ที่ใช้ flip
   semi-stable ควร ≥10
5. 🟢 **promptfoo เป็นทางเลือก harness** — declarative/reproducible/shareable · แต่ blind-judge + Thai +
   per-fork trap ของเราเป็นจุดแข็งที่ promptfoo ไม่มี → พิจารณา hybrid ไม่ใช่แทนที่
6. ✅ **honesty bar — ยืนยันถูกทาง ไม่ต้องแก้** — เขา report failed fix + ปฏิเสธ ship text ที่ไม่ขยับ metric
   = ethos เดียวกับ METHOD.md เรา

## บทเรียน drop (ไม่เอา + ทำไม)
- **adapter หลาย platform (Cursor/Copilot/Windsurf rule files)** — เหมาะ plugin model ของเขา ไม่ใช่ paste-in
  ของเรา; ถ้าทำต้องมี generator (เขายัง manual = drift) → skip จนกว่าจะเปลี่ยน distribution model
- **intensity modes (lite/full/ultra)** — เหมาะ behavior-injection ต่อเนื่อง ไม่ใช่ judgment skill ที่ตอบเป็นเคส

## Convergence ที่น่าสังเกต
Ponytail = หลักฐานว่า thesis เรา (แพ็ก *วิจารณญาณรุ่นพี่* เป็นไฟล์พกพา) มีตลาดจริง (21k★) · ใช้
`AGENTS.md` + `skills/` เหมือนเรา · มี "when NOT / boundaries" = hedge-instinct เดียวกับ flag-only clinical
ของเรา. ต่างที่โดเมน (coding minimalism ↔ MT judgment) + distribution (install ↔ paste). บทเรียนที่หนักสุด
อยู่ที่ **eval** (control arm + correctness gate) — ตรงกับที่เพิ่งคุยกันว่า "ปรับแล้วต้องเทสต์ด้วยโจทย์ยาก".
