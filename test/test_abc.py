from fractions import Fraction

from frostsynth import abc
from frostsynth.note import Note


def test_score_to_notes():
    score = """
    X:1
    T:A little test song
    Q:1/4=120
    L:1/4
    K:C
    _A, B =c/2 ^d'/
    """
    notes = set(abc.score_to_notes(score, as_floats=False))
    assert (
        notes ==
        set([
            Note(56, Fraction(1, 8), Fraction(0, 1)),
            Note(71, Fraction(1, 8), Fraction(1, 8)),
            Note(72, Fraction(1, 16), Fraction(1, 4)),
            Note(87, Fraction(1, 16), Fraction(5, 16)),
        ])
    )
