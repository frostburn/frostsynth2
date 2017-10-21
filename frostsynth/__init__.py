from numpy import cumsum, concatenate


def cumsum0(signal):
    return concatenate(([0], cumsum(signal)))
    