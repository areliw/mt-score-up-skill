# Changelog

Notable changes to the MT Score UP! skills hub. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/). **มาตรฐานความพร้อม 3 ชั้น:**
`draft` (ยังไม่ verify / มี blocker) → `semi-stable` (ผ่าน Codex review + empirical stress-test, ไม่มี error ที่รู้ — **แต่ยังไม่ผ่าน formal/clinical peer-review**) → `stable` (ผ่าน clinical/formal peer-review — *สงวนไว้ ยังไม่มีสกิลใดถึง*).
ปัจจุบัน: 35 สกิล non-clinical ที่ผ่าน Codex review + empirical eval = `semi-stable` · สกิลกลุ่ม clinical (🩸) + ตัวที่ยังมี blocker = `draft`.

## [Unreleased]

### Added
- `histotech-cytology-judgment` — งาน histo/cyto ระดับ **process** (W1 gap-fill, สกิลที่ 93; *MT ไม่วินิจฉัย*): specimen adequacy (flag/แนะนำ recollect) · fixation/cold-ischemia/decalc กระทบ IHC-molecular (ER/PR/HER2) ทำซ้ำบนเนื้อเดิมไม่ได้ · air-dried vs wet-fixed ให้ตรง stain · artifact vs จริง (re-cut/re-stain) · control fail = invalid≠negative. 🩸 clinical — `draft` · **ผ่าน codex 2 รอบ** (hedge: Pap/TZ adequacy ไม่ใช่ "ไม่มี TZ=unsat", fixation→IHC ไม่ absolute, control-scope ต่อ assay, recollect = flag ตาม SOP/พยาธิแพทย์). flag-only.
- `result-release-judgment` — ด่าน post-analytical/ปล่อยผล (W1 gap-fill, สกิลที่ 92): ปล่อย/repeat/recollect/hold/escalate · delta-check เด้ง→แยกเปลี่ยนจริง/artifact/**specimen mix-up** · autoverify stop-rule · critical value (read-back+log) · corrected/amended report. 🩸 clinical — `draft` · **ผ่าน codex 2 รอบ** (แก้ overstatement: delta-mixup ไม่ใช่กฎ, AMR≠reportable-range, read-back/corrected-amended ตาม SOP/accreditor, CLSI AUTO15 ไม่ใช่ AUTO10). flag-only verify.
- `receiving-review-judgment` — รับ/ตอบ feedback (code review · รีวิวเปเปอร์ · หัวหน้าติ · codex/CI) ให้เป็น: triage **take/drop/push-back** (ไม่ caved/ไม่ ego) · disagree-and-commit **ยกเว้น correctness/security/legal** · อ่าน nit ที่ชี้ root · AI-review = **verify ก่อน apply** ไม่เชื่อดิบ. สกัดจากการเทียบ repo กับ `obra/superpowers` — ช่องว่างเดียวที่เป็น judgment แท้ (สกิลที่ 91) — `draft` (ผ่าน codex).

### Changed
- **W1 forks (3 สกิลเดิม เติม fork ปิด wave content-void):** ทุกตัวผ่าน codex review · clinical = flag-only · ตัวเลข hedge เป็น teaching illustration ผูก SOP/มาตรฐาน
  - `clinchem-judgment` +**Fork 7 operational continuity** — เครื่องหลักล่ม/โหลดถล่ม → triage critical/STAT ก่อน routine · backup/manual ใช้ได้เฉพาะ run QC ผ่าน + รู้ comparability ข้ามเครื่อง · ส่งต่อ · แจ้ง ward เชิงรุก (เร็ว>ครบ) · เครื่องกลับมาอย่า dump backlog ก่อน run QC (แยกจาก accept/reject run ปกติ Fork 1)
  - `lab-management-judgment` +**Fork 9 EQA/PT failure investigation** — สอบสวนเป็นระบบก่อน CAPA (clerical→IQC→peer/method-group→lot→competency) · PT sample commutability/matrix · miss เดี่ยว≠systematic · **ห้ามรันซ้ำจนผ่าน/แลกผล PT (referral)=เพิกถอน accreditation** (ต่อยอด Fork 2 EQA concept)
  - `infection-control-judgment` +**Fork 7 chemical/occupational safety** — formalin/xylene → **fume hood ไม่ใช่ BSC** (type A หมุนเวียนไอเคมี) · exposure limit = teaching ยึดเกณฑ์พื้นที่ · spill ใหญ่/ระเหย=อพยพ+เรียกทีม (เคมี≠ชีวภาพ) · ของเสียแยก incompatibility/ห้ามลงท่อ · ขยาย scope เป็น lab safety (ชีวภาพ+เคมี/อาชีวะ)
- `mt-career-judgment` — เพิ่ม **Fork 1B "ราชการสายข้าง: ทนพ → นวก./สสจ./สคร."** (เคสจริงจากคอมมูฯ MT, ตัวเลข case-specific ต้อง verify): break-even = heuristic "คุ้มต่อเมื่อไปไกลถึงเชี่ยวชาญ (ชช.)" · comp-cliff เคสเล่าเงินรวมหาย ~20K/เดือน (ฉ.11+พตส.+เงินตำแหน่ง+ค่าเวร) — ยืนยันสิทธิ์กับ HR ก่อน · บางหน่วยลังเลรับคนนอกสาย นวก. (ไม่ใช่กฎ ก.พ.) + 2 anti-pattern. PII-clean · ผ่าน codex review (PR #40)

## [0.9.0] — 2026-06-15

### Added
- `interprofessional-communication-judgment` — สื่อสารสหวิชาชีพแนวราบ (พูดภาษาของแต่ละวิชาชีพ) + golden-period: แจ้งเร็วสำคัญกว่าแจ้งครบ (สกิลที่ 89)
- `professional-voice-exit-judgment` — Hirschman voice/exit/loyalty สำหรับการตัดสินใจเชิงองค์กร/สภาวิชาชีพ: เลือกท่า (อ่านช่องรับฟัง+ทางเลือกจริง ไม่ใช่ reflex ต้นทุน) · ส่ง voice ให้เป็นสัญญาณไม่ใช่โจมตี · ผู้บริหารอ่านเสียงบ่น (lazy-monopoly) · governance ใครตัดสิน-vs-ใครแบกผล (สกิลที่ 90) — `draft` (ผ่าน codex แล้ว, รอ stress-test)

### Changed
- **Round 6 — full blind-judge A/B coverage 89/89:** upgrade 36 SCREEN-only skills (round 4-5 light-screen) → full blind-judge (Haiku answerer + Opus blind judge, 3-run avg). ผล: **17 lift(real, Δ>1.4) · 18 safe · 1 regression (พบ+แก้แล้ว)**. ทุกสกิลมี Δ จริงครบแล้ว. ดู [`eval/round6-probe.md`](eval/round6-probe.md). **Library-wide 0 regression หลังแก้.**
- **`deep-research` demote `semi-stable` → `draft` + no-tool guard:** round 6 พบว่าเป็น *tool-execution* skill — โมเดลที่ไม่มี search/fetch tool โหลดแล้ว **fabricate citation table** (regression −0.33). เพิ่ม guard หัวไฟล์ (ไม่มี tool → ห้ามสร้างตาราง/ลิงก์เอง ส่งแผนการค้นแทน); re-verify แล้ว regression ปิด (rescued·tie·tie, +0.67, 0 regression) → codex ตรวจ guard ผ่าน → **re-promote กลับ `semi-stable`** (เป็น semi-stable ที่มี guard แล้ว).
- **Promote round 6 → `semi-stable` (codex-gated) — 7 ตัว:** ผ่าน A/B lift + codex review. รอบแรกผ่าน 2 (`report-up-judgment` · `writing-judgment`); อีก 5 codex BLOCK เพราะยก heuristic เป็นกฎสากล/overstate → **hedging-fix แบบ surgical (default/depends/verify, ไม่ bloat) → re-codex ผ่าน 5/5** → promote: `interprofessional-communication-judgment` · `humanize-ai-writing` · `ab-test-judgment` (แก้ p-hacking→judge bias, threshold เป็น rule-of-thumb) · `lead-intelligence-judgment` · `lab-clinic-business-judgment`.
- **`mt-career-judgment` +Fork 7 (สายแล็บข้างเคียง):** เพิ่มการตัดสินใจ diversify เข้าแล็บอาหาร/เกษตร/QC/โภชนาการเมื่อสาย bench ตัน — กับดัก "งานสบาย/ไม่ต้องแม่น" (จริงๆ ความเข้มงวดอยู่ที่ validate method + accreditation ISO/IEC 17025 + legal liability ทั้งล็อต) · กับดัก gatekeeping ("งานนอกคลินิก = ไม่ใช่ MT") · 4 เกณฑ์อ่านโอกาส.
- **Maturity ladder ใช้เต็มรูป (`draft` → `semi-stable` → `stable`):** promote 29 สกิล non-clinical (กลุ่มโค้ด/เทคนิค/data · ใช้ AI · วิจัย/สถิติ core) เป็น `semi-stable` หลังผ่าน Codex review + empirical eval. 4 สกิล R2R-stats (`choose-stat-test` / `r2r-stats` / `research-design-judgment` / `critical-appraisal-judgment`) rework แก้ความถูกต้องเชิงสถิติแล้ว promote.
- **R2R wave สุดท้าย:** promote อีก 6 สกิลวิจัย/สถิติ (`r2r-research-proposal` · `sample-size-power` · `literature-review-judgment` · `deep-research` · `source-credibility-judgment` · `pubmed-search-judgment`) เป็น `semi-stable` หลัง Codex หา + ยืนยันแก้ — two-proportion N → pooled score-test (≈93/กลุ่ม), evidence/source/pyramid ขึ้นกับชนิดคำถาม (diagnostic ≠ RCT), EC = approval **หรือ** exempt determination (ไม่มีย้อนหลัง). รวม **35 semi-stable**.
- **README เกลาให้อ่านง่าย:** แก้จำนวนเป็น 89 · รวมสองส่วน Privacy / clinical-stack ที่เนื้อหาทับกันเป็นส่วนเดียว · ย่อสรุป eval เหลือประเด็นหลัก · ย่อคำอธิบาย catalog 62 รายการให้สั้น-สม่ำเสมอ (รายละเอียดเต็มยังอยู่ที่ `skills/README.md`).

## [0.8.2] — 2026-06-10

### Added — launch infrastructure
- `docs/USING.md` (ใช้ skill ครบ 7 platform incl. Claude Code/CLI) · `docs/LAUNCH.md` (แผนปล่อย แคบ→กว้าง + human-only checklist) · `docs/FEEDBACK.md` + issue template `skill-feedback.md`
- `prompts/skill-interview.md` — **Skill Maker** (AI สัมภาษณ์ถอดวิจารณญาณผู้เชี่ยวชาญ/คนเกษียณเป็นร่าง skill)
- `docs/skill-registry-spec.md` (frontmatter schema + dedup/merge play) · `scripts/check_duplicates.py` (char-3gram overlap detector, wired เข้า build-triage CI) · `CONTRIBUTORS.md` · `contributions/INTAKE.md` (maintainer playbook)
- wire ทั้งหมดเข้า README/CONTRIBUTING/triage/config/setup-custom-gpt/vision (175 links, 0 broken)

### Changed — tighten pass (55 non-clinical skills)
- 55 สกิล non-clinical: tighten density (net −30 บรรทัด, ตัดน้ำ/คม verdict-first) · ตัวบางเติม judgment ที่ขาด (เช่น `db-judgment`: UNION ALL default, keyset pagination, transaction isolation)
- **18 สกิลคลินิกไม่แตะเนื้อ** โดยตั้งใจ (flag-only — เนื้อคลินิกผิด = ฉีด error) · 0 regression · ทุก edit verify แล้ว

### Fixed — clinical peer-review (4 สกิลใหม่, AI pre-screen)
ดู [`eval/peer-review-clinical-2026-06-10.md`](eval/peer-review-clinical-2026-06-10.md):
- **🔴 `preanalytical`:** EDTA carryover **Mg↑→Mg↓** (chelation; ขัดกับ Fork 3 ในไฟล์เอง) + ALP↓ · NaF ออกฤทธิ์ช้า 1-4 ชม.แรก
- **🟠 `poct`:** glucose interference เติม landmine — ทิศ Hct · O₂ เฉพาะ glucose-oxidase · **GDH-PQQ+maltose/PD-fluid (FDA boxed warning)** · capillary ใน shock เชื่อไม่ได้ · EQA/PT
- **🟠 `flow-cytometry`:** FMO≠isotype (isotype=legacy) · gating order +time/dump · over-comp→false-neg · PNH lineage-specific/RBC caveat
- **`urinalysis`:** clean — เติม CSF xanthochromia (supernatant ปั่นทันที) + clearing ไม่ตัด SAH
- ⚠️ AI pre-screen ≠ MT เซ็นรับรอง — 4 ตัวยังคง `draft`, รอ MT คนที่สองตรวจก่อนชู public

## [0.8.1] — 2026-06-08

### Added
- `eval/round5-remaining.md` — spot-A/B ของ 26 ตัวที่เหลือ (v0.4–0.5 + `lab-clinic-business`/`ab-test`): **~24 tie · ~2 better · 0 regression**. รวมกับ round 4 → **ทั้งคลัง 87 ผ่าน A/B-screen แล้ว: 0 dangerous regression library-wide** (53 blind-judge + 34 screen)

### Notes
- screen เบากว่า round 1-3 (self-derived trap, single-pass, ไม่ blind-judge) · Haiku cold จับ trap textbook ได้เอง — รวมที่ไม่ obvious (knowledge≠judgment, moat≠เครื่องมือ, root-cause≠โทษคน) → skill เพิ่ม **specificity + forcing function** ไม่ใช่ rescue · limitation ค้าง: Haiku ≠ junior MT จริง → rescue value ต้องเทสกับคน (เอา triage ไปวางหน้า junior MT)

## [0.8.0] — 2026-06-08

### Fixed — full audit + improve pass (ทั้งคลัง 87 + repo)
audit ทั้ง 87 skill (multi-agent, confidence-filtered: clinical correctness · dup · cross-link · format · repo) → แก้เฉพาะ error จริง:
- **🔴 correctness 3:** `clinmicro` MRSA cefoxitin breakpoint **แยก species** (S. aureus ≤21 vs **CoNS ≤24 mm** — กัน under-call MRSE) · `cv-judgment` Harris "ไม่ทน scale" (เดิมกำกวม) · `photography` shutter ผูกกับ focal length (เดิม 1/50 เป็นกฎสากล)
- **🟠 clinical 8:** `bloodbank` RhIG standard dose ครอบ FMH จำกัด → KB/flow ถ้า FMH มาก · `immunoassay` HIV window เป็น range + "neg ≠ rule out" · `infection-control` droplet ≥6 ฟุต (CDC) · `clinchem` 4₁ₛ/10ₓ เงื่อนไข warning ชัด · `clinmicro` AmpC core-3 (Hafnia → หลักฐานจำกัด) · `chemistry-interpretation` urine-Cr ชาย 20–25 · `parasitology` zinc 1.18–1.20 · `urinalysis` CSF xanthochromia↔traumatic-tap แยก
- **🟠 non-clinical 3:** `mt-exam-strategy` เลิก assert เลขกฎหมาย → สอน "ชนิดกับดัก + verify ตัวบทเอง" · `lab-management` sync % pre-analytical (เดิมขัดกันเองในไฟล์) · `ml-judgment` Lasso wording

### Changed
- `data-project-survival` ↔ `data-science-workflow` คม boundary (survival ชี้ phase-map ไป workflow, เน้น decision-gate/vendor) — dup เดียวที่พบในคลัง
- README footnote v0.5.0→v0.7.0 + eval scope (53→87, +34 ยังไม่ A/B) · `eval/RESULTS.md`+`eval/ab-scorecard.md` เติม scope footnote (n=53 = คลัง ณ ตอน eval) · ลบ `docs/skill-gap-candidates.md` (scratchpad ที่ candidate ถูก add ครบแล้ว)

### Added
- `eval/round4-new-skills.md` — spot-A/B ของ 8 ตัว v0.6.0 (weak model Haiku, มี/ไม่มี skill): **8 tie · 0 rescue · 0 regression**. harness เบากว่า round-1 (trap self-derived, single-pass, ไม่ blind-judge) = **safety screen** ไม่ใช่ scorecard. ยืนยัน finding เดิม: weak model รู้ trap #1 (textbook) อยู่แล้ว → เสมอ; คุณค่า = ความสม่ำเสมอ + scaffold junior จริง (ต้องเทสกับคน). **0 regression = ไม่มี skill ใหม่ทำให้แย่ลง**

### Notes
- cross-link ครบ **100%** ไม่มี broken · frontmatter 8-key + canonical format + disclaimer ทั้ง 87 ผ่าน · **ไม่พบ 🔴 ที่อันตรายถึงคนไข้** (ทั้งหมด = precision เชิงเทคนิค) · 8 ตัวใหม่ (v0.6.0) clinically clean + spot-A/B 0 regression
- งานสร้างเสร็จ; clinical 4 ตัวใหม่ยังควร peer-review + 34 ตัวยังรอ weak-model A/B

## [0.7.0] — 2026-06-08

### Changed — graft "เพชร" จาก 19 dropped skills เข้า skill เดิม (diamond mantra)
ไม่ทิ้งคุณค่าของ 19 ตัวที่ drop ตอน reconcile PR #11 — สกัด **33 เพชร** (judgment/trap/เกณฑ์ที่ unique จริง ไม่ซ้ำ) graft เข้า **15 skill เดิม** (ตัวไฟล์ทิ้ง คุณค่าดูดเข้า skill ที่อยู่):
- **safety/coding:** `ai-coding-guardrails` (ห้าม paste PHI/secret · ห้ามรันคำสั่งลบที่ไม่เข้าใจ · backup ก่อนรัน) · `ml-engineering-workflow` (reject option · งานกระทบคนไข้=คนตัดสิน · ใช้นอกขอบเขต validate) · `offload-to-automation` (ROI gate เมื่อไหร่คุ้ม · idempotent/rollback · hardcode พังเงียบ) · `prompt-optimizer` (กัน PHI/secret หลุด)
- **data/research:** `data-science-workflow` (เปิดดู raw ก่อน clean · เก็บ raw+log transformation · median+P90 ไม่ใช่ mean · Simpson's paradox) · `molecular-judgment` (genome build hg19/hg38 + liftover) · `source-credibility-judgment` (retraction check · recency vs guideline) · `pubmed-search-judgment` (อย่าพึ่งฐานเดียว) · `manuscript-judgment` (สี colorblind-safe · bar แกนเริ่มศูนย์)
- **comms/career/learning:** `content-creator-judgment` (repurpose native · discoverability · vanity metric · teaching-objective · PDPA เคสคนไข้) · `report-up-judgment` (timing/รอบงบ · skip-level) · `market-research-judgment` (demand ≠ ถาม "สนใจไหม") · `grill-my-plan` (analysis paralysis) · `interactive-course` (spaced repetition) · `time-blocking` (สำคัญ vs เร่ง)

### Notes
- วิธี: parallel agents สกัด (diff feat-version vs main-version → propose) → apply surgical → verify (emoji-heading=0 · disclaimer footer · frontmatter 8 keys · diffstat เล็ก)
- 3/19 ไม่มีเพชร (`ship-a-small-app`·`personal-brand` ซ้ำ main; `pomodoro-focus`·`photography-judgment` ไม่รับเพิ่ม) — รายงานตรงๆ ไม่ยัด
- ขนาดไม่บวม: +40 บรรทัดรวม 15 ไฟล์ (~2-3/ไฟล์) · จำนวน skill ยัง **87** (ไม่เพิ่มไฟล์) · bundle regen

## [0.6.0] — 2026-06-08

### Added — reconcile parallel branch (T-shaped clinical expansion)
- **+8 skills (79 → 87)** — cherry-pick จาก PR #11 (`feat/t-shaped-mt-expansion`, แชทขนาน) เฉพาะตัวที่เติม **gap จริง ไม่ซ้ำ**:
  - 🩸 `urinalysis-judgment` · `preanalytical-judgment` · `poct-judgment` · `flow-cytometry-judgment` — clinical bench ที่ main ขาดสนิท
  - 🔬 `method-validation-stats` — method comparison (Bland-Altman/Deming)/reference interval/diagnostic accuracy (≠ research stats)
  - 🗂️ `phi-data-handling` — PDPA de-identify เฉพาะ PHI
  - 💻 `spreadsheet-judgment` · `mt-databases` — เครื่องมือ data รายวัน MT

### Changed
- README ทั้ง 2 (root + skills/) + count 79→87 (4 จุด) · `dist/all-skills.md` (~125K→~133K) · build_triage regenerated INDEX/triage/bundle (87, in-sync)

### Notes
- **ทิ้ง 19/27 ของ PR #11** = ซ้ำ concept กับ main (8 คู่: `deploy-ml-safely`≈`ml-engineering-workflow` · `manage-up`≈`report-up-judgment` · `prompt-craft`≈`prompt-optimizer` · `pubmed-search`≈`pubmed-search-judgment` · `source-credibility`≈`source-credibility-judgment` · `vibe-coding-safely`≈`ai-coding-guardrails` · `focus-and-time`≈`pomodoro-focus`/`time-blocking` · `market-opportunity`≈`market-research-judgment`) + generic ที่ main domain รวยแล้ว (11) → กัน dup bloat + style ชนกัน ("do-X" vs "-judgment")
- PR #11 แตกจาก 55-era → **CONFLICTING/DIRTY** กับ main (ตามหลัง 5 commit, แตะ catalog ชุดเดียวกัน) → reconcile ด้วยการ **cherry-pick ไฟล์** ไม่ใช่ `git merge`
- 8 ตัว = `status: draft` · ยังไม่ผ่าน weak-model A/B · clinical 4 ตัว (urinalysis/preanalytical/poct/flow) ยังรอ clinical peer-review

## [0.5.0] — 2026-06-08

### Added
- **+14 skills (65 → 79)** — port จากคลัง global `~/.claude/skills` ที่ใช้คู่ Life OS → reframe เป็นภาษาไทย/audience MT/วางในแชตได้ (ตัด Claude-Code/IDE-only + knowledge-only ออก):
  - 🔬 `source-credibility-judgment` · `pubmed-search-judgment`
  - 💻 `tdd-judgment` (merge tdd+python-testing) · `debugging-judgment` (merge debug-mantra+diagnose) · `ai-coding-guardrails` (karpathy)
  - 🤖 `token-budget-judgment`
  - 💬 `writing-judgment` · `report-up-judgment` (reframe management-talk → lab/รพ.)
  - 💼 `market-research-judgment` · `lead-intelligence-judgment` · `incident-postmortem-judgment` (reframe post-mortem → lab NC/CAPA)
  - 🧭 `pomodoro-focus` · `time-blocking` · `interactive-course`

### Changed
- README counts 65→79 (3 จุด) + `dist/all-skills.md` (~105K→~125K tokens) · build_triage regenerated INDEX/triage/bundle (79, in-sync) · eval honesty note: 26 ตัวยังไม่ A/B

### Notes
- ทั้ง 14 = non-clinical · `status: draft` · ยังไม่ผ่าน weak-model A/B
- ตัด ~30 ตัวจาก global ที่ off-mission (frontend/video/Claude-Code-meta เช่น overnight/handoff/ultracode, knowledge-only เช่น python-patterns) — ไม่เข้า audience MT
- merge ตัวซ้ำ: tdd+python-testing → `tdd-judgment` · debug-mantra+diagnose → `debugging-judgment`

## [0.4.0] — 2026-06-08

### Added
- **+10 skills (55 → 65)** — ชุด AI-usage / research / data / decision / sales ที่คลังยังขาด:
  - `prompt-optimizer` (#65) — วินิจฉัย+ซ่อม prompt: แก้สาเหตุที่ใช่ก่อน · few-shot · สเปก output · ไม่ยัดยาวเฟ้อ
  - `verification-panel` (#64) — ตั้งคณะตรวจ 3 มุม (Factual/Logic/Context) แบบ adversarial ก่อนเชื่อคำตอบ high-stakes
  - `write-a-skill` (#63) — แพ็กวิจารณญาณเป็น skill (judgment-not-knowledge test, type fork, PII, ส่งเข้า repo) — เป็นคู่มือ contributor ในตัว
  - `humanize-ai-writing` (#62) — เกลางานที่ AI ร่างให้เป็นคนเขียน ตัดสัญญาณ AI โดยคงความถูกต้อง/ศัพท์
  - `literature-review-judgment` (#61) — กระบวนการรีวิววรรณกรรม (search→screen→synthesize) เสริม `critical-appraisal-judgment` (อันนั้น = ประเมินเปเปอร์เดียว)
  - `deep-research` (#60) — ค้นเรื่องใดก็ได้ลึก หลายแหล่ง + cross-check ≥2 แหล่ง + cite ตรวจได้
  - `data-science-workflow` (#59) — CRISP-DM phase navigator (กัน leakage / vanity metric / skip Business)
  - `ml-engineering-workflow` (#58) — นำโมเดลขึ้นใช้จริง: reproducible train · shadow/A-B · monitor drift · rollback
  - `grill-my-plan` (#57) — ให้ AI ซักไซ้แผนแบบ adversarial ก่อน decision แก้ยาก
  - `dx-company-brief` (#56) — brief บริษัท diagnostics ก่อนสัมภาษณ์/ขาย (6-section + verify ตัวเลขตลาด)

### Changed
- README category tables + counts (55→65, 3 จุด) + `dist/all-skills.md` token estimate (~90K→~105K)
- `scripts/build_triage.py` regenerated INDEX / triage catalog / bundle (65 skills, in-sync)
- eval honesty note: ตัวที่เพิ่มหลัง eval-53 รวมเป็น 12 ตัวที่ยังไม่ A/B (ผ่าน design review)

### Notes
- ทั้ง 10 ตัว = non-clinical (AI/วิจัย/data/อาชีพ) → disclaimer ระดับเบาตามความเสี่ยง · `status: draft` · ยังไม่ผ่าน weak-model A/B (รอ round ถัดไป)

## [0.3.0] — 2026-06-07

### Added
- `ab-test-judgment` (#55) — general judgment for evaluating prompt/skill changes without chasing
  noise: credible design (own-worst-case + blind judge, no biased-judge), delta-of-deltas with a
  control, noise floor, review-vs-A/B, and scaling (test by risk×uncertainty, not count).
- `lab-clinic-business-judgment` (#54) — MT lab-clinic business: model choice (premium vs state-volume
  vs hybrid), the real moat (profession+registration+LIS-HIS), gov revenue, reading the buyer.
- `eval/IMPROVE-PLAYBOOK.md` — how to lift a skill + how to validate an edit via a controlled
  before/after (without-skill = noise control). Worked example: a per-edit A/B can't resolve a <1pt
  change against ±2–3 noise → judge edits by review, use the A/B only at library-aggregate level.
- `eval/round3/` — fixed-scenario, 2-run-averaged, harder-trap re-eval + recovery of all 53. Honest
  lift is *lower* than the noisy number (noise removed), with 0 dangerous regressions.

### Changed
- Critical "would-it-break-for-a-real-user" review over all 55 skills (**0 critical · 0 needs-work**)
  → fixed 8: `financial-statement` AFS→FVOCI (IFRS 9 currency); `bloodbank` ×5 clinical polish
  (platelet plasma-risk, Cryo-fallback, FFP→PCC, weak-D rule); `mt-career`, `ai-assistant-calibration`,
  `what-skill-do-i-need`, `photography`, `ivd-sales`, `self-development-coach`.
- Credits genericized — dropped specific institution names, kept the gratitude + non-endorsement note.
- Skill count 53 → 55.

## [0.2.0] — 2026-06-04

### Added — a real evaluation (`eval/`)
- **A/B scorecard ([`eval/ab-scorecard.md`](eval/ab-scorecard.md)):** all 53 skills, each tested on
  its *own* #1 anti-pattern, answered twice by a **weak** model (Haiku) with/without the skill,
  blind-judged 0–5. Result: **9 rescued · 16 better · 19 tie · 7 style-cost · 2 no-rescue · 0 regression.**
  No skill made a weak model's correct answer wrong.
- **Literature cross-check ([`eval/literature-check.md`](eval/literature-check.md)):** 66 clinical/method
  claims across 22 skills vs AABB/ACOG/CLSI/KDIGO/NKF-ASN/peer-review → **43 supported · 23 nuanced ·
  0 contradicted · 0 unverified**. Nuances are currency/precision upgrades, logged with sources.
- **Titanic exemplar ([`eval/titanic/`](eval/titanic/)):** `ml-judgment`'s leakage trap quantified —
  selecting features outside CV fabricates **+0.031 ROC-AUC** of fake performance (reproducible script).
- **[`eval/METHOD.md`](eval/METHOD.md) + [`eval/RESULTS.md`](eval/RESULTS.md):** the 4-layer design, the
  honest verdict, and the threats to validity. Key finding: skills lift a *weak* model / non-expert;
  a frontier model already embodies the judgment (so for it they're consistency rails, not boosts).

### Changed
- `bloodbank-judgment`: two literature-driven precision upgrades — irradiation stated as "≥25 Gy
  central, ≥15 Gy minimum to any portion" (was flat 25 Gy); fetal-anemia surveillance now leads with
  **MCA-PSV Doppler**, demoting ΔOD450/amniocentesis to legacy.
- Skill count 51 → 53 (`know-yourself`, `mt-career-judgment`).

### Known limitations (updated)
- The eval is **one run** of a weak-model A/B + literature check + a code exemplar — *not* a powered
  clinical-outcome study, and the judge is itself an LLM. Per-skill grades carry run-to-run variance
  (documented). 23 literature nuances are captured in `literature-check.md` but **not yet folded into
  every skill body** — open work. Still a *thinking aide*, not a source of truth.

## [0.1.0] — 2026-06-03

First tagged version, so MT can cite a fixed version in documents / audit trails.

### Skills (51)
- 🩸 **Lab bench:** bloodbank · hematology · clinchem · chemistry-interpretation · clinmicro · applied-microbiology · immunoassay · molecular · pathology · parasitology · toxicology · pharmacology · clinical-correlation · infection-control
- 🔬 **Research:** critical-appraisal · r2r-research-proposal · research-design · choose-stat-test · sample-size-power · r2r-stats · manuscript
- 🧭 **Life/career:** mt-law-ethics · mt-exam-strategy · finance · financial-statement · ikigai · self-development · digital
- 💼 **Lab-mgmt / IVD:** lab-management · ivd-sales · crm · marketing · sales-psychology
- 🤖 **AI-use** · 💬 **comms** · 💻 **code/data** · 🗂️ **files**

### Safety scaffolding
- Clinical skills carry an in-body `verify-first` guard: decision-support not the final answer; pair with `anti-hallucination`; patient-affecting steps need MT/physician confirmation.
- Risk-tiered disclaimers (heavy for patient-safety skills, light for utility) — by design, documented in README.
- `STANDARDS.md` source-of-truth: ISO 15189:2022 · ISO 15190:2020 · AABB Technical Manual 21st (2023) · AABB Standards 35th (effective 1 Apr 2026). Monthly auto-recheck (ISO) flags a newer edition for human review (no silent edit).

### Known limitations
- `eval/` is a preliminary paired-prompt harness — error-reduction claims **not yet proven at scale**.
- Not yet clinical-peer-reviewed; intended as a *thinking aide*, not a source of truth.
