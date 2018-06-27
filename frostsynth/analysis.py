from __future__ import division

import numpy as np
# from matplotlib.pyplot import imshow, xticks, yticks

from .chunk import chunkify, dechunkify
from .sampling import sampled, get_sample_rate, dur

def hilbert(signal):
    frequencies = np.fft.fft(signal)
    # Remove DC
    frequencies[0] = 0
    # Remove negative frequencies
    frequencies[len(frequencies) // 2:] = 0
    return 2 * np.fft.ifft(frequencies)


def spectrogram(signal, window, overlap):
    return np.array(map(np.fft.rfft, chunkify(signal, window, overlap, ljust=True))).T


# @sampled
# def pltspec(signal, freq_max=None):
#     window_size = 2048
#     overlap = 32
#     ratio = 1
#     if freq_max is not None:
#         ratio = 2 * freq_max / get_sample_rate()
#         window_size = int(window_size / ratio)
#         overlap = int(overlap / ratio)
#     x = np.arange(window_size) / window_size * 8 - 4
#     window = np.exp(-x*x)
#     spec = abs(spectrogram(signal, window, overlap))
#     height, width = spec.shape
#     if freq_max is not None:
#         f_limit = int(round(height * ratio))
#         spec = spec[:f_limit]
#         height, width = spec.shape
#     else:
#         freq_max = 0.5 * get_sample_rate()
#     imshow(
#         spec,
#         origin="lower",
#     )
#     xticks(np.linspace(0, width - 1, 5), np.linspace(0, dur(signal), 5))
#     yticks(np.linspace(0, height - 1, 5), np.linspace(0, freq_max, 5))


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
