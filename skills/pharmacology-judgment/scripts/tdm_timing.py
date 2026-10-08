#!/usr/bin/env python3
"""tdm_timing — is this drug level interpretable? Steady state, peak vs trough, the drug's own rule.

Black-box tool for pharmacology-judgment. Run --help first; read the source only if a verdict looks wrong.
Rules (card Fork 7 + trap list; PHARMACOLOGY digest §10 TDM, §8c digoxin, §2 kinetics):
  - sample at steady state, ~4-5 t½ after start or a dose change:  < 4 t½ -> NOT at steady state
    (4 to < 5 t½ = approaching, >= 5 t½ = steady state)
  - efficacy -> trough (before the next dose) · toxicity -> peak
  - aminoglycoside -> BOTH peak and trough (peak = kill, trough = nephro/ototoxicity)
  - vancomycin does NOT follow that peak/trough rule: card cites AUC/MIC 400-600 (guideline since 2020)
    -> AUC estimation is needed; this tool does not compute AUC
  - digoxin -> read with K+: hypokalemia makes digoxin more toxic
  - zero-order drugs (phenytoin ...) -> t½ not constant: steady-state timing from t½ is unreliable,
    and a small dose change can push the level up disproportionately
Therapeutic range and K+ lower limit are LAB values -> arguments; the digest ranges are teaching values.
ADVISORY ONLY: MT does not prescribe; dose decisions belong to the physician/pharmacist.

Examples
  python tdm_timing.py --drug-class digoxin --half-life 40 --hours-on-regimen 72 --sample trough --purpose efficacy
  python tdm_timing.py --drug-class aminoglycoside --half-life 2.5 --hours-on-regimen 24 --sample trough --purpose toxicity
  python tdm_timing.py --drug-class digoxin --half-life 40 --hours-on-regimen 220 --sample trough \\
        --purpose efficacy --level 1.6 --range 1 2 --k 3.1 --k-low 3.5
  python tdm_timing.py --csv ../data/tdm_teaching_requests.csv
"""
import argparse
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pk_calc import fraction_of_steady_state  # noqa: E402

SS_MIN_HALF_LIVES = 4.0     # card Fork 7 / digest §10: "~4-5 t½"
SS_FULL_HALF_LIVES = 5.0
DRUG_CLASSES = ["aminoglycoside", "vancomycin", "digoxin", "zero-order", "other"]


def steady_state_status(half_lives):
    if half_lives >= SS_FULL_HALF_LIVES:
        return "STEADY STATE"
    if half_lives >= SS_MIN_HALF_LIVES:
        return "APPROACHING STEADY STATE (4-5 t½)"
    return "NOT AT STEADY STATE"


def expected_sample(drug_class, purpose):
    """Which sample(s) the card's rule asks for."""
    if drug_class == "aminoglycoside":
        return {"peak", "trough"}
    if drug_class == "vancomycin":
        return {"auc"}
    return {"trough"} if purpose == "efficacy" else {"peak"}


def assess(drug_class, half_life, hours_on_regimen, sample, purpose, paired_sample="none",
           level=None, range_low=None, range_high=None, k=None, k_low=None):
    if drug_class not in DRUG_CLASSES:
        raise ValueError("drug class must be one of %s" % DRUG_CLASSES)
    problems, cautions, notes = [], [], []
    res = {"drug_class": drug_class, "sample": sample, "purpose": purpose}

    # 1. steady state
    if drug_class == "zero-order":
        res["steady_state"] = "UNKNOWN (zero-order)"
        cautions.append("zero-order kinetics: t½ is not constant -> steady-state timing from t½ is unreliable; "
                     "small dose increases raise the level disproportionately (card Fork 7)")
    else:
        if half_life is None or half_life <= 0:
            raise ValueError("half-life (h) is required and must be > 0")
        n = hours_on_regimen / half_life
        res["half_lives_elapsed"] = n
        res["pct_of_steady_state"] = fraction_of_steady_state(n) * 100
        res["steady_state"] = steady_state_status(n)
        if res["steady_state"] == "NOT AT STEADY STATE":
            problems.append("sampled at %.2f t½ (%.1f%% of steady state) - wait until ~4-5 t½ after the start or "
                            "last dose change (%.4g-%.4g h)" % (n, res["pct_of_steady_state"],
                                                                SS_MIN_HALF_LIVES * half_life,
                                                                SS_FULL_HALF_LIVES * half_life))

    # 2. sample type vs the drug's rule
    want = expected_sample(drug_class, purpose)
    res["expected_sample"] = sorted(want)
    if drug_class == "vancomycin":
        problems.append("vancomycin: peak/trough logic of aminoglycosides does not apply - card cites "
                        "AUC/MIC 400-600; an AUC estimate (per local protocol) is needed")
    elif drug_class == "aminoglycoside":
        have = {sample} | ({paired_sample} if paired_sample in ("peak", "trough") else set())
        missing = want - have
        if missing:
            problems.append("aminoglycoside needs BOTH peak and trough - missing: %s" % ", ".join(sorted(missing)))
    elif sample == "random":
        problems.append("random-time sample: timing unknown -> cannot be read against a trough/peak range")
    elif sample not in want:
        problems.append("%s sampled for %s - the rule is %s (efficacy -> trough, toxicity -> peak)"
                        % (sample, purpose, "/".join(sorted(want))))

    # 3. digoxin needs K+
    if drug_class == "digoxin":
        if k is None:
            problems.append("digoxin without K+ - read digoxin together with K+ (hypokalemia raises toxicity)")
        elif k_low is None:
            cautions.append("K+ given without the lab's lower limit (--k-low) - hypokalemia not assessed")
        elif k < k_low:
            cautions.append("HYPOKALEMIA (K+ %.2f < %.2f): digoxin toxicity risk is higher even inside the range"
                         % (k, k_low))

    # 4. level vs the lab's range (only meaningful when timing is right)
    if level is not None and range_low is not None and range_high is not None:
        pos = "below" if level < range_low else ("above" if level > range_high else "within")
        res["level_vs_range"] = "%s (%.4g vs %.4g-%.4g, lab range)" % (pos, level, range_low, range_high)
        if problems:
            notes.append("level compared to range only for information - timing/sample problems above come first")

    res["problems"] = problems
    res["cautions"] = cautions
    res["notes"] = notes
    res["verdict"] = ("NOT INTERPRETABLE AS REQUESTED" if problems else
                      "INTERPRETABLE WITH CAUTION" if cautions else "INTERPRETABLE")
    return res


def _f(v):
    return float(v) if v not in (None, "") else None


def load_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        r = {k.strip().lower(): (v or "").strip() for k, v in r.items()}
        out.append((r.get("id", ""), dict(
            drug_class=r["drug_class"], half_life=_f(r.get("half_life_h")),
            hours_on_regimen=float(r["hours_on_regimen"]), sample=r["sample"], purpose=r["purpose"],
            paired_sample=r.get("paired_sample") or "none", level=_f(r.get("level")),
            range_low=_f(r.get("range_low")), range_high=_f(r.get("range_high")),
            k=_f(r.get("k")), k_low=_f(r.get("k_low")))))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--drug-class", choices=DRUG_CLASSES)
    ap.add_argument("--half-life", type=float, help="hours (patient-specific estimate)")
    ap.add_argument("--hours-on-regimen", type=float, help="hours since start or last dose change")
    ap.add_argument("--sample", choices=["trough", "peak", "random"])
    ap.add_argument("--purpose", choices=["efficacy", "toxicity"], default="efficacy")
    ap.add_argument("--paired-sample", choices=["none", "peak", "trough"], default="none",
                    help="the other level already drawn (aminoglycoside)")
    ap.add_argument("--level", type=float)
    ap.add_argument("--range", nargs=2, type=float, metavar=("LOW", "HIGH"), help="lab therapeutic range")
    ap.add_argument("--k", type=float, help="K+ mmol/L (digoxin)")
    ap.add_argument("--k-low", type=float, help="lab lower reference limit for K+")
    ap.add_argument("--csv", help="batch: id,drug_class,half_life_h,hours_on_regimen,sample,purpose,"
                                  "paired_sample,level,range_low,range_high,k,k_low")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.csv:
            cases = load_csv(a.csv)
        else:
            if not (a.drug_class and a.hours_on_regimen is not None and a.sample):
                ap.error("give --drug-class --hours-on-regimen --sample (and --half-life), or --csv")
            lo, hi = (a.range if a.range else (None, None))
            cases = [("request", dict(drug_class=a.drug_class, half_life=a.half_life,
                                      hours_on_regimen=a.hours_on_regimen, sample=a.sample, purpose=a.purpose,
                                      paired_sample=a.paired_sample, level=a.level, range_low=lo, range_high=hi,
                                      k=a.k, k_low=a.k_low))]
        results = [dict(id=cid, **assess(**kw)) for cid, kw in cases]
    except (ValueError, KeyError) as e:
        ap.error(str(e))
    if a.json:
        print(json.dumps(results if a.csv else results[0], ensure_ascii=False, indent=1))
        return 0
    for r in results:
        ss = r["steady_state"]
        if "half_lives_elapsed" in r:
            ss += " (%.2f t½, %.1f%%)" % (r["half_lives_elapsed"], r["pct_of_steady_state"])
        print("%-10s %s | %s sample for %s | %s" % (r["id"], r["drug_class"], r["sample"], r["purpose"], ss))
        if r.get("level_vs_range"):
            print("%-10s level %s" % ("", r["level_vs_range"]))
        for p_ in r["problems"]:
            print("%-10s PROBLEM: %s" % ("", p_))
        for c in r["cautions"]:
            print("%-10s CAUTION: %s" % ("", c))
        for n in r["notes"]:
            print("%-10s note: %s" % ("", n))
        print("%-10s -> %s" % ("", r["verdict"]))
    print("ADVISORY: decision support only - MT does not prescribe; confirm with the lab SOP, physician/pharmacist.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
