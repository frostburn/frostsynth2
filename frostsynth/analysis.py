from numpy.fft import fft, ifft


def hilbert(signal):
    frequencies = fft(signal)
    # Remove DC
    frequencies[0] = 0
    # Remove negative frequencies
    frequencies[len(frequencies) // 2:] = 0
    return 2 * ifft(frequencies)
