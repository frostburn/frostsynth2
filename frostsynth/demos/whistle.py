from __future__ import division
import os.path

from numpy import *
from scipy.io import wavfile

from . import DATA_PATH
from .. import tau
from ..process import decompose_frequency, clean_frequency
from ..filter import Polezero
from ..sampling import time_like, read_and_set_sample_rate, shift, write

data = read_and_set_sample_rate(os.path.join(DATA_PATH, "whistle.wav"))

frequency, amplitude = decompose_frequency(data)
frequency, amplitude = clean_frequency(frequency, amplitude)

vibrato = 1 + 0.02 * sin(time_like(frequency) * 5)

phase = cumsum(frequency * vibrato * 0.5) * tau
data = sin(phase + sin(5 * phase) * amplitude) * amplitude

filename = raw_input("Enter (WAV) output filename: ")
if filename:
    write(filename, data)
else:
    print "No file given"
