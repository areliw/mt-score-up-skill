#!/usr/bin/env python3
"""reply_lint - check an AI reply against the calibration card's mechanical rules.

Black-box tool for ai-assistant-calibration. Run --help first; read the source only if a check fails.
Use it to test whether a calibration prompt actually changed the AI's habits (paste the reply, lint it),
or to self-check a draft before sending. It checks HABITS, not whether the content is true.

Rules checked (skills/ai-assistant-calibration.md)
  PREAMBLE      first line is a greeting / praise / "let me" instead of the answer   (ฟันธงก่อน)        FLAG
  HEDGE         น่าจะ / มั้ง / คงจะ / probably / I think ... with no uncertainty label  (ตรวจก่อนพูด)      FLAG
                label = [~mem] [~est] [?confirm] [ไม่แน่ใจ] or "ไม่แน่ใจ / ยังไม่ได้เช็ก / not sure" in the line
  SCAFFOLDING   internal rule numbers / thinking steps shown to the user          (ซ่อนเบื้องหลัง)     FLAG
  TOO_LONG      more than --max-lines non-empty lines (default 5)                (สั้น 2-5 บรรทัด)    WARN
  OPTIONS_DUMP  3+ "Option / ตัวเลือก / ทางเลือก" items nobody asked for        (อย่าโปรย options)   WARN
  APOLOGY       2+ apologies                                                    (อย่าขอโทษพร่ำเพรื่อ) WARN
  RECAP         a closing "สรุป / In summary" that repeats the answer            (ไม่ต้องสรุปซ้ำ)     WARN
Not checked (cannot be checked mechanically): grade-3 sentence length in Thai, whether the verdict is right.

Examples
  python reply_lint.py reply.txt
  python reply_lint.py reply.txt --long-ok              # user asked for a long / grade-3 explanation
  cat reply.txt | python reply_lint.py - --strict --json
"""
import argparse
import json
import re
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

PREAMBLE = re.compile(
    r"^\W*(?:คำถามที่ดี|เป็นคำถามที่ดี|ขอบคุณ(?:ที่|สำหรับ)|ยินดี(?:ที่|ช่วย)|แน่นอน(?:ครับ|ค่ะ|คะ)?\s*[!！]|"
    r"ได้เลย(?:ครับ|ค่ะ)?\s*[!！]|สวัสดี|ก่อนอื่น|ในคำตอบนี้|ผมจะ(?:อธิบาย|ช่วย)|ดิฉันจะ|เราจะมาดู|"
    r"great question|good question|sure[!,. ]|certainly|absolutely[!,. ]|of course|i'd be happy|"
    r"i would be happy|thanks for|thank you for|let me |let's dive|as an ai)", re.I)
HEDGE = re.compile(r"น่าจะ|มั้ง|คงจะ|อาจจะใช่|\bprobably\b|\bi think\b|\bi believe\b|\bmaybe\b|\bperhaps\b|"
                   r"\bmight be\b|\bi guess\b", re.I)
UNSURE_LABEL = re.compile(r"\[\s*(?:~mem|~est|\?confirm|mem|est|unverified|ไม่แน่ใจ|ต้องเช็ค|ยืนยันไม่ได้)[^\]]*\]|"
                          r"ไม่แน่ใจ|ยังไม่ได้เช็[กค]|ยังไม่ได้ตรวจ|ยืนยันไม่ได้|not sure|haven't checked|unverified", re.I)
SCAFFOLD = re.compile(r"\brule\s*#?\s*\d|กฎ\s*(?:ข้อ\s*)?#?\s*\d|ตามกฎข้อ|ขั้นตอนคิด|chain of thought|"
                      r"my reasoning process|thinking process|scaffold", re.I)
OPTION_ITEM = re.compile(r"^\s*(?:[-*•]|\d+[.)])?\s*\**(?:option|ตัวเลือก|ทางเลือก)\s*(?:[A-Za-z0-9ก-ฮ]|ที่)", re.I)
APOLOGY = re.compile(r"ขอโทษ|ขออภัย|\bsorry\b|\bapologi[sz]e", re.I)
RECAP = re.compile(r"^\W*(?:สรุป(?:แล้ว|ก็คือ|สั้นๆ)?\s*[:：]|โดยสรุป|in summary|to summarize|to sum up|in conclusion)", re.I)


def lint(text, max_lines=5, long_ok=False, options_asked=False):
    lines = [(i, l.strip()) for i, l in enumerate(text.splitlines(), 1) if l.strip()]
    findings = []
    if lines and PREAMBLE.search(lines[0][1]):
        findings.append({"line": lines[0][0], "level": "FLAG", "kind": "PREAMBLE",
                         "detail": "opens with %r - put the answer / verdict on line 1" % lines[0][1][:40]})
    for no, l in lines:
        h = HEDGE.search(l)
        if h and not UNSURE_LABEL.search(l):
            findings.append({"line": no, "level": "FLAG", "kind": "HEDGE",
                             "detail": "%r without a check - verify first, or say 'ไม่แน่ใจ' / tag [~est]" % h.group(0)})
        if SCAFFOLD.search(l):
            findings.append({"line": no, "level": "FLAG", "kind": "SCAFFOLDING",
                             "detail": "internal rule/thinking shown to the user: %r" % l[:50]})
    if not long_ok and len(lines) > max_lines:
        findings.append({"line": 0, "level": "WARN", "kind": "TOO_LONG",
                         "detail": "%d lines > %d - default is 2-5 lines unless the user asked for more"
                                   % (len(lines), max_lines)})
    opts = [no for no, l in lines if OPTION_ITEM.search(l)]
    if len(opts) >= 3 and not options_asked:
        findings.append({"line": opts[0], "level": "WARN", "kind": "OPTIONS_DUMP",
                         "detail": "%d options listed - pick one and say why, unless the user asked to compare" % len(opts)})
    n_apology = sum(len(APOLOGY.findall(l)) for _, l in lines)
    if n_apology >= 2:
        findings.append({"line": 0, "level": "WARN", "kind": "APOLOGY",
                         "detail": "%d apologies - a correction is calibration, fix it and move on" % n_apology})
    recaps = [no for no, l in lines if RECAP.search(l)]
    if recaps and len(lines) > 1:
        findings.append({"line": recaps[-1], "level": "WARN", "kind": "RECAP",
                         "detail": "closing summary repeats the answer - the verdict is already on line 1"})
    summary = {"lines": len(lines),
               "flag": sum(1 for f in findings if f["level"] == "FLAG"),
               "warn": sum(1 for f in findings if f["level"] == "WARN")}
    summary["verdict"] = "FIX" if summary["flag"] else ("TIGHTEN" if summary["warn"] else "PASS")
    return {"findings": findings, "summary": summary}


def render(res):
    out = ["line | level | kind | detail", "-----|-------|------|-------"]
    for f in res["findings"]:
        out.append("%4s | %-5s | %s | %s" % (f["line"] or "-", f["level"], f["kind"], f["detail"]))
    if not res["findings"]:
        out.append("(no findings)")
    s = res["summary"]
    out += ["", "lines: %d | FLAG: %d | WARN: %d | VERDICT: %s" % (s["lines"], s["flag"], s["warn"], s["verdict"]),
            "ADVISORY: ตรวจแค่ 'นิสัยการตอบ' ตามการ์ด ไม่ได้ตรวจว่าเนื้อหาถูก - ความถูกต้องยังต้องเช็กกับแหล่งจริง"]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Lint an AI reply against the calibration card's habits.")
    ap.add_argument("path", help="text file with the reply, or - for stdin")
    ap.add_argument("--max-lines", type=int, default=5, help="default length budget in non-empty lines (card: 2-5)")
    ap.add_argument("--long-ok", action="store_true", help="the user asked for a long / grade-3 explanation")
    ap.add_argument("--options-asked", action="store_true", help="the user asked to compare options")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--strict", action="store_true", help="exit 1 when any FLAG is present")
    a = ap.parse_args(argv)
    if a.path == "-":
        # read bytes as UTF-8: a Thai Windows console would decode piped text as cp874 (mojibake / crash)
        text = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")
    else:
        with open(a.path, encoding="utf-8-sig") as f:
            text = f.read()
    res = lint(text, a.max_lines, a.long_ok, a.options_asked)
    print(json.dumps(res, ensure_ascii=False, indent=1) if a.json else render(res))
    return 1 if (a.strict and res["summary"]["flag"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
