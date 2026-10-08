#!/usr/bin/env python3
"""roi - is building an automation worth it? Time saved x frequency vs build + upkeep, with break-even.

Black-box tool for offload-to-automation. Run --help first; read the source only if a check fails.
It encodes the card's table rows:
  * "ซ้ำ + กฎนิ่ง + ทำบ่อย + ใช้ไปอีกนาน -> automation (คุ้ม ROI)"
  * "ทำครั้งเดียว / กฎเปลี่ยนตลอด / ปริมาณน้อย -> ทำมือ (เวลาที่เสียเขียน+ดูแล > เวลาที่ประหยัด)"
and the ⛔ box: "พลาดแล้วมีผล = ใช้ tool" - accuracy is a separate reason from time.

Formula (all in hours)
  saved/month   = (manual_min - auto_min) x runs_per_month / 60      auto_min = time still spent per run
                                                                     (launch + CHECK the output, card step 4)
  upkeep/month  = maintain_hours_per_month + rule_changes_per_year x rework_hours / 12
  net/month     = saved/month - upkeep/month
  break-even    = build_hours / net/month   (months; never if net <= 0)
  net@horizon   = net/month x horizon_months - build_hours

Verdict
  AUTOMATE      break-even <= horizon
  MANUAL        never breaks even, or break-even > horizon
  SCRIPT-ONCE   MANUAL on time, but --error-costly: still compute with code/formula, just don't build a system

Examples
  python roi.py --manual-min 20 --auto-min 2 --runs-per-month 8 --build-hours 4 --maintain-hours-per-month 0.5
  python roi.py --manual-min 30 --runs-total 1 --build-hours 2 --error-costly
  python roi.py --manual-min 10 --auto-min 1 --runs-per-month 4 --build-hours 3 --rule-changes-per-year 12 --rework-hours 1 --json
"""
import argparse
import json
import math
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def monthly_saving_hours(manual_min, auto_min, runs_per_month):
    """Hours saved per month: per-run saving TIMES how often it runs."""
    return (manual_min - auto_min) * runs_per_month / 60.0


def monthly_upkeep_hours(maintain_hours_per_month, rule_changes_per_year, rework_hours):
    """Hours spent keeping the automation correct: routine upkeep + rework every time the rules change."""
    return maintain_hours_per_month + rule_changes_per_year * rework_hours / 12.0


def roi(manual_min, auto_min, runs_per_month, build_hours, maintain_hours_per_month=0.0,
        rule_changes_per_year=0.0, rework_hours=0.0, horizon_months=12.0, error_costly=False):
    saved = monthly_saving_hours(manual_min, auto_min, runs_per_month)
    upkeep = monthly_upkeep_hours(maintain_hours_per_month, rule_changes_per_year, rework_hours)
    net = saved - upkeep
    breakeven = build_hours / net if net > 0 else math.inf
    at_horizon = net * horizon_months - build_hours
    if breakeven <= horizon_months:
        verdict = "AUTOMATE"
    elif error_costly:
        verdict = "SCRIPT-ONCE"
    else:
        verdict = "MANUAL"
    notes = []
    if auto_min <= 0:
        notes.append("WARN auto_min = 0: checking the output is never free (card step 4 Verify) - put the real check time in")
    if net <= 0:
        notes.append("never breaks even: upkeep >= saving (card: one-off / rules keep changing / low volume -> do it by hand)")
    elif breakeven > horizon_months:
        notes.append("breaks even after %.1f months but you only expect to use it %.1f months" % (breakeven, horizon_months))
    if verdict == "SCRIPT-ONCE":
        notes.append("accuracy, not time: a mistake costs something (card ⛔ box) -> compute this once with code/a formula, "
                     "but do not build/maintain a reusable system")
    return {
        "inputs": {"manual_min": manual_min, "auto_min": auto_min, "runs_per_month": runs_per_month,
                   "build_hours": build_hours, "maintain_hours_per_month": maintain_hours_per_month,
                   "rule_changes_per_year": rule_changes_per_year, "rework_hours": rework_hours,
                   "horizon_months": horizon_months, "error_costly": error_costly},
        "saved_hours_per_month": saved,
        "upkeep_hours_per_month": upkeep,
        "net_hours_per_month": net,
        "breakeven_months": breakeven,
        "net_hours_at_horizon": at_horizon,
        "verdict": verdict,
        "notes": notes,
    }


def fmt(x):
    return "never" if x == math.inf else ("%.2f" % x)


def render(r):
    i = r["inputs"]
    out = [
        "input | value",
        "------|------",
        "manual min/run | %g" % i["manual_min"],
        "automated min/run (launch + check) | %g" % i["auto_min"],
        "runs/month | %g" % i["runs_per_month"],
        "build hours | %g" % i["build_hours"],
        "upkeep h/month | %g  (+ %g rule changes/yr x %g h rework)" % (i["maintain_hours_per_month"],
                                                                     i["rule_changes_per_year"], i["rework_hours"]),
        "horizon months | %g" % i["horizon_months"],
        "",
        "step | formula | result",
        "-----|---------|-------",
        "saved/month | (%g - %g) x %g / 60 | %s h" % (i["manual_min"], i["auto_min"], i["runs_per_month"],
                                                     fmt(r["saved_hours_per_month"])),
        "upkeep/month | %g + %g x %g / 12 | %s h" % (i["maintain_hours_per_month"], i["rule_changes_per_year"],
                                                    i["rework_hours"], fmt(r["upkeep_hours_per_month"])),
        "net/month | saved - upkeep | %s h" % fmt(r["net_hours_per_month"]),
        "break-even | build / net | %s months" % fmt(r["breakeven_months"]),
        "net at horizon | net x %g - %g | %s h" % (i["horizon_months"], i["build_hours"], fmt(r["net_hours_at_horizon"])),
        "",
        "VERDICT: %s" % r["verdict"],
    ]
    out += ["NOTE: " + n for n in r["notes"]]
    out.append("ADVISORY: ตัวเลขนี้ตอบแค่ 'คุ้มเวลาไหม' - ส่วนที่ต้องใช้ดุลพินิจคน (ความเป็นธรรม/บริบทคน, การ์ดขั้น 6) "
               "ไม่อยู่ในสูตร และ automation ที่สร้างแล้วยังต้องตรวจ output ทุกครั้ง")
    return "\n".join(out)


def json_safe(o):
    """JSON has no Infinity/NaN: an unbounded value (e.g. a ratio with a zero denominator) is written as null."""
    if isinstance(o, float) and not math.isfinite(o):
        return None
    if isinstance(o, dict):
        return {k: json_safe(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [json_safe(v) for v in o]
    return o


def main(argv=None):
    ap = argparse.ArgumentParser(description="Automation ROI: time saved x frequency vs build + upkeep, with break-even.")
    ap.add_argument("--manual-min", type=float, required=True, help="minutes per run done by hand")
    ap.add_argument("--auto-min", type=float, default=0.0,
                    help="minutes per run that remain with automation (launch + check output). default 0 = warned")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--runs-per-month", type=float, help="how often the task runs per month")
    g.add_argument("--runs-total", type=float, help="total runs expected over the horizon (e.g. 1 = one-off)")
    ap.add_argument("--build-hours", type=float, required=True, help="hours to write + test the automation")
    ap.add_argument("--maintain-hours-per-month", type=float, default=0.0, help="routine upkeep hours per month")
    ap.add_argument("--rule-changes-per-year", type=float, default=0.0, help="how often the rules/inputs change")
    ap.add_argument("--rework-hours", type=float, default=0.0, help="hours to adapt the automation per rule change")
    ap.add_argument("--horizon-months", type=float, default=12.0, help="how long you expect to keep using it")
    ap.add_argument("--error-costly", action="store_true", help="a wrong number has consequences (money, patients, grades)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args(argv)
    if a.horizon_months <= 0:
        ap.error("--horizon-months must be > 0")
    runs = a.runs_per_month if a.runs_per_month is not None else a.runs_total / a.horizon_months
    r = roi(a.manual_min, a.auto_min, runs, a.build_hours, a.maintain_hours_per_month,
            a.rule_changes_per_year, a.rework_hours, a.horizon_months, a.error_costly)
    if a.json:
        print(json.dumps(json_safe(r), ensure_ascii=False, indent=1, default=lambda x: None, allow_nan=False))
    else:
        print(render(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
