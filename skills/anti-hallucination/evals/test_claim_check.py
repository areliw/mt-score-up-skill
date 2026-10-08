"""Oracle tests for anti-hallucination tool claim_check.py.

Expected labels come from the card's own rules (skills/anti-hallucination.md), NOT from the code:
  rule 1 box  : every citation / number / dose = something a person opens, not a final answer
  §2          : separate "confident" from "must check"; medical values must be verified before use
  §3          : never invent DOI / paper / author / year; unsure reference = "something to search"
  checklist   : "has a reference" is not proof - open it yourself
Each test sentence was labelled by hand against those rules before running the tool.
Must-fail controls inject the traps the card warns about and require the oracle tests to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import os
import subprocess
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import claim_check as cc  # noqa: E402

SCRIPT = os.path.join(SKILL, "scripts", "claim_check.py")
EXAMPLE = os.path.join(SKILL, "data", "answer_example.txt")


def kinds(text):
    return [(f["level"], f["kind"]) for f in cc.check(text)["findings"]]


# ---------------------------------------------------------------- numbers / medical values (§2)
def test_unsourced_medical_value_is_flagged():
    # §2: a reference range with no source or confidence label must not be sent as-is
    assert kinds("Hb ปกติผู้ชาย 13.5-17.5 g/dL") == [("FLAG", "UNSOURCED_MEDICAL")]


def test_confirmed_source_tag_clears_the_number():
    # owner's provenance tag [✓src] = source stated -> no FLAG on the number
    assert ("FLAG", "UNSOURCED_MEDICAL") not in kinds("Hb 12.0-15.5 g/dL [✓src]")
    assert kinds("Hb 12.0-15.5 g/dL [✓src]") == []


def test_unsure_medical_value_is_honest_but_still_check():
    # §2 + rule 1: saying "from memory" is honest, but a dose must still be verified before use
    assert kinds("ขนาดยา 500 mg ทุก 8 ชม. [~mem]") == [("CHECK", "MEDICAL_UNVERIFIED")]


def test_unsure_non_medical_number_is_enough():
    # §2: labelled estimate on a non-medical figure = the separation the card asks for
    assert kinds("ประมาณ 40% ของผู้ตอบ [~est]") == []


def test_dates_and_money_are_claims():
    # rule 1: dates and amounts are checkable claims exactly like numbers
    k = kinds("Paid 13,560 บาท on 2026-09-27.")
    assert k == [("FLAG", "UNSOURCED_CLAIM")]
    detail = cc.check("Paid 13,560 บาท on 2026-09-27.")["findings"][0]["detail"]
    assert "2026-09-27" in detail and "13,560 บาท" in detail


def test_lab_value_is_not_mistaken_for_a_doi():
    # "10.5 mg/dL" looks like "10.<digits>" but is a lab value, not an identifier
    assert ("CHECK", "DOI_SHAPE_ONLY") not in kinds("K 10.5 mg/dL")
    assert kinds("K 10.5 mg/dL") == [("FLAG", "UNSOURCED_MEDICAL")]


def test_numeric_footnote_points_to_a_reference_line():
    # a [1] footnote is a pointer; the reference line itself is checked on its own line
    assert kinds("Hb 13.5 g/dL [1].") == []


# ---------------------------------------------------------------- identifiers (§3)
def test_well_formed_doi_is_never_silently_ok():
    # checklist: "has a reference" is not proof; a perfectly formed DOI can be fabricated
    assert ("CHECK", "DOI_SHAPE_ONLY") in kinds("ดู doi:10.1000/182")


def test_malformed_doi_is_flagged():
    # 10.12/... has a 2-digit registrant: no DOI can have that shape -> cannot be opened
    assert ("FLAG", "DOI_MALFORMED") in kinds("อ้างอิง doi:10.12/abc")


def test_pmid_is_check_not_ok():
    assert kinds("PMID: 12345678 supports it") == [("CHECK", "ID_SHAPE_ONLY")]


def test_author_year_without_identifier_is_flagged():
    # §3: author + year with nothing to open = the most fluent fabrication
    assert ("FLAG", "CITATION_NO_IDENTIFIER") in kinds("Smith et al. (2019) รายงานว่าได้ผลดี")


def test_author_year_labelled_unsure_is_check():
    # §3: unsure reference said out loud = "something to search", honest -> CHECK, not FLAG
    assert kinds("Smith et al. (2019) found it [~mem].") == [("CHECK", "CITATION_UNSURE")]


def test_author_year_inside_source_tag_is_check():
    assert kinds("Hb 12.0 g/dL [✓src WHO 2011]") == [("CHECK", "SOURCE_TAG_NO_IDENTIFIER")]


def test_author_year_with_doi_is_not_flagged():
    k = kinds("Lee and Park (2020) doi:10.1000/182")
    assert ("FLAG", "CITATION_NO_IDENTIFIER") not in k and ("CHECK", "DOI_SHAPE_ONLY") in k


# ---------------------------------------------------------------- whole-file + CLI
def test_example_file_hand_labelled():
    # data/answer_example.txt labelled line by line from the rules above:
    # 1 FLAG medical · 2 CHECK tag-only source · 3 CHECK unsure dose · 4 FLAG cite + FLAG 95%
    # 5 CHECK PMID · 6 FLAG malformed DOI + CHECK good DOI · 7 FLAG date
    with open(EXAMPLE, encoding="utf-8") as f:
        res = cc.check(f.read())
    assert res["summary"]["flag"] == 5
    assert res["summary"]["check"] == 4
    lines = {f["line"] for f in res["findings"] if f["level"] == "FLAG"}
    assert lines == {1, 4, 6, 7}


def test_strict_exit_codes():
    env = dict(os.environ, PYTHONIOENCODING="cp874")
    bad = subprocess.run([sys.executable, SCRIPT, "-", "--strict"], input="Target is 5 mg.",
                         capture_output=True, text=True, encoding="utf-8", env=env)
    ok = subprocess.run([sys.executable, SCRIPT, "-", "--strict"], input="ดู PMID: 12345678",
                        capture_output=True, text=True, encoding="utf-8", env=env)
    assert bad.returncode == 1 and "ADVISORY" in bad.stdout
    assert ok.returncode == 0


def test_thai_stdin_under_cp874_keeps_unsure_tag():
    # a piped Thai answer on a cp874 console must still see the Thai "ไม่แน่ใจ" label (no mojibake)
    env = dict(os.environ, PYTHONIOENCODING="cp874")
    p = subprocess.run([sys.executable, SCRIPT, "-", "--json"], input="ขนาดยา 500 mg [ไม่แน่ใจ] ✅".encode("utf-8"),
                       capture_output=True, env=env)
    assert p.returncode == 0, p.stderr
    assert b"MEDICAL_UNVERIFIED" in p.stdout


# ---------------------------------------------------------------- must-fail controls
def test_must_fail_control_any_tag_counts_as_source(monkeypatch):
    """Trap 'confidence != correctness': treat ANY [..] label (even [~mem]) as a source."""
    monkeypatch.setattr(cc, "has_evidence", lambda s: bool(cc.TAG_RE.search(s)))
    with pytest.raises(AssertionError):
        test_unsure_medical_value_is_honest_but_still_check()


def test_must_fail_control_well_formed_doi_trusted(monkeypatch):
    """Trap 'it has a reference so it is real': a well-formed DOI is accepted without a CHECK."""
    real = cc.id_finding
    monkeypatch.setattr(cc, "id_finding",
                        lambda no, kind, val: None if (kind == "doi" and cc.DOI_SHAPE.match(val)) else real(no, kind, val))
    with pytest.raises(AssertionError):
        test_well_formed_doi_is_never_silently_ok()


def test_must_fail_control_author_year_accepted_as_citation(monkeypatch):
    """Trap §3: 'Smith et al. (2019)' treated as a real citation because it has author + year."""
    monkeypatch.setattr(cc, "CITATION_RE", cc.re.compile(r"(?!x)x"))
    with pytest.raises(AssertionError):
        test_author_year_without_identifier_is_flagged()
