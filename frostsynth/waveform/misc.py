import numpy as np


def twine(phase):
    x = phase - np.floor(phase + 0.5)
    return 4 * x * np.sqrt(1 - 4 * x * x)


def halfcircle_dc(phase):
    x = phase - np.floor(phase + 0.5)
    return np.sqrt(1 - 4 * x * x)


def halfcircle(phase):
    x = phase - np.floor(phase + 0.5)
    return np.sqrt(1.6211389382774044 - 6.484555753109618 * x * x) - 1


def tang(phase):
    x = phase - np.floor(phase + 0.5)
    return np.where(
        abs(x) < 0.499,
        (np.tanh(np.tan(np.pi * phase)) - 2 * x) * 3.5686502577037404,
        7.137300515407481 * (0.5 - phase + np.floor(phase)),
    )


def pinch(phase):
    x = phase - np.floor(phase + 0.5)
    return np.arctan(np.arctanh(0.99 - 1.98 * abs(x + x))) * 0.82675935153194158


def tooth(phase, tension=1):
    return np.tanh(tension * np.tan(np.pi * phase) ** 2) * 2 - 1


def tri(phase, tension=1):
    x = phase - np.floor(phase + 0.5)
    return np.tanh(abs(tension) * np.tan(2 * np.pi * abs(x) - 0.5 * np.pi))
