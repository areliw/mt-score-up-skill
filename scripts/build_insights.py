#!/usr/bin/env python3
"""
The L3 (synthesis) engine — auto-build meta-insight artifacts from the A/B scoreboard.

Reads eval/_ab_slim.json (the canonical A/B record) + skills/ and regenerates:
  1) eval/insights-data.json   structured computed insights (machine-readable, the canonical output)
  2) eval/INSIGHTS.md          human digest (the "what does all the data say" report)
  3) eval/leaderboard.html     self-contained interactive judgment-gap leaderboard (GitHub-Pages-ready)

WHY this exists: collecting/adjusting skills (L1) is linear; *proving* which judgment
changes a decision (L2, the A/B records) is the moat; **synthesising that into insight
that regenerates itself from the data (L3)** is what turns one-off analysis into a
repeatable product. Change the data -> run this -> fresh insight. No hand-typing.

Deterministic (no judgment, no dates embedded) -> safe to run in CI / auto-commit,
exactly like build_triage.py. stdlib only.

Usage:  python scripts/build_insights.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
SLIM = ROOT / "eval" / "_ab_slim.json"
DATA_OUT = ROOT / "eval" / "insights-data.json"
MD_OUT = ROOT / "eval" / "INSIGHTS.md"
HTML_OUT = ROOT / "eval" / "leaderboard.html"

# category keyword map (first match wins) — keep in sync with the repo's domains
CATS = [
    ("clinical", ["hema", "clinmicro", "clinchem", "chemistry", "immuno", "bloodbank", "blood-donor",
                  "urinalysis", "parasit", "histo", "flow", "molecular", "toxicolog", "pharmac", "patho",
                  "clinical-corr", "preanalytic", "poct", "result-release", "receiving", "infection",
                  "method-validation", "applied-micro"]),
    ("career", ["career", "exit", "ikigai", "know-yourself", "self-dev", "mt-law", "mt-exam",
                "professional-voice", "self-improving"]),
    ("AImeta", ["anti-halluc", "ai-", "prompt", "verification", "what-skill", "write-a-skill", "digital",
                "explain", "humaniz", "offload", "source-cred", "deep-research"]),
    ("comms", ["polite", "report-up", "interprofess", "incident", "grill", "management"]),
    ("research", ["r2r", "stats", "research-design", "literature", "critical-appraisal", "pubmed",
                  "choose-stat", "sample-size", "manuscript", "ml-", "data-", "cv-", "optim"]),
    ("business", ["ivd-sales", "sales", "marketing", "crm", "lead-intel", "market-research", "finance",
                  "financial", "dx-company", "content-creator", "lab-clinic-bus"]),
    ("tools", ["python", "spreadsheet", "db-", "git-work", "tdd", "debug", "never-lose", "progress",
               "token", "time-block", "pomodoro", "photo", "interactive", "mt-databases"]),
]

# the "human-judgment" clusters whose value AI cannot replicate (vs clinical textbook)
JUDGMENT_CLUSTER = {"career", "business", "comms", "AImeta"}

# Thai labels for readability on the leaderboard (slug -> short gloss)
LABELS = {
    "ivd-sales-judgment": "ขายน้ำยา/IVD", "content-creator-judgment": "ทำคอนเทนต์/แคสเกม",
    "mt-career-judgment": "เส้นทางอาชีพ MT", "anti-hallucination": "กัน AI มั่ว",
    "mt-exam-strategy-judgment": "กลยุทธ์สอบใบประกอบ", "polite-but-clear": "พูดสุภาพแต่ชัด",
    "report-up-judgment": "รายงานขึ้นบน", "pubmed-search-judgment": "ค้น PubMed",
    "r2r-research-proposal": "เขียน proposal R2R", "literature-review-judgment": "ทบทวนวรรณกรรม",
    "parasitology-judgment": "ปรสิตวิทยา", "lead-intelligence-judgment": "หาลีดลูกค้า",
    "token-budget-judgment": "คุม token/งบ AI", "what-skill-do-i-need": "เลือกสกิลไหนดี",
    "spreadsheet-judgment": "ใช้ Excel/Sheets", "ikigai-finder": "หาทิศชีวิต (ikigai)",
    "professional-voice-exit-judgment": "ทน/พูด/ลาออก", "writing-judgment": "เขียนงานยาว",
    "blood-donor-component-judgment": "ผู้บริจาค/ส่วนประกอบเลือด", "histotech-cytology-judgment": "ชิ้นเนื้อ/เซลล์วิทยา",
    "ai-assistant-calibration": "ตั้ง AI ให้คม", "critical-appraisal-judgment": "ประเมินงานวิจัย",
    "data-project-survival": "เอาตัวรอดงาน data", "financial-statement-judgment": "อ่านงบการเงิน",
    "marketing-judgment": "การตลาด", "ml-judgment": "ตัดสินใจ ML", "optimization-judgment": "optimization",
    "photography-judgment": "ถ่ายภาพ", "research-design-judgment": "ออกแบบงานวิจัย",
    "sales-psychology-judgment": "จิตวิทยาการขาย", "sample-size-power": "คำนวณ n/power",
    "self-development-coach": "พัฒนาตัวเอง", "molecular-judgment": "อณูชีววิทยา",
    "clinical-correlation-judgment": "เชื่อมผลแล็บ-คลินิก", "pharmacology-judgment": "เภสัชวิทยา",
    "chemistry-interpretation-judgment": "แปลผลเคมีคลินิก", "receiving-review-judgment": "รับ/กรอง feedback",
    "tdd-judgment": "เขียนเทสต์ก่อน", "choose-stat-test": "เลือกสถิติ", "self-improving-agent": "AI เรียนรู้ตัวเอง",
    "pathology-judgment": "พยาธิวิทยา", "result-release-judgment": "ปล่อยผลแล็บ",
    "source-credibility-judgment": "ประเมินแหล่งข้อมูล", "mt-law-ethics-judgment": "กฎหมาย/จรรยาบรรณ MT",
    "crm-judgment": "จัดการลูกค้า CRM", "cv-judgment": "computer vision", "progress-tracker": "ติดตามงาน",
    "python-coach": "โค้ช Python", "r2r-stats": "สถิติ R2R", "lab-management-judgment": "บริหารแล็บ",
    "applied-microbiology-judgment": "จุลชีววิทยาประยุกต์", "hematology-judgment": "โลหิตวิทยา",
    "clinmicro-judgment": "จุลชีววิทยาคลินิก", "immunoassay-judgment": "immunoassay/serology",
    "debugging-judgment": "ดีบักโค้ด", "interprofessional-communication-judgment": "สื่อสารข้ามวิชาชีพ",
    "db-judgment": "ฐานข้อมูล", "explain-simply": "อธิบายให้ง่าย", "finance-judgment": "การเงิน/ลงทุน",
    "manuscript-judgment": "เขียน manuscript", "lab-clinic-business-judgment": "เปิดแล็บ/คลินิก",
    "ai-agent-team": "ตั้งทีม AI", "digital-judgment": "PDPA/ดิจิทัล", "never-lose-a-file": "ไม่ทำไฟล์หาย",
    "clinchem-judgment": "เคมีคลินิก QC", "know-yourself": "รู้จักตัวเอง", "toxicology-judgment": "พิษวิทยา",
    "infection-control-judgment": "ควบคุมติดเชื้อ", "bloodbank-judgment": "ธนาคารเลือด",
    "offload-to-automation": "ยกงานให้ automation",
}

CAT_TH = {"clinical": "คลินิก", "career": "อาชีพ", "business": "ธุรกิจ/ขาย", "research": "วิจัย/data",
          "AImeta": "AI/meta", "comms": "สื่อสาร", "tools": "เครื่องมือ", "other": "อื่นๆ"}


def categorize(slug: str) -> str:
    for cat, keys in CATS:
        if any(k in slug for k in keys):
            return cat
    return "other"


def tier(d: float) -> str:
    if d >= 1.5:
        return "gap"
    if d >= 0.5:
        return "lift"
    if d > -0.5:
        return "tie"
    return "back"


def avg(xs):
    return round(sum(xs) / len(xs), 2) if xs else None


def compute(rows):
    items = []
    for r in rows:
        d = r.get("delta")
        if not isinstance(d, (int, float)):
            continue
        slug = str(r.get("skill", "")).replace(".md", "")
        items.append({
            "slug": slug, "label": LABELS.get(slug, slug), "delta": round(float(d), 2),
            "with": r.get("withScore"), "without": r.get("withoutScore"),
            "cat": categorize(slug), "tier": tier(float(d)),
        })
    items.sort(key=lambda x: -x["delta"])

    dist = {"gap": 0, "lift": 0, "tie": 0, "back": 0}
    for it in items:
        dist[it["tier"]] += 1

    by_cat = {}
    for cat in set(it["cat"] for it in items):
        ds = [it["delta"] for it in items if it["cat"] == cat]
        by_cat[cat] = {"n": len(ds), "avg": avg(ds)}

    clin = [it["delta"] for it in items if it["cat"] == "clinical"]
    judg = [it["delta"] for it in items if it["cat"] in JUDGMENT_CLUSTER]
    clin_avg, judg_avg = avg(clin), avg(judg)
    ratio = round(judg_avg / clin_avg, 1) if (clin_avg and clin_avg > 0) else None

    return {
        "n": len(items),
        "headline": {
            "judgment_avg": judg_avg, "judgment_n": len(judg),
            "clinical_avg": clin_avg, "clinical_n": len(clin),
            "ratio": ratio,
        },
        "distribution": dist,
        "by_category": dict(sorted(by_cat.items(), key=lambda kv: -(kv[1]["avg"] or 0))),
        "top_gaps": items[:10],
        "backfires": [it for it in items if it["tier"] == "back"],
        "items": items,
    }


def write_md(ins):
    h = ins["headline"]
    d = ins["distribution"]
    L = []
    L.append("# MT Score UP — Auto-Generated Insights (L3 synthesis)")
    L.append("")
    L.append(f"> regenerated by `scripts/build_insights.py` from `eval/_ab_slim.json` · **{ins['n']} A/B records**")
    L.append("> ตัวเลขเป็น benchmark ภายใน (×5 blind-judge, โมเดลอ่อนเป็น proxy) — ทิศของสัญญาณ ไม่ใช่สถิติประชากร MT")
    L.append("")
    L.append("## พาดหัว: รุ่นพี่ vs ตำรา (วัดได้)")
    if h["ratio"]:
        L.append(f"- **judgment cluster** (อาชีพ/ธุรกิจ/สื่อสาร/AI-meta): Δ **{h['judgment_avg']:+}** /สกิล (n={h['judgment_n']})")
        L.append(f"- **clinical** (ตำรา): Δ **{h['clinical_avg']:+}** /สกิล (n={h['clinical_n']})")
        L.append(f"- → วิจารณญาณมีค่ากว่าตำรา **~{h['ratio']}x** (จุดที่ AI-เปล่าพลาด = จุดที่ต้องมีคน)")
    L.append("")
    L.append("## การกระจาย (judgment-gap)")
    L.append("| tier | นิยาม | n |")
    L.append("|---|---|---|")
    L.append(f"| 🔴 GAP | Δ≥1.5 ห้ามเชื่อ AI ดิบ | {d['gap']} |")
    L.append(f"| 🟢 LIFT | 0.5–1.5 สกิลช่วย | {d['lift']} |")
    L.append(f"| 🟡 TIE | AI เสมอ/เก่งเอง | {d['tie']} |")
    L.append(f"| ⚫ BACKFIRE | กฎเหมารวมทำแย่ลง | {d['back']} |")
    L.append("")
    L.append("## Top 10 — AI พลาดหนักสุด (ต้องมีวิจารณญาณ)")
    for i, it in enumerate(ins["top_gaps"], 1):
        L.append(f"{i}. **{it['label']}** ({CAT_TH.get(it['cat'], it['cat'])}) · Δ {it['delta']:+} · `{it['slug']}`")
    L.append("")
    L.append("## Backfires — heuristic ที่เหมารวม (เปิดเผยตามจริง)")
    for it in ins["backfires"]:
        L.append(f"- **{it['label']}** Δ {it['delta']:+} `{it['slug']}` — *Δ ติดลบ = กฎเราทำ AI แย่ลง ไม่ได้แปลว่า AI ปลอดภัยเรื่องนั้น*")
    L.append("")
    L.append("## ค่าเฉลี่ยรายหมวด")
    L.append("| หมวด | n | Δ เฉลี่ย |")
    L.append("|---|---|---|")
    for cat, v in ins["by_category"].items():
        L.append(f"| {CAT_TH.get(cat, cat)} | {v['n']} | {v['avg']:+} |")
    L.append("")
    MD_OUT.write_text("\n".join(L) + "\n", encoding="utf-8")


def write_html(ins):
    data_json = json.dumps(ins["items"], ensure_ascii=False)
    d = ins["distribution"]
    h = ins["headline"]
    ratio_txt = f"~{h['ratio']}x" if h["ratio"] else "—"
    html = HTML_TEMPLATE.replace("__DATA__", data_json) \
        .replace("__GAP__", str(d["gap"])).replace("__LIFT__", str(d["lift"])) \
        .replace("__TIE__", str(d["tie"])).replace("__BACK__", str(d["back"])) \
        .replace("__N__", str(ins["n"])).replace("__RATIO__", ratio_txt) \
        .replace("__JUDG__", f"{h['judgment_avg']:+}" if h["judgment_avg"] is not None else "—") \
        .replace("__CLIN__", f"{h['clinical_avg']:+}" if h["clinical_avg"] is not None else "—")
    HTML_OUT.write_text(html, encoding="utf-8")


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI พลาดอะไรกับ MT — Judgment-Gap Leaderboard</title>
<style>
:root{--ink:#1a1a1a;--muted:#5f5e5a;--line:#e6e4db;--bg:#fbfbf9;--card:#fff;--teal:#0f6e56;--tealbg:#e1f5ee;--red:#a32d2d;--redbg:#fcebeb;--coral:#d85a30;--gray:#888780;}
*{box-sizing:border-box}body{font-family:-apple-system,Segoe UI,Roboto,'Sarabun',sans-serif;color:var(--ink);background:var(--bg);margin:0;padding:0 0 4rem;line-height:1.55}
.wrap{max-width:980px;margin:0 auto;padding:0 22px}header{background:#111;color:#fff;padding:2.2rem 0 1.8rem;margin-bottom:1.4rem}
h1{font-size:24px;font-weight:700;margin:0 0 6px}.sub{color:#bdbdb6;font-size:14px;max-width:720px}
.thesis{background:var(--tealbg);border-radius:12px;padding:.85rem 1.2rem;margin:1.1rem 0;font-size:15px}.thesis b{color:var(--teal)}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:1.1rem 0}
.m{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.75rem .9rem}.m .n{font-size:22px;font-weight:700}.m .l{font-size:12px;color:var(--muted)}
.controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:1rem 0 .5rem}.controls input{flex:1;min-width:160px;padding:8px 12px;border:1px solid var(--line);border-radius:8px;font-size:14px;font-family:inherit}
.chip{font-size:12.5px;padding:5px 12px;border:1px solid var(--line);border-radius:20px;background:var(--card);cursor:pointer;user-select:none}.chip.on{background:#111;color:#fff;border-color:#111}
.row{display:grid;grid-template-columns:34px 1fr 150px 96px;gap:10px;align-items:center;padding:8px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card);margin:5px 0}
.rank{font-size:15px;font-weight:700;color:var(--muted);text-align:center}.nm{font-size:14.5px;font-weight:600}.nm small{font-weight:400;color:var(--muted);font-size:12px}
.catb{display:inline-block;font-size:10.5px;padding:1px 7px;border-radius:10px;margin-left:6px}
.barwrap{position:relative;height:20px;background:#f1efe8;border-radius:5px;overflow:hidden}.barmid{position:absolute;left:50%;top:0;bottom:0;width:1px;background:#cfcdc4}.bar{position:absolute;top:3px;height:14px;border-radius:3px}
.delta{text-align:right;font-size:14px;font-weight:700;font-variant-numeric:tabular-nums}.tier{font-size:10.5px;font-weight:600;padding:1px 7px;border-radius:10px;white-space:nowrap}
.t-gap{background:var(--redbg);color:var(--red)}.t-lift{background:var(--tealbg);color:var(--teal)}.t-tie{background:#f1efe8;color:var(--gray)}.t-back{background:#2c2c2a;color:#fff}
.legend{font-size:12px;color:var(--muted);margin:.3rem 0}.legend span{margin-right:14px}
.foot{margin-top:2rem;padding-top:1rem;border-top:1px solid var(--line);font-size:12px;color:var(--muted)}
@media(max-width:640px){.row{grid-template-columns:28px 1fr 70px}.barwrap{display:none}}
</style></head><body>
<header><div class="wrap"><h1>AI พลาดอะไรกับ MT — Judgment-Gap Leaderboard</h1>
<div class="sub">จัดอันดับ __N__ จุด ว่า AI-เปล่า (ไม่มีวิจารณญาณกำกับ) พลาด/เสมอ/ดีกว่าตรงไหนในงานนักเทคนิคการแพทย์ — วัดด้วย blind-judge ×5 · regenerate อัตโนมัติจาก data</div></div></header>
<div class="wrap">
<div class="thesis">ยิ่ง <b>Δ บวกมาก</b> = AI-เปล่ายิ่งพลาดหนัก = <b>จุดที่ห้ามเชื่อ AI ดิบที่สุด</b> · Δ≈0 = AI เก่งเอง (ตำรา) · <b>Δ ติดลบ</b> = กฎเหมารวมทำให้แย่ลง (เปิดเผยตามจริง) · พาดหัว: judgment Δ __JUDG__ vs clinical Δ __CLIN__ = รุ่นพี่ค่ากว่าตำรา __RATIO__</div>
<div class="metrics">
<div class="m"><div class="n" style="color:#a32d2d">__GAP__</div><div class="l">🔴 GAP — ห้ามเชื่อ AI ดิบ</div></div>
<div class="m"><div class="n" style="color:#0f6e56">__LIFT__</div><div class="l">🟢 LIFT — สกิลช่วย</div></div>
<div class="m"><div class="n" style="color:#888780">__TIE__</div><div class="l">🟡 TIE — AI เก่งเอง</div></div>
<div class="m"><div class="n">__BACK__</div><div class="l">⚫ BACKFIRE — กฎทำแย่ลง</div></div>
</div>
<div class="legend"><span>🔴 GAP Δ≥1.5</span><span>🟢 LIFT 0.5–1.5</span><span>🟡 TIE</span><span>⚫ BACKFIRE Δ≤−0.5</span></div>
<div class="controls"><input id="q" placeholder="ค้นหาสกิล...">
<span class="chip on" data-cat="all">ทั้งหมด</span><span class="chip" data-cat="clinical">คลินิก</span><span class="chip" data-cat="career">อาชีพ</span><span class="chip" data-cat="business">ธุรกิจ/ขาย</span><span class="chip" data-cat="research">วิจัย/data</span><span class="chip" data-cat="AImeta">AI/meta</span><span class="chip" data-cat="comms">สื่อสาร</span><span class="chip" data-cat="tools">เครื่องมือ</span></div>
<div id="list"></div>
<div class="foot">ที่มา: eval/_ab_slim.json · regenerated by scripts/build_insights.py · benchmark ภายใน (Haiku proxy) — ทิศของสัญญาณ ไม่ใช่สถิติประชากร MT · Δ ติดลบของคลินิก = heuristic เหมารวม ไม่ได้แปลว่า AI ปลอดภัยเรื่องนั้น</div>
</div>
<script>
const CATB={clinical:["คลินิก","#fcebeb","#a32d2d"],career:["อาชีพ","#e1f5ee","#0f6e56"],business:["ธุรกิจ","#faeeda","#854f0b"],research:["วิจัย","#e6f1fb","#185fa5"],AImeta:["AI/meta","#eeedfe","#534ab7"],comms:["สื่อสาร","#fbeaf0","#993556"],tools:["tools","#f1efe8","#5f5e5a"],other:["อื่นๆ","#f1efe8","#5f5e5a"]};
const DATA=__DATA__;
function tcls(t){return t==='gap'?['🔴 GAP','t-gap']:t==='lift'?['🟢 LIFT','t-lift']:t==='tie'?['🟡 TIE','t-tie']:['⚫ BACK','t-back'];}
let curCat="all",curQ="";
function render(){const list=document.getElementById("list");list.innerHTML="";
 const f=DATA.filter(r=>(curCat==="all"||r.cat===curCat)&&(!curQ||(r.label||'').toLowerCase().includes(curQ)||r.slug.includes(curQ)));
 f.forEach((r,i)=>{const[tl,tc]=tcls(r.tier);const cb=CATB[r.cat]||CATB.other;const pos=r.delta>=0;const mag=Math.min(Math.abs(r.delta)/4,1)*48;
  const bar=`<div class="barwrap"><div class="barmid"></div><div class="bar" style="${pos?'left:50%':'right:50%'};width:${mag}%;background:${pos?'#1d9e75':'#2c2c2a'}"></div></div>`;
  list.insertAdjacentHTML("beforeend",`<div class="row"><div class="rank">${i+1}</div><div class="nm">${r.label}<span class="catb" style="background:${cb[1]};color:${cb[2]}">${cb[0]}</span><br><small>${r.slug} · ${r.without}→${r.with}</small></div>${bar}<div><span class="delta" style="color:${pos?'#0f6e56':'#a32d2d'}">${pos?'+':''}${r.delta.toFixed(1)}</span><br><span class="tier ${tc}">${tl}</span></div></div>`);});
 if(!f.length)list.innerHTML='<p style="color:#5f5e5a;padding:1rem">ไม่พบ</p>';}
document.querySelectorAll(".chip").forEach(ch=>ch.onclick=()=>{document.querySelectorAll(".chip").forEach(x=>x.classList.remove("on"));ch.classList.add("on");curCat=ch.dataset.cat;render();});
document.getElementById("q").oninput=e=>{curQ=e.target.value.toLowerCase().trim();render();};
render();
</script></body></html>"""


def main() -> int:
    try:
        rows = json.loads(SLIM.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"build_insights: cannot read {SLIM}: {e}")
        return 1
    if not isinstance(rows, list):
        print("build_insights: _ab_slim.json is not a list")
        return 1

    ins = compute(rows)
    DATA_OUT.write_text(json.dumps(ins, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_md(ins)
    write_html(ins)

    h = ins["headline"]
    print(f"build_insights: {ins['n']} records -> insights-data.json + INSIGHTS.md + leaderboard.html")
    print(f"  distribution: GAP {ins['distribution']['gap']} · LIFT {ins['distribution']['lift']} "
          f"· TIE {ins['distribution']['tie']} · BACKFIRE {ins['distribution']['back']}")
    if h["ratio"]:
        print(f"  headline: judgment {h['judgment_avg']:+} vs clinical {h['clinical_avg']:+} = ~{h['ratio']}x")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
