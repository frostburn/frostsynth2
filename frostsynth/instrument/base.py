import ipywidgets as widgets

from ..ipython import Audio
from ..sampling import sampled, merge
from ..note import Note
from ..abc import score_to_sheet


class Instrument(object):
    def __init__(self):
        self.el = widgets.Label("Instrument")

    @sampled
    def preview(self, note=None):
        note = note or Note(56, 1)
        return Audio(self.play(note))

    def _ipython_display_(self):
        return self.el._ipython_display_()

    @sampled
    def play_abc(self, score, transpose=0):
        sheet = score_to_sheet(score).transpose(transpose)
        return self.play_sheet(sheet)

    @sampled
    def play_sheet(self, sheet):
        samples = []
        for note in sheet:
            samples.append((note.time, self.play(note)))
        return merge(samples)
