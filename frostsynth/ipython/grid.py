from __future__ import division

import numpy as np
import ipywidgets as widgets

from .. import note
from ..sampling import merge, sampled


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


class TempoGrid(ToggleGrid):
    def __init__(self, *args, **kwargs):
        super(TempoGrid, self).__init__(*args, **kwargs)
        grid = self.el
        self.tempo = widgets.FloatText(
            description="Tempo",
            value=120,
        )
        self.el = widgets.VBox([
            self.tempo,
            grid,
        ])

    @property
    def duration(self):
        return len(self.cells) * 60 / self.tempo.value

    def time(self, index):
        return index * 60 / self.tempo.value


class NoteGrid(TempoGrid):
    def __init__(self, num_columns, scale):
        self.scale = scale
        super(NoteGrid, self).__init__(len(self.scale), num_columns)

    @property
    def beat_duration(self):
        return 60 / self.tempo.value

    @property
    def sheet(self):
        notes = []
        for pitch, row in zip(reversed(self.scale), self.value):
            for x, value in enumerate(row):
                if value:
                    t = self.time(x)
                    notes.append(note.Note(pitch, self.beat_duration, t))
        return note.Sheet(notes, duration=self.duration)


class CallableGrid(TempoGrid):
    def __init__(self, num_columns, callables):
        self.callables = callables
        super(CallableGrid, self).__init__(len(self.callables), num_columns)


    @sampled
    def _play(self):
        samples = []
        for call, row in zip(self.callables, self.value):
            for x, value in enumerate(row):
                if value:
                    samples.append((self.time(x), call()))
        return merge(samples)

    @sampled
    def play(self, repeats=1):
        samples = []
        for i in range(repeats):
            samples.append((i * self.duration, self._play()))
        return merge(samples)
