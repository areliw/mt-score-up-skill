"""Oracle tests for scripts/lp_check.py.

Expected numbers come from places other than this code:
  HL    = Hillier & Lieberman, Introduction to Operations Research, Wyndor Glass Co. example (ch.3-4):
          max 3x1+5x2, x1<=4, 2x2<=12, 3x1+2x2<=18 -> (2, 6), Z = 36; dual solution y = (0, 3/2, 1)
  TAXA  = Taha, Operations Research, Reddy Mikks model: max 5x1+4x2 s.t. 6x1+4x2<=24, x1+2x2<=6, -x1+x2<=1, x2<=2
          -> LP optimum (3, 1.5), Z = 21
  WIN   = Winston, Operations Research, assignment example "Machineco" (4 machines x 4 jobs): minimum total 15
  261475= CMU 261475 course digest: tableau example max 350x1+300x2 (12x1+16x2<=2880, 9x1+6x2<=1566, x1+x2<=200)
          -> x1=122, x2=78, Z=66,100, slack S1=168, S2 and S3 binding, shadow price of S2 = 16.67; the digest's
          "Unbounded" case: max 3x1+4x2, x1-x2<=1, -x1+x2<=2
  HAND  = arithmetic in the comment next to each assertion
Must-fail controls inject the traps the card warns about (a forgotten constraint, rounding an LP answer instead of
solving the integer program, extrapolating a shadow price outside its allowable range) and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import itertools
import json
import os
import random
import sys
from fractions import Fraction as Fr

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import lp_check  # noqa: E402

DATA = os.path.join(SKILL, "data")


def model(name):
    return lp_check.load_model(os.path.join(DATA, name))


def make(sense, c, cons):
    return lp_check.parse_model({"name": "t", "sense": sense, "vars": ["x%d" % (i + 1) for i in range(len(c))], "c": c,
                                 "constraints": [{"name": "k%d" % i, "a": a, "op": op, "b": b} for i, (a, op, b) in enumerate(cons)]})


def sp_by_name(m, sol):
    return {r["name"]: r["shadow_price"] for r in lp_check.shadow_prices(m, sol)}


# ---------------------------------------------------------------- LP optimum, binding, shadow price
def test_wyndor_optimum_and_duals_match_textbook():
    m = model("wyndor.json")
    s = lp_check.solve_lp(m)
    assert s["status"] == "OPTIMAL"
    assert s["x"] == [2, 6] and s["objective"] == 36        # HL; HAND: 3*2 + 5*6 = 36
    sp = sp_by_name(m, s)
    assert (sp["plant1"], sp["plant2"], sp["plant3"]) == (0, Fr(3, 2), 1)  # HL dual y = (0, 3/2, 1)
    # strong duality, HAND: 4*0 + 12*(3/2) + 18*1 = 36 = primal optimum
    assert 4 * sp["plant1"] + 12 * sp["plant2"] + 18 * sp["plant3"] == 36
    table = {t["name"]: t for t in lp_check.constraint_table(m, s["x"])}
    assert [table[k]["binding"] for k in ("plant1", "plant2", "plant3")] == [False, True, True]
    assert table["plant1"]["slack"] == 2                      # HAND: 4 - 1*2


def test_course_tableau_example_matches_261475_digest():
    m = model("tableau_example.json")
    s = lp_check.solve_lp(m)
    assert s["x"] == [122, 78] and s["objective"] == 66100    # digest; HAND: 350*122 + 300*78 = 42700 + 23400
    table = {t["name"]: t for t in lp_check.constraint_table(m, s["x"])}
    assert table["S1"]["slack"] == 168                        # HAND: 2880 - (12*122 + 16*78) = 2880 - 2712
    assert table["S2"]["binding"] and table["S3"]["binding"]
    sp = sp_by_name(m, s)
    assert float(sp["S2"]) == pytest.approx(16.67, abs=0.005)  # digest: "S2 shadow price = 16.67"
    # HAND: binding S2,S3:  9y2 + y3 = 350 ; 6y2 + y3 = 300  =>  3y2 = 50, y2 = 50/3, y3 = 200 ; S1 non-binding => 0
    assert (sp["S1"], sp["S2"], sp["S3"]) == (0, Fr(50, 3), 200)
    assert 2880 * sp["S1"] + 1566 * sp["S2"] + 200 * sp["S3"] == 66100  # dual objective = primal objective


def test_minimisation_and_equality_constraint():
    # HAND: min 2x1+3x2, x1+x2>=4, x1<=3 : x1 is cheaper so x1=3, x2=1 -> 2*3+3*1 = 9
    s = lp_check.solve_lp(make("min", [2, 3], [([1, 1], ">=", 4), ([1, 0], "<=", 3)]))
    assert s["status"] == "OPTIMAL" and s["x"] == [3, 1] and s["objective"] == 9
    # HAND: max x1 s.t. x1 + x2 = 3, x2 >= 1 -> x2 = 1, x1 = 2, objective 2
    s = lp_check.solve_lp(make("max", [1, 0], [([1, 1], "=", 3), ([0, 1], ">=", 1)]))
    assert s["x"] == [2, 1] and s["objective"] == 2


def test_alternate_optima_are_reported():
    # HAND: max x1+x2 s.t. x1+x2<=4 : the whole edge is optimal; its vertices (4,0) and (0,4) both give 4
    s = lp_check.solve_lp(make("max", [1, 1], [([1, 1], "<=", 4)]))
    assert s["objective"] == 4 and sorted(s["optimal_vertices"]) == [[0, 4], [4, 0]]


# ---------------------------------------------------------------- infeasible / unbounded
def test_unbounded_case_from_digest():
    s = lp_check.solve_lp(model("unbounded_example.json"))
    assert s["status"] == "UNBOUNDED"                         # 261475 digest special case
    assert s["ray"] == [1, 1]                                 # HAND: x1 = x2 = t keeps both constraints, objective 7t -> infinity


def test_infeasible_case():
    # HAND: x1+x2<=1 and x1+x2>=3 cannot both hold
    s = lp_check.solve_lp(make("max", [1, 1], [([1, 1], "<=", 1), ([1, 1], ">=", 3)]))
    assert s["status"] == "INFEASIBLE"


# ---------------------------------------------------------------- shadow price allowable range
def test_shadow_price_valid_inside_range_wrong_outside():
    m = model("wyndor.json")
    s = lp_check.solve_lp(m)
    inside = {r["name"]: r for r in lp_check.shadow_prices(m, s, 6)}["plant3"]
    # HAND: plant3 RHS 18 -> 24 keeps x = (4,6): 3*4 + 5*6 = 42 = 36 + 1*6 -> prediction holds
    assert inside["actual_change"] == 6 and inside["within_allowable_range"] is True
    outside = {r["name"]: r for r in lp_check.shadow_prices(m, s, 12)}["plant3"]
    # HAND: RHS 30 is no longer binding (x1<=4, x2<=6 cap the answer at (4,6) = 42): actual +6, shadow x delta = +12
    assert outside["actual_change"] == 6 and outside["predicted_change"] == 12
    assert outside["within_allowable_range"] is False


# ---------------------------------------------------------------- integer programming
def test_integer_optimum_is_not_the_rounded_lp_answer():
    m = model("reddy_mikks.json")
    lp = lp_check.solve_lp(m)
    assert lp["x"] == [3, Fr(3, 2)] and lp["objective"] == 21                 # TAXA
    ip = lp_check.solve_integer(m, [0, 1])
    # HAND: lattice points feasible for 6x1+4x2<=24, x1+2x2<=6, x2<=2 : (4,0)=20, (3,1)=19, (2,2)=18, (3,2) needs 26>24
    assert ip["status"] == "OPTIMAL" and ip["x"] == [4, 0] and ip["objective"] == 20
    naive = lp_check.check_solution(m, [3, 2], [0, 1])                        # round(1.5) = 2
    assert naive["feasible"] is False                                          # 6*3 + 4*2 = 26 > 24
    best_floor = lp_check.check_solution(m, [3, 1], [0, 1])
    assert best_floor["feasible"] and best_floor["objective"] == 19 < ip["objective"]


def test_integer_variables_can_be_a_subset():
    m = model("reddy_mikks.json")
    mixed = lp_check.solve_integer(m, [0])  # only x1 integer: LP answer x1 = 3 already integral
    assert mixed["x"] == [3, Fr(3, 2)] and mixed["objective"] == 21


# ---------------------------------------------------------------- audit a candidate answer (forgotten constraint)
def test_check_solution_catches_the_forgotten_constraint():
    full = model("wyndor.json")
    forgot = make("max", [3, 5], [([1, 0], "<=", 4), ([0, 2], "<=", 12)])      # plant3 left out of the model
    wrong = lp_check.solve_lp(forgot)
    assert wrong["x"] == [4, 6] and wrong["objective"] == 42                    # HAND: 3*4 + 5*6, "looks better than 36"
    res = lp_check.check_solution(full, wrong["x"])
    assert res["feasible"] is False and any("plant3" in p for p in res["problems"])  # HAND: 3*4 + 2*6 = 24 > 18
    assert lp_check.check_solution(full, [2, 6])["feasible"] is True


def test_check_reports_negativity_and_integrality():
    m = model("reddy_mikks.json")
    res = lp_check.check_solution(m, [3, Fr(3, 2)], [0, 1])
    assert not res["feasible"] and any("x2" in p and "integer" in p for p in res["problems"])
    assert any("< 0" in p for p in lp_check.check_solution(m, [-1, 0])["problems"])


# ---------------------------------------------------------------- assignment
def test_machineco_assignment_total_15():
    cost = lp_check.read_costs(os.path.join(DATA, "machineco.csv"))
    total, pairs = lp_check.hungarian(cost)
    assert total == 15                                                          # WIN
    assert pairs == [(0, 1), (1, 3), (2, 2), (3, 0)]                            # HAND: 5 + 5 + 3 + 2
    assert sum(cost[r][c] for r, c in pairs) == 15
    # independent check by brute force over all 4! = 24 assignments
    assert min(sum(cost[i][p[i]] for i in range(4)) for p in itertools.permutations(range(4))) == 15


def test_hungarian_matches_brute_force_on_random_matrices():
    rnd = random.Random(7)
    for _ in range(25):
        n = rnd.choice([3, 4, 5, 6])
        cost = [[Fr(rnd.randint(1, 20)) for _ in range(n)] for _ in range(n)]
        brute = min(sum(cost[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n)))  # independent algorithm
        assert lp_check.hungarian(cost)[0] == brute
        negated = [[-v for v in r] for r in cost]
        best = max(sum(cost[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n)))
        assert -lp_check.hungarian(negated)[0] == best                           # maximisation by negation


# ---------------------------------------------------------------- CLI
def test_cli_solve_json_and_check_exit_code(capsys):
    assert lp_check.main(["--json", "solve", os.path.join(DATA, "wyndor.json")]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["lp"]["status"] == "OPTIMAL" and out["lp"]["objective"]["exact"] == "36"
    assert lp_check.main(["check", os.path.join(DATA, "wyndor.json"), "--x", "4", "6"]) == 1   # violates plant3
    assert "VIOLATED" in capsys.readouterr().out
    assert lp_check.main(["check", os.path.join(DATA, "wyndor.json"), "--x", "2", "6"]) == 0


def test_help_runs():
    with pytest.raises(SystemExit) as e:
        lp_check.main(["--help"])
    assert e.value.code == 0


def test_oversized_model_is_refused():
    big = make("max", [1] * 8, [([1] * 8, "<=", 10)] * 12)
    with pytest.raises(ValueError):
        lp_check.solve_lp(big, max_combos=1000)


# ---------------------------------------------------------------- must-fail controls (trap injected -> oracle must go red)
def test_must_fail_control_forgotten_constraint(monkeypatch):
    """Trap: the solver is never told about the last constraint. The Wyndor optimum oracle must go red."""
    real = lp_check.le_rows
    monkeypatch.setattr(lp_check, "le_rows", lambda m: real(dict(m, constraints=m["constraints"][:-1])))
    with pytest.raises(AssertionError):
        test_wyndor_optimum_and_duals_match_textbook()


def test_must_fail_control_round_the_lp_answer(monkeypatch):
    """Trap: forget integrality and round the LP answer. The integer-optimum oracle must go red."""
    def rounding(model, int_vars, max_nodes=20000):
        lp = lp_check.solve_lp(model)
        x = [Fr(round(v)) if j in int_vars else v for j, v in enumerate(lp["x"])]
        return {"status": "OPTIMAL", "x": x, "objective": lp_check.dot(model["c"], x), "nodes": 1}
    monkeypatch.setattr(lp_check, "solve_integer", rounding)
    with pytest.raises(AssertionError):
        test_integer_optimum_is_not_the_rounded_lp_answer()


def test_must_fail_control_shadow_price_extrapolated(monkeypatch):
    """Trap: assume shadow price x delta holds for any delta. The allowable-range oracle must go red."""
    real = lp_check.shadow_prices

    def extrapolate(model, sol, delta=None):
        rows = real(model, sol, delta)
        for r in rows:
            if "within_allowable_range" in r:
                r["actual_change"] = r["predicted_change"]
                r["within_allowable_range"] = True
        return rows
    monkeypatch.setattr(lp_check, "shadow_prices", extrapolate)
    with pytest.raises(AssertionError):
        test_shadow_price_valid_inside_range_wrong_outside()
