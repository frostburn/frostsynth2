import numpy as np

TWO_ROOT_TWELVE = 1.0594630943592953
I_LOG_TWO_ROOT_TWELVE = 17.312340490667548
PITCH_FIX = 36.37631656229583


def mtof(pitch):
    """Midi pitch to frequency"""
    # Same as 440.0 * pow(2.0, (pitch - 69) / 12.0);
    return TWO_ROOT_TWELVE ** (pitch + PITCH_FIX)


def ftom(freq):
    """Frequency to midi pitch"""
    return np.log(freq) * I_LOG_TWO_ROOT_TWELVE - PITCH_FIX


def itor(interval):
    """Midi interval to frequency ratio"""
    return TWO_ROOT_TWELVE ** interval


def rtoi(ratio):
    """Frequency ratio to midi interval"""
    return np.log(ratio) * I_LOG_TWO_ROOT_TWELVE
