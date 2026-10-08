"""Oracle tests for scripts/cv_calc.py (cv-judgment: HSV fork F, GLCM fork C / blood-smear step 3, morphology step 2).

Every expected number comes from a source that is NOT this code:
  D1 sN = CMU 261753 deck #1 "Image & Color" (268_ComputerVision_01_261753.pdf), printed slide number N
  D2 sN = deck #2 part 2 "Edge + Morphology" (268_Chapter2_Part2.pdf), printed slide N (slides 94-116 = pdf p.22-40)
  D5 sN = deck #5 "GLCM" (268_ComputerVision_05.pdf), printed slide N (slides 3-12 = pdf p.3-12; 16-26 = pdf p.15-25)
          (course folder: 01_Study_Masters/261753-COMPUTER VISION-Lec.801[2 68]/Course Materials/)
  H73   = Haralick, Shanmugam & Dinstein (1973) IEEE Trans. SMC-3(6):610-621, Fig. 2 (symmetric GLCMs of a 4x4 image)
  [ทดสอบ] lib = value printed by that library on 2026-10-08 (skimage 0.25.2, scipy 1.15.3, OpenCV 4.11.0, Python 3.13
          colorsys) and pasted here as a constant - the libraries are NOT imported when the tests run
  HAND  = arithmetic written out in the comment next to the assert
The must-fail controls inject a trap the card warns about (or a convention another source uses) and require the oracle
to go RED; if a control passes, the oracle could not tell right from wrong.

Run from the repo root:  python -m pytest skills/cv-judgment/evals -q
"""
import json
import math
import os
import subprocess
import sys
from fractions import Fraction

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SCRIPT = os.path.join(SKILL, "scripts", "cv_calc.py")
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import cv_calc as vc  # noqa: E402


def M(s):
    return [[int(v) for v in r.split()] for r in s.strip().split(";")]


def r2(mat):
    return [[round(float(v), 2) for v in r] for r in mat]


def close(a, b, tol=1e-6):
    return abs(float(a) - float(b)) <= tol


# ------------------------------------------------------------------ fixtures from the slides
SLIDE5 = M("3 3 2 1 0 0; 3 3 3 2 1 0; 3 3 2 1 0 0; 2 3 2 2 0 0; 1 2 3 1 1 0; 0 1 2 2 0 0; 0 0 0 1 0 0")
HARALICK = M("0 0 1 1; 0 0 1 1; 0 2 2 2; 2 2 3 3")
SLIDE22_26_C = [[Fraction("0"), Fraction("0.2"), Fraction("0")],
                [Fraction("0"), Fraction("0"), Fraction("0")],
                [Fraction("0.2"), Fraction("0"), Fraction("0.6")]]

A96 = M("0 0 0 0 0 0 0 0 0;0 1 0 0 0 1 0 0 0;0 0 0 0 0 1 1 0 0;0 0 0 0 0 0 0 0 0;"
        "0 0 1 0 0 0 0 0 0;0 0 1 0 0 0 0 0 0;0 1 0 0 0 1 1 1 0;0 0 0 0 0 0 0 0 0")
SE96 = M("0 1 0;0 1 1;0 0 0")
OUT96 = M("0 1 0 0 0 1 0 0 0;0 1 1 0 0 1 1 0 0;0 0 0 0 0 1 1 1 0;0 0 1 0 0 0 0 0 0;"
          "0 0 1 1 0 0 0 0 0;0 1 1 1 0 1 1 1 0;0 1 1 0 0 1 1 1 1;0 0 0 0 0 0 0 0 0")
A98 = M("0 0 0 0 0 0 0 0 0;0 0 0 0 1 1 1 0 0;0 1 0 0 0 0 0 0 0;0 1 0 0 1 1 1 0 0;"
        "0 1 0 0 1 1 1 0 0;0 1 0 0 1 1 1 1 0;0 1 0 0 1 1 1 0 0;0 0 0 0 0 0 0 0 0")
SE98 = M("0 0 1 0 0;0 0 1 0 0;1 1 1 1 1;0 0 1 0 0;0 0 1 0 0")
OUT98 = M("0 1 0 0 1 1 1 0 0;0 1 1 1 1 1 1 1 1;1 1 1 1 1 1 1 0 0;1 1 1 1 1 1 1 1 1;"
          "1 1 1 1 1 1 1 1 1;1 1 1 1 1 1 1 1 1;1 1 1 1 1 1 1 1 1;0 1 0 0 1 1 1 1 0")
A104 = M("0 0 0 0 0 0 0 0 0;0 0 0 1 1 1 0 0 0;0 0 0 1 1 1 1 0 0;0 0 1 1 0 0 1 0 0;"
         "0 0 1 0 1 1 1 0 0;0 0 1 0 0 1 0 0 0;0 0 0 0 1 1 1 0 0;0 0 0 0 0 0 0 0 0")
SE104 = M("0 1 0;1 1 1;0 0 0")
HSE = M("0 0 0;1 1 1;0 0 0")               # D2 s107-115: horizontal 1x3 SE inside a 3x3 frame
A108 = M("0 0 0 0 0 0 0 0 0;0 1 1 1 0 0 0 0 0;0 0 1 0 0 0 0 1 0;0 0 1 0 0 1 0 1 0;"
         "0 0 0 0 0 0 0 1 0;0 0 0 0 0 0 0 0 0;0 0 1 1 1 1 1 0 0;0 0 0 0 0 0 0 0 0")
OUT108 = M("0 0 0 0 0 0 0 0 0;0 1 1 1 0 0 0 0 0;0 0 0 0 0 0 0 0 0;0 0 0 0 0 0 0 0 0;"
           "0 0 0 0 0 0 0 0 0;0 0 0 0 0 0 0 0 0;0 0 1 1 1 1 1 0 0;0 0 0 0 0 0 0 0 0")
A113 = M("0 0 0 0 0 0 0 0 0;0 1 0 1 0 1 0 1 0;0 0 0 0 0 0 0 0 0;0 1 0 0 0 0 0 1 0;"
         "0 0 0 0 0 0 0 0 0;0 1 0 0 0 0 0 1 0;0 0 1 0 1 0 1 0 0;0 0 0 0 0 0 0 0 0")
DIL114 = M("0 0 0 0 0 0 0 0 0;1 1 1 1 1 1 1 1 1;0 0 0 0 0 0 0 0 0;1 1 1 0 0 0 1 1 1;"
           "0 0 0 0 0 0 0 0 0;1 1 1 0 0 0 1 1 1;0 1 1 1 1 1 1 1 0;0 0 0 0 0 0 0 0 0")
OUT115 = M("0 0 0 0 0 0 0 0 0;0 1 1 1 1 1 1 1 0;0 0 0 0 0 0 0 0 0;0 1 0 0 0 0 0 1 0;"
           "0 0 0 0 0 0 0 0 0;0 1 0 0 0 0 0 1 0;0 0 1 1 1 1 1 0 0;0 0 0 0 0 0 0 0 0")


# ------------------------------------------------------------------ oracle checks (shared by tests and controls)
def check_hsv_slides():
    a = vc.rgb_to_hsv(128, 0, 0)                                   # D1 s21: h = 0, v = 128/255 = 0.5, s = 1
    assert (a["h"], round(float(a["v"]), 2), a["s"]) == (0, 0.5, 1)
    b = vc.rgb_to_hsv(250, 30, 30)                                 # D1 s22: h = 0, v = 0.98, s = 0.88
    assert (b["h"], round(float(b["v"]), 2), round(float(b["s"]), 2)) == (0, 0.98, 0.88)
    c = vc.rgb_to_hsv(128, 128, 0)                                 # D1 s23: tie r = g -> M = r row -> 60°
    assert (c["branch"], c["h"], round(float(c["v"]), 2), c["s"]) == ("M=r", 60, 0.5, 1)
    d = vc.rgb_to_hsv(100, 0, 200)                                 # D1 s25: M = b row, h = 0.5*60 + 240 = 270
    assert (d["branch"], d["h"], round(float(d["v"]), 2), d["s"]) == ("M=b", 270, 0.78, 1)


def check_hsv_negative_raw_hue():
    p = vc.rgb_to_hsv(255, 0, 128)
    assert p["branch"] == "M=r" and close(p["h"], 329.8824, 1e-4)  # [ทดสอบ] OpenCV 4.11 + colorsys: 329.8824
    q = vc.rgb_to_hsv(230, 150, 170)
    assert q["h"] == 345                                            # HAND: (150-170)/80*60 = -15 -> mod 360 = 345


def check_slide8(res):
    assert res["C"] == [[7, 2, 0, 0], [5, 1, 2, 0], [2, 3, 2, 2], [0, 1, 4, 4]]        # D5 s5 / s8
    assert res["N"] == 35
    assert r2(res["P"]) == [[0.20, 0.06, 0, 0], [0.14, 0.03, 0.06, 0],
                            [0.06, 0.09, 0.06, 0.06], [0, 0.03, 0.11, 0.11]]          # D5 s8 joint probabilities


def check_slide12(res):
    assert res["C"] == [[14, 7, 2, 0], [7, 2, 5, 1], [2, 5, 4, 6], [0, 1, 6, 8]]       # D5 s12
    assert r2(res["P"]) == [[0.20, 0.10, 0.03, 0], [0.10, 0.03, 0.07, 0.01],
                            [0.03, 0.07, 0.06, 0.09], [0, 0.01, 0.09, 0.11]]          # D5 s12 (Normalized)


H73_SYM = {0: [[4, 2, 1, 0], [2, 4, 0, 0], [1, 0, 6, 1], [0, 0, 1, 2]],
           45: [[4, 1, 0, 0], [1, 2, 2, 0], [0, 2, 4, 1], [0, 0, 1, 0]],
           90: [[6, 0, 2, 0], [0, 4, 2, 0], [2, 2, 2, 2], [0, 0, 2, 0]],
           135: [[2, 1, 3, 0], [1, 2, 1, 0], [3, 1, 0, 2], [0, 0, 2, 0]]}
# [ทดสอบ] skimage 0.25.2 graycomatrix(symmetric=True): angle 0 -> H73 0°, pi/2 -> H73 90°, but pi/4 -> H73 *135°*
#         and 3pi/4 -> H73 *45°* (skimage rows point down) - the reason --angle follows H73 and prints the skimage call.


def check_haralick_angles():
    for ang, expected in H73_SYM.items():
        dx, dy = vc.resolve_offset(0, 1, ang, 1)
        assert vc.glcm(HARALICK, dx, dy, levels=4, symmetric=True)["C"] == expected, ang


def check_haralick_features(F):
    # HAND on H73 0° (sum 24): contrast = (2*1 + 2*1 + 1*4 + 1*4 + 1*1 + 1*1)/24 = 14/24 = 7/12
    assert F["contrast"] == Fraction(7, 12)                         # [ทดสอบ] skimage 'contrast' 0.5833333333
    # HAND: homogeneity |i-j| = (16 + 6/2 + 2/3)/24 = 59/72 (D5 s18 form; skimage has no such property)
    assert F["homogeneity"] == Fraction(59, 72)
    assert F["idm"] == Fraction(97, 120)                            # [ทดสอบ] skimage 'homogeneity' 0.8083333333
    assert F["asm"] == Fraction(7, 48)                              # HAND 84/576 · [ทดสอบ] skimage 'ASM' 0.1458333333
    assert close(F["sqrt_asm"], 0.38188130791298663)               # [ทดสอบ] skimage 'energy' (= sqrt ASM)
    assert F["correlation"] == Fraction(431, 599)                   # HAND cov 431/576 / var 599/576 · skimage 0.7195325543
    assert F["max_prob"] == Fraction(1, 4)                          # HAND 6/24


def check_entropy_log2(F):
    # [ทดสอบ] skimage 0.25.2 'entropy' (natural log) = 2.0947290475276485 -> D5 s18 uses log2: / ln 2 = 3.0220552088
    assert close(F["entropy"], 2.0947290475276485 / math.log(2), 1e-9)


def check_slide26(F):
    assert (F["mu1"], F["mu2"]) == (Fraction(8, 5), Fraction(7, 5))                    # D5 s24-25: 1.6, 1.4
    assert (F["var1"], F["var2"]) == (Fraction(16, 25), Fraction(16, 25))              # D5 s24-25: sigma 0.8, 0.8
    assert F["correlation"] == Fraction(1, 4)                                          # D5 s26: 0.25


def check_slide108(res):
    assert res["steps"][0]["step"] == "erode"
    assert [(x, y) for x, r in enumerate(res["steps"][0]["image"]) for y, v in enumerate(r) if v] == \
        [(1, 2), (6, 3), (6, 4), (6, 5)]                                               # D2 s109 erosion image
    assert res["result"] == OUT108                                                     # D2 s108/s110 output


def check_slide115(res):
    assert res["steps"][0]["image"] == DIL114                                          # D2 s114 dilation image
    assert res["result"] == OUT115                                                     # D2 s113/s115 output


# ------------------------------------------------------------------ HSV
def test_hsv_slides_21_22_23_25():
    check_hsv_slides()


def test_hsv_mod_360_and_negative_raw_hue():
    check_hsv_negative_raw_hue()


def test_hsv_trap1_same_stain_two_lightings():
    res = vc.hsv_table([(180, 60, 200), (90, 30, 100)])
    a, b = res["pixels"]
    assert close(a["h"], 291.4286, 1e-4) and close(b["h"], 291.4286, 1e-4)      # [ทดสอบ] OpenCV 4.11: 291.4286 both
    assert a["s"] == b["s"] == Fraction(7, 10)                                    # [ทดสอบ] OpenCV 4.11: s 0.700000 both
    assert close(a["v"], 0.784314) and close(b["v"], 0.392157)                    # [ทดสอบ] OpenCV 4.11
    assert b["dh_vs_1"] == 0 and close(b["rgb_dist_vs_1"], math.sqrt(19000))      # HAND: 90²+30²+100² = 19000 -> 137.84


def test_hsv_gray_and_wrapping_window():
    res = vc.hsv_table([(200, 200, 200), (250, 30, 30), (230, 150, 170), (180, 60, 200)], h_range=(330, 30))
    assert [p["pass"] for p in res["pixels"]] == [False, True, True, False]       # gray h=0 is undefined, not red
    res = vc.hsv_table([(200, 200, 200), (180, 60, 200)], h_range=(270, 320), s_min=0.2)
    assert [p["pass"] for p in res["pixels"]] == [False, True]


# ------------------------------------------------------------------ GLCM
def test_glcm_slide5_8_asymmetric_counts_and_P():
    res = vc.glcm(SLIDE5, 0, 1, levels=4)
    check_slide8(res)
    assert len(res["pairs"]) == 35                                                 # HAND: 7 rows x 5 right-neighbours


def test_glcm_slide10_diagonal_offsets_are_transposes():
    a = vc.glcm(SLIDE5, 1, -1, levels=4)
    b = vc.glcm(SLIDE5, -1, 1, levels=4)
    assert a["C"] == [[4, 4, 2, 0], [1, 1, 3, 1], [3, 0, 2, 3], [0, 2, 1, 3]]       # D5 s10 C_ASYM(1,-1)
    assert b["C"] == [[4, 1, 3, 0], [4, 1, 0, 2], [2, 3, 2, 1], [0, 1, 3, 3]]       # D5 s10 C_ASYM(-1,1)
    assert r2(a["P"])[0] == [0.13, 0.13, 0.07, 0] and r2(b["P"])[1] == [0.13, 0.03, 0, 0.07]   # D5 s10
    assert b["C"] == vc.transpose(a["C"])                                          # D5 s11 note


def test_glcm_slide12_symmetric():
    check_slide12(vc.glcm(SLIDE5, 0, 1, levels=4, symmetric=True))


def test_glcm_slide26_correlation_of_a_given_matrix():
    check_slide26(vc.glcm(given=SLIDE22_26_C)["features"])


def test_glcm_haralick_1973_fig2_four_angles():
    check_haralick_angles()


def test_glcm_haralick_features_hand_and_skimage():
    F = vc.glcm(HARALICK, 0, 1, levels=4, symmetric=True)["features"]
    check_haralick_features(F)
    check_entropy_log2(F)


def test_glcm_slide_image_features_vs_skimage():
    F = vc.glcm(SLIDE5, 0, 1, levels=4)["features"]
    assert F["contrast"] == Fraction(6, 7)                 # HAND 30/35 · [ทดสอบ] skimage 'contrast' 0.8571428571
    assert F["homogeneity"] == Fraction(24, 35)            # HAND (14 + 18/2 + 3/3)/35 (D5 s18 form)
    assert close(F["idm"], 0.6742857142857143)             # [ทดสอบ] skimage 'homogeneity'
    assert F["asm"] == Fraction(137, 1225)                 # HAND sum c^2 = 137 · [ทดสอบ] skimage 'ASM' 0.1118367347
    assert close(F["correlation"], 0.7114672772718791)     # [ทดสอบ] skimage 'correlation' (asymmetric)
    assert close(F["entropy"], 2.327170228171682 / math.log(2), 1e-9)   # [ทดสอบ] skimage 'entropy' (ln) / ln 2


def test_glcm_quantize_slide4_bins():
    q = vc.quantize([[0, 63, 64, 127], [128, 191, 192, 255]], 4)
    assert q == [[0, 0, 1, 1], [2, 2, 3, 3]]               # D5 s4: 0-63 -> 0, 64-127 -> 1, 128-191 -> 2, 192-255 -> 3


def test_glcm_slide19_20_stripes_follow_the_axis_convention():
    stripes = M("0 1 0 1; 0 1 0 1; 0 1 0 1; 0 1 0 1")    # D5 s19-20 quiz idea: vertical stripes
    horiz = vc.glcm(stripes, 0, 1, levels=2, symmetric=True)["features"]
    vert = vc.glcm(stripes, 1, 0, levels=2, symmetric=True)["features"]
    assert horiz["contrast"] == 1 and horiz["homogeneity"] == Fraction(1, 2)       # HAND: every right-pair differs
    assert vert["contrast"] == 0 and vert["homogeneity"] == 1                       # HAND: every down-pair is equal


def test_glcm_constant_image_uniformity_one_and_correlation_undefined():
    F = vc.glcm(M("2 2 2; 2 2 2"), 0, 1, levels=3, symmetric=True)["features"]
    assert F["asm"] == 1 and F["correlation"] is None                              # D5 s16: Uniformity = 1 if constant


def test_glcm_prints_the_matching_skimage_call():
    assert vc.skimage_equivalent(0, 1) == (1, 0.0)
    d, a = vc.skimage_equivalent(1, 1)
    assert d == 1 and close(a, math.pi / 4)               # skimage pi/4 = DOWN-RIGHT = Haralick 135°
    d, a = vc.skimage_equivalent(-1, 1)
    assert close(a, 7 * math.pi / 4)                      # Haralick 45° (up-right) = skimage 7pi/4 (or 3pi/4 if symmetric)


# ------------------------------------------------------------------ morphology
def test_morph_slide96_dilation_stamps_an_asymmetric_se():
    assert vc.morph(A96, "dilate", SE96)["result"] == OUT96   # D2 s96 · [ทดสอบ] scipy binary_dilation identical


def test_morph_slide98_dilation_plus_se_has_12_zeros():
    res = vc.morph(A98, "dilate", SE98)
    assert res["result"] == OUT98 and res["zeros"] == 12      # D2 s98 "How many zeros?" · [ทดสอบ] scipy: 12


def test_morph_slide104_erosion_three_ones():
    res = vc.morph(A104, "erode", SE104)
    assert res["ones"] == 3 and res["removed"] and \
        [(x, y) for x, r in enumerate(res["result"]) for y, v in enumerate(r) if v] == [(2, 4), (2, 5), (6, 5)]   # D2 s104


def test_morph_slide108_110_opening():
    check_slide108(vc.morph(A108, "open", HSE))


def test_morph_slide113_115_closing():
    check_slide115(vc.morph(A113, "close", HSE))


def test_morph_teaching_mask_open_vs_close():
    A = vc.parse_int_mat("@data/smear_mask_12x12.txt")
    op, cl = vc.morph(A, "open"), vc.morph(A, "close")
    assert op["ones"] == 9 and cl["ones"] == 20               # [ทดสอบ] scipy 1.15.3 + skimage 0.25.2: 9 and 20
    assert cl["added"] == [(8, 8)] and cl["removed"] == []    # closing fills the ring's hole, keeps both specks
    assert (2, 9) in op["removed"] and (9, 2) in op["removed"] and op["added"] == []   # opening drops specks + ring
    assert vc.morph(A, "close", border="ignore")["result"] == cl["result"]             # objects away from the edge


def test_morph_border_ignore_matches_skimage_default():
    res = vc.morph(A113, "close", HSE, border="ignore")
    # [ทดสอบ] skimage 0.25.2 binary_closing(A113, footprint) default mode -> rows 1/3/5 keep the edge columns
    assert ["".join(map(str, r)) for r in res["result"]] == [
        "000000000", "111111111", "000000000", "110000011", "000000000", "110000011", "001111100", "000000000"]


# ------------------------------------------------------------------ CLI
def run(*args, env_extra=None, cwd=None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    env.update(env_extra or {})
    return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True, encoding="utf-8",
                          env=env, cwd=cwd or SKILL)


def test_cli_help_json_and_advisory(tmp_path):
    for args in ([], ["hsv"], ["glcm"], ["morph"]):
        r = run(*args, "--help", env_extra={"PYTHONIOENCODING": "cp874"})        # Thai Windows console
        assert r.returncode == 0 and "usage" in r.stdout, r.stderr
    j = json.loads(run("hsv", "100 0 200", "--json").stdout)
    assert j["pixels"][0]["h"] == 270 and "ADVISORY" in j["advisory"]
    j = json.loads(run("glcm", "@data/glcm_slide5_7x6.txt", "--json").stdout)
    assert j["C"] == [[7, 2, 0, 0], [5, 1, 2, 0], [2, 3, 2, 2], [0, 1, 4, 4]] and j["n_pairs"] == 35
    j = json.loads(run("morph", "@data/smear_mask_12x12.txt", "--op", "open", "--json").stdout)
    assert j["ones"] == 9
    t = run("glcm", "@data/haralick1973_4x4.txt", "--angle", "45", "--symmetric", cwd=str(tmp_path))  # @file from any cwd
    assert t.returncode == 0 and "ADVISORY:" in t.stdout and "C_SYM" in t.stdout and "skimage equivalent" in t.stdout
    assert run("morph", "0 2 1", "--op", "open").returncode == 2                  # non-binary input is refused


# ------------------------------------------------------------------ must-fail controls
def test_must_fail_control_hue_without_mod_360(monkeypatch):
    monkeypatch.setattr(vc, "_wrap360", lambda h: h)              # forget "mod 360°" in the M = r row (D1 s20)
    with pytest.raises(AssertionError):
        check_hsv_negative_raw_hue()


def test_must_fail_control_hue_branch_offsets_swapped(monkeypatch):
    monkeypatch.setattr(vc, "HUE_OFFSET", {"r": 0, "g": 240, "b": 120})   # +120 / +240 put on the wrong rows
    with pytest.raises(AssertionError):
        check_hsv_slides()


def test_must_fail_control_glcm_axes_swapped(monkeypatch):
    monkeypatch.setattr(vc, "_neighbour", lambda x, y, dx, dy: (x + dy, y + dx))   # read x as column (deck #1 habit)
    with pytest.raises(AssertionError):
        check_slide8(vc.glcm(SLIDE5, 0, 1, levels=4))


def test_must_fail_control_glcm_offset_reversed(monkeypatch):
    monkeypatch.setattr(vc, "_neighbour", lambda x, y, dx, dy: (x - dx, y - dy))   # count j -> i instead of i -> j
    with pytest.raises(AssertionError):
        check_slide8(vc.glcm(SLIDE5, 0, 1, levels=4))


def test_must_fail_control_glcm_not_symmetrized(monkeypatch):
    monkeypatch.setattr(vc, "symmetrize", lambda C: C)            # "--symmetric" silently ignored
    with pytest.raises(AssertionError):
        check_slide12(vc.glcm(SLIDE5, 0, 1, levels=4, symmetric=True))


def test_must_fail_control_glcm_features_on_raw_counts(monkeypatch):
    monkeypatch.setattr(vc, "normalize", lambda C: ([[Fraction(c) for c in r] for r in C], 1))   # skip P = C / sum
    with pytest.raises(AssertionError):
        check_haralick_features(vc.glcm(HARALICK, 0, 1, levels=4, symmetric=True)["features"])


def test_must_fail_control_glcm_skimage_angle_map(monkeypatch):
    monkeypatch.setattr(vc, "ANGLE_TO_OFFSET", {0: (0, 1), 45: (1, 1), 90: (1, 0), 135: (1, -1)})   # rows-down angles
    with pytest.raises(AssertionError):
        check_haralick_angles()


def test_must_fail_control_homogeneity_squared_denominator(monkeypatch):
    monkeypatch.setattr(vc, "_w_homogeneity", vc._w_idm)          # skimage's 1/(1+(i-j)^2) instead of D5 s18
    with pytest.raises(AssertionError):
        check_haralick_features(vc.glcm(HARALICK, 0, 1, levels=4, symmetric=True)["features"])


def test_must_fail_control_entropy_natural_log():
    F = vc.glcm(HARALICK, 0, 1, levels=4, symmetric=True, log_base="e")["features"]   # skimage's ln, not D5 s18 log2
    with pytest.raises(AssertionError):
        check_entropy_log2(F)


def test_must_fail_control_opening_closing_swapped(monkeypatch):
    monkeypatch.setattr(vc, "OPEN_ORDER", ("dilate", "erode"))    # card trap: Opening <-> Closing
    with pytest.raises(AssertionError):
        check_slide108(vc.morph(A108, "open", HSE))


def test_must_fail_control_dilation_touch_rule_mirrors_se(monkeypatch):
    def touch_rule(A, offs, border="zero"):                        # "SE touches a 1 -> centre = 1" (no stamping)
        H, W = len(A), len(A[0])
        return [[1 if any(0 <= x + ox < H and 0 <= y + oy < W and A[x + ox][y + oy] for ox, oy in offs) else 0
                 for y in range(W)] for x in range(H)]
    monkeypatch.setattr(vc, "dilate", touch_rule)
    with pytest.raises(AssertionError):
        assert vc.morph(A96, "dilate", SE96)["result"] == OUT96


def test_must_fail_control_border_ignore_breaks_slide115():
    with pytest.raises(AssertionError):
        check_slide115(vc.morph(A113, "close", HSE, border="ignore"))   # skimage default edge handling
