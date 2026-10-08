#!/usr/bin/env python3
"""pcr_call — call each well of a real-time PCR run POSITIVE / NEGATIVE / INVALID, controls first.

Black-box tool for molecular-judgment. Run --help first; read the source only if a call looks wrong.
Rules come from the skill card and the 510415 Molecular Biology digest:
  run gate   positive control + NTC/negative control must be present; any NTC/negative-control
             amplification = contamination -> WHOLE RUN INVALID; positive control not amplified ->
             reaction failure -> WHOLE RUN INVALID   (card "3 ด่าน" #2, Fork 4, Fork 6; digest §9)
  specimen   heparin tube -> reject (inhibits PCR)   (card ด่าน #1, trap 1; digest §9 pre-analytical)
  sample     target detected -> POSITIVE; target not detected + internal control detected -> NEGATIVE;
             target AND internal control not detected -> INVALID (inhibition / reaction failure),
             never "negative"; no internal control at all -> NO-CALL for a negative
             (card iron rule #1, Fork 4, Fork 5; digest §9 "internal/amplification control กัน false-negative")
  SYBR       a positive needs a single melt peak at the expected Tm; else non-specific/primer-dimer
             (card Fork 3/4, trap "SYBR/HRM โดยไม่ดู melt curve"; digest §8)
Ct cut-off, IC cut-off, expected Tm and Tm tolerance are ASSAY/LAB values -> arguments, never built in.
ADVISORY ONLY: release follows the assay IFU, the lab SOP and an authorised signatory.

CSV columns (header required): well, role, target_ct, ic_ct  [, tube, melt_tm, melt_peaks]
  role       sample | ntc | neg | pos
  target_ct  number, or blank / undet / - when no amplification (same for ic_ct)
  ic_ct      leave the whole column out only if the assay has no internal control (negatives become NO-CALL)

Examples
  python pcr_call.py ../data/qpcr_run_teaching.csv --ct-cutoff 38
  python pcr_call.py run.csv --ct-cutoff 40 --ic-cutoff 35
  python pcr_call.py sybr.csv --ct-cutoff 35 --chemistry sybr --melt-tm 82.5 --melt-tol 1.0
  python pcr_call.py run.csv --ct-cutoff 38 --json
"""
import argparse
import csv
import json
import sys

NOT_DETECTED = {"", "undet", "undetermined", "-", "na", "n/a", "nd", "no ct", "noct"}


def parse_ct(v):
    t = (v or "").strip().lower()
    if t in NOT_DETECTED:
        return None
    return float(t)


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        cols = [c.strip().lower() for c in reader.fieldnames or []]
        rows = list(reader)
    wells = []
    for r in rows:
        r = {k.strip().lower(): (v or "").strip() for k, v in r.items()}
        peaks = r.get("melt_peaks", "")
        wells.append({"well": r["well"], "role": r["role"].lower(), "target_ct": parse_ct(r.get("target_ct")),
                      "ic_ct": parse_ct(r.get("ic_ct")) if "ic_ct" in cols else "absent",
                      "tube": r.get("tube", "").lower(),
                      "melt_tm": float(r["melt_tm"]) if r.get("melt_tm") else None,
                      "melt_peaks": int(peaks) if peaks else None})
    return wells


def detected(ct, cutoff):
    return ct is not None and ct != "absent" and ct <= cutoff


def run_gate(wells):
    """Card ด่าน #2 + Fork 6: controls present, NTC clean, positive control amplified."""
    reasons = []
    ntcs = [w for w in wells if w["role"] in ("ntc", "neg")]
    pcs = [w for w in wells if w["role"] == "pos"]
    if not ntcs:
        reasons.append("no NTC/negative control in the run (controls incomplete -> stop)")
    if not pcs:
        reasons.append("no positive control in the run (controls incomplete -> stop)")
    for w in ntcs:
        if w["target_ct"] is not None:
            reasons.append("%s (%s) amplified at Ct %.2f -> contamination" % (w["well"], w["role"], w["target_ct"]))
    return reasons


def call_sample(w, ct_cutoff, ic_cutoff, chemistry="probe", melt_tm=None, melt_tol=None):
    """Returns (call, reason) for one patient well. Run-level validity is checked separately."""
    if w["tube"] == "heparin":
        return "REJECT SPECIMEN", "heparin tube inhibits PCR -> recollect in EDTA/ACD"
    target = detected(w["target_ct"], ct_cutoff)
    ic_absent = w["ic_ct"] == "absent"
    ic = (not ic_absent) and detected(w["ic_ct"], ic_cutoff)
    if target:
        if chemistry == "sybr":
            if w["melt_peaks"] is None and w["melt_tm"] is None:
                return "REVIEW", "SYBR positive without melt data -> cannot exclude primer-dimer/non-specific"
            if w["melt_peaks"] is not None and w["melt_peaks"] > 1:
                return "REVIEW", "multiple melt peaks -> non-specific product, not a true positive yet"
            if melt_tm is not None and w["melt_tm"] is not None and abs(w["melt_tm"] - melt_tm) > melt_tol:
                return "REVIEW", "melt Tm %.2f vs expected %.2f +/- %.2f -> non-specific product" % (
                    w["melt_tm"], melt_tm, melt_tol)
        if ic_absent or ic:
            return "POSITIVE", "target Ct %.2f <= cut-off %.2f" % (w["target_ct"], ct_cutoff)
        return "POSITIVE (check IC)", ("target detected but internal control not detected - card does not cover "
                                       "this case; follow the assay IFU")
    late = ("" if w["target_ct"] is None else
            " (late amplification Ct %.2f beyond cut-off - handle per IFU)" % w["target_ct"])
    if ic_absent:
        return "NO-CALL", "no internal control -> 'negative' cannot be told from a failed reaction" + late
    if ic:
        return "NEGATIVE", "target not detected, internal control Ct %.2f valid%s" % (w["ic_ct"], late)
    return "INVALID", "target AND internal control not detected -> inhibition/reaction failure: repeat/re-extract"


def evaluate(wells, ct_cutoff, ic_cutoff=None, chemistry="probe", melt_tm=None, melt_tol=None):
    ic_cutoff = ct_cutoff if ic_cutoff is None else ic_cutoff
    if chemistry == "sybr" and melt_tm is not None and melt_tol is None:
        raise ValueError("--melt-tm needs --melt-tol (assay value)")
    run_reasons = run_gate(wells)
    pcs = [w for w in wells if w["role"] == "pos"]
    for w in pcs:
        if not detected(w["target_ct"], ct_cutoff):
            run_reasons.append("positive control %s not amplified within cut-off -> reaction failure" % w["well"])
    run_valid = not run_reasons
    out = []
    for w in wells:
        if w["role"] != "sample":
            continue
        call, why = call_sample(w, ct_cutoff, ic_cutoff, chemistry, melt_tm, melt_tol)
        reportable = run_valid and call in ("POSITIVE", "NEGATIVE")
        if not run_valid and call != "REJECT SPECIMEN":
            why = "run invalid - " + why
        out.append({"well": w["well"], "target_ct": w["target_ct"],
                    "ic_ct": None if w["ic_ct"] == "absent" else w["ic_ct"],
                    "call": call if run_valid or call == "REJECT SPECIMEN" else "RUN INVALID",
                    "sample_level_call": call, "reportable": reportable, "reason": why})
    return {"ct_cutoff": ct_cutoff, "ic_cutoff": ic_cutoff, "chemistry": chemistry,
            "run_valid": run_valid, "run_reasons": run_reasons, "samples": out}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--ct-cutoff", type=float, required=True, help="assay positivity cut-off (IFU/validation)")
    ap.add_argument("--ic-cutoff", type=float, help="internal-control valid Ct limit (default = --ct-cutoff)")
    ap.add_argument("--chemistry", choices=["probe", "sybr"], default="probe")
    ap.add_argument("--melt-tm", type=float, help="expected product Tm (SYBR)")
    ap.add_argument("--melt-tol", type=float, help="allowed Tm deviation (SYBR)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        res = evaluate(load(a.csv), a.ct_cutoff, a.ic_cutoff, a.chemistry, a.melt_tm, a.melt_tol)
    except (ValueError, KeyError) as e:
        ap.error(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("cut-off Ct %.2f  IC cut-off %.2f  chemistry %s" % (res["ct_cutoff"], res["ic_cutoff"], res["chemistry"]))
    print("RUN: %s" % ("VALID" if res["run_valid"] else "INVALID"))
    for r in res["run_reasons"]:
        print("   - %s" % r)
    fmt = lambda v: "-" if v is None else "%.2f" % v  # noqa: E731
    print("%-8s %-8s %-8s %-20s %s" % ("well", "target", "IC", "call", "reason"))
    for s in res["samples"]:
        print("%-8s %-8s %-8s %-20s %s" % (s["well"], fmt(s["target_ct"]), fmt(s["ic_ct"]), s["call"], s["reason"]))
    print("-" * 70)
    print("reportable now: %d of %d sample wells" % (sum(s["reportable"] for s in res["samples"]), len(res["samples"])))
    print("ADVISORY: decision support only - confirm with the assay IFU, lab SOP and an authorised signatory.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
