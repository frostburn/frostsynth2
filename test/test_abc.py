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
    notes = set(abc.score_to_sheet(score, as_floats=False).notes)
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
    D E F =F C =C
    """
    notes = set(abc.score_to_sheet(score, as_floats=False).notes)
    assert (
        notes ==
        set([
            Note(62, Fraction(1, 1), Fraction(0, 1)),
            Note(64, Fraction(1, 1), Fraction(1, 1)),
            Note(66, Fraction(1, 1), Fraction(2, 1)),
            Note(65, Fraction(1, 1), Fraction(3, 1)),
            Note(61, Fraction(1, 1), Fraction(4, 1)),
            Note(60, Fraction(1, 1), Fraction(5, 1)),
        ])
    )


def test_repeat():
    score = """
    X:3
    T:Unit test in G minor
    Q:1/4=60
    L:1/4
    M:3/4
    K:Gm
    A B C :| D E F |]
    """
    notes = set(abc.score_to_sheet(score, as_floats=False).notes)
    assert (
        notes ==
        set([
            Note(69, Fraction(1, 1), Fraction(0, 1)),
            Note(70, Fraction(1, 1), Fraction(1, 1)),
            Note(60, Fraction(1, 1), Fraction(2, 1)),
            Note(69, Fraction(1, 1), Fraction(3, 1)),
            Note(70, Fraction(1, 1), Fraction(4, 1)),
            Note(60, Fraction(1, 1), Fraction(5, 1)),
            Note(62, Fraction(1, 1), Fraction(6, 1)),
            Note(63, Fraction(1, 1), Fraction(7, 1)),
            Note(65, Fraction(1, 1), Fraction(8, 1)),
        ])
    )


def test_first_repeat():
    score = """
    X:3
    T:Unit test in B minor
    Q:1/4=120
    L:2/4
    M:2/4
    K:BMin
    C |[1 D :|[2 E |]
    """
    notes = set(abc.score_to_sheet(score, as_floats=False).notes)
    assert (
        notes ==
        set([
            Note(61, Fraction(1, 1), Fraction(0, 1)),
            Note(62, Fraction(1, 1), Fraction(1, 1)),
            Note(61, Fraction(1, 1), Fraction(2, 1)),
            Note(64, Fraction(1, 1), Fraction(3, 1)),
        ])
    )
