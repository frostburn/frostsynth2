from __future__ import division

import numpy as np

from frostsynth import chunk


def test_identity():
    window = 32.0 - abs(np.arange(64) - 32)
    window /= 16
    overlap = 2
    data = np.random.randn(100)

    chunks = chunk.chunkify(data, window, overlap)
    clone = chunk.dechunkify(chunks, overlap)

    assert np.allclose(
        data[len(window)//2:-len(window)//2],
        clone[len(window)//2:len(data)-len(window)//2],
    )


def test_identity_ljust():
    window = 32.0 - abs(np.arange(64) - 32)
    window /= 16
    overlap = 2
    data = np.random.randn(100)

    chunks = chunk.chunkify(data, window, overlap, ljust=True)
    clone = chunk.dechunkify(chunks, overlap)

    assert np.allclose(
        data,
        clone[len(window)//2:][:len(data)]
    )


def test_short():
    window = np.ones(32)
    overlap = 4

    data = np.random.randn(10)

    chunks = chunk.chunkify(data, window, overlap)
    clone = chunk.dechunkify(chunks, overlap)
