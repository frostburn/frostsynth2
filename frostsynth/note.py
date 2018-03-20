from .pitch import ftom, mtof
from .sampling import sampled, trange


class Note(object):
    def __init__(self, pitch, duration, time=None, velocity=0.5):
        self.pitch = pitch
        self.duration = duration
        self.time = time
        self.velocity = velocity

    def __hash__(self):
        return hash((self.pitch, self.duration, self.time, self.velocity))

    def __repr__(self):
        return "{}({!r}, {!r}, {!r})".format(
            self.__class__.__name__,
            self.pitch,
            self.duration,
            self.time
        )

    def __eq__(self, other):
        return (
            self.pitch == other.pitch and
            self.duration == other.duration and
            self.time == other.time
        )

    @property
    def freq(self):
        return mtof(self.pitch)

    @freq.setter
    def freq(self, value):
        self.pitch = ftom(value)

    @sampled
    def get_phase(self, duration):
        return trange(duration) * self.freq
