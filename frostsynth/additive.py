from __future__ import division

from numbers import Number

import numpy as np

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
