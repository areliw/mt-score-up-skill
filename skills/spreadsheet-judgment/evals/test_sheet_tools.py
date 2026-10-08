"""Oracle tests for spreadsheet-judgment tools (sheet_stats.py, sheet_audit.py).

Expected numbers come from places other than this code:
  MSDOC = Microsoft Office documentation examples.  STDEV.S / STDEV.P: breaking strengths
          1345 1301 1368 1322 1310 1370 1318 1350 1303 1299 -> 27.46391572 and 26.05455814.
          PERCENTILE.INC({1,2,3,4}, 0.3) = 1.9 ; PERCENTILE.EXC({1,2,3,4}, 0.25) = 1.25 ; EXC is #NUM! below 1/(n+1).
  ZIEMANN= Ziemann, Eren & El-Osta (2016) Genome Biology 17:177: SEPT2 -> 2-Sep, MARCH1 -> 1-Mar, DEC1 -> 1-Dec
  XLSPEC = Excel specifications and limits: numbers keep 15 significant digits
  HAND   = arithmetic in the comment next to each assertion
Must-fail controls inject the traps the card warns about (STDEV.P for a sample, an off-by-one percentile rank, trusting
the file as if Excel would not convert anything) and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import csv
import json
import math
import os
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import sheet_audit  # noqa: E402
import sheet_stats  # noqa: E402

BREAKING = [1345, 1301, 1368, 1322, 1310, 1370, 1318, 1350, 1303, 1299]
EXAMPLE = os.path.join(SKILL, "data", "samples_example.csv")


def kinds(value):
    return [k for k, _, _ in sheet_audit.cell_risks(value)]


def rows_of(text_rows):
    return [list(r) for r in text_rows]


def found(findings, kind):
    return [f for f in findings if f["kind"] == kind]


# ================================================================ sheet_stats (Excel definitions)
def test_stdev_s_and_p_match_microsoft_docs():
    assert sheet_stats.stdev_s(BREAKING) == pytest.approx(27.46391572, abs=1e-8)   # MSDOC
    assert sheet_stats.stdev_p(BREAKING) == pytest.approx(26.05455814, abs=1e-8)   # MSDOC
    # HAND: the two differ by exactly sqrt(n/(n-1)) = sqrt(10/9) = 1.054093
    assert sheet_stats.stdev_s(BREAKING) / sheet_stats.stdev_p(BREAKING) == pytest.approx(math.sqrt(10 / 9))


def test_stdev_s_needs_two_values():
    with pytest.raises(ValueError):
        sheet_stats.stdev_s([5])  # Excel: #DIV/0!


def test_levey_jennings_lines_use_sample_sd():
    d = sheet_stats.describe_stdev(BREAKING)
    assert d["mean"] == pytest.approx(1328.6)                                       # HAND: 13286 / 10
    assert d["lj_lines"]["+2SD"] == pytest.approx(1328.6 + 2 * 27.46391572, abs=1e-6)
    assert d["lj_lines"]["-3SD"] == pytest.approx(1328.6 - 3 * 27.46391572, abs=1e-6)


def test_percentile_inc_and_exc_match_microsoft_docs():
    assert sheet_stats.percentile_inc([1, 2, 3, 4], 0.3) == pytest.approx(1.9)      # MSDOC; HAND: rank 0.3*3+1 = 1.9
    assert sheet_stats.percentile_exc([1, 2, 3, 4], 0.25) == pytest.approx(1.25)    # MSDOC; HAND: rank 0.25*5 = 1.25
    assert sheet_stats.percentile_inc(list(range(1, 11)), 0.9) == pytest.approx(9.1)  # HAND: rank 0.9*9+1 = 9.1
    assert sheet_stats.percentile_inc([1, 2, 3, 4], 0.5) == pytest.approx(2.5)      # median
    with pytest.raises(ValueError):
        sheet_stats.percentile_exc([1, 2, 3, 4], 0.1)                               # MSDOC: #NUM! below 1/(n+1) = 0.2


def test_skewed_tat_summary_prefers_median_and_p90(tmp_path):
    p = tmp_path / "tat.csv"
    vals = [10, 12, 11, 13, 12, 11, 10, 12, 90]
    p.write_text("tat\n" + "\n".join(map(str, vals)) + "\nabc\n", encoding="utf-8")
    nums, text, blank = sheet_stats.read_column(str(p), "tat")
    s = sheet_stats.summarize(nums, text, blank)
    assert s["mean"] == pytest.approx(181 / 9)                                      # HAND: 181 / 9 = 20.11
    assert s["median"] == 12                                                        # HAND: sorted 10 10 11 11 12 12 12 13 90 -> 5th
    assert s["p90"] == pytest.approx(28.4)                                          # HAND: rank 0.9*8 = 7.2 -> 13 + 0.2*(90-13)
    assert any("right-skewed" in h for h in s["hints"])
    assert s["text_cells_skipped"] == [{"row": 11, "value": "abc"}]                 # numbers-as-text are skipped silently by Excel
    assert any("non-numeric" in h for h in s["hints"])


def test_symmetric_column_gets_no_skew_hint():
    s = sheet_stats.summarize([10, 11, 12, 13, 14])
    assert s["hints"] == []


def test_stats_cli_json_and_errors(capsys):
    assert sheet_stats.main(["stdev", "--json"] + [str(v) for v in BREAKING]) == 0
    assert json.loads(capsys.readouterr().out)["stdev_s"] == pytest.approx(27.46391572, abs=1e-6)
    assert sheet_stats.main(["percentile", "--p", "0.1", "--exc", "1", "2", "3", "4"]) == 2   # #NUM!
    with pytest.raises(SystemExit) as e:
        sheet_stats.main(["--help"])
    assert e.value.code == 0


# ================================================================ sheet_audit (Excel auto-conversion + layout)
def test_gene_symbols_that_excel_turns_into_dates():
    got = [(sheet_audit.cell_risks(v) or [(None, None, None)])[0][2] for v in ("SEPT2", "MARCH1", "DEC1")]
    assert got == ["2-Sep", "1-Mar", "1-Dec"]  # ZIEMANN
    assert "gene-date" in kinds("Oct4") and "gene-date" in kinds("sept10")
    for safe in ("TP53", "BRCA1", "SEPTIN2", "MARCHF1", "ABC123", "DEC32", "MAR0"):  # new HGNC symbols are safe; day 32 / 0 is not a date
        assert "gene-date" not in kinds(safe), safe


def test_leading_zero_and_long_digit_strings():
    first = sheet_audit.cell_risks("00123")[0]
    assert (first[0], first[2]) == ("leading-zero", "123")  # HAND: Excel stores the number 123
    assert "leading-zero" not in kinds("0") and "leading-zero" not in kinds("0.5") and "leading-zero" not in kinds("123")
    assert "long-digits" in kinds("1234567890123456")       # XLSPEC: 16 digits -> only 15 survive
    assert "long-digits" not in kinds("123456789012345")    # exactly 15 digits is kept
    assert sheet_audit.cell_risks("1234567890123456")[0][2] == "1234567890123450"  # HAND: the 16th digit becomes 0


def test_date_like_and_scientific_notation():
    assert "date-like" in kinds("1-2") and "date-like" in kinds("3/4") and "date-like" in kinds("12/5/2020")
    assert "date-like" not in kinds("13/45") and "date-like" not in kinds("2026")
    assert sheet_audit.cell_risks("12E3")[0][2] == "12000" and "sci-notation" in kinds("1e5")
    assert kinds("E2F1") == []                              # a gene name with an E in it is not scientific notation


def test_audit_of_the_example_file_finds_the_planted_problems():
    with open(EXAMPLE, encoding="utf-8-sig", newline="") as f:
        findings = sheet_audit.audit(list(csv.reader(f)))
    assert {f["row"] for f in found(findings, "leading-zero")} == {2, 3, 4, 6}      # 00123 00456 00789 01012
    assert {f["row"] for f in found(findings, "gene-date")} == {2, 4}                # SEPT2, MARCH1
    assert found(findings, "already-converted") and found(findings, "unit-or-flag-in-value")
    assert found(findings, "single-cell-row")[0]["row"] == 7 and found(findings, "blank-key-cell")[0]["row"] == 5


def test_text_mixed_into_numeric_column_only_when_the_rest_is_numeric():
    mixed = sheet_audit.audit([["v"], ["5.2"], ["6.1 mg/dL"], ["4.8"]])
    assert found(mixed, "unit-or-flag-in-value")
    assert not found(sheet_audit.audit([["v"], ["5.2"], ["6.1"], ["4.8"]]), "unit-or-flag-in-value")
    assert not found(sheet_audit.audit([["v"], ["alpha"], ["beta"]]), "unit-or-flag-in-value")
    assert found(sheet_audit.audit([["v"], ["12"], ["<5"], ["9"]]), "unit-or-flag-in-value")  # censored value as text


def test_header_and_blank_row_checks():
    f = sheet_audit.audit(rows_of([["a", "", "a"], ["1", "2", "3"], ["", "", ""], ["4", "5", "6"]]))
    assert len(found(f, "blank-header")) == 1 and len(found(f, "duplicate-header")) == 1
    assert found(f, "blank-row")[0]["row"] == 3
    assert sheet_audit.audit(rows_of([["a", "b"], ["1", "2"], ["3", "4"]])) == []   # a clean table has no findings


def test_audit_cli_exit_code_and_json(tmp_path, capsys):
    bad = tmp_path / "bad.csv"
    bad.write_text("code,gene\n00123,TP53\n", encoding="utf-8")
    assert sheet_audit.main([str(bad), "--json"]) == 1                              # leading zero = ERROR
    assert json.loads(capsys.readouterr().out)[0]["would_become"] == "123"
    ok = tmp_path / "ok.csv"
    ok.write_text("code,gene\nA123,TP53\n", encoding="utf-8")
    assert sheet_audit.main([str(ok)]) == 0
    with pytest.raises(SystemExit) as e:
        sheet_audit.main(["--help"])
    assert e.value.code == 0


# ================================================================ must-fail controls (trap injected -> oracle must go red)
def test_must_fail_control_stdev_p_used_for_a_sample(monkeypatch):
    """Trap: STDEV.P where the cells are a sample. The Microsoft-docs oracle must go red."""
    monkeypatch.setattr(sheet_stats, "stdev_s", sheet_stats.stdev_p)
    with pytest.raises(AssertionError):
        test_stdev_s_and_p_match_microsoft_docs()


def test_must_fail_control_percentile_rank_off_by_one(monkeypatch):
    """Trap: rank = p*n instead of p*(n-1). The PERCENTILE.INC oracle must go red."""
    def wrong(xs, p):
        s = sorted(xs)
        r = min(p * len(s), len(s) - 1)
        lo = int(math.floor(r))
        hi = min(lo + 1, len(s) - 1)
        return s[lo] + (s[hi] - s[lo]) * (r - lo)
    monkeypatch.setattr(sheet_stats, "percentile_inc", wrong)
    with pytest.raises(AssertionError):
        test_percentile_inc_and_exc_match_microsoft_docs()


def test_must_fail_control_assume_excel_converts_nothing(monkeypatch):
    """Trap: trust the file ('it looks fine as text'). The auto-conversion oracle must go red."""
    monkeypatch.setattr(sheet_audit, "cell_risks", lambda v: [])
    with pytest.raises(AssertionError):
        test_gene_symbols_that_excel_turns_into_dates()
    with pytest.raises(AssertionError):
        test_audit_of_the_example_file_finds_the_planted_problems()
