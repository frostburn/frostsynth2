import numpy as np
from . import sampling

class SoundClip(object):
    @sampling.sampled
    def __init__(self, data, start=0, end=None):
        self.data = np.array(data, dtype=float)
        self.start = start
        if end is None:
            end = sampling.dur(data)
        self.end = end

    def __repr__(self):
        return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.data, self.start, self.end)

    def __eq__(self, other):
        return (self.data == other.data).all() and self.start == other.start and self.end == other.end

    def add(self, other):
        """
        Create a new clip with equal start times.
        """
        if self.start < other.start:
            return other.add(self)
        offset = self.start - other.start
        data = sampling.merge([(0, self.data), (offset, other.data)])
        return SoundClip(data, self.start, max(self.end, other.end + offset))

    def concat(self, other):
        """
        Create a new clip with start and end glued together.
        """
        offset = self.end - other.start
        if offset >= 0:
            data = sampling.merge([(0, self.data), (offset, other.data)])
            return SoundClip(data, self.start, max(self.end, other.end + offset))
        else:
            data = sampling.merge([(-offset, self.data), (0, other.data)])
            return SoundClip(data, other.start, max(self.end - offset, other.end))
