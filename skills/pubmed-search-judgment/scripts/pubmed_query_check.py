#!/usr/bin/env python3
"""pubmed_query_check - syntax + shape checker for a PubMed query (field tags, Boolean grouping, the card's traps).

Black-box tool for pubmed-search-judgment. Run `--help` first; you do not need to read the source.
It never contacts PubMed: it checks that the query is well formed and that it does not fall into the traps the card
warns about. Result COUNTS must come from the PubMed screen (the card's rule: never fill a number by guessing).

Rules checked
  well-formed      balanced ( ) [ ] " ; no empty group, leading/trailing/double operator; implicit AND between groups
  Boolean case     AND / OR / NOT must be uppercase (PubMed User Guide, fetched 2026-10-08); lowercase = ordinary words
  grouping         OR inside a concept (synonyms), AND between concepts. AND and OR at the same level without ( ) is an
                   error because PubMed evaluates strictly left to right (User Guide, 2026-10-08)
  concepts         "usually 2-3" concepts (card rule 1): > 3 is a warning
  field tags       card set [tiab] [mh] [majr] [pt] [dp] [la] [au] [ti] + the other tags in PubMed Help; unknown tag = warning
  MeSH only        a concept with MeSH and no keyword misses records not yet indexed (card Fork 1 VERDICT)
  [majr]           central-topic only: may drop relevant papers; with [ti] it is too tight (card Forks 1, 3)
  UK / US spelling anemia/anaemia, leukemia/leukaemia, thalassemia/thalassaemia, pediatric/paediatric: a keyword
                   concept needs both (card Fork 3 and Anti-patterns). MeSH terms cover both spellings
  whole sentence   a long phrase with no operator and no tag (card Anti-pattern)
  date             2020:2026[dp] - start year must not be after the end year
  RCT-only filter  randomized controlled trial[pt] on a DIAGNOSTIC question (card Fork 2 VERDICT)

Examples
  python pubmed_query_check.py "(thalassemia[mh] OR thalassaemia[tiab]) AND (machine learning[tiab] OR deep learning[tiab])"
  python pubmed_query_check.py --file query.txt --question diagnostic --row --filters "2018:2026, Humans"
  python pubmed_query_check.py "..." --json
Exit code: 0 = no ERROR - 1 = at least one ERROR.
"""
import argparse
import datetime
import json
import re
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print some symbols and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

CARD_TAGS = {"tiab", "mh", "majr", "pt", "dp", "la", "au", "ti"}
OTHER_TAGS = {"mesh", "sh", "tw", "ad", "ta", "pmid", "all", "pdat", "edat", "crdt", "sb", "fau", "lastau", "auid", "gr", "nm", "ps", "jour", "tt"}
KEYWORD_TAGS = {"tiab", "tw", "all", "ti", None}
MESH_TAGS = {"mh", "mesh", "majr"}
SPELLINGS = [("anemi", "anaemi"), ("leukemi", "leukaemi"), ("thalassemi", "thalassaemi"), ("pediatric", "paediatric")]
DIAGNOSTIC = re.compile(r"sensitiv|specificit|diagnostic accuracy|predictive value|likelihood ratio|\broc\b|accuracy", re.I)
RCT = re.compile(r"randomi[sz]ed controlled trial|\brct\b", re.I)
MAX_CONCEPTS = 3          # card rule 1: "usually 2-3"
LONG_SENTENCE = 6         # words with no operator and no tag


# ---------------------------------------------------------------- tokenizer + parser
def tokenize(q):
    toks, i = [], 0
    while i < len(q):
        c = q[i]
        if c.isspace():
            i += 1
        elif c in "()":
            toks.append((c, c, i))
            i += 1
        elif c == "[":
            j = q.find("]", i)
            if j < 0:
                toks.append(("BADBRACKET", q[i:], i))
                break
            toks.append(("TAG", q[i + 1:j].strip().lower(), i))
            i = j + 1
        elif c == "]":
            toks.append(("BADBRACKET", "]", i))
            i += 1
        elif c == '"':
            j = q.find('"', i + 1)
            if j < 0:
                toks.append(("BADQUOTE", q[i:], i))
                break
            toks.append(("WORD", q[i:j + 1], i))
            i = j + 1
        else:
            j = i
            while j < len(q) and not q[j].isspace() and q[j] not in '()[]"':
                j += 1
            w = q[i:j]
            if w in ("AND", "OR", "NOT"):
                toks.append(("OP", w, i))
            elif w.lower() in ("and", "or", "not"):
                toks.append(("LOWOP", w, i))
            else:
                toks.append(("WORD", w, i))
            i = j
    return toks


class Parser:
    def __init__(self, toks, rep):
        self.t, self.p, self.rep = toks, 0, rep

    def peek(self):
        return self.t[self.p] if self.p < len(self.t) else (None, None, len(self.t))

    def parse_expr(self, depth):
        children, ops = [], []
        while True:
            kind, val, pos = self.peek()
            if kind == "OP":
                self.rep.add("ERROR", "an operator %s with nothing before it (leading or double operator)" % val, "well-formed")
                self.p += 1
                ops.append(val)
                continue
            child = self.parse_operand(depth)
            if child is None:
                break
            children.append(child)
            kind, val, pos = self.peek()
            if kind == "OP":
                ops.append(val)
                self.p += 1
                if self.peek()[0] in (None, ")"):
                    self.rep.add("ERROR", "the query ends with the operator %s" % val, "well-formed")
                    break
                continue
            if kind in ("(", "WORD", "LOWOP"):
                self.rep.add("WARN", "two groups next to each other with no operator (PubMed reads it as AND): write AND explicitly", "well-formed")
                ops.append("AND")
                continue
            break
        return {"type": "group", "ops": ops, "children": children}

    def parse_operand(self, depth):
        kind, val, pos = self.peek()
        if kind == "(":
            self.p += 1
            inner = self.parse_expr(depth + 1)
            if self.peek()[0] == ")":
                self.p += 1
            else:
                self.rep.add("ERROR", "unclosed '(' at position %d" % pos, "well-formed")
            if not inner["children"]:
                self.rep.add("ERROR", "empty parentheses at position %d" % pos, "well-formed")
            if self.peek()[0] == "TAG":
                self.rep.add("WARN", "a [tag] right after ')' does not tag the group: put the tag on each term", "field tags (card Fork 2 examples)")
                self.p += 1
            return inner
        if kind in ("WORD", "LOWOP"):
            words = []
            while self.peek()[0] in ("WORD", "LOWOP"):
                k, v, _ = self.peek()
                if k == "LOWOP":
                    self.rep.add("WARN", "lowercase '%s' is read as an ordinary word, not a Boolean operator: write %s" % (v, v.upper()), "Boolean case")
                words.append(v)
                self.p += 1
            tag = None
            if self.peek()[0] == "TAG":
                tag = self.peek()[1]
                self.p += 1
            return {"type": "term", "text": " ".join(words), "tag": tag}
        if kind == "TAG":
            self.rep.add("ERROR", "a [%s] tag with no term in front of it" % val, "well-formed")
            self.p += 1
            return self.parse_operand(depth)
        return None


class Report:
    def __init__(self):
        self.items = []

    def add(self, sev, msg, rule=""):
        self.items.append({"severity": sev, "message": msg, "rule": rule})

    def count(self, sev):
        return sum(1 for i in self.items if i["severity"] == sev)


def leaves(node):
    if node["type"] == "term":
        return [node]
    return [l for c in node["children"] for l in leaves(c)]


def walk(node):
    yield node
    if node["type"] == "group":
        for c in node["children"]:
            yield from walk(c)


# ---------------------------------------------------------------- checks
def check_tags(all_leaves, rep):
    for l in all_leaves:
        tag = l["tag"]
        if tag is not None and tag not in CARD_TAGS and tag not in OTHER_TAGS:
            rep.add("WARN", "unrecognised field tag [%s] on '%s': check PubMed Help (card tags: %s)" % (tag, l["text"], " ".join("[%s]" % t for t in sorted(CARD_TAGS))), "field tags")
        if tag == "dp":
            check_date(l["text"], rep)
    untagged = [l["text"] for l in all_leaves if l["tag"] is None]
    if untagged:
        rep.add("INFO", "untagged term(s): %s. Tag them ([mh] / [tiab]) so the search is exact and reproducible" % "; ".join(untagged[:6]), "field tags (card Fork 2)")


def check_date(text, rep):
    m = re.fullmatch(r"(\d{4})(?:/\d{2}(?:/\d{2})?)?(?::(\d{4})(?:/\d{2}(?:/\d{2})?)?)?", text)
    if not m:
        rep.add("ERROR", "date term '%s'[dp] is not YYYY or YYYY:YYYY (or YYYY/MM/DD)" % text, "date (card Fork 2: 2020:2026[dp])")
    elif m.group(2) and int(m.group(1)) > int(m.group(2)):
        rep.add("ERROR", "date range %s:%s runs backwards" % (m.group(1), m.group(2)), "date")


def check_grouping(root, rep):
    for node in walk(root):
        if node["type"] != "group":
            continue
        s = set(node["ops"])
        if "OR" in s and (s & {"AND", "NOT"}):
            rep.add("ERROR", "AND/OR/NOT mixed at one level without parentheses (%s): PubMed evaluates left to right, so group each synonym set with ( OR )" % " ".join(
                "%s" % o for o in node["ops"]), "grouping (card Fork 2)")


def concepts_of(root):
    if root["type"] == "group" and root["ops"] and set(root["ops"]) <= {"AND", "NOT"}:
        return root["children"]
    if root["type"] == "group" and len(root["children"]) == 1:
        return root["children"]
    return [root]


def check_concepts(root, rep, question):
    concepts = [c for c in concepts_of(root) if leaves(c)]
    n = len(concepts)
    if n > MAX_CONCEPTS:
        rep.add("WARN", "%d concepts joined by AND; the card says usually 2-3 (more concepts = silently dropped records). Drop the least necessary one" % n, "card rule 1")
    for i, c in enumerate(concepts, 1):
        ls = leaves(c)
        tags = {l["tag"] for l in ls}
        if tags and tags <= MESH_TAGS:
            rep.add("WARN", "concept %d (%s) is MeSH only: OR a keyword ([tiab]) too, recent or niche records may not be indexed yet" % (i, ls[0]["text"]),
                    "card Fork 1 VERDICT")
        if "majr" in tags:
            rep.add("WARN", "concept %d uses [majr]: precision up, but papers where this is not the central topic are lost" % i, "card Fork 1")
        elif tags and tags <= {"tiab", "tw", "all", "ti"} and len(ls) >= 1 and not (tags & MESH_TAGS):
            rep.add("INFO", "concept %d (%s) has keywords only: add its MeSH term with OR if one exists, so renamed or differently worded records are caught" % (i, ls[0]["text"]), "card Fork 1")
    return n


def check_spelling(all_leaves, rep):
    kw = [l["text"].lower() for l in all_leaves if l["tag"] in KEYWORD_TAGS]
    mesh = [l["text"].lower() for l in all_leaves if l["tag"] in MESH_TAGS]
    for us, uk in SPELLINGS:
        if any(us in t or uk in t for t in mesh):      # the card's own example pairs thalassemia[mh] with thalassaemia[tiab]
            continue
        has_us, has_uk = any(us in t for t in kw), any(uk in t for t in kw)
        if has_us != has_uk:
            have, miss = (us, uk) if has_us else (uk, us)
            rep.add("WARN", "keyword spelling '%s...' without '%s...': add the other spelling with OR (MeSH terms already cover both)" % (have, miss), "card Fork 3 / Anti-patterns")


def check_traps(all_leaves, rep, question):
    pts = [l for l in all_leaves if l["tag"] == "pt" and RCT.search(l["text"])]
    diag = question == "diagnostic" or (question == "auto" and any(DIAGNOSTIC.search(l["text"]) for l in all_leaves))
    if pts and diag:
        rep.add("ERROR", "randomized-controlled-trial filter on a DIAGNOSTIC-accuracy question: those studies are cross-sectional/cohort designs, so this filter drops the right papers", "card Fork 2 VERDICT")
    if any(l["tag"] == "majr" for l in all_leaves) and any(l["tag"] == "ti" for l in all_leaves):
        rep.add("WARN", "[majr] together with [ti] is very tight: 0-3 results are likely; use [tiab] and/or [mh]", "card Fork 3")
    if diag and not any(l["text"].lower().strip('"') in ("humans", "human") for l in all_leaves):
        rep.add("INFO", "diagnostic question: add the Humans filter (or Humans[mh]) to keep in-vitro/animal work out; note it only filters indexed records", "card Fork 2 / Anti-patterns")


def check_sentence(toks, rep):
    words = [t for t in toks if t[0] in ("WORD", "LOWOP")]
    structure = [t for t in toks if t[0] in ("OP", "TAG", "(", ")")]
    if len(words) >= LONG_SENTENCE and not structure:
        rep.add("ERROR", "the whole question typed as one sentence (%d words, no operators, no tags): split it into 2-3 concepts, each with MeSH + synonyms joined by OR" % len(words),
                "card rule 1 / Anti-patterns")


def balance(q, rep):
    if q.count("(") != q.count(")"):
        rep.add("ERROR", "parentheses are not balanced: %d '(' vs %d ')'" % (q.count("("), q.count(")")), "well-formed")
    if q.count("[") != q.count("]"):
        rep.add("ERROR", "square brackets are not balanced: %d '[' vs %d ']'" % (q.count("["), q.count("]")), "well-formed")
    if q.count('"') % 2:
        rep.add("ERROR", "an odd number of double quotes", "well-formed")


def run(query, question="auto"):
    rep = Report()
    q = query.strip()
    if not q:
        rep.add("ERROR", "empty query", "well-formed")
        return rep, None
    balance(q, rep)
    toks = tokenize(q)
    for k, v, pos in toks:
        if k == "BADBRACKET":
            rep.add("ERROR", "stray or unclosed '[' / ']' at position %d" % pos, "well-formed")
        if k == "BADQUOTE":
            rep.add("ERROR", "unclosed double quote at position %d" % pos, "well-formed")
    check_sentence(toks, rep)
    parser = Parser([t for t in toks if t[0] not in ("BADBRACKET", "BADQUOTE")], rep)
    root = parser.parse_expr(0)
    while parser.peek()[0] == ")":
        rep.add("ERROR", "unmatched ')' at position %d" % parser.peek()[2], "well-formed")
        parser.p += 1
        extra = parser.parse_expr(0)
        root["children"] += extra["children"]
        root["ops"] += ["AND"] * len(extra["children"])
    all_leaves = leaves(root)
    check_tags(all_leaves, rep)
    check_grouping(root, rep)
    n = check_concepts(root, rep, question)
    check_spelling(all_leaves, rep)
    check_traps(all_leaves, rep, question)
    rep.concepts = [{"terms": [("%s[%s]" % (l["text"], l["tag"]) if l["tag"] else l["text"]) for l in leaves(c)]} for c in concepts_of(root) if leaves(c)]
    return rep, root


def log_row(query, filters, date):
    return "| %s | `%s` | %s | (เปิดดูจริง) |" % (date, query.strip(), filters or "-")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="?", help="the PubMed query (quote it); or use --file")
    ap.add_argument("--file", help="read the query from a UTF-8 text file")
    ap.add_argument("--question", choices=["auto", "diagnostic", "treatment", "other"], default="auto",
                    help="kind of clinical question (auto guesses 'diagnostic' from sensitivity/specificity/accuracy words)")
    ap.add_argument("--row", action="store_true", help="also print the Fork 5 reproducibility row (date | query | filters | results left for you to read off PubMed)")
    ap.add_argument("--filters", default="", help="filters you ticked in PubMed, for the --row line (e.g. '2018:2026, Humans')")
    ap.add_argument("--date", default="", help="search date for --row (default: today)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args(argv)
    if a.file:
        with open(a.file, encoding="utf-8-sig") as f:
            query = " ".join(f.read().split())
    elif a.query:
        query = a.query
    else:
        ap.error("give a query or --file")
    rep, _ = run(query, a.question)
    out = {"errors": rep.count("ERROR"), "warnings": rep.count("WARN"), "query": query,
           "concepts": getattr(rep, "concepts", []), "findings": rep.items}
    if a.row:
        out["log_row"] = log_row(query, a.filters, a.date or datetime.date.today().isoformat())
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        for i, c in enumerate(out["concepts"], 1):
            print("CONCEPT %d: %s" % (i, "  OR  ".join(c["terms"])))
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        for it in sorted(rep.items, key=lambda x: order[x["severity"]]):
            print("%-5s %s%s" % (it["severity"], it["message"], ("  [" + it["rule"] + "]") if it["rule"] else ""))
        print("RESULT: %d error(s), %d warning(s)" % (out["errors"], out["warnings"]))
        if a.row:
            print("LOG ROW (card Fork 5; fill the result count from the PubMed screen, never from a guess):")
            print("| date | query | filters | results |")
            print(out["log_row"])
        print("ADVISORY: syntax and shape check only; PubMed was not searched. Open the results and verify every citation "
              "(PMID, title, abstract) before citing; abstracts are for screening, numbers come from the full text.")
    return 1 if out["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
