import numpy as np
import ipywidgets as widgets

from .. import sampling
from . import audio


class ToggleGrid(object):
    def __init__(self, num_rows, num_columns):
        self.cells = []
        columns = []
        for _ in range(num_columns):
            items = []
            for _ in range(num_rows):
                layout = widgets.Layout(
                    width="auto",
                    flex="1 1 auto",
                )
                button = widgets.ToggleButton(layout=layout)
                items.append(button)
            self.cells.append(items)
            columns.append(widgets.VBox(items))
        self.el = widgets.HBox(columns)

    def __setitem__(self, xy, value):
        x, y = xy
        self.cells[x][y].value = bool(value)

    def __getitem__(self, xy):
        x, y = xy
        return self.cells[x][y].value

    @property
    def value(self):
        return np.array([
            [self[x, y] for x in range(len(self.cells))] for \
            y in range(len(self.cells[0]))
        ])

    @value.setter
    def value(self, values):
        for y, row in enumerate(values):
            for x, value in enumerate(row):
                self[x, y] = value

    def _ipython_display_(self):
        return self.el._ipython_display_()


class InstrumentGrid(ToggleGrid):
    def __init__(self, num_columns, beat_duration, instrument, scale):
        self.scale = scale
        self.beat_duration = beat_duration
        self.instrument = instrument
        super(InstrumentGrid, self).__init__(len(self.scale), num_columns)

    @sampling.sampled
    def render(self):
        notes = []
        for pitch, row in zip(reversed(self.scale), self.value):
            for x, value in enumerate(row):
                if value:
                    t = x * self.beat_duration
                    try:
                        sound = self.instrument(pitch, t=t)
                    except TypeError:
                        sound = self.instrument(pitch)
                    notes.append((t, sound))
        return sampling.merge(notes)

    @sampling.sampled
    def display(self, **kwargs):
        return audio.Audio(self.render(), **kwargs)
