from io import BytesIO

import numpy as np

from frostsynth import sampling


def test_merge():
    sampling.set_sample_rate(10)
    t = sampling.trange(1)
    result = sampling.merge([
        (0.5, t),
        (1, t),
        (2, t*t),
    ])
    assert np.allclose(result, [
       0, 0, 0, 0, 0, 0, 0.1, 0.2, 0.3, 0.4,
       0.5, 0.7 , 0.9 , 1.1 , 1.3 , 0.5 , 0.6 , 0.7 , 0.8 , 0.9 ,
       0, 0.01, 0.04, 0.09, 0.16, 0.25, 0.36, 0.49, 0.64, 0.81
    ])


def test_write_mono():
    sampling.set_sample_rate(10)
    t = sampling.trange(1)
    signal = np.sin(t)
    sio = BytesIO()
    sampling.write(sio, signal)
    assert (sio.getvalue() == b''
        b'RIFF8\x00\x00\x00WAVEfmt '
        b'\x10\x00\x00\x00\x01\x00\x01\x00\n\x00\x00\x00\x14\x00\x00\x00\x02\x00\x10\x00'
        b'data\x14\x00\x00\x00\x00\x00\xa6\x0c,\x19r%X1\xc0<\x8dG\xa2Q\xe7ZCc'
    )


def test_write_stereo():
    sampling.set_sample_rate(10)
    t = sampling.trange(1)
    left = np.sin(t)
    right = np.cos(t)
    sio = BytesIO()
    sampling.write(sio, [left, right])
    assert (sio.getvalue() == b''
        b'RIFFL\x00\x00\x00WAVEfmt '
        b'\x10\x00\x00\x00\x01\x00\x02\x00\n\x00\x00\x00(\x00\x00\x00\x04\x00\x10\x00'
        b'data(\x00\x00\x00\x00\x00\xb8~\xa6\x0c\x16~,\x191|r%\x0fyX1\xb7t\xc0<5o\x8dG\x96h\xa2Q\xeb`\xe7ZIXCc\xc5N'
    )


def test_read_mono():
    sio = BytesIO()
    sio.write(b''
        b'RIFF8\x00\x00\x00WAVEfmt '
        b'\x10\x00\x00\x00\x01\x00\x01\x00\n\x00\x00\x00\x14\x00\x00\x00\x02\x00\x10\x00'
        b'data\x14\x00\x00\x00\x00\x00\xa6\x0c,\x19r%X1\xc0<\x8dG\xa2Q\xe7ZCc'
    )
    sio.seek(0)
    signal = sampling.read_and_set_sample_rate(sio)
    t = sampling.trange(1)
    assert (sampling.get_sample_rate() == 10)
    assert np.allclose(np.sin(t), signal, 0.01, 0.01)


def test_read_stereo():
    sio = BytesIO()
    sio.write(b''
        b'RIFFL\x00\x00\x00WAVEfmt '
        b'\x10\x00\x00\x00\x01\x00\x02\x00\n\x00\x00\x00(\x00\x00\x00\x04\x00\x10\x00'
        b'data(\x00\x00\x00\x00\x00\xb8~\xa6\x0c\x16~,\x191|r%\x0fyX1\xb7t\xc0<5o\x8dG\x96h\xa2Q\xeb`\xe7ZIXCc\xc5N'
    )
    sio.seek(0)
    left, right = sampling.read_and_set_sample_rate(sio)
    t = sampling.trange(1)
    assert (sampling.get_sample_rate() == 10)
    assert np.allclose(np.sin(t), left, 0.01, 0.01)
    assert np.allclose(np.cos(t), right, 0.01, 0.01)
