import numpy as np

tau = 2 * np.pi


def cumsum0(signal):
    return np.concatenate(([0], np.cumsum(signal)))


def raised_cosine(t):
    return 0.5 * np.cos(tau * t) + 0.5


def raised_tanh(t):
    return 0.5 * np.tanh(t) + 0.5
