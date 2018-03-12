from numpy import cumsum, concatenate, pi


tau = 2 * pi


def cumsum0(signal):
    return concatenate(([0], cumsum(signal)))
