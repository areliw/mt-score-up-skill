#!/usr/bin/env python3
"""claim_check - flag checkable claims in an AI answer that carry no source / confidence tag.

Black-box tool for anti-hallucination. Run --help first; read the source only if a check fails.
It does NOT know whether a claim is true. It only enforces the card's mechanical rules:
  * every number with a unit, every percentage, every year  = a claim a human must be able to check
    -> needs a source tag / identifier in the SAME sentence, otherwise FLAG
  * a medical value labelled only "from memory / estimate / unsure" is honest but not usable
    -> CHECK (open the authoritative source before use)
  * every DOI / PMID / arXiv id = something for a person to OPEN. A well-formed id is NOT proof it
    exists (a fabricated citation can be perfectly formed) -> always CHECK, never "OK"
  * a malformed DOI -> FLAG (cannot be opened at all)
  * "Author et al. (2019)" with no DOI / PMID / URL / arXiv id -> FLAG (nothing to open)
      - already labelled unsure ([~mem] ...)  -> CHECK (honest: 'something to search', card §3)
      - inside a confirmed tag ([✓src WHO 2011]) -> CHECK (tagged, but a reader has nothing to open)
  * dates (2026-10-08, 8/10/2026) and money (500 บาท, ฿500, $20, 1,200 THB) are claims like numbers

Tags accepted as evidence (case-insensitive, must be inside [...]):
  confirmed : src  verified  ✓src          (e.g. [✓src], [src: WHO 2011])
  unsure    : mem  est  confirm  unverified  ~mem  ~est  ?confirm  ไม่แน่ใจ  ต้องเช็ค  ยืนยันไม่ได้
  derived   : calc  คำนวณ
A URL, DOI, PMID, arXiv id, a numeric footnote [3] (its reference-list line is checked on its own line)
or "source:/ที่มา:/อ้างอิง:" in the sentence also counts as evidence.

Examples
  python claim_check.py answer.txt
  python claim_check.py answer.txt --json
  cat answer.txt | python claim_check.py - --strict          # exit 1 if any FLAG
  python claim_check.py answer.txt --all-numbers             # also flag bare numbers with >= 2 digits

Output: one row per finding (line | level | kind | detail), then a summary and an ADVISORY line.
"""
import argparse
import json
import re
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print some symbols and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# ---------------------------------------------------------------- patterns
CONFIRMED_TAGS = ("✓src", "src", "verified")
UNSURE_TAGS = ("~mem", "~est", "?confirm", "unverified", "mem", "est", "confirm",
               "ไม่แน่ใจ", "ต้องเช็ค", "ยืนยันไม่ได้")
DERIVED_TAGS = ("calc", "คำนวณ")
TAG_RE = re.compile(r"\[\s*([^\]\n]{1,80})\]")

URL_RE = re.compile(r"https?://\S+", re.I)
# Crossref's recommended modern-DOI shape: ^10.\d{4,9}/[-._;()/:A-Z0-9]+$  (case-insensitive)
DOI_SHAPE = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", re.I)
# prefixed form may be malformed (we want to flag it); a bare form must already look like 10.<4-9 digits>/...
# so lab values such as "10.5 mg" or "10.5/uL" are never mistaken for a DOI.
DOI_CANDIDATE = re.compile(r"(?:doi\s*[:\s]\s*|https?://(?:dx\.)?doi\.org/)(10\.\S*)|\b(10\.\d{4,9}/\S+)", re.I)
PMID_RE = re.compile(r"\bPMID:?\s*(\d+)", re.I)
ARXIV_RE = re.compile(r"\barXiv:?\s*(\d{4}\.\d{4,5}(?:v\d+)?)", re.I)
SOURCE_WORD = re.compile(r"(?:source|ที่มา|อ้างอิง)\s*[:：]", re.I)
FOOTNOTE_RE = re.compile(r"\[\s*\d{1,3}(?:\s*[,–-]\s*\d{1,3})*\s*\]")

MONTHS = ("January|February|March|April|May|June|July|August|September|October|November|December|"
          "Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec")
CITATION_RE = re.compile(
    r"(?<![A-Za-z])(?!(?:%s)\b)[A-Z][A-Za-z'\-]+(?:\s+et\s+al\.?|\s+(?:and|&)\s+[A-Z][A-Za-z'\-]+)?,?\s*"
    r"\(?(?:19|20)\d{2}[a-z]?\)?" % MONTHS)

UNITS = (r"mg/dL|g/dL|ng/mL|pg/mL|mmol/L|mEq/L|IU/L|U/L|×\s?10\^?\d+(?:/[µμu]?L)?|x\s?10\^?\d+(?:/[µμu]?L)?|"
         r"/[µμu]L|mmHg|mcg|µg|μg|ug|mg|kg|mL|ml|dL|IU|fL|pg|ng|°C|bpm|%|g|L")
NUM = r"\d+(?:[.,]\d+)?"
UNIT_CLAIM = re.compile(r"(?<![\w.])%s(?:\s?[–-]\s?%s)?\s?(?:%s)(?![A-Za-z])" % (NUM, NUM, UNITS))
DATE_CLAIM = re.compile(r"(?<![\d/.-])(?:(?:19|20)\d{2}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/(?:\d{4}|\d{2}))(?![\d/-]|\.\d)")
MONEY_CLAIM = re.compile(r"(?:[฿$€£]\s?\d[\d,]*(?:\.\d+)?|\d[\d,]*(?:\.\d+)?\s?(?:บาท|baht|THB|USD|EUR)(?![A-Za-z]))", re.I)
YEAR_CLAIM = re.compile(r"(?<![\d\-/])(?:19|20)\d{2}(?![\d\-/])")
BARE_NUMBER = re.compile(r"(?<![\w.\-/])\d{2,}(?:[.,]\d+)?(?![\w\-/])")
MEDICAL_UNITS = re.compile(r"mg|mcg|µg|μg|ug|IU|mmol|mEq|U/L|g/dL|fL|pg|ng|mL|ml|mmHg", re.I)
MEDICAL_WORDS = re.compile(r"dose|dosage|ขนาดยา|reference range|ช่วงอ้างอิง|ค่าปกติ|ค่าวิกฤต|critical value|cut-?off", re.I)


# ---------------------------------------------------------------- helpers
def split_sentences(text):
    """[(lineno, sentence)] - split on newlines, then on Latin sentence ends followed by a capital."""
    out = []
    for no, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        for s in re.split(r"(?<=[a-z0-9)\]])[.!?]\s+(?=[A-Z])|(?<=[!?])\s+", line):
            if s.strip():
                out.append((no, s.strip()))
    return out


def tag_classes(sentence):
    """Return the set of tag classes present in [..] tags: confirmed / unsure / derived."""
    found = set()
    for m in TAG_RE.finditer(sentence):
        body = m.group(1).strip().lower()
        head = re.split(r"[\s:：]", body, maxsplit=1)[0]
        if head in CONFIRMED_TAGS:
            found.add("confirmed")
        elif head in UNSURE_TAGS:
            found.add("unsure")
        elif head in DERIVED_TAGS:
            found.add("derived")
    return found


def identifiers(sentence):
    ids = []
    for m in DOI_CANDIDATE.finditer(sentence):
        ids.append(("doi", (m.group(1) or m.group(2)).rstrip(".,;)")))
    ids += [("pmid", m.group(1)) for m in PMID_RE.finditer(sentence)]
    ids += [("arxiv", m.group(1)) for m in ARXIV_RE.finditer(sentence)]
    return ids


def has_evidence(sentence):
    """True when the sentence carries a source: confirmed/derived tag, URL, id, or 'source:' word."""
    cls = tag_classes(sentence)
    if cls & {"confirmed", "derived"}:
        return True
    return bool(URL_RE.search(sentence) or identifiers(sentence) or SOURCE_WORD.search(sentence)
                or FOOTNOTE_RE.search(sentence))


def claim_tokens(sentence, all_numbers=False):
    """Checkable tokens in a sentence, after removing citation spans (handled separately)."""
    scrub = CITATION_RE.sub(" ", sentence)
    scrub = TAG_RE.sub(" ", scrub)
    scrub = URL_RE.sub(" ", scrub)
    scrub = DOI_CANDIDATE.sub(" ", scrub)
    scrub = PMID_RE.sub(" ", scrub)
    scrub = ARXIV_RE.sub(" ", scrub)
    toks = [m.group(0).strip() for m in DATE_CLAIM.finditer(scrub)]
    scrub = DATE_CLAIM.sub(" ", scrub)
    toks += [m.group(0).strip() for m in MONEY_CLAIM.finditer(scrub)]
    scrub = MONEY_CLAIM.sub(" ", scrub)
    toks += [m.group(0).strip() for m in UNIT_CLAIM.finditer(scrub)]
    rest = UNIT_CLAIM.sub(" ", scrub)
    toks += [m.group(0) for m in YEAR_CLAIM.finditer(rest)]
    if all_numbers:
        rest2 = YEAR_CLAIM.sub(" ", rest)
        toks += [m.group(0) for m in BARE_NUMBER.finditer(rest2)]
    return toks


def is_medical(sentence, tokens):
    if MEDICAL_WORDS.search(sentence):
        return True
    return any(MEDICAL_UNITS.search(t) for t in tokens)


def id_finding(no, kind, val):
    """One finding per identifier. Never returns None: a well-formed id is still unverified (card §3)."""
    if kind == "doi":
        if DOI_SHAPE.match(val):
            return {"line": no, "level": "CHECK", "kind": "DOI_SHAPE_ONLY",
                    "detail": "%s - shape OK, NOT VERIFIED (shape OK != exists). Open https://doi.org/%s" % (val, val)}
        return {"line": no, "level": "FLAG", "kind": "DOI_MALFORMED",
                "detail": "%s - not a valid DOI shape (10.<4-9 digits>/<suffix>); cannot be opened" % val}
    if kind == "pmid":
        return {"line": no, "level": "CHECK", "kind": "ID_SHAPE_ONLY",
                "detail": "PMID %s - NOT VERIFIED. Open https://pubmed.ncbi.nlm.nih.gov/%s/" % (val, val)}
    return {"line": no, "level": "CHECK", "kind": "ID_SHAPE_ONLY",
            "detail": "arXiv %s - NOT VERIFIED. Open https://arxiv.org/abs/%s" % (val, val)}


# ---------------------------------------------------------------- main check
def check(text, all_numbers=False):
    findings = []
    sentences = split_sentences(text)
    for no, s in sentences:
        # 1. identifiers: always something for a human to open
        for kind, val in identifiers(s):
            f = id_finding(no, kind, val)
            if f:
                findings.append(f)
        # 2. author-year citation with nothing to open
        openable = bool(URL_RE.search(s) or identifiers(s))
        in_tags = [m.group(0).strip() for t in TAG_RE.finditer(s) for m in CITATION_RE.finditer(t.group(1))]
        free = [m.group(0).strip() for m in CITATION_RE.finditer(TAG_RE.sub(" ", s))]
        if free and not openable:
            if "unsure" in tag_classes(s):
                findings.append({"line": no, "level": "CHECK", "kind": "CITATION_UNSURE",
                                 "detail": "%s - labelled unsure: search for it before citing (card §3), not a citation yet" % "; ".join(free)})
            else:
                findings.append({"line": no, "level": "FLAG", "kind": "CITATION_NO_IDENTIFIER",
                                 "detail": "%s - no DOI/PMID/URL/arXiv id to open; treat as 'something to search', not a citation" % "; ".join(free)})
        if in_tags and not openable:
            findings.append({"line": no, "level": "CHECK", "kind": "SOURCE_TAG_NO_IDENTIFIER",
                             "detail": "%s - tagged as a source but a reader has nothing to open; add URL/DOI if others must verify" % "; ".join(in_tags)})
        # 3. numbers / units / years
        toks = claim_tokens(s, all_numbers)
        if not toks:
            continue
        medical = is_medical(s, toks)
        cls = tag_classes(s)
        if has_evidence(s):
            continue
        if "unsure" in cls:
            if medical:
                findings.append({"line": no, "level": "CHECK", "kind": "MEDICAL_UNVERIFIED",
                                 "detail": "%s - labelled unsure (honest) but a medical value: verify with the authoritative source before use" % ", ".join(toks)})
            continue
        findings.append({"line": no, "level": "FLAG", "kind": "UNSOURCED_MEDICAL" if medical else "UNSOURCED_CLAIM",
                         "detail": "%s - no source/confidence tag in this sentence" % ", ".join(toks)})
    summary = {"sentences": len(sentences),
               "flag": sum(1 for f in findings if f["level"] == "FLAG"),
               "check": sum(1 for f in findings if f["level"] == "CHECK")}
    return {"findings": findings, "summary": summary}


ADVISORY = "ADVISORY: tool นี้ตรวจแค่ 'มีที่มา/ป้ายความมั่นใจไหม' ไม่ได้ตรวจว่าจริงไหม - ค่าทางการแพทย์/citation ต้องเปิดแหล่ง authoritative ยืนยันเอง"


def render(res):
    lines = ["line | level | kind | detail", "-----|-------|------|-------"]
    for f in res["findings"]:
        lines.append("%4d | %-5s | %s | %s" % (f["line"], f["level"], f["kind"], f["detail"]))
    if not res["findings"]:
        lines.append("(no findings)")
    s = res["summary"]
    lines.append("")
    lines.append("sentences scanned: %d | FLAG: %d | CHECK: %d" % (s["sentences"], s["flag"], s["check"]))
    lines.append("FLAG = fix before sending (add source tag / identifier or say 'unsure'); CHECK = a person must open it")
    lines.append(ADVISORY)
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Flag unsourced numbers / malformed DOIs / citations with nothing to open.")
    ap.add_argument("path", help="text file to scan, or - for stdin")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--strict", action="store_true", help="exit 1 when any FLAG is present")
    ap.add_argument("--all-numbers", action="store_true", help="also flag bare numbers with >= 2 digits")
    a = ap.parse_args(argv)
    if a.path == "-":
        # read bytes as UTF-8: a Thai Windows console would decode piped text as cp874 (mojibake / crash)
        text = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")
    else:
        with open(a.path, encoding="utf-8-sig") as f:
            text = f.read()
    res = check(text, a.all_numbers)
    print(json.dumps(res, ensure_ascii=False, indent=1) if a.json else render(res))
    return 1 if (a.strict and res["summary"]["flag"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
