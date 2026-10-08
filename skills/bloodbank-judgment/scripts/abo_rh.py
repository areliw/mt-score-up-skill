#!/usr/bin/env python3
"""abo_rh - ABO/RhD typing interpretation and ABO/Rh component compatibility.

Black-box tool for bloodbank-judgment. Run --help first; read the source only if a result looks wrong.
Rules come from the owner's course digests and the card:
  512303 Transfusion Science 1 digest
    §2.1 Landsteiner's rule (antibody to the ABO antigens a person lacks)
    §2.4 serum (reverse) grouping is valid only from ~3-6 months; neonates = forward only
    §2.6 ABO compatibility table (RBC / plasma / whole blood; platelet = identical or plasma-compatible;
         cryo = any ABO group) - RBC O and plasma AB are the universal donors
    §3.2 weak D: donor -> label D-positive; patient -> give D-negative; pregnant -> test (RhIG decision)
    §8   discrepancy = weaker than expected, missing or extra; §8.1 RBC-side and §8.2 serum-side causes
    §11  grading: w+ is a (weak) positive, mf = mixed-field, hemolysis in reverse = positive
  512304 Transfusion Science 2 digest §4 Case 1 (acquired B: forward anti-B 1+ = abnormally weak),
         Case 2 (A2 with anti-A1), Case 5 (passive anti-A,B from group O platelets)
  510403 Clinical Lab Practice digest §3.1 (forward anti-A/anti-B/anti-D; reverse A1/B/O cells)
  card bloodbank-judgment Fork 1 (discrepancy table; unresolved in an emergency -> group O RBC;
         Bombay -> Bombay blood only), Fork 5 (platelet risk sits in donor PLASMA; ABO-identical is
         ideal; plasma direction AB > A/B > O), Fork 7 (emergency O; O-neg for women of child-bearing
         potential and children), Fork 9 (weak D: donor D-positive / patient D-negative)
ADVISORY ONLY. Group assignment and unit release belong to the lab SOP and an authorised signatory.

Subcommands
  type     interpret forward/reverse ABO + RhD; status CONCORDANT / DISCREPANCY / FORWARD-ONLY /
           INCOMPLETE, the flags that triggered it, the card's candidate causes, and what to issue
           while it is unresolved
  compat   ABO (and RhD for red cells) donor groups acceptable for a recipient, per component

Grades: 0 | neg | -   w+   1+ 2+ 3+ 4+   mf (mixed-field)   H / CH / PH (hemolysis = positive)
"Weak" = positive but below --forward-min (default 2, i.e. w+ and 1+ are weak; 512304 Case 1) or
below --reverse-min (default 1, i.e. only w+ is weak). These are reading conventions: set them from
your SOP.

Examples
  python abo_rh.py type --anti-a 4+ --anti-b 0 --a1-cells 0 --b-cells 4+ --anti-d 3+
  python abo_rh.py type --anti-a 4+ --anti-b 1+ --a1-cells 0 --b-cells 3+ --auto 0
  python abo_rh.py type --anti-a 0 --anti-b 0 --a1-cells 4+ --b-cells 4+ --o-cells 3+ --auto 0
  python abo_rh.py type --anti-a 4+ --anti-b 0 --a1-cells 0 --b-cells 4+ --anti-d 0 --d-ahg 2+ --role patient
  python abo_rh.py compat --recipient A --component platelet
  python abo_rh.py compat --recipient unknown --component all --rh unknown --json
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

ADVISORY = "ADVISORY: decision support only - confirm with the blood bank SOP and an authorised signatory."

_NUM = {"0": 0, "neg": 0, "-": 0, "w": 0.5, "w+": 0.5, "+w": 0.5, "wk": 0.5,
        "1": 1, "1+": 1, "2": 2, "2+": 2, "3": 3, "3+": 3, "4": 4, "4+": 4}


def parse_grade(raw):
    """Return None (not tested) or {raw, pos, strength, mf, hemolysis}."""
    if raw is None:
        return None
    t = str(raw).strip().lower().replace(" ", "")
    if t in ("", "nt", "nd"):
        return None
    if t == "mf":
        return {"raw": raw, "pos": True, "strength": None, "mf": True, "hemolysis": False}
    if t in ("h", "ch", "ph"):
        return {"raw": raw, "pos": True, "strength": None, "mf": False, "hemolysis": True}
    if t in _NUM:
        v = _NUM[t]
        return {"raw": raw, "pos": v > 0, "strength": v, "mf": False, "hemolysis": False}
    raise ValueError("unknown grade %r (use 0, w+, 1+..4+, mf, H)" % raw)


def pos(g):
    return bool(g and g["pos"])


def weak(g, minimum):
    """Positive but weaker than expected (or mixed-field)."""
    if not pos(g):
        return False
    if g["mf"]:
        return True
    return g["strength"] is not None and g["strength"] < minimum


def group_from_antigens(a, b):
    return {(True, True): "AB", (True, False): "A", (False, True): "B", (False, False): "O"}[(a, b)]


def group_from_antibodies(anti_a, anti_b):
    # Landsteiner (512303 §2.1): the antibodies present are against the antigens the person lacks
    return {(True, True): "O", (False, True): "A", (True, False): "B", (False, False): "AB"}[(anti_a, anti_b)]


# ------------------------------------------------------------------ RhD (512303 §3.2, card Fork 9)
def interpret_rh(anti_d, d_ahg=None, role="patient", forward_min=2, auto=None):
    d, w = parse_grade(anti_d), parse_grade(d_ahg)
    out = {"anti_d": anti_d, "d_ahg": d_ahg, "role": role, "d_status": "not tested",
           "label_as": None, "transfuse_as": None, "notes": []}
    if d is None:
        return out
    if pos(parse_grade(auto)):
        out["notes"].append("autocontrol positive: a positive anti-D may be false (coated cells) - resolve first")
    if d["mf"]:
        out.update(d_status="MIXED-FIELD D", label_as="unresolved", transfuse_as="D-negative")
        out["notes"].append("mixed-field D: recent transfusion / HSCT -> history; genotype (card Fork 9)")
        return out
    if pos(d) and not weak(d, forward_min):
        out.update(d_status="D-POSITIVE", label_as="D-positive", transfuse_as="D-positive")
        return out
    if pos(d):  # weak reactivity at immediate spin
        out["d_status"] = "WEAK D REACTIVITY (immediate spin)"
    elif pos(w):
        out["d_status"] = "WEAK D (negative at IS, positive at 37C/AHG)"
    elif w is not None:
        out.update(d_status="D-NEGATIVE", label_as="D-negative", transfuse_as="D-negative")
        return out
    else:  # IS negative, weak-D test not done
        if role == "donor":
            out.update(d_status="INCOMPLETE", label_as="pending weak-D test", transfuse_as=None)
            out["notes"].append("donor negative at IS must have a weak-D test before labelling D-negative (512303 §3.2)")
        elif role == "prenatal":
            out.update(d_status="INCOMPLETE", label_as="pending weak-D test", transfuse_as="D-negative")
            out["notes"].append("pregnant woman: weak-D test is needed for the RhIG decision (512303 §3.2)")
        else:
            out.update(d_status="D-NEGATIVE", label_as="D-negative", transfuse_as="D-negative")
            out["notes"].append("patient: weak-D test not required - give D-negative (512303 §3.2)")
        return out
    # weak D handling depends on who the cells belong to
    if role == "donor":
        out.update(label_as="D-positive", transfuse_as="D-positive (donor unit)")
        out["notes"].append("donor weak D -> label D-POSITIVE so it is never given to a D-negative recipient (512303 §3.2; card Fork 9)")
    else:
        out.update(label_as="weak D (report wording per SOP)", transfuse_as="D-negative")
        out["notes"].append("patient weak/partial D -> transfuse D-NEGATIVE (partial D can make anti-D) (512303 §3.2; card Fork 9)")
        out["notes"].append("510403 §3.1 reports weak D as 'Rh positive' with no donor/patient split - for transfusing a patient the role-specific rule above applies")
        if role == "prenatal":
            out["notes"].append("pregnant: RhIG decision per SOP/physician; consider RHD genotyping (card Fork 9)")
    return out


# ------------------------------------------------------------------ ABO typing (512303 §8, card Fork 1)
def interpret_type(anti_a, anti_b, a1_cells=None, b_cells=None, o_cells=None, auto=None,
                   anti_d=None, d_ahg=None, role="patient", neonate=False, forward_min=2, reverse_min=1):
    fa, fb = parse_grade(anti_a), parse_grade(anti_b)
    ra, rb, ro, au = parse_grade(a1_cells), parse_grade(b_cells), parse_grade(o_cells), parse_grade(auto)
    if fa is None or fb is None:
        raise ValueError("forward grouping needs both --anti-a and --anti-b")
    A, B = pos(fa), pos(fb)
    fwd = group_from_antigens(A, B)
    flags, causes = [], []
    res = {"forward_group": fwd, "reverse_group": None, "status": None, "flags": flags,
           "candidate_causes": causes, "issue_while_unresolved": None, "bombay_suspect": False,
           "thresholds": {"forward_min": forward_min, "reverse_min": reverse_min}}

    for name, g in (("anti-A", fa), ("anti-B", fb)):
        if g["mf"]:
            flags.append("RBC: mixed-field with %s" % name)
        elif weak(g, forward_min):
            flags.append("RBC: weak %s reaction (%s)" % (name, g["raw"]))
        if g["hemolysis"]:
            flags.append("RBC: hemolysis in forward tube with %s - check sample / repeat" % name)
    if any(g["mf"] for g in (fa, fb)):
        causes.append("mixed-field: recent group O (or other) transfusion, post-HSCT, A3/B3 subgroup -> "
                      "transfusion/transplant history (512303 §8.1; card Fork 1)")

    if neonate:
        res["status"] = "FORWARD-ONLY"
        res["issue_while_unresolved"] = ("neonate: serum grouping is not valid before ~3-6 months (512303 §2.4); "
                                         "follow the neonatal protocol (card scope note)")
        res["rh"] = interpret_rh(anti_d, d_ahg, role, forward_min, auto)
        return res
    if ra is None or rb is None:
        res["status"] = "INCOMPLETE"
        res["issue_while_unresolved"] = "reverse grouping (A1 and B cells) is required to assign a group"
        res["rh"] = interpret_rh(anti_d, d_ahg, role, forward_min, auto)
        return res

    anti_A, anti_B = pos(ra), pos(rb)
    rev = group_from_antibodies(anti_A, anti_B)
    res["reverse_group"] = rev
    for name, g in (("A1 cells", ra), ("B cells", rb)):
        if weak(g, reverse_min):
            flags.append("SERUM: weak reaction with %s (%s)" % (name, g["raw"]))

    # antigen/antibody conflicts and gaps (512303 §8: weak / missing / extra; RBC side vs serum side)
    for ag, has_ag, has_ab, fg, rg in (("A", A, anti_A, fa, ra), ("B", B, anti_B, fb, rb)):
        if has_ag and has_ab:
            flags.append("CONFLICT: RBC show %s antigen AND serum has anti-%s" % (ag, ag))
            if weak(fg, forward_min):
                if ag == "B" and A:
                    causes.append("acquired B (RBC extra; group A + colon cancer / gram-negative sepsis): acidified "
                                  "anti-B pH 6, patient's own anti-B does not agglutinate own cells -> transfuse "
                                  "group A (512304 Case 1; card Fork 1)")
                causes.append("weak extra %s antigen on RBC (B(A)/A(B) phenotype) -> molecular / ref lab; transfuse "
                              "by true group (512303 §8.1; card Fork 1)" % ag)
            else:
                if ag == "A":
                    causes.append("anti-A1 in an A2/A2B person (serum extra): anti-A1 lectin (Dolichos biflorus) + "
                                  "A2 cells -> give A2 or O RBC (512304 Case 2; card Fork 1)")
                causes.append("serum extra antibody reacting with %s cells: cold allo/autoantibody or rouleaux -> "
                              "autocontrol, O cells, prewarm 37C, saline replacement (512303 §8.2)" %
                              ("A1" if ag == "A" else "B"))
        elif not has_ag and not has_ab:
            flags.append("GAP: RBC lack %s antigen AND serum lacks anti-%s" % (ag, ag))
            causes.append("RBC missing/weak %s (subgroup e.g. A-weak, leukemia, transplant): extended incubation, "
                          "anti-A,B, adsorption-elution, saliva, molecular (512303 §8.1; 510403 §3.1 Aweak case)" % ag)
            causes.append("serum missing/weak anti-%s (neonate, elderly, hypogammaglobulinemia, immunosuppression, "
                          "BMT, myeloma): incubate RT/4C longer + autocontrol (512303 §8.2)" % ag)

    if pos(ro):
        flags.append("SERUM: unexpected reaction with O cells (%s)" % ro["raw"])
        if pos(au):
            causes.append("cold autoantibody (anti-I / anti-IH), screen+ and auto+: prewarm 37C, cold "
                          "autoadsorption (512303 §8.2; card Fork 1)")
            causes.append("rouleaux (high protein, myeloma): saline replacement (512303 §8.2)")
        else:
            causes.append("cold alloantibody (anti-M, -N, -P1, -Le, -Lua), auto-: antibody identification (512303 §8.2)")
            if fwd == "O":
                res["bombay_suspect"] = True
                causes.append("anti-H (Bombay / para-Bombay): forward O, O cells reactive, auto- -> confirm with "
                              "Bombay RBC + saliva; GROUP O BLOOD IS NOT SAFE (512303 §2.5, §8.2; card Fork 1) RED FLAG")
            if au is None:
                causes.append("autocontrol not run: run it - it separates cold auto (auto+) from allo/anti-H (auto-)")
    if pos(au):
        flags.append("AUTOCONTROL positive (%s)" % au["raw"])
        causes.append("autoantibody / DAT+ coating, or passive anti-A,B from group O platelets/plasma: check "
                      "component history, DAT, eluate (512304 Case 5; card Fork 1)")

    discrepant = (fwd != rev) or bool(flags)
    res["status"] = "DISCREPANCY" if discrepant else "CONCORDANT"
    if res["bombay_suspect"]:
        res["issue_while_unresolved"] = ("DO NOT issue group O RBC: suspected anti-H (Bombay). Bombay (Oh) RBC only - "
                                         "ref lab / rare donor registry. RED FLAG")
    elif discrepant:
        res["issue_while_unresolved"] = ("do not assign a group. If transfusion cannot wait: RBC group O (O D-neg for "
                                         "women of child-bearing potential/children), plasma group AB "
                                         "(512303 §2.6; card Fork 1 and Fork 7)")
    else:
        res["issue_while_unresolved"] = "none - group %s; pick units with `compat --recipient %s`" % (fwd, fwd)
    # de-duplicate, keep order
    seen = set()
    res["candidate_causes"] = [c for c in causes if not (c in seen or seen.add(c))]
    res["rh"] = interpret_rh(anti_d, d_ahg, role, forward_min, auto)
    return res


# ------------------------------------------------------------------ compatibility (512303 §2.6, card Fork 5/7)
GROUPS = ["O", "A", "B", "AB"]
RBC_COMPAT = {"A": ["A", "O"], "B": ["B", "O"], "AB": ["AB", "A", "B", "O"], "O": ["O"]}
PLASMA_COMPAT = {"A": ["A", "AB"], "B": ["B", "AB"], "AB": ["AB"], "O": ["O", "A", "B", "AB"]}
PLASMA_STRENGTH_ORDER = ["AB", "A", "B", "O"]  # card Fork 5: plasma compatibility direction AB > A/B > O
COMPONENTS = ["rbc", "plasma", "platelet", "cryo", "wb"]


def rbc_rh(rh):
    note = ("D-positive only per SOP/physician when D-negative stock is short, and never for women of "
            "child-bearing potential or children (card Fork 7)")
    if rh == "pos":
        return {"acceptable": ["D-positive", "D-negative"], "note": ""}
    return {"acceptable": ["D-negative"], "note": note}


def compat(recipient, component, rh="unknown"):
    r = recipient.upper() if recipient.lower() != "unknown" else "unknown"
    if r not in GROUPS + ["unknown"]:
        raise ValueError("recipient must be O, A, B, AB or unknown")
    out = {"recipient": r, "component": component, "rh": rh}
    if component == "rbc":
        groups = RBC_COMPAT[r] if r != "unknown" else ["O"]
        out.update(acceptable=groups, preferred=[r] if r != "unknown" else ["O"],
                   rule="RBC: donor RBC must lack the antigens the recipient has antibody to; O = universal "
                        "RBC donor (512303 §2.6)", rh_rbc=rbc_rh(rh))
    elif component == "plasma":
        groups = PLASMA_COMPAT[r] if r != "unknown" else ["AB"]
        out.update(acceptable=groups, preferred=[r] if r != "unknown" else ["AB"],
                   rule="plasma: donor plasma must lack antibody to the recipient's antigens; AB = universal "
                        "plasma donor (512303 §2.6)")
    elif component == "wb":
        groups = [r] if r != "unknown" else []
        out.update(acceptable=groups, preferred=groups,
                   rule="whole blood: ABO-identical only (512303 §2.6); recipient group must be known",
                   rh_rbc=rbc_rh(rh))
    elif component == "cryo":
        out.update(acceptable=list(GROUPS), preferred=list(GROUPS),
                   rule="cryoprecipitate: any ABO group (512303 §2.6) - confirm volume/paediatric policy in SOP")
    elif component == "platelet":
        if r == "unknown":
            out.update(acceptable=["AB"], preferred=["AB"], plasma_incompatible=["A", "B", "O"],
                       rule="platelets, recipient group unknown: AB plasma is compatible with everyone; other "
                            "groups only per SOP (low-titre / plasma-reduced) (512303 §2.6; card Fork 5)")
        else:
            plasma_ok = [g for g in PLASMA_STRENGTH_ORDER if g in PLASMA_COMPAT[r] and g != r]
            incompatible = [g for g in PLASMA_STRENGTH_ORDER if g not in PLASMA_COMPAT[r]]
            out.update(acceptable=[r] + plasma_ok, preferred=[r], plasma_incompatible=incompatible,
                       rule="platelets: ABO-identical ideal, then plasma-compatible; the risk is anti-A/anti-B in "
                            "donor PLASMA - plasma-incompatible units (e.g. high-titre group O to A/B) only per SOP, "
                            "low-titre or plasma-reduced (512303 §2.6; card Fork 5; 512304 Case 5)")
    else:
        raise ValueError("component must be one of %s" % COMPONENTS)
    return out


# ------------------------------------------------------------------ CLI
def print_type(res):
    print("forward group : %s" % res["forward_group"])
    print("reverse group : %s" % (res["reverse_group"] or "-"))
    print("STATUS        : %s" % res["status"])
    for f in res["flags"]:
        print("  flag  - %s" % f)
    if res["candidate_causes"]:
        print("candidate causes (card Fork 1 / 512303 §8):")
        for c in res["candidate_causes"]:
            print("  * %s" % c)
    print("issue         : %s" % res["issue_while_unresolved"])
    rh = res["rh"]
    if rh["d_status"] != "not tested":
        print("RhD (%s)  : %s | label as: %s | transfuse as: %s" % (rh["role"], rh["d_status"], rh["label_as"],
                                                                rh["transfuse_as"]))
        for n in rh["notes"]:
            print("  note  - %s" % n)
    print("thresholds    : weak = forward below %s+, reverse below %s+ (set from SOP)" %
          (res["thresholds"]["forward_min"], res["thresholds"]["reverse_min"]))


def print_compat(rows):
    print("%-9s %-9s %-22s %-12s %s" % ("recipient", "component", "acceptable donor ABO", "preferred",
                                        "RhD for red cells (recipient %s)" % rows[0]["rh"]))
    for o in rows:
        rh = ", ".join(o["rh_rbc"]["acceptable"]) if "rh_rbc" in o else "per SOP"
        print("%-9s %-9s %-22s %-12s %s" % (o["recipient"], o["component"], ", ".join(o["acceptable"]) or "NONE",
                                            ", ".join(o["preferred"]) or "-", rh))
    for o in rows:
        print("  %s: %s" % (o["component"], o["rule"]))
        if o.get("plasma_incompatible"):
            print("    plasma-INCOMPATIBLE (per SOP only): %s" % ", ".join(o["plasma_incompatible"]))
        if o.get("rh_rbc", {}).get("note"):
            print("    Rh: %s" % o["rh_rbc"]["note"])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("type", help="interpret forward/reverse ABO and RhD")
    t.add_argument("--anti-a", required=True)
    t.add_argument("--anti-b", required=True)
    t.add_argument("--a1-cells")
    t.add_argument("--b-cells")
    t.add_argument("--o-cells", help="reverse O cells / screening cells, if tested")
    t.add_argument("--auto", help="autocontrol, if tested")
    t.add_argument("--anti-d")
    t.add_argument("--d-ahg", help="weak-D test (37C/AHG) result, if done")
    t.add_argument("--role", choices=["patient", "donor", "prenatal"], default="patient")
    t.add_argument("--neonate", action="store_true", help="forward only (serum grouping not valid yet)")
    t.add_argument("--forward-min", type=float, default=2, help="forward grade below this = weak (default 2)")
    t.add_argument("--reverse-min", type=float, default=1, help="reverse grade below this = weak (default 1)")
    c = sub.add_parser("compat", help="acceptable donor groups for a recipient")
    c.add_argument("--recipient", required=True, help="O, A, B, AB or unknown")
    c.add_argument("--component", choices=COMPONENTS + ["all"], default="all")
    c.add_argument("--rh", choices=["pos", "neg", "unknown"], default="unknown", help="recipient RhD")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "type":
            res = interpret_type(a.anti_a, a.anti_b, a.a1_cells, a.b_cells, a.o_cells, a.auto, a.anti_d, a.d_ahg,
                                 a.role, a.neonate, a.forward_min, a.reverse_min)
        else:
            comps = COMPONENTS if a.component == "all" else [a.component]
            res = [compat(a.recipient, k, a.rh) for k in comps]
    except ValueError as e:
        ap.error(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print_type(res) if a.cmd == "type" else print_compat(res)
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
