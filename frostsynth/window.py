from numpy import arange, cos, pi, zeros, concatenate


def pad(window, width):
    return concatenate((zeros(width), window, zeros(width)))


def cosine(width):
    return 0.5 - cos(arange(width) * 2 * pi / width) * 0.5
