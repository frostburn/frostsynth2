PITCHES_BASE = {
    "_C": 59,
    "=C": 60,
    "^C": 61,
    "_D": 61,
    "=D": 62,
    "^D": 63,
    "_E": 63,
    "=E": 64,
    "^E": 65,
    "_F": 64,
    "=F": 65,
    "^F": 66,
    "_G": 66,
    "=G": 67,
    "^G": 68,
    "_A": 68,
    "=A": 69,
    "^A": 70,
    "_B": 70,
    "=B": 71,
    "^B": 72,
}

# TODO: All of the key signatures
PITCHES = {
    "C": {
        "C": 60,
        "D": 62,
        "E": 64,
        "F": 65,
        "G": 67,
        "A": 69,
        "B": 71,
    },
    "G": {
        "C": 60,
        "D": 62,
        "E": 64,
        "F": 66,
        "G": 67,
        "A": 69,
        "B": 71,
    },
    "D": {
        "C": 61,
        "D": 62,
        "E": 64,
        "F": 66,
        "G": 67,
        "A": 69,
        "B": 71,
    },
    "F": {
        "C": 60,
        "D": 62,
        "E": 64,
        "F": 65,
        "G": 67,
        "A": 69,
        "B": 70,
    },
    "Bb": {
        "C": 60,
        "D": 62,
        "E": 63,
        "F": 65,
        "G": 67,
        "A": 69,
        "B": 70,
    },
}


for key, pitches in PITCHES.items():
    pitches.update(PITCHES_BASE)
    for note, pitch in list(pitches.items()):
        pitches[note.lower()] = pitch + 12

for pitches in PITCHES.values():
    pitches["z"] = None


PITCHES["Am"] = PITCHES["C"]
PITCHES["AMin"] = PITCHES["C"]
PITCHES["Em"] = PITCHES["G"]
PITCHES["EMin"] = PITCHES["G"]
PITCHES["Bm"] = PITCHES["D"]
PITCHES["BMin"] = PITCHES["D"]
PITCHES["Dm"] = PITCHES["F"]
PITCHES["DMin"] = PITCHES["F"]
PITCHES["Gm"] = PITCHES["Bb"]
PITCHES["GMin"] = PITCHES["Bb"]
