import numpy as np
import ipywidgets as widgets

from .. import note


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


class NoteGrid(ToggleGrid):
    def __init__(self, num_columns, beat_duration, scale):
        self.scale = scale
        self.beat_duration = beat_duration
        super(NoteGrid, self).__init__(len(self.scale), num_columns)

    @property
    def duration(self):
        return len(self.cells) * self.beat_duration

    @property
    def sheet(self):
        notes = []
        for pitch, row in zip(reversed(self.scale), self.value):
            for x, value in enumerate(row):
                if value:
                    t = x * self.beat_duration
                    notes.append(note.Note(pitch, self.beat_duration, t))
        return note.Sheet(notes, duration=self.duration)
