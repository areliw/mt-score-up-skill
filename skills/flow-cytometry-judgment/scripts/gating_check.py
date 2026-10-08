#!/usr/bin/env python3
"""gating_check - check a flow gating hierarchy and recompute % of parent / % of total.

Black-box tool for flow-cytometry-judgment (card rule #1, trap #1, Fork 1). Run --help, not the source.
ADVISORY ONLY: a clean hierarchy is necessary, not sufficient; FMO controls, compensation and
morphology/clinical correlation still decide (card Forks 2-5).

What it checks (card Fork 1 order: time/flow-stability -> scatter (FSC/SSC) -> singlet -> viable + dump
-> CD45 vs SSC -> marker):
  REQUIRED above every `marker` gate:  singlet, viable, and scatter or cd45
      missing one = trap #1: doublets / dead cells / debris sit in the denominator -> % is wrong
  RECOMMENDED:  time gate (cut clogs / unstable flow)  -> WARN if absent
  ORDER:        ancestors out of the Fork 1 order -> NOTE (some labs swap steps; judge, don't auto-fail)
  SANITY:       unknown parent, more events than the parent, duplicate names -> ERROR

Input CSV (header required): gate,parent,events,kind
  kind = all | time | scatter | singlet | viable | dump | cd45 | marker | other
  exactly one row has an empty parent (the root, usually kind=all). Example: data/gating_example.csv

Examples
  python gating_check.py data/gating_example.csv
  python gating_check.py data/gating_no_singlet_viable.csv
  python gating_check.py data/gating_example.csv --target CD4+ --json
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

KINDS = {"all", "time", "scatter", "singlet", "viable", "dump", "cd45", "marker", "other"}
ORDER = {"time": 0, "scatter": 1, "singlet": 2, "viable": 3, "dump": 3, "cd45": 4, "marker": 5}
REQUIRED_UPSTREAM = {
    "singlet": "no singlet gate: doublets are counted as single cells",
    "viable": "no viability/dump gate: dead cells bind antibody non-specifically",
    "scatter|cd45": "no scatter or CD45/SSC gate: debris sits in the denominator",
}
RECOMMENDED_UPSTREAM = {"time": "no time/flow-stability gate: clogs or unstable flow not removed"}
ADVISORY = ("ADVISORY: decision support only - confirm gates against FMO controls and compensation, correlate "
            "with morphology/clinical, and follow the lab SOP; diagnosis belongs to the physician.")


class GatingError(ValueError):
    pass


def parse(rows):
    nodes, roots = {}, []
    for i, r in enumerate(rows):
        r = {(k or "").strip().lower(): (v or "").strip() for k, v in r.items()}
        name, parent, kind = r.get("gate", ""), r.get("parent", ""), r.get("kind", "").lower()
        if not name:
            raise GatingError("row %d: empty gate name" % (i + 2))
        if name in nodes:
            raise GatingError("duplicate gate name %r" % name)
        if kind not in KINDS:
            raise GatingError("gate %r: kind %r not in %s" % (name, kind, sorted(KINDS)))
        try:
            events = int(float(r.get("events", "")))
        except ValueError:
            raise GatingError("gate %r: events must be a number" % name)
        if events < 0:
            raise GatingError("gate %r: events < 0" % name)
        nodes[name] = {"gate": name, "parent": parent or None, "events": events, "kind": kind, "order": i}
        if not parent:
            roots.append(name)
    if len(roots) != 1:
        raise GatingError("need exactly one root (empty parent), found %d" % len(roots))
    for n in nodes.values():
        p = n["parent"]
        if p is not None and p not in nodes:
            raise GatingError("gate %r: parent %r not defined" % (n["gate"], p))
        if p is not None and n["events"] > nodes[p]["events"]:
            raise GatingError("gate %r has more events (%d) than its parent %r (%d)"
                              % (n["gate"], n["events"], p, nodes[p]["events"]))
    for n in nodes:  # cycle guard
        ancestors(nodes, n)
    return nodes


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return parse(list(csv.DictReader(f)))


def ancestors(nodes, gate):
    """Gates from the root down to the parent of `gate`."""
    chain, seen, p = [], {gate}, nodes[gate]["parent"]
    while p is not None:
        if p in seen:
            raise GatingError("cycle in hierarchy at %r" % p)
        seen.add(p)
        chain.append(p)
        p = nodes[p]["parent"]
    return list(reversed(chain))


def root_of(nodes):
    return next(n for n in nodes if nodes[n]["parent"] is None)


def pct_of_parent(nodes, gate):
    p = nodes[gate]["parent"]
    if p is None:
        return 100.0
    pe = nodes[p]["events"]
    return nodes[gate]["events"] / pe * 100 if pe else 0.0


def pct_of_total(nodes, gate):
    te = nodes[root_of(nodes)]["events"]
    return nodes[gate]["events"] / te * 100 if te else 0.0


def check_path(nodes, gate):
    kinds = [nodes[a]["kind"] for a in ancestors(nodes, gate)]
    missing = []
    for need, why in REQUIRED_UPSTREAM.items():
        if not any(k in kinds for k in need.split("|")):
            missing.append(why)
    warn = [why for need, why in RECOMMENDED_UPSTREAM.items() if need not in kinds]
    ranked = [(k, ORDER[k]) for k in kinds if k in ORDER]
    order_notes = []
    for (k1, r1), (k2, r2) in zip(ranked, ranked[1:]):
        if r2 < r1:
            order_notes.append("%s gate sits below %s (card Fork 1 order: time -> scatter -> singlet -> "
                               "viable/dump -> CD45/SSC -> marker)" % (k2, k1))
    return {"missing": missing, "warn": warn, "order_notes": order_notes}


def evaluate(nodes, targets=None):
    if targets:
        for t in targets:
            if t not in nodes:
                raise GatingError("target %r not in the hierarchy" % t)
    else:
        targets = [n for n in nodes if nodes[n]["kind"] == "marker"]
    rows = []
    for name in sorted(nodes, key=lambda n: nodes[n]["order"]):
        rows.append({"gate": name, "kind": nodes[name]["kind"], "parent": nodes[name]["parent"],
                     "events": nodes[name]["events"],
                     "pct_parent": pct_of_parent(nodes, name), "pct_total": pct_of_total(nodes, name)})
    checks = {}
    for t in targets:
        c = check_path(nodes, t)
        c["status"] = "FAIL" if c["missing"] else ("WARN" if c["warn"] or c["order_notes"] else "PASS")
        c["path"] = ancestors(nodes, t) + [t]
        checks[t] = c
    overall = "FAIL" if any(c["status"] == "FAIL" for c in checks.values()) else (
        "WARN" if any(c["status"] == "WARN" for c in checks.values()) else "PASS")
    return {"rows": rows, "checks": checks, "overall": overall}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--target", action="append", help="gate(s) to check (default: every kind=marker gate)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        res = evaluate(load(a.csv), a.target)
    except GatingError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        res["advisory"] = ADVISORY
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("%-16s %-8s %-14s %9s %9s %9s  %s" % ("gate", "kind", "parent", "events", "%parent", "%total", "check"))
    for r in res["rows"]:
        st = res["checks"].get(r["gate"], {}).get("status", "")
        print("%-16s %-8s %-14s %9d %9.2f %9.2f  %s" % (r["gate"], r["kind"], r["parent"] or "-", r["events"],
                                                        r["pct_parent"], r["pct_total"], st))
    for t, c in res["checks"].items():
        for m in c["missing"]:
            print("  FAIL %s: %s" % (t, m))
        for w in c["warn"]:
            print("  WARN %s: %s" % (t, w))
        for o in c["order_notes"]:
            print("  NOTE %s: %s" % (t, o))
    print("-" * 78)
    msg = {"FAIL": "re-gate before reporting any %: the denominator may contain what the FAIL lines name",
           "WARN": "hierarchy usable but see WARN/NOTE lines",
           "PASS": "required upstream gates present for every target"}[res["overall"]]
    print("OVERALL %s -> %s" % (res["overall"], msg))
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
