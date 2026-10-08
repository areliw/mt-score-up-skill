#!/usr/bin/env python3
"""cv_calc — the hand computations behind cv-judgment's forks (CMU 261753 Computer Vision), as checkable tables.

    hsv    RGB -> HSV by the slide's branch rule (deck #1 slide 20): M = max, m = min,
           h = 0 (M = m) | (g-b)/(M-m)*60 mod 360 (M = r) | (b-r)/(M-m)*60 + 120 (M = g) | (r-g)/(M-m)*60 + 240 (M = b),
           ties take r first (slide 23), v = M/255, s = 1 - m/M.  Prints the branch used and the substituted formula,
           plus RGB Euclidean distance and hue difference against pixel 1 (card fork F + trap #1: light changes RGB,
           not hue).  --h-range LO HI (LO > HI wraps through 0, e.g. 330 30 for red) and --s-min mark which pixels pass.
    glcm   co-occurrence counts for offset (dx, dy) with x = ROW (down) and y = COLUMN (right), deck #5 slide 3:
           C(i, j) = #{(x, y): I(x, y) = i and I(x+dx, y+dy) = j}.  --symmetric adds the transpose (slide 11),
           P = C / sum(C) (slide 8), then every feature's per-cell sum terms and totals (slides 16-26): max probability,
           ASM (= Uniformity = Energy on the slide), contrast, homogeneity 1/(1+|i-j|), entropy with log2,
           correlation with mu1/sigma1 from row sums and mu2/sigma2 from column sums.
           --quantize L maps 0-255 to L labels (slide 4: 0-63 -> 0, 64-127 -> 1, ...).  --given = the input already IS
           a GLCM (counts or probabilities, slides 22-26).  --angle 0|45|90|135 --d N follows Haralick 1973 / MATLAB
           (counter-clockwise on screen); the skimage call that gives the same matrix is printed too.
    morph  binary erode / dilate / open / close, SE origin = its centre (deck #2 slides 94-116):
           dilation stamps the SE on every 1 (slide 96: an asymmetric SE grows up + right), erosion keeps z only where
           the whole SE fits (slide 104), opening = erosion -> dilation (slides 107-110), closing = dilation -> erosion
           (slides 112-115).  Pixels outside the image count as 0 (slide 115); --border ignore = skimage's default.

Not here (on purpose): histogram stretch/equalization, mean/median filters, Sobel/Prewitt/Roberts, connected-component
labeling -> image-processing-judgment's scripts/vision_calc.py.
Proof = evals/test_cv_calc.py (expected values from the slides and Haralick 1973 Fig. 2; skimage / scipy / OpenCV
numbers are recorded as constants in comments, never imported at test time).  Python 3 stdlib only.
ADVISORY: a checker for hand calculations and teaching data - not a diagnosis or a classifier; no patient data.

    python cv_calc.py hsv "100 0 200; 128 128 0"
    python cv_calc.py hsv @data/stain_two_lightings_rgb.txt --h-range 270 320 --s-min 0.2
    python cv_calc.py glcm @data/glcm_slide5_7x6.txt --dx 0 --dy 1 --symmetric
    python cv_calc.py glcm @data/haralick1973_4x4.txt --angle 45 --symmetric
    python cv_calc.py glcm "0 0.2 0; 0 0 0; 0.2 0 0.6" --given
    python cv_calc.py glcm "10 70 130 200; 60 64 127 128" --quantize 4 --trace
    python cv_calc.py morph @data/smear_mask_12x12.txt --op open
    python cv_calc.py morph "0 1 0 1 0 1 0" --op close --se "1 1 1" --json
(@file paths resolve against the current folder first, then the skill folder; '#' starts a comment in data files.)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from fractions import Fraction

# cp874-safe-stdout: Thai Windows consoles default to cp874, which cannot print the symbols below and crashes.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADVISORY = ("ADVISORY: ตัวช่วยตรวจเลขคิดมือ/ข้อมูลสอน ไม่ใช่การวินิจฉัยหรือ classifier — ห้ามใช้ตัดสินคนไข้ · "
            "ไม่มีข้อมูลผู้ป่วย · convention ของสไลด์วิชา/ผู้สอนเป็นตัวตัดสินเมื่อขัดกัน")


# ---------------------------------------------------------------- input parsing
def read_arg(s: str) -> str:
    """'@path' -> file text ('#' comments dropped, rows joined by ';'); anything else is returned unchanged."""
    if not s.startswith("@"):
        return s
    rel = s[1:]
    for cand in (rel, os.path.join(SKILL_DIR, rel)):
        if os.path.isfile(cand):
            with open(cand, encoding="utf-8") as f:
                lines = [ln.split("#", 1)[0] for ln in f.read().splitlines()]
            return ";".join(ln for ln in lines if ln.strip())
    raise SystemExit(f"file not found: {rel} (looked in the current folder and {SKILL_DIR})")


def parse_rows(s: str) -> list[list[str]]:
    rows = [r.replace(",", " ").split() for r in read_arg(s).replace("\n", ";").split(";")]
    rows = [r for r in rows if r]
    if not rows:
        raise ValueError("empty matrix")
    return rows


def parse_int_mat(s: str) -> list[list[int]]:
    m = [[int(float(v)) for v in r] for r in parse_rows(s)]
    if len({len(r) for r in m}) != 1:
        raise ValueError("ragged matrix: every row needs the same number of values")
    return m


def parse_frac_mat(s: str) -> list[list[Fraction]]:
    m = [[Fraction(v) for v in r] for r in parse_rows(s)]
    if len({len(r) for r in m}) != 1:
        raise ValueError("ragged matrix: every row needs the same number of values")
    return m


def fmt(x, dp: int = 4) -> str:
    """Exact fraction + decimal, e.g. '7/12 = 0.5833'; integers stay integers."""
    if x is None:
        return "undefined"
    if isinstance(x, int):
        return str(x)
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        return f"{x.numerator}/{x.denominator} = {float(x):.{dp}f}"
    return f"{x:.{dp}f}"


def dec(x, dp: int = 4) -> str:
    if x is None:
        return "-"
    if isinstance(x, Fraction) and x.denominator == 1:
        return str(x.numerator)
    return f"{float(x):.{dp}f}"


def grid(m, w: int = 0) -> str:
    w = w or max(len(dec(v, 0) if isinstance(v, int) else str(v)) for r in m for v in r)
    return "\n".join("  " + " ".join(str(v).rjust(w) for v in r) for r in m)


def jsonable(o):
    if isinstance(o, Fraction):
        return float(o)
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    return o


# ---------------------------------------------------------------- hsv (deck #1 slides 16-25)
HUE_OFFSET = {"r": 0, "g": 120, "b": 240}      # slide 20: M=r -> +0 then mod 360 · M=g -> +120 · M=b -> +240


def _wrap360(h):
    """Slide 20 'mod 360°' (Python % keeps the result in [0, 360) for negative values too)."""
    return h % 360


def rgb_to_hsv(r: int, g: int, b: int) -> dict:
    for c in (r, g, b):
        if not (isinstance(c, int) and 0 <= c <= 255):
            raise ValueError(f"r, g, b must be integers 0-255, got {c}")
    M, m = max(r, g, b), min(r, g, b)
    C = M - m
    v = Fraction(M, 255)
    s = Fraction(0) if M == 0 else 1 - Fraction(m, M)
    if C == 0:
        branch, raw = "M=m", Fraction(0)
        formula = "h = 0 (M = m: gray, hue undefined - NOT red)"
    elif M == r:
        branch, raw = "M=r", Fraction(60 * (g - b), C) + HUE_OFFSET["r"]
        formula = f"h = (g-b)/(M-m)*60 mod 360 = ({g}-{b})/({M}-{m})*60 = {dec(raw)} -> mod 360"
    elif M == g:
        branch, raw = "M=g", Fraction(60 * (b - r), C) + HUE_OFFSET["g"]
        formula = f"h = (b-r)/(M-m)*60 + 120 = ({b}-{r})/({M}-{m})*60 + 120 = {dec(raw)}"
    else:
        branch, raw = "M=b", Fraction(60 * (r - g), C) + HUE_OFFSET["b"]
        formula = f"h = (r-g)/(M-m)*60 + 240 = ({r}-{g})/({M}-{m})*60 + 240 = {dec(raw)}"
    h = _wrap360(raw)
    return {"rgb": (r, g, b), "M": M, "m": m, "branch": branch, "h_raw": raw, "h": h, "s": s, "v": v,
            "formula": formula, "gray": C == 0}


def hue_diff(h1, h2) -> Fraction:
    d = abs(Fraction(h1) - Fraction(h2)) % 360
    return min(d, 360 - d)


def in_hue_range(h, lo: float, hi: float) -> bool:
    h = float(h)
    return lo <= h <= hi if lo <= hi else (h >= lo or h <= hi)


def hsv_table(pixels: list[tuple[int, int, int]], h_range=None, s_min=None) -> dict:
    rows = [rgb_to_hsv(*p) for p in pixels]
    ref = rows[0]
    for k, row in enumerate(rows):
        dr = [a - b for a, b in zip(row["rgb"], ref["rgb"])]
        row["rgb_dist_vs_1"] = math.sqrt(sum(d * d for d in dr))       # deck #1: Euclidean distance in RGB space
        row["dh_vs_1"] = hue_diff(row["h"], ref["h"])
        row["dv_vs_1"] = row["v"] - ref["v"]
        if h_range is not None or s_min is not None:
            ok = True
            if h_range is not None:
                ok = ok and not row["gray"] and in_hue_range(row["h"], *h_range)
            if s_min is not None:
                ok = ok and float(row["s"]) >= s_min
            row["pass"] = ok
    return {"pixels": rows, "h_range": h_range, "s_min": s_min}


def print_hsv(res: dict, dp: int) -> None:
    print("RGB -> HSV  (deck #1 slide 20 · ties take M=r first, slide 23 · h in [0, 360), s and v in [0, 1])")
    for k, p in enumerate(res["pixels"], 1):
        r, g, b = p["rgb"]
        print(f"\n#{k}  [r g b] = [{r} {g} {b}]   M = {p['M']}  m = {p['m']}   branch {p['branch']}")
        print(f"    {p['formula']}")
        print(f"    h = {fmt(p['h'], dp)}°   s = 1 - m/M = {fmt(p['s'], dp)}   v = M/255 = {fmt(p['v'], dp)}")
        if p["gray"]:
            print("    NOTE: M = m -> hue is undefined (reported 0 by the slide rule); 0 here does NOT mean red -> use --s-min")
    if len(res["pixels"]) > 1:
        print("\nvs pixel #1 (card trap #1: same stain under other light = big RGB distance, ~same hue):")
        print("    #   RGB distance    Δh (circular)   Δv")
        for k, p in enumerate(res["pixels"], 1):
            print(f"  {k:>3}   {p['rgb_dist_vs_1']:>12.{dp}f}   {float(p['dh_vs_1']):>13.{dp}f}   {float(p['dv_vs_1']):+.{dp}f}")
    if res["h_range"] is not None or res["s_min"] is not None:
        lo_hi = res["h_range"]
        rule = []
        if lo_hi is not None:
            rule.append(f"h in [{lo_hi[0]:g}, {lo_hi[1]:g}]" + (" (wraps through 0°)" if lo_hi[0] > lo_hi[1] else ""))
        if res["s_min"] is not None:
            rule.append(f"s >= {res['s_min']:g}")
        print("\nthreshold: " + " and ".join(rule) + (" · gray pixels (M = m) never pass a hue range" if lo_hi else ""))
        for k, p in enumerate(res["pixels"], 1):
            print(f"  #{k}  h = {dec(p['h'], 2):>7}  s = {dec(p['s'], 3)}  -> {'PASS' if p['pass'] else 'fail'}")


# ---------------------------------------------------------------- glcm (deck #5)
# deck #5 slide 3: x = ROW (down), y = COLUMN (right); the neighbour of (x, y) is (x + dx, y + dy).
ANGLE_TO_OFFSET = {0: (0, 1), 45: (-1, 1), 90: (-1, 0), 135: (-1, -1)}   # Haralick 1973 / MATLAB: CCW on screen


def _neighbour(x: int, y: int, dx: int, dy: int) -> tuple[int, int]:
    return x + dx, y + dy


def resolve_offset(dx: int, dy: int, angle: int | None = None, d: int = 1) -> tuple[int, int]:
    if angle is None:
        return dx, dy
    ux, uy = ANGLE_TO_OFFSET[angle]
    return ux * d, uy * d


def quantize(img: list[list[int]], levels: int, src_levels: int = 256) -> list[list[int]]:
    """Slide 4: equal-width bins over 0..src_levels-1 -> label = floor(v * levels / src_levels)."""
    out = []
    for row in img:
        for v in row:
            if not 0 <= v < src_levels:
                raise ValueError(f"value {v} outside 0..{src_levels - 1}")
        out.append([v * levels // src_levels for v in row])
    return out


def cooccurrence(img: list[list[int]], dx: int, dy: int, levels: int):
    H, W = len(img), len(img[0])
    C = [[0] * levels for _ in range(levels)]
    pairs = []
    for x in range(H):
        for y in range(W):
            x2, y2 = _neighbour(x, y, dx, dy)
            if 0 <= x2 < H and 0 <= y2 < W:
                i, j = img[x][y], img[x2][y2]
                if not (0 <= i < levels and 0 <= j < levels):
                    raise ValueError(f"gray level {max(i, j)} >= levels {levels} (use --levels or --quantize)")
                C[i][j] += 1
                pairs.append(((x, y), (x2, y2), i, j))
    return C, pairs


def transpose(C):
    return [list(r) for r in zip(*C)]


def symmetrize(C):
    """Slide 11: C_SYM(dx, dy) = C_ASYM(dx, dy) + C_ASYM(dx, dy)^T."""
    T = transpose(C)
    return [[C[i][j] + T[i][j] for j in range(len(C))] for i in range(len(C))]


def normalize(C):
    """Slide 8: P = C / sum(C) (the slide calls it optional for the matrix, but slide 16 computes features on it)."""
    N = sum(sum(r) for r in C)
    if N == 0:
        raise ValueError("no pixel pairs: the offset is larger than the image")
    return [[Fraction(c) / N for c in r] for r in C], N


def _w_homogeneity(i: int, j: int) -> Fraction:
    return Fraction(1, 1 + abs(i - j))          # slide 18: C(i,j) / (1 + |i - j|)


def _w_idm(i: int, j: int) -> Fraction:
    return Fraction(1, 1 + (i - j) ** 2)       # skimage graycoprops 'homogeneity' (inverse difference moment)


def _log(p: float, base: str) -> float:
    return {"2": math.log2, "e": math.log, "10": math.log10}[base](p)


def features(P, log_base: str = "2") -> dict:
    L = len(P)
    p_i = [sum(P[i]) for i in range(L)]                                   # row sums -> mu1, sigma1 (slide 22)
    p_j = [sum(P[i][j] for i in range(L)) for j in range(L)]              # column sums -> mu2, sigma2 (slide 23)
    mu1 = sum(i * p for i, p in enumerate(p_i))
    mu2 = sum(j * p for j, p in enumerate(p_j))
    var1 = sum((i - mu1) ** 2 * p for i, p in enumerate(p_i))
    var2 = sum((j - mu2) ** 2 * p for j, p in enumerate(p_j))
    cells, tot = [], {"contrast": Fraction(0), "homogeneity": Fraction(0), "idm": Fraction(0),
                      "asm": Fraction(0), "entropy": 0.0, "cov": Fraction(0)}
    for i in range(L):
        for j in range(L):
            p = P[i][j]
            if p == 0:
                continue
            t = {"i": i, "j": j, "P": p,
                 "contrast": (i - j) ** 2 * p,
                 "homogeneity": p * _w_homogeneity(i, j),
                 "idm": p * _w_idm(i, j),
                 "asm": p * p,
                 "entropy": -float(p) * _log(float(p), log_base),
                 "cov": (i - mu1) * (j - mu2) * p}
            cells.append(t)
            for k in tot:
                tot[k] += t[k]
    sd = var1 * var2
    corr = None if sd == 0 else float(tot["cov"]) / math.sqrt(float(sd))
    if var1 == var2 and var1 != 0:
        corr = tot["cov"] / var1                  # exact when sigma1 = sigma2 (always true for a symmetric GLCM)
    pmax = max(max(r) for r in P)
    argmax = [(i, j) for i in range(L) for j in range(L) if P[i][j] == pmax]
    return {"max_prob": pmax, "max_at": argmax, "asm": tot["asm"], "sqrt_asm": math.sqrt(float(tot["asm"])),
            "contrast": tot["contrast"], "homogeneity": tot["homogeneity"], "idm": tot["idm"],
            "entropy": tot["entropy"], "correlation": corr, "cov": tot["cov"],
            "mu1": mu1, "mu2": mu2, "var1": var1, "var2": var2, "p_i": p_i, "p_j": p_j,
            "log_base": log_base, "cells": cells}


def skimage_equivalent(dx: int, dy: int):
    """skimage graycomatrix uses row offset round(sin(a)*d), col offset round(cos(a)*d): rows point DOWN."""
    d = max(abs(dx), abs(dy))
    if d == 0:
        return None
    a = math.atan2(dx, dy) % (2 * math.pi)
    if round(math.sin(a) * d) == dx and round(math.cos(a) * d) == dy:
        return d, a
    return None


def glcm(img=None, dx: int = 0, dy: int = 1, levels: int | None = None, symmetric: bool = False,
         log_base: str = "2", quantize_levels: int | None = None, given=None) -> dict:
    res = {"dx": dx, "dy": dy, "symmetric": symmetric, "log_base": log_base}
    if given is not None:
        C = given
        res.update(image=None, quantized=None, pairs=[], C_asym=None)
        if len({len(r) for r in C} | {len(C)}) != 1:
            raise ValueError("--given needs a square L x L matrix")
        if symmetric:
            res["C_asym"] = C
            C = symmetrize(C)
    else:
        q = quantize(img, quantize_levels) if quantize_levels else img
        L = levels or quantize_levels or (max(max(r) for r in q) + 1)
        C0, pairs = cooccurrence(q, dx, dy, L)
        res.update(image=img, quantized=q if quantize_levels else None, pairs=pairs, C_asym=C0)
        C = symmetrize(C0) if symmetric else C0
    P, N = normalize(C)
    res.update(C=C, N=N, P=P, levels=len(C), features=features(P, log_base))
    res["skimage"] = None if given is not None else skimage_equivalent(dx, dy)
    return res


def _direction_words(dx: int, dy: int) -> str:
    v = {-1: "UP", 0: "", 1: "DOWN"}[(dx > 0) - (dx < 0)]
    h = {-1: "LEFT", 0: "", 1: "RIGHT"}[(dy > 0) - (dy < 0)]
    return "-".join(w for w in (v, h) if w) or "same pixel"


def print_glcm(res: dict, dp: int, trace: bool) -> None:
    F, L = res["features"], res["levels"]
    lg = {"2": "log2", "e": "ln", "10": "log10"}[res["log_base"]]
    print("GLCM - deck #5 convention: x = ROW (down), y = COLUMN (right); "
          "C(i, j) counts I(x, y) = i with I(x+dx, y+dy) = j (slide 3)")
    if res["image"] is not None:
        dx, dy = res["dx"], res["dy"]
        print(f"offset (dx, dy) = ({dx}, {dy}) -> neighbour {_direction_words(dx, dy)} of the reference pixel")
        if res["quantized"] is not None:
            print("\ninput image (0-255):\n" + grid(res["image"]))
            print("quantized I_Q (slide 4: label = floor(v*L/256)):\n" + grid(res["quantized"]))
        else:
            print("\ninput image I_Q:\n" + grid(res["image"]))
        print(f"pairs counted N_pairs = {len(res['pairs'])}")
        if trace:
            for (a, b, i, j) in res["pairs"]:
                print(f"    {a} -> {b}:  i = {i}, j = {j}")
    else:
        print("input = a GLCM given directly (--given): no counting step")
    sym = "yes: C_SYM = C + C^T (slide 11)" if res["symmetric"] else "no (C_ASYM) · --symmetric adds C^T (slide 11)"
    print(f"symmetric = {sym} · levels L = {L} · entropy uses {lg} (slide 18 uses log2)")
    head = "      " + " ".join(f"j={j}".rjust(6) for j in range(L))
    def mat(M, title):
        print(f"\n{title}\n{head}")
        for i, r in enumerate(M):
            print(f"  i={i} " + " ".join(dec(v, dp if isinstance(v, Fraction) and v.denominator != 1 else 0).rjust(6) for v in r))
    if res["symmetric"] and res["C_asym"] is not None:
        mat(res["C_asym"], "C_ASYM (rows i = reference pixel, columns j = neighbour):")
        mat(transpose(res["C_asym"]), "C_ASYM^T (= C_ASYM of the opposite offset):")
        mat(res["C"], "C_SYM = C_ASYM + C_ASYM^T:")
    else:
        mat(res["C"], "C (rows i = reference pixel, columns j = neighbour):")
    print(f"\nsum C = {fmt(res['N'], dp)}  ->  P = C / {fmt(res['N'], dp)}  (slide 8; features use P, slide 16)")
    mat(res["P"], "P (normalized):")
    print(f"\nper-cell terms (non-zero cells):")
    print(f"  {'i':>2} {'j':>2} {'P':>8} {'(i-j)^2*P':>10} {'P/(1+|i-j|)':>12} {'P^2':>8} {'-P*' + lg + 'P':>10} {'(i-mu1)(j-mu2)P':>16}")
    for t in F["cells"]:
        print(f"  {t['i']:>2} {t['j']:>2} {dec(t['P'], dp):>8} {dec(t['contrast'], dp):>10} {dec(t['homogeneity'], dp):>12} "
              f"{dec(t['asm'], dp):>8} {t['entropy']:>10.{dp}f} {dec(t['cov'], dp):>16}")
    print(f"  {'sum':>5} {'':>8} {dec(F['contrast'], dp):>10} {dec(F['homogeneity'], dp):>12} {dec(F['asm'], dp):>8} "
          f"{F['entropy']:>10.{dp}f} {dec(F['cov'], dp):>16}")
    print("\nmarginals:  p_i (row sums) = [" + ", ".join(dec(p, dp) for p in F["p_i"]) + "]"
          + "   p_j (column sums) = [" + ", ".join(dec(p, dp) for p in F["p_j"]) + "]")
    print(f"  mu1 = sum i*p_i = {fmt(F['mu1'], dp)}   sigma1^2 = {fmt(F['var1'], dp)}   sigma1 = {math.sqrt(float(F['var1'])):.{dp}f}")
    print(f"  mu2 = sum j*p_j = {fmt(F['mu2'], dp)}   sigma2^2 = {fmt(F['var2'], dp)}   sigma2 = {math.sqrt(float(F['var2'])):.{dp}f}")
    print("\nfeatures (slides 16-26):")
    print(f"  1 max probability   max P                     = {fmt(F['max_prob'], dp)}   at {F['max_at']}")
    print(f"  2 ASM (Uniformity, Energy)  sum P^2           = {fmt(F['asm'], dp)}"
          f"   [skimage 'energy' = sqrt(ASM) = {F['sqrt_asm']:.{dp}f}]")
    print(f"  3 contrast          sum (i-j)^2 P             = {fmt(F['contrast'], dp)}")
    print(f"  4 homogeneity       sum P/(1+|i-j|)           = {fmt(F['homogeneity'], dp)}"
          f"   [skimage 'homogeneity' = sum P/(1+(i-j)^2) = {fmt(F['idm'], dp)}]")
    print(f"  5 entropy           -sum P {lg} P              = {F['entropy']:.{dp}f}"
          + ("   [skimage 0.25 'entropy' uses ln]" if res["log_base"] == "2" else ""))
    corr = F["correlation"]
    print(f"  6 correlation       sum (i-mu1)(j-mu2)P/(sigma1 sigma2) = "
          + (fmt(corr, dp) if corr is not None else "undefined (sigma = 0: constant image; skimage reports 1)"))
    sk = res.get("skimage")
    if sk:
        d, a = sk
        print(f"\nskimage equivalent: graycomatrix(I, distances=[{d}], angles=[{a:.6f}], levels={L}, "
              f"symmetric={res['symmetric']}, normed=True)   # angle = {math.degrees(a):g}°")
        print("  NOTE: skimage rows point DOWN, so its pi/4 is DOWN-RIGHT = --dx 1 --dy 1 = --angle 135 here (Haralick 45° is UP-RIGHT)")
    elif res["image"] is not None:
        print("\nskimage equivalent: no exact (distance, angle) pair for this offset")


# ---------------------------------------------------------------- morphology (deck #2 slides 94-116)
OPEN_ORDER = ("erode", "dilate")      # slide 107: A o B = (A ⊖ B) ⊕ B
CLOSE_ORDER = ("dilate", "erode")     # slide 112: A • B = (A ⊕ B) ⊖ B


def se_offsets(se: list[list[int]]) -> list[tuple[int, int]]:
    h, w = len(se), len(se[0])
    if h % 2 == 0 or w % 2 == 0:
        raise ValueError("the SE needs odd height and width (its origin is the centre)")
    cx, cy = h // 2, w // 2
    offs = [(x - cx, y - cy) for x in range(h) for y in range(w) if se[x][y]]
    if not offs:
        raise ValueError("the SE has no 1s")
    return offs


def _check_binary(A):
    for r in A:
        for v in r:
            if v not in (0, 1):
                raise ValueError("morph needs a binary image (0/1); threshold first")


def erode(A, offs, border: str = "zero"):
    """Slide 104: keep (x, y) only if every SE 1 placed at (x, y) lands on a 1 (the SE 'fits').
    border 'zero': outside the image = 0 (slide 115) · 'ignore': outside positions are skipped (skimage default)."""
    H, W = len(A), len(A[0])
    out = [[0] * W for _ in range(H)]
    for x in range(H):
        for y in range(W):
            ok = True
            for ox, oy in offs:
                x2, y2 = x + ox, y + oy
                if 0 <= x2 < H and 0 <= y2 < W:
                    ok = A[x2][y2] == 1
                else:
                    ok = border == "ignore"
                if not ok:
                    break
            out[x][y] = 1 if ok else 0
    return out


def dilate(A, offs, border: str = "zero"):
    """Slide 96: stamp the SE (origin on the pixel) on every 1 = Minkowski sum; an asymmetric SE is NOT mirrored
    the way the 'SE touches a 1 -> centre = 1' shortcut would mirror it. Outside the image is never written."""
    H, W = len(A), len(A[0])
    out = [[0] * W for _ in range(H)]
    for x in range(H):
        for y in range(W):
            if A[x][y]:
                for ox, oy in offs:
                    x2, y2 = x + ox, y + oy
                    if 0 <= x2 < H and 0 <= y2 < W:
                        out[x2][y2] = 1
    return out


def _apply(name: str, A, offs, border: str):
    return erode(A, offs, border) if name == "erode" else dilate(A, offs, border)


def morph(A, op: str, se=None, border: str = "zero") -> dict:
    _check_binary(A)
    se = se or [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    offs = se_offsets(se)
    order = {"erode": ("erode",), "dilate": ("dilate",), "open": OPEN_ORDER, "close": CLOSE_ORDER}[op]
    steps, cur = [], A
    for name in order:
        cur = _apply(name, cur, offs, border)
        steps.append({"step": name, "image": cur, "ones": sum(map(sum, cur))})
    H, W = len(A), len(A[0])
    removed = [(x, y) for x in range(H) for y in range(W) if A[x][y] == 1 and cur[x][y] == 0]
    added = [(x, y) for x in range(H) for y in range(W) if A[x][y] == 0 and cur[x][y] == 1]
    symmetric_se = all(se[x][y] == se[len(se) - 1 - x][len(se[0]) - 1 - y]
                       for x in range(len(se)) for y in range(len(se[0])))
    return {"op": op, "border": border, "se": se, "se_offsets": offs, "se_symmetric": symmetric_se,
            "input": A, "input_ones": sum(map(sum, A)), "steps": steps, "result": cur,
            "ones": sum(map(sum, cur)), "zeros": H * W - sum(map(sum, cur)), "removed": removed, "added": added}


def print_morph(res: dict) -> None:
    names = {"erode": "erosion", "dilate": "dilation"}
    seq = " -> ".join(names[s["step"]] for s in res["steps"])
    print(f"morphology: {res['op']} = {seq}   (deck #2: opening = erosion -> dilation, closing = dilation -> erosion)")
    print(f"border = {res['border']}: " + ("pixels outside the image count as 0 (slide 115)" if res["border"] == "zero"
                                           else "outside positions are skipped in erosion (skimage default) - differs from slide 115 at the edge"))
    print("\nSE (origin = centre, offsets (row, col) = " + ", ".join(str(o) for o in res["se_offsets"]) + "):\n" + grid(res["se"]))
    if not res["se_symmetric"]:
        print("  NOTE: asymmetric SE - dilation stamps it as drawn (slide 96); the 'touches a 1' shortcut would mirror it")
    print(f"\ninput A ({res['input_ones']} ones):\n" + grid(res["input"]))
    for s in res["steps"]:
        print(f"\nafter {names[s['step']]} ({s['ones']} ones):\n" + grid(s["image"]))
    print(f"\nresult: {res['ones']} ones, {res['zeros']} zeros · removed {len(res['removed'])} · added {len(res['added'])}")
    if res["removed"] and len(res["removed"]) <= 24:
        print("  removed (row, col): " + " ".join(str(p) for p in res["removed"]))
    if res["added"] and len(res["added"]) <= 24:
        print("  added   (row, col): " + " ".join(str(p) for p in res["added"]))


# ---------------------------------------------------------------- CLI
def _emit_json(obj) -> None:
    print(json.dumps(jsonable(obj), ensure_ascii=False, indent=1))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="cv_calc", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="machine-readable output")
    common.add_argument("--dp", type=int, default=4, help="decimals shown (slides show 2; display only)")

    h = sub.add_parser("hsv", parents=[common], help="RGB -> HSV with the slide's branch rule")
    h.add_argument("pixels", help='"r g b; r g b; ..." or @file')
    h.add_argument("--h-range", nargs=2, type=float, metavar=("LO", "HI"), help="hue window in degrees; LO > HI wraps through 0")
    h.add_argument("--s-min", type=float, help="minimum saturation to pass (removes gray pixels whose hue is meaningless)")

    g = sub.add_parser("glcm", parents=[common], help="GLCM counts, P and features with every sum term")
    g.add_argument("image", help='"a b c; d e f" (rows; x = row, y = column) or @file')
    g.add_argument("--dx", type=int, default=0, help="row offset (down +), default 0 (slide 5)")
    g.add_argument("--dy", type=int, default=1, help="column offset (right +), default 1 (slide 5)")
    g.add_argument("--angle", type=int, choices=sorted(ANGLE_TO_OFFSET), help="Haralick/MATLAB angle (CCW on screen); overrides --dx/--dy")
    g.add_argument("--d", type=int, default=1, help="distance for --angle")
    g.add_argument("--symmetric", action="store_true", help="C_SYM = C + C^T (slide 11)")
    g.add_argument("--levels", type=int, help="number of gray levels L (default: max value + 1)")
    g.add_argument("--quantize", type=int, metavar="L", help="map 0-255 to L labels first (slide 4)")
    g.add_argument("--log", choices=["2", "e", "10"], default="2", help="entropy log base (slide 18: 2)")
    g.add_argument("--given", action="store_true", help="the input already IS a GLCM (counts or probabilities)")
    g.add_argument("--trace", action="store_true", help="list every counted pixel pair")

    m = sub.add_parser("morph", parents=[common], help="binary erosion/dilation/opening/closing step by step")
    m.add_argument("image", help='binary "0 1 1; 0 1 0" or @file')
    m.add_argument("--op", choices=["erode", "dilate", "open", "close"], required=True)
    m.add_argument("--se", help='structuring element, odd size, origin = centre (default "1 1 1;1 1 1;1 1 1")')
    m.add_argument("--border", choices=["zero", "ignore"], default="zero", help="outside the image: zero (slide 115) | ignore (skimage)")

    a = ap.parse_args(argv)
    try:
        if a.cmd == "hsv":
            px = [tuple(int(float(v)) for v in r) for r in parse_rows(a.pixels)]
            if any(len(p) != 3 for p in px):
                raise ValueError("each pixel needs exactly 3 values r g b")
            res = hsv_table(px, a.h_range, a.s_min)
            if a.json:
                _emit_json({**res, "advisory": ADVISORY})
            else:
                print_hsv(res, a.dp)
                print("\n" + ADVISORY)
        elif a.cmd == "glcm":
            dx, dy = resolve_offset(a.dx, a.dy, a.angle, a.d)
            if a.given:
                res = glcm(given=parse_frac_mat(a.image), symmetric=a.symmetric, log_base=a.log, dx=dx, dy=dy)
            else:
                res = glcm(parse_int_mat(a.image), dx, dy, a.levels, a.symmetric, a.log, a.quantize)
            if a.angle is not None:
                res["angle"] = a.angle
            if a.json:
                out = {k: v for k, v in res.items() if k != "pairs"}
                out["n_pairs"] = len(res["pairs"])
                if a.trace:
                    out["pairs"] = res["pairs"]
                _emit_json({**out, "advisory": ADVISORY})
            else:
                if a.angle is not None:
                    print(f"--angle {a.angle} --d {a.d} (Haralick 1973 / MATLAB, CCW on screen) -> (dx, dy) = ({dx}, {dy})")
                print_glcm(res, a.dp, a.trace)
                print("\n" + ADVISORY)
        else:
            se = parse_int_mat(a.se) if a.se else None
            res = morph(parse_int_mat(a.image), a.op, se, a.border)
            if a.json:
                _emit_json({**res, "advisory": ADVISORY})
            else:
                print_morph(res)
                print("\n" + ADVISORY)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
