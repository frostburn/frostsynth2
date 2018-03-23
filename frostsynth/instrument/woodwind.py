import numpy as np

import ipywidgets as widgets

from .base import Instrument
from ..sampling import sampled, trange
from ..waveform import tang, sine


class TangBassoon(Instrument):
    def __init__(self):
        self.sharpness = widgets.FloatSlider(
            description="sharpness",
            value=2, min=0, max=3, step=0.1
        )
        self.balance = widgets.FloatSlider(
            description="balance",
            value=0.2, min=0, max=1, step=0.1
        )
        self.attack = widgets.FloatSlider(
            description="attack",
            value=20, min=0, max=30, step=1
        )
        self.decay = widgets.FloatSlider(
            description="decay",
            value=40, min=0, max=60, step=1
        )
        self.index = widgets.IntSlider(
            description="index",
            value=0, min=0, max=5
        )
        self.el = widgets.VBox([
            widgets.Label("Tang bassoon"),
            self.sharpness,
            self.balance,
            self.attack,
            self.decay,
            self.index
        ])

    @sampled
    def play(self, note):
        dur = note.duration + 1
        t = trange(dur)
        p = note.get_phase(dur)
        a = np.tanh(self.attack.value * t)
        modulator = tang(p) - sine(p) * (1 - self.balance.value * a)
        d = np.tanh((note.duration - t) * self.decay.value) * 0.5 + 0.5
        return np.cbrt(a) * sine(self.index.value * p + a * self.sharpness.value * modulator * d) * d * note.velocity
