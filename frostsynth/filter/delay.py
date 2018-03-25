from numbers import Number

import numpy as np

from ..sampling import sampled, get_sample_rate
from .base import Filter


class Delay(Filter):
    def __init__(self, duration=None):
        self.duration = duration
        self.reset()

    def reset(self):
        self.samples = []

    @sampled
    def map(self, data, duration=None):
        self.reset()
        result = []
        if duration is None:
            duration = self.duration
        if isinstance(duration, Number):
            duration = np.full_like(data, duration)
        for y, d in zip(data, duration):
            self.duration = d
            result.append(self.step(y))
        return np.array(result)

    @sampled
    def step(self, y):
        delta = self.duration * get_sample_rate()
        z0 = int(delta)
        mu = delta - z0
        self.samples.append(y)
        y0 = self[z0]
        y1 = self[z0 + 1]
        return y0 + mu * (y1 - y0)

    def __getitem__(self, index):
        if index >= len(self.samples) or index < 0:
            return 0.0
        return self.samples[-index]


class Comb(Delay):
    def __init__(self, duration=None, alpha=None):
        super(Comb, self).__init__(duration)
        self.alpha = alpha

    def reset(self):
        super(Comb, self).reset()
        self.last = 0

    @sampled
    def map(self, data, duration=None, alpha=None):
        self.reset()
        result = []
        if duration is None:
            duration = self.duration
        if isinstance(duration, Number):
            duration = np.full_like(data, duration)
        if alpha is None:
            alpha = self.alpha
        if isinstance(alpha, Number):
            alpha = np.full_like(data, alpha)
        for y, d, a in zip(data, duration, alpha):
            self.duration = d
            self.alpha = a
            result.append(self.step(y))
        return np.array(result)

    @sampled
    def step(self, y):
        self.last = super(Comb, self).step(y + self.last * self.alpha)
        return self.last
