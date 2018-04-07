from __future__ import division

import numpy as np

from .sampling import sampled, get_sample_rate, integrate

EPSILON = 1e-6


def sine_series_mu(phase, n):
    n += 1
    floor_n = np.floor(n)
    mu = n - floor_n
    s = np.sin(np.pi * floor_n * phase)
    return -np.tan(np.pi * (phase + 0.5)) * s * s + np.sin(2 * np.pi * floor_n * phase) * (mu - 0.5)


def cosine_series_mu(phase, n):
    floor_n = np.floor(n)
    mu = n - floor_n
    s = np.sin(np.pi * phase)
    too_small = (abs(s) < EPSILON)
    series = 0.5 * np.sin(np.pi * (2 * floor_n - 1) * phase) / (s + too_small) - 0.5
    return np.where(
        too_small,
        n - 1,
        series + np.cos(2 * np.pi * floor_n * phase) * mu
    )


def sine_series_odd_mu(phase, n):
    s = np.sin(2 * np.pi * phase)
    floor_n = np.floor(n)
    mu = n - floor_n
    theta = 4 * np.pi * floor_n * phase
    phi = 2 * np.pi * (2 * floor_n + 1) * phase
    too_small = (abs(s) < EPSILON)
    return np.where(
        too_small,
        s * (floor_n ** 2 + mu),
        (0.5 - 0.5 * np.cos(theta)) / (s + too_small) + np.sin(phi) * mu
    )


def power_series_mu(z, n):
    z1 = 1 - z
    floor_n = np.floor(n)
    z_floor_n = z ** floor_n
    too_small = (abs(z1) < EPSILON)
    return np.where(
        too_small,
        n,
        (1 - z_floor_n) / (z1 + too_small) + (n - floor_n) * z_floor_n
    )


@sampled
def sine_blit(freq):
    phase = integrate(freq)
    return sine_series_mu(phase, 0.5 * get_sample_rate() / freq)


@sampled
def odd_blit(freq):
    phase = integrate(freq)
    return sine_series_odd_mu(phase, 0.25 * get_sample_rate() / freq - 0.5)


@sampled
def cblit(freq, softness=0, padding=0):
    phase = integrate(freq)
    return power_series_mu(
        np.exp(2j * np.pi * phase - softness),
        (0.5 * get_sample_rate() - padding) / freq
    )


@sampled
def saw_blit(freq):
    phase = integrate(freq)
    derivative = cosine_series_mu(phase, 0.5 * get_sample_rate() / freq)
    current = -0.25 * get_sample_rate()
    result = []
    for v in (derivative * freq):
        current = 0.99 * current - v
        result.append(current)
    return 2 * np.array(result) / get_sample_rate()


@sampled
def rect_blit(freq, separation=0.5):
    separation *= 0.5
    phase = integrate(freq)
    derivative = cosine_series_mu(phase - separation, 0.5 * get_sample_rate() / freq)
    derivative -= cosine_series_mu(phase + separation, 0.5 * get_sample_rate() / freq)
    current = -0.25 * get_sample_rate()
    result = []
    for v in (derivative * freq):
        current = 0.99 * current + v
        result.append(current)
    return 2 * np.array(result) / get_sample_rate()
