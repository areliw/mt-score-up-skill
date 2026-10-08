# Skill Architecture v2 — judgment + craft + tools + proof

> v1 ของคลังนี้ = **judgment-only** (decision forks + traps). ยังถูกอยู่: judgment ดีกว่า knowledge dump.
> v2 เติม 3 ชั้นที่ skill ที่คนใช้มากที่สุดในโลกมี แต่ของเราไม่มี — **โดยไม่ลบ judgment เดิมแม้แต่บรรทัดเดียว**

## ทำไม (benchmark 2026-10-08)

เทียบกับ skill ที่ชนะจริงในสนาม (ยอดติดตั้งจาก skills.sh และดาว GitHub ณ 2026-10-08):

| skill | ยอดใช้ | SKILL.md | ไฟล์ประกอบ |
|---|---|---|---|
| mattpocock `grill-me` | 1.31M installs | 7 บรรทัด (alias ไป skill อื่น) | — |
| mattpocock `tdd` | 1.04M | 38 บรรทัด | 3 ไฟล์ (tests.md, mocking.md, agent) |
| anthropics `frontend-design` | 962K | 71 | — |
| vercel `react-best-practices` | 779K | 149 | 72 ไฟล์กฎ เรียงตามผลกระทบ CRITICAL→LOW |
| vercel `agent-browser` | 1.06M | 52 (stub ชี้ไป CLI ที่ตรงเวอร์ชัน) | CLI ทั้งตัว |
| heygen `hyperframes` | 826K | 154 | 25 references + 3 scripts + CLI |
| anthropics `skill-creator` | (repo 180K★) | 485 | 9 scripts + eval viewer: with-skill vs baseline, blind compare |
| anthropics `docx` / `mcp-builder` / `webapp-testing` | (repo 180K★) | 95–236 | 59 / 4 / 1 scripts; mcp-builder มีเฟส "Create Evaluations" |
| obra `test-driven-development` / `writing-skills` | (repo 296K★) | 330 / 681 | Iron Law · Rationalizations · Red Flags · TDD สำหรับ skill |
| Google `clasp` plugin (สนามเดียวกับงาน GAS) | — | — | ส่ง MCP server ให้ agent เรียกใช้ ไม่ใช่ข้อความ |

ข้อสรุปที่ผู้ชนะทำ แต่ v1 ของเราไม่ทำ:
1. **เครื่องมือ (scripts/CLI/MCP) อยู่ในโฟลเดอร์ skill** — ส่วนที่คำนวณ/ตรวจได้ ให้เครื่องทำ ไม่ให้โมเดลคิดเลขเอง. v1: 0 script ใน 65 judgment skills; สคริปต์ที่ใช้ทวนเลขของ `decision-tree-judgment` อยู่ใน temp แล้ว**หายไป** → ตัวเลข `[คำนวณ]` ทำซ้ำไม่ได้
2. **Proof อยู่กับ skill** — eval cases + baseline compare รันซ้ำได้ (skill-creator, mcp-builder). v1: ผล A/B อยู่ใน `eval/` แยก ไม่มี case ให้รันซ้ำในโฟลเดอร์ skill
3. **Craft สำหรับงานที่ผลลัพธ์เป็นชิ้นงาน** — ขั้นตอนพร้อมด่าน, template, ตัวอย่างที่ทำเสร็จ (frontend-design: plan → review against brief → build → critique)
4. **SKILL.md บาง โหลดส่วนลึกเมื่อจำเป็น** (progressive disclosure)

สิ่งที่ v1 ของเราทำดีกว่าผู้ชนะส่วนใหญ่ (ห้ามทิ้ง): provenance ทุกเลข (`[คำนวณ]` `[ทั่วไป]` หน้าสไลด์), แคตตาล็อกเลขผิดในแหล่งต้นทาง, disclaimer ความปลอดภัยผู้ป่วย, gate ×3 A/B

## 5 ชั้น

| ชั้น | อยู่ที่ | บังคับเมื่อ |
|---|---|---|
| **L0 Entry** — ใช้เมื่อ/ไม่ใช้เมื่อ, VERDICT, กับดัก #1, แผนที่ไปชั้นอื่น | `skills/<name>.md` ส่วนบน | ทุก skill |
| **L1 Judgment** — forks, traps เรียงตามผลกระทบ, red flags | `skills/<name>.md` (ของเดิม) | ทุก skill |
| **L2 Craft** — ขั้นตอนพร้อมด่าน, template คำตอบ/รายงาน, ตัวอย่างทำเสร็จ, นิยาม "เสร็จ" | `skills/<name>.md` § หรือ `skills/<name>/references/` | ผลลัพธ์เป็น**ชิ้นงาน** (รายงาน, แบบฟอร์ม, คำตอบข้อสอบ, เอกสาร, แอป) |
| **L3 Tools** — สคริปต์ที่ทำส่วนที่คำนวณ/ตรวจกฎได้ | `skills/<name>/scripts/` | มีขั้นใดที่**คำนวณหรือตรวจกฎได้แน่นอน** |
| **L4 Proof** — oracle tests + must-fail control + ผล A/B | `skills/<name>/evals/` | มี L3 หรือเปลี่ยนพฤติกรรม |

**กฎทรงตาม output:** ผลลัพธ์ = คำตัดสิน → L0+L1 (+L3 ถ้ามีส่วนคำนวณ) · ผลลัพธ์ = ชิ้นงาน → ครบทุกชั้น

## กฎของ L3 Tools
- Python 3 **stdlib เท่านั้น** (เครื่องไหนก็รันได้) · 1 สคริปต์ = 1 งาน · `--help` ใช้ได้เสมอ · มี `--json`
- **ต้องรันบน Windows ภาษาไทย (cp874) ได้:** ใส่ guard `# cp874-safe-stdout` ที่ reconfigure stdout/stderr เป็น UTF-8 หลัง import (แพตช์อัตโนมัติ: `~/.claude/skills_sync/patch_utf8_stdout.py` · ตรวจ: `--check`) — 2026-10-08 พบ 21/53 สคริปต์พังที่ `--help` เพราะ § Σ ≥
- skill สั่งให้ **รัน black-box ก่อนคิดเลขเอง** ไม่ต้องอ่านซอร์ส (แบบ anthropics `webapp-testing`)
- พิมพ์ **ตารางที่ตรวจทานได้** (ค่าเข้า, สูตรที่ใช้, ผลกลาง, check รวม) ไม่ใช่แค่คำตอบสุดท้าย
- เครื่องมือ = **ตัวช่วยตรวจ ไม่ใช่ผู้ตัดสิน**: ทุก output ที่กระทบผู้ป่วยต้องพิมพ์บรรทัด `ADVISORY: ยืนยันกับ SOP/ผู้มีอำนาจลงนามของแล็บ`
- cutoff ที่ขึ้นกับแล็บ (critical value, reference range, TEa ที่เลือกใช้) = **รับเป็น argument** ห้าม hardcode เป็นความจริง · ค่าตัวอย่างใน `data/` ติดป้ายว่าเป็นค่าสอน
- ห้ามคัดลอกตารางที่มีลิขสิทธิ์ (เช่น CLSI M100 breakpoints) ลงสคริปต์ → รับจากผู้ใช้
- ห้ามมีข้อมูลผู้ป่วยจริงใน `data/` หรือ `evals/`

## กฎของ L4 Proof
- `evals/test_<tool>.py` (pytest) — **ค่าคาดหวังต้องมาจากแหล่งอื่นที่ไม่ใช่โค้ดนี้**: ตัวอย่างในสไลด์/digest/ตำรา (อ้างหน้า), เฉลยการบ้าน, ตัวอย่างในมาตรฐาน · คำนวณด้วยมือในคอมเมนต์ได้ถ้าไม่มีแหล่ง
- **must-fail control อย่างน้อย 1 ตัว**: จำลองกับดักที่ skill เตือน (เช่น เฉลี่ยไม่ถ่วงน้ำหนัก, R4s ข้าม run) แล้ว test ต้องแดง — ถ้าไม่แดง test พิสูจน์อะไรไม่ได้
- ผล A/B (ถ้ามี) เขียนที่ `evals/RESULT.md`: วันที่, โมเดล, arm, n, metric, Δ

## กฎแก้การ์ด (L0/L1/L2 ใน `skills/<name>.md`)
- **เพิ่มเท่านั้น** — forks/traps/ตัวเลขเดิมคงไว้ทั้งหมด (diff ต้องเป็นบรรทัด `+` เกือบทั้งหมด; ถ้าแก้บรรทัดเดิมต้องมีเหตุผลใน commit)
- เพิ่ม `## เครื่องมือ (รันก่อนคิดเลข)` ใต้กล่อง VERDICT: คำสั่งตัวอย่าง 1–3 บรรทัด + บอกว่าอ่าน output ตรงไหน
- เพิ่ม `## ผลงานที่ต้องส่ง` เมื่อ output เป็นชิ้นงาน: template + นิยามเสร็จ
- path ในการ์ดเขียนแบบ `scripts/<tool>.py` (สัมพัทธ์กับโฟลเดอร์ skill ที่ติดตั้งแล้ว; ใน repo อยู่ที่ `skills/<name>/scripts/`)
- อัปเดต `last_edited`

## บันไดเวอร์ชัน — skill ต้องไต่ต่อเรื่อยๆ ไม่อยู่เฉย (owner 2026-10-08)

> "ยิ่งโลกพัฒนา เราก็ต้องยิ่งอัปตัวเอง" — เลขเวอร์ชันได้มาจาก**การผ่านด่าน** ไม่ใช่จากการแก้ไฟล์
> ทุกขั้นตรวจด้วยเครื่องได้ (`~/.claude/skills_sync/skill_gates.py`) · เวอร์ชันที่แสดง = ขั้นสูงสุดที่ผ่าน**ต่อเนื่อง**จาก v1

| ขั้น | เพิ่มอะไร | ด่าน (เครื่องตรวจ) |
|---|---|---|
| **v1** | judgment: forks + traps | มี description บอกว่าใช้เมื่อไร + มี fork และ trap |
| **v2** | tools + proof หรือ craft | gate G2–G4 ที่เข้าเงื่อนไขผ่านครบ · `evals/test_*.py` เขียว + มี must-fail control |
| **v3** | **พิสูจน์ว่าดีกว่าเวอร์ชันก่อน** | `evals/RESULT.md` มี A/B เทียบเวอร์ชันก่อน Δ ≥ 2·SE (floor 0.8) หรือ owner verdict (สาย Track B) |
| **v4** | trigger แม่น | router/description probe: เคสที่ต้องยิงยิงครบ + false positive 0 บนคลัง prompt จริง (`router_regress.py probe`) บันทึกใน `evals/TRIGGERS.md` |
| **v5** | เรียนจากคำติ | `evals/LESSONS.jsonl` append-only (คำติ owner + วันที่ + ที่มา) · ทุกบทเรียนที่ live ถูกอ้างใน skill (coverage check) |
| **v6** | ไม่ล้าสมัย | ทุกแหล่งใน `evals/VERSION.json → sources` มี `last_verified` ≤ 90 วัน และแหล่งที่เป็นไฟล์ไม่ได้ถูกแก้หลังวันนั้น |
| **v7** | เทียบโลก | `evals/BENCHMARK.md` เทียบผู้ชนะในสนามเดียวกัน ≥ 8 ชิ้นพร้อมตัวเลข (skill `benchmark-the-best`) ≤ 180 วัน |
| **v8** | ต่อกับ skill อื่นได้จริง | ทุก skill ที่อ้างถึงด้วย `ชื่อ` มีอยู่จริง (contract check) + ไม่มีกฎขัดกับ skill คู่ |
| **v9** | วัดผลการใช้จริง | `VERSION.json → telemetry`: จำนวนครั้งที่ถูกเรียก, อัตราผ่าน eval, คำติที่เข้า — ทบทวนล่าสุด ≤ 30 วัน |

### Trigger — อะไรเกิดขึ้นแล้วต้องเริ่มอัป (เครื่องคำนวณให้ทุกครั้งที่รัน audit)
| ลำดับ | trigger | เงื่อนไข | ทำอะไร |
|---|---|---|---|
| 1 | **FAIL** | eval เดิมแดง หรือมีคำติ owner ค้างใน `LESSONS.jsonl` | แก้ทันที (พลาดเรื่องเดิม 2+ = แก้ที่ราก) |
| 2 | **GAP** | ขาด gate ของขั้นปัจจุบัน/ขั้นถัดไป | อัปตอนถูกเรียกใช้ครั้งถัดไป (hook เตือน) |
| 3 | **HOT** | ถูก route ≥ 20 ครั้งตั้งแต่ promote ล่าสุด | ไต่ขั้นถัดไป — ใช้บ่อย = คุ้มที่สุด |
| 4 | **STALE** | แหล่งเกิน 90 วัน หรือไฟล์แหล่ง (digest/สไลด์) ถูกแก้หลัง `last_edited` | ทวนแหล่ง + อัปเนื้อ |
| 5 | **WORLD** | มาตรฐานออก edition ใหม่ / เครื่องมือออกเวอร์ชันหลัก / ผู้ชนะในสนามเปลี่ยน | re-benchmark (รอบสแกนรายสัปดาห์) |
| 6 | **IDLE** | ไม่มี promotion 30 วัน ทั้งที่ยังถูกใช้ | ลองขั้นถัดไป — **ห้ามอยู่เฉย** |

### ประตู promote (vN → vN+1) — ไม่ผ่าน = ไม่ได้เลข แต่บันทึกความพยายามไว้
1. test เดิมเขียวทั้งหมด + ด่านของขั้นใหม่ผ่าน
2. judgment เดิมไม่หาย (diff ลบบรรทัด fork/trap = 0 เว้นแต่ owner สั่ง)
3. objective: A/B เทียบ vN บน eval ของ skill เอง Δ ≥ 2·SE · taste: owner verdict append-only
4. clinical/เงิน/ความปลอดภัย: คนยืนยันก่อน promote แม้ A/B ผ่าน
5. เขียน `evals/VERSION.json → history`: `{v, date, trigger, evidence, gate}`

## การติดตั้ง
`sync_mt_skills.py` (v3) คัดลอก `skills/<name>/` ทั้งโฟลเดอร์ไปที่ `~/.claude/skills/<name>/` ให้ skill ที่ sync ดูแล · validator ของ repo อ่านแค่ `skills/*.md` จึงไม่กระทบ
