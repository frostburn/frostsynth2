import numpy as np

from . import tau
from . import analysis
from . import chunk
from . import window


def decompose_frequency(data, window_size=1024):
    w = window.pad(window.cosine(window_size), window_size // 2)
    chunks = chunk.chunkify(data, window=w, overlap=4)

    chunks = map(analysis.hilbert, chunks)

    data = 4 * chunk.dechunkify(chunks, overlap=4)

    phase = np.unwrap(np.angle(data)) / tau
    frequency = np.concatenate(([0.0], np.diff(phase)))
    amplitude = abs(data)

    return frequency, amplitude


def clean_frequency(frequency, amplitude, window_size=1024):
    w = window.cosine(window_size)
    weighted_frequency = np.convolve(frequency * amplitude, w)
    average_weight = np.convolve(amplitude, w)
    return (
        weighted_frequency / (average_weight + (average_weight == 0)),
        average_weight / w.sum()
    )


def recompose_frequency(frequency, amplitude):
    phase = np.cumsum(frequency)
    return np.sin(tau * phase) * amplitude
