#!/usr/bin/env python3
"""ast_read - interpret an AST panel with YOUR breakpoints and flag the phenotypes the card warns about.

Black-box tool for clinmicro-judgment. Run --help first; read the source only if a result looks wrong.
This tool contains NO CLSI/EUCAST table. Breakpoints, QC ranges and phenotype criteria come from a
rules JSON you supply (data/ast_rules_teaching.json = a few TEACHING values quoted in the owner's
digests; load your lab's current CLSI M100/EUCAST edition for real work).

What it does, in order (each step cites where the rule comes from)
  1. QC gate      QC strain zone outside its range -> every patient result for that drug = HOLD
                  (card trap #8 + RED FLAGS; MICRO-QC digest §B11; 508304 §9 "QC fail -> no report")
  2. S/I/R        disk: S if zone >= s, R if zone <= r, else I | MIC: S if <= s, R if >= r, else I
                  breakpoint looked up by (group, drug, method) ONLY - never borrowed from another
                  group (card FORK 4: CoNS cefoxitin <=24 mm = R; using the S. aureus 21 mm cut
                  under-calls MR-CoNS). A result may instead carry a user-read "sir".
  3. phenotypes   methicillin screen (cefoxitin R -> report as oxacillin R, MRSA/MR-CoNS alert;
                  509402 digest §3.3) · D-test (erythromycin R + clindamycin S -> D-test required;
                  D+ -> clindamycin R; 509402 §3.3, card FORK 4) · ESBL combination disk (zone with
                  clavulanate - zone alone >= criterion mm -> ESBL+; 509402 §3.3) · beta-lactamase
                  staph vs penicillin: sharp "cliff" zone edge = R whatever the zone (509402 §3.1)
                  · intrinsic resistance (card trap 10; 509402 §3.4) · AmpC-inducible species:
                  "S" to 3rd-gen cephalosporin flagged, avoid (card trap 10b)

Isolate JSON
  {"organism": "...", "group": "CoNS",
   "results": [{"drug": "cefoxitin", "method": "disk", "value": 23},
               {"drug": "erythromycin", "sir": "R"},
               {"drug": "penicillin", "method": "disk", "value": 30, "edge": "sharp"}],
   "d_test": "positive" | "negative" | null,
   "esbl_combo": [{"drug": "ceftazidime", "alone": 14, "with_clav": 21}],
   "qc": [{"strain": "S. aureus ATCC 25923", "drug": "gentamicin", "value": 22}]}

Examples (run from the skill folder)
  python scripts/ast_read.py data/isolate_cons_teaching.json --rules data/ast_rules_teaching.json
  python scripts/ast_read.py data/isolate_kpn_teaching.json --rules data/ast_rules_teaching.json --json
ADVISORY ONLY: the report decision belongs to the lab SOP and an authorised signatory.
"""
import argparse
import json
import re
import sys

ADVISORY = "ADVISORY: decision support only - confirm with the lab SOP, current breakpoint edition and an authorised signatory."


def norm(s):
    return (s or "").strip().lower()


def name_hit(term, organism):
    return re.search(r"\b" + re.escape(term) + r"\b", organism or "", re.IGNORECASE) is not None


# ---------------------------------------------------------------- step 2: S/I/R
def interpret(value, method, s, r):
    method = norm(method)
    if method == "disk":
        if not s > r:
            raise ValueError("disk breakpoints need s > r (zone mm)")
        return "S" if value >= s else ("R" if value <= r else "I")
    if method == "mic":
        if not s < r:
            raise ValueError("MIC breakpoints need s < r")
        return "S" if value <= s else ("R" if value >= r else "I")
    raise ValueError("method must be disk or mic, got %r" % method)


def find_breakpoint(rules, group, drug, method):
    """Strict lookup on (group, drug, method). No fallback to another organism group."""
    for bp in rules.get("breakpoints", []):
        if norm(bp["group"]) == norm(group) and norm(bp["drug"]) == norm(drug) and norm(bp["method"]) == norm(method):
            return bp
    return None


# ---------------------------------------------------------------- step 1: QC gate
def qc_gate(rules, qc_results):
    """Return ({drug: reason} for out-of-range QC, notes)."""
    held, notes = {}, []
    for q in qc_results or []:
        rng = next((x for x in rules.get("qc_ranges", [])
                    if norm(x["strain"]) == norm(q["strain"]) and norm(x["drug"]) == norm(q["drug"])), None)
        if rng is None:
            notes.append("no QC range supplied for %s / %s - cannot verify QC" % (q["strain"], q["drug"]))
            continue
        if not rng["low"] <= q["value"] <= rng["high"]:
            held[norm(q["drug"])] = "QC %s = %g outside %g-%g" % (q["strain"], q["value"], rng["low"], rng["high"])
    return held, notes


# ---------------------------------------------------------------- step 3: phenotypes
def apply_d_test(rows, d_test, alerts):
    ery = next((r for r in rows if r["drug"] == "erythromycin"), None)
    cli = next((r for r in rows if r["drug"] == "clindamycin"), None)
    if not (ery and cli) or ery["final"] != "R" or cli["final"] != "S":
        return
    if d_test is None:
        cli["final"] = "HOLD"
        cli["flags"].append("erythromycin R + clindamycin S -> D-test required before reporting clindamycin")
    elif norm(d_test) == "positive":
        cli["final"] = "R"
        cli["flags"].append("D-test positive -> inducible clindamycin resistance, report R")
        alerts.append("inducible clindamycin resistance (D-test +)")
    else:
        cli["flags"].append("D-test negative -> clindamycin S stands")


def esbl_screen(combos, criterion_mm):
    out = []
    for c in combos or []:
        inc = c["with_clav"] - c["alone"]
        out.append({"drug": c["drug"], "alone": c["alone"], "with_clav": c["with_clav"], "increase_mm": inc,
                    "esbl": inc >= criterion_mm})
    return out


def read_panel(isolate, rules):
    organism, group = isolate.get("organism", ""), isolate.get("group", "")
    held, notes = qc_gate(rules, isolate.get("qc"))
    alerts = []
    meth_drug = norm(rules.get("methicillin_screen", {}).get("drug", "cefoxitin"))
    rows = []
    for res in isolate.get("results", []):
        drug, method = norm(res["drug"]), norm(res.get("method"))
        row = {"drug": drug, "method": method or "-", "value": res.get("value"), "bp": None,
               "raw": None, "final": None, "reported_as": drug, "flags": []}
        if res.get("sir"):
            row["raw"] = res["sir"].upper()
            row["bp"] = "user-read"
        else:
            bp = find_breakpoint(rules, group, drug, method)
            if bp is None:
                row["raw"] = "NI"
                row["flags"].append("no breakpoint for group %r / %s / %s - NOT INTERPRETED "
                                    "(do not borrow another group's breakpoint)" % (group, drug, method))
            else:
                row["raw"] = interpret(res["value"], method, bp["s"], bp["r"])
                row["bp"] = "%s s%s r%s" % (bp["group"], ("%g" % bp["s"]), ("%g" % bp["r"]))
                if bp.get("report_as"):
                    row["reported_as"] = norm(bp["report_as"])
        row["final"] = row["raw"]
        # beta-lactamase staph vs penicillin: sharp edge = R whatever the zone (509402 §3.1)
        if drug == "penicillin" and norm(res.get("edge")) == "sharp":
            row["final"] = "R"
            row["flags"].append("sharp 'cliff' zone edge -> beta-lactamase+ -> R regardless of zone size")
        # intrinsic resistance
        for ir in rules.get("intrinsic_resistance", []):
            if name_hit(ir["organism"], organism) and drug in [norm(d) for d in ir["drugs"]]:
                if row["final"] != "R":
                    row["flags"].append("%s is intrinsically resistant to %s - an '%s' here is wrong; report R/suppress per SOP"
                                        % (ir["organism"], drug, row["final"]))
                row["final"] = "R"
        # methicillin screen
        if drug == meth_drug and row["final"] == "R":
            alerts.append("methicillin resistance (%s R -> report %s R): all beta-lactams R except anti-MRSA "
                          "cephalosporin; MDR alert -> infection control" % (drug, row["reported_as"]))
        rows.append(row)
    apply_d_test(rows, isolate.get("d_test"), alerts)
    crit = rules.get("criteria", {})
    if isolate.get("esbl_combo") and "esbl_combo_min_increase_mm" not in crit:
        raise SystemExit("rules.criteria.esbl_combo_min_increase_mm is required to read ESBL combination disks")
    esbl = esbl_screen(isolate.get("esbl_combo"), crit.get("esbl_combo_min_increase_mm"))
    if any(e["esbl"] for e in esbl):
        alerts.append("ESBL confirmed (combination disk) -> MDR alert, infection control; report beta-lactams per SOP")
    # AmpC-inducible species: S to 3rd-gen cephalosporin is not trustworthy (card trap 10b)
    if any(name_hit(sp, organism) for sp in rules.get("ampc_high_risk_species", [])):
        third = [norm(d) for d in rules.get("third_gen_cephalosporins", [])]
        for row in rows:
            if row["drug"] in third and row["final"] == "S":
                row["flags"].append("AmpC-inducible species: 'S' to 3rd-gen cephalosporin may fail on therapy -> "
                                    "comment 'avoid'; cefepime/carbapenem more reliable")
    # QC gate overrides everything for that drug
    for row in rows:
        if row["drug"] in held:
            row["final"] = "HOLD"
            row["flags"].append(held[row["drug"]] + " -> do not report until QC passes")
    return {"organism": organism, "group": group, "rows": rows, "esbl": esbl, "alerts": alerts, "qc_notes": notes}


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("isolate", help="isolate JSON (see docstring)")
    ap.add_argument("--rules", required=True, help="rules JSON: breakpoints, qc_ranges, criteria (YOUR lab's values)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    with open(a.isolate, encoding="utf-8") as f:
        isolate = json.load(f)
    with open(a.rules, encoding="utf-8") as f:
        rules = json.load(f)
    res = read_panel(isolate, rules)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("organism: %s | group: %s | rules: %s" % (res["organism"], res["group"], rules.get("_label", a.rules)[:90]))
    print("%-14s %-6s %7s %-22s %-4s %-6s %s" % ("drug", "method", "value", "breakpoint used", "raw", "FINAL", "reported as"))
    for r in res["rows"]:
        v = "-" if r["value"] is None else "%g" % r["value"]
        print("%-14s %-6s %7s %-22s %-4s %-6s %s" % (r["drug"], r["method"], v, (r["bp"] or "-")[:22], r["raw"],
                                                    r["final"], r["reported_as"]))
        for fl in r["flags"]:
            print("%16s - %s" % ("", fl))
    for e in res["esbl"]:
        print("ESBL combo %-12s alone %g / +clav %g -> +%g mm -> %s" % (e["drug"], e["alone"], e["with_clav"],
                                                                      e["increase_mm"], "ESBL+" if e["esbl"] else "not ESBL"))
    for n in res["qc_notes"]:
        print("QC NOTE: " + n)
    for al in res["alerts"]:
        print("ALERT: " + al)
    if not res["alerts"]:
        print("ALERT: none")
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
