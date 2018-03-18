import numpy as np


def saw(phase):
    x = phase - np.floor(phase + 0.5)
    return 2 * x


def par(phase):
    x = phase - np.floor(phase + 0.5)
    return 0.5  - 6 * x * x


def par0(phase):
    return par(phase - 0.2886751345948129)


def cub(phase):
    x = phase - np.floor(phase + 0.5)
    return x * (5.19615242270663188 - 20.7846096908265275 * x * x)


def qua(phase):
    x = phase - np.floor(phase + 0.5)
    x2 = x * x
    return 0.875 - x2 * (15 - 30 * x2)


def qua0(phase):
    return qua(phase - 0.2688041932036011)


def qui(phase):
    x = phase - np.floor(phase + 0.5)
    x2 = x * x
    return x * (5.96255602510703402 - x2 * (34.0717487148973373 - 40.8860984578768047 * x2))


def sex(phase):
    x = phase - np.floor(phase + 0.5)
    x2 = x * x
    return 0.96875 - x2 * (18.375 + x2 * (42 * x2 - 52.5))


def sex0(phase):
    return sex(phase - 0.25245928375632665)


def sep(phase):
    x = phase - np.floor(phase + 0.5)
    x2 = x * x
    return x * (x2 * (x2 * (67.13954839183351 - 38.365456223904864 * x2) - 39.164736561902885) + 6.19442261948464)


def oct(phase):
    x = phase - np.floor(phase + 0.5)
    x2 = x * x
    return 0.9921875 - x2 * (19.375 - x2 * (61.25 - x2 * (70 - 30 * x2)))


def oct0(phase):
    return oct(phase - 0.2506196160773293)


def non(phase):
    x = phase - np.floor(phase + 0.5)
    x2 = x * x
    return x * (6.25978410646591 - x2 * (40.74610127043427 - x2 * (77.28615337746888 - x2 *(63.090737450995 - 21.03024581699833 * x2))))
