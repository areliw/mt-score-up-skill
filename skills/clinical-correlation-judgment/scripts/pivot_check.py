#!/usr/bin/env python3
"""pivot_check — route a pivotal lab value to the next branch the card teaches, without anchoring:
anemia (MCV -> iron study -> Hb typing) and jaundice (DB/TB ratio read against EVERY source heuristic).

Black-box tool for clinical-correlation-judgment. Run --help first; read the source only if a branch looks wrong.
Sources:
  - clinical-correlation-judgment card Fork 1 (MCV < 80 microcytic -> iron study; > 100 macrocytic -> B12/folate;
    normocytic -> retic/hemolysis; ferritin low + TIBC high + %sat low = IDA -> find the blood-loss source;
    ferritin normal in a microcytic patient -> do NOT stop at IDA -> Hb typing / DNA), Fork 3 (Hb typing
    puzzling / A2 high -> DNA; KLF1), trap list (anchoring: keep >= 3 DDx), and the DB/TB heuristic with
    its own warning: "teaching heuristic, not a fixed cut-off - boundaries blur / overlap"
  - 510416 Clinical Correlation digest §2 (microcytic DDx IDA/thal/ACD/sideroblastic/lead; DB/TB pre < 0.2,
    intra 0.3-0.6, post >= 0.5) and Case 5 (KLF1 mutation mimics beta-thal trait with HbA2 > 3.5%)
  - 505402 Clinical Chemistry digest §5.3 (DB/TB < 20-30% unconjugated, ~30-60% mixed, > 70% conjugated)
  - 510403 Clinical Laboratory Practice digest §3.8 (A2A pattern: HbA2 >= 3.5% = beta-thal trait)
Iron-study inputs are the LAB'S OWN flags (L / N / H against its reference range) - no ranges are built in.
MCV 80/100 and HbA2 3.5% are the card/digest teaching values and can be overridden.
ADVISORY ONLY: MT correlates and points the way; diagnosis belongs to the physician.

Examples
  python pivot_check.py anemia --mcv 66 --ferritin N
  python pivot_check.py anemia --mcv 66 --ferritin L --tibc H --sat L --serum-iron L
  python pivot_check.py anemia --mcv 70 --ferritin N --hba2 5.2
  python pivot_check.py jaundice --db 2.9 --tb 5.0
"""
import argparse
import json
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

MICRO_DDX = ["iron deficiency anemia", "thalassemia trait / Hb variant", "anemia of chronic disease",
             "sideroblastic anemia", "lead poisoning"]                       # 510416 §2


def anemia(mcv, ferritin=None, tibc=None, sat=None, serum_iron=None, hba2=None,
           mcv_low=80.0, mcv_high=100.0, hba2_cut=3.5):
    steps, ddx, caveats = [], [], []
    if mcv < mcv_low:
        branch = "microcytic"
        ddx = list(MICRO_DDX)
        steps.append("MCV %g < %g -> iron study (ferritin, serum iron, TIBC, %%sat)" % (mcv, mcv_low))
        flags = {"ferritin": ferritin, "tibc": tibc, "sat": sat}
        if ferritin is None:
            steps.append("ferritin not given -> iron study incomplete; no branch beyond 'do the iron study'")
        elif ferritin == "L" and tibc == "H" and sat == "L":
            steps.append("ferritin L + TIBC H + %sat L = IDA pattern -> find the SOURCE of blood loss next")
            caveats.append("IDA found does not end the work-up: the cause (e.g. GI / menstrual loss) is the next question")
        elif ferritin in ("N", "H"):
            steps.append("ferritin %s in a microcytic patient -> do NOT stop at IDA -> reflex Hb typing / DNA" % ferritin)
            ddx = [d for d in ddx if d != "iron deficiency anemia"] + ["iron deficiency (less likely: ferritin not low)"]
        else:
            missing = [k for k, v in flags.items() if v is None]
            steps.append("iron pattern mixed/incomplete (%s) -> complete all four tests before labelling"
                         % (", ".join("%s=%s" % (k, v) for k, v in flags.items())))
            if missing:
                caveats.append("missing: " + ", ".join(missing))
        if hba2 is not None:
            if hba2 >= hba2_cut:
                steps.append("HbA2 %g%% >= %g%% (A2A) -> beta-thal trait PATTERN" % (hba2, hba2_cut))
                caveats.append("KLF1 mutation can mimic beta-thal trait (510416 Case 5) -> DNA before couple counselling")
            else:
                steps.append("HbA2 %g%% < %g%% -> beta-thal trait unlikely by typing; alpha-thal not excluded "
                             "(510403 §3.8: 'Normal (+/- alpha-thal)')" % (hba2, hba2_cut))
    elif mcv > mcv_high:
        branch = "macrocytic"
        ddx = ["vitamin B12 deficiency", "folate deficiency", "other causes - see references"]
        steps.append("MCV %g > %g -> B12 / folate" % (mcv, mcv_high))
    else:
        branch = "normocytic"
        ddx = ["hemolysis", "blood loss", "other causes - see references"]
        steps.append("MCV %g within %g-%g -> reticulocyte count / hemolysis work-up (bilirubin, haptoglobin, LDH)"
                     % (mcv, mcv_low, mcv_high))
    return {"branch": branch, "steps": steps, "keep_open_ddx": ddx, "caveats": caveats,
            "anchoring_guard": "keep >= 3 DDx open and order a test that could REFUTE each, not only confirm one"}


# DB/TB bands per source (predicate, label, category). category: pre / hepatic / post / unclear
BANDS = {
    "card (heuristic)": [
        (lambda r: r < 0.20, "pre-hepatic (unconjugated)", "pre"),
        (lambda r: 0.20 <= r <= 0.50, "hepatocellular", "hepatic"),
        (lambda r: r > 0.50, "post-hepatic (obstructive)", "post")],
    "505402 §5.3": [
        (lambda r: r < 0.20, "unconjugated", "pre"),
        (lambda r: 0.20 <= r < 0.30, "boundary of '<20-30%' unconjugated", "unclear"),
        (lambda r: 0.30 <= r <= 0.60, "mixed (hepatitis / cirrhosis)", "hepatic"),
        (lambda r: 0.60 < r <= 0.70, "not covered (60-70% gap)", "unclear"),
        (lambda r: r > 0.70, "conjugated (cholestasis)", "post")],
    "510416 §2": [
        (lambda r: r < 0.20, "pre-hepatic", "pre"),
        (lambda r: 0.20 <= r < 0.30, "not covered (0.2-0.3 gap)", "unclear"),
        (lambda r: 0.30 <= r < 0.50, "intra-hepatic", "hepatic"),
        (lambda r: 0.50 <= r <= 0.60, "overlap: intra (0.3-0.6) AND post (>=0.5)", "unclear"),
        (lambda r: r > 0.60, "post-hepatic", "post")],
}


def jaundice(db=None, tb=None, ratio=None):
    if ratio is None:
        if db is None or tb is None or tb <= 0:
            raise ValueError("give --db and --tb (tb > 0), or --ratio")
        if db > tb:
            raise ValueError("direct bilirubin cannot exceed total - check the values/units")
        ratio = db / tb
    readings = {}
    for src, bands in BANDS.items():
        for pred, label, cat in bands:
            if pred(ratio):
                readings[src] = {"label": label, "category": cat}
                break
    cats = {v["category"] for v in readings.values()}
    agree = len(cats) == 1 and "unclear" not in cats
    return {"ratio": ratio, "readings": readings, "sources_agree": agree,
            "verdict": ("sources agree: %s" % next(iter(cats))) if agree else
            "SOURCES DISAGREE / boundary zone -> the ratio cannot decide; use the enzyme pattern (AST/ALT vs "
            "ALP/GGT) + clinical context (card Fork 1)",
            "next": "DB/TB separates unconjugated (< 0.20) from conjugated only; hepatocellular vs cholestatic "
                    "-> run: pivot_check.py liver --alt .. --alt-uln .. --alp .. --alp-uln .. (R ratio)"}


def liver_pattern(alt, alt_uln, alp, alp_uln):
    """Injury pattern from the R ratio = (ALT/ULN) / (ALP/ULN), with the lab's own ULNs.

    Convention (ACG 2014 DILI guideline; LiverTox/RUCAM manual, NBK548272): R >= 5 hepatocellular,
    R <= 2 cholestatic, 2 < R < 5 mixed. RUCAM writes the bounds strictly (> 5 / < 2), so an R of exactly
    5 or 2 is flagged. Shortcuts from the same manual: ALT > 2xULN with ALP normal = hepatocellular, and
    ALP > 2xULN with ALT normal = cholestatic (no ratio needed). Use same-day values.
    Added 2026-10-08: the owner could not settle the DB/TB bands and our three sources disagree; the
    R ratio is the standard way to split hepatocellular from cholestatic (510416 Case 8: ALT 1220,
    ALP 111 normal, DB/TB 0.58 -> hepatocellular DILI, which the card's DB/TB band calls post-hepatic).
    """
    for v, name in ((alt, "ALT"), (alt_uln, "ALT ULN"), (alp, "ALP"), (alp_uln, "ALP ULN")):
        if v is None or v <= 0:
            raise ValueError("%s must be > 0 (use the lab's own reference limits)" % name)
    alt_x, alp_x = alt / alt_uln, alp / alp_uln
    if alt_x > 2 and alp_x <= 1:
        return {"alt_x_uln": alt_x, "alp_x_uln": alp_x, "r": None, "pattern": "hepatocellular",
                "how": "shortcut: ALT > 2xULN with ALP normal (RUCAM manual)", "boundary": False}
    if alp_x > 2 and alt_x <= 1:
        return {"alt_x_uln": alt_x, "alp_x_uln": alp_x, "r": None, "pattern": "cholestatic",
                "how": "shortcut: ALP > 2xULN with ALT normal (RUCAM manual)", "boundary": False}
    r = alt_x / alp_x
    if r >= 5:
        pattern = "hepatocellular"
    elif r <= 2:
        pattern = "cholestatic"
    else:
        pattern = "mixed"
    boundary = abs(r - 5) < 1e-9 or abs(r - 2) < 1e-9
    return {"alt_x_uln": alt_x, "alp_x_uln": alp_x, "r": r, "pattern": pattern,
            "how": "R = (ALT/ULN) / (ALP/ULN) = %.2f / %.2f" % (alt_x, alp_x), "boundary": boundary}


def main(argv=None):
    try:  # never crash a non-UTF-8 console (e.g. Thai cp874) on the section sign / Thai text
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("anemia")
    p.add_argument("--mcv", type=float, required=True)
    for k in ("ferritin", "tibc", "sat", "serum-iron"):
        p.add_argument("--" + k, choices=["L", "N", "H"], help="lab flag vs its own reference range")
    p.add_argument("--hba2", type=float, help="HbA2 %% from Hb typing")
    p.add_argument("--mcv-low", type=float, default=80.0)
    p.add_argument("--mcv-high", type=float, default=100.0)
    p.add_argument("--hba2-cut", type=float, default=3.5)
    p = sub.add_parser("jaundice")
    p.add_argument("--db", type=float, help="direct bilirubin")
    p.add_argument("--tb", type=float, help="total bilirubin (same unit)")
    p.add_argument("--ratio", type=float, help="DB/TB as a fraction (0-1) if already computed")
    p = sub.add_parser("liver", help="R ratio: hepatocellular / mixed / cholestatic")
    p.add_argument("--alt", type=float, required=True)
    p.add_argument("--alt-uln", type=float, required=True, help="your lab's ALT upper reference limit")
    p.add_argument("--alp", type=float, required=True)
    p.add_argument("--alp-uln", type=float, required=True, help="your lab's ALP upper reference limit")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "anemia":
            res = anemia(a.mcv, a.ferritin, a.tibc, a.sat, a.serum_iron, a.hba2, a.mcv_low, a.mcv_high, a.hba2_cut)
        elif a.cmd == "liver":
            res = liver_pattern(a.alt, a.alt_uln, a.alp, a.alp_uln)
        else:
            res = jaundice(a.db, a.tb, a.ratio)
    except ValueError as e:
        sys.exit(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "anemia":
        print("BRANCH: " + res["branch"])
        for s in res["steps"]:
            print("  -> " + s)
        for c in res["caveats"]:
            print("  CAVEAT: " + c)
        print("KEEP OPEN: " + "; ".join(res["keep_open_ddx"]))
        print("GUARD: " + res["anchoring_guard"])
    elif a.cmd == "liver":
        print("ALT %.2f x ULN · ALP %.2f x ULN" % (res["alt_x_uln"], res["alp_x_uln"]))
        print("PATTERN: %s  (%s)" % (res["pattern"].upper(), res["how"]))
        if res["boundary"]:
            print("  NOTE: R exactly on a bound - RUCAM writes > 5 / < 2, so this case is 'mixed' under RUCAM")
    else:
        print("DB/TB = %.2f (%.0f%%)" % (res["ratio"], res["ratio"] * 100))
        for src, r in res["readings"].items():
            print("  %-18s %s" % (src, r["label"]))
        print("VERDICT: " + res["verdict"])
        print("NEXT: " + res["next"])
    print("ADVISORY: MT correlates and flags; diagnosis belongs to the physician - confirm per SOP and references.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
