#!/usr/bin/env python3
"""panel_ruleout - antibody identification: cross-out (rule-out) on a panel antigram YOU supply.

Black-box tool for bloodbank-judgment. Run --help first; read the source only if a result looks wrong.
The antigram must come from your own panel sheet (this tool ships no commercial panel).
Rules come from the owner's course digests and the card:
  512304 Transfusion Science 2 digest §3: rule-out = a NON-reactive cell crosses out the antigens it
         carries; for antibodies that show dosage rule out ONLY with homozygous cells; 95% (3-cell)
         rule = >=3 antigen-positive reactive cells AND >=3 antigen-negative non-reactive cells;
         Case 4 (anti-E + anti-Jka: "still need 1 more E+ Jka- cell")
  510403 Clinical Lab Practice digest §3.3 (cross out -> list survivors -> phase -> most likely;
         confirm the patient lacks the antigen; all cells + with auto- = high-incidence antigen) and
         §3.5 (all cells + with auto+ = autoantibody)
  512303 Transfusion Science 1 digest §1.3 (antithetical pairs, dosage), §4.1 (which antibodies are
         clinically significant)
  card bloodbank-judgment Fork 2 (read autocontrol first; rule out with homozygous cells; dosage
         systems Jk/Rh/Duffy/Kell/MNS; 3-cell rule; pan-reactive -> high-incidence / ref lab)
ADVISORY ONLY. Antibody identification is signed off by the lab, never by this script.

Input CSV (header required): one row per panel cell
  cell,D,C,E,c,e,...,Jka,Jkb,result
  antigen columns: + (positive) | 0 or - (negative) | blank or nt (not typed)
  result column  : 0 | w+ | 1+..4+ | mf | H     (choose another column with --result-col, e.g. AHG)
  columns named cell/id/#/notes/comment and the result column are not antigens; drop others with
  --ignore-cols. Names like Fy(a), Jk(a), Le(a) are normalised to Fya, Jka, Lea.

Rule-out modes
  --rule-out homozygous  (default) antigens in the dosage list are crossed out only by a non-reactive
                          cell that is homozygous (antigen + AND its antithetical antigen typed 0)
  --rule-out any          any antigen-positive non-reactive cell crosses out (the dosage trap - shown
                          only so you can see what it would hide)
  default dosage list = card Fork 2: C c E e M N S s Fya Fyb Jka Jkb K k   (--dosage-antigens to change;
  e.g. some SOPs accept K+k+ cells for anti-K: --dosage-antigens C,c,E,e,M,N,S,s,Fya,Fyb,Jka,Jkb)

Rule of three is counted STRICTLY: an antigen-positive reactive cell only counts for antibody X if it
is negative for every other candidate that explains reactivity (or every antigen in --confirm).

Examples
  python panel_ruleout.py ../data/panel_teaching_anti-E_anti-Jka.csv --auto 0
  python panel_ruleout.py ../data/panel_teaching_anti-E_anti-Jka.csv --auto 0 --confirm E,Jka --patient "E-,Jka-"
  python panel_ruleout.py panel.csv --result-col AHG --rule-out any --json
"""
import argparse
import csv
import json
import re
import sys

ADVISORY = "ADVISORY: decision support only - antibody ID is confirmed and signed off per blood bank SOP."

PAIRS = {"C": "c", "c": "C", "E": "e", "e": "E", "M": "N", "N": "M", "S": "s", "s": "S",
         "Fya": "Fyb", "Fyb": "Fya", "Jka": "Jkb", "Jkb": "Jka", "K": "k", "k": "K", "Lua": "Lub", "Lub": "Lua"}
DEFAULT_DOSAGE = ["C", "c", "E", "e", "M", "N", "S", "s", "Fya", "Fyb", "Jka", "Jkb", "K", "k"]
# 512303 §4.1 (+ §3/§5.1 for Rh): usually clinically significant (IgG, 37C/AHG) vs usually not (IgM, RT)
CLIN_SIG = {"D": "yes", "C": "yes", "c": "yes", "E": "yes", "e": "yes", "K": "yes", "k": "yes",
            "Fya": "yes", "Fyb": "yes", "Jka": "yes", "Jkb": "yes", "S": "yes", "s": "yes", "Lub": "yes",
            "M": "usually not", "N": "usually not", "P1": "usually not", "Lea": "usually not",
            "Leb": "usually not", "Lua": "usually not"}
NON_ANTIGEN = {"cell", "id", "#", "no", "notes", "note", "comment", "comments", "donor", "lot"}
_MULTI = {"fya": "Fya", "fyb": "Fyb", "jka": "Jka", "jkb": "Jkb", "lea": "Lea", "leb": "Leb", "lua": "Lua",
          "lub": "Lub", "kpa": "Kpa", "kpb": "Kpb", "jsa": "Jsa", "jsb": "Jsb", "dia": "Dia", "dib": "Dib",
          "p1": "P1", "xga": "Xga", "mia": "Mia"}
_NUM = {"0": 0, "neg": 0, "-": 0, "w": 0.5, "w+": 0.5, "+w": 0.5, "wk": 0.5,
        "1": 1, "1+": 1, "2": 2, "2+": 2, "3": 3, "3+": 3, "4": 4, "4+": 4}


def norm_antigen(name):
    n = re.sub(r"[\s()^]", "", name.strip())
    return _MULTI.get(n.lower(), n)


def parse_ag(v):
    t = (v or "").strip().lower()
    if t in ("+", "1", "pos", "p", "+w", "w+", "w"):
        return True
    if t in ("0", "-", "neg", "n"):
        return False
    if t in ("", "nt", "nd", "/"):
        return None
    raise ValueError("antigen value %r not understood (use +, 0, or blank)" % v)


def parse_result(v):
    t = (v or "").strip().lower().replace(" ", "")
    if t in ("mf", "h", "ch", "ph"):
        return True
    if t in _NUM:
        return _NUM[t] > 0
    raise ValueError("result %r not understood (use 0, w+, 1+..4+, mf, H)" % v)


def load(path, result_col="result", ignore=()):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("empty CSV")
    headers = list(rows[0].keys())
    rc = next((h for h in headers if h.strip().lower() == result_col.lower()), None)
    if rc is None:
        raise ValueError("result column %r not found in %s" % (result_col, headers))
    skip = {i.strip().lower() for i in ignore} | NON_ANTIGEN | {rc.strip().lower()}
    idc = next((h for h in headers if h.strip().lower() in ("cell", "id", "#", "no")), None)
    ag_cols = [h for h in headers if h.strip().lower() not in skip]
    antigens = [norm_antigen(h) for h in ag_cols]
    cells = []
    for i, r in enumerate(rows):
        cid = (r.get(idc) or "").strip() if idc else str(i + 1)
        cells.append({"id": cid or str(i + 1),
                      "ag": {a: parse_ag(r.get(h)) for a, h in zip(antigens, ag_cols)},
                      "reactive": parse_result(r.get(rc)), "result": (r.get(rc) or "").strip()})
    return antigens, cells


def is_homozygous(cell, ag):
    """True / False / None(unknown). Antigens with no antithetical partner in the model count as True."""
    pair = PAIRS.get(ag)
    if pair is None:
        return True
    partner = cell["ag"].get(pair)
    if cell["ag"].get(ag) is not True or partner is None:
        return None
    return partner is False


def rule_out(cells, antigens, mode="homozygous", dosage=DEFAULT_DOSAGE):
    excluded, het_only = {}, {}
    for ag in antigens:
        for c in cells:
            if c["reactive"] or c["ag"].get(ag) is not True:
                continue
            if mode == "any" or ag not in dosage:
                excluded.setdefault(ag, []).append(c["id"])
                continue
            hz = is_homozygous(c, ag)
            if hz:
                excluded.setdefault(ag, []).append(c["id"])
            else:
                het_only.setdefault(ag, []).append((c["id"], "heterozygous" if hz is False else "zygosity unknown"))
    for ag in excluded:
        het_only.pop(ag, None)
    return excluded, het_only


def strict_positive(cells, x, others):
    """Reactive cells that carry x and are typed NEGATIVE for every other hypothesised antigen."""
    return [c["id"] for c in cells if c["reactive"] and c["ag"].get(x) is True
            and all(c["ag"].get(o) is False for o in others if o != x)]


def analyse(antigens, cells, mode="homozygous", dosage=DEFAULT_DOSAGE, min_cells=3, auto=None,
            confirm=None, patient=None):
    excluded, het_only = rule_out(cells, antigens, mode, dosage)
    reactive = [c["id"] for c in cells if c["reactive"]]
    nonreactive = [c["id"] for c in cells if not c["reactive"]]
    candidates = [a for a in antigens if a not in excluded]
    rows = {}
    for x in candidates:
        rows[x] = {"antigen": x,
                   "pos_reactive": [c["id"] for c in cells if c["reactive"] and c["ag"].get(x) is True],
                   "pos_nonreactive": [cid for cid, _ in het_only.get(x, [])],
                   "neg_reactive": [c["id"] for c in cells if c["reactive"] and c["ag"].get(x) is False],
                   "neg_nonreactive": [c["id"] for c in cells if not c["reactive"] and c["ag"].get(x) is False],
                   "not_typed": [c["id"] for c in cells if c["ag"].get(x) is None],
                   "clinically_significant": CLIN_SIG.get(x, "check"),
                   "excluded_only_by_dosage_rule": x in het_only}
    explaining = [x for x in candidates if rows[x]["pos_reactive"]]
    hypothesis = [norm_antigen(h) for h in confirm] if confirm else explaining
    notes, verdict_reasons = [], []
    for x in candidates:
        r = rows[x]
        r["strict_pos_reactive"] = strict_positive(cells, x, hypothesis if x in hypothesis else explaining)
        r["rule_of_three"] = (len(r["strict_pos_reactive"]) >= min_cells and len(r["neg_nonreactive"]) >= min_cells)
        r["need_more_pos"] = max(0, min_cells - len(r["strict_pos_reactive"]))
        r["need_more_neg"] = max(0, min_cells - len(r["neg_nonreactive"]))
        r["explains_all_reactive_alone"] = bool(reactive) and set(r["pos_reactive"]) == set(reactive)

    unexplained = [c["id"] for c in cells if c["reactive"] and not any(c["ag"].get(h) is True for h in hypothesis)]
    pan = bool(cells) and len(reactive) == len(cells)
    auto_pos = auto is not None and parse_result(auto)
    if auto is None:
        notes.append("autocontrol not given: read it first - auto- = alloantibody work-up, auto+ = think auto / cold "
                     "auto / recent transfusion first (card Fork 2; 512303 §7)")
    elif auto_pos:
        notes.append("autocontrol POSITIVE: autoantibody / DAT+ / recent transfusion before calling an alloantibody "
                     "(card Fork 2; 510403 §3.5)")
    if pan:
        if auto_pos:
            notes.append("all cells reactive + auto+: autoantibody pattern -> autologous adsorption, then look for "
                         "alloantibody underneath (510403 §3.5)")
        elif auto is not None:
            notes.append("all cells reactive + auto-: antibody to a high-incidence antigen (e.g. anti-k, anti-Jsb) or "
                         "multiple alloantibodies; daratumumab interference -> ref lab (510403 §3.3; card Fork 2) RED FLAG")
    if not reactive:
        notes.append("no reactive cells: no specificity identified on this phase")
    for x, cids in het_only.items():
        notes.append("anti-%s NOT excluded only because the non-reactive %s+ cell(s) %s are not proven homozygous "
                     "(dosage, 512304 §3) - test a homozygous %s+ cell or enzyme/selected cells" %
                     (x, x, ", ".join(c for c, _ in cids), x))
    if unexplained:
        verdict_reasons.append("reactive cell(s) %s not explained by %s -> another antibody, low-incidence antigen "
                               "or technique problem" % (", ".join(unexplained), ", ".join(hypothesis) or "any candidate"))
    for h in hypothesis:
        if h in excluded:
            verdict_reasons.append("anti-%s was RULED OUT by non-reactive cell(s) %s" % (h, ", ".join(excluded[h])))
        elif h in rows:
            r = rows[h]
            if not r["rule_of_three"]:
                need = []
                if r["need_more_pos"]:
                    others = [o for o in hypothesis if o != h]
                    need.append("%d more reactive %s+%s cell(s)" % (r["need_more_pos"], h,
                                "".join(" %s-" % o for o in others)))
                if r["need_more_neg"]:
                    need.append("%d more non-reactive %s- cell(s)" % (r["need_more_neg"], h))
                verdict_reasons.append("anti-%s: rule of three not met - need %s" % (h, " and ".join(need)))
        else:
            verdict_reasons.append("anti-%s: antigen %s is not on this antigram" % (h, h))
    not_yet = [x for x in candidates if x not in hypothesis]
    if not_yet:
        verdict_reasons.append("still NOT excluded: %s -> selected cell(s) positive for it (homozygous if dosage), "
                               "negative for %s, must be non-reactive" %
                               (", ".join("anti-" + x for x in not_yet), ", ".join(hypothesis) or "the others"))
    pheno = {}
    for item in (patient or []):
        m = re.match(r"^\s*([A-Za-z0-9()^]+)\s*[:=]?\s*([+\-0]|pos|neg)\s*$", item)
        if not m:
            raise ValueError("patient phenotype item %r - use e.g. E-,Jka-,K+" % item)
        pheno[norm_antigen(m.group(1))] = m.group(2) in ("+", "pos")
    for h in hypothesis:
        if pheno.get(h) is True:
            verdict_reasons.append("patient's own RBC are %s+ -> alloanti-%s is unlikely (autoantibody? recent "
                                   "transfusion?) (510403 §3.3 confirmation; 512304 §3)" % (h, h))
        elif h not in pheno:
            notes.append("confirm the patient's own RBC are %s- (510403 §3.3; 512304 §3)" % h)
    if not hypothesis:
        verdict = "NO SPECIFICITY"
    elif verdict_reasons:
        verdict = "NOT CONCLUSIVE"
    else:
        verdict = "CONSISTENT WITH anti-%s (rule of three met; all other specificities excluded)" % " + anti-".join(hypothesis)
    return {"mode": mode, "dosage_antigens": list(dosage), "min_cells": min_cells, "reactive": reactive,
            "nonreactive": nonreactive, "excluded": excluded, "candidates": rows, "explaining": explaining,
            "hypothesis": hypothesis, "unexplained_reactive": unexplained, "verdict": verdict,
            "reasons": verdict_reasons, "notes": notes}


def print_report(antigens, cells, res):
    w = max(4, max(len(a) for a in antigens) + 1)
    print("cell  " + "".join(a.ljust(w) for a in antigens) + "result")
    for c in cells:
        marks = "".join(("+" if c["ag"].get(a) else ("0" if c["ag"].get(a) is False else ".")).ljust(w)
                        for a in antigens)
        print("%-6s%s%s" % (c["id"], marks, c["result"]))
    print("-" * 70)
    print("rule-out mode: %s | dosage antigens: %s | rule of %d" %
          (res["mode"], " ".join(res["dosage_antigens"]), res["min_cells"]))
    print("crossed out  : " + ", ".join("%s (cell %s)" % (a, "/".join(c)) for a, c in res["excluded"].items()))
    print("NOT excluded :")
    print("  %-6s %-14s %-12s %-12s %-12s %-10s %s" % ("anti-", "Ag+ reactive", "Ag+ nonreact", "Ag- reactive",
                                                       "Ag- nonreact", "strict +", "clin. sig."))
    for x, r in res["candidates"].items():
        print("  %-6s %-14s %-12s %-12s %-12s %-10s %s" % (
            x, ",".join(r["pos_reactive"]) or "-", ",".join(r["pos_nonreactive"]) or "-",
            ",".join(r["neg_reactive"]) or "-", str(len(r["neg_nonreactive"])),
            "%d%s" % (len(r["strict_pos_reactive"]), " ok" if r["rule_of_three"] else ""), r["clinically_significant"]))
    print("hypothesis   : %s%s" % (", ".join("anti-" + h for h in res["hypothesis"]) or "-",
                                   "" if res["hypothesis"] != res["explaining"] else "  (candidates that explain reactivity)"))
    print("VERDICT      : %s" % res["verdict"])
    for r in res["reasons"]:
        print("  - %s" % r)
    for n in res["notes"]:
        print("  note: %s" % n)
    if res["mode"] == "any":
        print("  WARNING: --rule-out any crosses out on heterozygous cells - dosage can hide anti-Jk/-Fy/-Rh/-MNS "
              "(512304 §3; card Fork 2)")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--result-col", default="result")
    ap.add_argument("--ignore-cols", default="", help="comma list of extra non-antigen columns")
    ap.add_argument("--rule-out", choices=["homozygous", "any"], default="homozygous")
    ap.add_argument("--dosage-antigens", default=",".join(DEFAULT_DOSAGE))
    ap.add_argument("--min-cells", type=int, default=3, help="rule-of-three threshold (default 3)")
    ap.add_argument("--auto", help="autocontrol result (0, w+, 1+..)")
    ap.add_argument("--confirm", help="hypothesis to test, e.g. E,Jka")
    ap.add_argument("--patient", help="patient's own phenotype, e.g. \"E-,Jka-\"")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        antigens, cells = load(a.csv, a.result_col, [x for x in a.ignore_cols.split(",") if x])
        dosage = [norm_antigen(x) for x in a.dosage_antigens.split(",") if x.strip()]
        res = analyse(antigens, cells, a.rule_out, dosage, a.min_cells, a.auto,
                      [x for x in (a.confirm or "").split(",") if x.strip()] or None,
                      [x for x in (a.patient or "").split(",") if x.strip()])
    except ValueError as e:
        ap.error(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print_report(antigens, cells, res)
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
