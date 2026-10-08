"""Oracle tests for scripts/bluf_check.py (report-up-judgment).

There is no external dataset for "how to write upward"; every expected outcome comes from a sentence in the
report-up-judgment card itself, applied by hand to constructed messages (card section named in each comment):
  rule #1 + trap "ฝัง bottom line ไว้ท้ายสุด"   -> the ask must be in the first line
  § ขอการตัดสินใจให้ชัด                          -> exactly one of เพื่อทราบ / ขออนุมัติ / ขอตัดสินใจ;
                                                    ขออนุมัติ = ตัวเลือก + ตัวเลข + เส้นตาย
  § ตัวอย่างเต็ม                                  -> "ตัวเลขในวงเล็บ [ ] ต้องเติมของจริง ห้ามปล่อยลอย"
  § สิ่งที่เก็บไว้ / ตัดทิ้ง / แปล + ตารางผู้รับ  -> jargon by audience; "อย่า over-strip" for the head of lab
  § Escalate เรื่อง NC                             -> "อาจมีผล...N ราย" must not become "ข้อสังเกตเล็กน้อย"
  § ❌/✅ VERDICT examples                         -> the ✅ openers carry the ask; the ❌ ones do not
Note: the card's one-line VERDICT examples are only the *opening line*; they omit the deadline that
"ขออนุมัติ" requires, so the passing fixtures below are complete messages.

Must-fail controls inject the traps the card warns about into the tool; the matching oracle test must go red.
Run from the skill folder:  python -m pytest evals -q
"""
import json
import os
import re
import subprocess
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import bluf_check as bc  # noqa: E402

DATA = os.path.join(SKILL, "data")
TOOL = os.path.join(SKILL, "scripts", "bluf_check.py")


def status(text, cid, **kw):
    """Status of one check id, or None when that check did not run."""
    return next((c["status"] for c in bc.check(text, **kw)["checks"] if c["id"] == cid), None)


def result(text, **kw):
    return bc.check(text, **kw)["result"]


def read(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return f.read()


# --- the card's four ✅ openers with every [ ] filled by hand; each is only the first line -------------
GOOD_OPENERS = [
    ("APPROVE", "เครื่องปัจจุบันทำให้ผลออกช้าเฉลี่ย 3 ชม. คนไข้ตกค้าง 12 ราย/วัน — ขออนุมัติงบ 850,000 บาท "
                "คืนทุนใน 14 เดือนจากค่าล่วงเวลาและน้ำยาที่เสียซ้ำที่ลดได้"),
    ("INFO", "พบค่าควบคุมหลุดเกณฑ์รายการน้ำตาลเช้านี้ — กลั้นผลไว้ ยังไม่กระทบคนไข้ ทีมแก้แล้ว "
             "คาดปล่อยผลได้ภายใน 14:00 น. · รายงานเพื่อทราบ ไม่ต้องตัดสินใจ"),
    ("APPROVE", "ปรับลำดับงานช่วยให้ผลด่วนถึงมือแพทย์เร็วขึ้น 10 นาที ไม่ใช้งบเพิ่ม — ขออนุมัติทดลอง 2 สัปดาห์แล้ววัดผล"),
    ("APPROVE", "ปริมาณงานโตขึ้น 25% ใน 6 เดือน ทำให้ค่าล่วงเวลา 40,000 บาท/เดือน และเสี่ยงผลพลาดจากความล้า — "
                "ขออนุมัติอัตรา 2 ตำแหน่ง คุ้มกว่าค่า OT ใน 8 เดือน"),
    ("INFO", "เครื่องที่ 2 ใช้งานไม่ได้ตั้งแต่ 08:30 — รายการ CBC หยุดชั่วคราว, ส่งงานด่วนไปเครื่องสำรองแล้ว, "
             "ช่างมา 13:00 · รายงานเพื่อทราบ จะอัปเดตเมื่อกลับมาปกติ"),
]

# --- the card's ❌ openers, verbatim ----------------------------------------------------------------
BAD_OPENERS = [
    "เครื่องเดิม throughput ต่ำ rerun เยอะ",
    "2-2s across 2 levels, recalibrate แล้ว",
    "ย้ายขั้น centrifuge มาก่อน aliquot ลด TAT",
    "คนไม่พอ overtime เยอะ",
    "เครื่อง down รอช่าง",
]

BURIED = ("เมื่อเช้าเครื่องที่ 2 ค่าควบคุมหลุดเกณฑ์ ทีมไล่ตรวจแล้วพบสาเหตุจากอะไหล่เสื่อม\n"
          "ผลออกช้าไป 2 ชม. คนไข้ตกค้าง 10 ราย\n"
          "ขออนุมัติซื้ออะไหล่ 45,000 บาท ภายในวันที่ 15 ธ.ค.")


# ============================================================ rule #1 - the ask is in the first line
@pytest.mark.parametrize("kind,text", GOOD_OPENERS)
def test_good_openers_carry_exactly_one_ask(kind, text):
    # card VERDICT ✅ examples: the first line says what is needed
    r = bc.check(text, audience="director")
    assert r["ask"] == [kind]
    assert status(text, "ASK", audience="director") == "PASS"
    assert status(text, "JARGON", audience="director") == "PASS"


@pytest.mark.parametrize("text", BAD_OPENERS)
def test_bad_openers_have_no_ask(text):
    # card VERDICT ❌ examples: technical statement, nobody told what to do -> "จบลอย"
    assert status(text, "ASK", audience="director") == "FAIL"
    assert result(text, audience="director") == "FAIL"


def test_bottom_line_buried_at_the_end_fails():
    # trap: "ฝัง bottom line ไว้ท้ายสุด - เขาอ่านไม่ถึง". Same facts; only the order differs.
    assert status(BURIED, "ASK") == "FAIL"
    lines = BURIED.splitlines()
    fixed = "\n".join([lines[2]] + lines[:2])  # ask moved to line 1 (hand edit)
    assert status(fixed, "ASK") == "PASS"


def test_message_with_no_ask_ends_in_the_air():
    # § ขอการตัดสินใจให้ชัด: "จบลอยไม่ขอการตัดสินใจ" is a trap
    assert status("รายงานสถานการณ์: เครื่องเสียตั้งแต่เช้า ช่างกำลังมา คนไข้รอผล", "ASK") == "FAIL"


def test_two_asks_in_the_first_line_fail():
    # § ขอการตัดสินใจให้ชัด: "ต้องระบุ 1 อย่าง"
    assert status("รายงานเพื่อทราบ และขออนุมัติงบ 5,000 บาท ภายในวันที่ 3 ธ.ค.", "ASK") == "FAIL"


def test_email_may_close_on_the_decision_point():
    # § เลือกความยาว/รูปแบบตามช่องทาง: email subject = TL;DR, "ปิดท้ายด้วยจุดที่ต้องการการตัดสินใจ"
    email = ("หัวเรื่อง: เครื่องเดิมทำให้ผลล่าช้า 2 ชม./วัน - ข้อเสนอทดแทน 2 ทางเลือก\n"
             "เรียน ผอ.\n"
             "เครื่องเดิมอายุเกินอายุใช้งาน ผลล่าช้าเฉลี่ย 2 ชม./วัน คนไข้รอเพิ่ม 15 ราย/วัน\n"
             "ขออนุมัติตัวเลือก A หรือ B ภายในวันที่ 30 พ.ย.")
    assert status(email, "ASK", channel="email") == "PASS"
    assert status(email, "ASK", channel="memo") == "FAIL"  # the memo's first line must carry the ask


def test_email_greeting_is_not_the_bottom_line_but_memo_greeting_fails():
    body = "เรียน ผอ.\nขออนุมัติซื้ออะไหล่ 45,000 บาท ภายในวันที่ 15 ธ.ค.\nเครื่องที่ 2 ผลออกช้า 2 ชม."
    assert status(body, "ASK", channel="email") == "PASS"   # greeting skipped for email
    assert status(body, "ASK", channel="line") == "FAIL"    # LINE: "ไม่ต้องทักทาย" - first line is the bottom line


def test_markdown_title_is_not_the_bottom_line():
    memo = "# บันทึกเสนอจัดซื้อ\n\n> **สรุป:** ขออนุมัติซื้ออะไหล่ 45,000 บาท ภายในวันที่ 15 ธ.ค."
    assert status(memo, "ASK") == "PASS"


# ============================================================ § ขอการตัดสินใจให้ชัด - approval content
def test_approval_needs_a_number_and_a_deadline():
    assert status("ขออนุมัติเครื่องใหม่", "APPROVAL-NUMBER") == "FAIL"
    assert status("ขออนุมัติเครื่องใหม่", "APPROVAL-DEADLINE") == "FAIL"
    assert status("ขออนุมัติงบ 500,000 บาท", "APPROVAL-NUMBER") == "PASS"
    assert status("ขออนุมัติงบ 500,000 บาท", "APPROVAL-DEADLINE") == "FAIL"
    assert status("ขออนุมัติงบ 500,000 บาท ภายในวันที่ 30 พ.ย.", "APPROVAL-DEADLINE") == "PASS"
    assert status("ขออนุมัติงบ 500,000 บาท ให้ทันรอบงบประมาณ", "APPROVAL-DEADLINE") == "PASS"


def test_payback_period_is_not_a_deadline():
    # "คืนทุนภายใน 6 เดือน" says how fast the money comes back, not by when the reader must decide
    assert status("ขออนุมัติงบ 500,000 บาท คืนทุนภายใน 6 เดือน", "APPROVAL-DEADLINE") == "FAIL"


def test_info_and_decision_asks_do_not_need_a_deadline():
    # card: only ขออนุมัติ is defined as "ตัวเลือก + ตัวเลข + เส้นตาย"
    assert status("รายงานเพื่อทราบ: เครื่องกลับมาใช้งานได้แล้ว", "APPROVAL-DEADLINE") is None
    assert status("ขอตัดสินใจ: ส่งงานด่วนไปรพ.ข้างเคียงหรือรอช่าง", "APPROVAL-DEADLINE") is None


# ============================================================ § ตัวอย่างเต็ม - blanks must be filled
def test_unfilled_blanks_fail():
    raw = ("สรุป: ขออนุมัติจัดซื้อเครื่อง [รุ่น] งบ [Z] บาท คาดคืนทุน [N] เดือน\n"
           "ภายในวันที่ ___ เพื่อทันรอบงบประมาณ")
    assert status(raw, "PLACEHOLDER") == "FAIL"
    assert status("ขออนุมัติงบ 5 บาท ภายในวันที่ ___", "PLACEHOLDER") == "FAIL"


def test_document_ids_and_links_are_not_blanks():
    ok = "ขออนุมัติปิด [NC-2026-014] ภายในวันที่ 3 ธ.ค. รายละเอียดที่ [ลิงก์เอกสาร](http://example.invalid/doc) งบ 5 บาท"
    assert status(ok, "PLACEHOLDER") == "PASS"


def test_complete_card_memo_passes():
    # § ตัวอย่างเต็ม - บันทึกขออนุมัติเครื่อง, every [ ] filled (data/good_approval_request.txt, teaching numbers)
    assert result(read("good_approval_request.txt"), audience="director") == "PASS"


# ============================================================ § สิ่งที่เก็บไว้ / ตัดทิ้ง / แปล - by audience
JARGONY = ("ขออนุมัติซ่อมเครื่อง 12,000 บาท ภายในวันที่ 3 ธ.ค.\n"
           "Levey-Jennings พบ 1-3s และ 2-2s, Westgard fire, CV 4.2% ต้อง troubleshoot ต่อ")


@pytest.mark.parametrize("aud", ["committee", "director", "admin"])
def test_jargon_is_stripped_for_non_lab_readers(aud):
    assert status(JARGONY, "JARGON", audience=aud) == "FAIL"


def test_head_of_lab_keeps_concept_level_terms():
    # card: "อย่า over-strip - หัวหน้าแล็บอ่านศัพท์ระดับแนวคิดออก (QC, calibration, TAT...)"
    assert status(JARGONY, "JARGON", audience="labhead") == "PASS"
    assert status("ขออนุมัติ 5 บาท ภายในวันที่ 3 ธ.ค. QC ตกและ TAT ยาว", "JARGON-CONCEPT", audience="labhead") is None


def test_exec_only_terms_and_concept_warnings():
    t = "ขออนุมัติ 5 บาท ภายในวันที่ 3 ธ.ค. throughput ต่ำ"
    assert status(t, "JARGON", audience="director") == "FAIL"
    assert status(t, "JARGON", audience="committee") == "PASS"   # quality committee reads this level
    q = "ขออนุมัติ 5 บาท ภายในวันที่ 3 ธ.ค. QC ตก TAT ยาว"
    assert status(q, "JARGON-CONCEPT", audience="director") == "WARN"
    assert status(q, "JARGON-CONCEPT", audience="committee") is None


def test_no_audience_skips_the_jargon_check():
    assert status(JARGONY, "JARGON") == "INFO"


def test_patronising_replacements_fail_for_everyone():
    # card: แทน "QC fail" ด้วย "เครื่องงอน" = ดูถูกคนอ่าน · อย่าลดเป็น "เครื่องมีปัญหานิดหน่อย"
    for aud in (None, "labhead", "director"):
        assert status("รายงานเพื่อทราบ: เครื่องงอนตั้งแต่เช้า", "PATRONISING", audience=aud) == "FAIL"
        assert status("รายงานเพื่อทราบ: เครื่องมีปัญหานิดหน่อย", "PATRONISING", audience=aud) == "FAIL"
    assert status("รายงานเพื่อทราบ: ค่าควบคุมคุณภาพหลุดเกณฑ์", "PATRONISING") == "PASS"


# ============================================================ § Escalate เรื่อง NC / ความปลอดภัย
def test_safety_report_must_not_be_made_lighter():
    # card: "อาจมีผลที่รายงานผิดออกไปแล้ว N ราย" ห้ามแปลงเป็น "อาจมีข้อสังเกตเล็กน้อย"
    soft = "ขอตัดสินใจ: อาจมีข้อสังเกตเล็กน้อยเรื่องผลที่ปล่อยไปแล้ว"
    honest = "ขอตัดสินใจ: อาจมีผลที่รายงานผิดออกไปแล้ว 3 ราย กำลังเรียกคืนผล ขอตัดสินใจแจ้งแพทย์เจ้าของไข้ภายในวันนี้"
    assert status(soft, "SAFETY-MINIMISE", safety=True) == "FAIL"
    assert status(honest, "SAFETY-MINIMISE", safety=True) == "PASS"
    assert status(honest, "SAFETY-IMPACT", safety=True) is None      # a count is given
    assert status(soft, "SAFETY-IMPACT", safety=True) == "WARN"      # no count, no "not affected"
    assert status(soft, "SAFETY-MINIMISE") is None                   # only judged when --safety is set


# ============================================================ tone: advice, not verdicts
def test_commanding_the_reader_is_a_warning_not_a_failure():
    # card: "ท่านควรรีบอนุมัติ" = เสียมารยาท -> offer options instead
    t = "ขออนุมัติงบ 5 บาท ภายในวันที่ 3 ธ.ค. ท่านควรรีบอนุมัติ"
    assert status(t, "COMMANDING") == "WARN"
    assert result(t) == "PASS"


def test_negated_decision_is_not_commanding():
    # regression: "ไม่ต้องตัดสินใจ" (the card's own FYI wording) must not be read as an order
    assert status("รายงานเพื่อทราบ ไม่ต้องตัดสินใจ", "COMMANDING") is None


def test_hedging_is_a_warning():
    assert status("รายงานเพื่อทราบ: น่าจะเป็นที่หลอดไฟ อาจจะซ่อมได้", "HEDGING") == "WARN"
    assert status("รายงานเพื่อทราบ: ยังหาสาเหตุไม่เจอ", "HEDGING") is None


def test_numbers_are_listed_for_the_human_to_verify():
    r = bc.check("ขออนุมัติงบ 850,000 บาท ภายในวันที่ 30 พ.ย. คืนทุน 14 เดือน")
    nums = next(c["msg"] for c in r["checks"] if c["id"] == "NUMBERS")
    assert "850,000 บาท" in nums and "14 เดือน" in nums


def test_empty_text_fails():
    assert result("   \n") == "FAIL"


# ============================================================ command line
def run_cli(*args, stdin=None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run([sys.executable, TOOL, *args], input=stdin, capture_output=True, text=True,
                          encoding="utf-8", env=env)


def test_cli_exit_codes_and_json():
    ok = run_cli(os.path.join(DATA, "good_approval_request.txt"), "--audience", "director", "--json")
    assert ok.returncode == 0
    assert json.loads(ok.stdout)["result"] == "PASS"
    bad = run_cli(os.path.join(DATA, "bad_buried_ask.txt"), "--audience", "director")
    assert bad.returncode == 1
    assert "RESULT: FAIL" in bad.stdout and "ADVISORY" in bad.stdout


def test_cli_help_and_stdin():
    assert run_cli("--help").returncode == 0
    r = run_cli("-", "--audience", "labhead", stdin="รายงานเพื่อทราบ: เครื่องกลับมาใช้งานได้แล้ว")
    assert r.returncode == 0 and "RESULT: PASS" in r.stdout


# ============================================================ must-fail controls (the oracle must catch these)
def test_must_fail_control_ask_anywhere_counts(monkeypatch):
    """Inject the trap 'bottom line may sit anywhere' (= the line-1 rule removed). Oracle must go red."""
    monkeypatch.setattr(bc, "find_bluf_line", lambda text, channel="memo": text)
    with pytest.raises(AssertionError):
        test_bottom_line_buried_at_the_end_fails()
    with pytest.raises(AssertionError):
        test_email_may_close_on_the_decision_point()  # memo no longer needs the ask in line 1


def test_must_fail_control_blanks_are_fine(monkeypatch):
    """Inject the trap 'leave [ ] / ___ blanks in the message'. Oracle must go red."""
    monkeypatch.setattr(bc, "PLACEHOLDER_RE", re.compile(r"(?!x)x"))
    with pytest.raises(AssertionError):
        test_unfilled_blanks_fail()


def test_must_fail_control_payback_counts_as_deadline(monkeypatch):
    """Inject the trap 'any ภายใน N เดือน is a deadline'. Oracle must go red."""
    monkeypatch.setattr(bc, "DEADLINE_RE", re.compile(r"ภายใน|เดือน"))
    with pytest.raises(AssertionError):
        test_payback_period_is_not_a_deadline()


def test_must_fail_control_jargon_not_stripped(monkeypatch):
    """Inject the trap 'send the lab-bench explanation upward as is'. Oracle must go red."""
    monkeypatch.setattr(bc, "JARGON_CORE", [])
    monkeypatch.setattr(bc, "JARGON_EXEC", [])
    with pytest.raises(AssertionError):
        test_jargon_is_stripped_for_non_lab_readers("director")


def test_must_fail_control_safety_made_lighter(monkeypatch):
    """Inject the trap 'soften the NC report for tidiness'. Oracle must go red."""
    monkeypatch.setattr(bc, "SAFETY_MINIMISERS", re.compile(r"(?!x)x"))
    with pytest.raises(AssertionError):
        test_safety_report_must_not_be_made_lighter()


def test_must_fail_control_head_of_lab_over_stripped(monkeypatch):
    """Inject the trap 'strip concept-level terms for the head of lab too' (over-strip). Oracle must go red."""
    real = bc.check

    def over_strip(text, audience=None, channel="memo", safety=False):
        return real(text, audience="director" if audience == "labhead" else audience, channel=channel, safety=safety)

    monkeypatch.setattr(bc, "check", over_strip)
    with pytest.raises(AssertionError):
        test_head_of_lab_keeps_concept_level_terms()
