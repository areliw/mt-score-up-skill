#!/usr/bin/env python3
"""eqa_eval — score EQA/PT results (bias %, SDI) against the SCHEME'S criterion, tell a single miss from a
pattern, and print the investigation order to follow before any CAPA.

Black-box tool for lab-management-judgment. Run --help first; read the source only if a number looks wrong.
Sources:
  - lab-management-judgment card Fork 2 (EQA bias = (mean lab - mean peer) / mean peer x 100; IQC passing
    does not prove accuracy) and Fork 9 (investigate before CAPA, in order: clerical/transcription ->
    IQC on the PT day -> right peer/method group -> reagent lot / calibration drift -> competency;
    a single miss != systematic; commutability of PT material; never rerun-until-pass; never PT referral;
    "fail" criteria differ by scheme)
  - LAB-MANAGEMENT digest §2/§3 (bias formula; EQA fail != instrument broken)
  - 510403 Clinical Laboratory Practice digest §2.7 (SDI = (lab - group mean) / group SD; teaching bands
    excellent <= 0.5, satisfactory <= 2.0, serious > 3.0 - the band 2.0-3.0 is not named there)
The pass/fail criterion is the scheme's -> --fail-sdi and/or --fail-bias-pct (or per-row columns
limit_sdi / limit_bias_pct). ADVISORY ONLY: the EQA provider's report and the lab's QA lead decide.

Input CSV header: analyte,result,peer_mean[,peer_sd][,round][,limit_sdi][,limit_bias_pct]

Examples
  python eqa_eval.py ../data/eqa_example.csv --fail-sdi 2
  python eqa_eval.py ../data/eqa_example.csv --fail-bias-pct 10 --json
"""
import argparse
import csv
import json
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

INVESTIGATION = [
    "1 clerical / transcription: units, decimal, swapped samples, result entered in the wrong field (most common)",
    "2 IQC on the day the PT sample was run: did it pass?",
    "3 peer / method group: compared with your own method/instrument group? wrong group = false 'bias'",
    "4 reagent lot / calibration drift around that date",
    "5 competency / procedure of the person who ran it",
]
NEVER = ["rerun until it passes without finding a root cause",
         "share or compare PT results with another lab (PT referral) - serious nonconformity in many schemes"]
ALSO = "commutability: PT material may not behave like patient samples - read the method-specific target first"


def num(x):
    return None if x in (None, "") else float(x)


def bias_pct(result, peer_mean):
    return (result - peer_mean) / peer_mean * 100.0


def sdi(result, peer_mean, peer_sd):
    return (result - peer_mean) / peer_sd


def sdi_band(v):
    a = abs(v)
    if a <= 0.5:
        return "excellent (<=0.5)"
    if a <= 2.0:
        return "satisfactory (<=2.0)"
    if a > 3.0:
        return "serious (>3.0)"
    return "2.0-3.0: not banded in 510403 §2.7 - use the scheme criterion"


def evaluate(rows, fail_sdi=None, fail_bias=None):
    out = []
    for r in rows:
        res, pm, psd = num(r["result"]), num(r["peer_mean"]), num(r.get("peer_sd"))
        b = bias_pct(res, pm)
        s = sdi(res, pm, psd) if psd else None
        lim_s = num(r.get("limit_sdi")) if r.get("limit_sdi") else fail_sdi
        lim_b = num(r.get("limit_bias_pct")) if r.get("limit_bias_pct") else fail_bias
        reasons, judged = [], False
        if lim_s is not None and s is not None:
            judged = True
            if abs(s) > lim_s:
                reasons.append("|SDI| %.2f > %g" % (abs(s), lim_s))
        if lim_b is not None:
            judged = True
            if abs(b) > lim_b:
                reasons.append("|bias| %.1f%% > %g%%" % (abs(b), lim_b))
        status = ("FLAG" if reasons else "ok") if judged else "NO CRITERION"
        out.append({"analyte": r["analyte"], "round": r.get("round", ""), "result": res, "peer_mean": pm,
                    "peer_sd": psd, "bias_pct": b, "sdi": s, "sdi_band": sdi_band(s) if s is not None else None,
                    "status": status, "reasons": reasons})
    flagged = [x for x in out if x["status"] == "FLAG"]
    pattern = []
    by_round, by_analyte = {}, {}
    for x in flagged:
        by_round.setdefault(x["round"], []).append(x)
        by_analyte.setdefault(x["analyte"], []).append(x)
    for rd, xs in by_round.items():
        if len(xs) >= 2:
            signs = {x["bias_pct"] > 0 for x in xs}
            pattern.append("round %s: %d analytes flagged%s" % (rd or "-", len(xs), " in the same direction" if len(signs) == 1 else ""))
    for an, xs in by_analyte.items():
        if len({x["round"] for x in xs}) >= 2:
            pattern.append("%s flagged in %d rounds" % (an, len({x["round"] for x in xs})))
    if not flagged:
        kind = "no flag" if all(x["status"] != "NO CRITERION" for x in out) else "some rows have NO CRITERION"
    elif pattern:
        kind = "PATTERN -> treat as possible systematic problem: " + "; ".join(pattern)
    else:
        kind = "single miss -> investigate, but do not assume a systematic fault"
    return {"rows": out, "flagged": len(flagged), "summary": kind,
            "investigation": INVESTIGATION if flagged else [], "never": NEVER if flagged else [],
            "also_check": ALSO if flagged else ""}


def main(argv=None):
    try:  # never crash a non-UTF-8 console (e.g. Thai cp874) on the section sign / Thai text
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--fail-sdi", type=float, help="scheme criterion: |SDI| above this = flag")
    ap.add_argument("--fail-bias-pct", type=float, help="scheme criterion: |bias %%| above this = flag")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        rows = [{k.strip().lower(): (v or "").strip() for k, v in r.items()}
                for r in csv.DictReader(ln for ln in f if not ln.lstrip().startswith("#"))]
    res = evaluate(rows, a.fail_sdi, a.fail_bias_pct)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("bias% = (lab - peer mean) / peer mean x 100 ; SDI = (lab - peer mean) / peer SD")
    print("%-12s %-6s %-9s %-9s %-8s %-7s %-12s %s" % ("analyte", "round", "result", "peer", "bias%", "SDI", "status", "band / reason"))
    for x in res["rows"]:
        print("%-12s %-6s %-9g %-9g %-+8.2f %-7s %-12s %s" % (
            x["analyte"], x["round"] or "-", x["result"], x["peer_mean"], x["bias_pct"],
            "-" if x["sdi"] is None else "%+.2f" % x["sdi"], x["status"],
            "; ".join(x["reasons"]) or (x["sdi_band"] or "")))
    print("-" * 70)
    print("SUMMARY: " + res["summary"])
    if res["investigation"]:
        print("INVESTIGATE BEFORE CAPA (in this order):")
        for s in res["investigation"]:
            print("  " + s)
        print("  ALSO: " + res["also_check"])
        for s in res["never"]:
            print("  NEVER: " + s)
    print("ADVISORY: decision support only - the EQA provider's evaluation and the lab QA lead decide.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
