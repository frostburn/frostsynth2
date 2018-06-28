from numpy import ones
from frostsynth import sampling
from frostsynth.soundclip import SoundClip

def test_add():
    sampling.set_sample_rate(16)
    a = SoundClip(ones(16), 0.25, 0.75)
    b = SoundClip(ones(16) * 2, 0.5, 0.75)
    c = a.add(b)

    assert c == SoundClip([2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1], 0.5, 1.0)


def test_concat():
    sampling.set_sample_rate(16)
    a = SoundClip(ones(16), 0.25, 0.75)
    b = SoundClip(ones(16) * 2, 0.5, 0.75)
    c = a.concat(b)

    assert c == SoundClip([1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2], 0.25, 1.0)
