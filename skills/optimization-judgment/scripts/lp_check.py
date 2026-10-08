#!/usr/bin/env python3
"""lp_check - exact arithmetic for small LP / integer / assignment problems (teaching and sanity-check scale).

Black-box tool for optimization-judgment: run `--help` / a subcommand first; do not read the source unless a run fails.
The card says "do not let the model do Simplex in its head - use a solver". For real models use Excel Solver, OR-Tools
or GUROBI; this tool exists to (1) audit a candidate answer against EVERY constraint, (2) cross-check a small model
exactly (Fractions, no rounding), (3) show what ignoring integrality or leaving a constraint out does.

  solve MODEL.json [--integer x1,x2|all] [--delta D] [--max-combos N]
      status OPTIMAL / INFEASIBLE / UNBOUNDED, optimum, slack and BINDING flag per constraint, right-hand shadow price
      per constraint (re-solve with RHS + 1/1000), and with --delta D the actual change vs shadow price x D (so you can
      see when D leaves the allowable range). --integer runs branch-and-bound and shows what naive rounding of the LP gives.
  check MODEL.json --x v1 v2 ... [--integer ...]
      verdict per constraint (LHS vs RHS), non-negativity, integrality, objective value of a candidate solution.
  assign COSTS.csv [--max]
      square assignment problem (Hungarian method), rows = workers/machines, columns = jobs; no header.

MODEL.json: {"name": "...", "sense": "max"|"min", "vars": ["x1","x2"], "c": [3,5],
             "constraints": [{"name": "plant3", "a": [3,2], "op": "<=", "b": 18}, ...]}   (op: <= >= =; all vars >= 0)
Vertex enumeration is exact but exponential: keep to about 4 variables / 12 constraints (a guard stops runaway sizes).

Examples
  python lp_check.py solve ../data/wyndor.json --delta 6
  python lp_check.py solve ../data/reddy_mikks.json --integer all
  python lp_check.py check ../data/wyndor.json --x 4 6
  python lp_check.py assign ../data/machineco.csv
ADVISORY: small-scale cross-check only - confirm production models with a real solver and test against the real constraints.
"""
import argparse
import csv
import itertools
import json
import math
import sys
from fractions import Fraction as Fr

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ADVISORY = "ADVISORY: small-scale cross-check only - confirm production models with a real solver and test against the real constraints."
EPS = Fr(1, 1000)


def fr(x):
    return x if isinstance(x, Fr) else Fr(str(x))


def fmt(x):
    x = fr(x)
    return str(x.numerator) if x.denominator == 1 else "%s (%.4f)" % (x, float(x))


# ---------------------------------------------------------------- model
def load_model(path):
    with open(path, encoding="utf-8-sig") as f:
        return parse_model(json.load(f))


def parse_model(d):
    n = len(d["vars"])
    if len(d["c"]) != n:
        raise ValueError("c has %d entries for %d variables" % (len(d["c"]), n))
    cons = []
    for i, c in enumerate(d["constraints"]):
        if len(c["a"]) != n:
            raise ValueError("constraint %r has %d coefficients for %d variables" % (c.get("name", i), len(c["a"]), n))
        if c["op"] not in ("<=", ">=", "="):
            raise ValueError("op must be <=, >= or =")
        cons.append({"name": c.get("name", "c%d" % (i + 1)), "a": [fr(v) for v in c["a"]], "op": c["op"], "b": fr(c["b"])})
    if d.get("sense", "max") not in ("max", "min"):
        raise ValueError("sense must be max or min")
    return {"name": d.get("name", "model"), "sense": d.get("sense", "max"), "vars": list(d["vars"]),
            "c": [fr(v) for v in d["c"]], "constraints": cons}


def dot(a, x):
    return sum((p * q for p, q in zip(a, x)), Fr(0))


def le_rows(model):
    """Every constraint as a.x <= b (equality = two rows) plus x_j >= 0 as -x_j <= 0."""
    n = len(model["vars"])
    rows = []
    for c in model["constraints"]:
        if c["op"] in ("<=", "="):
            rows.append((c["a"], c["b"]))
        if c["op"] in (">=", "="):
            rows.append(([-v for v in c["a"]], -c["b"]))
    for j in range(n):
        rows.append(([Fr(-1) if k == j else Fr(0) for k in range(n)], Fr(0)))
    return rows


def solve_square(A, b):
    """Gauss-Jordan over Fractions; None when singular."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        piv = next((r for r in range(col, n) if M[r][col] != 0), None)
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [v / pv for v in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [a - f * c for a, c in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]


def nullspace_1d(A, n):
    """Basis vector of the null space when A (k x n) has rank n-1; None otherwise."""
    M = [list(r) for r in A]
    pivots = []
    row = 0
    for col in range(n):
        piv = next((r for r in range(row, len(M)) if M[r][col] != 0), None)
        if piv is None:
            continue
        M[row], M[piv] = M[piv], M[row]
        pv = M[row][col]
        M[row] = [v / pv for v in M[row]]
        for r in range(len(M)):
            if r != row and M[r][col] != 0:
                f = M[r][col]
                M[r] = [a - f * c for a, c in zip(M[r], M[row])]
        pivots.append(col)
        row += 1
        if row == len(M):
            break
    free = [c for c in range(n) if c not in pivots]
    if len(free) != 1:
        return None
    fcol = free[0]
    vec = [Fr(0)] * n
    vec[fcol] = Fr(1)
    for r, pc in enumerate(pivots):
        vec[pc] = -M[r][fcol]
    return vec


def solve_lp(model, max_combos=300000):
    """Exact LP by vertex enumeration. Returns dict(status, x, objective, optimal_vertices)."""
    n = len(model["vars"])
    rows = le_rows(model)
    m = len(rows)
    if math.comb(m, n) > max_combos:
        raise ValueError("model too large for vertex enumeration (%d combinations > %d); use a real solver" % (math.comb(m, n), max_combos))
    sgn = 1 if model["sense"] == "max" else -1
    cvec = [sgn * v for v in model["c"]]
    vertices = set()
    for comb in itertools.combinations(range(m), n):
        x = solve_square([rows[i][0] for i in comb], [rows[i][1] for i in comb])
        if x is not None and all(dot(a, x) <= b for a, b in rows):
            vertices.add(tuple(x))
    if not vertices:
        return {"status": "INFEASIBLE", "x": None, "objective": None, "optimal_vertices": []}
    # unbounded <=> some extreme ray of the recession cone {d: a.d <= 0} improves the objective
    for comb in itertools.combinations(range(m), n - 1):
        base = [rows[i][0] for i in comb]
        d0 = nullspace_1d(base, n) if n > 1 else [Fr(1)]
        if d0 is None:
            continue
        for d in (d0, [-v for v in d0]):
            if all(dot(a, d) <= 0 for a, _ in rows) and dot(cvec, d) > 0:
                return {"status": "UNBOUNDED", "x": None, "objective": None, "optimal_vertices": [], "ray": d}
    best = max(dot(cvec, v) for v in vertices)
    opt = sorted(v for v in vertices if dot(cvec, v) == best)
    return {"status": "OPTIMAL", "x": list(opt[0]), "objective": sgn * best, "optimal_vertices": [list(v) for v in opt]}


def with_rhs(model, idx, delta):
    cons = [dict(c) for c in model["constraints"]]
    cons[idx]["b"] = cons[idx]["b"] + fr(delta)
    return dict(model, constraints=cons)


def constraint_table(model, x):
    out = []
    for c in model["constraints"]:
        lhs = dot(c["a"], x)
        slack = c["b"] - lhs if c["op"] == "<=" else (lhs - c["b"] if c["op"] == ">=" else abs(c["b"] - lhs))
        out.append({"name": c["name"], "lhs": lhs, "op": c["op"], "rhs": c["b"], "slack": slack, "binding": slack == 0,
                    "satisfied": slack >= 0 and (c["op"] != "=" or lhs == c["b"])})
    return out


def shadow_prices(model, sol, delta=None):
    """Right-hand shadow price per constraint (objective change per +1 RHS) by exact re-solve with RHS + 1/1000;
    with delta, also the actual objective after RHS + delta versus the linear prediction shadow x delta."""
    res = []
    for i, c in enumerate(model["constraints"]):
        s = solve_lp(with_rhs(model, i, EPS))
        sp = (s["objective"] - sol["objective"]) / EPS if s["status"] == "OPTIMAL" else None
        row = {"name": c["name"], "shadow_price": sp}
        if delta is not None and sp is not None:
            s2 = solve_lp(with_rhs(model, i, delta))
            row["delta"] = fr(delta)
            if s2["status"] == "OPTIMAL":
                row["actual_change"] = s2["objective"] - sol["objective"]
                row["predicted_change"] = sp * fr(delta)
                row["within_allowable_range"] = row["actual_change"] == row["predicted_change"]
            else:
                row["actual_change"] = s2["status"]
                row["within_allowable_range"] = False
        res.append(row)
    return res


def solve_integer(model, int_vars, max_nodes=20000):
    """Branch and bound over the exact LP. int_vars = indices of integer variables."""
    best = {"objective": None, "x": None}
    maximize = model["sense"] == "max"
    nodes = 0
    stack = [model]
    while stack:
        mdl = stack.pop()
        nodes += 1
        if nodes > max_nodes:
            raise ValueError("branch-and-bound exceeded %d nodes; use a real MIP solver" % max_nodes)
        s = solve_lp(mdl)
        if s["status"] == "INFEASIBLE":
            continue
        if s["status"] == "UNBOUNDED":
            return {"status": "UNBOUNDED-RELAXATION", "x": None, "objective": None, "nodes": nodes}
        if best["objective"] is not None and ((maximize and s["objective"] <= best["objective"]) or
                                              (not maximize and s["objective"] >= best["objective"])):
            continue
        frac = next((j for j in int_vars if s["x"][j].denominator != 1), None)
        if frac is None:
            best = {"objective": s["objective"], "x": s["x"]}
            continue
        v = s["x"][frac]
        unit = [Fr(1) if k == frac else Fr(0) for k in range(len(model["vars"]))]
        for op, rhs in (("<=", Fr(math.floor(v))), (">=", Fr(math.ceil(v)))):
            cons = [dict(c) for c in mdl["constraints"]] + [{"name": "branch", "a": unit, "op": op, "b": rhs}]
            stack.append(dict(mdl, constraints=cons))
    if best["objective"] is None:
        return {"status": "INFEASIBLE", "x": None, "objective": None, "nodes": nodes}
    return {"status": "OPTIMAL", "x": best["x"], "objective": best["objective"], "nodes": nodes}


def check_solution(model, x, int_vars=()):
    x = [fr(v) for v in x]
    if len(x) != len(model["vars"]):
        raise ValueError("expected %d values" % len(model["vars"]))
    table = constraint_table(model, x)
    problems = ["constraint %s violated: %s %s %s" % (t["name"], fmt(t["lhs"]), t["op"], fmt(t["rhs"])) for t in table if not t["satisfied"]]
    problems += ["%s = %s < 0" % (nm, fmt(v)) for nm, v in zip(model["vars"], x) if v < 0]
    problems += ["%s = %s is not an integer" % (model["vars"][j], fmt(x[j])) for j in int_vars if x[j].denominator != 1]
    return {"feasible": not problems, "objective": dot(model["c"], x), "constraints": table, "problems": problems}


def hungarian(cost):
    """Min-cost perfect assignment, O(n^3). cost: square list of Fractions. Returns (total, [(row, col)])."""
    n = len(cost)
    u, v, p, way = [Fr(0)] * (n + 1), [Fr(0)] * (n + 1), [0] * (n + 1), [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [None] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0, delta, j1 = p[j0], None, 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if minv[j] is None or cur < minv[j]:
                        minv[j], way[j] = cur, j0
                    if delta is None or minv[j] < delta:
                        delta, j1 = minv[j], j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    pairs = sorted((p[j] - 1, j - 1) for j in range(1, n + 1))
    return sum((cost[r][c] for r, c in pairs), Fr(0)), pairs


def read_costs(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = [[fr(v) for v in r] for r in csv.reader(f) if r and any(x.strip() for x in r)]
    if any(len(r) != len(rows) for r in rows):
        raise ValueError("assignment matrix must be square (pad with zero-cost dummy rows/columns if needed)")
    return rows


# ---------------------------------------------------------------- output
def jsonable(o):
    if isinstance(o, Fr):
        return {"exact": str(o), "value": float(o)}
    if isinstance(o, dict):
        return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    return o


def render_solve(model, sol, sp, integer=None, rounded=None):
    L = ["model: %s (%s)" % (model["name"], model["sense"]), "status: %s" % sol["status"]]
    if sol["status"] == "OPTIMAL":
        L.append("  ".join("%s = %s" % (nm, fmt(v)) for nm, v in zip(model["vars"], sol["x"])))
        L.append("objective = %s" % fmt(sol["objective"]))
        if len(sol["optimal_vertices"]) > 1:
            L.append("NOTE: multiple optimal vertices (alternate optima): " + " | ".join(
                "(" + ", ".join(fmt(v) for v in vtx) + ")" for vtx in sol["optimal_vertices"]))
        L.append("%-10s %14s %3s %10s %10s %8s %14s" % ("constraint", "LHS", "", "RHS", "slack", "binding", "shadow price"))
        for t, s in zip(constraint_table(model, sol["x"]), sp or [{}] * len(model["constraints"])):
            L.append("%-10s %14s %3s %10s %10s %8s %14s" % (
                t["name"], fmt(t["lhs"]), t["op"], fmt(t["rhs"]), fmt(t["slack"]), "yes" if t["binding"] else "no",
                fmt(s["shadow_price"]) if s.get("shadow_price") is not None else "-"))
        for s in sp or []:
            if "within_allowable_range" in s:
                ok = "within range" if s["within_allowable_range"] else "OUTSIDE allowable range - shadow price x delta is WRONG here"
                ac = s["actual_change"]
                L.append("delta %s on %s: actual change %s vs shadow x delta %s -> %s" % (
                    fmt(s["delta"]), s["name"], fmt(ac) if isinstance(ac, Fr) else ac, fmt(s.get("predicted_change", 0)), ok))
        L.append("NOTE: shadow price = right-hand derivative (+1 RHS); non-binding => 0; valid only inside the allowable range (use --delta to test)")
    elif sol["status"] == "UNBOUNDED":
        L.append("objective improves forever along direction " + str([fmt(v) for v in sol["ray"]]) +
                 " -> usually a FORGOTTEN constraint: re-read the problem statement word by word")
    else:
        L.append("no point satisfies all constraints -> constraints contradict each other: relax one or re-check the data")
    if integer:
        L.append("--- integer (branch and bound, %s nodes): %s" % (integer["nodes"], integer["status"]))
        if integer["status"] == "OPTIMAL":
            L.append("  ".join("%s = %s" % (nm, fmt(v)) for nm, v in zip(model["vars"], integer["x"])) +
                     "   objective = %s" % fmt(integer["objective"]))
            L.append("integer optimum differs from LP relaxation by %s" % fmt(sol["objective"] - integer["objective"]))
        if rounded is not None:
            L.append("naive rounding of the LP answer -> (%s): %s%s" % (
                ", ".join(fmt(v) for v in rounded["x"]), "FEASIBLE" if rounded["feasible"] else "INFEASIBLE",
                "" if not rounded["feasible"] else ", objective %s" % fmt(rounded["objective"])))
    L.append(ADVISORY)
    return "\n".join(L)


def render_check(model, res):
    L = ["model: %s (%s)" % (model["name"], model["sense"])]
    for t in res["constraints"]:
        L.append("%-10s %s %s %s  slack %s  %s" % (t["name"], fmt(t["lhs"]), t["op"], fmt(t["rhs"]), fmt(t["slack"]),
                                                    "OK" + (" (binding)" if t["binding"] else "") if t["satisfied"] else "VIOLATED"))
    L.append("objective at x = %s" % fmt(res["objective"]))
    L.append("VERDICT: " + ("FEASIBLE" if res["feasible"] else "NOT FEASIBLE - " + "; ".join(res["problems"])))
    L.append(ADVISORY)
    return "\n".join(L)


def int_indices(model, spec):
    if not spec:
        return []
    if spec == "all":
        return list(range(len(model["vars"])))
    names = [s.strip() for s in spec.split(",") if s.strip()]
    bad = [s for s in names if s not in model["vars"]]
    if bad:
        raise ValueError("unknown variable(s) %s; have %s" % (bad, model["vars"]))
    return [model["vars"].index(s) for s in names]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", dest="json_main")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("solve")
    p.add_argument("model")
    p.add_argument("--integer", default="")
    p.add_argument("--delta", default=None, help="change every RHS by this amount and compare with shadow price x delta")
    p.add_argument("--max-combos", type=int, default=300000)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("check")
    p.add_argument("model")
    p.add_argument("--x", nargs="+", required=True)
    p.add_argument("--integer", default="")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("assign")
    p.add_argument("costs")
    p.add_argument("--max", action="store_true", help="maximise instead of minimise")
    p.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    want_json = a.json_main or a.json
    if a.cmd == "assign":
        cost = read_costs(a.costs)
        work = [[-v for v in r] for r in cost] if a.max else cost
        _, pairs = hungarian(work)
        total = sum((cost[r][c] for r, c in pairs), Fr(0))
        res = {"objective": "max" if a.max else "min", "total": total, "pairs": [{"row": r + 1, "col": c + 1, "cost": cost[r][c]} for r, c in pairs]}
        if want_json:
            print(json.dumps(jsonable(res), ensure_ascii=False, indent=1))
        else:
            for pr in res["pairs"]:
                print("row %d -> col %d   cost %s" % (pr["row"], pr["col"], fmt(pr["cost"])))
            print("total %s (%s)" % (fmt(total), res["objective"]))
            print(ADVISORY)
        return 0
    model = load_model(a.model)
    ints = int_indices(model, a.integer)
    if a.cmd == "check":
        res = check_solution(model, a.x, ints)
        if want_json:
            print(json.dumps(jsonable(res), ensure_ascii=False, indent=1))
        else:
            print(render_check(model, res))
        return 0 if res["feasible"] else 1
    sol = solve_lp(model, a.max_combos)
    sp = shadow_prices(model, sol, a.delta) if sol["status"] == "OPTIMAL" else None
    integer = rounded = None
    if ints and sol["status"] == "OPTIMAL":
        integer = solve_integer(model, ints)
        rx = [Fr(round(v)) if j in ints else v for j, v in enumerate(sol["x"])]
        rounded = dict(check_solution(model, rx, ints), x=rx)
    if want_json:
        print(json.dumps(jsonable({"model": model["name"], "lp": sol, "shadow_prices": sp, "integer": integer, "rounded": rounded}),
                         ensure_ascii=False, indent=1))
    else:
        print(render_solve(model, sol, sp, integer, rounded))
    return 0


if __name__ == "__main__":
    sys.exit(main())
