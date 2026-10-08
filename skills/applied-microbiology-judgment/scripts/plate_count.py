#!/usr/bin/env python3
"""plate_count - standard/aerobic plate count (CFU per mL or g) with the countable-range rule.

Black-box tool for applied-microbiology-judgment. Run --help first; read the source only if a
result looks wrong. ADVISORY ONLY: food/water release decisions follow the applicable standard
(ISO / FDA BAM / Thai MOPH notification) and the lab's own SOP.

Rules and where they come from
  countable range  only plates with LOW <= colonies <= HIGH are counted; outside = discarded.
                   The range is a METHOD choice -> --range is required. Sources differ:
                   APPLIED-MICRO digest §2 says 30-300; 508304 lecture digest §3 (APC) says 25-250.
  one dilution     N = mean colonies x dilution factor / volume plated
                   (APPLIED-MICRO digest §2: CFU/mL = avg colony x dilution factor / mL)
  two dilutions    N = sum(C) / ((n1 + 0.1 n2) x d1 x V)   (508304 digest §3 APC formula;
                   d1 = the less-diluted plate's dilution, e.g. 1e-2). The tool uses the general
                   pooled form N = sum(C) / (V x sum(n_i x d_i)), which equals it for 10-fold steps.
  no valid plate   not a valid count (digest: outside range = discard). The tool prints an
                   estimate labelled EST only so you can see the order of magnitude, and says
                   to re-plate. All plates 0 -> "< detection limit", never 0: the card's deeper trap
                   is "not detected" != "absent" (card rule #1).
  optional limit   --limit compares N with a limit YOU supply (e.g. 508304 §3 teaching: SPC >= 1e6
                   CFU/g = spoiled). The tool never assumes a limit.

Plates: --plate DILUTION:COUNT, repeat. DILUTION as a fraction (1e-2) and COUNT an integer or TNTC.

Examples (run from the skill folder)
  python scripts/plate_count.py --input data/apc_two_dilutions_teaching.json
  python scripts/plate_count.py --range 25 250 --volume 1 --plate 1e-2:232 --plate 1e-2:244 --plate 1e-3:33 --plate 1e-3:28
  python scripts/plate_count.py --range 30 300 --volume 1 --plate 1e-1:TNTC --plate 1e-2:150 --plate 1e-2:170 --plate 1e-3:14
  python scripts/plate_count.py --range 30 300 --volume 1 --unit g --plate 1e-1:0 --plate 1e-1:0
  python scripts/plate_count.py --range 30 300 --volume 1 --unit g --limit 1e6 --plate 1e-4:120 --plate 1e-4:110 --json
"""
import argparse
import json
import sys

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print § Σ Δ ≥ and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ADVISORY = ("ADVISORY: decision support only - release/reject per the applicable food/water standard, "
            "the lab SOP and an authorised signatory.")


def parse_plate(spec):
    if ":" not in spec:
        raise ValueError("--plate must be DILUTION:COUNT, got %r" % spec)
    d, c = spec.split(":", 1)
    d = float(d)
    if not 0 < d <= 1:
        raise ValueError("dilution must be a fraction in (0, 1], e.g. 1e-2 (got %g)" % d)
    c = c.strip().upper()
    return {"dilution": d, "count": None if c == "TNTC" else float(c), "tntc": c == "TNTC"}


def in_range(count, low, high):
    return count is not None and low <= count <= high


def pooled_count(plates, volume):
    """General pooled estimator N = sum(C) / (V x sum(d_i)) over the counted plates.

    For two 10-fold dilutions this is exactly 508304's sum(C) / ((n1 + 0.1 n2) x d1) / V.
    """
    total = sum(p["count"] for p in plates)
    denom = volume * sum(p["dilution"] for p in plates)
    return total / denom


def plate_count(plates, low, high, volume, limit=None):
    if low >= high:
        raise ValueError("range LOW must be < HIGH")
    if volume <= 0:
        raise ValueError("volume plated must be > 0")
    for p in plates:
        p["counted"] = in_range(p["count"], low, high)
    used = [p for p in plates if p["counted"]]
    res = {"range": [low, high], "volume": volume, "plates": plates, "valid": bool(used), "flags": []}
    if used:
        dils = sorted({p["dilution"] for p in used}, reverse=True)
        res["dilutions_used"] = dils
        for a, b in zip(dils, dils[1:]):
            if abs(a / b - 10) > 1e-6:
                res["flags"].append("counted dilutions %g and %g are not consecutive 10-fold steps - check the series"
                                    % (a, b))
        res["n"] = pooled_count(used, volume)
        res["formula"] = ("mean x DF / V" if len(dils) == 1 else
                          "sum(C) / (V x sum d_i)  [= sum(C) / ((n1 + 0.1 n2) x d1 x V) for 10-fold steps]")
        res["report"] = "%.4g" % res["n"]
    else:
        least = max(plates, key=lambda p: p["dilution"])
        numeric = [p for p in plates if p["count"] is not None]
        if numeric and len(numeric) == len(plates) and all(p["count"] == 0 for p in plates):
            lod = 1.0 / (least["dilution"] * volume)
            res["n"] = None
            res["detection_limit"] = lod
            res["report"] = "< %g (not detected at the least-diluted plate; not detected != absent)" % lod
        elif all(p["tntc"] or (p["count"] is not None and p["count"] > high) for p in plates):
            most = min(plates, key=lambda p: p["dilution"])
            group = [p for p in plates if p["dilution"] == most["dilution"] and not p["tntc"]]
            est = pooled_count(group, volume) if group else None
            res["n"] = None
            res["estimate"] = est
            res["report"] = ("EST > %g - all plates above range; NOT a valid count, re-plate at higher dilution"
                             % est) if est else "TNTC - NOT a valid count, re-plate at higher dilution"
        else:
            d = max(p["dilution"] for p in numeric)  # least-diluted plate that has a number
            group = [p for p in numeric if p["dilution"] == d]
            est = pooled_count(group, volume)
            res["n"] = None
            res["estimate"] = est
            res["report"] = ("EST %.4g - no plate inside %g-%g; NOT a valid count (outside range = discard), "
                             "re-plate or follow SOP for estimated counts" % (est, low, high))
    if limit is not None:
        if res.get("n") is not None:
            res["vs_limit"] = "AT/ABOVE limit %g" % limit if res["n"] >= limit else "below limit %g" % limit
        elif res.get("detection_limit") is not None:
            res["vs_limit"] = ("below limit %g (detection limit %g)" % (limit, res["detection_limit"])
                               if res["detection_limit"] < limit else
                               "CANNOT JUDGE: detection limit %g >= limit %g" % (res["detection_limit"], limit))
        else:
            res["vs_limit"] = "CANNOT JUDGE: no valid count"
    return res


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", help="JSON with range, volume, plates (+ optional unit, limit); flags override it")
    ap.add_argument("--plate", action="append", help="DILUTION:COUNT, e.g. 1e-2:232 or 1e-1:TNTC")
    ap.add_argument("--range", nargs=2, type=float, metavar=("LOW", "HIGH"),
                    help="countable range of your method (digests: 30 300 or 25 250) - required")
    ap.add_argument("--volume", type=float, help="volume plated per plate in mL (pour plate usually 1) - required")
    ap.add_argument("--unit", choices=["mL", "g"], help="per mL or per g of the original sample (default mL)")
    ap.add_argument("--limit", type=float, help="optional limit from YOUR standard, same unit")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.input:
        with open(a.input, encoding="utf-8") as f:
            cfg = json.load(f)
        a.plate = a.plate or cfg.get("plates")
        a.range = a.range or cfg.get("range")
        a.volume = a.volume if a.volume is not None else cfg.get("volume")
        a.unit = a.unit or cfg.get("unit")
        a.limit = a.limit if a.limit is not None else cfg.get("limit")
    a.unit = a.unit or "mL"
    for need in ("plate", "range", "volume"):
        if not getattr(a, need):
            ap.error("--%s is required (flag or --input JSON)" % need)
    plates = [parse_plate(s) for s in a.plate]
    res = plate_count(plates, a.range[0], a.range[1], a.volume, a.limit)
    res["unit"] = "CFU/" + a.unit
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print("countable range %g-%g | volume plated %g mL | unit %s" % (a.range[0], a.range[1], a.volume, res["unit"]))
    print("%-10s %-8s %s" % ("dilution", "count", "counted?"))
    for p in plates:
        print("%-10g %-8s %s" % (p["dilution"], "TNTC" if p["tntc"] else "%g" % p["count"],
                                 "yes" if p["counted"] else "no (outside range)"))
    if res["valid"]:
        print("formula: %s" % res["formula"])
        print("-> N = %s %s" % (res["report"], res["unit"]))
    else:
        print("-> %s  [unit: %s]" % (res["report"], res["unit"]))
    for f in res["flags"]:
        print("FLAG: " + f)
    if "vs_limit" in res:
        print("vs your limit: %s" % res["vs_limit"])
    print("NOTE: a count says nothing about pathogens; screen-positive = presumptive, confirm (card Fork 2).")
    print(ADVISORY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
