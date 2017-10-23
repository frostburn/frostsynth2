from __future__ import division
from math import *


class Filter(object):
    def map(self, data):
        self.reset()
        return [self.step(y) for y in data]


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


class Lowpass(Biquad):
    def __init__(self, w0, Q, sample_rate=None):
        if sample_rate is not None:
            w0 *= 2 * pi / sample_rate
        alpha = sin(w0) / (2 * Q)
        self.b0 = (1 - cos(w0))/2
        self.b1 =  1 - cos(w0)
        self.b2 = (1 - cos(w0))/2
        self.a0 =  1 + alpha
        self.a1 = -2 * cos(w0)
        self.a2 =  1 - alpha