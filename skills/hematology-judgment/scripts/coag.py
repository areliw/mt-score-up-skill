#!/usr/bin/env python3
"""coag - screening-coagulation pattern, mixing-test read, and citrate volume for high Hct.

Black-box tool for hematology-judgment Fork 6 and trap #9 / #10. Run --help, not the source.
ADVISORY ONLY: patterns point to a differential; the lab SOP, factor assays and the physician decide.

  pattern     PT / aPTT / TT, each given as a value with the lab's upper limit (--pt-uln ...) or as the
              word long|normal. Reference ranges are reagent/lab specific -> NO default ULN.
              Table (card Fork 6; 503402 digest §6 "Pattern แปลผล"):
                PT long alone                -> FVII: early warfarin / vitamin K deficiency / liver
                aPTT long alone              -> FVIII/IX (hemophilia A/B), FXI/FXII, vWD, heparin, lupus anticoagulant
                PT + aPTT long, TT normal    -> FX / FV / FII, liver disease, vitamin K deficiency
                PT + aPTT + TT long          -> DIC / afibrinogenemia (dysfibrinogenemia) -> fibrinogen + D-dimer
                all normal BUT bleeding      -> mild factor deficiency (>5%), FXIII deficiency, fibrinolysis, mild vWD
                                                (card trap #9: a normal screen does not end the work-up)
              PT or aPTT long -> mixing test 1:1 with normal pooled plasma (card Fork 6)
  mixing      corrected -> factor deficiency; not corrected -> inhibitor (FVIII inhibitor / lupus anticoagulant)
              (card Fork 6; 503402 §6). "Corrected" needs a lab criterion, supplied by you:
                --uln          mix result <= lab upper limit of the reference interval = corrected
                --patient --npp --rosner-cutoff   Rosner index = (mix - NPP) / patient x 100;
                               index <= cutoff = corrected (index: Rosner et al., Thromb Haemost 1987; cutoff = lab's)
  citrate-hct only when Hct > 55% (card trap #10; 503402 §6):
                digest  citrate mL = std_citrate_mL x (100 - Hct) / 55       (503402 §6, std 0.5 mL teaching default)
                clsi    citrate mL = 0.00185 x (100 - Hct) x blood mL         (CLSI H21 form; published variant)

Examples
  python coag.py pattern --pt 18.2 --pt-uln 14.5 --aptt 31 --aptt-uln 35 --tt normal
  python coag.py pattern --pt normal --aptt normal --bleeding
  python coag.py mixing --mix 34.1 --uln 35
  python coag.py mixing --mix 52 --patient 68 --npp 30 --rosner-cutoff 15
  python coag.py citrate-hct --hct 65
  python coag.py citrate-hct --hct 65 --formula clsi --blood-ml 4.5
"""
import argparse
import json
import sys

ADVISORY = ("ADVISORY: decision support only - confirm with the lab SOP, factor assays / D-dimer as indicated, "
            "and the responsible MT/physician.")

WORDS_LONG = {"long", "prolonged", "high", "l"}
WORDS_NORMAL = {"normal", "n", "ok"}

TABLE = {
    ("L", "N"): "PT long alone -> FVII: early warfarin / vitamin K deficiency / liver disease",
    ("N", "L"): ("aPTT long alone -> FVIII/IX (hemophilia A/B), FXI/FXII, vWD, heparin, lupus anticoagulant"),
}


def status(value, uln, name):
    """Return 'L', 'N' or None (not done). value may be a number (needs uln) or a word."""
    if value is None:
        return None
    s = str(value).strip().lower()
    if s in WORDS_LONG:
        return "L"
    if s in WORDS_NORMAL:
        return "N"
    try:
        v = float(s)
    except ValueError:
        raise ValueError("%s: give a number or long/normal, got %r" % (name, value))
    if uln is None:
        raise ValueError("%s given as a number: also pass --%s-uln (the lab's upper limit; no default)"
                         % (name, name.lower()))
    return "L" if v > uln else "N"


def pattern(pt, aptt, tt=None, bleeding=False, pt_uln=None, aptt_uln=None, tt_uln=None):
    p, a, t = status(pt, pt_uln, "PT"), status(aptt, aptt_uln, "APTT"), status(tt, tt_uln, "TT")
    if p is None or a is None:
        raise ValueError("PT and aPTT are both required")
    nxt = []
    if p == "L" and a == "L":
        if t is None:
            read = ("PT + aPTT long, TT not done -> run TT/fibrinogen to split common pathway / liver / "
                    "vitamin K (TT normal) from DIC / afibrinogenemia (TT long)")
        elif t == "N":
            read = "PT + aPTT long, TT normal -> FX / FV / FII deficiency, liver disease, vitamin K deficiency"
        else:
            read = ("PT + aPTT + TT long -> DIC / afibrinogenemia (dysfibrinogenemia) "
                    "-> fibrinogen + D-dimer now")
    elif (p, a) in TABLE:
        read = TABLE[(p, a)]
        if t == "L":
            read += " [TT also long: combination not in the card table -> consult]"
    else:  # both normal
        if t == "L":
            read = ("PT and aPTT normal, TT long: not in the card pattern table; 503402 §6 TT row lists "
                    "heparin / DIC / afibrinogenemia -> consult")
        elif bleeding:
            read = ("normal screen BUT the patient bleeds -> do NOT stop: mild factor deficiency (>5%), "
                    "FXIII deficiency, fibrinolysis disorder, mild vWD -> specific assays (card trap #9)")
        else:
            read = "no screening-test pattern (PT/aPTT normal, no bleeding reported)"
    if p == "L" or a == "L":
        nxt.append("mixing test 1:1 with normal pooled plasma -> corrected = deficiency, not corrected = inhibitor")
    if t == "L" or (p == "L" and a == "L"):
        nxt.append("fibrinogen + D-dimer if DIC is possible (APL / sepsis / snake bite)")
    return {"inputs": {"PT": pt, "aPTT": aptt, "TT": tt, "bleeding": bleeding},
            "status": {"PT": p, "aPTT": a, "TT": t or "not done"},
            "pattern": read, "next": nxt}


def mixing(mix, uln=None, patient=None, npp=None, rosner_cutoff=None):
    calls = {}
    if uln is not None:
        calls["within_reference"] = {"criterion": "mix <= ULN %g" % uln, "corrected": mix <= uln}
    if None not in (patient, npp, rosner_cutoff):
        if patient <= 0:
            raise ValueError("--patient must be > 0")
        idx = (mix - npp) / patient * 100
        calls["rosner"] = {"criterion": "Rosner index <= %g" % rosner_cutoff, "index": idx,
                           "corrected": idx <= rosner_cutoff}
    elif any(x is not None for x in (patient, npp, rosner_cutoff)):
        raise ValueError("Rosner index needs all of --patient, --npp and --rosner-cutoff")
    if not calls:
        raise ValueError("give a lab criterion: --uln, or --patient --npp --rosner-cutoff")
    verdicts = {c["corrected"] for c in calls.values()}
    if len(verdicts) > 1:
        verdict = "DISCORDANT criteria -> follow the lab SOP (repeat / incubated mix / specific assays)"
    elif verdicts.pop():
        verdict = "CORRECTED -> factor deficiency -> factor assays"
    else:
        verdict = "NOT CORRECTED -> inhibitor (FVIII inhibitor / lupus anticoagulant) -> inhibitor work-up"
    return {"inputs": {"mix": mix, "uln": uln, "patient": patient, "npp": npp}, "criteria": calls,
            "verdict": verdict}


def citrate_hct(hct, formula="digest", std_citrate_ml=0.5, blood_ml=4.5, threshold=55.0):
    if not 0 < hct < 100:
        raise ValueError("Hct must be a percentage between 0 and 100")
    if hct <= threshold:
        return {"inputs": {"hct_pct": hct}, "adjust": False,
                "verdict": "Hct <= %g%% -> standard 9:1 blood:citrate tube, no adjustment" % threshold}
    if formula == "digest":
        ml = std_citrate_ml * (100 - hct) / 55
        expr = "%g x (100 - %g) / 55" % (std_citrate_ml, hct)
        ref = std_citrate_ml
    else:
        ml = 0.00185 * (100 - hct) * blood_ml
        expr = "0.00185 x (100 - %g) x %g" % (hct, blood_ml)
        ref = None
    res = {"inputs": {"hct_pct": hct, "formula": formula}, "adjust": True,
           "citrate_ml": ml, "expression": expr,
           "verdict": ("Hct > %g%% -> plasma volume is low; use %.3f mL citrate (less than standard) "
                       "or the result (PT/aPTT) is falsely prolonged" % (threshold, ml))}
    if ref is not None:
        res["remove_from_standard_ml"] = ref - ml
    return res


def _print(res):
    for k, v in res.items():
        if isinstance(v, float):
            v = "%.4f" % v
        elif isinstance(v, list):
            if not v:
                continue
            v = "\n" + "\n".join("    - " + str(x) for x in v)
        elif isinstance(v, dict) and k == "criteria":
            v = "\n" + "\n".join("    - %s: %s" % (n, c) for n, c in v.items())
        print("%-24s %s" % (k, v))
    print(ADVISORY)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pattern", help="PT/aPTT/TT pattern -> differential + next step")
    p.add_argument("--pt", required=True, help="seconds, or long/normal")
    p.add_argument("--aptt", required=True, help="seconds, or long/normal")
    p.add_argument("--tt", help="seconds, or long/normal (optional)")
    p.add_argument("--pt-uln", type=float, help="lab upper limit, seconds")
    p.add_argument("--aptt-uln", type=float, help="lab upper limit, seconds")
    p.add_argument("--tt-uln", type=float, help="lab upper limit, seconds")
    p.add_argument("--bleeding", action="store_true", help="patient has clinically significant bleeding")
    p = sub.add_parser("mixing", help="read a 1:1 mixing study")
    p.add_argument("--mix", type=float, required=True, help="clotting time of the 1:1 mix (s)")
    p.add_argument("--uln", type=float, help="lab upper limit of the reference interval (s)")
    p.add_argument("--patient", type=float, help="patient plasma clotting time (s), for the Rosner index")
    p.add_argument("--npp", type=float, help="normal pooled plasma clotting time (s), for the Rosner index")
    p.add_argument("--rosner-cutoff", type=float, help="lab cut-off for the Rosner index")
    p = sub.add_parser("citrate-hct", help="citrate volume when Hct > 55%%")
    p.add_argument("--hct", type=float, required=True)
    p.add_argument("--formula", choices=["digest", "clsi"], default="digest")
    p.add_argument("--std-citrate-ml", type=float, default=0.5, help="teaching default 0.5 mL (503402 §6)")
    p.add_argument("--blood-ml", type=float, default=4.5, help="blood volume for the clsi form (default 4.5)")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "pattern":
            res = pattern(a.pt, a.aptt, a.tt, a.bleeding, a.pt_uln, a.aptt_uln, a.tt_uln)
        elif a.cmd == "mixing":
            res = mixing(a.mix, a.uln, a.patient, a.npp, a.rosner_cutoff)
        else:
            res = citrate_hct(a.hct, a.formula, a.std_citrate_ml, a.blood_ml)
    except ValueError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        res["advisory"] = ADVISORY
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        _print(res)
    return 0


if __name__ == "__main__":
    sys.exit(main())
