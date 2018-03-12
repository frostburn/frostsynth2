from __future__ import division
import os.path

from numpy import *
from scipy.io import wavfile

from . import DATA_PATH
from ..process import decompose_frequency
from ..filter import Polezero
from ..waveform import sine, softsaw
from ..sampling import read_and_set_sample_rate, write

data = read_and_set_sample_rate(os.path.join(DATA_PATH, "ocarina.wav"))

frequency, amplitude = decompose_frequency(data)

polezero = Polezero()
polezero.a1 = -1
polezero.b0 = 0.003
polezero.a0 = polezero.b0 - polezero.a1
polezero.b1 = 0
frequency = array(polezero.map(frequency))

polezero = Polezero()
polezero.a1 = -1
polezero.b0 = 0.1
polezero.a0 = polezero.b0 - polezero.a1
polezero.b1 = 0
amplitude = maximum(0, array(polezero.map(amplitude)) - 0.01)
amplitude = concatenate((amplitude[:-1000], zeros(1000)))

phase = cumsum(frequency)

amplitude /= amplitude.max()
data = softsaw(phase * 0.25 + 0.06 * sine(phase * 1.75), cbrt(amplitude) * 0.96) * amplitude

filename = raw_input("Enter (WAV) output filename: ")
if filename:
    write(filename, data)
else:
    print "No file given"
