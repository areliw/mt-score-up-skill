#!/usr/bin/env python3
"""release_gate — walk each result through the layered release checks BEFORE looking at the number,
and say whether it may auto-release, must stop for a person, or must be notified as critical.

Black-box tool for result-release-judgment. Run --help first; read the source only if a check fails.
Layers and stop-conditions come from the result-release-judgment card:
  Fork 1  1 QC of that run passed?  2 sample integrity (HIL/clot/wrong tube/QNS)?  3 instrument flag /
          outside AMR (-> validated dilution OR report ">limit" per SOP - not "always dilute")?
          4 delta check?  5 plausible with clinical / rest of the panel?  6 critical? (-> notify, not just release)
  Fork 3  auto-release only when ALL clear: QC pass, within AMR, not critical, delta pass, no instrument/sample
          flag. Anything else STOPS for human review. An unknown layer is a stop, never a pass.
  Fork 4  critical = notify the responsible person now + read-back + log; do not delay past the turnaround.
Limits (AMR, critical, delta) are lab-specific -> read from a limits CSV you supply. Delta uses delta_check.py.
ADVISORY ONLY: release/hold is the authorised MT's decision under the lab SOP.

Results JSON: list of {"id", "analyte", "value", "qc": "pass"|"fail", "integrity": "ok"|"hemolyzed"|"clotted"|
  "wrong-tube"|"qns", "instrument_flag": bool, "prev": number, "plausible": bool}
Limits CSV header: analyte,amr_low,amr_high,crit_low,crit_high,delta_abs,delta_pct   (blank = not set)

Examples
  python release_gate.py ../data/release_example.json --limits ../data/limits_example.csv
  python release_gate.py ../data/release_example.json --limits ../data/limits_example.csv --json
"""
import argparse
import csv
import json
import os
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import delta_check  # noqa: E402

# Fork 3: conditions that must ALL hold for auto-release
AUTO_CONDITIONS = ("qc", "integrity", "amr_flag", "delta", "critical")


def num(x):
    return None if x in (None, "") else float(x)


def load_limits(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = [{k.strip().lower(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(ln for ln in f if not ln.lstrip().startswith("#"))]
    return {r["analyte"].lower(): {k: num(r.get(k)) for k in
                                   ("amr_low", "amr_high", "crit_low", "crit_high", "delta_abs", "delta_pct")}
            for r in rows}


def layer(name, status, msg):
    return {"layer": name, "status": status, "msg": msg}   # status: PASS / STOP / NOTIFY / NOT SET


def evaluate(res, lim):
    v = float(res["value"])
    L = []
    qc = res.get("qc")
    L.append(layer("1 QC", "PASS" if qc == "pass" else "STOP",
                   "QC passed" if qc == "pass" else ("QC failed -> investigate which results are affected; fix + rerun "
                                                     "only those" if qc == "fail" else "QC status unknown -> cannot release")))
    integ = res.get("integrity")
    L.append(layer("2 integrity", "PASS" if integ == "ok" else "STOP",
                   "sample OK" if integ == "ok" else ("sample %s -> do not release affected analyte; comment or "
                                                     "recollect (preanalytical-judgment)" % integ if integ else
                                                     "sample integrity unknown -> cannot release")))
    amr_msg, amr_status = [], "PASS"
    if res.get("instrument_flag"):
        amr_status, amr_msg = "STOP", ["instrument flag -> review per SOP"]
    lo, hi = lim.get("amr_low"), lim.get("amr_high")
    if lo is None or hi is None:
        amr_status = "STOP"
        amr_msg.append("AMR not set in limits file -> cannot confirm reportable range")
    elif v > hi:
        amr_status = "STOP"
        amr_msg.append("above AMR %g -> validated dilution OR report '>%g' OR other method, per SOP" % (hi, hi))
    elif v < lo:
        amr_status = "STOP"
        amr_msg.append("below AMR %g -> report '<%g' per SOP" % (lo, lo))
    L.append(layer("3 flag/AMR", amr_status, "; ".join(amr_msg) or "within AMR, no flag"))
    prev = res.get("prev")
    if prev is None:
        L.append(layer("4 delta", "PASS", "no previous result -> delta not applicable (first result: some SOPs "
                                          "still stop first-time abnormals)"))
    elif lim.get("delta_abs") is None and lim.get("delta_pct") is None:
        L.append(layer("4 delta", "STOP", "previous result exists but no delta limit set -> cannot clear"))
    else:
        d = delta_check.delta(float(prev), v, lim.get("delta_abs"), lim.get("delta_pct"), analyte=res.get("analyte", ""))
        L.append(layer("4 delta", "STOP" if d["flagged"] else "PASS",
                       ("delta FLAG (%s) -> ID/mix-up first, then artifact, then real change" % "; ".join(d["reasons"]))
                       if d["flagged"] else "delta within limit"))
    pl = res.get("plausible")
    L.append(layer("5 plausible", {True: "PASS", False: "STOP", None: "NOT SET"}[pl],
                   {True: "consistent with clinical/panel", False: "conflicts with clinical/panel -> hold + investigate",
                    None: "plausibility not assessed (not an auto-release condition)"}[pl]))
    clo, chi = lim.get("crit_low"), lim.get("crit_high")
    if clo is None and chi is None:
        L.append(layer("6 critical", "STOP", "critical limits not set -> cannot rule out a critical value"))
        critical = None
    else:
        critical = (clo is not None and v < clo) or (chi is not None and v > chi)
        L.append(layer("6 critical", "NOTIFY" if critical else "PASS",
                       "CRITICAL -> notify responsible person now + identifiers + read-back + log; escalate if "
                       "unreachable (critical_log_check.py)" if critical else "not critical"))
    by = {x["layer"].split()[1]: x["status"] for x in L}
    cond = {"qc": by["QC"] == "PASS", "integrity": by["integrity"] == "PASS", "amr_flag": by["flag/AMR"] == "PASS",
            "delta": by["delta"] == "PASS", "critical": by["critical"] == "PASS"}
    stops = [x for x in L if x["status"] == "STOP"]
    auto = all(cond[c] for c in AUTO_CONDITIONS) and not stops
    if stops:
        action = "STOP at %s -> human review" % stops[0]["layer"]
        if critical:
            action += " (value is in the CRITICAL range: resolve fast, do not exceed the notification turnaround)"
    elif critical:
        action = "RELEASE + NOTIFY CRITICAL (not auto-release)"
    else:
        action = "AUTO-RELEASE eligible" if auto else "RELEASE after review"
    return {"id": res.get("id"), "analyte": res.get("analyte"), "value": v, "layers": L,
            "auto_release": auto, "action": action}


def main(argv=None):
    try:  # never crash a non-UTF-8 console (e.g. Thai cp874) on the section sign / Thai text
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results_json")
    ap.add_argument("--limits", required=True, help="CSV of lab limits per analyte")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    limits = load_limits(a.limits)
    with open(a.results_json, encoding="utf-8") as f:
        data = json.load(f)
    out = []
    for r in (data if isinstance(data, list) else [data]):
        lim = limits.get(str(r.get("analyte", "")).lower())
        if lim is None:
            out.append({"id": r.get("id"), "analyte": r.get("analyte"), "value": r.get("value"), "layers": [],
                        "auto_release": False, "action": "STOP: analyte not in limits file -> no rule, cannot release"})
            continue
        out.append(evaluate(r, lim))
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0
    for r in out:
        print("%s  %s = %s" % (r["id"], r["analyte"], r["value"]))
        for x in r["layers"]:
            print("   %-12s %-8s %s" % (x["layer"], x["status"], x["msg"]))
        print("   -> %s   (auto-release: %s)" % (r["action"], "yes" if r["auto_release"] else "no"))
    print("ADVISORY: decision support only - release/hold per the lab SOP; confirm with an authorised MT.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
