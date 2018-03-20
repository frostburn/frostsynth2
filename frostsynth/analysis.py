import numpy as np

from .chunk import chunkify

def hilbert(signal):
    frequencies = np.fft.fft(signal)
    # Remove DC
    frequencies[0] = 0
    # Remove negative frequencies
    frequencies[len(frequencies) // 2:] = 0
    return 2 * np.fft.ifft(frequencies)


def spectrogram(signal, window, overlap):
    return np.array(map(np.fft.rfft, chunkify(signal, window, overlap, ljust=True))).T
