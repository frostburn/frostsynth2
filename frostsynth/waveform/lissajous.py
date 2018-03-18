from __future__ import division

import numpy as np

from .trig import sine

EPSILON = 1e-12


def lissajous11(phase, sharpness=0):
    too_small = (abs(sharpness) < EPSILON)
    s = np.clip(sharpness, EPSILON - 1, 1 - EPSILON)
    x = np.pi * (phase - np.floor(phase + 0.5))
    a = 1 + s
    b = 1 - s
    return np.where(
        too_small,
        sine(phase),
        (np.arctan2(a**2 * np.sin(x), b**2 * np.cos(x)) - x) /
        (2 * np.arctan2(b, a) - 0.5 * np.pi)
    )


def lissajous12(phase, sharpness=0, bias=0):
    s = np.clip(sharpness, -1, 1)
    b = 0.5 * np.pi * np.clip(bias, EPSILON - 1, 1 - EPSILON)
    return np.arctan2(
        (1 + s) * np.sin(2 * np.pi * phase),
        (1 - s) * np.cos(4 * np.pi * phase + b)
    ) * 4 / (3 * np.pi)


def lissajous13(phase, sharpness=0, bias=0):
    x = phase - np.floor(phase + 0.5)
    s = np.clip(sharpness, -1, 1)
    b = np.pi / 6 * np.clip(bias, EPSILON - 1, 1 - EPSILON)
    return np.arctan2(
        (1 + s) * np.sin(3 * np.pi * x),
        (1 - s) * np.cos(np.pi * x + b)
    ) * 2 / np.pi + 2 * x


# def lissajous14(phase, sharpness=0, bias=0):
#     s = clip(sharpness, -1, 1)
#     b = pi_per_eight * clip(bias, EPSILON - 1, 1 - EPSILON)
#     return atan2((1 - s) * cos(two_pi * phase + b), (1 + s) * cos(eight_pi * phase)) * 0.39328116619206743


# def lissajous15(phase, sharpness=0, bias=0):
#     x = phase - floor(phase + 0.5)
#     s = clip(sharpness, -1, 1)
#     b = pi_per_ten * clip(bias, EPSILON - 1, 1 - EPSILON)
#     return atan2((1 + s) * sin(five_pi * x), (1 - s) * cos(pi * x + b)) * 0.4754858297894094 - 1.4937827897524554 * x


# def lissajous16(phase, sharpness=0, bias=0):
#     s = clip(sharpness, -1, 1)
#     b = half_pi * clip(bias, EPSILON - 1, 1 - EPSILON)
#     return atan2((1 - s) * sin(two_pi * phase), (1 + s) * cos(twelve_pi * phase + b)) * 0.3708887239244341


def lissajous23(phase, sharpness=0, bias=0):
    x = phase - np.floor(phase + 0.5)
    s = np.clip(sharpness, -1, 1)
    b = np.pi / 6 * np.clip(bias, EPSILON - 1, 1 - EPSILON)
    l = np.arctan2(
        (1 + s) * np.sin(6 * np.pi * x),
        (1 - s) * np.cos(4 * np.pi * x + b)
    )
    l += 2 * np.pi * (x > 0) * (l < 0)
    l -= 2 * np.pi * (x < 0) * (l > 0)

    return l * 4 / (5 * np.pi)


# def lissajous25(phase, sharpness=0, bias=0):
#     x = phase - floor(phase + 0.5)
#     s = clip(sharpness, -1, 1)
#     b = pi_per_ten * clip(bias, EPSILON - 1, 1 - EPSILON)
#     l = atan2((-1 - s) * sin(ten_pi * x), (1 - s) * cos(four_pi * x + b))
#     if 0.15 < x < 0.35 and l < 0:
#         l += two_pi
#     elif -0.35 < x < -0.15 and l > 0:
#         l -= two_pi
#     return l * four_fifths_per_pi


# def lissajous34(phase, sharpness=0, bias=0):
#     x = phase - floor(phase + 0.5)
#     s = clip(sharpness, -1, 1)
#     b = pi_per_six * clip(bias, EPSILON - 1, 1 - EPSILON)
#     l = atan2((1 - s) * sin(six_pi * x), (1 + s) * cos(eight_pi * x + b))
#     if 0.1 < x < 0.4 and l < 0:
#         l += two_pi
#     elif -0.4 < x < -0.1 and l > 0:
#         l -= two_pi
#     return l * four_sevenths_per_pi


# def lissajous35(phase, sharpness=0, bias=0):
#     x = phase - floor(phase + 0.5)
#     s = clip(sharpness, -1, 1)
#     b = pi_per_ten * clip(bias, EPSILON - 1, 1 - EPSILON)
#     l = atan2((1 + s) * sin(five_pi * x), (1 - s) * cos(three_pi * x + b))
#     if x > 0 and l < 0:
#         l += two_pi
#     elif x < 0 and l > 0:
#         l -= two_pi
#     return l * one_per_pi - x


# def lissajous45(phase, sharpness=0, bias=0):
#     x = phase - floor(phase + 0.5)
#     s = clip(sharpness, -1, 1)
#     b = pi_per_ten * clip(bias, EPSILON - 1, 1 - EPSILON)
#     l = atan2((1 + s) * sin(ten_pi * x), (1 - s) * cos(eight_pi * x + b))
#     if (x > 0 and l < 0) or (0.15 < x < 0.35):
#         l += two_pi
#     elif (x < 0 and l > 0) or (-0.35 < x < -0.15):
#         l -= two_pi
#     return l * four_ninths_per_pi


# def lissajous56(phase, sharpness=0, bias=0):
#     x = phase - floor(phase + 0.5)
#     s = clip(sharpness, -1, 1)
#     b = pi_per_ten * clip(bias, EPSILON - 1, 1 - EPSILON)
#     l = atan2((1 - s) * sin(ten_pi * x), (1 + s) * cos(twelve_pi * x + b))
#     if (x > 0 and l < 0) or (0.15 < x < 0.35):
#         l += two_pi
#     elif (x < 0 and l > 0) or (-0.35 < x < -0.15):
#         l -= two_pi
#     return l * four_elevenths_per_pi
