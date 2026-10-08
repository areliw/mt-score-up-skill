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

## การติดตั้ง
`sync_mt_skills.py` (v3) คัดลอก `skills/<name>/` ทั้งโฟลเดอร์ไปที่ `~/.claude/skills/<name>/` ให้ skill ที่ sync ดูแล · validator ของ repo อ่านแค่ `skills/*.md` จึงไม่กระทบ
