#!/usr/bin/env python3
"""tox_calc - cholinesterase depression, TDM sampling time, and specimen-tube rules.

Black-box tool for toxicology-judgment. Run --help first. Sources:
  che       % depression from the patient's own baseline = (baseline - current) / baseline x 100.
            OP poisoning = ChE down > 50 % from baseline (card Fork 5; owner digest 510414 section 6).
            Plasma (butyryl) ChE also falls in liver failure / malnutrition (false low) -> confirm with
            RBC-AChE + baseline. Without a baseline you may compare with YOUR lab's lower reference
            (--ref-low); the card's "~3,500-8,000 U/L" is illustrative and is NOT built in.
  tdm       sample at steady state (card Fork 6; 510414 section 3). Fraction of steady state after
            time t on a fixed regimen = 1 - 0.5^(t / t_half) (first-order kinetics, standard
            pharmacokinetics); "reached" is judged at --ss-halflives (default 5 half-lives = 96.9 %,
            a textbook convention - some SOPs use 4). Use the PATIENT's half-life (longer in renal /
            hepatic impairment). Trough = drawn before the next dose; the acceptable window is your
            SOP's (--trough-window); peak timing is drug/route-specific and is not judged here.
  specimen  phenytoin: gel separator absorbs the drug -> plain tube; tacrolimus / cyclosporine ->
            whole blood (510414 section 3, card Fork 6 + trap list); ethanol / toluene / volatile /
            cyanide -> whole blood in a SEALED tube, no gel (card Fork 2 + trap list; 510414 section 2).
ADVISORY ONLY.

Examples
  python tox_calc.py che --current 2500 --baseline 6000 --type plasma
  python tox_calc.py tdm --half-life 6 --since-start 30 --interval 12 --since-last-dose 11.75 \
      --trough-window 0.5 --order trough
  python tox_calc.py specimen --analyte phenytoin --tube gel
"""
import argparse
import json
import sys

TYPE_NOTE = {
    "plasma": "plasma (butyryl) ChE: sensitive for ACUTE exposure but falls in liver failure / malnutrition "
              "(false low) -> confirm with RBC-AChE + baseline",
    "rbc": "RBC-AChE: same enzyme as NMJ/CNS -> target-site effect, chronic/cumulative, recovers slowly",
}


def percent_depression(current, baseline):
    """Percent FALL from the patient's own baseline (not percent remaining)."""
    if baseline <= 0:
        raise ValueError("baseline must be > 0")
    return (baseline - current) / baseline * 100


def che(current, baseline=None, che_type=None, threshold=50.0, ref_low=None):
    res = {"current": current, "type": che_type, "type_note": TYPE_NOTE.get(che_type, "")}
    if baseline is not None:
        dep = percent_depression(current, baseline)
        res.update({"baseline": baseline, "depression_pct": dep, "remaining_pct": 100 - dep,
                    "threshold_pct": threshold, "exceeds": dep > threshold})
        res["reading"] = ("depression %.1f %% > %g %% of baseline -> consistent with OP-level inhibition (card Fork 5)"
                          % (dep, threshold) if dep > threshold else
                          "depression %.1f %% <= %g %% of baseline -> below the card's OP-level threshold" % (dep, threshold))
    elif ref_low is not None:
        res["ref_low"] = ref_low
        res["reading"] = ("below your lab's lower reference (%g)" % ref_low if current < ref_low else
                          "within/above your lab's lower reference (%g)" % ref_low)
        res["note"] = "population reference is less sensitive than the patient's own baseline (wide normal range)"
    else:
        raise ValueError("need --baseline (preferred) or --ref-low (your lab's lower reference limit)")
    return res


def steady_state_fraction(hours_on_regimen, half_life):
    if half_life <= 0:
        raise ValueError("half-life must be > 0")
    return 1 - 0.5 ** (hours_on_regimen / half_life)


def tdm(half_life, since_start, ss_halflives=5.0, interval=None, since_last=None, trough_window=None, order=None):
    n = since_start / half_life
    frac = steady_state_fraction(since_start, half_life)
    res = {"half_life_h": half_life, "hours_on_regimen": since_start, "half_lives_elapsed": n,
           "fraction_of_steady_state": frac, "ss_rule_halflives": ss_halflives,
           "steady_state": n >= ss_halflives,
           "earliest_ss_sample_h": ss_halflives * half_life,
           "notes": ["use the PATIENT's half-life (renal / hepatic impairment prolongs it); count from the last "
                     "dose CHANGE, not the first dose ever"]}
    if not res["steady_state"]:
        res["steady_state_reading"] = ("NOT at steady state (%.2f of %g half-lives) -> level will under-read; "
                                       "card trap: sampling before steady state" % (n, ss_halflives))
    else:
        res["steady_state_reading"] = "at steady state by the %g-half-life rule" % ss_halflives
    if interval is not None and since_last is not None:
        if since_last > interval:
            res["position"] = "sample taken after the scheduled next dose time: check whether that dose was given"
        else:
            before_next = interval - since_last
            res.update({"hours_after_last_dose": since_last, "hours_before_next_dose": before_next,
                        "pct_through_interval": since_last / interval * 100})
            if trough_window is None:
                res["position"] = "no --trough-window: position reported, trough not judged (window = your SOP)"
            else:
                is_trough = before_next <= trough_window
                res["is_trough"] = is_trough
                res["position"] = ("trough window (<= %g h before next dose)" % trough_window if is_trough
                                   else "NOT a trough (%.2f h before next dose > %g h window)" % (before_next, trough_window))
                if order == "trough" and not is_trough:
                    res["order_check"] = "WRONG TIME: trough ordered but sample is not pre-dose (card trap)"
                elif order == "trough":
                    res["order_check"] = "timing consistent with a trough order"
    if order == "peak":
        res["order_check"] = "peak timing is drug/route-specific (e.g. after infusion end): check your SOP"
    return res


SPECIMEN_RULES = {
    "phenytoin": {"forbid": {"gel": "gel separator absorbs phenytoin -> falsely low; use a plain (no-gel) tube"}},
    "tacrolimus": {"require": "whole-blood", "why": "drug sits in RBC/lymphocytes -> whole blood"},
    "cyclosporine": {"require": "whole-blood", "why": "drug sits in RBC/lymphocytes -> whole blood"},
    "ethanol": {"require": "whole-blood", "sealed": True, "why": "volatile -> whole blood, sealed tube (GC-headspace)"},
    "toluene": {"require": "whole-blood", "sealed": True, "why": "volatile -> whole blood, sealed tube"},
    "volatile": {"require": "whole-blood", "sealed": True, "why": "volatile -> whole blood, sealed tube"},
    "cyanide": {"require": "whole-blood", "sealed": True, "why": "card trap list: CN in an open / gel tube is lost"},
}
ANALYTE_ALIASES = {"alcohol": "ethanol", "ciclosporin": "cyclosporine", "cyclosporin": "cyclosporine"}
# anticoagulated, unspun tubes count as whole blood (grey-top NaF is the usual ethanol tube: 510403 section 2.8)
WHOLE_BLOOD = {"whole-blood", "edta", "heparin", "fluoride"}


def specimen(analyte, tube, sealed=True):
    an = ANALYTE_ALIASES.get(analyte.lower(), analyte.lower())
    tube = tube.lower()
    rule = SPECIMEN_RULES.get(an)
    if rule is None:
        return {"analyte": analyte, "tube": tube, "ok": None, "reading": "no card rule for this analyte -> follow SOP"}
    problems = []
    if tube in rule.get("forbid", {}):
        problems.append(rule["forbid"][tube])
    if rule.get("require") == "whole-blood" and tube not in WHOLE_BLOOD:
        problems.append("needs anticoagulated WHOLE BLOOD (unspun), got %s: %s" % (tube, rule["why"]))
    if rule.get("sealed") and (not sealed or tube == "gel"):
        problems.append("volatile analyte: tube must be sealed, no gel (loss by evaporation / absorption)")
    return {"analyte": an, "tube": tube, "ok": not problems,
            "reading": "WRONG SPECIMEN: " + "; ".join(problems) if problems else "tube consistent with card rules"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("che")
    p.add_argument("--current", type=float, required=True, help="current ChE activity (U/L)")
    p.add_argument("--baseline", type=float, help="patient's own pre-exposure baseline (same method)")
    p.add_argument("--type", choices=["plasma", "rbc"], dest="che_type")
    p.add_argument("--threshold", type=float, default=50.0, help="depression threshold (default 50 = card/digest)")
    p.add_argument("--ref-low", type=float, help="your lab's lower reference limit (if no baseline)")
    p = sub.add_parser("tdm")
    p.add_argument("--half-life", type=float, required=True, help="hours (patient's, if known)")
    p.add_argument("--since-start", type=float, required=True, help="hours on the current regimen")
    p.add_argument("--ss-halflives", type=float, default=5.0, help="steady-state rule (default 5)")
    p.add_argument("--interval", type=float, help="dosing interval h")
    p.add_argument("--since-last-dose", type=float, help="hours from last dose to sample")
    p.add_argument("--trough-window", type=float, help="your SOP's trough window, h before next dose")
    p.add_argument("--order", choices=["trough", "peak"])
    p = sub.add_parser("specimen")
    p.add_argument("--analyte", required=True)
    p.add_argument("--tube", required=True, choices=["gel", "plain", "edta", "heparin", "fluoride", "whole-blood"],
                   help="gel = serum separator; plain = serum, no gel; edta/heparin/fluoride/whole-blood = unspun whole blood")
    p.add_argument("--unsealed", action="store_true", help="tube was left open / not airtight")
    a = ap.parse_args(argv)

    if a.cmd == "che":
        res = che(a.current, a.baseline, a.che_type, a.threshold, a.ref_low)
    elif a.cmd == "tdm":
        res = tdm(a.half_life, a.since_start, a.ss_halflives, a.interval, a.since_last_dose, a.trough_window, a.order)
    else:
        res = specimen(a.analyte, a.tube, sealed=not a.unsealed)

    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        for k, v in res.items():
            if isinstance(v, list):
                for item in v:
                    print("%-26s %s" % ("note", item))
            elif v not in ("", None):
                print("%-26s %s" % (k, ("%.3f" % v) if isinstance(v, float) else v))
        print("ADVISORY: decision support only - confirm with the lab SOP and the physician / poison centre (1367).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
