import warnings

import numpy as np

from .sampling import sampled, get_sample_rate, integrate, time_like, trange


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


@sampled
def uniform(duration):
    rate = get_sample_rate()
    return np.random.rand(int(round(duration * rate))) * 2 - 1


@sampled
def linsnow(frequency, variation=0.5, duration=None):
    if variation < 0:
        raise ValueError("Lattice variation must be positive")
    elif variation >= 1:
        raise ValueError("Lattice variation too large")
    if duration is None:
        phase = integrate(frequency)
    else:
        phase = trange(duration) * frequency
    total_samples = int(np.ceil(phase[-1]))
    total_samples *= 2  # Some extra buffer due to indeterminancy
    delta = np.ones(total_samples)
    delta += variation * (np.random.rand(total_samples) - np.random.rand(total_samples))
    xp = delta.cumsum()
    if xp[-1] < phase[-1]:
        warnings.warn("Ran out of samples. Snow tail will suffer.")
    fp = np.random.rand(total_samples) * 2 - 1
    return np.interp(phase, xp, fp)
