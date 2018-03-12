from __future__ import division
import os.path

from numpy import *
from scipy.io import wavfile

from . import DATA_PATH
from ..process import decompose_frequency
from ..filter import Polezero
from ..sampling import time_like, read_and_set_sample_rate, shift, write

data = read_and_set_sample_rate(os.path.join(DATA_PATH, "whistle.wav"))

frequency, amplitude = decompose_frequency(data)

polezero = Polezero()
polezero.a1 = -1
polezero.b0 = 0.02
polezero.a0 = polezero.b0 - polezero.a1
polezero.b1 = 0
frequency = array(polezero.map(frequency))
amplitude = maximum(0, array(polezero.map(amplitude)) - 0.01)

vibrato = 1 + 0.02 * sin(time_like(frequency) * 5)

phase = cumsum(frequency * vibrato * 0.5)
data = 2 * sin(phase + sin(5 * phase) * amplitude) * amplitude

filename = raw_input("Enter (WAV) output filename: ")
if filename:
    write(filename, data)
else:
    print "No file given"
