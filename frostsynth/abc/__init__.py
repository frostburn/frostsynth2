from fractions import Fraction
import re

from ..note import Note



HEADER_SPECS = [
    ("UNIT_LENGTH", r'\s*L:(\d+(/\d+)?)\n'),
    ("TEMPO", r'\s*Q:(\d+(/\d+)?)=(\d+)\n'),
    ("KEY", r'\s*K:([A-G](#|b)?m?)\n'),
    ("ID", r'\s*X:\d+'),
    ("TITLE", r'\s*T:.*\n'),
    ("METER", r'\s*M:.*\n'),
    ("COMPOSER", r'\s*C:.*\n'),
    ("NEWLINE", r'\s*\n'),
    ("BODY", r'.'),
]


NOTE_SPECS = [
    ("NOTE", r'(|\^|_|=)([A-Ga-g]|z)'),
    ("DURATION", r'\d+'),
    ("INVERT_DURATION", r'/'),
    ("OCTAVE_UP", r"'"),
    ("OCTAVE_DOWN", r','),
    ("MISMATCH", r'.'),
]


PITCHES_C = {
    "_C": 59,
    "C": 60,
    "=C": 60,
    "^C": 61,
    "_D": 61,
    "D": 62,
    "=D": 62,
    "^D": 63,
    "_E": 63,
    "E": 64,
    "=E": 64,
    "^E": 65,
    "_F": 64,
    "F": 65,
    "=F": 65,
    "^F": 66,
    "_G": 66,
    "G": 67,
    "=G": 67,
    "^G": 68,
    "_A": 68,
    "A": 69,
    "=A": 69,
    "^A": 70,
    "_B": 70,
    "B": 71,
    "=B": 71,
    "^B": 72,
}

for note, pitch in PITCHES_C.items():
    PITCHES_C[note.lower()] = pitch + 12

PITCHES_C["z"] = None


HEADER_REGEX = '|'.join('(?P<{}>{})'.format(*pair) for pair in HEADER_SPECS)
NOTE_REGEX = '|'.join('(?P<{}>{})'.format(*pair) for pair in NOTE_SPECS)


def score_to_notes(score, as_floats=True):
    unit_length = Fraction(1)
    tempo_multiplier = Fraction(1)
    key = "C"
    for mo in re.finditer(HEADER_REGEX, score):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == "UNIT_LENGTH":
            unit_length = Fraction(mo.groups()[1])
        elif kind == "TEMPO":
            unit = mo.groups()[4]
            bpm = mo.groups()[6]
            tempo_multiplier = Fraction(int(bpm), 60) * Fraction(unit)
        elif kind == "KEY":
            key = mo.groups()[8]
            if key not in ("C", "Am"):
                raise NotImplementedError("Key signatures not implemented")
        elif kind == "BODY":
            pitches = PITCHES_C
            tempo_multiplier *= unit_length
            for note in score_body_to_notes(score[mo.start():], pitches, as_floats):
                note.duration *= tempo_multiplier
                note.time *= tempo_multiplier
                yield note
            return


def score_body_to_notes(score, pitches, as_floats=True):
    if as_floats:
        for note in score_body_to_notes(score, pitches, as_floats=False):
            note.duration = float(note.duration)
            note.time = float(note.time)
            yield note
        return
    notes = []
    time = Fraction(0)
    current_note = None
    duration_inverted = False
    for mo in re.finditer(NOTE_REGEX, score):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == "NOTE":
            if current_note is not None:
                if duration_inverted:
                    current_note.duration /= 2
                time += current_note.duration
                if current_note.pitch is not None:
                    yield current_note
            current_note = Note(pitches[value], Fraction(1), time)
            duration_inverted = False
        elif kind == "DURATION":
            value = int(value)
            if duration_inverted:
                current_note.duration /= value
            else:
                current_note.duration *= value
            duration_inverted = False
        elif kind == "INVERT_DURATION":
            duration_inverted = True
        elif kind == "OCTAVE_UP":
            current_note.pitch += 12
        elif kind == "OCTAVE_DOWN":
            current_note.pitch -= 12

    if current_note is not None:
        if duration_inverted:
            current_note.duration /= 2
        time += current_note.duration
        if current_note.pitch is not None:
            yield current_note
