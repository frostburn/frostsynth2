import numpy as np
from scipy.interpolate import interp1d

from .sampling import sampled

def sheet_to_pitch(sheet, attack):
    """
    Early attack
    """
    data = []
    for note in sheet.notes:
        data.append((note.time, note.pitch))
    data.sort()

    last_time = 0
    last_pitch = data[0][1]
    attacks = []
    for time, pitch in data:
        if time - attack > last_time:
            attacks.append((time - attack, last_pitch))
        last_time = time
        last_pitch = pitch

    data.extend(attacks)
    data.sort()

    x, y = zip(*data)

    return interp1d(
        x, y,
        bounds_error=False,
        fill_value=(data[0][1], data[-1][1]),
        assume_sorted=True
    )


def sheet_to_amplitude(sheet, attack, release):
    """
    Late attack
    """
    data = []
    for note in sheet.notes:
        data.append((note.time, note.duration, note.velocity))
    data.sort()

    envelopes = []
    for time, duration, velocity in data:
        if duration > attack:
            envelopes.append(interp1d(
                [time, time + attack, time + duration, time + duration + release],
                [0, velocity, velocity, 0],
                bounds_error=False,
                fill_value=(0, 0),
                assume_sorted=True
            ))
        else:
            envelopes.append(interp1d(
                [time, time + attack, time + attack + release],
                [0, velocity, 0],
                bounds_error=False,
                fill_value=(0, 0),
                assume_sorted=True
            ))

    # TODO: Pre-calculate the segments
    def amplitude(t):
        if not envelopes:
            return t * 0
        result = envelopes[0](t)
        for envelope in envelopes[1:]:
            result = np.maximum(result, envelope(t))
        return result

    return amplitude
