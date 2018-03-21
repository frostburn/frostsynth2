from .pitch import ftom, mtof
from .sampling import sampled, trange


class Note(object):
    def __init__(self, pitch, duration, time=None, velocity=0.75):
        self.pitch = pitch
        self.duration = duration
        self.time = time
        self.velocity = velocity

    def __hash__(self):
        return hash((self.pitch, self.duration, self.time, self.velocity))

    def __repr__(self):
        return "{}({!r}, {!r}, {!r}, {!r})".format(
            self.__class__.__name__,
            self.pitch,
            self.duration,
            self.time,
            self.velocity,
        )

    def __eq__(self, other):
        return (
            self.pitch == other.pitch and
            self.duration == other.duration and
            self.time == other.time and
            self.velocity == other.velocity
        )

    @property
    def freq(self):
        return mtof(self.pitch)

    @freq.setter
    def freq(self, value):
        self.pitch = ftom(value)

    @property
    def off_time(self):
        return self.time + self.duration

    @sampled
    def get_phase(self, duration):
        return trange(duration) * self.freq

    def copy(self):
        return self.__class__(self.pitch, self.duration, self.time, self.velocity)


class Sheet(object):
    def __init__(self, notes, duration=None):
        self.notes = notes
        self._duration = duration

    def __iter__(self):
        return iter(self.notes)

    def __add__(self, other):
        first_part = self.copy()
        second_part = other.copy()
        second_part.shift(self.duration)

        first_part.notes.extend(second_part.notes)
        return first_part

    def __mul__(self, times):
        if times == 0:
            return self.__class__([])
        result = self.copy()
        for _ in range(times - 1):
            result = self + result
        return result

    @property
    def off_time(self):
        return max([n.off_time for n in self.notes])

    @property
    def duration(self):
        if self._duration is None:
            return self.off_time
        return self._duration

    def copy(self):
        return self.__class__([n.copy() for n in self.notes])

    def shift(self, duration):
        for note in self.notes:
            note.time += duration
        return self

    def transpose(self, interval):
        for note in self.notes:
            note.pitch += interval
        return self
