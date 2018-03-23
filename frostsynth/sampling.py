from __future__ import division

from functools import wraps

import numpy as np
from scipy.io import wavfile

SAMPLE_RATE = None


def sampled(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        global SAMPLE_RATE
        old_rate = SAMPLE_RATE
        sample_rate = kwargs.pop("sample_rate", None)
        SAMPLE_RATE = sample_rate or SAMPLE_RATE
        if SAMPLE_RATE is None:
            raise ValueError("Cannot call sampling function without setting sample rate first.")
        result = f(*args, **kwargs)
        SAMPLE_RATE = old_rate
        return result
    return wrapper


def set_sample_rate(rate):
    global SAMPLE_RATE
    SAMPLE_RATE = rate


def get_sample_rate(default=None):
    if SAMPLE_RATE is None:
        return default
    return SAMPLE_RATE


def read_and_set_sample_rate(filename):
    rate, data = wavfile.read(filename)
    set_sample_rate(rate)
    info = np.iinfo(data.dtype)
    data = data.astype(float) / max(abs(info.min), abs(info.max))
    if len(data.shape) > 1 and data.shape[0] > data.shape[1]:
        return data.T
    return data


@sampled
def write(filename, data):
    if data.dtype == float:
        data = (data * (0.99 * 2.0 ** 15)).astype("int16")
    wavfile.write(filename, SAMPLE_RATE, data)


@sampled
def trange(a, b=None):
    if b is None:
        start = 0
        end = a
    else:
        start = a
        end = b
    return np.arange(
        int(round(start * SAMPLE_RATE)),
        int(round(end * SAMPLE_RATE))
    ) / SAMPLE_RATE


@sampled
def time_like(a):
    return np.arange(len(a)) / SAMPLE_RATE


@sampled
def shift(samples, duration, interpolation=None):
    duration = int(round(duration * SAMPLE_RATE))
    if duration > 0:
        return np.concatenate((np.zeros(duration), samples[duration:]))
    else:
        return np.concatenate((samples[:duration], np.zeros(-duration)))


@sampled
def differentiate(samples):
    return np.concatenate(([0], np.diff(samples) * SAMPLE_RATE))


@sampled
def integrate(samples):
    return np.cumsum(samples / SAMPLE_RATE)


def amerge(args):
    length = 0
    for x, values in args:
        length = max(length, x + len(values))
    result = np.zeros(length)
    for x, values in args:
        result += np.concatenate((
            np.zeros(x),
            values,
            np.zeros(length - x - len(values))
        ))
    return result


@sampled
def merge(args):
    args = args[:]
    for i in range(len(args)):
        x, values = args[i]
        args[i] = (int(round(x * SAMPLE_RATE)), values)
    return amerge(args)


@sampled
def add(*samples):
    return amerge([(0, sample) for sample in samples])
