from __future__ import division

from numbers import Number

import numpy as np
from scipy.interpolate import CubicSpline

from .sampling import sampled, trange, integrate, get_sample_rate
from . import tau


@sampled
def harmonics(freq, weights):
    if isinstance(freq, Number):
        phase = np.arange(len(weights[0])) * freq / get_sample_rate()
    else:
        phase = integrate(freq)
    z = np.exp(2j * np.pi * phase)
    result = 0
    for w in reversed(weights):
        result = z * result + w
    return result


@sampled
def sinepings(duration, params):
    # XXX: There is a cheap way to generate these using IIR filters.
    # Somehow scipy.signal.lfilter seems to be slower so using numpy for now.
    t = trange(duration)
    return sum(w * np.sin(tau * f * t) * np.exp(-t * d) for f, w, d in params)


def make_periodic(samples):
    phase = np.arange(len(samples) + 1) / len(samples)
    samples = np.concatenate((samples, [samples[0]]))
    return CubicSpline(phase, samples, bc_type="periodic")


def fourier(weights):
    samples = np.fft.irfft(weights) * len(weights)
    return make_periodic(samples)


def make_pad(f, num_harmonics, oversampling):
    freq = np.arange((num_harmonics + 1) * oversampling) / oversampling
    density = f(freq)
    if not np.iscomplexobj(freq):
        density = density * (np.random.randn(len(density)) + 1j * np.random.randn(len(density)))
    samples = np.fft.irfft(density) * len(density)
    phase = np.arange(len(samples) + 1) * oversampling / len(samples)
    samples = np.concatenate((samples, [samples[0]]))
    return CubicSpline(phase, samples, bc_type="periodic")
