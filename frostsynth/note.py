class Note(object):
    def __init__(self, pitch, duration, time):
        self.pitch = pitch
        self.duration = duration
        self.time = time

    def __hash__(self):
        return hash((self.pitch, self.duration, self.time))

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
