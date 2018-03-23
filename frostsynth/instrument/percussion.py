from __future__ import division
import json

import numpy as np
import ipywidgets as widgets

from .base import Instrument
from ..ipython import Audio
from ..sampling import sampled, trange, get_sample_rate
from ..note import NonPitched
from ..waveform import sine
from ..additive import sinepings
from .. import noise


class Percussion(Instrument):
    @sampled
    def preview(self, note=None):
        note = note or NonPitched()
        return Audio(self.play(note))


class Kick(Percussion):
    def __init__(self):
        self.frequency = widgets.FloatSlider(
            description="frequency",
            value=10, min=1, max=50, step=1
        )
        self.attack = widgets.FloatSlider(
            description="attack",
            value=2, min=0.5, max=6, step=0.1
        )
        self.meekness = widgets.FloatSlider(
            description="meekness",
            value=0.1, min=0.01, max=0.5, step=0.01
        )
        self.decay = widgets.FloatSlider(
            description="decay",
            value=20, min=0, max=60, step=1
        )
        self.distortion = widgets.FloatSlider(
            description="distortion",
            value=1, min=0.5, max=5, step=0.5
        )
        self.el = widgets.VBox([
            widgets.Label("Kick drum"),
            self.frequency,
            self.attack,
            self.meekness,
            self.decay,
            self.distortion,
        ])

    @sampled
    def play(self, note):
        t = trange(0.5)
        freq = self.frequency.value
        attack = self.attack.value
        meekness = self.meekness.value
        decay = self.decay.value
        distortion = self.distortion.value * note.velocity
        return np.tanh(
            sine(np.log(attack * t + meekness) * freq) * np.exp(-t * decay) * distortion
        ) * 0.5 * (np.tanh(1000 * t - 2) + 1)  * note.velocity

class Snare(Percussion):
    modes = [
        (156, 5, 30),
        (185, 25, 10),
        (467, 20, 10),
        (650, 7, 10),
        (773, 7, 12),
        (961, 5, 10),
        (1131, 5, 10),
        (1211, 5, 10),
        (1311, 3, 15),
        (1552, 3, 15),
    ]
    def __init__(self):
        self.detune = widgets.FloatSlider(
            description="detune",
            value=1, min=0.8, max=1.2, step=0.01
        )
        self.decay = widgets.FloatSlider(
            description="decay",
            value=1, min=0.5, max=2, step=0.1
        )
        self.distortion = widgets.FloatSlider(
            description="distortion",
            value=15, min=0.1, max=50, step=0.1
        )
        self.noise_volume = widgets.FloatSlider(
            description="noise volume",
            value=1, min=0.1, max=2, step=0.1
        )
        self.noise_decay = widgets.FloatSlider(
            description="noise decay",
            value=16, min=4, max=30, step=1
        )
        self.el = widgets.VBox([
            widgets.Label("Snare"),
            self.detune,
            self.decay,
            self.distortion,
            self.noise_volume,
            self.noise_decay,
        ])

    @sampled
    def play(self, note):
        duration = 1
        t = trange(duration)
        modes = []
        norm = 0
        detune = self.detune.value
        decay = self.decay.value
        for f, w, d in self.modes:
            norm += w
            modes.append((f * detune, w, d * decay))
        modal = sinepings(duration, modes) / norm
        distortion = self.distortion.value
        modal = np.tanh(modal * note.velocity * distortion) / distortion
        noisy = noise.pink(duration) * np.exp(-t * self.noise_decay.value) * 0.01 * self.noise_volume.value
        return (modal + noisy) * note.velocity
