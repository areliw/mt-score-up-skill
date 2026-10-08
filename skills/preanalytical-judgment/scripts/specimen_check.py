#!/usr/bin/env python3
"""specimen_check — run one specimen (or a list) through a pre-analytical rejection checklist and
say which analytes must NOT be reported, and whether to accept, hold or recollect.

Black-box tool for preanalytical-judgment. Run --help first; read the source only if a check fails.
Rules come from the preanalytical-judgment card (no other source):
  Fork 5  identity: 2 identifiers, label at the bedside, never pre-label; mismatch = recollect
  Fork 3  hemolysis -> K, LDH, AST, Mg, phosphate falsely high + troponin/immunoassay interference;
          lipemia -> Hb / turbidity-sensitive analytes; icterus -> bilirubin-sensitive methods.
          reject vs report-with-comment is decided by HIL index + SOP -> index limits are ARGUMENTS
  Fork 2  citrate tube 1:9 (underfill -> PT/aPTT falsely long); Hct > 55% -> citrate must be adjusted
  Fork 4  IV line above the site -> dilution + spike; tourniquet should be < 1 min
  Fork 6  ammonia/lactate/blood gas on ice; bilirubin protected from light; past stability -> reject
  Trap #1 re-running the same tube does not fix hemolysis/clot/wrong tube/IV contamination
Lab-specific limits (HIL index cut-offs, min fill %, stability hours) are never built in: pass them.
A field you do not supply is reported NOT CHECKED - it is never treated as a pass.
ADVISORY ONLY: reject/accept follows the lab SOP and the responsible MT.

Input: JSON object or list of objects. Keys (all optional):
  id, id_match (bool), identifiers (int), labeled_at ("bedside"|"counter"|"pre-labeled"),
  tube, tests [..], hemolysis_index, icterus_index, lipemia_index, hemolyzed (bool), clotted (bool),
  fill_pct, hct, hours_since_collection, transport ("ice"|"room"), light_protected (bool),
  iv_line ("above"|"below"|"opposite-arm"|"none"), tourniquet_min

Examples
  python specimen_check.py ../data/specimen_example.json --hi-limit 50
  python specimen_check.py ../data/specimen_example.json --hi-limit 50 --min-fill 90 --max-hours 4 --json
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

HEMOLYSIS_AFFECTED = {"k", "ldh", "ast", "mg", "phosphate", "troponin"}   # card Fork 3
LIPEMIA_AFFECTED = {"hb"}                                                   # card Fork 3 (turbidity)
ICTERUS_AFFECTED = {"bilirubin", "creatinine"}                              # card Fork 3 (+ clinchem Jaffe)
COAG_TESTS = {"pt", "aptt", "ptt", "inr", "tt", "fibrinogen"}
ON_ICE = {"ammonia", "lactate", "blood-gas", "abg"}                         # card Fork 6
LIGHT = {"bilirubin"}                                                       # card Fork 6

SEVERITY = {"PASS": 0, "NOT CHECKED": 1, "COMMENT": 2, "HOLD": 3, "RECOLLECT": 4, "REJECT": 5}


def item(crit, status, msg, blocks=()):
    return {"criterion": crit, "status": status, "msg": msg, "do_not_report": sorted(blocks)}


def check(sp, hi_limit=None, ii_limit=None, li_limit=None, min_fill=None, max_hours=None):
    shown = {t.strip().lower(): t.strip() for t in sp.get("tests", [])}   # keep the user's spelling
    tests = set(shown)
    tube = (sp.get("tube") or "").lower()
    out = []
    # ---- identity (Fork 5): unknown identity can never be cleared
    if sp.get("id_match") is None:
        out.append(item("identity", "HOLD", "label-vs-request match not recorded -> cannot clear identity", tests))
    elif sp["id_match"] is False:
        out.append(item("identity", "REJECT", "label does not match request -> recollect; never relabel "
                                              "(wrong-blood-in-tube risk)", tests))
    else:
        out.append(item("identity", "PASS", "label matches request"))
    n_id = sp.get("identifiers")
    if n_id is None:
        out.append(item("identifiers", "HOLD", "number of identifiers not recorded", tests))
    elif n_id < 2:
        out.append(item("identifiers", "REJECT", "%d identifier(s) < 2 -> recollect" % n_id, tests))
    else:
        out.append(item("identifiers", "PASS", "%d identifiers" % n_id))
    where = sp.get("labeled_at")
    if where is None:
        out.append(item("labeling", "NOT CHECKED", "where the tube was labelled not recorded"))
    elif where != "bedside":
        out.append(item("labeling", "REJECT", "labelled at %s -> wrong-blood-in-tube risk; recollect" % where, tests))
    else:
        out.append(item("labeling", "PASS", "labelled at the bedside"))
    # ---- HIL (Fork 3)
    hem = sp.get("hemolyzed")
    hi = sp.get("hemolysis_index")
    if hi is not None:
        if hi_limit is None:
            out.append(item("hemolysis", "NOT CHECKED", "hemolysis_index %s given but no --hi-limit (lab SOP)" % hi))
            hem = None
        else:
            hem = hi > hi_limit
    if hem is None and hi is None:
        out.append(item("hemolysis", "NOT CHECKED", "no hemolysis data"))
    elif hem:
        blocked = tests & HEMOLYSIS_AFFECTED
        if blocked:
            out.append(item("hemolysis", "RECOLLECT", "hemolyzed -> %s falsely high/interfered: do not report; "
                                                      "re-running this tube will not fix it"
                            % ", ".join(shown[t] for t in sorted(blocked)), blocked))
        else:
            out.append(item("hemolysis", "COMMENT", "hemolyzed, none of the ordered tests is on the hemolysis list "
                                                    "-> report per SOP with comment"))
    elif hem is False:
        out.append(item("hemolysis", "PASS", "not hemolyzed" + (" (index %s <= %s)" % (hi, hi_limit) if hi is not None else "")))
    for crit, idx, lim, affected in (("icterus", sp.get("icterus_index"), ii_limit, ICTERUS_AFFECTED),
                                     ("lipemia", sp.get("lipemia_index"), li_limit, LIPEMIA_AFFECTED)):
        if idx is None:
            continue
        if lim is None:
            out.append(item(crit, "NOT CHECKED", "%s index %s given but no limit argument" % (crit, idx)))
        elif idx > lim:
            blocked = tests & affected
            status = "HOLD" if blocked else "COMMENT"
            out.append(item(crit, status, "%s index %s > %s -> %s" % (crit, idx, lim, (
                "check method interference for " + ", ".join(sorted(blocked))) if blocked else "report per SOP with comment"),
                blocked))
        else:
            out.append(item(crit, "PASS", "%s index %s <= %s" % (crit, idx, lim)))
    # ---- clot / fill / Hct (Fork 2)
    if sp.get("clotted"):
        out.append(item("clot", "REJECT", "clotted -> re-running will not fix it; recollect", tests))
    elif sp.get("clotted") is False:
        out.append(item("clot", "PASS", "no clot"))
    if tube in ("citrate", "blue") or tests & COAG_TESTS:
        fill = sp.get("fill_pct")
        if fill is None:
            out.append(item("citrate fill", "NOT CHECKED", "fill_pct not recorded for a citrate tube"))
        elif min_fill is None:
            out.append(item("citrate fill", "NOT CHECKED", "fill %s%% but no --min-fill (lab SOP)" % fill))
        elif fill < min_fill:
            out.append(item("citrate fill", "REJECT", "underfilled %s%% < %s%% -> excess citrate -> PT/aPTT "
                                                      "falsely long" % (fill, min_fill), tests & COAG_TESTS))
        else:
            out.append(item("citrate fill", "PASS", "fill %s%% >= %s%%" % (fill, min_fill)))
        hct = sp.get("hct")
        if hct is not None and hct > 55:
            out.append(item("hct", "HOLD", "Hct %s%% > 55%% -> citrate volume must be adjusted (formula: lab SOP / "
                                           "CLSI, not this script)" % hct, tests & COAG_TESTS))
    # ---- collection site (Fork 4)
    iv = sp.get("iv_line")
    if iv == "above":
        out.append(item("IV line", "RECOLLECT", "drawn above an IV line -> dilution + spike; recollect from the "
                                                "opposite arm / below the line", tests))
    elif iv in ("below", "opposite-arm", "none"):
        out.append(item("IV line", "PASS", "site %s" % iv))
    tq = sp.get("tourniquet_min")
    if tq is not None and tq > 1:
        out.append(item("tourniquet", "COMMENT", "tourniquet %s min > 1 -> hemoconcentration + K/lactate leak; "
                                                 "interpret with care" % tq))
    # ---- transport / stability (Fork 6)
    need_ice = tests & ON_ICE
    if need_ice:
        if sp.get("transport") is None:
            out.append(item("transport", "NOT CHECKED", "%s need ice; transport not recorded" % ", ".join(sorted(need_ice))))
        elif sp["transport"] != "ice":
            out.append(item("transport", "RECOLLECT", "%s not sent on ice" % ", ".join(sorted(need_ice)), need_ice))
        else:
            out.append(item("transport", "PASS", "sent on ice"))
    need_dark = tests & LIGHT
    if need_dark and sp.get("light_protected") is False:
        out.append(item("light", "HOLD", "bilirubin not protected from light", need_dark))
    hrs = sp.get("hours_since_collection")
    if hrs is not None:
        if max_hours is None:
            out.append(item("stability", "NOT CHECKED", "%s h since collection but no --max-hours (analyte "
                                                        "stability table of the lab)" % hrs))
        elif hrs > max_hours:
            out.append(item("stability", "REJECT", "%s h > %s h stability -> reject/recollect" % (hrs, max_hours), tests))
        else:
            out.append(item("stability", "PASS", "%s h <= %s h" % (hrs, max_hours)))
    worst = max(out, key=lambda r: SEVERITY[r["status"]])["status"]
    verdict = {"PASS": "ACCEPT", "NOT CHECKED": "ACCEPT (some criteria NOT CHECKED)",
               "COMMENT": "ACCEPT WITH COMMENT"}.get(worst, worst)
    blocked = {t for r in out for t in r["do_not_report"]}
    for r in out:
        r["do_not_report"] = [shown[t] for t in r["do_not_report"]]
    return {"id": sp.get("id"), "verdict": verdict, "do_not_report": sorted(shown[t] for t in blocked),
            "reportable": sorted(shown[t] for t in tests - blocked), "checks": out}


def main(argv=None):
    try:  # never crash a non-UTF-8 console (e.g. Thai cp874) on the section sign / Thai text
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json_file")
    ap.add_argument("--hi-limit", type=float, help="hemolysis index above which the specimen counts as hemolyzed (SOP)")
    ap.add_argument("--ii-limit", type=float, help="icterus index limit (SOP)")
    ap.add_argument("--li-limit", type=float, help="lipemia index limit (SOP)")
    ap.add_argument("--min-fill", type=float, help="minimum citrate fill %% accepted by the SOP")
    ap.add_argument("--max-hours", type=float, help="stability limit in hours for the ordered analytes (SOP)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    with open(a.json_file, encoding="utf-8") as f:
        data = json.load(f)
    specimens = data if isinstance(data, list) else [data]
    res = [check(s, a.hi_limit, a.ii_limit, a.li_limit, a.min_fill, a.max_hours) for s in specimens]
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    for r in res:
        print("specimen %s" % r["id"])
        print("  %-13s %-12s %s" % ("criterion", "status", "detail"))
        for c in r["checks"]:
            print("  %-13s %-12s %s" % (c["criterion"], c["status"], c["msg"]))
        print("  DO NOT REPORT (now): %s" % (", ".join(r["do_not_report"]) or "-"))
        print("  reportable:          %s" % (", ".join(r["reportable"]) or "-"))
        print("  VERDICT: %s" % r["verdict"])
    print("ADVISORY: decision support only - reject/accept per the lab SOP; confirm with the responsible MT.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
