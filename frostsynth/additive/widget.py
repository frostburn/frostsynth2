import ipywidgets as widgets
import numpy as np

from .base import fourier, make_periodic
from .. import tau


class HarmonicSlider(object):
    def __init__(self, num_harmonics):
        self.sliders = []
        for i in range(num_harmonics):
            self.sliders.append(widgets.FloatSlider(
                description="#{}".format(i + 1),
                value=0, min=0, max=1, step=0.01,
                orientation="vertical"
            ))
        self.offsets = np.zeros(num_harmonics)
        self.randomizer = widgets.Button(
            description="Randomize phase"
        )
        self.randomizer.on_click(lambda args: self.randomize_phase())

        self.el = widgets.VBox([
            widgets.Label("Harmonics"),
            widgets.HBox(self.sliders),
            self.randomizer,
        ])

    def _ipython_display_(self):
        return self.el._ipython_display_()

    def __call__(self, phase):
        partials = []
        for i, slider, offset in zip(range(len(self.sliders)), self.sliders, self.offsets):
            weight = slider.value
            partials.append(
                weight * np.sin(tau * (i + 1) * phase + offset)
            )
        return sum(partials)

    def freeze(self):
        weights = [0]
        for slider, offset in zip(self.sliders, self.offsets):
            weights.append(-1j * slider.value * np.exp(1j * offset))
        weights.extend([0] * len(self.sliders))
        return fourier(weights)

    def randomize_phase(self):
        self.offsets = np.random.rand(len(self.offsets)) * tau


class SplineSlider(object):
    def __init__(self, num_samples):
        self.sliders = []
        for i in range(num_samples):
            self.sliders.append(widgets.FloatSlider(
                description="#{}".format(i),
                value=0, min=0, max=1, step=0.01,
                orientation="vertical"
            ))
        self.el = widgets.VBox([
            widgets.Label("Samples"),
            widgets.HBox(self.sliders),
        ])

    def _ipython_display_(self):
        return self.el._ipython_display_()

    def __call__(self, phase):
        return self.freeze()(phase)

    def freeze(self):
        samples = [slider.value for slider in self.sliders]
        return make_periodic(samples)
