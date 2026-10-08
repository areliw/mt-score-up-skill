#!/usr/bin/env python3
"""hbv_panel — read an HBV serology panel as ONE pattern, never marker by marker.

Black-box tool for immunoassay-judgment. Run --help first; read the source only if a case looks wrong.
Rules come from the skill card (FORK 2 HBV table; "Viral serology" HBV-window line; trap #5) and the
506202 Immunology digest §14 (HBsAg, anti-HBs/anti-HBc). Rows NOT in the card table are labelled
[ทั่วไป] (general teaching) or ATYPICAL -> refer; the tool never invents a diagnosis for them.
ADVISORY ONLY: the report belongs to the lab SOP, the authorised signatory and the clinician.

Markers (pos / neg / na = not done)
  --hbsag        HBsAg
  --anti-hbc     total anti-HBc
  --anti-hbs     anti-HBs
  --igm-anti-hbc IgM anti-HBc        (optional; splits acute vs chronic, flags the core window)
  --hbsag-months months HBsAg has been positive (optional; card: chronic = HBsAg+ > 6 months)

Card table (HBsAg / anti-HBc total / anti-HBs)
  + / + (IgM+) / -  -> acute infection
  + / + (IgM-) / -  -> chronic (HBsAg+ > 6 months)
  - / +        / +  -> recovered (natural immunity)
  - / -        / +  -> vaccinated (no anti-HBc)
  - / +        / -  -> core-only: window / occult / false-positive -> follow-up
The decider between vaccinated and recovered is anti-HBc. HBsAg+ alone cannot tell acute vs chronic.

Examples
  python hbv_panel.py --hbsag neg --anti-hbc pos --anti-hbs pos
  python hbv_panel.py --hbsag pos --anti-hbc pos --anti-hbs neg --igm-anti-hbc pos
  python hbv_panel.py --csv ../data/hbv_teaching_cases.csv
  python hbv_panel.py --hbsag neg --anti-hbc na --anti-hbs pos --json
"""
import argparse
import csv
import json
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

VALUES = {"pos": "pos", "+": "pos", "positive": "pos", "reactive": "pos", "r": "pos",
          "neg": "neg", "-": "neg", "negative": "neg", "nonreactive": "neg", "nr": "neg",
          "na": "na", "": "na", "nd": "na", "unknown": "na", "?": "na"}


def norm(v):
    key = (v or "").strip().lower()
    if key not in VALUES:
        raise ValueError("marker value %r: use pos / neg / na" % v)
    return VALUES[key]


def interpret(hbsag, anti_hbc, anti_hbs, igm=None, hbsag_months=None):
    """Return a dict: pattern, status, provenance, next_step, notes. Inputs already normalised."""
    igm = igm or "na"
    pattern = "HBsAg %s / anti-HBc %s / anti-HBs %s / IgM anti-HBc %s" % (hbsag, anti_hbc, anti_hbs, igm)
    notes = []

    def out(status, prov, nxt, extra=None):
        return {"pattern": pattern, "status": status, "provenance": prov, "next_step": nxt,
                "notes": notes + (extra or [])}

    if hbsag == "na":
        return out("CANNOT INTERPRET", "card FORK 2", "HBsAg is required to read the panel")

    if hbsag == "pos":
        if anti_hbs == "pos":
            return out("ATYPICAL: HBsAg+ with anti-HBs+", "not in card table",
                       "repeat/confirm both markers; refer to clinician - do not force a category")
        if anti_hbc == "na":
            return out("UNDETERMINED: HBsAg+ alone", "card trap #5",
                       "add total anti-HBc + IgM anti-HBc: HBsAg+ alone does not tell acute vs chronic")
        if anti_hbc == "neg":
            return out("ATYPICAL: HBsAg+ / anti-HBc-", "not in card table",
                       "repeat/confirm HBsAg and follow up; refer - do not force a category")
        # HBsAg+ anti-HBc+ anti-HBs- or na
        if anti_hbs == "na":
            notes.append("anti-HBs not done - card row assumes anti-HBs negative")
        long_course = hbsag_months is not None and hbsag_months > 6
        if igm == "pos" and long_course:
            return out("CONFLICT: IgM anti-HBc+ but HBsAg+ > 6 months", "card rows 1 vs 2 disagree",
                       "do not pick a row - refer to clinician with both facts")
        if igm == "pos":
            return out("ACUTE HBV infection", "card FORK 2 row 1", "report per SOP; clinician follow-up")
        if long_course:
            return out("CHRONIC HBV infection", "card FORK 2 row 2 (HBsAg+ > 6 months)",
                       "report per SOP; clinician follow-up")
        if igm == "neg":
            return out("CHRONIC HBV infection (IgM anti-HBc negative)", "card FORK 2 row 2",
                       "card defines chronic as HBsAg+ > 6 months - confirm duration with clinician")
        return out("UNDETERMINED: acute vs chronic", "card FORK 2 rows 1-2",
                   "need IgM anti-HBc, or HBsAg persistence > 6 months")

    # HBsAg negative
    if anti_hbs == "pos":
        if anti_hbc == "pos":
            return out("RECOVERED (natural immunity)", "card FORK 2 row 3", "report per SOP")
        if anti_hbc == "neg":
            return out("VACCINATED (immune, no anti-HBc)", "card FORK 2 row 4", "report per SOP")
        return out("UNDETERMINED: immune, but vaccinated vs recovered unknown", "card FORK 2 + trap #5",
                   "anti-HBc decides vaccinated (neg) vs recovered (pos) - run anti-HBc")
    if anti_hbs == "na":
        return out("UNDETERMINED: anti-HBs not done", "card FORK 2", "run anti-HBs (and anti-HBc if missing)")
    # HBsAg- anti-HBs-
    if anti_hbc == "pos":
        if igm == "pos":
            return out("CORE WINDOW (acute, between HBsAg loss and anti-HBs)",
                       "card FORK 2 row 5 + viral-serology HBV-window line",
                       "do not report as 'not infected'; clinician follow-up / repeat")
        return out("ISOLATED anti-HBc (core-only)", "card FORK 2 row 5",
                   "needs follow-up: window / occult infection / false-positive cannot be told apart here"
                   + ("" if igm == "neg" else " - add IgM anti-HBc"))
    if anti_hbc == "neg":
        return out("NO HBV MARKER (susceptible) [ทั่วไป]", "not in card table - general teaching",
                   "if exposure was recent, the early window is not excluded -> repeat later",
                   ["negative panel is not a rule-out of very early infection (card iron rule #2)"])
    return out("UNDETERMINED: anti-HBc not done", "card FORK 2 + viral-serology HBV-window line",
               "HBsAg-/anti-HBs- is not 'not infected': run anti-HBc (+ IgM anti-HBc)")


def load_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    cases = []
    for r in rows:
        r = {k.strip().lower(): (v or "").strip() for k, v in r.items()}
        months = r.get("hbsag_months", "")
        cases.append((r.get("id", ""), norm(r["hbsag"]), norm(r["anti_hbc"]), norm(r["anti_hbs"]),
                      norm(r.get("igm_anti_hbc", "")), float(months) if months else None))
    return cases


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hbsag")
    ap.add_argument("--anti-hbc")
    ap.add_argument("--anti-hbs")
    ap.add_argument("--igm-anti-hbc", default="na")
    ap.add_argument("--hbsag-months", type=float)
    ap.add_argument("--csv", help="batch: columns id,hbsag,anti_hbc,anti_hbs[,igm_anti_hbc,hbsag_months]")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.csv:
            cases = load_csv(a.csv)
        else:
            if a.hbsag is None or a.anti_hbc is None or a.anti_hbs is None:
                ap.error("give --hbsag --anti-hbc --anti-hbs (use na for not done), or --csv")
            cases = [("case", norm(a.hbsag), norm(a.anti_hbc), norm(a.anti_hbs), norm(a.igm_anti_hbc),
                      a.hbsag_months)]
    except ValueError as e:
        ap.error(str(e))
    results = [dict(id=c[0], **interpret(*c[1:])) for c in cases]
    if a.json:
        print(json.dumps(results if a.csv else results[0], ensure_ascii=False, indent=1))
        return 0
    for r in results:
        print("%-10s %s" % (r["id"], r["pattern"]))
        print("%-10s -> %s   [%s]" % ("", r["status"], r["provenance"]))
        print("%-10s next: %s" % ("", r["next_step"]))
        for n in r["notes"]:
            print("%-10s note: %s" % ("", n))
    print("ADVISORY: decision support only - confirm with the lab SOP, an authorised signatory and the clinician.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
