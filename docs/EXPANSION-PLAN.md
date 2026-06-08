# Expansion Plan — T-shaped MT (AI era)

> **Thesis (ผู้สร้าง, 2026-06-08):** ยุค AI มาแรง — MT ไม่ควรอยู่แค่หน้า bench.
> เดี๋ยวนี้ MT ทำ dashboard / automate งานซ้ำ / จัดการ data / สร้างเครื่องมือเล็กๆ
> เองได้แล้ว. คลังสกิลจึงต้องครอบ **"MT ที่ทำมากกว่า MT"** ไม่ใช่แค่งานแล็บ.
>
> หลักการ reframe: เอา judgment สาย dev/design/business/productivity มา **แต่เปลี่ยน
> audience เป็น "MT ที่ไม่ใช่โปรแกรมเมอร์"** — กับดัก #1 ของทุกตัวผูกกับ
> **ความปลอดภัยข้อมูลคนไข้ (PDPA)** + **verify ค่ากับ source** ซึ่ง dev ทั่วไปไม่เน้น
> แต่ MT ห้ามพลาด. ทุกตัวเชื่อมกลับ `digital-judgment` / `anti-hallucination`.

Source = คลังสกิลของ Claude (mt-shift-optimizer session): project-bundled 17 + user-level ~84.
ตารางนี้ map **ทุก tier ไม่ตกหล่น** → สถานะการพอร์ตเข้า repo.

สถานะ: ✅ done · 🟢 wave1 (กำลังทำ) · ⏳ planned · ⚪ ซ้ำของเดิม (ไม่ทำ) · ⛔ ไม่พอร์ต (เหตุผลระบุ)

---

## Track 1 — Lab bench (clinical, net-new ที่คลังยังขาด)
| skill ใหม่ | reframe จาก | ช่องที่เติม | สถานะ |
|---|---|---|---|
| `urinalysis-judgment` | net-new | UA + body fluid (CSF/serous/synovial) microscopy — แขนง MT bench ที่หายทั้งดุ้น | 🟢 wave1 |
| `preanalytical-judgment` | net-new | pre-analytical/phlebotomy = error #1 ของแล็บ (เดิมกระจาย 11 ไฟล์) | 🟢 wave1 |
| `poct-judgment` | net-new | Point-of-care testing (รวมเข้า ISO 15189:2022) — connectivity/QC/operator | 🟢 wave3 |
| `flow-cytometry-judgment` | net-new | gating/panel/immunophenotyping (niche, เสริม hema) | 🟢 wave3 |

## Track 2 — R2R / สถิติ
| skill ใหม่ | reframe จาก | ช่องที่เติม | สถานะ |
|---|---|---|---|
| `method-validation-stats` | `mt-stats-helper` | method comparison (Bland-Altman/Passing-Bablok), reference interval (CLSI EP28), diagnostic accuracy เชิงลึก — stats เฉพาะ MT ที่ choose-stat-test ยังตื้น | 🟢 wave3 |
| `pubmed-search` | `scientific-db-pubmed-database` | ค้น PubMed/MeSH เป็นระบบ | 🟢 wave3 |
| `source-credibility` | `scientific-thinking-scholar-evaluation` | ประเมิน journal/predatory/ผู้เขียน (เสริม critical-appraisal) | 🟢 wave3 |
| `deep-research` | `deep-research` | multi-source + cited report (งานวิจัย/สแกน IVD) | 🟢 wave3 |
| `gget-genomics` | `scientific-pkg-gget` | ดึงข้อมูล gene/variant/sequence ผ่าน gget CLI (Ensembl/BLAST/UniProt) สาย molecular/bioinformatics (niche) | 🟢 wave3 |
| — | `scientific-thinking-literature-review` | ⚪ ทับ `critical-appraisal-judgment` | ⚪ |

## Track 3 — MT++ : build / data / automate (แกน T-shaped)
| skill ใหม่ | reframe จาก | ช่องที่เติม | สถานะ |
|---|---|---|---|
| `build-a-dashboard` | `dashboard-builder` `db-judgment` | MT ทำ dashboard (TAT/QC/workload) เอง — เลือกเครื่องมือ + กับดักข้อมูล lab + PDPA | 🟢 wave1 |
| `automate-lab-tasks` | `offload-to-automation` `python-coach` | งานซ้ำ (รายงาน/คำนวณ/จัดเวร) → ให้ code/AI ทำ เมื่อไหร่คุ้ม + กันผิดเงียบ | 🟢 wave2 |
| `clean-messy-data` | `data-project-survival` `regex-vs-llm-structured-text` | ล้างข้อมูล lab/วิจัย (date ปน/หน่วยปน/missing) ก่อนวิเคราะห์ | 🟢 wave2 |
| `mt-databases` | `db-judgment` `postgres-patterns` `database-migrations` | เก็บข้อมูลใน Sheets vs Access vs SQL vs REDCap เมื่อไหร่ + กันพัง/หาย | 🟢 wave2 |
| `ship-a-small-app` | `deployment-patterns` `fastapi-patterns` `docker-patterns` | ทำเครื่องมือเล็กให้ทีมใช้ — no-code/low-code vs code, hosting, auth/PDPA | 🟢 wave2 |
| `vibe-coding-safely` | `python-coach` `python-testing` `error-handling` `safety-guard` `e2e-testing` | ให้ AI เขียนโค้ดให้ แต่ไม่พัง/ไม่รั่วข้อมูล — "รันได้≠ถูก" | 🟢 wave2 |
| `spreadsheet-judgment` | `python-patterns` (reframe) | Excel/Sheets: tidy/VLOOKUP/STDEV · กัน autoconvert · median TAT | 🟢 wave2 |
| `deploy-ml-safely` | `mle-workflow` `ml-judgment` | MT เทรนโมเดลแล้ว (เช่น smear classifier) จะเอาไปใช้จริงยังไงไม่ให้เงียบๆ พัง (data drift/monitor) | 🟢 wave3 |

## Track 4 — Design / visual
| skill ใหม่ | reframe จาก | ช่องที่เติม | สถานะ |
|---|---|---|---|
| `design-a-clear-figure` | `design-system` `frontend-design-direction` `make-interfaces-feel-better` | ทำกราฟ/โปสเตอร์/รูปวิจัยให้อ่านรู้เรื่อง (chart choice, colorblind-safe, layout) | 🟢 wave4 |
| — | `liquid-glass-design` `motion-foundations` `motion-ui` `motion-patterns` | ⛔ UI motion เฉพาะ web app — เกินขอบเขต MT (เก็บไว้ถ้าทำ landing page) | ⛔ |
| — | `photography-judgment` | ⚪ มีแล้วใน repo | ⚪ |

## Track 5 — Media / สอน-เรียน
| skill ใหม่ | reframe จาก | ช่องที่เติม | สถานะ |
|---|---|---|---|
| `learn-anything-fast` | `interactive-course` `karpathy-teach` `teach` | ใช้ AI เป็นติวเตอร์เรียน topic ใหม่ (เตรียมสอบ/ขึ้นงานใหม่) | 🟢 wave4 |
| `make-a-teaching-video` | `video-editing` `remotion-video-creation` `manim-video` `notebooklm` | ทำคลิป/explainer สอนทีม-นักเรียน MT | 🟢 wave4 |

## Track 6 — อาชีพ 2.0 / ธุรกิจ / แบรนด์
| skill ใหม่ | reframe จาก | ช่องที่เติม | สถานะ |
|---|---|---|---|
| `personal-brand` | `brand-voice` `know-yourself` | MT สร้างตัวตนวิชาชีพออนไลน์ (LinkedIn/เพจ) ในเสียงตัวเอง | 🟢 wave4 |
| `content-distribution` | `content-engine` `crosspost` `seo` | กระจายคอนเทนต์ข้ามแพลตฟอร์ม + หาให้เจอ (เสริม content-creator) | 🟢 wave4 |
| `market-opportunity` | `market-research` `lead-intelligence` `product-lens` `product-capability` | ประเมินช่องว่างตลาด/ลูกค้า ก่อน MT ทำธุรกิจ/แอป/แล็บ | 🟢 wave4 |
| — | `dx-company-brief` `dxco` | ⚪ ทับ `ivd-sales-judgment` | ⚪ |

## Track 7 — Productivity / self-management
| skill ใหม่ | reframe จาก | ช่องที่เติม | สถานะ |
|---|---|---|---|
| `focus-and-time` | `pomodoro` `time-blocking` | บริหารเวลา/โฟกัส สำหรับ MT เวรหมุน + เรียน/ทำโปรเจกต์ข้างงาน | 🟢 wave4 |
| `manage-up` | `management-talk` | คุยกับหัวหน้า/ขอทรัพยากร/รายงานปัญหาให้ได้ผล | 🟢 wave4 |

## Track 8 — ทำงานกับ AI ให้คม
| skill ใหม่ | reframe จาก | ช่องที่เติม | สถานะ |
|---|---|---|---|
| `plan-with-ai` | `plan-orchestrate` `grill-me` `grill-with-docs` | ใช้ AI วางแผนโปรเจกต์/วิจัยทีละ step + ตกผลึกก่อนเริ่ม | 🟢 wave4 |
| `prompt-craft` | `prompt-optimizer` | เขียน prompt ให้ได้ผล (generic, ทุกสาย) | 🟢 wave4 |
| — | `strategic-compact` `token-budget-advisor` `handoff` `overnight` `pre-flight` `ultracode` `ultrareview` `plan-orchestrate`(adv) `karpathy-guidelines` | ⛔ meta สำหรับ "ผู้สร้าง repo/agent" ไม่ใช่ผู้ใช้ MT | ⛔ |

## Track 9 — Contributor / maintainer (process ของ repo เอง, ไม่ใช่ skill ผู้ใช้)
| รับมาทำ | reframe จาก | ใช้กับ | สถานะ |
|---|---|---|---|
| ยกเครื่อง `CONTRIBUTING.md` | `write-a-skill` | มาตรฐานเขียน skill ใหม่ให้ contributor | ⏳ |
| `docs/how-we-audit.md` | `scrutinize` `verification-panel` `production-audit` `agent-architecture-audit` | กระบวนการ QA clinical accuracy ก่อน merge | ⏳ |
| `docs/how-we-eval.md` | `eval-harness` `ab-test-judgment`(มีแล้ว) | ทำ eval/ ให้เป็นระบบ + เก็บ 2 ตัวที่ยัง A/B ไม่ครบ | ⏳ |
| `docs/how-we-maintain.md` | `skill-stocktake` `rules-distill` `post-mortem` `continuous-learning-v2` | ออดิตคลังเป็นรอบ + กลั่น cross-cutting rules | ⏳ |
| (skill ผู้ใช้) `phi-data-handling` | `healthcare-phi-compliance` | จัดการข้อมูลคนไข้/PDPA ในงาน MT (ก้ำกึ่ง user skill — เข้าคู่ digital-judgment) | ⏳ |
| `humanizer` | `humanizer` | ขัดภาษาไทยใน skill ให้อ่านเป็นมนุษย์ (process) | ⏳ |
| `article-writing` | `article-writing` | เขียน README/docs/บทความโปรโมต (process) | ⏳ |

## ⚪ ซ้ำของเดิม (พอร์ตไปแล้ว — ไม่ทำซ้ำ)
clinical: bloodbank · hematology · clinchem · clinmicro · immunoassay · molecular · pathology · parasitology · toxicology · clinical-correlation
อื่นๆ: cv · db · ml · optimization · crm · content-creator · digital · finance · python-coach · ds-workflow(=data-project-survival)

## ⛔ ไม่พอร์ต (เหตุผล)
- Pure software/infra สำหรับสร้าง *แอป* Shift/Connect (ไม่ใช่ความรู้ MT): `fastapi-patterns` `postgres-patterns`(แกน) `docker-patterns` `e2e-testing`(แกน) `hospital-intel-pipeline` `vite-patterns` `frontend-patterns` `tdd` `pocock-typescript` `diagnose` `debug-mantra` — *แต่ judgment บางส่วนถูกดูดเข้า Track 3 ในมุม non-coder แล้ว*
- Orchestration meta สำหรับ builder: ดู Track 8 ⛔
- `scientific-db-uspto-database` (patents — ไม่ตรง audience)

---

### Build waves
- ✅ **Wave 1:** urinalysis · preanalytical · build-a-dashboard + manifest นี้
- ✅ **Wave 2:** automate-lab-tasks · clean-messy-data · vibe-coding-safely · ship-a-small-app · spreadsheet-judgment · mt-databases — แกน T-shaped 
- ✅ **Wave 3:** method-validation-stats · pubmed-search · source-credibility · deep-research · gget-genomics · poct-judgment · flow-cytometry-judgment · deploy-ml-safely
- ✅ **Wave 4:** design-a-clear-figure · learn-anything-fast · make-a-teaching-video · personal-brand · content-distribution · market-opportunity · focus-and-time · manage-up · plan-with-ai · prompt-craft
- **Wave 3:** Track 2 (stats/research) + Track 1 ที่เหลือ
- **Wave 4:** Track 4–8 (design/media/career/productivity/AI)
- **Wave 5:** Track 9 (contributor/maintainer process docs)

หลัง merge แต่ละ wave: รัน `python scripts/build_triage.py` (regenerate INDEX/dist/triage) + อัปเดต count ใน README + เพิ่ม eval ของตัวใหม่.

---

## Completeness ledger — ขุดหมดแล้ว (97/97)
แหล่ง source skill ทั้งหมดของ Claude (session mt-shift-optimizer) = **80 user-level + 17 project = 97**.
ทุกตัวถูกจัดลงตารางด้านบน 1 ใน 5 สถานะ (✅/🟢/⏳/⚪/⛔) — verify ได้ด้วยการ grep ชื่อ slug ในไฟล์นี้.

- **ไม่นับ** (อยู่นอก "skill ที่ผู้สร้างเขียนเอง"): plugin skills ของบุคคลที่สาม (cockroachdb / astronomer / aws / atlassian / canva / notion ฯลฯ) + built-in slash commands ของ Claude Code (`/code-review` `/commit` `/run` `/verify` `/teach` `/dxco` `/loop` `/schedule` `/claude-api` ฯลฯ) — เป็นเครื่องมือ/ปลั๊กอิน ไม่ใช่เนื้อหา judgment ของ MT จึงไม่พอร์ต.
