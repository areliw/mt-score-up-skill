#!/usr/bin/env python3
"""poct_gate - can this POCT result be used? Checks the card's gates before anyone acts on the number.

Black-box tool for poct-judgment. Run --help first. Gates (each finding prints its card fork/trap):
  Fork 2 / trap 1  QC not passed, operator not competent or competency expired, new lot not verified
                   -> BLOCK (a POCT result is a lab result: same QC + competency as the central lab)
  trap 3           value outside the device's measuring range -> BLOCK numeric result; report as
                   < / > range per SOP and send to the central lab
  Fork 3 (glucose) Hct outside the meter's validated range: HIGH Hct -> glucose falsely LOW,
                   LOW Hct -> falsely HIGH -> BLOCK, use lab / venous
                   GDH-PQQ + maltose / icodextrin (PD fluid) / galactose -> falsely HIGH (fatal insulin
                   overdose reported) -> BLOCK
                   glucose-oxidase + high O2 / arterial sample -> falsely LOW (GDH is O2-insensitive) -> CONFIRM
                   acetaminophen / vitamin C / uric acid -> amperometric interference -> CONFIRM
                   capillary sample in shock / hypotension / oedema / vasopressor -> BLOCK capillary,
                   use venous / blood-gas analyzer
  Fork 4 / trap 4  manual transcription instead of LIS -> CAUTION (not traceable)
  Fork 5 / trap 5  critical value per YOUR policy limits -> NOTIFY + consider central-lab confirmation
All limits are inputs: measuring range and Hct range are the manufacturer's; critical limits and the
competency interval are your institution's. Nothing clinical is hard-coded. ADVISORY ONLY.

Examples
  python poct_gate.py --analyte glucose --value 45 --qc pass --operator-competent --lot-verified \
      --range 20-600 --critical 40-400 --method gdh-pqq --interferent icodextrin
  python poct_gate.py --analyte glucose --value 120 --qc pass --operator-competent --lot-verified \
      --range 20-600 --hct 65 --hct-range 20-60 --json
"""
import argparse
import datetime as dt
import json
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

LEVELS = ["BLOCK", "CONFIRM", "NOTIFY", "CAUTION", "INFO"]
GDH_PQQ_SUGARS = {"maltose", "icodextrin", "galactose"}
AMPEROMETRIC = {"acetaminophen", "paracetamol", "vitamin-c", "ascorbic-acid", "uric-acid"}
POOR_PERFUSION = {"shock", "hypotension", "edema", "oedema", "vasopressor"}


def parse_range(text):
    lo, hi = (float(x) for x in text.replace(" ", "").split("-", 1))
    if lo >= hi:
        raise argparse.ArgumentTypeError("range must be LOW-HIGH with LOW < HIGH")
    return (lo, hi)


def hct_bias(hct, hct_range):
    """Fork 3: direction of glucose-meter error when Hct is outside the meter's validated range."""
    if hct > hct_range[1]:
        return "falsely LOW"
    if hct < hct_range[0]:
        return "falsely HIGH"
    return None


def add(out, level, fork, finding, action):
    out.append({"level": level, "fork": fork, "finding": finding, "action": action})


def evaluate(s):
    out = []
    today = s.get("today") or dt.date.today()
    if s.get("qc") != "pass":
        add(out, "BLOCK", "Fork 2", "QC %s" % (s.get("qc") or "not recorded"),
            "no patient result from a device whose QC has not passed - fix QC first")
    if not s.get("operator_competent"):
        add(out, "BLOCK", "Fork 2", "operator competency not confirmed", "result not usable; competent operator repeats")
    if s.get("competency_date") and s.get("competency_interval_days"):
        due = s["competency_date"] + dt.timedelta(days=s["competency_interval_days"])
        if today > due:
            add(out, "BLOCK", "Fork 2", "competency expired on %s" % due.isoformat(),
                "re-assess the operator (interval = your policy)")
    if not s.get("lot_verified"):
        add(out, "BLOCK", "Fork 2", "strip/cartridge lot not verified", "verify the new lot before patient use (trap 8)")
    v = s.get("value")
    rng = s.get("range")
    if v is not None and rng is not None and not (rng[0] <= v <= rng[1]):
        add(out, "BLOCK", "trap 3", "value %g outside measuring range %g-%g" % (v, rng[0], rng[1]),
            "do not report the number; report < / > range per SOP and send to the central lab")
    if (s.get("analyte") or "").lower() == "glucose":
        if s.get("hct") is not None and s.get("hct_range") is not None:
            b = hct_bias(s["hct"], s["hct_range"])
            if b:
                add(out, "BLOCK", "Fork 3", "Hct %g outside meter range %g-%g -> glucose %s"
                    % (s["hct"], s["hct_range"][0], s["hct_range"][1], b),
                    "use central-lab / venous glucose (ICU, neonates, anaemia, dialysis)")
        method = (s.get("method") or "").lower()
        inter = {i.lower() for i in s.get("interferents") or []}
        if method == "gdh-pqq" and inter & GDH_PQQ_SUGARS:
            add(out, "BLOCK", "Fork 3", "GDH-PQQ meter + %s" % ", ".join(sorted(inter & GDH_PQQ_SUGARS)),
                "glucose falsely HIGH (insulin overdose deaths reported) -> lab glucose / non-PQQ method")
        if method == "gox" and (s.get("sample") == "arterial" or "high-o2" in inter):
            add(out, "CONFIRM", "Fork 3", "glucose-oxidase meter + high O2 / arterial sample",
                "glucose falsely LOW (GDH methods are O2-insensitive) -> confirm before acting")
        if inter & AMPEROMETRIC:
            add(out, "CONFIRM", "Fork 3", "amperometric interferent: %s" % ", ".join(sorted(inter & AMPEROMETRIC)),
                "confirm with the central lab before acting")
        if s.get("sample", "capillary") == "capillary" and (s.get("perfusion") or "normal") in POOR_PERFUSION:
            add(out, "BLOCK", "Fork 3", "capillary glucose with %s" % s["perfusion"],
                "capillary is unreliable with poor perfusion -> venous / blood-gas analyzer")
    if s.get("connectivity") == "manual":
        add(out, "CAUTION", "Fork 4", "result transcribed by hand", "not traceable - enter via LIS/middleware (trap 4)")
    crit = s.get("critical")
    if v is not None and crit is not None and (v < crit[0] or v > crit[1]):
        add(out, "NOTIFY", "Fork 5", "critical value %g (policy limits %g-%g)" % (v, crit[0], crit[1]),
            "notify per policy + read-back; consider central-lab confirmation")
    out.sort(key=lambda f: LEVELS.index(f["level"]))
    levels = {f["level"] for f in out}
    if "BLOCK" in levels:
        status = "BLOCKED: do not act on this POCT result"
    elif "CONFIRM" in levels:
        status = "CONFIRM BEFORE ACTING (central lab / venous)"
    elif "NOTIFY" in levels:
        status = "USABLE + CRITICAL: notify per policy"
    else:
        status = "USABLE (gates passed)"
    return {"findings": out, "status": status}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--analyte", default="glucose")
    ap.add_argument("--value", type=float)
    ap.add_argument("--qc", choices=["pass", "fail", "not-done"])
    ap.add_argument("--operator-competent", action="store_true")
    ap.add_argument("--competency-date", type=dt.date.fromisoformat, help="YYYY-MM-DD of last assessment")
    ap.add_argument("--competency-interval-days", type=int, help="your policy's re-assessment interval")
    ap.add_argument("--today", type=dt.date.fromisoformat)
    ap.add_argument("--lot-verified", action="store_true")
    ap.add_argument("--range", type=parse_range, help="device measuring range LOW-HIGH (manufacturer)")
    ap.add_argument("--critical", type=parse_range, help="critical limits LOW-HIGH (your policy)")
    ap.add_argument("--method", choices=["gox", "gdh-pqq", "gdh-fad", "gdh-nad", "other"])
    ap.add_argument("--hct", type=float)
    ap.add_argument("--hct-range", type=parse_range, help="meter's validated Hct range LOW-HIGH (manufacturer)")
    ap.add_argument("--sample", choices=["capillary", "venous", "arterial"], default="capillary")
    ap.add_argument("--perfusion", choices=["normal", "shock", "hypotension", "edema", "vasopressor"], default="normal")
    ap.add_argument("--interferent", action="append", dest="interferents", default=[],
                    help="repeatable: maltose icodextrin galactose acetaminophen vitamin-c uric-acid high-o2")
    ap.add_argument("--connectivity", choices=["lis", "manual"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    res = evaluate(vars(a))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1, default=str))
        return 0
    for f in res["findings"]:
        print("%-8s %-7s %s\n%17s-> %s" % (f["level"], f["fork"], f["finding"], "", f["action"]))
    print("STATUS: %s" % res["status"])
    print("ADVISORY: decision support only - follow the POCT policy/SOP (ISO 15189) and confirm with the lab/physician.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
