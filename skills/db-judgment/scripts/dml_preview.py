#!/usr/bin/env python3
"""dml_preview - run the db-judgment iron rule: preview the rows an UPDATE/DELETE will hit, inside a transaction, then roll back.

Black-box tool (SQLite only, standard library). Run `--help` first; do not read the source unless a run fails.
Given a SQLite file and ONE UPDATE or DELETE statement it prints
  - the equivalent SELECT (copy it and eyeball the rows),
  - total rows in the table, rows the WHERE matches, a sample of them,
  - the rowcount the real statement reports when executed inside BEGIN ... ROLLBACK (nothing is ever committed),
  - flags: NO-WHERE, ALL-ROWS, ZERO-ROWS (typical symptom of NOT IN + NULL, wrong key, trailing spaces),
          MORE-THAN-EXPECTED (--max-expected N), COUNT-MISMATCH (triggers/cascades or a WHERE the preview cannot reproduce).

Examples
  python dml_preview.py lab.db "DELETE FROM results WHERE status = 'void'" --max-expected 20
  python dml_preview.py lab.db "UPDATE stock SET qty = 0 WHERE lot NOT IN (SELECT lot FROM received)"
Exit code 0 = no flags, 1 = at least one flag, 2 = could not parse / run.
ADVISORY: a clean preview does not replace a backup, a staging run and review by the data owner before the real statement.
"""
import argparse
import json
import re
import sqlite3
import sys

import sql_lint

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ADVISORY = "ADVISORY: a clean preview does not replace a backup, a staging run and review by the data owner before the real statement."
IDENT = re.compile(r'^[\w."`\[\]]+$')


class PreviewError(Exception):
    pass


def parse_dml(sql):
    """-> (verb, table, where_text_or_None) for a single UPDATE / DELETE statement."""
    text = sql.strip().rstrip(";")
    masked = sql_lint.mask(text)
    if len(sql_lint.split_statements(masked)) != 1:
        raise PreviewError("give exactly one statement")
    verb, _ = sql_lint.statement_verb(masked)
    if verb == "DELETE":
        m = re.search(r"\bDELETE\s+FROM\s+([^\s(]+)", masked, re.I)
    elif verb == "UPDATE":
        m = re.search(r"\bUPDATE\s+(?:OR\s+\w+\s+)?([^\s(]+)\s+SET\b", masked, re.I)
    else:
        raise PreviewError("only UPDATE / DELETE are previewed (found %r)" % verb)
    if not m or not IDENT.match(text[m.start(1):m.end(1)]):
        raise PreviewError("could not read the table name")
    table = text[m.start(1):m.end(1)]
    dm = sql_lint.depth_map(masked)
    wpos = next((w.end() for w in re.finditer(r"\bWHERE\b", masked, re.I) if dm[w.start()] == 0), None)
    return verb, table, (text[wpos:].strip() if wpos is not None else None)


def finish(conn):
    """End the preview transaction WITHOUT keeping anything."""
    conn.execute("ROLLBACK")


def preview(db_path, sql, sample=5, max_expected=None):
    verb, table, where = parse_dml(sql)
    conn = sqlite3.connect(db_path, isolation_level=None)  # autocommit; we control BEGIN/ROLLBACK ourselves
    try:
        total = conn.execute("SELECT COUNT(*) FROM %s" % table).fetchone()[0]
        select = "SELECT * FROM %s%s" % (table, " WHERE " + where if where else "")
        matched = conn.execute("SELECT COUNT(*) FROM (%s)" % select).fetchone()[0]
        rows = conn.execute(select + " LIMIT %d" % sample).fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM %s LIMIT 0" % table).description]
        conn.execute("BEGIN")
        try:
            affected = conn.execute(sql.strip().rstrip(";")).rowcount
        finally:
            finish(conn)
        after = conn.execute("SELECT COUNT(*) FROM %s" % table).fetchone()[0]
    except sqlite3.Error as e:
        raise PreviewError("sqlite error: %s" % e)
    finally:
        conn.close()
    flags = []
    if where is None:
        flags.append("NO-WHERE: the statement hits ALL %d rows" % total)
    elif total and affected == total:
        flags.append("ALL-ROWS: the WHERE matched every one of the %d rows" % total)
    if affected == 0:
        flags.append("ZERO-ROWS: nothing would change - check NOT IN with NULL (use NOT EXISTS), the key, case, trailing spaces")
    if max_expected is not None and affected > max_expected:
        flags.append("MORE-THAN-EXPECTED: %d rows > the %d you expected" % (affected, max_expected))
    if affected != matched:
        flags.append("COUNT-MISMATCH: preview SELECT matched %d but the statement reports %d (triggers/cascades or a WHERE the SELECT cannot reproduce)" % (matched, affected))
    return {"statement": sql.strip(), "verb": verb, "table": table, "preview_select": select, "total_rows": total,
            "matched_by_where": matched, "affected_if_run": affected, "sample_columns": cols,
            "sample_rows": [list(r) for r in rows], "rows_after_rollback": after, "committed": False,
            "db_unchanged": after == total, "flags": flags}


def render(res):
    L = ["statement : " + res["statement"], "preview   : " + res["preview_select"] + ";",
         "table %s has %d rows; WHERE matches %d; the statement reports %d affected" % (
             res["table"], res["total_rows"], res["matched_by_where"], res["affected_if_run"]),
         "sample (%s):" % ", ".join(res["sample_columns"])]
    L += ["  " + str(r) for r in res["sample_rows"]] or ["  (none)"]
    L.append("NOTHING WAS COMMITTED (rolled back; rows after = %d)" % res["rows_after_rollback"])
    L += ["FLAG: " + f for f in res["flags"]]
    if not res["flags"]:
        L.append("no flags - now read the sample rows above before running the statement for real")
    L.append(ADVISORY)
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("db", help="SQLite database file")
    ap.add_argument("sql", help="ONE UPDATE or DELETE statement")
    ap.add_argument("--sample", type=int, default=5)
    ap.add_argument("--max-expected", type=int, default=None, help="rows you expect to touch; more is flagged")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        res = preview(a.db, a.sql, a.sample, a.max_expected)
    except PreviewError as e:
        print("ERROR: %s" % e)
        return 2
    print(json.dumps(res, ensure_ascii=False, indent=1, default=str) if a.json else render(res))
    return 1 if res["flags"] else 0


if __name__ == "__main__":
    sys.exit(main())
