from IPython.display import Audio as IAudio

from ..sampling import get_sample_rate


class Audio(IAudio):
    def __init__(self, data=None, filename=None, url=None, embed=None, rate=None, autoplay=True):
        rate = rate or get_sample_rate()
        super(Audio, self).__init__(data, filename, url, embed, rate, autoplay)

    def _make_wav(self, data, rate):
        """ Transform a numpy array to a PCM bytestring without normalizing """
        import struct
        from io import BytesIO
        import wave

        try:
            import numpy as np

            data = np.array(data, dtype=float)
            if len(data.shape) == 1:
                nchan = 1
            elif len(data.shape) == 2:
                # In wave files,channels are interleaved. E.g.,
                # "L1R1L2R2..." for stereo. See
                # http://msdn.microsoft.com/en-us/library/windows/hardware/dn653308(v=vs.85).aspx
                # for channel ordering
                nchan = data.shape[0]
                data = data.T.ravel()
            else:
                raise ValueError('Array audio input must be a 1D or 2D array')
            # --------- Begin frostsynth specific changes ------------
            scaled = np.int16(data*32767).tolist()
            # --------- End frostsynth specific changes --------------
        except ImportError:
            # check that it is a "1D" list
            idata = iter(data)  # fails if not an iterable
            try:
                iter(idata.next())
                raise TypeError('Only lists of mono audio are '
                    'supported if numpy is not installed')
            except TypeError:
                # this means it's not a nested list, which is what we want
                pass
            # --------- Begin frostsynth specific changes ------------
            maxabsvalue = 1
            # --------- End frostsynth specific changes --------------
            scaled = [int(x/maxabsvalue*32767) for x in data]
            nchan = 1

        fp = BytesIO()
        waveobj = wave.open(fp,mode='wb')
        waveobj.setnchannels(nchan)
        waveobj.setframerate(rate)
        waveobj.setsampwidth(2)
        waveobj.setcomptype('NONE','NONE')
        waveobj.writeframes(b''.join([struct.pack('<h',x) for x in scaled]))
        val = fp.getvalue()
        waveobj.close()

        return val
