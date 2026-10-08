#!/usr/bin/env python3
"""westgard — evaluate IQC results against Westgard multirules, run by run.

Black-box tool for clinchem-judgment. Run --help first; read the source only if a run fails.
Source of the rules: 505402 Clinical Chemistry Lab digest §2.3 (rule table, classic vs modified
algorithm) and §3.1 (sigma-based rule selection). ADVISORY ONLY: the run decision belongs to the
lab's QC policy and an authorised signatory.

Input CSV columns (header required): run, level, value, mean, sd
  rows in time order; one row per control level per run; `run` may be a number or a date label.

Modes
  all       apply every rejection rule to every run (default; how LIS/middleware usually run it)
  classic   1-2s is the gate: other rules are inspected only when a value is beyond 2SD
  modified  stable systems: 1-2s / 4-1s / 10x = warning; 1-3s / 2-2s / R-4s = reject
  sigma     pick rules from --sigma (6: 1-3s · 5: +2-2s R-4s · 4: +4-1s · <4: +8x)

Examples
  python westgard.py qc.csv
  python westgard.py qc.csv --mode classic
  python westgard.py qc.csv --mode sigma --sigma 5.4
  python westgard.py qc.csv --json
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

ERROR_TYPE = {"1-3s": "random", "R-4s": "random", "2-2s": "systematic", "4-1s": "systematic",
              "10x": "systematic", "8x": "systematic", "2of3-2s": "systematic", "1-2s": "warning"}


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    obs = []
    for i, r in enumerate(rows):
        r = {k.strip().lower(): (v or "").strip() for k, v in r.items()}
        mean, sd, value = float(r["mean"]), float(r["sd"]), float(r["value"])
        if sd <= 0:
            sys.exit("row %d: sd must be > 0" % (i + 2))
        obs.append({"i": i, "run": r["run"], "level": r["level"], "value": value, "mean": mean, "sd": sd,
                    "z": (value - mean) / sd})
    return obs


def runs_in_order(obs):
    order = []
    for o in obs:
        if o["run"] not in order:
            order.append(o["run"])
    return order


# ---------------------------------------------------------------- single rules
def rule_1_2s(run_obs):
    return [o for o in run_obs if abs(o["z"]) > 2]


def rule_1_3s(run_obs):
    return [o for o in run_obs if abs(o["z"]) > 3]


def rule_r4s(run_obs):
    """Within ONE run only: one control > +2SD and another < -2SD. Never across runs."""
    hi = [o for o in run_obs if o["z"] > 2]
    lo = [o for o in run_obs if o["z"] < -2]
    return (hi[:1] + lo[:1]) if hi and lo else []


def same_side_run(seq, k, limit):
    """Last k observations of seq all beyond +limit, or all beyond -limit."""
    if len(seq) < k:
        return []
    tail = seq[-k:]
    if all(o["z"] > limit for o in tail) or all(o["z"] < -limit for o in tail):
        return tail
    return []


def rule_2_2s(run_obs, history_by_level):
    hits = []
    # (a) within run, across levels
    for side in (1, -1):
        both = [o for o in run_obs if side * o["z"] > 2]
        if len(both) >= 2:
            hits.append(("within-run across levels", both[:2]))
    # (b) across runs, within level
    for o in run_obs:
        seq = history_by_level[o["level"]]
        tail = same_side_run(seq, 2, 2)
        if tail:
            hits.append(("across runs, level %s" % o["level"], tail))
    return hits


def rule_k_limit(run_obs, history_by_level, flat_history, k, limit):
    """4-1s (limit=1) or Nx (limit=0): within level across runs, then across levels (run-major)."""
    hits = []
    for o in run_obs:
        tail = same_side_run(history_by_level[o["level"]], k, limit)
        if tail:
            hits.append(("within level %s across runs" % o["level"], tail))
    tail = same_side_run(flat_history, k, limit)
    if tail and len({o["level"] for o in tail}) > 1:
        hits.append(("across levels (run-major order)", tail))
    return hits


def rule_2of3_2s(run_obs):
    if len(run_obs) < 3:
        return []
    for side in (1, -1):
        beyond = [o for o in run_obs if side * o["z"] > 2]
        if len(beyond) >= 2:
            return beyond
    return []


# ---------------------------------------------------------------- evaluation
def rules_for(mode, sigma):
    if mode != "sigma":
        return ["1-3s", "2-2s", "R-4s", "4-1s", "10x"]
    if sigma is None:
        sys.exit("--mode sigma needs --sigma")
    if sigma >= 6:
        return ["1-3s"]
    if sigma >= 5:
        return ["1-3s", "2-2s", "R-4s"]
    if sigma >= 4:
        return ["1-3s", "2-2s", "R-4s", "4-1s"]
    return ["1-3s", "2-2s", "R-4s", "4-1s", "8x"]


def evaluate(obs, mode="all", sigma=None, use_2of3=False):
    order = runs_in_order(obs)
    active = rules_for(mode, sigma)
    if use_2of3:
        active = active + ["2of3-2s"]
    warn_only = {"4-1s", "10x"} if mode == "modified" else set()
    history_by_level, flat = {}, []
    report = []
    for run in order:
        run_obs = [o for o in obs if o["run"] == run]
        for o in run_obs:
            history_by_level.setdefault(o["level"], []).append(o)
            flat.append(o)
        fired = {}
        w12 = rule_1_2s(run_obs)
        if w12:
            fired["1-2s"] = [("any level", w12)]
        candidates = {
            "1-3s": lambda: [("any level", rule_1_3s(run_obs))] if rule_1_3s(run_obs) else [],
            "R-4s": lambda: [("within run", rule_r4s(run_obs))] if rule_r4s(run_obs) else [],
            "2-2s": lambda: rule_2_2s(run_obs, history_by_level),
            "4-1s": lambda: rule_k_limit(run_obs, history_by_level, flat, 4, 1),
            "10x": lambda: rule_k_limit(run_obs, history_by_level, flat, 10, 0),
            "8x": lambda: rule_k_limit(run_obs, history_by_level, flat, 8, 0),
            "2of3-2s": lambda: [("within run", rule_2of3_2s(run_obs))] if rule_2of3_2s(run_obs) else [],
        }
        all_hits = {}
        for name in active:
            hits = candidates[name]()
            if hits:
                all_hits[name] = hits
        gated_out = mode == "classic" and not w12
        if not gated_out:
            fired.update(all_hits)
        reject = sorted(r for r in fired if r != "1-2s" and r not in warn_only)
        warning = sorted(r for r in fired if r == "1-2s" or r in warn_only)
        decision = "REJECT" if reject else ("WARNING" if warning else "ACCEPT")
        note = ""
        if gated_out and all_hits:
            note = ("classic 1-2s gate skipped %s because no value was beyond 2SD; "
                    "mode=all would REJECT" % sorted(all_hits))
        report.append({"run": run, "z": {o["level"]: round(o["z"], 3) for o in run_obs},
                       "decision": decision, "reject_rules": reject, "warning_rules": warning,
                       "error_type": sorted({ERROR_TYPE[r] for r in reject}),
                       "detail": {r: [(how, [(o["run"], o["level"], round(o["z"], 3)) for o in os_])
                                      for how, os_ in hits] for r, hits in fired.items()},
                       "note": note})
    return {"mode": mode, "sigma": sigma, "rules_active": active, "runs": report}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--mode", choices=["all", "classic", "modified", "sigma"], default="all")
    ap.add_argument("--sigma", type=float, help="method sigma metric, used by --mode sigma")
    ap.add_argument("--2of3", dest="two_of_three", action="store_true", help="add 2of3-2s (3-level QC)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    res = evaluate(load(a.csv), a.mode, a.sigma, a.two_of_three)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("mode=%s  rules=%s%s" % (res["mode"], ", ".join(res["rules_active"]),
                                   ("  sigma=%s" % res["sigma"]) if res["sigma"] is not None else ""))
    print("%-12s %-30s %-8s %s" % ("run", "z by level", "decision", "rules"))
    for r in res["runs"]:
        zs = "  ".join("%s:%+.2f" % (k, v) for k, v in r["z"].items())
        rules = ", ".join(r["reject_rules"] + ["(warn) " + w for w in r["warning_rules"]])
        print("%-12s %-30s %-8s %s" % (r["run"], zs, r["decision"], rules))
        for rule, hits in r["detail"].items():
            if rule == "1-2s":
                continue
            for how, pts in hits:
                print("%14s %s [%s]: %s" % ("", rule, how, pts))
        if r["note"]:
            print("%14s NOTE: %s" % ("", r["note"]))
    last = res["runs"][-1]
    print("-" * 70)
    print("LATEST RUN %s -> %s %s" % (last["run"], last["decision"],
                                       ("(" + "/".join(last["error_type"]) + " error)") if last["error_type"] else ""))
    print("ADVISORY: decision support only - confirm with the lab QC policy/SOP and an authorised signatory.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
