"""Oracle tests for db-judgment tools (sql_lint.py, dml_preview.py).

The oracle is an independent SQL engine: every trap the linter flags is first RUN on SQLite (standard-library
sqlite3) to prove it really misbehaves, and only then is the linter required to flag it (and to stay silent on the
safe rewrite). Expected numbers are SQL semantics, written by hand in the comments:
  270701 = CMU 270701 Database Systems digest: three-valued logic (use IS NULL, not = NULL), "DELETE ... without
           WHERE deletes every row", CROSS JOIN = Cartesian product, HAVING filters after group, NOT EXISTS
  HAND   = arithmetic in the comment next to each assertion
Must-fail controls inject the traps (a WHERE that only exists in a subquery, a preview that commits, a linter that
reads keywords inside comments) and require the oracle to go red.

Run from the skill folder:  python -m pytest evals -q
"""
import os
import sqlite3
import sys

import pytest

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import dml_preview  # noqa: E402
import sql_lint  # noqa: E402


@pytest.fixture
def con():
    c = sqlite3.connect(":memory:")
    c.executescript("""
        CREATE TABLE a(id INTEGER);  INSERT INTO a VALUES (1),(2),(3);
        CREATE TABLE b(id INTEGER);  INSERT INTO b VALUES (1),(NULL);
        CREATE TABLE p(id INTEGER);  INSERT INTO p VALUES (1);
        CREATE TABLE r(pid INTEGER, v INTEGER);  INSERT INTO r VALUES (1,10),(1,20);
        CREATE TABLE t(id INTEGER, x INTEGER);   INSERT INTO t VALUES (1,NULL),(2,5),(3,6);
    """)
    yield c
    c.close()


def rules(sql, **kw):
    return [f["rule"] for f in sql_lint.lint(sql, **kw)]


def one(con, sql):
    return con.execute(sql).fetchall()


# ================================================================ sql_lint: each trap is real on SQLite, then linted
def test_not_in_with_null_returns_nothing_not_exists_does(con):
    bad = "SELECT id FROM a WHERE id NOT IN (SELECT id FROM b)"
    good = "SELECT id FROM a WHERE NOT EXISTS (SELECT 1 FROM b WHERE b.id = a.id)"
    # HAND (three-valued logic): b holds {1, NULL}. id=2: 2<>1 TRUE and 2<>NULL UNKNOWN -> UNKNOWN -> row dropped. Same for 3. id=1 is FALSE.
    assert one(con, bad) == []
    assert one(con, good) == [(2,), (3,)]
    assert "D002" in rules(bad) and "D002" not in rules(good)
    assert "D002" in rules("DELETE FROM a WHERE id NOT IN (1, 2, NULL)")


def test_join_without_condition_is_a_cartesian_product(con):
    assert one(con, "SELECT COUNT(*) FROM a JOIN b") == [(6,)]                      # HAND: 3 x 2
    assert one(con, "SELECT COUNT(*) FROM a JOIN b ON a.id = b.id") == [(1,)]       # only id 1 (NULL matches nothing)
    assert "D004" in rules("SELECT COUNT(*) FROM a JOIN b")
    assert "D004" not in rules("SELECT COUNT(*) FROM a JOIN b ON a.id = b.id")
    assert "D004" not in rules("SELECT COUNT(*) FROM a JOIN b USING (id)")
    assert "D004" not in rules("SELECT COUNT(*) FROM a CROSS JOIN b")                # explicit cross join is intentional
    assert one(con, "SELECT COUNT(*) FROM a, b") == [(6,)] and "D005" in rules("SELECT * FROM a, b WHERE a.id = b.id")


def test_second_join_missing_its_condition_is_found():
    sql = "SELECT 1 FROM a JOIN b ON a.id = b.id JOIN p WHERE p.id = 1"
    assert rules(sql).count("D004") == 1


def test_update_delete_without_where_touch_every_row(con):
    assert con.execute("DELETE FROM a WHERE id = 2").rowcount == 1
    assert con.execute("DELETE FROM a").rowcount == 2                                 # the 2 rows still left: everything goes
    assert "D001" in rules("DELETE FROM a") and "D001" in rules("UPDATE t SET x = 0")
    assert "D001" not in rules("DELETE FROM a WHERE id = 2")
    assert "D001" not in rules("WITH c AS (SELECT 1) DELETE FROM t WHERE id = 1")


def test_where_inside_a_subquery_is_not_a_where_clause(con):
    sql = "UPDATE t SET x = (SELECT v FROM r WHERE r.pid = 1 LIMIT 1)"
    assert con.execute(sql).rowcount == 3                                             # HAND: no outer WHERE -> all 3 rows
    assert "D001" in rules(sql)
    assert "D001" not in rules(sql + " WHERE id = 1")


def test_equals_null_never_matches(con):
    assert one(con, "SELECT COUNT(*) FROM t WHERE x = NULL") == [(0,)]                # comparison is UNKNOWN for every row
    assert one(con, "SELECT COUNT(*) FROM t WHERE x IS NULL") == [(1,)]
    assert "D009" in rules("SELECT * FROM t WHERE x = NULL") and "D009" in rules("SELECT * FROM t WHERE x <> NULL")
    assert "D009" not in rules("SELECT * FROM t WHERE x IS NULL")
    assert "D009" not in rules("UPDATE t SET x = NULL WHERE id = 2")                  # assignment of NULL is legal


def test_union_removes_duplicates_union_all_does_not(con):
    assert len(one(con, "SELECT 1 UNION SELECT 1")) == 1
    assert len(one(con, "SELECT 1 UNION ALL SELECT 1")) == 2
    assert "D006" in rules("SELECT 1 UNION SELECT 1") and "D006" not in rules("SELECT 1 UNION ALL SELECT 1")


def test_count_after_join_counts_rows_not_patients(con):
    assert one(con, "SELECT COUNT(*) FROM p JOIN r ON r.pid = p.id") == [(2,)]       # 1 patient, 2 results
    assert one(con, "SELECT COUNT(DISTINCT p.id) FROM p JOIN r ON r.pid = p.id") == [(1,)]
    assert "D008" in rules("SELECT COUNT(*) FROM p JOIN r ON r.pid = p.id")
    assert "D008" not in rules("SELECT COUNT(DISTINCT p.id) FROM p JOIN r ON r.pid = p.id")


def test_deep_offset_and_select_star():
    assert "D007" in rules("SELECT id FROM t ORDER BY id LIMIT 20 OFFSET 100000")
    assert "D007" in rules("SELECT id FROM t ORDER BY id LIMIT 100000, 20")
    assert "D007" not in rules("SELECT id FROM t ORDER BY id LIMIT 20 OFFSET 100")
    assert "D007" in rules("SELECT id FROM t LIMIT 5 OFFSET 500", offset_warn=500)
    assert "D003" in rules("SELECT * FROM t") and "D003" in rules("SELECT x.* FROM t x")
    assert "D003" not in rules("SELECT COUNT(*) FROM t")


def test_keywords_in_comments_and_strings_do_not_fire():
    assert rules("-- DELETE FROM a\nSELECT id FROM t") == []
    assert rules("/* UPDATE t SET x = 1 */ SELECT id FROM t") == []
    assert rules("SELECT 'DELETE FROM a' AS s FROM t") == []
    bad = "SELECT 1;\n\nDELETE FROM a"          # line numbers survive the masking
    assert [(f["rule"], f["line"]) for f in sql_lint.lint(bad)] == [("D001", 3)]


def test_string_built_sql_in_application_code():
    code = "\n".join([
        'cur.execute(f"SELECT * FROM t WHERE id={x}")',            # 1 f-string
        'cur.execute("SELECT * FROM t WHERE id=" + x)',            # 2 concatenation
        'cur.execute("SELECT * FROM t WHERE id=%s" % x)',          # 3 % formatting
        'cur.execute("SELECT * FROM t WHERE id={}".format(x))',    # 4 .format
        'cur.execute("SELECT * FROM t WHERE id=?", (x,))',         # 5 parameterised: safe
        'print("hello " + name)',                                   # 6 not SQL
    ])
    assert [f["line"] for f in sql_lint.scan_code(code)] == [1, 2, 3, 4]


def test_cli_exit_codes_and_help(capsys):
    assert sql_lint.main(["--sql", "DELETE FROM a"]) == 1
    assert sql_lint.main(["--sql", "SELECT * FROM t"]) == 0          # WARN only
    assert sql_lint.main(["--sql", "SELECT id FROM t WHERE id = 1"]) == 0
    with pytest.raises(SystemExit) as e:
        sql_lint.main(["--help"])
    assert e.value.code == 0


# ================================================================ dml_preview: counts what WOULD happen, keeps nothing
@pytest.fixture
def db(tmp_path):
    path = str(tmp_path / "lab.db")
    c = sqlite3.connect(path)
    c.executescript("""
        CREATE TABLE results(id INTEGER PRIMARY KEY, lot TEXT, status TEXT);
        INSERT INTO results VALUES (1,'A','ok'),(2,'B','void'),(3,'C','void'),(4,'D',NULL);
        CREATE TABLE received(lot TEXT);  INSERT INTO received VALUES ('A'),(NULL);
    """)
    c.commit()
    c.close()
    return path


def count(path, sql="SELECT COUNT(*) FROM results"):
    c = sqlite3.connect(path)
    try:
        return c.execute(sql).fetchone()[0]
    finally:
        c.close()


def test_preview_counts_rows_and_never_commits(db):
    res = dml_preview.preview(db, "DELETE FROM results WHERE status = 'void'")
    assert (res["total_rows"], res["matched_by_where"], res["affected_if_run"]) == (4, 2, 2)  # HAND: ids 2 and 3
    assert res["flags"] == [] and res["committed"] is False and res["db_unchanged"] is True
    assert count(db) == 4                                    # the DELETE was rolled back


def test_preview_update_leaves_values_untouched(db):
    res = dml_preview.preview(db, "UPDATE results SET status = 'x' WHERE id = 1")
    assert res["affected_if_run"] == 1 and res["flags"] == []
    assert count(db, "SELECT status FROM results WHERE id = 1") == "ok"


def test_preview_zero_rows_exposes_not_in_null(db):
    bad = dml_preview.preview(db, "DELETE FROM results WHERE lot NOT IN (SELECT lot FROM received)")
    # HAND: received = {'A', NULL}; every lot is either 'A' (FALSE) or compared with NULL (UNKNOWN) -> 0 rows, silently
    assert bad["affected_if_run"] == 0 and any(f.startswith("ZERO-ROWS") for f in bad["flags"])
    good = dml_preview.preview(
        db, "DELETE FROM results WHERE NOT EXISTS (SELECT 1 FROM received r WHERE r.lot = results.lot)")
    assert good["affected_if_run"] == 3                       # lots B, C, D are not received


def test_preview_flags_no_where_all_rows_and_more_than_expected(db):
    r = dml_preview.preview(db, "UPDATE results SET status = 'x'")
    assert r["affected_if_run"] == 4 and any(f.startswith("NO-WHERE") for f in r["flags"])
    r = dml_preview.preview(db, "DELETE FROM results WHERE id > 0")
    assert any(f.startswith("ALL-ROWS") for f in r["flags"])
    r = dml_preview.preview(db, "DELETE FROM results WHERE status = 'void'", max_expected=1)
    assert any(f.startswith("MORE-THAN-EXPECTED") for f in r["flags"])


def test_preview_refuses_select_and_multiple_statements(db):
    with pytest.raises(dml_preview.PreviewError):
        dml_preview.preview(db, "SELECT * FROM results")
    with pytest.raises(dml_preview.PreviewError):
        dml_preview.preview(db, "DELETE FROM results WHERE id = 1; DELETE FROM results")


def test_preview_cli_exit_codes(db, capsys):
    assert dml_preview.main([db, "DELETE FROM results WHERE id = 1"]) == 0
    assert dml_preview.main([db, "DELETE FROM results"]) == 1
    assert dml_preview.main([db, "SELECT 1"]) == 2
    out = capsys.readouterr().out
    assert "NOTHING WAS COMMITTED" in out
    with pytest.raises(SystemExit) as e:
        dml_preview.main(["--help"])
    assert e.value.code == 0


# ================================================================ must-fail controls (trap injected -> oracle must go red)
def test_must_fail_control_where_in_subquery_counts_as_where(monkeypatch, con):
    """Trap: 'there is a WHERE somewhere in the text, so it is safe'. The subquery-WHERE oracle must go red."""
    monkeypatch.setattr(sql_lint, "has_top_level", lambda kw, text: kw.upper() in text.upper())
    with pytest.raises(AssertionError):
        test_where_inside_a_subquery_is_not_a_where_clause(con)


def test_must_fail_control_preview_that_commits(monkeypatch, db):
    """Trap: 'preview' by actually running the statement and committing. The untouched-database oracle must go red."""
    monkeypatch.setattr(dml_preview, "finish", lambda conn: conn.execute("COMMIT"))
    with pytest.raises(AssertionError):
        test_preview_counts_rows_and_never_commits(db)


def test_must_fail_control_keywords_read_inside_comments(monkeypatch):
    """Trap: lint raw text without masking comments/strings. The comment/string oracle must go red."""
    monkeypatch.setattr(sql_lint, "mask", lambda s: s)
    with pytest.raises(AssertionError):
        test_keywords_in_comments_and_strings_do_not_fire()
