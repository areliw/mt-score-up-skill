"""Oracle tests for scripts/pubmed_query_check.py (pubmed-search-judgment).

Expected outcomes come from sources that are NOT this code:
  CARD  = the examples and rules written in skills/pubmed-search-judgment.md before the tool existed:
          rule 1 (2-3 concepts, MeSH + synonyms with OR, then AND, never the whole sentence), Fork 1 (MeSH vs keyword,
          [majr] risk), Fork 2 (field tags [tiab] [mh] [pt] [dp] [la] [au]; 2020:2026[dp]; no RCT-only filter on a
          diagnostic question), Fork 3 (0-3 results: [majr]+[ti] too tight; UK/US spellings), Fork 5 (log row).
  HELP  = the PubMed User Guide (pubmed.ncbi.nlm.nih.gov/help, read 2026-10-08): Boolean operators must be UPPERCASE;
          PubMed processes searches left to right; a field tag after several words searches them as a phrase.
Must-fail controls inject the card's traps and require the checker to go RED. Nothing here searches PubMed.

Run from the repo root:   python -m pytest skills/pubmed-search-judgment/evals -q
Run from the skill folder: python -m pytest evals -q
"""
import json
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import pubmed_query_check as pq  # noqa: E402

CARD_FORK5 = "(thalassemia[mh]) AND (machine learning[tiab] OR deep learning[tiab])"      # CARD Fork 5 table row
CARD_FORK2 = "(thalassemia[mh] OR thalassaemia[tiab])"                                      # CARD Fork 2 example


def check(q, question="auto"):
    return pq.run(q, question)[0]


def sev(q, level, question="auto"):
    return [i["message"] for i in check(q, question).items if i["severity"] == level]


def has(msgs, needle):
    return any(needle in m for m in msgs)


# ---------------------------------------------------------------- the card's own examples are valid
def test_card_fork5_example_has_no_error_and_one_mesh_only_warning():
    rep = check(CARD_FORK5)
    assert rep.count("ERROR") == 0
    warn = sev(CARD_FORK5, "WARN")
    assert len(warn) == 1 and "MeSH only" in warn[0]             # Fork 1 VERDICT: OR a keyword to the MeSH-only concept
    assert [c["terms"] for c in rep.concepts] == [["thalassemia[mh]"], ["machine learning[tiab]", "deep learning[tiab]"]]


def test_card_fork2_synonym_group_is_clean():
    rep = check(CARD_FORK2)
    assert rep.count("ERROR") == 0 and rep.count("WARN") == 0       # MeSH + keyword in one OR group


@pytest.mark.parametrize("q", ["2020:2026[dp]", "2018[dp]", "(thalassemia[mh]) AND 2020:2026[dp]"])
def test_card_year_forms_are_accepted(q):
    assert check(q).count("ERROR") == 0


def test_card_tags_are_all_recognised():
    q = " AND ".join("(x%d[%s])" % (i, t) for i, t in enumerate(["tiab", "mh", "majr", "pt", "la", "au", "ti"]))
    assert not has(sev(q, "WARN"), "unrecognised")


def test_unknown_tag_is_a_warning_not_an_error():
    rep = check("thalassemia[mh] AND screening[tiabs]")
    assert has(sev("thalassemia[mh] AND screening[tiabs]", "WARN"), "unrecognised field tag [tiabs]") and rep.count("ERROR") == 0


def test_phrase_with_tag_is_one_term_per_help():
    # HELP: "Using a search field tag after multiple terms will attempt to search those terms as a phrase"
    root = pq.run("machine learning[tiab]")[1]
    assert root["children"][0] == {"type": "term", "text": "machine learning", "tag": "tiab"}


# ---------------------------------------------------------------- Boolean grouping (CARD Fork 2, HELP left-to-right)
def test_synonyms_with_or_and_concepts_with_and_are_grouped_correctly():
    assert check("(a[mh] OR b[tiab]) AND (c[mh] OR d[tiab])").count("ERROR") == 0


def test_and_or_at_the_same_level_is_an_error():
    assert has(sev("thalassemia[mh] OR anemia[mh] AND screening[tiab]", "ERROR"), "mixed at one level")
    assert has(sev("a[tiab] AND b[tiab] OR c[tiab]", "ERROR"), "mixed at one level")
    assert not has(sev("a[tiab] AND (b[tiab] OR c[tiab])", "ERROR"), "mixed")
    assert not has(sev("a[tiab] AND b[tiab] NOT c[tiab]", "ERROR"), "mixed")         # AND with NOT only is not ambiguous here


def test_lowercase_operators_are_ordinary_words_help():
    w = sev("thalassemia[mh] and screening[tiab]", "WARN")
    assert has(w, "lowercase 'and'")
    root = pq.run("thalassemia[mh] and screening[tiab]")[1]
    assert [t["text"] for t in root["children"]] == ["thalassemia", "and screening"]    # no AND was recognised


def test_implicit_and_between_groups_warns():
    assert has(sev("(a[tiab] OR b[tiab]) (c[tiab] OR d[tiab])", "WARN"), "no operator")


# ---------------------------------------------------------------- well-formedness
@pytest.mark.parametrize("q,needle", [
    ("(thalassemia[mh] OR thalassaemia[tiab] AND screening[tiab]", "parentheses are not balanced"),
    ("thalassemia[mh] OR thalassaemia[tiab]) AND screening[tiab]", "parentheses are not balanced"),
    ("thalassemia[mh AND screening[tiab]", "square brackets"),
    ('"machine learning[tiab] AND thalassemia[mh]', "double quotes"),
    ("()", "empty parentheses"),
    ("AND thalassemia[mh]", "operator"),
    ("thalassemia[mh] AND", "ends with the operator"),
    ("thalassemia[mh] AND AND screening[tiab]", "operator"),
])
def test_malformed_queries_are_errors(q, needle):
    assert has(sev(q, "ERROR"), needle), sev(q, "ERROR")


def test_date_range_must_not_run_backwards():
    assert has(sev("thalassemia[mh] AND 2026:2020[dp]", "ERROR"), "runs backwards")
    assert has(sev("thalassemia[mh] AND last year[dp]", "ERROR"), "not YYYY")


# ---------------------------------------------------------------- concept count, MeSH, majr (CARD rule 1, Forks 1 and 3)
def test_more_than_three_concepts_warns_card_rule_1():
    assert has(sev("(a[tiab]) AND (b[tiab]) AND (c[tiab]) AND (d[tiab])", "WARN"), "4 concepts")
    assert not has(sev("(a[tiab]) AND (b[tiab]) AND (c[tiab])", "WARN"), "concepts joined")


def test_mesh_only_concept_warns_but_mesh_or_keyword_does_not():
    assert has(sev("thalassemia[mh] AND screening[tiab]", "WARN"), "MeSH only")
    assert not has(sev("(thalassemia[mh] OR thalassaemia[tiab]) AND screening[tiab]", "WARN"), "MeSH only")


def test_majr_warns_and_majr_with_ti_is_too_tight():
    assert has(sev("thalassemia[majr] OR thalassaemia[tiab]", "WARN"), "[majr]")
    assert has(sev("thalassemia[majr] AND screening[ti]", "WARN"), "very tight")


# ---------------------------------------------------------------- UK / US spelling (CARD Fork 3 + Anti-patterns)
@pytest.mark.parametrize("q,missing", [
    ("(anemia[tiab]) AND screening[tiab]", "anaemi"),
    ("(anaemia[tiab]) AND screening[tiab]", "anemi"),
    ("(leukemia[tiab]) AND screening[tiab]", "leukaemi"),
    ("(thalassemia[tiab]) AND screening[tiab]", "thalassaemi"),
    ("(pediatric[tiab]) AND screening[tiab]", "paediatric"),
])
def test_one_spelling_without_the_other_warns(q, missing):
    assert has(sev(q, "WARN"), missing)


def test_both_spellings_or_mesh_term_do_not_warn():
    assert not has(sev("(anemia[tiab] OR anaemia[tiab]) AND screening[tiab]", "WARN"), "spelling")
    assert not has(sev("anemia[mh] AND screening[tiab]", "WARN"), "spelling")           # MeSH covers both spellings


# ---------------------------------------------------------------- diagnostic questions (CARD Fork 2 VERDICT)
DIAG_RCT = "(thalassemia[mh]) AND (sensitivity[tiab] OR specificity[tiab]) AND randomized controlled trial[pt]"


def test_rct_only_filter_on_a_diagnostic_question_is_an_error():
    assert has(sev(DIAG_RCT, "ERROR"), "DIAGNOSTIC")                                    # auto-detected from the words
    assert has(sev("(thalassemia[mh]) AND randomized controlled trial[pt]", "ERROR", "diagnostic"), "DIAGNOSTIC")


def test_rct_filter_is_fine_for_a_treatment_question():
    assert not has(sev("(thalassemia[mh]) AND (iron chelation[tiab]) AND randomized controlled trial[pt]", "ERROR", "treatment"), "DIAGNOSTIC")
    assert not has(sev(DIAG_RCT, "ERROR", "treatment"), "DIAGNOSTIC")


def test_systematic_review_filter_is_allowed_on_a_diagnostic_question():
    assert not has(sev("(thalassemia[mh]) AND (sensitivity[tiab]) AND systematic review[pt]", "ERROR"), "DIAGNOSTIC")


def test_humans_hint_only_for_diagnostic_questions():
    assert has(sev("(thalassemia[mh]) AND (sensitivity[tiab] OR specificity[tiab])", "INFO"), "Humans")
    assert not has(sev("(thalassemia[mh]) AND (sensitivity[tiab]) AND Humans[mh]", "INFO"), "Humans")


# ---------------------------------------------------------------- whole sentence (CARD rule 1 / Anti-patterns)
def test_whole_sentence_is_an_error_but_a_short_term_is_not():
    q = "what is the best test for thalassemia screening in pregnant women"
    assert has(sev(q, "ERROR"), "whole question typed as one sentence")
    assert not has(sev("thalassemia screening", "ERROR"), "sentence")
    assert not has(sev(q + " AND humans[mh]", "ERROR"), "sentence")


# ---------------------------------------------------------------- reproducibility row (CARD Fork 5)
def test_log_row_never_contains_a_made_up_result_count():
    row = pq.log_row(CARD_FORK5, "2018:2026, Humans", "2026-10-08")
    assert row == "| 2026-10-08 | `%s` | 2018:2026, Humans | (เปิดดูจริง) |" % CARD_FORK5     # the card's own placeholder wording
    cells = [c.strip() for c in row.strip("|").split("|")]
    assert cells[3] == "(เปิดดูจริง)" and not any(ch.isdigit() for ch in cells[3])


# ---------------------------------------------------------------- CLI
def cli(*args):
    return subprocess.run([sys.executable, os.path.join(SKILL, "scripts", "pubmed_query_check.py"), *args],
                          capture_output=True, text=True, encoding="utf-8", timeout=60)


def test_cli_exit_codes_json_row_and_help():
    assert cli("--help").returncode == 0
    ok = cli(CARD_FORK5, "--row", "--filters", "Humans", "--date", "2026-10-08")
    assert ok.returncode == 0 and "| 2026-10-08 |" in ok.stdout and "ADVISORY" in ok.stdout and "PubMed was not searched" in ok.stdout
    bad = cli("thalassemia[mh] OR a[mh] AND b[tiab]", "--json")
    data = json.loads(bad.stdout)
    assert bad.returncode == 1 and data["errors"] >= 1
    f = os.path.join(HERE, "_tmp_query.txt")
    try:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("(thalassemia[mh] OR thalassaemia[tiab])\n  AND screening[tiab]\n")
        assert cli("--file", f).returncode == 0
    finally:
        os.remove(f)


def test_example_queries_file_matches_the_labels_in_it():
    path = os.path.join(SKILL, "data", "example_queries.txt")
    seen = 0
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#") or "\t" not in line:
                continue
            label, q = line.rstrip("\n").split("\t", 1)
            rep = check(q)
            seen += 1
            if label.startswith("ERROR"):
                assert rep.count("ERROR") >= 1, label
            elif label.startswith("OK"):
                assert rep.count("ERROR") == 0, label
            elif label.startswith("WARN"):
                assert rep.count("ERROR") == 0 and rep.count("WARN") >= 1, label
    assert seen == 11


# ---------------------------------------------------------------- MUST-FAIL CONTROLS (the card's traps)
def test_must_fail_control_whole_question_typed_in():
    """Anti-pattern 2: 'what is the best test for ...' typed as one sentence. Must be red."""
    assert check("what is the best test for thalassemia screening in pregnant women").count("ERROR") >= 1


def test_must_fail_control_rct_only_filter_on_diagnostic_accuracy():
    """Fork 2 VERDICT: 'do not filter RCT-only on a diagnostic question'. Must be red."""
    assert check(DIAG_RCT).count("ERROR") >= 1
    assert check("(thalassemia[mh]) AND (sensitivity[tiab] OR specificity[tiab])").count("ERROR") == 0


def test_must_fail_control_ungrouped_synonyms():
    """OR/AND without parentheses: the query silently means something else. Must be red."""
    assert check("thalassemia[mh] OR thalassaemia[tiab] AND machine learning[tiab]").count("ERROR") >= 1
    assert check("(thalassemia[mh] OR thalassaemia[tiab]) AND machine learning[tiab]").count("ERROR") == 0


def test_must_fail_control_mesh_only_on_a_new_topic_and_single_spelling():
    """Anti-patterns 3-4: MeSH alone on a recent topic, and one spelling only. Both must be flagged."""
    q = "(anemia[tiab]) AND (large language model[mh])"
    w = sev(q, "WARN")
    assert has(w, "MeSH only") and has(w, "anaemi")


def test_must_fail_control_mutant_without_grouping_rule_goes_red(monkeypatch):
    """If the checker stopped catching ungrouped OR/AND, the oracle test must fail."""
    monkeypatch.setattr(pq, "check_grouping", lambda root, rep: None)
    with pytest.raises(AssertionError):
        test_and_or_at_the_same_level_is_an_error()
