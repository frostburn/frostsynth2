from __future__ import division

from cmath import exp
from math import sin, cos
from numbers import Number

import numpy as np

from .. import tau
from ..sampling import sampled, get_sample_rate
from .base import Transientless

tau_j = 1j * tau


class Dynamic(Transientless):
    def __init__(self):
        super(Dynamic, self).__init__()
        self.two_zero.a0 = 1

    @sampled
    def resonator(self, freq, decay):
        self.complex_pole.a1 = -exp((tau_j * freq - decay) / get_sample_rate())

    @sampled
    def two_zero_coefs(self, freq, decay):
        pass

    @sampled
    def map(self, data, freq, decay):
        self.reset()
        if isinstance(freq, Number):
            freq = np.full_like(data, freq)
        if isinstance(decay, Number):
            decay = np.full_like(data, decay)
        result = []
        for y, f, d in zip(data, freq, decay):
            self.resonator(f, d)
            self.two_zero_coefs(f, d)
            result.append(self.step(y))
        return np.array(result)


class Lowpass(Dynamic):
    def __init__(self):
        super(Lowpass, self).__init__()
        self.two_zero.b0 = 0.25
        self.two_zero.b1 = 0.5
        self.two_zero.b2 = 0.25


class Highpass(Dynamic):
    def __init__(self):
        super(Highpass, self).__init__()
        self.two_zero.b0 = 0.25
        self.two_zero.b1 = -0.5
        self.two_zero.b2 = 0.25


class Bandpass(Dynamic):
    def __init__(self):
        super(Bandpass, self).__init__()
        self.two_zero.b0 = 1
        self.two_zero.b1 = 0
        self.two_zero.b2 = -1


class Notch(Dynamic):
    def two_zero_coefs(self, freq, decay):
        self.two_zero.b0 = 1
        self.two_zero.b1 = -2 * cos(freq * tau / get_sample_rate())
        self.two_zero.b2 = 1


class Allpass(Dynamic):
    def two_zero_coefs(self, freq, decay):
        r = self.complex_pole.a1.real
        i = self.complex_pole.a1.imag
        m = 1 / sin(freq * tau / get_sample_rate())
        self.two_zero.b0 = (r * r + i * i) * m
        self.two_zero.b1 = 2 * r * m
        self.two_zero.b2 = m


@sampled
def lowpass(signal, freq, decay):
    lpf = Lowpass()
    return lpf.map(signal, freq, decay)


@sampled
def highpass(signal, freq, decay):
    hpf = Highpass()
    return hpf.map(signal, freq, decay)


@sampled
def bandpass(signal, freq, decay):
    bpf = Bandpass()
    return bpf.map(signal, freq, decay)


@sampled
def notch(signal, freq, decay):
    n = Notch()
    return n.map(signal, freq, decay)


@sampled
def allpass(signal, freq, decay):
    apf = Allpass()
    return apf.map(signal, freq, decay)
