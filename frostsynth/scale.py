import numpy as np

MAJOR_PITCHES = np.array([0, 2, 4, 5, 7, 9, 11])
MINOR_PITCHES = np.array([0, 2, 3, 5, 7, 8, 10])


def stack_octaves(scale, octaves):
    pitches = []
    offset = 0
    for _ in range(octaves):
        pitches.append(MAJOR_PITCHES + offset)
        offset += 12
    return np.concatenate(pitches)


def major(start=60, octaves=1):
    return stack_octaves(MAJOR_PITCHES, octaves) + start


def minor(start=57, octaves=1):
    return stack_octaves(MINOR_PITCHES, octaves) + start


def scale_round(pitch, scale=None):
    if scale is None:
        return np.around(pitch)

    result = []
    note = 0
    for value in pitch:
        if np.isnan(value):
            result.append(float("nan"))
            continue
        current = abs(value - scale[note])
        while note > 0 and abs(value - scale[note - 1]) < current:
            note -= 1
        while note < len(scale) - 1 and abs(value - scale[note + 1]) < current:
            note += 1
        result.append(scale[note])

    return np.array(result, dtype=float)
