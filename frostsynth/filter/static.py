from ..sampling import sampled, get_sample_rate
from .. import tau
from .base import Biquad


class Lowpass(Biquad):
    @sampled
    def __init__(self, freq, Q):
        super(Lowpass, self).__init__()
        w0 = freq * tau / get_sample_rate()
        alpha = sin(w0) / (2 * Q)
        self.b0 = (1 - cos(w0))/2
        self.b1 =  1 - cos(w0)
        self.b2 = (1 - cos(w0))/2
        self.a0 =  1 + alpha
        self.a1 = -2 * cos(w0)
        self.a2 =  1 - alpha
