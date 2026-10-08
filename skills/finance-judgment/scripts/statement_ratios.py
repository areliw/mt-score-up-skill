#!/usr/bin/env python3
"""statement_ratios - read simple financial-statement ratios the way the finance-judgment card says to.

Black-box tool: pass whatever numbers you have; it prints each ratio with its formula, the inputs it
used, and the card's warning sign. A ratio whose inputs are missing is listed as SKIPPED (never
silently dropped). Benchmarks that depend on the industry (D/E) are arguments you supply - nothing
here is a verdict on a company, and nothing recommends buying or selling anything.

Card thresholds used (Fork 2):  current / quick ratio < 1 = tight liquidity ; interest coverage < 2 =
weak ; D/E above the industry benchmark you pass in ; profit up while operating cash flow (CFO) is
negative = red flag (profit is accrual, cash is harder to fake).

Examples
  python statement_ratios.py --current-assets 300 --current-liabilities 200 --inventory 120 \\
      --total-debt 500 --equity 250 --ebit 90 --interest 60 --revenue 1000 --net-income 50 --cfo -20 \\
      --de-benchmark 1.5
"""
import argparse
import json
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print arrows/Greek and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ADVISORY = "ADVISORY: educational arithmetic, not financial advice"
LIQUIDITY_MIN = 1.0
COVERAGE_MIN = 2.0


def _row(name, value, formula, flag, reading, inputs):
    return {"ratio": name, "value": value, "formula": formula, "flag": flag, "reading": reading,
            "inputs": inputs}


def _skip(name, needs):
    return {"ratio": name, "value": None, "formula": None, "flag": "SKIPPED",
            "reading": "missing inputs: " + ", ".join(needs), "inputs": {}}


def _div(num, den):
    return None if den in (0, None) else num / den


def read_ratios(current_assets=None, current_liabilities=None, inventory=None, total_debt=None, equity=None,
                ebit=None, interest=None, revenue=None, cogs=None, gross_profit=None, net_income=None,
                total_assets=None, cfo=None, de_benchmark=None, net_income_prev=None, revenue_prev=None,
                cfo_prev=None):
    rows = []

    # --- liquidity
    if current_assets is not None and current_liabilities is not None:
        cr = _div(current_assets, current_liabilities)
        if cr is None:
            rows.append(_row("current ratio", None, "CA / CL", "N/A", "current liabilities = 0",
                             {"current_assets": current_assets, "current_liabilities": current_liabilities}))
        else:
            tight = cr < LIQUIDITY_MIN
            rows.append(_row("current ratio", cr, "current assets / current liabilities",
                             "TIGHT" if tight else "OK",
                             "< 1: short-term bills exceed short-term assets" if tight else ">= 1",
                             {"current_assets": current_assets, "current_liabilities": current_liabilities}))
        if inventory is not None:
            qr = _div(current_assets - inventory, current_liabilities)
            if qr is not None:
                tight = qr < LIQUIDITY_MIN
                rows.append(_row("quick ratio", qr, "(current assets - inventory) / current liabilities",
                                 "TIGHT" if tight else "OK",
                                 "< 1 without leaning on stock" if tight else ">= 1",
                                 {"current_assets": current_assets, "inventory": inventory,
                                  "current_liabilities": current_liabilities}))
        else:
            rows.append(_skip("quick ratio", ["--inventory"]))
    else:
        rows.append(_skip("current ratio", ["--current-assets", "--current-liabilities"]))
        rows.append(_skip("quick ratio", ["--current-assets", "--current-liabilities", "--inventory"]))

    # --- solvency
    if total_debt is not None and equity is not None:
        de = _div(total_debt, equity)
        if de is None:
            rows.append(_row("D/E", None, "total debt / equity", "N/A", "equity = 0", {}))
        elif de_benchmark is None:
            rows.append(_row("D/E", de, "total debt / equity", "NO-BENCHMARK",
                             "compare with the same industry and with the firm's own trend; pass "
                             "--de-benchmark to flag", {"total_debt": total_debt, "equity": equity}))
        else:
            high = de > de_benchmark
            rows.append(_row("D/E", de, "total debt / equity", "HIGH" if high else "OK",
                             "above the industry benchmark you supplied (%.2f)" % de_benchmark if high
                             else "at or below the benchmark you supplied (%.2f)" % de_benchmark,
                             {"total_debt": total_debt, "equity": equity, "benchmark": de_benchmark}))
    else:
        rows.append(_skip("D/E", ["--total-debt", "--equity"]))
    if ebit is not None and interest is not None:
        ic = _div(ebit, interest)
        if ic is None:
            rows.append(_row("interest coverage", None, "EBIT / interest expense", "N/A",
                             "interest expense = 0 (no interest burden)", {"ebit": ebit, "interest": interest}))
        else:
            weak = ic < COVERAGE_MIN
            rows.append(_row("interest coverage", ic, "EBIT / interest expense", "WEAK" if weak else "OK",
                             "< 2: thin cushion to pay interest" if weak else ">= 2",
                             {"ebit": ebit, "interest": interest}))
    else:
        rows.append(_skip("interest coverage", ["--ebit", "--interest"]))

    # --- profitability
    if revenue is not None and (gross_profit is not None or cogs is not None):
        gp = gross_profit if gross_profit is not None else revenue - cogs
        gm = _div(gp, revenue)
        if gm is not None:
            rows.append(_row("gross margin %", gm * 100, "(revenue - COGS) / revenue", "INFO", "compare with industry",
                             {"revenue": revenue, "gross_profit": gp}))
    else:
        rows.append(_skip("gross margin %", ["--revenue", "--gross-profit or --cogs"]))
    if revenue is not None and net_income is not None:
        nm = _div(net_income, revenue)
        if nm is not None:
            flag, reading = "INFO", "compare with industry and own trend"
            if net_income_prev is not None and revenue_prev:
                prev = net_income_prev / revenue_prev
                if nm < prev:
                    flag = "SHRINKING"
                    reading = ("margin %.2f%% vs prior %.2f%% - one step down; the card's warning needs the fall "
                               "to persist over several periods" % (nm * 100, prev * 100))
            rows.append(_row("net margin %", nm * 100, "net income / revenue", flag, reading,
                             {"revenue": revenue, "net_income": net_income}))
    else:
        rows.append(_skip("net margin %", ["--revenue", "--net-income"]))
    if net_income is not None and equity is not None and _div(net_income, equity) is not None:
        rows.append(_row("ROE %", net_income / equity * 100, "net income / equity", "INFO",
                         "read together with D/E (leverage can inflate ROE)",
                         {"net_income": net_income, "equity": equity}))
    if net_income is not None and total_assets is not None and _div(net_income, total_assets) is not None:
        rows.append(_row("ROA %", net_income / total_assets * 100, "net income / total assets", "INFO",
                         "profit per baht of assets", {"net_income": net_income, "total_assets": total_assets}))

    # --- cash vs profit (the card's biggest trap)
    if net_income is not None and cfo is not None:
        if net_income > 0 and cfo < 0:
            flag = "RED"
            reading = ("profit is positive but operating cash flow is negative: check receivables and "
                       "inventory build-up before trusting the profit")
        elif (net_income_prev is not None and cfo_prev is not None and net_income > net_income_prev
              and cfo < cfo_prev):
            flag = "AMBER"
            reading = "profit grew but operating cash flow fell versus the prior period"
        else:
            flag, reading = "OK", "operating cash flow does not contradict the profit"
        cover = _div(cfo, net_income) if net_income > 0 else None
        rows.append(_row("CFO vs net income", cover, "operating cash flow / net income", flag, reading,
                         {"net_income": net_income, "cfo": cfo}))
    else:
        rows.append(_skip("CFO vs net income", ["--net-income", "--cfo"]))
    return rows


def build_parser():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    for name in ("current-assets", "current-liabilities", "inventory", "total-debt", "equity", "ebit",
                 "interest", "revenue", "cogs", "gross-profit", "net-income", "total-assets", "cfo",
                 "net-income-prev", "revenue-prev", "cfo-prev"):
        ap.add_argument("--" + name, type=float, default=None)
    ap.add_argument("--de-benchmark", type=float, default=None,
                    help="industry D/E you want to compare with (never hard-coded here)")
    return ap


def main(argv=None):
    a = vars(build_parser().parse_args(argv))
    as_json = a.pop("json")
    rows = read_ratios(**{k.replace("-", "_"): v for k, v in a.items()})
    if as_json:
        print(json.dumps({"rows": rows, "advisory": ADVISORY}, ensure_ascii=False, indent=1))
        return 0
    print("%-20s %-12s %-12s %s" % ("ratio", "value", "flag", "reading"))
    for r in rows:
        val = "-" if r["value"] is None else "%.4f" % r["value"]
        print("%-20s %-12s %-12s %s" % (r["ratio"], val, r["flag"], r["reading"]))
        if r["formula"]:
            print("%-20s   formula: %s  inputs: %s" % ("", r["formula"], json.dumps(r["inputs"], ensure_ascii=False)))
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
