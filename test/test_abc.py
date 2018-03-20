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
            Note(56, Fraction(1, 2), Fraction(0, 1)),
            Note(71, Fraction(1, 2), Fraction(1, 2)),
            Note(72, Fraction(1, 4), Fraction(1, 1)),
            Note(87, Fraction(1, 4), Fraction(5, 4)),
        ])
    )


def test_key_signature():
    score = """
    X:2
    T:Unit test in D
    Q:1/4=60
    L:1/4
    K:D
    D E F =F G =G
    """
    notes = set(abc.score_to_notes(score, as_floats=False))
    assert (
        notes ==
        set([
            Note(62, Fraction(1, 1), Fraction(0, 1)),
            Note(64, Fraction(1, 1), Fraction(1, 1)),
            Note(66, Fraction(1, 1), Fraction(2, 1)),
            Note(65, Fraction(1, 1), Fraction(3, 1)),
            Note(68, Fraction(1, 1), Fraction(4, 1)),
            Note(67, Fraction(1, 1), Fraction(5, 1)),
        ])
    )
