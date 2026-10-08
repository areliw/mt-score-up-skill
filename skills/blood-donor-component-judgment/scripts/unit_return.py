#!/usr/bin/env python3
"""unit_return - can an issued unit that came back be returned to stock? Time AND temperature.

Black-box tool for blood-donor-component-judgment. Run --help first; read the source only if needed.
Source: card blood-donor-component-judgment Fork 6 - a unit that left controlled storage may go back
to stock ONLY if it is still inside the SOP's time AND temperature limits; never judge on time alone
when the cold chain may have broken ("it still feels cold" is not a measurement). Transport ranges
in the 512303 digest §10.6 (e.g. RBC 1-10 C; platelets 20-24 C; thawed plasma used within 4 h, never
refrozen) are teaching values: the limits are REQUIRED arguments, there are no defaults.
Rules the tool enforces:
  * time out of controlled storage <= --max-minutes   (unknown time = not accepted)
  * temperature on return within --temp-range LO:HI   (not measured = not accepted)
  * --integrity compromised (leak, broken seal, visible change) = not accepted
ADVISORY ONLY. Disposition belongs to the blood bank SOP and the responsible MT.

Examples (limits are YOUR SOP's; 30 min and 1-10 C shown only as an illustration)
  python unit_return.py --component RBC --minutes-out 20 --max-minutes 30 --temp-c 6 --temp-range 1:10
  python unit_return.py --component RBC --minutes-out 20 --max-minutes 30 --temp-range 1:10
  python unit_return.py --component RBC --minutes-out 25 --max-minutes 30 --temp-c 12 --temp-range 1:10 --json
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

ADVISORY = "ADVISORY: decision support only - disposition per blood bank SOP and the responsible MT."


def decide(minutes_out, max_minutes, temp_c, temp_lo, temp_hi, integrity="not recorded"):
    reasons = []
    time_ok = minutes_out is not None and minutes_out <= max_minutes
    if minutes_out is None:
        reasons.append("time out of controlled storage not known")
    elif not time_ok:
        reasons.append("out %g min > SOP limit %g min" % (minutes_out, max_minutes))
    temp_ok = temp_c is not None and temp_lo <= temp_c <= temp_hi
    if temp_c is None:
        reasons.append("temperature on return not measured - cold chain not documented")
    elif not temp_ok:
        reasons.append("temperature %g C outside SOP range %g-%g C" % (temp_c, temp_lo, temp_hi))
    integrity_ok = integrity != "compromised"
    if not integrity_ok:
        reasons.append("unit integrity compromised")
    accept = time_ok and temp_ok and integrity_ok
    return {"minutes_out": minutes_out, "max_minutes": max_minutes, "temp_c": temp_c,
            "temp_range": [temp_lo, temp_hi], "integrity": integrity, "time_ok": time_ok, "temp_ok": temp_ok,
            "decision": "RETURN TO STOCK" if accept else "QUARANTINE - do not re-issue; disposition per SOP",
            "reasons": reasons or ["time and temperature both within SOP limits"]}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--component", default="unit", help="label only (e.g. RBC, platelet, thawed plasma)")
    ap.add_argument("--minutes-out", type=float, help="minutes outside controlled storage")
    ap.add_argument("--max-minutes", type=float, required=True, help="SOP time limit (no default)")
    ap.add_argument("--temp-c", type=float, help="unit temperature measured on return")
    ap.add_argument("--temp-range", required=True, help="SOP acceptable range LO:HI in C (no default)")
    ap.add_argument("--integrity", choices=["ok", "compromised", "not recorded"], default="not recorded")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        lo, hi = (float(x) for x in a.temp_range.split(":"))
        if lo > hi:
            raise ValueError
    except ValueError:
        ap.error("--temp-range must be LO:HI, e.g. 1:10")
    res = decide(a.minutes_out, a.max_minutes, a.temp_c, lo, hi, a.integrity)
    res["component"] = a.component
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("component   : %s" % a.component)
    print("time out    : %s min (limit %g)  -> %s" % ("?" if a.minutes_out is None else "%g" % a.minutes_out,
                                                       a.max_minutes, "ok" if res["time_ok"] else "NOT OK"))
    print("temperature : %s C (range %g-%g) -> %s" % ("?" if a.temp_c is None else "%g" % a.temp_c, lo, hi,
                                                     "ok" if res["temp_ok"] else "NOT OK"))
    print("integrity   : %s" % a.integrity)
    print("DECISION    : %s" % res["decision"])
    for r in res["reasons"]:
        print("  - %s" % r)
    if a.integrity == "not recorded":
        print("  note: visual/seal check per SOP was not recorded here")
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
