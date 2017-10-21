import os.path

from numpy import *
from scipy.io import wavfile

from . import DATA_PATH
from .. import cumsum0
from ..analysis import hilbert
from ..chunk import chunkify, dechunkify
from ..window import pad, cosine

sample_rate, data = wavfile.read(os.path.join(DATA_PATH, "whistle.wav"))
data = data.astype(float) / 2.0 ** 15

chunks = chunkify(data, window=pad(cosine(1024), 512), overlap=4)

chunks = map(hilbert, chunks)

data = 2 * dechunkify(chunks, overlap=4)

phase = unwrap(angle(data))
frequency = diff(phase)
amplitude = abs(data)

vibrato = 1 + 0.03 * sin(linspace(0, 200, len(frequency)))

phase = cumsum0(frequency * vibrato * 0.5)
data = 2 * sin(phase + sin(5 * phase) * amplitude) * amplitude

filename = raw_input("Enter (WAV) output filename: ")
if filename:
    wavfile.write(filename, sample_rate, data)
else:
    print "No file given"
