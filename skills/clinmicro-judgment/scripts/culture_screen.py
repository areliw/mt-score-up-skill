#!/usr/bin/env python3
"""culture_screen - specimen-quality and culture-significance checks for clinmicro-judgment.

Black-box tool. Run --help first; read the source only if a result looks wrong.
Every cutoff is a LAB choice: pass it as flags, or point --cutoffs at a JSON file and pick a
--profile. data/micro_cutoffs_teaching.json holds TEACHING values from the owner's digests.
Sputum: use profile sputum-murray-washington-1975 (accept SEC<10 and PMN>25/LPF, reject SEC>10/LPF;
Murray & Washington, Mayo Clin Proc 1975, PMID 1127999; confirmed by the owner 2026-10-08). The old
sputum-card-fork5 profile (reject only SEC>25) mixed in Bartlett score points and now prints a
superseded WARNING. Your lab SOP still decides; the tool only applies it.

Subcommands
  sputum  SEC/LPF + PMN/LPF -> ACCEPT / BORDERLINE / REJECT
          rule shape: card FORK 5 + FORK 7 LRTI; 508304 lecture digest §2 (sputum quality)
  count   colonies -> CFU/mL = colonies / loop volume (mL) x dilution factor, then the band of
          the chosen profile; flags mixed growth, the symptom-status caveat, and reports a zero
          count as "< detection limit", never as 0
          509402 digest §4 (colony-count table, loop 0.001 mL -> x1,000); 508304 §2 BAL
          (loop 0.01 mL, 100 colonies = 1e4 CFU/mL, VAP >= 1e4); card FORK 3
  blood   blood-culture contaminant vs pathogen checklist: organism class x positive cultures
          card FORK 3 table; CLINMICRO1 digest §1 (normal flora of one site = pathogen of
          another), §4 (CoNS: 1 bottle = suspect contaminant, >=2 + line/prosthesis = maybe
          real), trap #1

Examples (run from the skill folder)
  python scripts/culture_screen.py sputum --sec 8 --pmn 30 --cutoffs data/micro_cutoffs_teaching.json --profile sputum-murray-washington-1975
  python scripts/culture_screen.py sputum --sec 15 --pmn 30 --sec-accept-below 10 --sec-reject-above 25 --pmn-above 25
  python scripts/culture_screen.py count --loop-ml 0.001 --org "E. coli=150" --symptoms no --cutoffs data/micro_cutoffs_teaching.json --profile urine-509402
  python scripts/culture_screen.py count --loop-ml 0.01 --org "P. aeruginosa=100" --cutoffs data/micro_cutoffs_teaching.json --profile bal-508304
  python scripts/culture_screen.py blood --organism "Staphylococcus epidermidis" --positive 1 --drawn 2 --flora data/blood_culture_flora_teaching.json
ADVISORY ONLY: the report decision belongs to the lab SOP and an authorised signatory.
"""
import argparse
import json
import re
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ADVISORY = "ADVISORY: decision support only - confirm with the lab SOP and an authorised signatory before reporting."


# ---------------------------------------------------------------- cutoffs
def load_profile(path, name, kind):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    profiles = data.get("profiles", {})
    if name not in profiles:
        raise SystemExit("profile %r not in %s (have: %s)" % (name, path, ", ".join(sorted(profiles))))
    prof = dict(profiles[name])
    if prof.get("kind") != kind:
        raise SystemExit("profile %r is kind=%r, not %r" % (name, prof.get("kind"), kind))
    prof["_from"] = "%s [%s] - %s" % (path, name, data.get("_label", "no label"))
    if prof.get("superseded_by"):
        prof["_warning"] = "WARNING: profile %r is superseded by %r - %s" % (
            name, prof["superseded_by"], prof.get("superseded_why", "see the cutoffs file"))
        print(prof["_warning"], file=sys.stderr)
    return prof


# ---------------------------------------------------------------- sputum
def sputum(sec, pmn, sec_accept_below, sec_reject_above, pmn_above):
    """SEC = squamous epithelial cells/LPF, PMN = neutrophils/LPF.

    REJECT when SEC > sec_reject_above (saliva). ACCEPT only when SEC < sec_accept_below AND
    PMN > pmn_above. Everything else = BORDERLINE (correlate with Gram/clinical, card FORK 5).
    """
    if sec_accept_below > sec_reject_above:
        raise ValueError("sec_accept_below must be <= sec_reject_above")
    if sec < 0 or pmn < 0:
        raise ValueError("counts must be >= 0")
    if sec > sec_reject_above:
        return {"verdict": "REJECT", "why": "SEC %g/LPF > %g -> saliva contamination; request a new specimen"
                % (sec, sec_reject_above)}
    if sec < sec_accept_below and pmn > pmn_above:
        return {"verdict": "ACCEPT", "why": "SEC %g < %g and PMN %g > %g/LPF -> lower-respiratory specimen"
                % (sec, sec_accept_below, pmn, pmn_above)}
    reasons = []
    if sec >= sec_accept_below:
        reasons.append("SEC %g/LPF in the grey zone [%g, %g]" % (sec, sec_accept_below, sec_reject_above))
    if pmn <= pmn_above:
        reasons.append("PMN %g/LPF not > %g" % (pmn, pmn_above))
    return {"verdict": "BORDERLINE", "why": "; ".join(reasons) + " -> correlate with Gram/clinical before processing"}


# ---------------------------------------------------------------- colony count
def cfu_per_ml(colonies, loop_ml, dilution_factor=1.0):
    """CFU/mL = colonies / volume plated (mL) x dilution factor (0.001 mL loop -> x1,000)."""
    if loop_ml <= 0 or dilution_factor <= 0:
        raise ValueError("loop_ml and dilution_factor must be > 0")
    if colonies < 0:
        raise ValueError("colonies must be >= 0")
    return colonies / loop_ml * dilution_factor


def band_of(cfu, bands):
    chosen = None
    for b in sorted(bands, key=lambda x: x["min"]):
        if cfu >= b["min"]:
            chosen = b
    return chosen


def parse_org(spec):
    if "=" not in spec:
        raise ValueError("--org must look like 'NAME=COLONIES', got %r" % spec)
    name, n = spec.rsplit("=", 1)
    return name.strip(), float(n)


def count(orgs, loop_ml, profile, dilution_factor=1.0, symptoms="unknown"):
    """orgs: list of (name, colonies). Returns per-organism CFU/mL + band + flags."""
    lod = cfu_per_ml(1, loop_ml, dilution_factor)
    rows = []
    for name, n in orgs:
        cfu = cfu_per_ml(n, loop_ml, dilution_factor)
        b = band_of(cfu, profile["bands"])
        rows.append({"organism": name, "colonies": n, "cfu_ml": cfu,
                     "report": ("< %g CFU/mL (none detected; detection limit = 1 colony)" % lod) if n == 0
                     else "%.3g CFU/mL" % cfu,
                     "band": b["label"] if b else "?", "action": b["action"] if b else "?"})
    growing = [r for r in rows if r["colonies"] > 0]
    flags = []
    mixed_min = profile.get("mixed_min_species")
    verdict = "SEE PER-ORGANISM BAND"
    if mixed_min and len(growing) >= mixed_min:
        verdict = "MIXED GROWTH"
        flags.append("%d species growing (>= %d) -> report 'Mixed bacterial growth', likely contamination; "
                     "request a new specimen, do not ID/AST" % (len(growing), mixed_min))
    elif len(growing) == 2:
        top = max(growing, key=lambda r: r["colonies"])
        flags.append("2 species: report both, AST the predominant one only (%s)" % top["organism"])
    if not growing:
        verdict = "NO GROWTH"
    sym_min = profile.get("symptomatic_single_uropathogen_min")
    if sym_min is not None and verdict != "MIXED GROWTH":
        if symptoms == "yes" and len(growing) == 1 and growing[0]["cfu_ml"] >= sym_min:
            flags.append("symptomatic + single organism at %.3g >= %g CFU/mL -> significant despite being below the "
                         "screening cutoff (card FORK 3)" % (growing[0]["cfu_ml"], sym_min))
            verdict = "SIGNIFICANT (symptomatic)"
        elif symptoms == "unknown":
            flags.append("symptom status unknown: the 1e5 band is a screening/asymptomatic cutoff; a symptomatic "
                         "patient can be significant from %g CFU/mL (card FORK 3) - ask before calling it" % sym_min)
    return {"loop_ml": loop_ml, "dilution_factor": dilution_factor, "detection_limit_cfu_ml": lod,
            "rows": rows, "verdict": verdict, "flags": flags, "cutoffs_from": profile.get("_from", "flags")}


# ---------------------------------------------------------------- blood culture
def classify(organism, flora):
    """Return (class, matched term). Overrides first, then classical, then skin flora; else 'other'."""
    def hit(term):
        return re.search(r"\b" + re.escape(term) + r"\b", organism, re.IGNORECASE)
    for term, cls in sorted(flora.get("overrides", {}).items(), key=lambda kv: -len(kv[0])):
        if hit(term):
            return cls, term
    for term in flora.get("classical", []):
        if hit(term):
            return "classical", term
    for term in flora.get("skin_flora", []):
        if hit(term):
            return "skin-flora", term
    return "other", None


def blood(org_class, positive, drawn, line=False, clinical=False):
    """Contaminant-vs-pathogen checklist (card FORK 3; CLINMICRO1 §1, §4, trap #1)."""
    if drawn < 1 or positive < 1 or positive > drawn:
        raise ValueError("need 1 <= positive <= drawn")
    if org_class == "classical":
        return {"verdict": "SIGNIFICANT", "why": "classical pathogen (never normal flora) -> report immediately"}
    if org_class == "other":
        return {"verdict": "SIGNIFICANT", "why": "blood is a sterile site; a non-skin-flora organism here is a pathogen "
                "-> report + correlate (normal flora of one site = pathogen of another)"}
    if org_class != "skin-flora":
        raise ValueError("unknown class %r" % org_class)
    if drawn < 2:
        return {"verdict": "INDETERMINATE", "why": "skin flora in the only culture drawn: one culture cannot separate "
                "contaminant from true bacteremia -> ask for a repeat/second culture + clinical correlation"}
    if positive == 1:
        return {"verdict": "LIKELY CONTAMINANT", "why": "skin flora in 1 of %d cultures -> suspect contamination; "
                "do not report as the pathogen, follow SOP for the comment" % drawn}
    if line or clinical:
        return {"verdict": "CORRELATE - possibly significant", "why": "skin flora in %d of %d cultures + %s -> may be "
                "real; ID + AST per SOP and tell the clinician" % (positive, drawn,
                                                                    "line/prosthesis" if line else "compatible clinical picture")}
    return {"verdict": "CORRELATE - possibly significant", "why": "skin flora in %d of %d cultures but no line/prosthesis/"
            "clinical data given -> ask before calling it real" % (positive, drawn)}


# ---------------------------------------------------------------- CLI
def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("sputum", help="sputum acceptability screen")
    p.add_argument("--sec", type=float, required=True, help="squamous epithelial cells per LPF")
    p.add_argument("--pmn", type=float, required=True, help="neutrophils per LPF")
    p.add_argument("--cutoffs", help="JSON cutoffs file (see data/)")
    p.add_argument("--profile", help="profile name inside --cutoffs")
    p.add_argument("--sec-accept-below", type=float)
    p.add_argument("--sec-reject-above", type=float)
    p.add_argument("--pmn-above", type=float)

    p = sub.add_parser("count", help="colony count -> CFU/mL + band")
    p.add_argument("--org", action="append", required=True, help="'NAME=COLONIES', repeat per organism")
    p.add_argument("--loop-ml", type=float, required=True, help="calibrated loop volume in mL (0.001 or 0.01)")
    p.add_argument("--dilution-factor", type=float, default=1.0)
    p.add_argument("--symptoms", choices=["yes", "no", "unknown"], default="unknown")
    p.add_argument("--cutoffs", required=True)
    p.add_argument("--profile", required=True)

    p = sub.add_parser("blood", help="blood-culture contaminant vs pathogen checklist")
    p.add_argument("--organism", required=True)
    p.add_argument("--positive", type=int, required=True, help="number of positive blood cultures (independent draws)")
    p.add_argument("--drawn", type=int, required=True, help="number of blood cultures drawn (independent draws)")
    p.add_argument("--line", action="store_true", help="patient has an intravascular line / prosthesis")
    p.add_argument("--clinical", action="store_true", help="clinical picture compatible with bacteremia")
    p.add_argument("--class", dest="org_class", choices=["skin-flora", "classical", "other"],
                   help="override the organism class")
    p.add_argument("--flora", help="JSON organism-class list (see data/)")

    for _sp in sub.choices.values():  # also accept --json after the subcommand, as the examples show

        _sp.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="print JSON")

    a = ap.parse_args(argv)
    if a.cmd == "sputum":
        if a.cutoffs and a.profile:
            prof = load_profile(a.cutoffs, a.profile, "sputum")
        else:
            prof = {"sec_accept_below": a.sec_accept_below, "sec_reject_above": a.sec_reject_above,
                    "pmn_above": a.pmn_above, "_from": "command-line flags"}
        for k in ("sec_accept_below", "sec_reject_above", "pmn_above"):
            if a.__dict__.get(k) is not None:
                prof[k] = a.__dict__[k]
            if prof.get(k) is None:
                raise SystemExit("missing cutoff %s: pass your SOP value (--%s) or --cutoffs + --profile"
                                 % (k, k.replace("_", "-")))
        res = sputum(a.sec, a.pmn, prof["sec_accept_below"], prof["sec_reject_above"], prof["pmn_above"])
        res.update({"sec": a.sec, "pmn": a.pmn, "cutoffs": {k: prof[k] for k in
                    ("sec_accept_below", "sec_reject_above", "pmn_above")}, "cutoffs_from": prof["_from"]})
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
            return 0
        print("SEC/LPF %-8g PMN/LPF %-8g" % (a.sec, a.pmn))
        print("rule: REJECT if SEC > %(sec_reject_above)g | ACCEPT if SEC < %(sec_accept_below)g and PMN > %(pmn_above)g"
              " | else BORDERLINE" % res["cutoffs"])
        print("cutoffs from: %s" % res["cutoffs_from"])
        print("-> %s: %s" % (res["verdict"], res["why"]))
    elif a.cmd == "count":
        prof = load_profile(a.cutoffs, a.profile, "count")
        res = count([parse_org(s) for s in a.org], a.loop_ml, prof, a.dilution_factor, a.symptoms)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
            return 0
        print("loop %g mL x dilution %g -> 1 colony = %g CFU/mL" % (a.loop_ml, a.dilution_factor,
                                                                     res["detection_limit_cfu_ml"]))
        print("%-26s %9s %14s  %-16s %s" % ("organism", "colonies", "CFU/mL", "band", "action"))
        for r in res["rows"]:
            print("%-26s %9g %14s  %-16s %s" % (r["organism"][:26], r["colonies"], "%.3g" % r["cfu_ml"],
                                                r["band"], r["action"]))
            if r["colonies"] == 0:
                print("%28s report as: %s" % ("", r["report"]))
        for f in res["flags"]:
            print("FLAG: " + f)
        print("cutoffs from: %s" % res["cutoffs_from"])
        print("-> %s" % res["verdict"])
    else:
        flora = {}
        if a.flora:
            with open(a.flora, encoding="utf-8") as f:
                flora = json.load(f)
        if a.org_class:
            cls, term = a.org_class, "--class"
        elif flora:
            cls, term = classify(a.organism, flora)
        else:
            raise SystemExit("pass --class or --flora so the organism can be classed")
        res = blood(cls, a.positive, a.drawn, a.line, a.clinical)
        res.update({"organism": a.organism, "class": cls, "class_from": term or "no list match -> 'other'",
                    "positive": a.positive, "drawn": a.drawn})
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
            return 0
        print("organism %s | class %s (from: %s) | positive %d of %d drawn | line=%s clinical=%s"
              % (a.organism, cls, res["class_from"], a.positive, a.drawn, a.line, a.clinical))
        if cls == "other" and not a.org_class:
            print("NOTE: no list match -> treated as 'other' (sterile-site pathogen). Check spelling or pass --class.")
        print("NOTE: count independent draws, not two bottles of one venipuncture [general practice].")
        print("-> %s: %s" % (res["verdict"], res["why"]))
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
