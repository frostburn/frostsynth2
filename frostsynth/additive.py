from __future__ import division

from numbers import Number

import numpy as np

from .sampling import sampled, integrate, get_sample_rate


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
