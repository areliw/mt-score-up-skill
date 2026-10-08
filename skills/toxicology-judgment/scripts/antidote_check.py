#!/usr/bin/env python3
"""antidote_check - check a poison -> antidote/chelator pairing against the card's table.

Black-box tool for toxicology-judgment (Forks 3-4 and the anti-pattern list). It answers ONE
question: "does the card list this pairing as first-line / adjunct, conditional, forbidden or a
wrong pair - and is a required companion missing?" It never gives doses and never says "safe".
An unknown pair is reported as NOT IN CARD TABLE (ask the poison centre), never as OK.

Sources: the card's Fork 3 (antidote tree), Fork 4 (chelator table) and anti-pattern list, all
cross-checked against the owner digest 510414-DIGEST-2026-05-31.md:
  section 4  opioid -> naloxone
  section 5  chelators: BAL for As/Hg/Pb, NOT for Cd (renal toxicity); Ca-EDTA for Pb, NEVER the Na
             salt (hypocalcemic tetany); penicillamine for Cu/Wilson; desferrioxamine for Fe;
             dithiocarb for acute nickel carbonyl
  section 6  OP -> atropine + 2-PAM (before aging); carbamate -> atropine, 2-PAM not needed / caution;
             paraquat -> no specific antidote, Fuller's earth + hemoperfusion < 10 h;
             organochlorine -> diazepam/phenobarbital, NEVER epinephrine; warfarin -> vitamin K
  section 8  methanol -> NaHCO3 + ethanol (card adds fomepizole first-line and hemodialysis)
  section 10 corrosive -> no emesis, no neutralising, dilute with water/milk
Card-only items (not in the digest): fomepizole first-line, hydroxocobalamin first-line in cyanide /
nitrite avoided with CO co-exposure, unknown cholinergic crisis -> keep 2-PAM until OP excluded.
ADVISORY ONLY: physician / Ramathibodi Poison Center 1367 decides; adults only (card scope).

Examples
  python antidote_check.py --agent lead --give Na-EDTA
  python antidote_check.py --agent op --give pralidoxime
  python antidote_check.py --agent cyanide --give nitrite --co-suspected
  python antidote_check.py --list
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

FIRST = "MATCHES CARD (first-line)"
ADJ = "MATCHES CARD (alternative / adjunct)"
COND = "CONDITIONAL"
FORBID = "FORBIDDEN BY CARD"
WRONG = "WRONG PAIR"
UNKNOWN = "NOT IN CARD TABLE"
AMBIG = "AMBIGUOUS NAME"

AGENT_ALIASES = {
    "op": "op", "organophosphate": "op", "carbamate": "carbamate",
    "cholinergic-unknown": "cholinergic-unknown", "unknown-cholinergic": "cholinergic-unknown",
    "cholinergic": "cholinergic-unknown",
    "opioid": "opioid", "heroin": "opioid", "morphine": "opioid",
    "methanol": "methanol", "cyanide": "cyanide", "cn": "cyanide", "paraquat": "paraquat",
    "warfarin": "warfarin", "coumarin": "warfarin",
    "lead": "lead", "pb": "lead", "arsenic": "arsenic", "as": "arsenic", "mercury": "mercury", "hg": "mercury",
    "cadmium": "cadmium", "cd": "cadmium", "copper": "copper", "cu": "copper", "wilson": "copper",
    "iron": "iron", "fe": "iron", "nickel-carbonyl": "nickel-carbonyl", "ni": "nickel-carbonyl",
    "organochlorine": "organochlorine", "ddt": "organochlorine", "corrosive": "corrosive",
}

TREAT_ALIASES = {
    "atropine": "atropine", "pralidoxime": "pralidoxime", "2-pam": "pralidoxime", "pam": "pralidoxime",
    "naloxone": "naloxone", "fomepizole": "fomepizole", "ethanol": "ethanol",
    "sodium-bicarbonate": "sodium-bicarbonate", "nahco3": "sodium-bicarbonate", "bicarbonate": "sodium-bicarbonate",
    "hemodialysis": "hemodialysis", "hd": "hemodialysis", "hydroxocobalamin": "hydroxocobalamin",
    "nitrite": "nitrite", "sodium-nitrite": "nitrite", "thiosulfate": "thiosulfate",
    "vitamin-k": "vitamin-k", "vit-k": "vitamin-k",
    "ca-edta": "ca-edta", "cana2edta": "ca-edta", "edetate-calcium-disodium": "ca-edta", "calcium-edta": "ca-edta",
    "na-edta": "na-edta", "na2edta": "na-edta", "edetate-disodium": "na-edta", "disodium-edta": "na-edta",
    "bal": "bal", "dimercaprol": "bal", "dmps": "dmps", "penicillamine": "penicillamine",
    "desferrioxamine": "desferrioxamine", "deferoxamine": "desferrioxamine", "dithiocarb": "dithiocarb",
    "ddc": "dithiocarb", "fullers-earth": "fullers-earth", "hemoperfusion": "hemoperfusion",
    "oxygen-high": "oxygen-high", "high-o2": "oxygen-high", "diazepam": "diazepam",
    "phenobarbital": "phenobarbital", "epinephrine": "epinephrine", "adrenaline": "epinephrine",
    "emesis": "emesis", "induce-vomiting": "emesis", "neutralize": "neutralize", "neutralise": "neutralize",
    "dilute-water-milk": "dilute-water-milk", "dilute": "dilute-water-milk",
}
AMBIGUOUS = {"edta": "say Ca-EDTA or Na-EDTA - the salt IS the trap (Na salt -> hypocalcemic tetany)"}

# agent -> {"label", "pairs": {treatment: (status, why)}, "expect": [treatments the card pairs together]}
TABLE = {
    "op": {"label": "organophosphate", "expect": ["atropine", "pralidoxime"], "pairs": {
        "atropine": (FIRST, "blocks muscarinic effects"),
        "pralidoxime": (FIRST, "reactivates AChE; must be given before 'aging'; always WITH atropine"),
        "naloxone": (WRONG, "naloxone is the opioid antidote - card anti-pattern 'naloxone in OP'")}},
    "carbamate": {"label": "carbamate (CONFIRMED)", "expect": ["atropine"], "pairs": {
        "atropine": (FIRST, "mainstay; carbamylation is reversible (~24-48 h)"),
        "pralidoxime": (COND, "usually unnecessary once carbamate is CONFIRMED (harm data from old carbaryl "
                              "reports, debated) - physician decides"),
        "naloxone": (WRONG, "opioid antidote, not for cholinergic crisis")}},
    "cholinergic-unknown": {"label": "cholinergic crisis, OP vs carbamate NOT distinguished",
                            "expect": ["atropine", "pralidoxime"], "pairs": {
        "atropine": (FIRST, "mainstay"),
        "pralidoxime": (FIRST, "card: flag 2-PAM until OP is ruled out (missing OP is worse; aging) - "
                               "physician/1367 orders; always WITH atropine"),
        "naloxone": (WRONG, "opioid antidote")}},
    "opioid": {"label": "opioid", "expect": ["naloxone"], "pairs": {
        "naloxone": (FIRST, "reverses miosis / respiratory depression / coma")}},
    "methanol": {"label": "methanol", "expect": ["fomepizole"], "pairs": {
        "fomepizole": (FIRST, "blocks ADH so formate is not made"),
        "ethanol": (ADJ, "competes for ADH when fomepizole is unavailable"),
        "sodium-bicarbonate": (ADJ, "corrects metabolic acidosis"),
        "hemodialysis": (ADJ, "removes methanol + formate; fomepizole does NOT replace HD when acidosis is "
                              "severe, visual symptoms or a high level")}},
    "cyanide": {"label": "cyanide", "expect": ["hydroxocobalamin"], "pairs": {
        "hydroxocobalamin": (FIRST, "first choice; safe when CO co-exposure is suspected"),
        "thiosulfate": (ADJ, "part of the cyanide kit"),
        "nitrite": (COND, "induces metHb - avoid in smoke inhalation / suspected CO (use --co-suspected)")}},
    "paraquat": {"label": "paraquat (no specific antidote)", "expect": [], "pairs": {
        "fullers-earth": (ADJ, "30% Fuller's earth adsorbent"),
        "hemoperfusion": (ADJ, "within 10 h"),
        "oxygen-high": (FORBID, "high O2 accelerates redox cycling / radical damage")}},
    "warfarin": {"label": "warfarin / coumarin rodenticide", "expect": ["vitamin-k"], "pairs": {
        "vitamin-k": (FIRST, "replaces the vitamin K the coumarin antagonises")}},
    "lead": {"label": "lead (Pb)", "expect": ["ca-edta"], "pairs": {
        "ca-edta": (FIRST, "calcium disodium EDTA"),
        "bal": (ADJ, "card: 'or BAL / penicillamine'"),
        "penicillamine": (ADJ, "card: 'or BAL / penicillamine'"),
        "na-edta": (FORBID, "Na salt chelates Ca -> hypocalcemic tetany")}},
    "arsenic": {"label": "arsenic (As)", "expect": ["bal"], "pairs": {
        "bal": (FIRST, "dimercaprol"), "dmps": (FIRST, "water-soluble BAL derivative")}},
    "mercury": {"label": "mercury (Hg)", "expect": ["bal"], "pairs": {
        "bal": (FIRST, "dimercaprol"), "dmps": (FIRST, "water-soluble BAL derivative")}},
    "cadmium": {"label": "cadmium (Cd) - supportive care", "expect": [], "pairs": {
        "bal": (FORBID, "BAL increases cadmium renal toxicity")}},
    "copper": {"label": "copper / Wilson's", "expect": ["penicillamine"], "pairs": {
        "penicillamine": (FIRST, "caution in penicillin allergy (cross-reaction possible; card: not an "
                                 "absolute contraindication)")}},
    "iron": {"label": "iron overload / transfusion haemosiderosis", "expect": ["desferrioxamine"], "pairs": {
        "desferrioxamine": (FIRST, "iron chelator")}},
    "nickel-carbonyl": {"label": "nickel carbonyl (acute)", "expect": ["dithiocarb"], "pairs": {
        "dithiocarb": (FIRST, "drug of choice")}},
    "organochlorine": {"label": "organochlorine (seizures)", "expect": [], "pairs": {
        "diazepam": (FIRST, "seizure control"), "phenobarbital": (FIRST, "seizure control"),
        "epinephrine": (FORBID, "myocardial irritability")}},
    "corrosive": {"label": "corrosive ingestion", "expect": [], "pairs": {
        "dilute-water-milk": (FIRST, "dilute"),
        "emesis": (FORBID, "re-exposes the oesophagus"),
        "neutralize": (FORBID, "exothermic reaction / re-injury")}},
}

RED_FLAG = ("RED FLAG (card): any antidote/chelator decision -> physician / Ramathibodi Poison Center 1367 "
            "confirms BEFORE giving; children / infants / pregnancy -> specialist protocol")


def norm(name):
    return name.strip().lower().replace(" ", "-").replace("_", "-")


def check(agent, gives, co_suspected=False):
    a = AGENT_ALIASES.get(norm(agent))
    if a is None:
        return {"agent": agent, "known_agent": False, "rows": [],
                "verdict": "agent not in card table -> no automated check; consult 1367", "red_flag": RED_FLAG}
    entry = TABLE[a]
    rows, canon = [], []
    for g in gives:
        n = norm(g)
        if n in AMBIGUOUS:
            rows.append({"give": g, "status": AMBIG, "why": AMBIGUOUS[n]})
            continue
        t = TREAT_ALIASES.get(n, n)
        canon.append(t)
        status, why = entry["pairs"].get(t, (UNKNOWN, "card table has no entry for this pair -> consult 1367"))
        if a == "cyanide" and t == "nitrite" and co_suspected:
            status, why = FORBID, "CO / smoke inhalation suspected: nitrite adds metHb (card) -> hydroxocobalamin"
        rows.append({"give": g, "as": t, "status": status, "why": why})
    missing = [t for t in entry["expect"] if t not in canon]
    warnings = []
    if "pralidoxime" in canon and "atropine" not in canon and a in ("op", "carbamate", "cholinergic-unknown"):
        warnings.append("2-PAM WITHOUT atropine: card - always give with atropine; 2-PAM alone may worsen")
    if missing:
        warnings.append("card pairs this agent with: %s (not in your list)" % ", ".join(missing))
    statuses = {r["status"] for r in rows}
    if FORBID in statuses or WRONG in statuses:
        verdict = "STOP: forbidden or wrong pair in the list"
    elif AMBIG in statuses or UNKNOWN in statuses or warnings:
        verdict = "CHECK: unresolved item(s) or missing companion"
    else:
        verdict = "consistent with the card table (still physician / 1367 decision)"
    return {"agent": agent, "as": a, "label": entry["label"], "known_agent": True, "rows": rows,
            "warnings": warnings, "verdict": verdict, "red_flag": RED_FLAG}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--agent", help="poison / toxidrome, e.g. op, carbamate, cholinergic-unknown, lead, cadmium")
    ap.add_argument("--give", action="append", default=[], help="treatment (repeatable), e.g. atropine, Na-EDTA")
    ap.add_argument("--co-suspected", action="store_true", help="smoke inhalation / CO co-exposure")
    ap.add_argument("--list", action="store_true", help="print the card table and exit")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.list:
        if a.json:
            print(json.dumps(TABLE, ensure_ascii=False, indent=1))
        else:
            for k, e in TABLE.items():
                print("%s (%s)" % (k, e["label"]))
                for t, (st, why) in e["pairs"].items():
                    print("   %-20s %-38s %s" % (t, st, why))
        return 0
    if not a.agent or not a.give:
        ap.error("--agent and at least one --give are required (or --list)")
    res = check(a.agent, a.give, a.co_suspected)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("agent: %s -> %s" % (a.agent, res.get("label", "unknown")))
    for r in res["rows"]:
        print("  %-18s %-38s %s" % (r["give"], r["status"], r["why"]))
    for w in res.get("warnings", []):
        print("  WARNING: %s" % w)
    print("VERDICT: %s" % res["verdict"])
    print(res["red_flag"])
    print("ADVISORY: decision support only - the physician / poison centre (1367) orders treatment per protocol.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
