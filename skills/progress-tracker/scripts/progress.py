#!/usr/bin/env python3
"""progress - build the progress panel from a CSV and enforce the card's honesty rules.

Black-box tool for progress-tracker. Run --help first; read the source only if a check fails.
CSV columns (header required; due/finished optional):
  step,status,evidence,reason,due,finished
  status    : done | doing | todo | skip   (or ✅ ▶️ ⬜ ⏭️)
  evidence  : what you SAW that proves it is done (test output, file path, screenshot, read-back)
  reason    : why a step is skipped (required for skip)
  due       : YYYY-MM-DD planned date (optional)       finished : YYYY-MM-DD actual date (optional)

Rules from the card (skills/progress-tracker.md)
  * ✅ only for steps done AND seen. done with no evidence, or evidence that only says it was started /
    sent / ordered ("สั่งแล้ว", "started", "รอผล") -> shown as ▶️ and FLAG DONE_WITHOUT_EVIDENCE
  * ⏭️ needs a reason -> otherwise FLAG SKIP_WITHOUT_REASON
  * "ตอนนี้อยู่ขั้น X / Y": Y = steps that are not skipped; X = verified-done steps + 1 if one is in progress
  * % done = verified-done / Y
  * 5-7 steps is the sweet spot -> WARN above 7
  * slip (when dates given): finished - due for done steps; today - due for open steps past due

Examples
  python progress.py steps.csv
  python progress.py steps.csv --today 2026-10-08 --json
"""
import argparse
import csv
import datetime as dt
import io
import json
import re
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

STATUS = {"done": "done", "✅": "done", "doing": "doing", "▶️": "doing", "▶": "doing",
          "todo": "todo", "⬜": "todo", "skip": "skip", "⏭️": "skip", "⏭": "skip"}
ICON = {"done": "✅", "doing": "▶️", "todo": "⬜", "skip": "⏭️"}
# evidence that only says the step was started / requested is NOT a seen result (card: กับดักเนียน)
NOT_EVIDENCE = re.compile(r"^\s*(?:started|sent|ordered|requested|queued|pending|running|in progress|todo|tbd|"
                          r"สั่งแล้ว|สั่ง(?:ให้)?ทำแล้ว|เริ่ม(?:ทำ)?แล้ว|ส่งแล้ว|รอผล|รอ|กำลัง\S*|ยังไม่เห็นผล)\s*$", re.I)
MAX_STEPS = 7


def parse_date(s):
    s = (s or "").strip()
    return dt.date.fromisoformat(s) if s else None


def is_verified_done(row):
    """done AND has evidence that shows a result (not just 'started')."""
    ev = (row.get("evidence") or "").strip()
    return row["status"] == "done" and bool(ev) and not NOT_EVIDENCE.match(ev)


def load(path):
    # stdin as UTF-8: a Thai Windows console would otherwise decode piped bytes as cp874 (✅ crashes it)
    f = (io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8-sig", newline="") if path == "-"
         else open(path, encoding="utf-8-sig", newline=""))
    try:
        rows = []
        for i, r in enumerate(csv.DictReader(f), 1):
            r = {k.strip().lower(): (v or "").strip() for k, v in r.items() if k}
            raw = r.get("status", "")
            st = STATUS.get(raw.lower(), STATUS.get(raw))
            if not st:
                raise SystemExit("row %d: unknown status %r (use done/doing/todo/skip)" % (i, raw))
            r["status"] = st
            r["row"] = i
            rows.append(r)
        return rows
    finally:
        if path != "-":
            f.close()


def evaluate(rows, today=None):
    today = today or dt.date.today()
    findings, panel = [], []
    for r in rows:
        shown = r["status"]
        if r["status"] == "done" and not is_verified_done(r):
            shown = "doing"
            findings.append({"row": r["row"], "level": "FLAG", "kind": "DONE_WITHOUT_EVIDENCE",
                             "detail": "%s - marked done but no seen result (evidence=%r) -> shown as ▶️ until you see the output"
                                       % (r["step"], r.get("evidence", ""))})
        if r["status"] == "skip" and not r.get("reason"):
            findings.append({"row": r["row"], "level": "FLAG", "kind": "SKIP_WITHOUT_REASON",
                             "detail": "%s - skipped with no reason (card: ⏭️ = not relevant + say why)" % r["step"]})
        due, fin = parse_date(r.get("due")), parse_date(r.get("finished"))
        slip = None
        if due and shown == "done" and fin:
            slip = (fin - due).days
        elif due and shown in ("doing", "todo") and today > due:
            slip = (today - due).days
        if slip and slip > 0:
            findings.append({"row": r["row"], "level": "WARN", "kind": "SLIP",
                             "detail": "%s - %d day(s) %s" % (r["step"], slip, "late" if shown == "done" else "overdue")})
        panel.append({"step": r["step"], "shown": shown, "evidence": r.get("evidence", ""),
                      "reason": r.get("reason", ""), "slip_days": slip})
    active = [p for p in panel if p["shown"] != "skip"]
    done = sum(1 for p in active if p["shown"] == "done")
    doing = any(p["shown"] == "doing" for p in active)
    total = len(active)
    position = min(done + (1 if doing else 0), total)
    if len(rows) > MAX_STEPS:
        findings.append({"row": 0, "level": "WARN", "kind": "TOO_MANY_STEPS",
                         "detail": "%d steps - card: 5-7 is enough to see the picture; group the small ones" % len(rows)})
    slips = [p["slip_days"] for p in panel if p["slip_days"]]
    summary = {"position": position, "total": total, "done": done,
               "percent_done": round(100.0 * done / total, 1) if total else 0.0,
               "max_slip_days": max(slips) if slips else 0,
               "flag": sum(1 for x in findings if x["level"] == "FLAG")}
    return {"panel": panel, "findings": findings, "summary": summary}


def render(res):
    s = res["summary"]
    out = ["📊 ความคืบหน้า (%d/%d) · %.0f%% done" % (s["position"], s["total"], s["percent_done"])]
    for p in res["panel"]:
        line = "%s %s" % (ICON[p["shown"]], p["step"])
        if p["shown"] == "done" and p["evidence"]:
            line += " - " + p["evidence"]
        if p["shown"] == "skip":
            line += " (เหตุผล: %s)" % (p["reason"] or "ไม่ได้ระบุ!")
        if p["slip_days"] and p["slip_days"] > 0:
            line += "  [+%dd]" % p["slip_days"]
        out.append(line)
    out.append("")
    if res["findings"]:
        out.append("row | level | kind | detail")
        out.append("----|-------|------|-------")
        for f in res["findings"]:
            out.append("%3s | %-4s | %s | %s" % (f["row"] or "-", f["level"], f["kind"], f["detail"]))
    else:
        out.append("(no findings)")
    out.append("")
    out.append("FLAG = the panel would show progress you have not seen; fix before showing it")
    out.append("ADVISORY: แผงนี้บอก 'ทำอะไรไปแล้วจริง' ไม่ได้บอกว่าเนื้องานถูก - ตรวจผลงานจริงเสมอ")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Progress panel (X/Y, %% done, slip) with the card's honesty rules.")
    ap.add_argument("path", help="CSV file (step,status,evidence,reason[,due,finished]) or - for stdin")
    ap.add_argument("--today", help="YYYY-MM-DD used for overdue (default: today)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--strict", action="store_true", help="exit 1 when any FLAG is present")
    a = ap.parse_args(argv)
    res = evaluate(load(a.path), parse_date(a.today))
    print(json.dumps(res, ensure_ascii=False, indent=1) if a.json else render(res))
    return 1 if (a.strict and res["summary"]["flag"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
