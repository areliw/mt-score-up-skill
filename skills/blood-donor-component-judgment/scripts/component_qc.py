#!/usr/bin/env python3
"""component_qc - blood component QC arithmetic and batch verdict, with limits YOU supply.

Black-box tool for blood-donor-component-judgment. Run --help first; read the source only if needed.
Sources:
  512304 Transfusion Science 2 digest §9: component volume = (bag weight - empty bag weight) / specific
         gravity; QC on >= 1% of each component
  card blood-donor-component-judgment Fork 5: QC is statistical (sample a % of production, a required
         proportion must pass); fail -> quarantine related units/co-components first, widen to the lot
         when it points to process/equipment/trend (critical, bacterial, repeated); an isolated
         non-critical outlier = record + investigate + trend - never discard one unit and walk on.
         Every limit and pass proportion is standard/edition-specific -> passed in, never built in.
ADVISORY ONLY. Release/quarantine decisions follow the component SOP and the responsible MT/physician.

Subcommands
  volume       --gross-g --tare-g --sg            -> mL  (SG of the component: from your SOP)
  sample-size  --produced N [--pct 1] [--min-units 0]  -> units to QC (ceil(N x pct/100), at least min)
  batch        CSV of QC results + specs           -> per-unit / per-parameter pass, batch verdict

batch input CSV: unit,<param1>,<param2>,...   (blank cell = not tested -> INCOMPLETE, never a pass)
  --spec NAME:MIN:MAX[:PASS_RATE]   numeric limit (leave MIN or MAX empty), e.g. volume_ml:200:
  --expect NAME=VALUE[:PASS_RATE]   categorical must equal VALUE, e.g. culture=neg
  --pass-rate R                     default required proportion for specs that give none (no built-in)
  --critical NAME[,NAME]            any failure of these = RED FLAG regardless of proportion

Examples (limits below are PLACEHOLDERS for the demo - take yours from your standard/edition)
  python component_qc.py volume --gross-g 312 --tare-g 52 --sg 1.03
  python component_qc.py sample-size --produced 850
  python component_qc.py batch ../data/platelet_qc_teaching.csv --spec volume_ml:200:400 \\
      --spec plt_e11:2.4::0.75 --spec ph:6.2:: --expect culture=neg --pass-rate 0.9 --critical culture
"""
import argparse
import csv
import json
import math
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ADVISORY = "ADVISORY: decision support only - confirm with the component SOP and the responsible MT/physician."


def volume_ml(gross_g, tare_g, sg):
    """512304 §9: (bag weight - empty bag) / specific gravity."""
    if sg <= 0:
        raise ValueError("--sg must be > 0")
    net = gross_g - tare_g
    if net <= 0:
        raise ValueError("gross weight must exceed tare weight")
    return {"gross_g": gross_g, "tare_g": tare_g, "net_g": net, "sg": sg, "volume_ml": net / sg,
            "formula": "(gross - tare) / SG  (512304 §9)"}


def sample_size(produced, pct=1.0, min_units=0):
    """512304 §9: QC at least 1% of each component (min_units only if your SOP sets one)."""
    if produced < 0 or pct <= 0:
        raise ValueError("produced must be >= 0 and pct > 0")
    n = math.ceil(produced * pct / 100.0 - 1e-9)
    return {"produced": produced, "pct": pct, "min_units": min_units, "units_to_qc": max(n, min_units),
            "formula": "ceil(produced x %g%%), at least %d  (512304 §9)" % (pct, min_units)}


def parse_specs(specs, expects, default_rate):
    out = {}
    for s in specs:
        parts = s.split(":")
        if len(parts) not in (3, 4):
            raise ValueError("--spec must be NAME:MIN:MAX[:PASS_RATE], got %r" % s)
        name, lo, hi = parts[0], parts[1], parts[2]
        rate = float(parts[3]) if len(parts) == 4 and parts[3] else default_rate
        out[name] = {"kind": "num", "min": float(lo) if lo else None, "max": float(hi) if hi else None, "rate": rate}
    for e in expects:
        if "=" not in e:
            raise ValueError("--expect must be NAME=VALUE[:PASS_RATE], got %r" % e)
        name, rest = e.split("=", 1)
        val, _, rate = rest.partition(":")
        out[name] = {"kind": "cat", "value": val.strip().lower(), "rate": float(rate) if rate else default_rate}
    for name, sp in out.items():
        if sp["rate"] is None:
            raise ValueError("no pass rate for %r: give NAME:...:RATE or --pass-rate (it is standard-specific)" % name)
        if not 0 < sp["rate"] <= 1:
            raise ValueError("pass rate for %r must be a fraction in (0, 1]" % name)
    return out


def check(value, sp):
    v = (value or "").strip()
    if v == "":
        return "MISSING"
    if sp["kind"] == "cat":
        return "PASS" if v.lower() == sp["value"] else "FAIL"
    x = float(v)
    if sp["min"] is not None and x < sp["min"]:
        return "FAIL"
    if sp["max"] is not None and x > sp["max"]:
        return "FAIL"
    return "PASS"


def batch_verdict(per_param, failed_units, critical):
    """Card Fork 5 escalation ladder."""
    crit_fail = [p for p in critical if per_param.get(p, {}).get("failed")]
    below = [p for p, r in per_param.items() if r["tested"] and r["proportion"] < r["required"]]
    missing = [p for p, r in per_param.items() if r["missing"]]
    if crit_fail:
        return ("RED FLAG", "critical parameter failed (%s): quarantine the unit(s), co-components and the related "
                "lot; investigate and report (card Fork 5, Fork 8)" % ", ".join(crit_fail))
    if below:
        return ("BATCH FAIL", "pass proportion below the required rate for %s: quarantine the lot/process, review "
                "centrifuge/temperature/technique, investigate (card Fork 5)" % ", ".join(below))
    if missing:
        return ("INCOMPLETE", "untested values for %s: QC cannot be signed as passed" % ", ".join(missing))
    if failed_units:
        return ("PASS WITH ISOLATED FAILURES", "quarantine failed unit(s) %s + co-components, record, investigate, "
                "trend - do not discard and walk on (card Fork 5)" % ", ".join(failed_units))
    return ("PASS", "all sampled units met every parameter")


def evaluate_batch(rows, specs, critical=()):
    for name in critical:
        if name not in specs:
            raise ValueError("critical parameter %r has no --spec/--expect" % name)
    units = []
    per_param = {p: {"tested": 0, "passed": 0, "failed": [], "missing": [], "required": sp["rate"]}
                 for p, sp in specs.items()}
    for r in rows:
        uid = (r.get("unit") or "").strip() or "?"
        res = {}
        for p, sp in specs.items():
            if p not in r:
                raise ValueError("parameter %r not in CSV columns" % p)
            c = check(r[p], sp)
            res[p] = c
            pp = per_param[p]
            if c == "MISSING":
                pp["missing"].append(uid)
                continue
            pp["tested"] += 1
            if c == "PASS":
                pp["passed"] += 1
            else:
                pp["failed"].append(uid)
        units.append({"unit": uid, "results": res, "pass": all(v == "PASS" for v in res.values())})
    for pp in per_param.values():
        pp["proportion"] = pp["passed"] / pp["tested"] if pp["tested"] else 0.0
    failed_units = [u["unit"] for u in units if any(v == "FAIL" for v in u["results"].values())]
    verdict, action = batch_verdict(per_param, failed_units, list(critical))
    return {"units": units, "per_param": per_param, "failed_units": failed_units, "verdict": verdict,
            "action": action}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("volume")
    v.add_argument("--gross-g", type=float, required=True)
    v.add_argument("--tare-g", type=float, required=True, help="empty bag (and attached tubing) weight")
    v.add_argument("--sg", type=float, required=True, help="specific gravity of the component (from your SOP)")
    s = sub.add_parser("sample-size")
    s.add_argument("--produced", type=int, required=True)
    s.add_argument("--pct", type=float, default=1.0, help="%% of production to QC (default 1, 512304 §9)")
    s.add_argument("--min-units", type=int, default=0, help="minimum units per period if your SOP sets one")
    b = sub.add_parser("batch")
    b.add_argument("csv")
    b.add_argument("--spec", action="append", default=[])
    b.add_argument("--expect", action="append", default=[])
    b.add_argument("--pass-rate", type=float)
    b.add_argument("--critical", default="")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "volume":
            res = volume_ml(a.gross_g, a.tare_g, a.sg)
        elif a.cmd == "sample-size":
            res = sample_size(a.produced, a.pct, a.min_units)
        else:
            specs = parse_specs(a.spec, a.expect, a.pass_rate)
            if not specs:
                raise ValueError("give at least one --spec or --expect")
            with open(a.csv, encoding="utf-8-sig", newline="") as f:
                rows = [{k.strip(): v for k, v in r.items()} for r in csv.DictReader(f)]
            res = evaluate_batch(rows, specs, [c.strip() for c in a.critical.split(",") if c.strip()])
            res["specs"] = specs
    except (ValueError, OSError) as e:
        ap.error(str(e))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    if a.cmd in ("volume", "sample-size"):
        for k, val in res.items():
            print("%-14s %s" % (k, ("%.2f" % val) if isinstance(val, float) else val))
    else:
        params = list(res["per_param"])
        print("%-10s " % "unit" + " ".join("%-12s" % p for p in params))
        for u in res["units"]:
            print("%-10s " % u["unit"] + " ".join("%-12s" % u["results"][p] for p in params))
        print("-" * 70)
        print("%-12s %-8s %-8s %-10s %-9s %s" % ("parameter", "tested", "passed", "proportion", "required", "status"))
        for p, r in res["per_param"].items():
            ok = r["tested"] and r["proportion"] >= r["required"] and not r["missing"]
            print("%-12s %-8d %-8d %-10.3f %-9.3f %s" % (p, r["tested"], r["passed"], r["proportion"], r["required"],
                                                       "ok" if ok else "NOT MET"))
        print("VERDICT: %s" % res["verdict"])
        print("action : %s" % res["action"])
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
