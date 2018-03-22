from __future__ import division

import numpy as np

from ..sampling import sampled


class Filter(object):
    @sampled
    def map(self, data):
        self.reset()
        return np.array([self.step(y) for y in data])


class Polezero(Filter):
    def step(self, sample):
        y0 = self.b0 * sample + self.b1 * self.x1 - self.a1 * self.y1
        y0 /= self.a0
        self.x1 = sample
        self.y1 = y0
        return y0

    def reset(self):
        self.x1 = 0
        self.y1 = 0


class TwoZero(Filter):
    def step(self, sample):
        y0 = self.b0 * sample + self.b1 * self.x1 + self.b2 * self.x2
        self.x2 = self.x1
        self.x1 = sample
        return y0 / self.a0

    def reset(self):
        self.x1 = 0
        self.x2 = 0


class Biquad(Filter):
    def step(self, sample):
        y0 = self.b0 * sample + self.b1 * self.x1 + self.b2 * self.x2 - self.a1 * self.y1 - self.a2 * self.y2
        y0 /= self.a0
        self.x2 = self.x1
        self.x1 = sample
        self.y2 = self.y1
        self.y1 = y0
        return y0

    def reset(self):
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0

    def __repr__(self):
        return "a={},{},{},b={},{},{}".format(self.a0, self.a1, self.a2, self.b0, self.b1, self.b2)


class _ComplexPole(Filter):
    def step(self, sample):
        self.y1 = sample - self.a1 * self.y1
        return self.y1

    def reset(self):
        self.y1 = 0


class ComplexPole(_ComplexPole):
    def step(self, sample):
        y0 = sample - self.a1 * self.y1
        self.y1 = y0 / self.a0


class Transientless(Filter):
    def __init__(self):
        self.two_zero = TwoZero()
        self.complex_pole = _ComplexPole()

    def step(self, sample):
        sample = self.two_zero.step(sample)
        return self.complex_pole.step(sample).imag

    def reset(self):
        self.two_zero.reset()
        self.complex_pole.reset()
