#!/usr/bin/env python3
"""sheet_audit - find the silent spreadsheet damage db/spreadsheet-judgment warns about, in a CSV, BEFORE it is opened in Excel/Sheets.

Black-box tool: run `--help` first; do not read the source unless a run fails. It reads the CSV as plain text (csv
module, nothing is converted) and reports, with row/column coordinates:
  A001 cells Excel will auto-convert (the data is destroyed on open/paste, often with no warning)
       leading-zero    000123 -> 123           (sample codes, barcodes, ID numbers)
       long-digits     16+ digits -> only 15 significant digits survive (rest become 0)
       gene-date       SEPT2 -> 2-Sep, MARCH1 -> 1-Mar, DEC1 -> 1-Dec   (Ziemann et al. 2016, Genome Biol 17:177)
       date-like       1-2, 3/4, 12/5/2020 -> a date or fraction
       sci-notation    12E3 -> 12000
  A002 text mixed into a numeric column ("6.1 mg/dL", "<5") - arithmetic silently skips those cells
  A003 header problems: blank or duplicate column names (merged-cell leftovers)
  A004 layout that breaks "1 row = 1 record": blank rows, rows with a single filled cell (group/subtotal rows),
       blank key cells under a filled cell (vertically merged cells)
  A005 cells that ALREADY look converted (e.g. 2-Sep in a column of gene symbols): the original value may be lost
Fix for A001: format the column as Text BEFORE paste/import (Data > From Text/CSV > set type Text), never open the CSV by double-click.
Not checked: formulas, absolute references, hard-coded cut-offs (they live in the workbook, not in a CSV).

Examples
  python sheet_audit.py samples.csv
  python sheet_audit.py samples.csv --json
Exit code 1 when any ERROR is found.
ADVISORY: heuristic screen - open the flagged cells yourself; patient files fall under PDPA (code the IDs, never share an open link).
"""
import argparse
import csv
import json
import re
import sys
from collections import Counter

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ADVISORY = "ADVISORY: heuristic screen - open the flagged cells yourself; patient files fall under PDPA (code the IDs, never share an open link)."
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
GENE_DATE = re.compile(r"^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEPT|SEP|OCT|NOV|DEC|MARCH)[-]?(\d{1,2})$", re.I)
CONVERTED = re.compile(r"^(\d{1,2})-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$", re.I)
NUMBER = re.compile(r"^[+-]?\d+(\.\d+)?$")
NUM_UNIT = re.compile(r"^[+-]?\d+(\.\d+)?\s*[A-Za-zµ%/][\w/%.^µ-]*$")
CENSORED = re.compile(r"^[<>≤≥]=?\s*\d")


def valid_day_month(a, b):
    """True when a/b can be read as day/month or month/day (so Excel turns it into a date)."""
    return (1 <= a <= 12 and 1 <= b <= 31) or (1 <= a <= 31 and 1 <= b <= 12)


def cell_risks(v):
    """[(kind, message, would_become)] for one raw cell text."""
    s = v.strip()
    out = []
    if re.fullmatch(r"0\d+", s):
        out.append(("leading-zero", "leading zero(s) are dropped when Excel reads the cell as a number", str(int(s))))
    if re.fullmatch(r"\d{16,}", s):
        out.append(("long-digits", "only 15 significant digits are kept; later digits become 0", s[:15] + "0" * (len(s) - 15)))
    m = GENE_DATE.match(s)
    if m and 1 <= int(m.group(2)) <= 31:
        mon = m.group(1).upper()[:3]
        out.append(("gene-date", "read as a date (gene symbols like SEPT2 / MARCH1 / DEC1 are classic victims)", "%d-%s" % (int(m.group(2)), mon.capitalize())))
    m = re.fullmatch(r"(\d{1,2})[-/](\d{1,2})([-/]\d{2,4})?", s)
    if m and valid_day_month(int(m.group(1)), int(m.group(2))):
        out.append(("date-like", "read as a date or fraction", "a date serial number"))
    if re.fullmatch(r"\d+[eE][+-]?\d+", s):
        out.append(("sci-notation", "read as scientific notation", "%g" % float(s)))
    return out


def audit(rows):
    """rows: list of lists (first row = header). Returns findings."""
    findings = []

    def add(sev, rule, kind, row, col, msg, extra=None):
        d = {"severity": sev, "rule": rule, "kind": kind, "row": row, "column": col, "message": msg}
        if extra:
            d["would_become"] = extra
        findings.append(d)

    if not rows:
        return findings
    header = rows[0]
    body = rows[1:]
    width = len(header)
    # ---- A003 headers
    for j, h in enumerate(header):
        if not h.strip():
            add("ERROR", "A003", "blank-header", 1, "col %d" % (j + 1), "blank column name (merged-cell leftover?) - every column needs one name")
    for name, c in Counter(h.strip() for h in header if h.strip()).items():
        if c > 1:
            add("ERROR", "A003", "duplicate-header", 1, name, "column name %r appears %d times" % (name, c))
    names = [h.strip() or "col %d" % (j + 1) for j, h in enumerate(header)]
    # ---- A001 / A005 per cell
    for i, r in enumerate(body, start=2):
        for j, v in enumerate(r[:width]):
            for kind, msg, becomes in cell_risks(v):
                add("ERROR" if kind in ("leading-zero", "gene-date", "long-digits") else "WARN", "A001", kind, i, names[j],
                    "%r: %s" % (v, msg), becomes)
    for j in range(width):
        col = [r[j].strip() for r in body if j < len(r) and r[j].strip()]
        if not col:
            continue
        conv = [c for c in col if CONVERTED.match(c)]
        if conv and len(conv) < len(col):
            add("WARN", "A005", "already-converted", "-", names[j],
                "%d cell(s) look like Excel-converted dates (%s) among non-date text: if this column holds symbols/codes the original is lost"
                % (len(conv), ", ".join(conv[:3])))
        # ---- A002 mixed text in a numeric column
        nums = [c for c in col if NUMBER.match(c)]
        mixed = [c for c in col if NUM_UNIT.match(c) or CENSORED.match(c)]
        if nums and mixed and len(nums) + len(mixed) == len(col):
            add("WARN", "A002", "unit-or-flag-in-value", "-", names[j],
                "%d numeric and %d number+text cell(s) (%s): text cells are skipped silently by SUM/AVERAGE/STDEV - split value / unit / flag columns"
                % (len(nums), len(mixed), ", ".join(mixed[:3])))
    # ---- A004 layout
    for i, r in enumerate(body, start=2):
        filled = [c for c in r if c.strip()]
        if not filled:
            add("WARN", "A004", "blank-row", i, "-", "completely blank row inside the table")
        elif width >= 3 and len(filled) == 1 and r and r[0].strip():
            add("WARN", "A004", "single-cell-row", i, names[0], "only the first cell is filled (%r): a group/subtotal/merged heading row breaks 1 row = 1 record" % r[0].strip())
    if body and width >= 2:
        blank_keys = [i for i, r in enumerate(body, start=2) if r and not r[0].strip() and any(c.strip() for c in r[1:])]
        if blank_keys and len(blank_keys) < len(body):
            add("WARN", "A004", "blank-key-cell", blank_keys[0], names[0],
                "%d row(s) have data but an empty first column (rows %s...): vertically merged cells export like this - fill the key down on every row"
                % (len(blank_keys), ", ".join(map(str, blank_keys[:4]))))
    return findings


def render(findings):
    if not findings:
        return "no findings\n" + ADVISORY
    L = []
    for f in findings:
        tail = "  -> Excel would show %s" % f["would_become"] if "would_become" in f else ""
        L.append("%-5s %s %-18s row %-4s col %-16s %s%s" % (f["severity"], f["rule"], f["kind"], f["row"], f["column"], f["message"], tail))
    n_err = sum(1 for f in findings if f["severity"] == "ERROR")
    L.append("summary: %d ERROR, %d WARN" % (n_err, len(findings) - n_err))
    L.append(ADVISORY)
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    with open(a.file, encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.reader(f)]
    findings = audit(rows)
    print(json.dumps(findings, ensure_ascii=False, indent=1) if a.json else render(findings))
    return 1 if any(f["severity"] == "ERROR" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
