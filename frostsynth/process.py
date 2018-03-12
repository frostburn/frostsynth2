import numpy as np

from . import tau
from . import analysis
from . import chunk
from . import window


def decompose_frequency(data, window_size=1024):
    w = window.pad(window.cosine(window_size), window_size // 2)
    chunks = chunk.chunkify(data, window=w, overlap=4)

    chunks = map(analysis.hilbert, chunks)

    data = 2 * chunk.dechunkify(chunks, overlap=4)

    phase = np.unwrap(np.angle(data)) / tau
    frequency = np.concatenate(([0.0], np.diff(phase)))
    amplitude = abs(data)

    return frequency, amplitude
