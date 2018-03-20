import numpy as np

import ipywidgets as widgets

from ..ipython import Audio
from ..sampling import sampled, trange, merge
from ..waveform import softsaw
from ..note import Note
from ..abc import score_to_notes

class Instrument(object):
    def __init__(self):
        self.el = widgets.Label("Instrument")

    @sampled
    def preview(self, note=None):
        note = note or Note(56, 1)
        return Audio(self.play(note))

    def _ipython_display_(self):
        return self.el._ipython_display_()

    def play_abc(self, score, transpose=0):
        notes = score_to_notes(score)
        samples = []
        for note in notes:
            note.pitch += transpose
            samples.append((note.time, self.play(note)))
        return merge(samples)


class SawBass(Instrument):
    def __init__(self):
        self.sharpness = widgets.FloatSlider(
            description="sharpness",
            value=0.75, min=0, max=1, step=0.02
        )
        self.sharpness_decay = widgets.FloatSlider(
            description="s-decay",
            value=2, min=0, max=10, step=0.2
        )
        self.decay = widgets.FloatSlider(
            description="decay",
            value=2, min=0, max=10, step=0.2
        )
        self.el = widgets.VBox([
            widgets.Label("Saw bass"),
            self.sharpness,
            self.sharpness_decay,
            self.decay,
        ])

    @sampled
    def play(self, note):
        dur = note.duration + 1
        t = trange(dur)
        p = note.get_phase(dur)
        s = np.exp(-t * self.sharpness_decay.value) * np.cbrt(self.sharpness.value)
        separation = 0.2

        voice = softsaw(p + separation * t, s) + softsaw(p - separation * t, s)
        envelope = note.velocity * 0.25
        envelope *= np.exp(-t * self.decay.value)
        envelope *= 1 + np.tanh(6 * (note.duration - t))

        return voice * envelope
