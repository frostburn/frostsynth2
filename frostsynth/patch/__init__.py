import ipywidgets as widgets

from ..sampling import integrate, sampled


class Patch(object):
    def __init__(self):
        self.el = widgets.Label("Patch")

    def _ipython_display_(self):
        return self.el._ipython_display_()

    def map(self, signals):
        for target, signal in signals.items():
            if target is self:
                return signal

    def __mul__(self, other):
        if not isinstance(other, Patch):
            other = ConstantPatch(other)
        return ProductPatch(self, other)


class ConstantPatch(Patch):
    def __init__(self, value):
        self.value = value

    def map(self, signals):
        return self.value


class ProductPatch(Patch):
    def __init__(self, *args):
        self.args = args

    def map(self, signals):
        result = 1
        for arg in self.args:
            result *= arg.map(signals)
        return result


class InputPatch(Patch):
    def __init__(self, label="Input"):
        self.el = widgets.Label(label)


class FloatPatch(Patch):
    def __init__(self, **kwargs):
        kwargs.setdefault("value", 0.5)
        kwargs.setdefault("min", 0.0)
        kwargs.setdefault("max", 1.0)
        kwargs.setdefault("orientation", "vertical")
        self.el = widgets.FloatSlider(**kwargs)

    def map(self, signals):
        return self.el.value


class DictPatchKey(object):
    def __init__(self, parent, key):
        self.parent = parent
        self.key = key


class DictPatch(Patch):
    def __init__(self, parent):
        self.parent = parent

    def map(self, signals):
        result = {}
        for target, signal in signals.items():
            if isinstance(target, DictPatchKey) and target.parent is self.parent:
                result[target.key] = signal
        return result

    def __getitem__(self, key):
        return DictPatchKey(self.parent, key)


class WavePatch(Patch):
    def __init__(self, waveform, frequency=None, label="Waveform"):
         self.waveform = waveform
         self.frequency = frequency

         self.phase_modulator = ConstantPatch(0)
         self.pm_patch = FloatPatch(description="PM", disabled=True)

         self.el = widgets.VBox([
            widgets.Label(label),
            self.pm_patch.el,
        ])

    def pm(self, other):
        self.phase_modulator = other * self.pm_patch
        self.pm_patch.el.disabled = False

    @sampled
    def map(self, signals):
        freq = self.frequency.map(signals)
        phase = integrate(freq) + self.phase_modulator.map(signals)

        kwargs = self.kwargs.map(signals)
        return self.waveform(phase, **kwargs)

    @property
    def kwargs(self):
        return DictPatch(self)
