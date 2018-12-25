from __future__ import division
import numpy as np

from frostsynth import sampling
from frostsynth import analysis


def test_spectral_envelope_identity():
    sampling.set_sample_rate(16)
    signal = sampling.trange(2.1)
    res = analysis.spectral_envelope(signal, lambda t, f: 1)
    assert np.allclose(signal, res)
