from __future__ import division

import numpy as np

from .chunk import chunkify, dechunkify
from .sampling import sampled, get_sample_rate

def hilbert(signal):
    frequencies = np.fft.fft(signal)
    # Remove DC
    frequencies[0] = 0
    # Remove negative frequencies
    frequencies[len(frequencies) // 2:] = 0
    return 2 * np.fft.ifft(frequencies)


def spectrogram(signal, window, overlap):
    return np.array(map(np.fft.rfft, chunkify(signal, window, overlap, ljust=True))).T


@sampled
def spectral_multiply(signal, f, window_size=8192, overlap=64):
    window = np.exp(-np.linspace(-5, 5, window_size) ** 2)
    freq = np.arange(1 + window_size // 2) / window_size * get_sample_rate()

    chunks = []
    t = 0
    dt = window_size / (overlap * get_sample_rate())
    for chunk in chunkify(signal, window, overlap):
        spectrum = f(np.fft.rfft(chunk), t, freq)
        chunks.append(np.fft.irfft(spectrum))
        t += dt
    return dechunkify(chunks, overlap)
