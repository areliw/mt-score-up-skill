"""Oracle tests for ai-assistant-calibration tool reply_lint.py.

Expected labels come from the card's rules (skills/ai-assistant-calibration.md), NOT from the code:
  top box      : ฟันธงก่อน แล้วค่อยอธิบาย · ตัดเกริ่นนำ/สรุปซ้ำ/options ที่ไม่ได้ขอ
  โทน          : ค่าเริ่มต้น = สั้น 2-5 บรรทัด (ยาวได้เมื่อถูกขอ / โหมด ป.3) · ซ่อน scaffolding (rule#/ขั้นตอนคิด)
  โต้ตอบ       : ผู้ใช้ค้าน = calibrate อย่าขอโทษพร่ำเพรื่อ
  ความซื่อสัตย์ : ถ้าจะใช้คำว่า "น่าจะ/มั้ง" = ไปเช็กก่อน; ไม่รู้ให้บอกว่าไม่รู้
Each sample reply was labelled by hand against those rules before running the tool.
Must-fail controls inject the two habits the card fights hardest (preamble, unchecked hedge).

Run from the skill folder:  python -m pytest evals -q
"""
import os
import subprocess
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import reply_lint as rl  # noqa: E402

SCRIPT = os.path.join(SKILL, "scripts", "reply_lint.py")
DATA = os.path.join(SKILL, "data")


def kinds(text, **kw):
    return sorted(f["kind"] for f in rl.lint(text, **kw)["findings"])


def read(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return f.read()


def test_preamble_first_line_is_flagged():
    # top box: verdict on line 1, no warm-up
    assert "PREAMBLE" in kinds("คำถามที่ดีมากครับ!\nตรวจซ้ำก่อน")
    assert "PREAMBLE" in kinds("Great question! The answer is 42.")


def test_verdict_first_line_passes():
    assert kinds("ตรวจซ้ำก่อน อย่าเพิ่งรายงาน\nเหตุผล: delta เกินเกณฑ์") == []


def test_unchecked_hedge_is_flagged():
    # ความซื่อสัตย์: "น่าจะ" = go check first
    assert kinds("ค่านี้น่าจะปกติครับ") == ["HEDGE"]
    assert kinds("This is probably fine.") == ["HEDGE"]


def test_hedge_with_honest_label_passes():
    # "ไม่รู้ให้บอกว่าไม่รู้": an explicit uncertainty label is the allowed form
    assert kinds("ค่านี้น่าจะปกติ แต่ไม่แน่ใจ ต้องเช็ก SOP") == []
    assert kinds("ค่านี้น่าจะปกติ [~est]") == []


def test_scaffolding_leak_is_flagged():
    assert "SCAFFOLDING" in kinds("ตามกฎข้อ 3 ผมควรตอบสั้น")
    assert "SCAFFOLDING" in kinds("Per rule #2 I will be brief.")


def test_length_budget_and_long_ok():
    six = "\n".join("บรรทัด %d" % i for i in range(6))
    assert "TOO_LONG" in kinds(six)
    assert "TOO_LONG" not in kinds(six, long_ok=True)          # ขยายยาวเฉพาะตอนถูกขอ
    assert "TOO_LONG" not in kinds("\n".join("x%d" % i for i in range(5)))   # 5 = still inside 2-5


def test_unasked_options_warn_but_asked_options_pass():
    opts = "ตัวเลือก A: รอ\nตัวเลือก B: ตรวจซ้ำ\nตัวเลือก C: ส่งต่อ"
    assert "OPTIONS_DUMP" in kinds(opts)
    assert "OPTIONS_DUMP" not in kinds(opts, options_asked=True)


def test_apology_spam_and_recap_warn():
    assert "APOLOGY" in kinds("ขอโทษครับ ผมพลาด ขอโทษอีกครั้ง")
    assert "APOLOGY" not in kinds("ขอโทษครับ แก้แล้ว: ค่าคือ 5")
    assert "RECAP" in kinds("ตรวจซ้ำก่อน\nเหตุผล: delta\nสรุป: ตรวจซ้ำก่อน")


def test_bad_example_file_hand_labelled():
    # data/reply_bad_example.txt, line by line: 1 preamble · 2 rule# · 3 hedge · 4 two apologies
    # 5-7 three options · 8 recap + hedge ; 8 lines > 5
    res = rl.lint(read("reply_bad_example.txt"))
    assert res["summary"]["verdict"] == "FIX"
    assert kinds(read("reply_bad_example.txt")) == sorted(
        ["PREAMBLE", "SCAFFOLDING", "HEDGE", "HEDGE", "TOO_LONG", "OPTIONS_DUMP", "APOLOGY", "RECAP"])


def test_good_example_file_passes():
    # verdict on line 1, 4 lines, the one uncertain value says "ไม่แน่ใจ ต้องเช็ก"
    assert rl.lint(read("reply_good_example.txt"))["summary"]["verdict"] == "PASS"


def test_cli_strict_thai_stdin_under_cp874():
    env = dict(os.environ, PYTHONIOENCODING="cp874")
    p = subprocess.run([sys.executable, SCRIPT, "-", "--strict"], input="ค่านี้น่าจะปกติ ✅".encode("utf-8"),
                       capture_output=True, env=env)
    assert p.returncode == 1 and b"HEDGE" in p.stdout


# ---------------------------------------------------------------- must-fail controls
def test_must_fail_control_any_opening_counts_as_verdict(monkeypatch):
    """Trap: 'it answered eventually' - warm-up openings accepted as the verdict."""
    monkeypatch.setattr(rl, "PREAMBLE", rl.re.compile(r"(?!x)x"))
    with pytest.raises(AssertionError):
        test_preamble_first_line_is_flagged()


def test_must_fail_control_hedge_accepted(monkeypatch):
    """Trap: 'น่าจะ' treated as honest enough - guessing in a confident voice slips through."""
    monkeypatch.setattr(rl, "UNSURE_LABEL", rl.re.compile(r"."))
    with pytest.raises(AssertionError):
        test_unchecked_hedge_is_flagged()
