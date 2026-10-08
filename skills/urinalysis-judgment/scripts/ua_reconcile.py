#!/usr/bin/env python3
"""ua_reconcile - check a urinalysis (strip + sediment + specimen) against the card's rules.

Black-box tool for urinalysis-judgment. It lists every strip<->sediment discordance and every
finding the card says must be resolved, re-collected or flagged BEFORE the report goes out.
It does not identify sediment - a person at the microscope does; it checks the logic.

Rules (each finding prints the card fork it comes from):
  pre      tested within 2 h or kept at 2-8 C; otherwise casts lyse, bacteria grow, pH rises,
           cells/glucose lyse, crystals form in vitro
  Fork 1   blood+ with no RBC -> hemoglobinuria / myoglobinuria, not bleeding; strip protein reads
           albumin (misses Bence-Jones) -> SSA / electrophoresis when myeloma is suspected;
           nitrite- and LE- never exclude UTI -> microscopy + culture; pH > 8 -> stale / urease
           (Proteus); glucose+ with normal blood glucose -> renal glycosuria / pregnancy
  Fork 2   RBC + menstruation -> contamination, re-collect; dysmorphic RBC -> glomerular;
           pyuria with negative culture -> sterile pyuria list; many squamous -> contamination,
           re-collect midstream; RTE cells -> significant (ATN / active injury)
  Fork 3   casts localise to the kidney; RBC cast (GN), WBC cast (pyelo/interstitial nephritis),
           muddy-brown (ATN) -> FLAG; others reported with their meaning
  Fork 4   crystal identity is read with pH (uric acid = acid urine; triple / amorphous phosphate =
           alkaline; calcium oxalate any pH); cystine / tyrosine / leucine / cholesterol / drug
           crystals always pathologic; calcium oxalate + AKI -> think ethylene glycol (emergency);
           talc / starch / fiber are artifacts
Cross-check in owner digests: nephritic urine = RBC + RBC casts (505402 section 5.4); red cell casts =
glomerular damage (510416 Case 7). "Seen" for RBC/WBC uses YOUR lab's upper limit per HPF
(--rbc-max / --wbc-max); without it any count > 0 counts as seen (stated in the output).
ADVISORY ONLY.

Examples
  python ua_reconcile.py --blood 2+ --rbc 0 --nitrite neg --le 1+ --wbc 25 --wbc-max 5 --bacteria many
  python ua_reconcile.py --ph 7.8 --crystal uric-acid --crystal calcium-oxalate --aki --age-h 1
  python ua_reconcile.py --squamous many --cast rbc --json
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

LEVEL_ORDER = ["HOLD", "RECOLLECT", "FLAG", "CAUTION", "INFO"]
NEG = {"neg", "negative", "0", "-", "none", "nil"}
SEMIQ = ["none", "few", "moderate", "many"]

CASTS = {
    "hyaline": ("INFO", "benign: dehydration / exercise / fever"),
    "rbc": ("FLAG", "RBC cast = glomerulonephritis -> flag + correlate"),
    "wbc": ("FLAG", "WBC cast = pyelonephritis / interstitial nephritis -> flag + correlate"),
    "muddy-brown": ("FLAG", "muddy-brown cast = ATN -> flag + correlate"),
    "granular": ("INFO", "granular cast: card groups with ATN (granular / muddy brown) - correlate"),
    "waxy": ("INFO", "waxy cast = chronic renal failure"),
    "broad": ("INFO", "broad cast = chronic renal failure"),
    "fatty": ("INFO", "fatty cast (+ oval fat body, Maltese cross) = nephrotic"),
}
CRYSTALS = {
    "uric-acid": {"ph": "acid"},
    "calcium-oxalate": {"ph": "any"},
    "triple-phosphate": {"ph": "alkaline", "note": "struvite / coffin-lid, think Proteus"},
    "struvite": {"ph": "alkaline", "note": "think Proteus"},
    "amorphous-phosphate": {"ph": "alkaline"},
    "cystine": {"ph": None, "path": "cystinuria"},
    "tyrosine": {"ph": None, "path": "liver disease"},
    "leucine": {"ph": None, "path": "liver disease"},
    "cholesterol": {"ph": None, "path": "always pathologic"},
    "sulfa": {"ph": None, "path": "drug crystal -> medication history"},
    "acyclovir": {"ph": None, "path": "drug crystal -> medication history"},
    "indinavir": {"ph": None, "path": "drug crystal -> medication history"},
    "drug": {"ph": None, "path": "drug crystal -> medication history"},
    "talc": {"artifact": True}, "starch": {"artifact": True}, "fiber": {"artifact": True},
    "amorphous": {"artifact": True},
}


def positive(x):
    return x is not None and str(x).strip().lower() not in NEG


def seen(count, upper):
    if count is None:
        return None
    return count > upper if upper is not None else count > 0


def add(out, level, fork, finding, action):
    out.append({"level": level, "fork": fork, "finding": finding, "action": action})


def nitrite_rule(nitrite, uti_signal):
    """Fork 1 / trap #2: a negative nitrite never excludes UTI."""
    if nitrite is None or positive(nitrite):
        return None
    if uti_signal:
        return ("FLAG", "Fork 1", "nitrite negative WITH other UTI signals",
                "do NOT exclude UTI (Enterococcus / Staph / Pseudomonas / Acinetobacter lack nitrate reductase; "
                "short bladder time) -> microscopy + urine culture")
    return ("CAUTION", "Fork 1", "nitrite negative",
            "does not exclude UTI by itself; read with LE, microscopy and clinical context; culture if suspected")


def evaluate(s):
    """s: dict of inputs (see main). Returns {"findings": [...], "status": str, "notes": [...]}."""
    out, notes = [], []
    rbc_seen = seen(s.get("rbc"), s.get("rbc_max"))
    wbc_seen = seen(s.get("wbc"), s.get("wbc_max"))
    if (s.get("rbc") is not None and s.get("rbc_max") is None) or (s.get("wbc") is not None and s.get("wbc_max") is None):
        notes.append("no --rbc-max/--wbc-max: 'seen' means > 0 per HPF; pass your lab's upper limits")
    bacteria = (s.get("bacteria") or "none").lower()
    stale = s.get("age_h") is not None and s["age_h"] > 2 and not s.get("refrigerated")

    # pre-analytical
    if stale:
        add(out, "RECOLLECT", "pre", "tested %.1f h after collection, not refrigerated" % s["age_h"],
            "re-collect (preferred); otherwise comment: casts/cells may have lysed, bacteria/pH/crystals unreliable")
    if s.get("ph") is not None and s["ph"] > 8:
        add(out, "CAUTION", "Fork 1", "pH %.1f > 8" % s["ph"], "stale specimen or urease organism (Proteus): check specimen age")

    # Fork 1 strip <-> sediment
    if positive(s.get("blood")) and rbc_seen is False:
        add(out, "HOLD", "Fork 1", "blood strip %s but RBC not seen" % s["blood"],
            "hemoglobinuria (hemolysis) or myoglobinuria (rhabdomyolysis), not bleeding -> plasma colour / CK; resolve before report")
    if s.get("blood") is not None and not positive(s.get("blood")) and rbc_seen:
        add(out, "HOLD", "Fork 1", "RBC seen but blood strip negative",
            "strip and microscopy disagree (card rule #1) -> re-check both per SOP before report")
    le = s.get("le")
    if le is not None and not positive(le) and wbc_seen:
        add(out, "HOLD", "Fork 1", "WBC seen but leukocyte esterase negative",
            "LE can be negative early / in neutropenia -> trust microscopy, re-check; resolve before report")
    if positive(le) and wbc_seen is False:
        add(out, "HOLD", "Fork 1", "leukocyte esterase %s but WBC not seen" % le,
            "strip and microscopy disagree (card rule #1) -> re-check both per SOP before report")
    uti_signal = bool(positive(le) or wbc_seen or bacteria in ("few", "moderate", "many") or s.get("suspect_uti"))
    r = nitrite_rule(s.get("nitrite"), uti_signal)
    if r:
        add(out, *r)
    if s.get("suspect_myeloma"):
        add(out, "FLAG", "Fork 1", "myeloma / light chain suspected",
            "strip protein reads ALBUMIN and misses Bence-Jones -> SSA or protein electrophoresis, whatever the strip says")
    if positive(s.get("glucose")) and s.get("serum_glucose_normal"):
        add(out, "INFO", "Fork 1", "glycosuria with normal blood glucose", "renal glycosuria / pregnancy")

    # Fork 2 cells
    if rbc_seen and s.get("menstruating"):
        add(out, "RECOLLECT", "Fork 2", "RBC during menstruation", "contamination -> re-collect")
    if rbc_seen and s.get("rbc_morph") == "dysmorphic":
        add(out, "FLAG", "Fork 2", "dysmorphic RBC / acanthocytes", "glomerular source -> flag + correlate")
    elif rbc_seen and s.get("rbc_morph") == "isomorphic":
        add(out, "INFO", "Fork 2", "isomorphic RBC", "lower tract / stone / tumour")
    if wbc_seen and s.get("culture") == "negative":
        add(out, "FLAG", "Fork 2", "sterile pyuria (WBC + culture negative)",
            "think TB, chlamydia/GC, treated infection, stone, interstitial nephritis")
    squam = (s.get("squamous") or "none").lower()
    if squam == "many":
        add(out, "RECOLLECT", "Fork 2", "many squamous epithelial cells",
            "contamination -> re-collect clean-catch midstream; bacteria in this sample are suspect")
    if s.get("rte"):
        add(out, "FLAG", "Fork 2", "renal tubular epithelial cells",
            "significant (ATN / active tubular injury) - do not lump with squamous")
    if bacteria in ("few", "moderate", "many"):
        if stale:
            add(out, "CAUTION", "Fork 2", "bacteria in a stale specimen", "may be in-vitro growth")
        elif wbc_seen is False:
            add(out, "CAUTION", "Fork 2", "bacteria without WBC", "correlate with WBC + freshness before calling infection")

    # Fork 3 casts
    for c in s.get("casts") or []:
        key = c.lower().replace(" ", "-")
        level, meaning = CASTS.get(key, ("INFO", "cast type not in card table - report per SOP"))
        add(out, level, "Fork 3", "%s cast" % c, meaning)
    if stale and not s.get("casts"):
        add(out, "CAUTION", "Fork 3", "no casts reported in a stale specimen", "casts lyse on standing: absence is not reassuring")

    # Fork 4 crystals
    ph = s.get("ph")
    ph_side = None if ph is None else ("acid" if ph < 7 else ("alkaline" if ph > 7 else "neutral"))
    for c in s.get("crystals") or []:
        key = c.lower().replace(" ", "-")
        info = CRYSTALS.get(key)
        if info is None:
            add(out, "INFO", "Fork 4", "%s crystal" % c, "not in card table - identify per SOP")
            continue
        if info.get("artifact"):
            add(out, "INFO", "Fork 4", "%s" % c, "artifact - do not report as a pathologic crystal")
            continue
        if info.get("path"):
            add(out, "FLAG", "Fork 4", "%s crystal" % c, "always pathologic: %s" % info["path"])
        expected = info.get("ph")
        if expected in ("acid", "alkaline"):
            if ph_side is None:
                notes.append("no --ph: crystal identity not cross-checked against pH")
            elif ph_side != "neutral" and ph_side != expected:
                add(out, "CAUTION", "Fork 4", "%s crystal at pH %.1f (%s urine)" % (c, ph, ph_side),
                    "card: %s forms in %s urine -> re-identify (amorphous / other crystal?)" % (c, expected))
        if key == "calcium-oxalate" and s.get("aki"):
            add(out, "FLAG", "Fork 4", "calcium oxalate + AKI",
                "EMERGENCY: think ethylene glycol poisoning -> notify now, link toxicology (antidote is time-critical)")

    out.sort(key=lambda f: LEVEL_ORDER.index(f["level"]))
    levels = {f["level"] for f in out}
    if levels & {"HOLD", "RECOLLECT"}:
        status = "DO NOT RELEASE YET: resolve / re-collect first"
    elif "FLAG" in levels:
        status = "RELEASE WITH FLAG: notify / correlate as listed"
    else:
        status = "no card-rule discordance found (microscopy review still applies)"
    return {"findings": out, "status": status, "notes": sorted(set(notes))}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--age-h", type=float, help="hours from collection to testing")
    ap.add_argument("--refrigerated", action="store_true", help="kept at 2-8 C until tested")
    for k in ("blood", "protein", "nitrite", "le", "glucose", "ketone"):
        ap.add_argument("--" + k, help="strip result: neg / trace / 1+ / 2+ / 3+ / pos")
    ap.add_argument("--ph", type=float)
    ap.add_argument("--rbc", type=float, help="RBC per HPF")
    ap.add_argument("--wbc", type=float, help="WBC per HPF")
    ap.add_argument("--rbc-max", type=float, help="your lab's upper limit RBC/HPF")
    ap.add_argument("--wbc-max", type=float, help="your lab's upper limit WBC/HPF")
    ap.add_argument("--rbc-morph", choices=["dysmorphic", "isomorphic"])
    ap.add_argument("--squamous", choices=SEMIQ)
    ap.add_argument("--bacteria", choices=SEMIQ)
    ap.add_argument("--rte", action="store_true", help="renal tubular epithelial cells seen")
    ap.add_argument("--cast", action="append", dest="casts", default=[],
                    help="repeatable: hyaline rbc wbc muddy-brown granular waxy broad fatty")
    ap.add_argument("--crystal", action="append", dest="crystals", default=[],
                    help="repeatable: uric-acid calcium-oxalate triple-phosphate amorphous-phosphate cystine ...")
    ap.add_argument("--culture", choices=["positive", "negative"])
    ap.add_argument("--menstruating", action="store_true")
    ap.add_argument("--suspect-uti", action="store_true")
    ap.add_argument("--suspect-myeloma", action="store_true")
    ap.add_argument("--serum-glucose-normal", action="store_true")
    ap.add_argument("--aki", action="store_true", help="acute kidney injury present")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    res = evaluate(vars(a))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    if not res["findings"]:
        print("(no findings)")
    for f in res["findings"]:
        print("%-9s %-6s %s\n%17s-> %s" % (f["level"], f["fork"], f["finding"], "", f["action"]))
    for n in res["notes"]:
        print("NOTE: %s" % n)
    print("STATUS: %s" % res["status"])
    print("ADVISORY: decision support only - microscopy by a person + the lab SOP + MT/physician confirm before release.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
