"""Oracle tests for finance-judgment tools (fin_calc.py, statement_ratios.py).

Expected values come from sources OTHER than this code:
  DIGEST = the finance / investing / entrepreneurship digest (SET e-Learning WMD1001, EQD1504), section 1:
           * "save 1,000 baht a month for 30 years": 2% = 486,817 / 5% = 797,266 / 10% = 1,973,928
             (these reproduce exactly with 12,000 baht a year, compounded yearly, paid at year end)
           * "months to a million at 1,000 baht a month": 1.73% = 51y8m, 5.15% = 32y5m, 11.61% = 20y6m
             (digest rounds to the nearest month, so the tool's fractional months must sit within 0.5)
           * rule of 72: 10% -> about 7.2 years
  CARD   = the finance-judgment card: ladder (debt > 15% first, buffer 3-6 / 6-12 months), Fork 2 ratio
           table (current / quick < 1, coverage < 2, profit up + CFO negative = red flag), Fork 8
           (deposit 2% vs inflation 2.5% -> money shrinks 0.5% a year)
  HAND   = arithmetic done by hand in the comments.
Must-fail controls inject the traps the card warns about (simple interest, nominal read as real, naive
debt division / minimum-payment trap, profit without cash flow) and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import json
import math
import os
import subprocess
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(SKILL, "scripts")
sys.path.insert(0, SCRIPTS)
import fin_calc  # noqa: E402
import statement_ratios  # noqa: E402

ADVISORY = "ADVISORY: educational arithmetic, not financial advice"


def cli(script, *args):
    return subprocess.run([sys.executable, os.path.join(SCRIPTS, script), *args], capture_output=True,
                          text=True, encoding="utf-8", timeout=60)


# ------------------------------------------------------------ compound growth (DIGEST section 1)
@pytest.mark.parametrize("rate,expected", [(2, 486817), (5, 797266), (10, 1973928)])
def test_grow_matches_digest_thirty_year_example(rate, expected):
    res = fin_calc.future_value(0, 12000, rate, 30, "annual")
    assert abs(res["future_value"] - expected) < 1.0, (rate, res["future_value"])
    assert res["total_paid_in"] == 360000  # HAND: 12,000 x 30


def test_grow_zero_rate_is_plain_sum():
    # HAND: no growth -> principal + contributions = 5,000 + 100 x 12 = 6,200
    res = fin_calc.future_value(5000, 100, 0, 1, "monthly")
    assert res["future_value"] == pytest.approx(6200)


def test_grow_lump_sum_one_year():
    # HAND: 1,000 x 1.05 = 1,050
    assert fin_calc.future_value(1000, 0, 5, 1, "annual")["future_value"] == pytest.approx(1050)


@pytest.mark.parametrize("rate,expected_months", [(1.73, 620), (5.15, 389), (11.61, 246)])
def test_months_to_million_matches_digest_table(rate, expected_months):
    res = fin_calc.months_to_goal(1_000_000, 1000, rate)
    assert res["reachable"]
    assert abs(res["months"] - expected_months) <= 0.5, (rate, res["months"])


def test_months_to_goal_no_growth_hand():
    # HAND: 12,000 / 1,000 per month at 0% = exactly 12 months
    res = fin_calc.months_to_goal(12000, 1000, 0)
    assert res["months"] == pytest.approx(12) and res["months_ceil"] == 12


def test_months_to_goal_unreachable_is_reported_not_hidden():
    res = fin_calc.months_to_goal(10000, 0, 0)
    assert res["reachable"] is False and res["months"] is None


def test_months_to_goal_already_there():
    assert fin_calc.months_to_goal(5000, 100, 5, principal=6000)["months"] == 0


# ------------------------------------------------------------ back-calculated goal (CARD Fork 6)
def test_goal_zero_rate_hand():
    # HAND: 120,000 in 12 months with no growth = 10,000 a month
    assert fin_calc.required_saving(120000, 12, 0)["required_monthly_saving"] == pytest.approx(10000)


def test_goal_with_monthly_growth_hand():
    # HAND: i = 1%/month (12%/yr), n = 12 -> 1.01^12 = 1.126825 ; PMT = 120,000 x 0.01 / 0.126825 = 9,461.9
    assert fin_calc.required_saving(120000, 12, 12)["required_monthly_saving"] == pytest.approx(9461.9, abs=0.5)


def test_goal_flags_infeasible_surplus_and_stretches_horizon():
    res = fin_calc.required_saving(120000, 12, 0, surplus=8000)
    assert res["feasible"] is False
    assert res["months_at_surplus"] == 15  # HAND: 120,000 / 8,000
    assert fin_calc.required_saving(120000, 12, 0, surplus=10000)["feasible"] is True


def test_goal_current_savings_already_cover_target():
    assert fin_calc.required_saving(100000, 12, 0, current=200000)["required_monthly_saving"] == 0


# ------------------------------------------------------------ rule of 72 (DIGEST) and real rate (CARD Fork 8)
def test_rule72_matches_digest_and_exact():
    res = fin_calc.rule_of_72(10)
    assert res["years_rule72"] == pytest.approx(7.2)           # DIGEST: 10% -> ~7.2 years
    assert res["years_exact"] == pytest.approx(7.2725, abs=1e-3)  # HAND: ln2 / ln1.1 = 0.693147 / 0.095310
    assert res["abs_error_years"] < 0.1


def test_rule72_degrades_at_high_rates():
    # HAND: 36% -> rule gives 2.0 years, exact ln2 / ln1.36 = 0.693147 / 0.307485 = 2.2542
    res = fin_calc.rule_of_72(36)
    assert res["years_exact"] == pytest.approx(2.2542, abs=1e-3)
    assert res["abs_error_years"] > 0.2


def test_real_rate_card_example():
    res = fin_calc.real_rate(2.0, 2.5)
    assert res["real_rate_card_approx_pct"] == pytest.approx(-0.5)        # CARD: money shrinks 0.5%/yr
    assert res["real_rate_exact_pct"] == pytest.approx(-0.4878, abs=1e-3)  # HAND: 1.02 / 1.025 - 1
    assert "NEGATIVE" in res["verdict"]


def test_real_rate_positive_case():
    # HAND: 6% nominal, 2% inflation -> 1.06 / 1.02 - 1 = 3.92%
    res = fin_calc.real_rate(6, 2)
    assert res["real_rate_exact_pct"] == pytest.approx(3.9216, abs=1e-3)
    assert "NEGATIVE" not in res["verdict"]


# ------------------------------------------------------------ emergency fund (CARD ladder step 2)
def test_emergency_months_hand_and_range():
    res = fin_calc.emergency_fund(20000, 90000)
    assert res["months_covered"] == pytest.approx(4.5)  # HAND: 90,000 / 20,000
    assert res["target_months"] == [3, 6] and res["status"] == "IN RANGE"


def test_emergency_below_target_gap_hand():
    res = fin_calc.emergency_fund(20000, 40000)
    assert res["months_covered"] == pytest.approx(2.0)
    assert res["status"].startswith("BELOW") and res["gap_to_low"] == 20000  # HAND: 3 x 20,000 - 40,000


def test_emergency_irregular_income_uses_six_to_twelve():
    res = fin_calc.emergency_fund(20000, 90000, irregular=True)
    assert res["target_months"] == [6, 12]
    assert res["status"].startswith("BELOW") and res["gap_to_low"] == 30000  # HAND: 6 x 20,000 - 90,000
    assert fin_calc.emergency_fund(20000, 90000, dependants=True)["target_months"] == [6, 12]


# ------------------------------------------------------------ debt payoff (CARD ladder step 1)
def test_payoff_one_month_hand():
    # HAND: 1,000 at 12% -> 1%/month = 10 interest ; paying 1,010 clears it in 1 month
    res = fin_calc.debt_payoff(1000, 12, 1010)
    assert res["months"] == 1 and res["total_interest"] == pytest.approx(10)


def test_payoff_zero_apr_hand():
    res = fin_calc.debt_payoff(1200, 0, 100)
    assert res["months"] == 12 and res["total_interest"] == pytest.approx(0)


def test_payoff_matches_closed_form_interest():
    # HAND: 10,000 at 24% (2%/month), pay 1,000. Closed form n = -ln(1 - 0.02 x 10,000/1,000)/ln1.02
    # = -ln(0.8)/ln(1.02) = 11.27 -> 12 payments. After 11 payments balance = 10,000 x 1.02^11
    # - 1,000 x (1.02^11 - 1)/0.02 = 12,433.74 - 12,168.72 = 265.02 ; last payment = 265.02 x 1.02 = 270.32
    # total paid = 11,000 + 270.32 = 11,270.32 -> interest 1,270.32
    res = fin_calc.debt_payoff(10000, 24, 1000)
    assert res["months"] == 12
    assert res["total_interest"] == pytest.approx(1270.32, abs=0.05)
    n = -math.log(1 - 0.02 * 10000 / 1000) / math.log(1.02)
    assert math.ceil(n) == res["months"]


def test_payoff_minimum_payment_trap_never():
    # CARD trap: paying only the interest (or less) never reduces the balance. HAND: 10,000 x 2% = 200
    for pay in (200, 199.99, 50):
        res = fin_calc.debt_payoff(10000, 24, pay)
        assert res["months"] is None and "NEVER" in res["verdict"], pay


def test_payoff_high_interest_flag_threshold_is_strictly_above_15():
    assert fin_calc.debt_payoff(10000, 24, 1000)["high_interest_debt"] is True
    assert fin_calc.debt_payoff(10000, 15, 1000)["high_interest_debt"] is False


# ------------------------------------------------------------ 3-step ladder (CARD)
def test_ladder_rungs():
    assert fin_calc.ladder(24, 1)["step"] == 1                      # debt above 15% comes first
    assert fin_calc.ladder(0, 2)["step"] == 2                       # buffer 2 < 3 months
    assert fin_calc.ladder(0, 5, irregular=True)["step"] == 2       # irregular income needs 6
    assert fin_calc.ladder(0, 7, irregular=True)["step"] == 4
    assert fin_calc.ladder(0, 4, has_insurance=False)["step"] == 3  # buffer ok, no insurance
    assert fin_calc.ladder(0, 4, has_goal=False)["step"] == 3
    assert fin_calc.ladder(0, 4)["step"] == 4


def test_ladder_never_recommends_a_product():
    text = json.dumps(fin_calc.ladder(0, 4), ensure_ascii=False).lower()
    for word in ("buy ", "sell ", "stock", "fund", "crypto"):
        assert word not in text


# ------------------------------------------------------------ CLI contract
def test_cli_help_works_for_both_tools():
    for script in ("fin_calc.py", "statement_ratios.py"):
        r = cli(script, "--help")
        assert r.returncode == 0 and "usage" in r.stdout.lower()


@pytest.mark.parametrize("args", [
    ("grow", "--contrib", "12000", "--rate", "5", "--years", "30"),
    ("months-to-goal", "--target", "1000000", "--contrib", "1000", "--rate", "5.15"),
    ("goal", "--target", "120000", "--months", "12", "--surplus", "8000"),
    ("rule72", "--rate", "10"),
    ("realrate", "--nominal", "2", "--inflation", "2.5"),
    ("emergency", "--expense", "20000", "--cash", "90000"),
    ("payoff", "--balance", "10000", "--apr", "24", "--payment", "1000"),
    ("ladder", "--debt-apr", "24", "--emergency-months", "1"),
])
def test_cli_every_subcommand_prints_advisory_and_json(args):
    r = cli("fin_calc.py", *args)
    assert r.returncode == 0 and ADVISORY in r.stdout
    j = cli("fin_calc.py", *args, "--json")
    assert j.returncode == 0 and json.loads(j.stdout)["advisory"] == ADVISORY
    j2 = cli("fin_calc.py", "--json", *args)
    assert j2.returncode == 0 and json.loads(j2.stdout)["advisory"] == ADVISORY


def test_cli_bad_input_exits_2_with_message():
    r = cli("fin_calc.py", "emergency", "--expense", "0", "--cash", "100")
    assert r.returncode == 2 and "ERROR" in r.stderr


# ------------------------------------------------------------ statement ratios (CARD Fork 2)
FULL = dict(current_assets=300, current_liabilities=200, inventory=120, total_debt=500, equity=250,
            ebit=90, interest=60, revenue=1000, net_income=50, cfo=-20, de_benchmark=1.5)


def by_name(rows):
    return {r["ratio"]: r for r in rows}


def test_ratios_hand_example():
    # HAND: current 300/200 = 1.5 ; quick (300-120)/200 = 0.9 ; D/E 500/250 = 2.0 ; coverage 90/60 = 1.5 ;
    # net margin 50/1000 = 5% ; ROE 50/250 = 20%
    r = by_name(statement_ratios.read_ratios(**FULL))
    assert r["current ratio"]["value"] == pytest.approx(1.5) and r["current ratio"]["flag"] == "OK"
    assert r["quick ratio"]["value"] == pytest.approx(0.9) and r["quick ratio"]["flag"] == "TIGHT"
    assert r["D/E"]["value"] == pytest.approx(2.0) and r["D/E"]["flag"] == "HIGH"
    assert r["interest coverage"]["value"] == pytest.approx(1.5) and r["interest coverage"]["flag"] == "WEAK"
    assert r["net margin %"]["value"] == pytest.approx(5.0)
    assert r["ROE %"]["value"] == pytest.approx(20.0)


def test_cfo_red_flag_when_profit_positive_and_cash_negative():
    # CARD trap: profit positive but operating cash flow negative = red flag
    r = by_name(statement_ratios.read_ratios(**FULL))
    assert r["CFO vs net income"]["flag"] == "RED"


def test_cfo_amber_when_profit_grows_and_cash_falls():
    rows = statement_ratios.read_ratios(net_income=80, cfo=10, net_income_prev=50, cfo_prev=40)
    assert by_name(rows)["CFO vs net income"]["flag"] == "AMBER"


def test_cfo_ok_when_cash_backs_profit():
    rows = statement_ratios.read_ratios(net_income=50, cfo=60)
    assert by_name(rows)["CFO vs net income"]["flag"] == "OK"


def test_de_without_benchmark_is_not_judged():
    rows = by_name(statement_ratios.read_ratios(total_debt=500, equity=250))
    assert rows["D/E"]["value"] == pytest.approx(2.0) and rows["D/E"]["flag"] == "NO-BENCHMARK"


def test_missing_inputs_are_listed_not_dropped():
    rows = by_name(statement_ratios.read_ratios(net_income=50))
    assert rows["current ratio"]["flag"] == "SKIPPED" and "--current-assets" in rows["current ratio"]["reading"]
    assert rows["CFO vs net income"]["flag"] == "SKIPPED"


def test_zero_denominators_do_not_crash():
    rows = by_name(statement_ratios.read_ratios(current_assets=10, current_liabilities=0, ebit=5, interest=0,
                                                total_debt=1, equity=0))
    assert rows["current ratio"]["flag"] == "N/A" and rows["interest coverage"]["flag"] == "N/A"
    assert rows["D/E"]["flag"] == "N/A"


def test_margin_step_down_is_flagged_but_not_called_a_trend():
    rows = by_name(statement_ratios.read_ratios(revenue=1000, net_income=40, revenue_prev=1000,
                                                net_income_prev=60))
    assert rows["net margin %"]["flag"] == "SHRINKING" and "several periods" in rows["net margin %"]["reading"]


def test_ratios_cli_prints_advisory_and_json():
    args = ["--current-assets", "300", "--current-liabilities", "200", "--cfo", "-20", "--net-income", "50"]
    r = cli("statement_ratios.py", *args)
    assert r.returncode == 0 and ADVISORY in r.stdout and "RED" in r.stdout
    j = cli("statement_ratios.py", "--json", *args)
    assert json.loads(j.stdout)["advisory"] == ADVISORY


# ------------------------------------------------------------ MUST-FAIL CONTROLS (inject the card's traps)
def test_must_fail_control_simple_interest_instead_of_compounding(monkeypatch):
    """Trap: forgetting compounding (simple interest). The digest oracle must go red."""
    def simple(principal, contrib, rate_pct, years, freq="annual"):
        n = years
        paid = principal + contrib * n
        interest = contrib * n * (n + 1) / 2 * rate_pct / 100  # simple interest on each deposit
        return {"future_value": paid + interest, "total_paid_in": paid}

    monkeypatch.setattr(fin_calc, "future_value", simple)
    with pytest.raises(AssertionError):
        test_grow_matches_digest_thirty_year_example(5, 797266)


def test_must_fail_control_nominal_read_as_real(monkeypatch):
    """Trap: ignoring inflation (reading nominal as real). The Fork 8 oracle must go red."""
    def nominal_only(nominal_pct, inflation_pct):
        return {"real_rate_card_approx_pct": nominal_pct, "real_rate_exact_pct": nominal_pct, "verdict": "ok"}

    monkeypatch.setattr(fin_calc, "real_rate", nominal_only)
    with pytest.raises(AssertionError):
        test_real_rate_card_example()


def test_must_fail_control_naive_division_hides_the_minimum_payment_trap(monkeypatch):
    """Trap: months = balance / payment ignores interest, so a payment that only covers the interest
    looks like it pays off. The 'NEVER' oracle must go red."""
    def naive(balance, apr_pct, payment, max_months=1200):
        months = math.ceil(balance / payment)
        return {"months": months, "total_interest": 0.0, "verdict": "PAID OFF", "high_interest_debt": False}

    monkeypatch.setattr(fin_calc, "debt_payoff", naive)
    with pytest.raises(AssertionError):
        test_payoff_minimum_payment_trap_never()
    with pytest.raises(AssertionError):
        test_payoff_matches_closed_form_interest()


def test_must_fail_control_profit_without_cash_flow(monkeypatch):
    """Trap: reading only the profit and loss statement. Dropping the CFO row must turn the oracle red."""
    real = statement_ratios.read_ratios

    def no_cfo(**kw):
        kw.pop("cfo", None)
        return real(**kw)

    monkeypatch.setattr(statement_ratios, "read_ratios", no_cfo)
    with pytest.raises(AssertionError):
        test_cfo_red_flag_when_profit_positive_and_cash_negative()


def test_must_fail_control_ladder_that_lets_high_interest_debt_wait(monkeypatch):
    """Trap: investing before clearing >15% debt. A ladder that skips step 1 must fail the rung oracle."""
    real = fin_calc.ladder

    def skip_debt(debt_apr_pct, *a, **kw):
        return real(0, *a, **kw)

    monkeypatch.setattr(fin_calc, "ladder", skip_debt)
    with pytest.raises(AssertionError):
        test_ladder_rungs()
