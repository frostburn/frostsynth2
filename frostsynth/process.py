import numpy as np

from . import tau
from . import analysis
from . import chunk
from . import window
from .sampling import sampled, differentiate, integrate
from .pitch import ftom, mtof
from .scale import scale_round


@sampled
def decompose_frequency(data, window_size=1024):
    w = window.pad(window.cosine(window_size), window_size // 2)
    chunks = chunk.chunkify(data, window=w, overlap=4)

    chunks = map(analysis.hilbert, chunks)

    data = 4 * chunk.dechunkify(chunks, overlap=4)

    phase = np.unwrap(np.angle(data)) / tau
    frequency = differentiate(phase)
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


@sampled
def recompose_frequency(frequency, amplitude):
    phase = integrate(frequency)
    return np.sin(tau * phase) * amplitude


def fillnan(data):
    """
    Fills out nan gaps in the data half way forward and backward
    """
    nans = np.isnan(data)

    i = 0
    while nans[i]:
        i += 1
        last = data[i]
        run_length = 2 * i

    run_length = 0
    for i, value, isnan in zip(range(len(data)), data, nans):
        if isnan:
            data[i] = last
            run_length += 1
        else:
            if run_length:
                data[i-run_length//2:i] = value
                run_length = 0
            last = value


def run_lengths(data):
    result = []
    last = float("nan")
    length = 0
    for value in data:
        if value == last:
            length += 1
        else:
            result.extend([length] * length)
            length = 1
        last = value
    result.extend([length] * length)
    return np.array(result)


def autotune(frequency, amplitude, threshold, scale=None, min_duration=None):
    frequency = frequency.copy()
    frequency[amplitude < threshold] = float("nan")
    pitch = scale_round(ftom(frequency), scale)

    if min_duration:
        pitch[run_lengths(pitch) < min_duration] = float("nan")

    fillnan(pitch)

    return mtof(pitch)
