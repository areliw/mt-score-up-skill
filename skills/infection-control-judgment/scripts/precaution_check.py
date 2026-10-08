#!/usr/bin/env python3
"""precaution_check - check a proposed isolation/PPE plan (or a don/doff order) against the card's rules.

Black-box tool for infection-control-judgment. Run --help first; read the source only if a result
looks wrong. It does not choose for you - it lists what the transmission route(s) require per the
card and marks each part of YOUR plan PASS / WARN / FAIL. ADVISORY ONLY: the hospital IPC policy
and IC committee decide.

Rules (all from skills/infection-control-judgment.md; the card was checked against CDC/HICPAC -
there is no course digest behind it, see CHANGELOG)
  mask   airborne OR aerosol-generating procedure -> N95 · droplet -> surgical mask (N95 also OK)
         (Fork 2 + Fork 3; trap #1: surgical mask for airborne)
  room   airborne -> negative pressure (AIIR); positive pressure with an airborne source = FAIL
         (Fork 4 "swapped = disaster") · immunocompromised host (no airborne source) -> positive
         pressure; negative = FAIL (swapped) · contact only -> single room preferred or cohort;
         negative pressure = WARN (AIIR reserved for airborne) · airborne source in an
         immunocompromised host = CONFLICT, the card does not cover it -> IPC decision
  gloves/gown  contact -> both (Fork 3)
  hands  alcohol rub by default; soap + water for C. difficile / spores / norovirus / visibly
         soiled hands (Fork 1)
  order  don: gown -> mask -> gloves (gloves last) · doff: gloves first ... hand hygiene last
         (Fork 2; Fork 1 "hand hygiene every time after removing gloves")

Agent names map to routes through a JSON you can edit (data/agent_routes_teaching.json = the
card's own examples); or give --route directly.

Examples (run from the skill folder)
  python scripts/precaution_check.py plan --map data/agent_routes_teaching.json --agent tuberculosis --mask surgical --room positive --hand alcohol
  python scripts/precaution_check.py plan --route contact --gloves --gown --mask none --room negative --hand alcohol
  python scripts/precaution_check.py sequence --don gown,mask,gloves --doff gloves,gown,mask,hand-hygiene
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

ADVISORY = "ADVISORY: decision support only - follow the hospital IPC policy and the IC committee."
MASK_RANK = {"none": 0, "surgical": 1, "n95": 2}


def routes_for(agents, amap):
    routes, soap = set(), False
    table = {k.lower(): v for k, v in amap.get("agents", {}).items()}
    soap_list = {s.lower() for s in amap.get("soap_and_water_agents", [])}
    for a in agents:
        key = a.lower()
        if key not in table and key in soap_list:
            soap = True  # hand-hygiene rule known (Fork 1) but the card gives no route -> pass --route too
            continue
        if key not in table:
            raise SystemExit("agent %r not in the map (have: %s) - add it or pass --route"
                             % (a, ", ".join(sorted(amap.get("agents", {})))))
        routes.update(table[key])
        soap = soap or key in soap_list
    return routes, soap


def required_mask(routes, agp):
    if "airborne" in routes or agp:
        return "n95"
    if "droplet" in routes:
        return "surgical"
    return "none"


def room_check(routes, protective_host, room):
    """Return (status, why)."""
    if "airborne" in routes and protective_host:
        return "CONFLICT", ("airborne source in an immunocompromised host: negative vs positive pressure conflict - "
                            "not covered by the card, escalate to IPC")
    if "airborne" in routes:
        if room == "negative":
            return "PASS", "airborne -> negative-pressure room (AIIR)"
        if room == "positive":
            return "FAIL", "DANGER: positive pressure blows an airborne agent out into the ward (rooms swapped)"
        return "FAIL", "airborne needs a negative-pressure room (AIIR), not %s" % room
    if protective_host:
        if room == "positive":
            return "PASS", "immunocompromised host -> positive pressure keeps organisms out"
        if room == "negative":
            return "FAIL", "swapped: negative pressure is for airborne sources; this host needs positive pressure"
        return "FAIL", "immunocompromised host (protective environment) needs positive pressure, not %s" % room
    if room == "negative":
        return "WARN", "negative pressure (AIIR) is reserved for airborne agents - this case does not need it"
    if "contact" in routes and room not in ("single", "cohort"):
        return "WARN", "contact precautions: single room preferred, or cohort"
    return "PASS", "no pressure requirement for these routes"


def check_plan(routes, plan, agp=False, protective_host=False, soap=False):
    rows = []
    need_mask = required_mask(routes, agp)
    have = plan.get("mask", "none")
    rows.append(("mask", need_mask, have, "PASS" if MASK_RANK[have] >= MASK_RANK[need_mask] else "FAIL",
                 "airborne/aerosol procedure -> N95; droplet -> surgical" if need_mask != "none" else "no mask rule"))
    st, why = room_check(routes, protective_host, plan.get("room", "standard"))
    rows.append(("room", "-", plan.get("room", "standard"), st, why))
    contact = "contact" in routes
    for item in ("gloves", "gown"):
        ok = plan.get(item, False) or not contact
        rows.append((item, "yes" if contact else "standard precautions", "yes" if plan.get(item) else "no",
                     "PASS" if ok else "FAIL", "contact precautions need gloves + gown" if contact else ""))
    need_hand = "soap" if (soap or plan.get("soiled")) else "alcohol"
    hand = plan.get("hand", "alcohol")
    hand_ok = hand == "soap" or need_hand == "alcohol"
    rows.append(("hand hygiene", need_hand, hand, "PASS" if hand_ok else "FAIL",
                 "spores (C. difficile)/norovirus/visibly soiled -> soap + water; alcohol does not remove spores"
                 if need_hand == "soap" else "alcohol rub is the default"))
    statuses = [r[3] for r in rows]
    verdict = "FAIL" if "FAIL" in statuses else ("CONFLICT" if "CONFLICT" in statuses else
                                                 ("WARN" if "WARN" in statuses else "PASS"))
    return {"routes": sorted(routes), "aerosol_procedure": agp, "protective_host": protective_host,
            "rows": [dict(zip(("item", "required", "proposed", "status", "why"), r)) for r in rows],
            "verdict": verdict}


def normalise_item(x):
    x = x.strip().lower()
    if x in ("n95", "respirator", "surgical-mask", "surgical mask", "mask"):
        return "mask"
    if x in ("hand-hygiene", "hand hygiene", "handwash", "hand-rub", "hands"):
        return "hand-hygiene"
    if x in ("glove", "gloves"):
        return "gloves"
    return x


def check_sequence(don, doff):
    don = [normalise_item(x) for x in don]
    doff = [normalise_item(x) for x in doff]
    problems = []
    if "gloves" in don and don[-1] != "gloves":
        problems.append("donning: gloves must go on LAST")
    order = [x for x in don if x in ("gown", "mask", "gloves")]
    if order != sorted(order, key=["gown", "mask", "gloves"].index):
        problems.append("donning order should be gown -> mask -> gloves (got %s)" % " -> ".join(order))
    if doff and "gloves" in doff and doff[0] != "gloves":
        problems.append("doffing: gloves must come off FIRST (most contaminated)")
    if doff and doff[-1] != "hand-hygiene":
        problems.append("doffing must END with hand hygiene (hand hygiene after removing gloves)")
    return {"don": don, "doff": doff, "problems": problems, "verdict": "FAIL" if problems else "PASS"}


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan", help="check an isolation/PPE plan")
    p.add_argument("--agent", action="append", default=[], help="agent name from --map (repeatable)")
    p.add_argument("--map", help="agent -> routes JSON (see data/)")
    p.add_argument("--route", action="append", default=[], choices=["contact", "droplet", "airborne"])
    p.add_argument("--aerosol-procedure", action="store_true", help="intubation / suction / nebuliser etc.")
    p.add_argument("--immunocompromised-host", action="store_true", help="BMT / neutropenia: protective environment")
    p.add_argument("--soiled", action="store_true", help="hands visibly soiled")
    p.add_argument("--mask", choices=["none", "surgical", "n95"], default="none")
    p.add_argument("--room", choices=["standard", "single", "cohort", "negative", "positive"], default="standard")
    p.add_argument("--gloves", action="store_true")
    p.add_argument("--gown", action="store_true")
    p.add_argument("--hand", choices=["alcohol", "soap"], default="alcohol")
    p = sub.add_parser("sequence", help="check a don/doff order")
    p.add_argument("--don", required=True, help="comma list, e.g. gown,mask,gloves")
    p.add_argument("--doff", required=True, help="comma list, e.g. gloves,gown,mask,hand-hygiene")
    a = ap.parse_args(argv)
    if a.cmd == "plan":
        routes, soap = set(a.route), False
        if a.agent:
            if not a.map:
                raise SystemExit("--agent needs --map (or pass --route)")
            with open(a.map, encoding="utf-8") as f:
                r2, soap = routes_for(a.agent, json.load(f))
            routes |= r2
        if not routes and not a.immunocompromised_host:
            raise SystemExit("give at least one --agent or --route (or --immunocompromised-host)")
        plan = {"mask": a.mask, "room": a.room, "gloves": a.gloves, "gown": a.gown, "hand": a.hand, "soiled": a.soiled}
        res = check_plan(routes, plan, a.aerosol_procedure, a.immunocompromised_host, soap)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
            return 0
        print("routes: %s | aerosol procedure: %s | immunocompromised host: %s"
              % (", ".join(res["routes"]) or "-", a.aerosol_procedure, a.immunocompromised_host))
        print("%-13s %-22s %-10s %-9s %s" % ("item", "required", "proposed", "status", "why"))
        for r in res["rows"]:
            print("%-13s %-22s %-10s %-9s %s" % (r["item"], r["required"], r["proposed"], r["status"], r["why"]))
        print("NOTE: standard precautions apply to every patient and specimen on top of this.")
        print("-> PLAN %s" % res["verdict"])
    else:
        res = check_sequence(a.don.split(","), a.doff.split(","))
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
            return 0
        print("don : %s" % " -> ".join(res["don"]))
        print("doff: %s" % " -> ".join(res["doff"]))
        for pr in res["problems"]:
            print("FAIL: " + pr)
        print("-> SEQUENCE %s" % res["verdict"])
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
