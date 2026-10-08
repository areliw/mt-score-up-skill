#!/usr/bin/env python3
"""sql_lint - static check of SQL text for the traps listed in db-judgment (heuristic, not a parser).

Black-box tool: run `--help` first; do not read the source unless a run fails. Comments and string literals are
masked before matching, so a keyword inside 'text' or -- a comment never fires. Rules (id, severity):
  D001 ERROR UPDATE/DELETE with no top-level WHERE            (a WHERE inside a subquery does not count)
  D002 ERROR NOT IN (subquery) or NOT IN (... NULL ...)        (one NULL makes every row UNKNOWN -> 0 rows, silently)
  D003 WARN  SELECT * / t.*                                    (pulls everything, breaks on schema change)
  D004 ERROR JOIN with no ON/USING                             (cartesian product, m x n rows)
  D005 WARN  comma join  FROM a, b                             (the join condition hides in WHERE; forget it = cartesian)
  D006 WARN  UNION without ALL                                 (sort + dedup cost; default to UNION ALL)
  D007 WARN  deep OFFSET (>= --offset-warn, default 10000)     (scans and discards that many rows; use keyset pagination)
  D008 INFO  COUNT(...) in a query with JOIN, no DISTINCT      (counts joined rows, not entities)
  D009 ERROR = NULL / <> NULL / != NULL in a condition         (always UNKNOWN; use IS [NOT] NULL; "SET x = NULL" is fine)
  D012 WARN  (--code) SQL built by f-string / + / % / .format  (injection; use parameters)
Not checked (needs a real parser): GROUP BY completeness, index choice, normalisation level.
--offset-warn is a screening heuristic; a flag means "read this line", not "this is wrong".

Examples
  python sql_lint.py query.sql
  python sql_lint.py --sql "DELETE FROM lab WHERE id NOT IN (SELECT id FROM done)"
  python sql_lint.py --code app.py          # scan application source for string-built SQL
  cat migration.sql | python sql_lint.py -     # exit code 1 when any ERROR is found
ADVISORY: heuristic lint only - test on staging with a backup, and run dml_preview.py before any UPDATE/DELETE.
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

ADVISORY = "ADVISORY: heuristic lint only - test on staging with a backup, and run dml_preview.py before any UPDATE/DELETE."
CLAUSE_END = r"(?=\b(?:WHERE|GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|UNION|INTERSECT|EXCEPT)\b|;|$)"


def mask(sql):
    """Blank out comments and string-literal contents, keeping length and newlines so offsets still map to lines."""
    out = []
    i, n = 0, len(sql)
    while i < n:
        ch = sql[i]
        if sql.startswith("--", i):
            j = sql.find("\n", i)
            j = n if j == -1 else j
            out.append(" " * (j - i))
            i = j
        elif sql.startswith("/*", i):
            j = sql.find("*/", i + 2)
            j = n if j == -1 else j + 2
            out.append("".join("\n" if c == "\n" else " " for c in sql[i:j]))
            i = j
        elif ch in ("'", '"', "`"):
            q = ch
            j = i + 1
            while j < n:
                if sql[j] == q:
                    if j + 1 < n and sql[j + 1] == q:  # doubled quote = escaped
                        j += 2
                        continue
                    break
                j += 1
            seg = sql[i + 1:j]
            out.append(q + "".join("\n" if c == "\n" else "_" for c in seg) + (q if j < n else ""))
            i = j + 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def split_statements(masked):
    """[(start_offset, text)] split on ';' (strings and comments are already blanked)."""
    res, start = [], 0
    for m in re.finditer(";", masked):
        res.append((start, masked[start:m.start()]))
        start = m.end()
    res.append((start, masked[start:]))
    return [(s, t) for s, t in res if t.strip()]


def depth_map(text):
    d, depth = [], 0
    for ch in text:
        if ch == ")":
            depth -= 1
        d.append(depth)
        if ch == "(":
            depth += 1
    return d


def has_top_level(keyword, text):
    """True when `keyword` appears at parenthesis depth 0 (so WHERE inside a subquery does not count)."""
    dm = depth_map(text)
    return any(dm[m.start()] == 0 for m in re.finditer(r"\b%s\b" % keyword, text, re.I))


def statement_verb(text):
    """First depth-0 keyword among the DML/DDL verbs (skips a leading WITH ... CTE block)."""
    dm = depth_map(text)
    for m in re.finditer(r"\b(SELECT|INSERT|UPDATE|DELETE|MERGE|REPLACE|TRUNCATE|CREATE|DROP|ALTER)\b", text, re.I):
        if dm[m.start()] == 0:
            return m.group(1).upper(), m.start()
    return "", 0


def line_of(masked, offset):
    return masked.count("\n", 0, offset) + 1


def lint(sql, offset_warn=10000):
    masked = mask(sql)
    findings = []

    def add(sev, rule, off, msg, fix):
        findings.append({"severity": sev, "rule": rule, "line": line_of(masked, off), "message": msg, "fix": fix})

    for start, st in split_statements(masked):
        norm = st
        verb, verb_off = statement_verb(norm)
        at = lambda m: start + m.start()  # noqa: E731
        if verb in ("UPDATE", "DELETE") and not has_top_level("WHERE", norm):
            add("ERROR", "D001", start + verb_off, "%s without a top-level WHERE touches EVERY row" % verb,
                "write the WHERE first, run it as SELECT COUNT(*) to see the rows, wrap the statement in a transaction")
        for m in re.finditer(r"\bNOT\s+IN\s*\(\s*(SELECT\b|[^)]*\bNULL\b)", norm, re.I):
            add("ERROR", "D002", at(m), "NOT IN with a subquery/NULL: one NULL in the list makes every comparison UNKNOWN, so the "
                "query/DELETE returns 0 rows without an error", "use NOT EXISTS (correlated) and confirm the row count with a SELECT preview")
        for m in re.finditer(r"\bSELECT\s+(?:DISTINCT\s+)?\*|,\s*\*|\b\w+\.\*", norm, re.I):
            add("WARN", "D003", at(m), "SELECT * / t.* pulls every column", "list the columns you need")
        joins = list(re.finditer(r"\b(CROSS\s+|NATURAL\s+)?(?:(?:INNER|LEFT|RIGHT|FULL)(?:\s+OUTER)?\s+)?JOIN\b", norm, re.I))
        for k, m in enumerate(joins):
            if m.group(1):
                continue
            end = joins[k + 1].start() if k + 1 < len(joins) else len(norm)
            seg = norm[m.end():end]
            cut = re.search(r"\b(WHERE|GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|UNION)\b", seg, re.I)
            seg = seg[:cut.start()] if cut else seg
            if not re.search(r"\b(ON|USING)\b", seg, re.I):
                add("ERROR", "D004", at(m), "JOIN without ON/USING = cartesian product (m x n rows)", "add the join condition")
        for m in re.finditer(r"\bFROM\s+[\w.\"`]+(?:\s+(?:AS\s+)?\w+)?\s*,\s*[\w.\"`]+", norm, re.I):
            add("WARN", "D005", at(m), "old-style comma join: the join condition lives in WHERE and is easy to forget (cartesian product)",
                "use JOIN ... ON ...")
        for m in re.finditer(r"\bUNION\b(?!\s+ALL\b)", norm, re.I):
            add("WARN", "D006", at(m), "UNION sorts and removes duplicates (extra cost)", "use UNION ALL unless you really need de-duplication")
        for m in re.finditer(r"\bOFFSET\s+(\d+)", norm, re.I):
            if int(m.group(1)) >= offset_warn:
                add("WARN", "D007", at(m), "OFFSET %s scans and throws away that many rows" % m.group(1), "keyset pagination: WHERE id > :last_id ORDER BY id LIMIT n")
        for m in re.finditer(r"\bLIMIT\s+(\d+)\s*,\s*\d+", norm, re.I):
            if int(m.group(1)) >= offset_warn:
                add("WARN", "D007", at(m), "LIMIT %s,n is a deep offset" % m.group(1), "keyset pagination: WHERE id > :last_id ORDER BY id LIMIT n")
        if joins and verb == "SELECT":
            for m in re.finditer(r"\bCOUNT\s*\(\s*(?!DISTINCT\b)", norm, re.I):
                add("INFO", "D008", at(m), "COUNT after JOIN counts joined rows; one entity with 2 matches is counted twice",
                    "COUNT(DISTINCT key), or aggregate before joining")
        cond = re.search(r"\b(WHERE|HAVING|ON|WHEN)\b", norm, re.I)
        if cond:
            for m in re.finditer(r"(=|<>|!=)\s*NULL\b", norm[cond.start():], re.I):
                add("ERROR", "D009", start + cond.start() + m.start(), "comparison with NULL using %s is always UNKNOWN (never true)" % m.group(1),
                    "use IS NULL / IS NOT NULL")
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    return sorted(findings, key=lambda f: (f["line"], order[f["severity"]], f["rule"]))


def scan_code(text):
    """D012: application source that assembles SQL from strings (f-string, +, %, .format, JS template)."""
    findings = []
    sqlish = re.compile(r"""["'`][^"'`]*\b(?:SELECT|INSERT\s+INTO|UPDATE|DELETE\s+FROM)\b""", re.I)
    for i, line in enumerate(text.splitlines(), 1):
        if not sqlish.search(line):
            continue
        reasons = []
        if re.search(r"""\bf["'][^"']*\{""", line):
            reasons.append("f-string interpolation")
        if re.search(r"""["']\s*\+\s*[\w(]|[\w)]\s*\+\s*["']""", line):
            reasons.append("string concatenation")
        if re.search(r"""["']\s*%\s*[\w(]""", line):
            reasons.append("% formatting")
        if ".format(" in line:
            reasons.append(".format()")
        if "${" in line:
            reasons.append("template-literal interpolation")
        if reasons:
            findings.append({"severity": "WARN", "rule": "D012", "line": i, "message": "SQL assembled with " + ", ".join(reasons),
                             "fix": "pass values as parameters (execute(sql, params)); never format them into the text"})
    return findings


def render(findings):
    if not findings:
        return "no findings\n" + ADVISORY
    L = ["line %-4d %-5s %s  %s\n          fix: %s" % (f["line"], f["severity"], f["rule"], f["message"], f["fix"]) for f in findings]
    n_err = sum(1 for f in findings if f["severity"] == "ERROR")
    L.append("summary: %d ERROR, %d WARN, %d INFO" % (n_err, sum(1 for f in findings if f["severity"] == "WARN"),
                                                       sum(1 for f in findings if f["severity"] == "INFO")))
    L.append(ADVISORY)
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="SQL file, or - for stdin")
    ap.add_argument("--sql", help="SQL text on the command line")
    ap.add_argument("--code", action="store_true", help="treat input as application source and look for string-built SQL (D012)")
    ap.add_argument("--offset-warn", type=int, default=10000)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.sql is not None:
        text = a.sql
    elif a.file == "-":
        text = sys.stdin.read()
    elif a.file:
        with open(a.file, encoding="utf-8-sig") as f:
            text = f.read()
    else:
        ap.error("give a file, - for stdin, or --sql")
    findings = scan_code(text) if a.code else lint(text, a.offset_warn)
    if a.json:
        print(json.dumps(findings, ensure_ascii=False, indent=1))
    else:
        print(render(findings))
    return 1 if any(f["severity"] == "ERROR" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
