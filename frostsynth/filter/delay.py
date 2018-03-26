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
    def step(self, sample):
        delta = self.duration * get_sample_rate()
        index = int(delta)
        mu = delta - index
        self.samples.append(sample)
        xn = self[index]
        xn1 = self[index + 1]
        return xn + mu * (xn1 - xn)

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
    def step(self, sample):
        self.last = super(Comb, self).step(sample - self.last * self.alpha)
        return self.last


class Schroeder(Filter):
    def __init__(self, duration=None, alpha=None):
        self.duration = duration
        self.alpha = alpha
        self.reset()

    def reset(self):
        self.samples = []
        self.outputs = []

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
    def step(self, sample):
        delta = self.duration * get_sample_rate()
        index = int(delta)
        mu = delta - index
        self.samples.append(sample)
        xn = self.get_sample(index)
        xn1 = self.get_sample(index + 1)
        yn = self.get_output(index + 1)
        yn1 = self.get_output(index + 2)
        y = self.alpha * (sample - yn - mu * (yn1 - yn)) + xn + mu * (xn1 - xn)
        self.outputs.append(y)
        return y

    def get_sample(self, index):
        if index >= len(self.samples) or index < 0:
            return 0.0
        return self.samples[-index]

    def get_output(self, index):
        if index >= len(self.outputs) or index < 0:
            return 0.0
        return self.outputs[-index]
