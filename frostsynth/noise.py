import numpy as np

from .sampling import sampled, get_sample_rate


def acolored(length, color):
    if color == 0:
        return np.random.randn(length)
    uneven = length % 2
    N = length // 2 + 1 + uneven
    f = np.arange(N, dtype=float)
    z = np.random.randn(N) + 1j * np.random.randn(N)
    if color < 0:
        f[0] = float("inf")
    noise = np.fft.irfft(z * f ** color)
    return noise * length ** (0.5 - color)


@sampled
def colored(duration, color):
    return acolored(int(round(duration * get_sample_rate())), color)


@sampled
def red(duration):
    return colored(duration, -1)


@sampled
def pink(duration):
    return colored(duration, -0.5)


@sampled
def white(duration):
    return colored(duration, 0)


@sampled
def blue(duration):
    return colored(duration, 0.5)


@sampled
def brownian(duration):
    """
    Brownian motion.
    Same power density as red() but has different characteristics at DC.
    """
    rate = get_sample_rate()
    return np.cumsum(np.random.randn(int(round(duration * rate))) * rate ** -0.5)
