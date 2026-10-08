#!/usr/bin/env python3
"""serology_algo — walk a confirm-before-report serology algorithm one step at a time.

Black-box tool for immunoassay-judgment. Run --help first; read the source only if a step looks wrong.
Sources:
  syphilis  traditional = NTT screen -> TT confirm; reverse = TT screen -> NTT (+ titer);
            TT+ NTT- -> early or treated-old -> a SECOND, different TT; BFP (pregnancy/SLE/HIV/TB);
            prozone gives a false-negative NTT when antibody is very high
            (card FORK 2 syphilis line + trap #1/#4; 506202 Immunology digest §14)
  hiv       4th-gen Ag/Ab screen -> confirm with assays of a different principle/antigen -> discordant or
            acute -> NAT; never report positive from one reactive screen; < 24 months -> NAT not antibody
            (card FORK 2 HIV line + trap #3; IMMUNODIAGNOSTIC digest §5.4; card says 18-24 months)
            The NUMBER of tests is set by the national algorithm (TH = serial 3 per card) -> --n-tests.
  ppv       PPV after 1..k serial positive tests from prevalence/sensitivity/specificity, assuming the
            tests err independently (IMMUNODIAGNOSTIC digest §5.4 worked example; card FORK 3)
ADVISORY ONLY: reporting follows the national algorithm, the lab SOP and an authorised signatory.

Results: R (reactive) / NR (non-reactive) / na (not done yet)

Examples
  python serology_algo.py syphilis --algorithm reverse --tt R --ntt NR
  python serology_algo.py syphilis --algorithm traditional --ntt NR --suspicion high
  python serology_algo.py hiv --n-tests 3 --results R R NR
  python serology_algo.py hiv --n-tests 3 --results R --age-months 9
  python serology_algo.py ppv --prevalence 0.0005 --sens 0.995 --spec 0.99 --tests 3
"""
import argparse
import json
import sys

RES = {"r": "R", "reactive": "R", "pos": "R", "+": "R",
       "nr": "NR", "nonreactive": "NR", "neg": "NR", "-": "NR",
       "na": "na", "": "na", "nd": "na"}


def norm(v):
    key = (v or "").strip().lower()
    if key not in RES:
        raise ValueError("result %r: use R / NR / na" % v)
    return RES[key]


def step(status, next_step, reportable=False, provenance="", notes=None):
    return {"status": status, "next_step": next_step, "reportable_as_positive": reportable,
            "provenance": provenance, "notes": notes or []}


# ---------------------------------------------------------------- syphilis
def syphilis(algorithm, ntt="na", tt="na", tt2="na", suspicion="routine"):
    notes = []
    if suspicion == "high":
        notes.append("clinical suspicion high: a non-reactive NTT may be PROZONE -> dilute and retest (card trap #1)")
    if algorithm == "traditional":
        if ntt == "na":
            return step("START", "run NTT screen (RPR/VDRL)", provenance="card FORK 2", notes=notes)
        if ntt == "NR":
            nxt = ("dilute the NTT and retest (prozone), and consider a TT" if suspicion == "high"
                   else "report non-reactive per SOP; recent exposure -> repeat later (window)")
            return step("NON-REACTIVE NTT (not a rule-out if clinically suspicious)", nxt,
                        provenance="card FORK 2 + iron rule #2", notes=notes)
        if tt == "na":
            return step("NTT REACTIVE - unconfirmed", "run a TT (TPHA/TPPA/FTA); do NOT report positive yet",
                        provenance="card iron rule #1 + FORK 2", notes=notes)
        if tt == "R":
            return step("NTT + TT REACTIVE: consistent with syphilis (current or past)",
                        "report per SOP; the NTT titer is the baseline for the fourfold rule",
                        reportable=True, provenance="card FORK 2", notes=notes)
        return step("NTT REACTIVE, TT NON-REACTIVE: biological false-positive NTT likely",
                    "do not report syphilis; clinical correlation (pregnancy/SLE/HIV/TB cause BFP)",
                    provenance="card FORK 2 (BFP) + trap #4", notes=notes)
    # reverse
    if tt == "na":
        return step("START", "run TT screen (CMIA/TPHA/TPPA)", provenance="card FORK 2", notes=notes)
    if tt == "NR":
        return step("NON-REACTIVE TT", "report non-reactive per SOP; recent exposure -> repeat later (window)",
                    provenance="card FORK 2 + trap #3", notes=notes)
    if ntt == "na":
        return step("TT REACTIVE - unconfirmed", "run NTT with titer; do NOT report positive from one screen",
                    provenance="card FORK 2 reverse", notes=notes)
    if ntt == "R":
        return step("TT + NTT REACTIVE: consistent with syphilis (untreated or recently treated)",
                    "report per SOP; NTT titer = baseline for follow-up (fourfold rule)",
                    reportable=True, provenance="card FORK 2 reverse", notes=notes)
    if tt2 == "na":
        return step("DISCORDANT: TT+ / NTT-", "run a SECOND, different TT (e.g. TPPA) before any conclusion",
                    provenance="card FORK 2 (TT+ NTT- -> early or treated-old -> second TT)", notes=notes)
    if tt2 == "R":
        return step("TT+ / NTT- / TT2+: past (treated) syphilis or early syphilis",
                    "history of treatment + clinical stage decide; lab reports the results, not the stage",
                    reportable=True, provenance="card FORK 2 + 506202 §14 (lab reports as found)", notes=notes)
    return step("TT+ / NTT- / TT2-: first TT not confirmed (likely false-reactive) [ทั่วไป]",
                "do not report syphilis; recent exposure -> repeat later",
                provenance="second-TT adjudication (card FORK 2) - false-reactive label is general teaching",
                notes=notes)


# ---------------------------------------------------------------- HIV
def hiv(results, n_tests, age_months=None):
    results = [r for r in results if r != "na"]
    if n_tests < 2:
        raise ValueError("--n-tests must be >= 2: one reactive screen is never reportable")
    if age_months is not None and age_months < 24:
        return step("ANTIBODY TESTS NOT DIAGNOSTIC (maternal IgG crosses the placenta)",
                    "use NAT (HIV DNA/RNA PCR)", provenance="IMMUNODIAGNOSTIC §5.4 (< 24 months); card: 18-24 months")
    if not results:
        return step("START", "run 4th-gen Ag/Ab screen (A1)", provenance="card FORK 2 HIV")
    if results[0] == "NR":
        return step("NON-REACTIVE screen",
                    "report per SOP; exposure inside the window (4th-gen ~2-3 weeks) -> repeat later",
                    provenance="card trap #3 (window period)")
    if "NR" in results[1:]:
        return step("DISCORDANT: screen reactive, a confirm test non-reactive",
                    "do NOT report positive; resolve per the national algorithm (card: discordant/acute -> NAT)",
                    provenance="card FORK 2 HIV + IMMUNODIAGNOSTIC §5.4")
    if len(results) < n_tests:
        return step("REACTIVE so far (%d of %d tests)" % (len(results), n_tests),
                    "run test A%d: different principle/antigen from the previous ones; do NOT report yet"
                    % (len(results) + 1), provenance="card iron rule #1 + IMMUNODIAGNOSTIC §5.4")
    return step("REACTIVE on all %d tests of the algorithm" % n_tests,
                "report per national guideline/SOP (TH: กรมควบคุมโรค serial algorithm)", reportable=True,
                provenance="card FORK 2 HIV + trap #3")


# ---------------------------------------------------------------- PPV
def ppv_after_positive(prior, sens, spec):
    tp = sens * prior
    fp = (1 - spec) * (1 - prior)
    return tp / (tp + fp)


def ppv_serial(prevalence, tests):
    """tests: list of (sens, spec). Returns PPV after each consecutive positive result."""
    if not 0 < prevalence < 1:
        raise ValueError("prevalence must be between 0 and 1 (e.g. 0.0005 for 0.05%)")
    rows, prior = [], prevalence
    for k, (se, sp) in enumerate(tests, 1):
        if not (0 < se <= 1 and 0 < sp <= 1):
            raise ValueError("sensitivity/specificity must be fractions in (0, 1]")
        post = ppv_after_positive(prior, se, sp)
        rows.append({"test": k, "sens": se, "spec": sp, "prior": prior, "ppv": post})
        prior = post
    return {"prevalence": prevalence, "rows": rows,
            "assumption": "tests err independently (different principle/antigen); correlated tests give less"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("syphilis")
    p.add_argument("--algorithm", choices=["traditional", "reverse"], required=True)
    p.add_argument("--ntt", default="na")
    p.add_argument("--tt", default="na")
    p.add_argument("--tt2", default="na", help="second, different treponemal test (reverse algorithm)")
    p.add_argument("--suspicion", choices=["routine", "high"], default="routine")
    p = sub.add_parser("hiv")
    p.add_argument("--n-tests", type=int, required=True, help="tests the national algorithm requires (TH: 3)")
    p.add_argument("--results", nargs="*", default=[], help="R/NR in testing order, screen first")
    p.add_argument("--age-months", type=float)
    p = sub.add_parser("ppv")
    p.add_argument("--prevalence", type=float, required=True, help="fraction, e.g. 0.0005 = 0.05%%")
    p.add_argument("--sens", type=float, help="fraction, same for every test")
    p.add_argument("--spec", type=float, help="fraction, same for every test")
    p.add_argument("--tests", type=int, default=1, help="number of serial positive tests")
    p.add_argument("--test", action="append", help="SENS,SPEC per test, in order (overrides --sens/--spec)")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "syphilis":
            res = syphilis(a.algorithm, norm(a.ntt), norm(a.tt), norm(a.tt2), a.suspicion)
        elif a.cmd == "hiv":
            res = hiv([norm(r) for r in a.results], a.n_tests, a.age_months)
        else:
            if a.test:
                tests = [tuple(float(x) for x in t.split(",")) for t in a.test]
            elif a.sens is not None and a.spec is not None:
                tests = [(a.sens, a.spec)] * a.tests
            else:
                raise ValueError("give --sens and --spec, or --test SENS,SPEC")
            res = ppv_serial(a.prevalence, tests)
    except ValueError as e:
        ap.error(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "ppv":
        print("prevalence %.4g%%   (%s)" % (res["prevalence"] * 100, res["assumption"]))
        print("%-6s %-8s %-8s %-12s %s" % ("test", "sens", "spec", "prior", "PPV if positive"))
        for r in res["rows"]:
            print("%-6d %-8.4g %-8.4g %-12.4f %.4f  (%.1f%%)" % (r["test"], r["sens"], r["spec"], r["prior"],
                                                               r["ppv"], r["ppv"] * 100))
    else:
        print("STATUS: %s   [%s]" % (res["status"], res["provenance"]))
        print("NEXT:   %s" % res["next_step"])
        print("reportable as positive: %s" % ("yes (per SOP)" if res["reportable_as_positive"] else "NO"))
        for n in res["notes"]:
            print("note:  ", n)
    print("ADVISORY: decision support only - confirm with the national algorithm, lab SOP and an authorised signatory.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
