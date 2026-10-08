#!/usr/bin/env python3
"""fin_calc - small, checkable personal-finance arithmetic for finance-judgment.

Black-box tool: run it BEFORE doing the arithmetic by hand. It only does the sums the card already
teaches (compound growth, months-to-goal, back-calculated saving, rule of 72, real vs nominal rate,
emergency-fund months, debt payoff, the 3-step ladder). It never picks securities or trades.
Every rate is an assumption you pass in - nothing here predicts a return.

Conventions (stated so the output can be audited):
  * annual mode  : contribution C once per YEAR (end of year), rate compounds yearly
  * monthly mode : contribution C once per MONTH (end of month), monthly rate = annual rate / 12
  * rates are given in percent (5 = 5%)

Examples
  python fin_calc.py grow --contrib 12000 --rate 5 --years 30                    # annual mode
  python fin_calc.py grow --contrib 1000 --rate 5 --years 30 --freq monthly
  python fin_calc.py months-to-goal --target 1000000 --contrib 1000 --rate 5.15
  python fin_calc.py goal --target 120000 --months 12 --rate 0 --surplus 8000
  python fin_calc.py rule72 --rate 10
  python fin_calc.py realrate --nominal 2 --inflation 2.5
  python fin_calc.py emergency --expense 20000 --cash 90000 [--irregular-income] [--dependants]
  python fin_calc.py payoff --balance 10000 --apr 24 --payment 1000
  python fin_calc.py ladder --debt-apr 24 --emergency-months 1
"""
import argparse
import json
import math
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print arrows/Greek and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ADVISORY = "ADVISORY: educational arithmetic, not financial advice"
HIGH_DEBT_APR = 15.0          # card ladder step 1: debt APR above this is paid before investing
EF_STABLE = (3, 6)            # card: emergency fund months, stable salary
EF_IRREGULAR = (6, 12)        # card: freelance / irregular income / dependants


def _need(cond, msg):
    if not cond:
        raise ValueError(msg)


# ------------------------------------------------------------------ growth
def future_value(principal, contrib, rate_pct, years, freq="annual"):
    """FV of a lump sum plus level end-of-period contributions."""
    _need(principal >= 0 and contrib >= 0 and years > 0, "principal/contrib must be >= 0 and years > 0")
    _need(rate_pct > -100, "rate must be > -100%")
    if freq == "annual":
        n, i = years, rate_pct / 100.0
    elif freq == "monthly":
        n, i = years * 12, rate_pct / 100.0 / 12.0
    else:
        raise ValueError("freq must be annual or monthly")
    growth_factor = (1 + i) ** n
    annuity_factor = n if i == 0 else (growth_factor - 1) / i
    fv_principal = principal * growth_factor
    fv_contrib = contrib * annuity_factor
    paid_in = principal + contrib * n
    fv = fv_principal + fv_contrib
    return {
        "freq": freq, "periods": n, "rate_per_period": i,
        "growth_factor": growth_factor, "annuity_factor": annuity_factor,
        "fv_of_principal": fv_principal, "fv_of_contributions": fv_contrib,
        "total_paid_in": paid_in, "future_value": fv, "growth_part": fv - paid_in,
        "formula": "FV = P*(1+i)^n + C*((1+i)^n - 1)/i  (C paid at END of each period)",
    }


def months_to_goal(target, contrib, rate_pct, principal=0.0):
    """Months (monthly compounding, end-of-month contributions) until balance >= target."""
    _need(target > 0 and contrib >= 0 and principal >= 0, "target > 0, contrib/principal >= 0")
    i = rate_pct / 100.0 / 12.0
    base = {"target": target, "contrib": contrib, "principal": principal, "monthly_rate": i,
            "formula": "x=(T+C/i)/(P+C/i); n=ln(x)/ln(1+i)  (i=0: n=(T-P)/C)"}
    if principal >= target:
        return dict(base, months=0.0, months_ceil=0, whole_years=0, rest_months=0, reachable=True)
    if i == 0:
        if contrib == 0:
            return dict(base, months=None, months_ceil=None, reachable=False,
                        note="NEVER: no contribution and no growth")
        n = (target - principal) / contrib
    else:
        _need(i > -1, "rate too negative")
        shift = contrib / i                      # the C/i term of the closed form
        top, bottom = target + shift, principal + shift
        x = top / bottom if bottom != 0 else 0.0
        n = math.log(x) / math.log(1 + i) if x > 0 else 0.0
        if n <= 0:                                # nothing invested, or a negative rate caps the balance
            return dict(base, months=None, months_ceil=None, reachable=False,
                        note="NEVER: nothing invested, or the rate caps the balance below the target")
    ceil_n = math.ceil(n - 1e-9)
    return dict(base, months=n, months_ceil=ceil_n, whole_years=ceil_n // 12, rest_months=ceil_n % 12,
                reachable=True, note="months = exact (fractional); months_ceil = first month-end at/above target")


def required_saving(target, months, rate_pct, current=0.0, surplus=None):
    """Back-calculate the monthly saving that reaches target in `months` (card Fork 6)."""
    _need(target > 0 and months > 0 and current >= 0, "target > 0, months > 0, current >= 0")
    i = rate_pct / 100.0 / 12.0
    growth = (1 + i) ** months
    need_after_current = target - current * growth
    if need_after_current <= 0:
        pmt = 0.0
    elif i == 0:
        pmt = need_after_current / months
    else:
        pmt = need_after_current * i / (growth - 1)
    res = {"target": target, "months": months, "monthly_rate": i, "current": current,
           "growth_factor": growth, "target_minus_grown_current": need_after_current,
           "required_monthly_saving": pmt,
           "formula": "PMT = (T - P*(1+i)^n) * i / ((1+i)^n - 1)  (i=0: (T-P)/n)"}
    if surplus is not None:
        _need(surplus >= 0, "surplus must be >= 0")
        res["monthly_surplus"] = surplus
        res["feasible"] = pmt <= surplus + 1e-9
        if res["feasible"]:
            res["verdict"] = "FEASIBLE: required saving fits the stated monthly surplus"
        else:
            alt = months_to_goal(target, surplus, rate_pct, current)
            res["months_at_surplus"] = alt.get("months_ceil")
            res["verdict"] = ("NOT FEASIBLE at this surplus: adjust the target, raise income, or stretch the "
                              "time (months_at_surplus shows the stretched horizon)")
    return res


def rule_of_72(rate_pct):
    _need(rate_pct > 0, "rate must be > 0")
    approx = 72.0 / rate_pct
    exact = math.log(2) / math.log(1 + rate_pct / 100.0)
    return {"rate_pct": rate_pct, "years_rule72": approx, "years_exact": exact,
            "abs_error_years": abs(approx - exact),
            "formula": "approx = 72 / rate% ;  exact = ln2 / ln(1+rate)"}


def real_rate(nominal_pct, inflation_pct):
    n, f = nominal_pct / 100.0, inflation_pct / 100.0
    _need(f > -1, "inflation must be > -100%")
    approx = nominal_pct - inflation_pct
    exact = ((1 + n) / (1 + f) - 1) * 100.0
    verdict = ("NEGATIVE real return: purchasing power shrinks (cash beyond the buffer loses to inflation)"
               if exact < 0 else "real return >= 0: purchasing power is kept or grows")
    return {"nominal_pct": nominal_pct, "inflation_pct": inflation_pct, "real_rate_card_approx_pct": approx,
            "real_rate_exact_pct": exact, "verdict": verdict,
            "formula": "card: real ~ nominal - inflation ;  exact (Fisher): (1+nominal)/(1+inflation) - 1"}


def emergency_fund(expense, cash, irregular=False, dependants=False):
    _need(expense > 0 and cash >= 0, "expense > 0 and cash >= 0")
    lo, hi = EF_IRREGULAR if (irregular or dependants) else EF_STABLE
    months = cash / expense
    if months < lo:
        status = "BELOW target: build the buffer before risking money"
    elif months <= hi:
        status = "IN RANGE"
    else:
        status = "ABOVE range: surplus beyond the buffer is the money whose horizon decides its vehicle (Fork 1)"
    return {"monthly_expense": expense, "cash": cash, "months_covered": months,
            "target_months": [lo, hi], "gap_to_low": max(0.0, lo * expense - cash),
            "gap_to_high": max(0.0, hi * expense - cash), "status": status,
            "formula": "months = cash / monthly_expense ; target 3-6 (stable salary) or 6-12 (irregular/dependants)"}


def debt_payoff(balance, apr_pct, payment, max_months=1200):
    _need(balance > 0 and apr_pct >= 0 and payment > 0, "balance > 0, apr >= 0, payment > 0")
    i = apr_pct / 100.0 / 12.0
    first_interest = balance * i
    high = apr_pct > HIGH_DEBT_APR
    res = {"balance": balance, "apr_pct": apr_pct, "monthly_rate": i, "payment": payment,
           "first_month_interest": first_interest, "high_interest_debt": high,
           "formula": "each month: interest = balance*i ; balance = balance + interest - payment"}
    if payment <= first_interest + 1e-9:
        res.update(months=None, total_paid=None, total_interest=None, payoff=False,
                   verdict="NEVER: payment <= monthly interest, the balance does not fall (minimum-payment trap)")
        return res
    bal, total_paid, months = balance, 0.0, 0
    while bal > 1e-9 and months < max_months:
        interest = bal * i
        due = bal + interest
        pay = min(payment, due)
        bal = due - pay
        total_paid += pay
        months += 1
    res.update(months=months, total_paid=total_paid, total_interest=total_paid - balance, payoff=bal <= 1e-6,
               verdict=("PAID OFF" if bal <= 1e-6 else "NOT paid off within %d months" % max_months))
    if high:
        res["ladder_note"] = "APR > %.0f%%: ladder step 1 - clear this before taking investment risk" % HIGH_DEBT_APR
    return res


def ladder(debt_apr_pct, emergency_months, irregular=False, dependants=False, has_insurance=None,
           has_goal=None):
    """Which rung of the card's 3-step ladder (debt -> buffer -> insurance/goal -> invest) you stand on."""
    lo, hi = EF_IRREGULAR if (irregular or dependants) else EF_STABLE
    if debt_apr_pct > HIGH_DEBT_APR:
        step, msg = 1, "STEP 1: debt above %.0f%% APR first (a guaranteed negative 'return' if left open)" % HIGH_DEBT_APR
    elif emergency_months < lo:
        step, msg = 2, "STEP 2: emergency buffer %.1f months < %d-%d target" % (emergency_months, lo, hi)
    elif has_insurance is False or has_goal is False:
        step = 3
        missing = [n for n, v in (("insurance", has_insurance), ("clear goal", has_goal)) if v is False]
        msg = "STEP 3 incomplete: missing %s" % " + ".join(missing)
    else:
        step, msg = 4, ("Ladder cleared: only the surplus is 'investable'; its vehicle is decided by horizon "
                        "(Fork 1), not by this tool")
    return {"debt_apr_pct": debt_apr_pct, "emergency_months": emergency_months, "target_months": [lo, hi],
            "has_insurance": has_insurance, "has_goal": has_goal, "step": step, "verdict": msg,
            "formula": "debt > %.0f%% APR -> buffer < target -> insurance/goal -> only then invest" % HIGH_DEBT_APR}


# ------------------------------------------------------------------ CLI
def _fmt(v):
    if isinstance(v, bool) or v is None:
        return str(v)
    if isinstance(v, float):
        return "%.6g" % v if abs(v) < 1e-3 else "%.4f" % v
    return str(v)


def _print_report(title, res):
    print("== %s ==" % title)
    for k, v in res.items():
        print("%-26s %s" % (k, _fmt(v) if not isinstance(v, (list, dict)) else json.dumps(v, ensure_ascii=False)))
    print(ADVISORY)


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="machine-readable output")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("grow", parents=[common], help="future value with level contributions")
    p.add_argument("--principal", type=float, default=0.0)
    p.add_argument("--contrib", type=float, default=0.0, help="per year (annual) or per month (monthly)")
    p.add_argument("--rate", type=float, required=True, help="annual rate, percent")
    p.add_argument("--years", type=float, required=True)
    p.add_argument("--freq", choices=["annual", "monthly"], default="annual")

    p = sub.add_parser("months-to-goal", parents=[common], help="months until a target is reached")
    p.add_argument("--target", type=float, required=True)
    p.add_argument("--contrib", type=float, default=0.0, help="per month")
    p.add_argument("--rate", type=float, required=True, help="annual rate, percent (monthly compounding)")
    p.add_argument("--principal", type=float, default=0.0)

    p = sub.add_parser("goal", parents=[common], help="monthly saving needed for a target (back-calc)")
    p.add_argument("--target", type=float, required=True)
    p.add_argument("--months", type=float, required=True)
    p.add_argument("--rate", type=float, default=0.0, help="annual rate, percent (assumption, not a promise)")
    p.add_argument("--current", type=float, default=0.0)
    p.add_argument("--surplus", type=float, default=None, help="what you can actually save per month")

    p = sub.add_parser("rule72", parents=[common], help="doubling time: rule of 72 vs exact")
    p.add_argument("--rate", type=float, required=True, help="percent")

    p = sub.add_parser("realrate", parents=[common], help="real vs nominal return")
    p.add_argument("--nominal", type=float, required=True, help="percent")
    p.add_argument("--inflation", type=float, required=True, help="percent")

    p = sub.add_parser("emergency", parents=[common], help="emergency-fund months covered")
    p.add_argument("--expense", type=float, required=True, help="monthly living expense")
    p.add_argument("--cash", type=float, required=True, help="liquid cash set aside")
    p.add_argument("--irregular-income", action="store_true", help="freelance / uneven income -> 6-12 months")
    p.add_argument("--dependants", action="store_true", help="people depend on you -> 6-12 months")

    p = sub.add_parser("payoff", parents=[common], help="months and interest to clear a debt")
    p.add_argument("--balance", type=float, required=True)
    p.add_argument("--apr", type=float, required=True, help="percent per year")
    p.add_argument("--payment", type=float, required=True, help="paid every month")

    p = sub.add_parser("ladder", parents=[common], help="which rung of debt -> buffer -> insurance -> invest")
    p.add_argument("--debt-apr", type=float, default=0.0, help="highest APR among your debts (0 = none)")
    p.add_argument("--emergency-months", type=float, required=True)
    p.add_argument("--irregular-income", action="store_true")
    p.add_argument("--dependants", action="store_true")
    p.add_argument("--no-insurance", action="store_true")
    p.add_argument("--no-goal", action="store_true")
    return ap


def run(a):
    if a.cmd == "grow":
        return "grow", future_value(a.principal, a.contrib, a.rate, a.years, a.freq)
    if a.cmd == "months-to-goal":
        return "months-to-goal", months_to_goal(a.target, a.contrib, a.rate, a.principal)
    if a.cmd == "goal":
        return "goal", required_saving(a.target, a.months, a.rate, a.current, a.surplus)
    if a.cmd == "rule72":
        return "rule72", rule_of_72(a.rate)
    if a.cmd == "realrate":
        return "realrate", real_rate(a.nominal, a.inflation)
    if a.cmd == "emergency":
        return "emergency", emergency_fund(a.expense, a.cash, a.irregular_income, a.dependants)
    if a.cmd == "payoff":
        return "payoff", debt_payoff(a.balance, a.apr, a.payment)
    return "ladder", ladder(a.debt_apr, a.emergency_months, a.irregular_income, a.dependants,
                            False if a.no_insurance else None, False if a.no_goal else None)


def main(argv=None):
    a = build_parser().parse_args(argv)
    try:
        title, res = run(a)
    except ValueError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2
    if getattr(a, "json", False):
        print(json.dumps(dict(res, advisory=ADVISORY), ensure_ascii=False, indent=1))
    else:
        _print_report(title, res)
    return 0


if __name__ == "__main__":
    sys.exit(main())
