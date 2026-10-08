#!/usr/bin/env python3
"""bluf_check - pre-send checker for a message that goes UP (head of lab / director / admin / committee).

Black-box tool for report-up-judgment. Run --help first; read the source only if a check surprises you.
It checks the *form* of the message against rules the card states in words. It cannot tell whether the
facts or numbers are true (the card: "verify, no guessing, no mental math") - it lists every number so
you can verify them yourself.

Rules checked (all from the report-up-judgment card):
  rule #1 / trap "buried bottom line"  the FIRST line carries the ask: exactly one of
         เพื่อทราบ (FYI) / ขออนุมัติ (approval) / ขอตัดสินใจ-สั่งการ (decision)        [FAIL]
         - no ask anywhere = "ends in the air" [FAIL]; ask only at the end = "buried" [FAIL]
         - channel email: subject = TL;DR and the email may close on the decision point, so the ask in
           the closing line is accepted (card § channel shapes)
  approval  "ขออนุมัติ" must carry options/figures (a number) and a deadline                   [FAIL]
  placeholder  "[ ]" blanks and "___" left in the text ("ห้ามปล่อยลอยหรือเดา") [FAIL]; lone X/Y/Z/N [WARN]
  jargon    by audience - cut Westgard rule codes, Levey-Jennings, raw CV/SD, error codes,
            troubleshoot (committee/director/admin); throughput, rerun, recalibrate (director/admin) [FAIL];
            concept-level lab terms TAT/QC/carryover... (director/admin) [WARN].
            labhead reads concept-level terms - nothing is stripped (card: "อย่า over-strip")
  patronising  "เครื่องงอน", "เครื่องมีปัญหานิดหน่อย" = over-strip / minimising a QC fail           [FAIL]
  --safety  patient-safety / NC reports must not be made lighter: เล็กน้อย / นิดหน่อย /
            ข้อสังเกตเล็กน้อย [FAIL]; no affected count and no "not affected" statement [WARN]
  commanding  "ท่านควร...", "ต้องรีบอนุมัติ" [WARN] ·  hedging น่าจะ/อาจจะ/ดูเหมือนว่า [WARN]
  numbers   every number found is printed for you to verify [INFO]

Usage
  python bluf_check.py draft.txt --audience director
  python bluf_check.py draft.txt --audience committee --channel email --safety
  cat draft.txt | python bluf_check.py - --audience admin --json
Exit code 0 = no FAIL (WARN allowed), 1 = at least one FAIL.
"""
import argparse
import json
import re
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874; keep UTF-8 so Thai text and symbols print.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ADVISORY = ("ADVISORY: ตัวตรวจเช็คโครง/ถ้อยคำเท่านั้น - ข้อเท็จจริงและตัวเลขต้อง verify เอง · "
            "เรื่องกระทบคนไข้/NC ยืนยันกับ SOP และผู้มีอำนาจของแล็บก่อนส่ง")

# ---- the three asks the card allows ("เพื่อทราบ / ขออนุมัติ / ขอตัดสินใจ-สั่งการ") ----
ASK_PATTERNS = {
    "INFO": re.compile(r"เพื่อทราบ|for\s+your\s+information|\bFYI\b|for\s+info\b", re.I),
    "APPROVE": re.compile(r"ขออนุมัติ|ขอความอนุมัติ|request(?:ing)?\s+approval|for\s+approval", re.I),
    "DECIDE": re.compile(r"ขอตัดสินใจ|ขอให้ตัดสินใจ|ขอสั่งการ|decision\s+(?:needed|requested)", re.I),
}

GREETING_RE = re.compile(r"^(เรียน|สวัสดี|dear\b|hi\b|hello\b)", re.I)
SUBJECT_RE = re.compile(r"^(subject|หัวเรื่อง|เรื่อง)\s*[:：]", re.I)

HAS_NUMBER_RE = re.compile(r"[0-9๐-๙]")
# a real deadline: a date/day word after ภายใน/ก่อน, a relative day/week count, the budget round, or the word itself.
# "ภายใน 6 เดือน" (payback period) is deliberately NOT a deadline.
DEADLINE_RE = re.compile(
    r"(?:ภายใน|ก่อน)\s*(?:วันที่|วัน(?:จันทร์|อังคาร|พุธ|พฤหัส\S*|ศุกร์|เสาร์|อาทิตย์)|วันนี้|พรุ่งนี้|สัปดาห์|สิ้น|รอบ|ประชุม|เที่ยง"
    r"|\d{1,2}\s*[/.]\s*\d{1,2}|\d{1,2}\s*(?:ม\.ค|ก\.พ|มี\.ค|เม\.ย|พ\.ค|มิ\.ย|ก\.ค|ส\.ค|ก\.ย|ต\.ค|พ\.ย|ธ\.ค))"
    r"|ภายใน\s*\d+\s*(?:วัน|สัปดาห์)|ทันรอบ|เส้นตาย|deadline|\bby\s+(?:mon|tue|wed|thu|fri|sat|sun|\d)",
    re.I)

# "[ ]" with no digit inside = a blank to fill ([รุ่น], [test], [N], [฿]); "[NC-123]" (has digits) is a real id.
# A markdown link [text](url) is not a blank.
PLACEHOLDER_RE = re.compile(r"\[[^\]\d\n]*\](?!\()|(?<!\w)_{3,}")
LONE_LETTER_RE = re.compile(r"(?<![A-Za-z0-9_])[XYZN](?![A-Za-z0-9_])")

# ---- jargon by audience (card: "สิ่งที่ตัดทิ้งได้" per audience + the "ตัดทิ้ง" list) ----
JARGON_CORE = [
    ("Westgard", re.compile(r"westgard", re.I)),
    ("Levey-Jennings", re.compile(r"levey[-\s]?jennings", re.I)),
    ("Westgard rule code", re.compile(r"(?<![A-Za-z0-9])(?:[1-4][-–][23]s|R[-–]?4s)(?![A-Za-z0-9])", re.I)),
    ("raw CV", re.compile(r"(?<![A-Za-z])%?CV(?![A-Za-z])")),
    ("raw SD", re.compile(r"(?<![A-Za-z])SD(?![A-Za-z])")),
    ("error code", re.compile(r"error\s*code|รหัส\s*error|จอ\s*error", re.I)),
    ("troubleshoot", re.compile(r"trouble-?shoot", re.I)),
]
JARGON_EXEC = [
    ("throughput", re.compile(r"throughput", re.I)),
    ("rerun", re.compile(r"(?<![A-Za-z])re-?run", re.I)),
    ("recalibrate", re.compile(r"recalibrat", re.I)),
]
JARGON_CONCEPT = [  # concept-level terms a head of lab reads fluently but a director/admin does not need
    ("TAT", re.compile(r"(?<![A-Za-z])TAT(?![A-Za-z])")),
    ("QC", re.compile(r"(?<![A-Za-z])QC(?![A-Za-z])")),
    ("carryover", re.compile(r"carry-?over", re.I)),
    ("reflex test", re.compile(r"reflex", re.I)),
]
AUDIENCES = ("labhead", "committee", "director", "admin")

# ---- patronising / minimising wording ----
PATRONISING = [
    ("เครื่องงอน (replaces 'QC fail' - patronises the reader)", re.compile(r"เครื่องงอน")),
    ("เครื่องมีปัญหานิดหน่อย (shrinks a QC fail)", re.compile(r"เครื่องมีปัญหานิดหน่อย")),
]
SAFETY_MINIMISERS = re.compile(r"ข้อสังเกตเล็กน้อย|เล็กน้อย|นิดหน่อย|ไม่น่ากังวล")
NOT_AFFECTED_RE = re.compile(r"ยังไม่กระทบ|ไม่กระทบ|ยังไม่พบ|ยังไม่ทราบจำนวน|ยังไม่ทราบ")

COMMANDING_RE = re.compile(r"(?:ท่าน|คุณ)\s*(?:ควร|ต้อง)|(?:ควร|ต้อง)รีบ\s*(?:อนุมัติ|ตัดสินใจ)")
HEDGE_RE = re.compile(r"น่าจะ|อาจจะ|ดูเหมือนว่า")
NUMBER_RE = re.compile(r"[0-9๐-๙][0-9๐-๙,\.:]*\s*(?:%|บาท|฿|ชม\.|ชั่วโมง|นาที|วัน|ราย|เดือน|คน|ตำแหน่ง|สัปดาห์)?")


def kinds_in(s):
    """Set of ask kinds (INFO / APPROVE / DECIDE) found in s."""
    return {k for k, rx in ASK_PATTERNS.items() if rx.search(s or "")}


def _nonempty(text):
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def find_bluf_line(text, channel="memo"):
    """The line that must carry the ask. Markdown titles and rules are skipped; for email the
    subject line (or the first line after the greeting) is the bottom line."""
    lines = [ln for ln in _nonempty(text) if not ln.startswith("#") and not re.fullmatch(r"[-=_*]{3,}", ln)]
    if not lines:
        return ""
    if channel == "email":
        for ln in lines:
            if SUBJECT_RE.match(ln):
                return ln
        for ln in lines:
            if not GREETING_RE.match(ln):
                return ln
    return lines[0]


def closing_line(text):
    lines = [ln for ln in _nonempty(text) if not re.fullmatch(r"[-=_*]{3,}", ln)]
    return lines[-1] if lines else ""


def check(text, audience=None, channel="memo", safety=False):
    out = []

    def add(cid, status, msg):
        out.append({"id": cid, "status": status, "msg": msg})

    text = text or ""
    if not text.strip():
        add("ASK", "FAIL", "ข้อความว่าง")
        return _finish(out, "", None, text)

    bluf = find_bluf_line(text, channel)
    all_kinds = kinds_in(text)
    first_kinds = kinds_in(bluf)
    eff = set(first_kinds)

    # ---- rule #1: the ask is in the first line ----
    if not all_kinds:
        add("ASK", "FAIL", "จบลอย: ไม่มีคำขอ - ต้องระบุ 1 อย่าง: เพื่อทราบ / ขออนุมัติ / ขอตัดสินใจ-สั่งการ")
    elif len(first_kinds) > 1:
        add("ASK", "FAIL", "บรรทัดแรกมีคำขอมากกว่า 1 ชนิด (%s) - ระบุได้ 1 อย่างเท่านั้น" % "+".join(sorted(first_kinds)))
    elif first_kinds:
        add("ASK", "PASS", "บรรทัดแรกขอ: %s" % next(iter(first_kinds)))
    else:
        tail = kinds_in(closing_line(text))
        if channel == "email" and len(tail) == 1:
            eff = set(tail)
            add("ASK", "PASS", "email: คำขอ (%s) อยู่ที่บรรทัดปิดท้าย - การ์ดอนุญาตให้ปิดอีเมลด้วยจุดตัดสินใจ" % next(iter(tail)))
        else:
            eff = set(all_kinds)
            where = "บรรทัดแรกเป็นคำทักทาย ไม่ใช่ bottom line" if GREETING_RE.match(bluf) else \
                "ฝัง bottom line ไว้ท้าย: บรรทัดแรกไม่มีคำขอ (พบ %s ที่อื่นในข้อความ)" % "+".join(sorted(all_kinds))
            add("ASK", "FAIL", where)
    if len(all_kinds) > 1 and len(first_kinds) == 1:
        add("ASK-MULTI", "WARN", "ทั้งข้อความมีคำขอหลายชนิด (%s) - การ์ด: ระบุ 1 อย่าง" % "+".join(sorted(all_kinds)))

    # ---- approval needs figures + a deadline ----
    if "APPROVE" in eff:
        if not HAS_NUMBER_RE.search(text):
            add("APPROVAL-NUMBER", "FAIL", "ขออนุมัติต้องมีตัวเลข (งบ/ผลกระทบ/คืนทุน) - ไม่พบตัวเลขเลย")
        else:
            add("APPROVAL-NUMBER", "PASS", "มีตัวเลขประกอบคำขออนุมัติ")
        if not DEADLINE_RE.search(text):
            add("APPROVAL-DEADLINE", "FAIL", "ขออนุมัติต้องมีเส้นตาย (เช่น 'ภายในวันที่ ...', 'ทันรอบงบ') - 'ภายใน N เดือน' ที่เป็นระยะคืนทุนไม่นับ")
        else:
            add("APPROVAL-DEADLINE", "PASS", "มีเส้นตาย")

    # ---- unfilled placeholders ----
    ph = [m.group(0) for m in PLACEHOLDER_RE.finditer(text)]
    if ph:
        add("PLACEHOLDER", "FAIL", "ยังมีช่องเว้นว่างที่ไม่ได้เติม: %s (การ์ด: ตัวเลขใน [ ] ต้องเติมของจริง ห้ามปล่อยลอย)" % ", ".join(dict.fromkeys(ph)))
    else:
        add("PLACEHOLDER", "PASS", "ไม่มีช่องเว้นว่าง")
    lone = [m.group(0) for m in LONE_LETTER_RE.finditer(text)]
    if lone:
        add("PLACEHOLDER-LETTER", "WARN", "มีตัวอักษรเดี่ยว %s - เป็น placeholder ที่ลืมเติมหรือเปล่า" % ", ".join(dict.fromkeys(lone)))

    # ---- jargon by audience ----
    if audience is None:
        add("JARGON", "INFO", "ไม่ได้ระบุ --audience: ข้ามการเช็คศัพท์เทคนิค")
    elif audience == "labhead":
        add("JARGON", "PASS", "labhead: อ่านศัพท์ระดับแนวคิดออก - ไม่ตัดศัพท์ (อย่า over-strip)")
    else:
        fail_terms = list(JARGON_CORE)
        if audience in ("director", "admin"):
            fail_terms += JARGON_EXEC
        hits = [name for name, rx in fail_terms if rx.search(text)]
        if hits:
            add("JARGON", "FAIL", "%s: ตัดศัพท์/รายละเอียดเทคนิคต่อไปนี้ แล้วแปลเป็นผลกระทบ: %s" % (audience, ", ".join(hits)))
        else:
            add("JARGON", "PASS", "%s: ไม่พบศัพท์เทคนิคที่ต้องตัด" % audience)
        if audience in ("director", "admin"):
            soft = [name for name, rx in JARGON_CONCEPT if rx.search(text)]
            if soft:
                add("JARGON-CONCEPT", "WARN", "%s: ศัพท์แล็บระดับแนวคิด %s - แปลเป็นผลที่คนไข้/เงิน/เวลาได้ไหม" % (audience, ", ".join(soft)))

    # ---- patronising / minimising ----
    pat = [name for name, rx in PATRONISING if rx.search(text)]
    if pat:
        add("PATRONISING", "FAIL", "ลดทอน/ดูถูกผู้รับ: " + "; ".join(pat))
    else:
        add("PATRONISING", "PASS", "ไม่มีคำที่ลด QC fail หรือดูถูกผู้รับ")

    # ---- patient-safety / NC report ----
    if safety:
        mins = list(dict.fromkeys(m.group(0) for m in SAFETY_MINIMISERS.finditer(text)))
        if mins:
            add("SAFETY-MINIMISE", "FAIL", "เรื่องกระทบคนไข้/NC ห้ามทำให้ดูเบาลง: พบ %s" % ", ".join(mins))
        else:
            add("SAFETY-MINIMISE", "PASS", "ไม่พบคำที่ทำให้เรื่องความปลอดภัยดูเบาลง")
        if not (HAS_NUMBER_RE.search(text) or NOT_AFFECTED_RE.search(text)):
            add("SAFETY-IMPACT", "WARN", "ไม่ระบุจำนวนผู้ได้รับผลกระทบ และไม่บอกว่ายังไม่กระทบ/ยังไม่ทราบ (กระทบใคร/กี่ราย)")

    # ---- tone ----
    cmd = list(dict.fromkeys(m.group(0) for m in COMMANDING_RE.finditer(text)))
    if cmd:
        add("COMMANDING", "WARN", "เสียงสั่งผู้บริหาร: %s - เสนอเป็นทางเลือก ให้เขาตัดสินใจ" % ", ".join(cmd))
    hed = list(dict.fromkeys(m.group(0) for m in HEDGE_RE.finditer(text)))
    if hed:
        add("HEDGING", "WARN", "hedge: %s - ถ้ารู้ให้บอก ถ้าไม่รู้ให้บอกว่าอะไรที่ยังไม่รู้" % ", ".join(hed))

    # ---- numbers to verify ----
    nums = list(dict.fromkeys(re.sub(r"\s+", " ", m.group(0)).strip().rstrip(".,:") for m in NUMBER_RE.finditer(text)))
    if nums:
        add("NUMBERS", "INFO", "ตัวเลขที่ต้อง verify กับแหล่งก่อนส่ง: " + " | ".join(nums[:15]))

    return _finish(out, bluf, eff, text)


def _finish(checks, bluf, eff, text):
    fails = sum(1 for c in checks if c["status"] == "FAIL")
    warns = sum(1 for c in checks if c["status"] == "WARN")
    return {"bluf_line": bluf, "ask": sorted(eff) if eff else [], "checks": checks,
            "fail": fails, "warn": warns, "result": "FAIL" if fails else "PASS"}


def render(res, audience, channel, safety):
    lines = ["bluf_check - audience=%s channel=%s safety=%s" % (audience or "-", channel, "yes" if safety else "no"),
             "BLUF line : " + (res["bluf_line"][:110] or "(none)"),
             "ask       : " + (",".join(res["ask"]) or "(none)"), "",
             "%-20s %-5s %s" % ("check", "state", "detail"), "-" * 78]
    for c in res["checks"]:
        lines.append("%-20s %-5s %s" % (c["id"], c["status"], c["msg"]))
    lines += ["-" * 78, "RESULT: %s (%d fail, %d warn)" % (res["result"], res["fail"], res["warn"]), ADVISORY]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="draft text file (UTF-8), or - for stdin")
    ap.add_argument("--audience", choices=AUDIENCES, help="who reads it; omit to skip the jargon check")
    ap.add_argument("--channel", choices=("memo", "email", "line", "meeting"), default="memo")
    ap.add_argument("--safety", action="store_true", help="the message reports a patient-safety issue / NC")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args(argv)
    if a.file == "-":
        text = sys.stdin.read()
    else:
        with open(a.file, encoding="utf-8-sig") as f:
            text = f.read()
    res = check(text, audience=a.audience, channel=a.channel, safety=a.safety)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        print(render(res, a.audience, a.channel, a.safety))
    return 1 if res["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
