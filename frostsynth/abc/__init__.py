from fractions import Fraction
import re

from .key import PITCHES
from ..note import Note



HEADER_SPECS = [
    ("UNIT_LENGTH", r'\s*L: *(\d+(/\d+)?)\n'),
    ("TEMPO", r'\s*Q: *((\d+(/\d+)?)=)?(\d+)\n'),
    ("KEY", r'\s*K: *([A-G](#|b)?m?)\n'),
    ("ID", r'\s*X: *\d+'),
    ("TITLE", r'\s*T:.*\n'),
    ("NOTES", r'\s*N:.*\n'),
    ("PARTS", r'\s*P:.*\n'),
    ("INSTRUCTION", r'\s*I:.*\n'),
    ("TRANSCRIPTION", r'\s*Z:.*\n'),
    ("AREA", r'\s*A:.*\n'),
    ("ORIGIN", r'\s*O:.*\n'),
    ("RYTHM", r'\s*R:.*\n'),
    ("BOOK", r'\s*B:.*\n'),
    ("DISCOGRAPHY", r'\s*D:.*\n'),
    ("HISTORY", r'\s*H:.*\n'),
    ("FILE", r'\s*F:.*\n'),
    ("SOURCE", r'\s*S:.*\n'),
    ("GROUP", r'\s*G:.*\n'),
    ("METER", r'\s*M:.*\n'),
    ("COMPOSER", r'\s*C:.*\n'),
    ("NEWLINE", r'\s*\n'),
    ("BODY", r'.'),
]


NOTE_SPECS = [
    ("NOTE", r'(|\^|_|=)([A-Ga-g]|z)'),
    ("GROUP", r'\[.*?\]'),
    ("CHORD_SYMBOL", r'".*?"'),
    ("DURATION", r'\d+'),
    ("INVERT_DURATION", r'/'),
    ("OCTAVE_UP", r"'"),
    ("OCTAVE_DOWN", r','),
    ("MISMATCH", r'.'),
]


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
            unit = mo.groups()[4] or "1/4"
            bpm = mo.groups()[7]
            tempo_multiplier = Fraction(60, int(bpm)) / Fraction(unit)
        elif kind == "KEY":
            key = mo.groups()[9]
            if key not in PITCHES.keys():
                raise NotImplementedError("Key signature {} not implemented yet".format(key))
        elif kind == "BODY":
            pitches = PITCHES[key]
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