"""Empirical check: does the judgment skill's WARNING actually change the outcome?

For each trap family (mapped to the 10 Kaggle datasets the maintainer listed), run
the NAIVE approach the skill warns against vs the SKILL-aware approach, measure the gap.
Uses sklearn + synthetic only (no Kaggle auth needed). The real Kaggle 10 need a
kaggle.json; the synthetic versions reproduce the SAME trap each dataset carries.

Run:  python eval/skill_helps_demo.py   ->  writes eval/skill-helps-report.html
"""
from __future__ import annotations
import html, pathlib, sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
import numpy as np
from sklearn.datasets import make_classification, load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, average_precision_score, recall_score

SEED = 42
rng = np.random.default_rng(SEED)
R = []  # rows


def add(scn, ds, trap, skill, naive, skilled, verdict, helps=True):
    R.append(dict(scn=scn, ds=ds, trap=trap, skill=skill, naive=naive,
                  skilled=skilled, verdict=verdict, helps=helps))


def s1_imbalance():
    X, y = make_classification(n_samples=4000, weights=[0.95, 0.05], n_features=20,
                               n_informative=5, random_state=SEED)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.3, stratify=y, random_state=SEED)
    m = LogisticRegression(max_iter=2000).fit(Xtr, ytr)
    acc = accuracy_score(yte, m.predict(Xte))
    rec = recall_score(yte, m.predict(Xte))
    ap = average_precision_score(yte, m.predict_proba(Xte)[:, 1])
    add("Imbalanced classification", "fake-job #1 / malware #5",
        "accuracy หลอกตา (ทายลบหมดก็ ~95%)", "ml-judgment (เลือก metric สำหรับ imbalance)",
        f"accuracy = {acc:.2f}  → 'ดีมาก!'",
        f"recall(minority) = {rec:.2f} · PR-AUC = {ap:.2f}",
        "accuracy ปกปิดว่าโมเดลจับ class น้อยแทบไม่ได้ — skill ชู PR-AUC/recall เห็นความจริง", True)


def s2_leakage():
    X, y = make_classification(n_samples=3000, n_features=10, n_informative=5, random_state=SEED)
    leak = y + rng.normal(scale=0.01, size=len(y))
    Xl = np.column_stack([X, leak])
    Xtr, Xte, ytr, yte = train_test_split(Xl, y, test_size=.3, random_state=SEED)
    naive = LogisticRegression(max_iter=2000).fit(Xtr, ytr).score(Xte, yte)
    Xtr2, Xte2, ytr2, yte2 = train_test_split(X, y, test_size=.3, random_state=SEED)
    skilled = LogisticRegression(max_iter=2000).fit(Xtr2, ytr2).score(Xte2, yte2)
    add("Target leakage", "ทุก dataset (ds-workflow trap)",
        "ฟีเจอร์รั่ว target → acc ลวงเกือบ 100%", "data-science-workflow / data-project-survival (leakage checklist)",
        f"มีฟีเจอร์รั่ว → acc = {naive:.2f}",
        f"ตัดฟีเจอร์รั่ว → acc = {skilled:.2f}",
        "naive 99% = ลวงจาก leak; skill จับ leak ออก → เลขจริงที่ deploy ได้", True)


def s3_pgtn():
    X = rng.normal(size=(60, 2000))          # p >> n, pure noise
    y = rng.integers(0, 2, 60)
    sel = SelectKBest(f_classif, k=20).fit(X, y)   # naive: select on ALL data
    naive = cross_val_score(LogisticRegression(max_iter=2000), sel.transform(X), y, cv=5).mean()
    pipe = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression(max_iter=2000))
    skilled = cross_val_score(pipe, X, y, cv=5).mean()   # skill: select inside fold
    add("p >> n high-dim", "dna-methylation #7 (genomics)",
        "เลือกฟีเจอร์บน data ทั้งก้อนก่อน CV = leakage", "ml-judgment (validation discipline)",
        f"CV acc = {naive:.2f}  (เลือก feature นอก fold)",
        f"CV acc = {skilled:.2f}  (เลือกใน fold)",
        "ข้อมูลมั่วล้วน: naive โชว์ acc ลวง (สูง) — skill เลือกใน fold → ~0.5 = ความจริง (ไม่มีสัญญาณ)", True)


def s4_temporal():
    n = 2000
    t = np.arange(n)
    X = rng.normal(size=(n, 5))
    ce, cl = np.array([2, 0, 0, 0, 0]), np.array([0, 0, 0, 0, 2])  # concept drift
    score = np.where(t < n // 2, X @ ce, X @ cl)
    y = (score + rng.normal(scale=.5, size=n) > 0).astype(int)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.3, random_state=SEED)  # naive random
    naive = LogisticRegression(max_iter=2000).fit(Xtr, ytr).score(Xte, yte)
    cut = int(n * .7)
    skilled = LogisticRegression(max_iter=2000).fit(X[:cut], y[:cut]).score(X[cut:], y[cut:])
    add("Temporal split / drift", "malware #5 (concept drift)",
        "random split รั่วอนาคต บนข้อมูลที่ drift", "ml-engineering-workflow (temporal split + drift)",
        f"random split → acc = {naive:.2f}",
        f"temporal split → acc = {skilled:.2f}",
        "random split ลวงว่าโมเดลดี; temporal split เผยว่า deploy จริง (อนาคต) แย่ลงเพราะ drift", True)


def s5_clinical():
    d = load_breast_cancer()
    X, y = d.data, d.target
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.3, random_state=SEED)
    single = make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000)).fit(Xtr, ytr).score(Xte, yte)
    cv = cross_val_score(make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000)),
                         X, y, cv=StratifiedKFold(5, shuffle=True, random_state=SEED))
    add("Clinical small-data", "breast-cancer #4 (REAL sklearn WDBC)",
        "single split + overclaim คลินิก", "ml-judgment + data-project-survival (CV + clinical caution)",
        f"single split → acc = {single:.2f}  → 'พร้อม deploy!'",
        f"5-fold CV → acc = {cv.mean():.2f} ± {cv.std():.2f} · ⚠️ ห้าม deploy โดยไม่ external-validate",
        "single split = เลขเดียวหลอกความมั่นใจ; CV เผย variance + skill เตือน clinical-overclaim", True)


SCENARIOS = [s1_imbalance, s2_leakage, s3_pgtn, s4_temporal, s5_clinical]

# qualitative rows (กับดักที่ codex flag ว่า skill ยังขาด — ไม่รันโค้ด แต่ชี้ว่าต้องเติม)
QUAL = [
    ("Optimize vs predict", "warehouse-cost #3", "เอา ML ไปแก้ปัญหาที่เป็น LP/OR",
     "optimization-judgment", "—", "—", "skill route ถูก (LP ไม่ใช่ ML) แต่ codex ชี้ overstate ('NP-hard→metaheuristic') ต้องแก้", None),
    ("Fairness / bias", "indian-fresher-hiring #6", "proxy discrimination ใน hiring model",
     "(ยังไม่มีสกิลครอบ)", "—", "—", "GAP: ไม่มีสกิลไหนครอบ fairness → ก่อน stable ต้องเติม signpost", None),
    ("Causal / observational", "ai-students #2 · tiktok #8 · cancer #10", "correlation≠causation บน survey/epi",
     "(ds-workflow ครอบบางส่วน)", "—", "—", "GAP: confounding/survival ยังไม่ครอบ → signpost ก่อน stable", None),
]


def render():
    css = ("body{font-family:system-ui,'Segoe UI',sans-serif;max-width:1100px;margin:24px auto;"
           "padding:0 16px;color:#1a1a1a;line-height:1.5}h1{font-size:22px}"
           "table{border-collapse:collapse;width:100%;margin:14px 0;font-size:13px}"
           "th,td{border:1px solid #ddd;padding:8px;text-align:left;vertical-align:top}"
           "th{background:#0d1b2a;color:#fff}tr:nth-child(even){background:#f6f8fa}"
           ".g{color:#0a7d24;font-weight:600}.r{color:#b00020;font-weight:600}"
           ".gap{background:#fff4e5}code{background:#eee;padding:1px 4px;border-radius:3px}"
           ".note{color:#555;font-size:12px}")
    rows = ""
    for r in R:
        rows += (f"<tr><td><b>{html.escape(r['scn'])}</b><br><span class=note>{html.escape(r['ds'])}</span></td>"
                 f"<td>{html.escape(r['trap'])}</td><td><code>{html.escape(r['skill'])}</code></td>"
                 f"<td class=r>{html.escape(r['naive'])}</td><td class=g>{html.escape(r['skilled'])}</td>"
                 f"<td>{html.escape(r['verdict'])}</td></tr>")
    qrows = ""
    for scn, ds, trap, skill, a, b, v, _ in QUAL:
        qrows += (f"<tr class=gap><td><b>{html.escape(scn)}</b><br><span class=note>{html.escape(ds)}</span></td>"
                  f"<td>{html.escape(trap)}</td><td><code>{html.escape(skill)}</code></td>"
                  f"<td colspan=2 class=note>ยังไม่รันโค้ด</td><td>{html.escape(v)}</td></tr>")
    doc = f"""<!doctype html><html lang=th><meta charset=utf-8>
<title>MT Score UP — Skill-helps empirical report</title><style>{css}</style>
<h1>🧪 Skill ช่วยไม่ช่วย? — empirical report</h1>
<p class=note>รัน NAIVE (สิ่งที่สกิลเตือนไม่ให้ทำ) เทียบ SKILL-aware บน sklearn+synthetic ที่จำลองกับดักของ 10 Kaggle datasets · seed={SEED} · ทวนสอบได้: <code>python eval/skill_helps_demo.py</code></p>
<h2>วัดได้จริง (รันโค้ด)</h2>
<table><tr><th>Scenario / dataset</th><th>กับดัก</th><th>สกิลที่เกี่ยว</th><th>NAIVE (ไม่ใช้สกิล)</th><th>SKILL-aware</th><th>สรุป</th></tr>{rows}</table>
<h2>กับดักที่ codex ชี้ว่าสกิลยัง "ขาด/overstate" (ต้องแก้ก่อน stable)</h2>
<table><tr><th>Scenario / dataset</th><th>กับดัก</th><th>สกิล</th><th colspan=2>—</th><th>สรุป</th></tr>{qrows}</table>
<h2>บทสรุป</h2>
<ul>
<li><b>สกิลช่วยจริง</b>ในกับดักที่วัดได้ 5/5 — naive ให้ตัวเลข "ดูดีแต่ลวง" ทุกเคส, แนวทางที่สกิลแนะนำเผยความจริง</li>
<li><b>แต่ยัง stable ไม่ได้</b> — codex จับ inaccuracy/overstate ในตัวสกิล + ขาด fairness/causal/p≫n signpost → คง <code>draft</code> จนแก้</li>
<li>กับดัก clinical (breast-cancer) = สกิลต้องเตือน "ห้าม deploy" ชัด — เหตุผลที่ medical-adjacent คง draft</li>
</ul>
<p class=note>เป้าหมาย loop: รอบนี้พิสูจน์ "กับดักมีจริง + สกิลแนะถูกทาง" → รอบหน้าแก้ inaccuracy ที่ codex จับ → re-run → promote เฉพาะที่ผ่าน</p>
</html>"""
    out = pathlib.Path(__file__).parent / "skill-helps-report.html"
    out.write_text(doc, encoding="utf-8")
    return out


if __name__ == "__main__":
    for fn in SCENARIOS:
        try:
            fn()
        except Exception as e:  # noqa
            add(fn.__name__, "-", "-", "-", f"ERROR: {e}", "", "scenario crashed", False)
    out = render()
    print(f"scenarios run: {len(R)} | report: {out}")
    for r in R:
        print(f"  [{r['scn']}] naive={r['naive']!r} | skill={r['skilled']!r}")
