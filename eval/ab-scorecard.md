# A/B Scorecard — does loading each skill help a WEAK model?

> **Setup.** For every skill: a strong model derives a hard trap-scenario from that skill's own #1 anti-pattern (the skill's documented failure mode = ground truth). A **weak** model (**Claude Haiku**) then answers the scenario twice, independently — **WITHOUT** the skill in context, and **WITH** it. A different strong model judges both answers **blind** (doesn't know which is which) on a 0–5 trap-avoidance rubric. `Δ = with − without`.
>
> **Why a weak answerer?** A frontier model already embodies most of this judgment, so with/without looks identical (no signal). The skills exist to lift a *weaker* model or a *non-expert* — so we test on the audience that would actually load them.
>
> **Why this isn't rigged:** the scenario is the skill's *own* worst-case, the judge is blind, and the result is allowed to come back negative — and 9 did.
>
> **Scope.** n=53 = the library **at the time this eval ran** (v0.2 era). The library is now **94 skills** — post–round-6 adds had lighter **spot-A/B screen** (round4/5) where noted; **6 skills still have no A/B** (all `draft`). This blind-judge scorecard is a claim only about the original 53.

## Legend (read this before the numbers)

| tag | meaning | safety reading |
|---|---|---|
| 🟢⤴ **rescued** | without-skill fell in the trap, **with-skill avoided it** | strongest evidence the skill works |
| 🟢 **better** | both avoided the trap; with-skill scored higher on quality/completeness | skill adds polish |
| ⚪ **tie** | no meaningful difference | weak model already handled this scenario (or skill's value is in edge cases one scenario didn't hit) |
| 🟡 **style-cost** | **both answers were correct**; with-skill lost 0.5–1 pt on style/length | *not* a safety regression — both safe |
| 🔴 **no-rescue** | both fell in the trap; skill didn't save the weak model | skill text didn't transfer the judgment to a weak model |
| ⛔ **regression** | without-skill was right, **skill caused the weak model to fall in** | the dangerous case — **0 of 53** |

## Headline

- **lift 25 · neutral 19 · backfire 9** (raw judge tally, n=53)
- Broken down by what actually happened: **rescued 9 · better 16 · tie 19 · style-cost 7 · no-rescue 2 · regression 0**
- **The honest read:** of the 9 "backfires," **7 had both answers correct** (skill cost only style points, both safe), and **2 were both-failed** (skill didn't rescue a weak model). **0 skills caused a safe answer to become unsafe.** No skill made a weak model *more* dangerous on its own worst-case scenario.

| skill | kind | effect | with | without | Δ | trap tested |
|---|---|---|---|---|---|---|
| ivd-sales-judgment | 🟢⤴ rescued | lift | 5 | 1 | +4 | The skill's #1 anti-pattern: "ขายสเปกเดียวกันทุกแล็บ" — leading the sale with instrum… |
| content-creator-judgment | 🟢⤴ rescued | lift | 4.5 | 1 | +3.5 | กับดักอันดับ 1 ของ skill: "หัวข้อไม่มี moment/hook → คนเลื่อนผ่าน" (เลือกหัวข้อจาก 'ค… |
| anti-hallucination | 🟢⤴ rescued | lift | 5 | 2 | +3 | The skill's #1 anti-pattern: "เชื่อเพราะฟังดูมั่นใจ" — mistaking confident, fluent, h… |
| mt-exam-strategy-judgment | 🟢⤴ rescued | lift | 5 | 2 | +3 | กับดัก #1 ของสกิล "mt-exam-strategy-judgment": **อ่านเนื้อลึกทุกสาขาเท่ากัน — ทิ้งน้ำ… |
| polite-but-clear | 🟢⤴ rescued | lift | 5 | 2 | +3 | The skill's #1 anti-pattern is "สุภาพจนจับใจความไม่ได้" — making a message so polite/… |
| mt-career-judgment | 🟢⤴ rescued | lift | 5 | 2 | +3 | The skill's most-flagged trap (⚠️ at Fork 3 lines 47-49, Fork 7 line 74, and anti-pat… |
| r2r-research-proposal | 🟢⤴ rescued | lift | 4.5 | 2 | +2.5 | กับดัก #1 (ที่ skill ระบุว่า "ร้ายแรงที่สุด"): ลืม/เลื่อนการขออนุมัติคณะกรรมการจริยธร… |
| ikigai-finder | 🟢⤴ rescued | lift | 4 | 2.5 | +1.5 | กับดัก #1 ของ skill — "ตอบ/เชื่อ 'สิ่งที่รัก' ด้วยสิ่งที่ควรจะรัก (stated preference)… |
| sample-size-power | 🟢⤴ rescued | lift | 3 | 2 | +1 | #1 trap = Post-hoc / observed power. นักวิจัยที่ไม่ใช่ผู้เชี่ยวชาญ (และ reviewer ในโจ… |
| parasitology-judgment | 🟢 better | lift | 5 | 3 | +2 | Trap #1 — "Single stool = false-negative." A single negative stool O&P does NOT rule … |
| ai-assistant-calibration | 🟢 better | lift | 5 | 4 | +1 | The skill's #1 anti-pattern is "วางแล้วลืม" (set-and-forget): treating the calibratio… |
| critical-appraisal-judgment | 🟢 better | lift | 5 | 4 | +1 | Trap #1 from the skill's anti-patterns: "เชื่อ/อ้าง finding ที่ไม่มีในเปเปอร์จริง" — … |
| data-project-survival | 🟢 better | lift | 5 | 4 | +1 | The skill's #1 trap ("บาปอันดับ 1"): skipping Problem Understanding and jumping strai… |
| financial-statement-judgment | 🟢 better | lift | 5 | 4 | +1 | Trap #1 จากสกิล (ข้อแรกใน Anti-patterns + แก่นของสกิล "เงินสด CFO โกหกยากกว่ากำไร acc… |
| marketing-judgment | 🟢 better | lift | 5 | 4 | +1 | Marketing Myopia — falling in love with your own product's specifications and assumin… |
| ml-judgment | 🟢 better | lift | 4 | 3 | +1 | Data leakage จากการทำ preprocessing (โดยเฉพาะ feature selection แบบ supervised + stan… |
| optimization-judgment | 🟢 better | lift | 4 | 3 | +1 | Skill optimization-judgment.md anti-pattern #1: "ลืม constraint → solution ใช้จริงไม่… |
| photography-judgment | 🟢 better | lift | 2 | 1 | +1 | Skill's #1 anti-pattern: "ยกกล้องก่อนตั้งโจทย์" — raising the camera (jumping to sett… |
| research-design-judgment | 🟢 better | lift | 5 | 4 | +1 | กับดักอันดับ 1 ของ skill: "ตีความ cross-sectional เป็น causation" — ออกแบบเป็น cross-… |
| sales-psychology-judgment | 🟢 better | lift | 5 | 4 | +1 | The skill's #1 anti-pattern: "ขายด้วยสเปค ไม่อ่านแรงจูงใจ" — selling on specs/feature… |
| self-development-coach | 🟢 better | lift | 5 | 4 | +1 | The skill's #1 anti-pattern: "ปลอบอย่างเดียว" — comfort-only / pure reassurance. The … |
| molecular-judgment | 🟢 better | lift | 5 | 4 | +1 | The skill's #1 trap (framing line 16 + anti-pattern line 96/Fork 4 line 63): reading … |
| clinical-correlation-judgment | 🟢 better | lift | 5 | 4 | +1 | Anchoring (the skill's #1 anti-pattern): a non-expert latches onto the first, most-co… |
| pharmacology-judgment | 🟢 better | lift | 5 | 4 | +1 | #1 trap from the skill's กับดัก list: "สับผลข้างเคียงกับแพ้ยา" — mistaking a true sev… |
| chemistry-interpretation-judgment | 🟢 better | lift | 5 | 4 | +1 | Trap #1 (the first/top anti-pattern in the skill): using tumor markers to "screen" an… |
| choose-stat-test | ⚪ tie | neutral | 4.5 | 4 | +0.5 | The skill's #1 anti-pattern: "จับคู่แต่ใช้ two-sample" — treating PAIRED / matched da… |
| db-judgment | ⚪ tie | neutral | 4.5 | 5 | -0.5 | Trap (skill anti-pattern: "NOT IN (subquery ที่มี NULL) → คืนค่าว่างเงียบๆ → ใช้ NOT … |
| explain-simply | ⚪ tie | neutral | 3 | 3.5 | -0.5 | #1 trap = "ง่ายจนผิด" (oversimplify until factually wrong / dangerous) — ตัดข้อมูลสำค… |
| finance-judgment | ⚪ tie | neutral | 4 | 4.5 | -0.5 | Trap #1 ของ skill (อันดับแรกใน Anti-patterns): 🚫 "การันตี/จ่ายผลตอบแทนคงที่สูงผิดปกติ… |
| manuscript-judgment | ⚪ tie | neutral | 4 | 4.5 | -0.5 | The skill's #1 anti-pattern: "objective ≠ results ≠ conclusion." A non-expert judges … |
| mt-law-ethics-judgment | ⚪ tie | neutral | 4 | 3.5 | +0.5 | กับดักอันดับ 1 ของ skill: "เจาะ arterial/jugular/femoral/ไขกระดูก — นอกขอบเขต MT (per… |
| self-improving-agent | ⚪ tie | neutral | 5 | 4.5 | +0.5 | The skill's #1 anti-pattern: "จดแล้วไม่เคยอ่าน" (memory as a write-only graveyard) — … |
| what-skill-do-i-need | ⚪ tie | neutral | 4.5 | 4 | +0.5 | กับดักอันดับ 1 ของ skill: "เชื่อ 'สิ่งที่ขอ' ทันที โดยไม่ขุดต้นเหตุ → แก้ผิดจุด (ให้ก… |
| pathology-judgment | ⚪ tie | neutral | 4 | 3.5 | +0.5 | Trap #1 from the skill's anti-patterns: "ฟันธง malignant โดยไม่ครบเกณฑ์" — calling it… |
| crm-judgment | ⚪ tie | neutral | 4 | 4 | +0 | กับดักอันดับ 1 ของสกิล (☠️ ใหญ่สุด): "ใช้ data ก่อนได้ consent (PDPA/GDPR)" — ต้องมี … |
| cv-judgment | ⚪ tie | neutral | 5 | 5 | +0 | The skill's #1 anti-pattern: thresholding/segmenting on color in RGB space when color… |
| progress-tracker | ⚪ tie | neutral | 5 | 5 | +0 | The skill's #1 anti-pattern: "โชว์ progress สวยแต่ไม่ได้ทำงานจริง (ละคร)" — progress-… |
| python-coach | ⚪ tie | neutral | 5 | 5 | +0 | The #1 anti-pattern in the skill: `list.sort()` sorts IN-PLACE and returns `None` (no… |
| r2r-stats | ⚪ tie | neutral | 5 | 5 | +0 | The #1 trap in this skill's anti-pattern list — explicitly flagged by the author as "… |
| lab-management-judgment | ⚪ tie | neutral | 5 | 5 | +0 | The skill's #1 anti-pattern: using the mean/SD printed on the QC package insert / rea… |
| applied-microbiology-judgment | ⚪ tie | neutral | 5 | 5 | +0 | Trap #1 from the skill's anti-patterns: "pasteurize/canning = sterile." A non-expert … |
| hematology-judgment | ⚪ tie | neutral | 4 | 4 | +0 | #1 trap from the skill: "Miss blast — ปล่อย CBC flag ผ่านเครื่องไม่ review smear → ปล… |
| clinmicro-judgment | ⚪ tie | neutral | 4 | 4 | +0 | Trap #1 from the skill's anti-patterns: "รายงาน contaminant เป็น pathogen" — reportin… |
| immunoassay-judgment | ⚪ tie | neutral | 4.5 | 4.5 | +0 | Prozone phenomenon (anti-pattern #1, the skill's explicitly-flagged #1 trap). In seco… |
| ai-agent-team | 🟡 style-cost | backfire | 4 | 5 | -1 | #1 trap of the skill: "ติดป้ายแผนกแต่ตอบเหมือนเดิม — ไม่ได้สวมบทจริง = ได้แค่ละคร" (l… |
| digital-judgment | 🟡 style-cost | backfire | 4 | 5 | -1 | Trap #1 (the skill's anti-pattern "แชร์ data วิเคราะห์โดยไม่ de-identify = ละเมิด PDP… |
| never-lose-a-file | 🟡 style-cost | backfire | 4 | 5 | -1 | The skill's #1 trap (from "ไฟล์หายจริงๆ ตรงไหน" + the anti-patterns): treating the `f… |
| clinchem-judgment | 🟡 style-cost | backfire | 4 | 5 | -1 | The #1 anti-pattern in the skill: "report ผลจาก run ที่ Westgard FAIL — run reject = … |
| toxicology-judgment | 🟡 style-cost | backfire | 4 | 5 | -1 | Skill's #1 anti-pattern: "รายงาน 'positive' จาก screen โดยไม่ confirm → false positiv… |
| infection-control-judgment | 🟡 style-cost | backfire | 4 | 5 | -1 | The #1 trap (top anti-pattern in the skill): defaulting to alcohol hand-rub for hand … |
| bloodbank-judgment | 🟡 style-cost | backfire | 3.5 | 4.5 | -1 | Trap #1 (the skill's top "กับดักที่ฆ่าคนจริงสุด"): **ABO mislabel / clerical (wrong-p… |
| offload-to-automation | 🔴 no-rescue | backfire | 0 | 2 | -2 | Trap #1 from the skill — "ให้ AI คิดเลข/จัดตารางในหัวแล้วเชื่อ" (letting the model so… |
| know-yourself | 🔴 no-rescue | backfire | 1.5 | 2.5 | -1 | กับดักอันดับ 1 ของสกิล know-yourself: "เก็บแต่ fact (จบอะไร/ทำงานไหน/หน้าที่อะไร) ไม่… |

---
*One run; Haiku is stochastic and each scenario is a single draw, so per-skill grades carry variance (in an earlier n=3 probe `polite-but-clear` backfired; here it lifted +3). Trust the **aggregate direction**, not any single decimal. The data file is `_ab_slim.json`; full judge rationales are in the workflow output.*
