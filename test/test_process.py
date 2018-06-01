from __future__ import division
import numpy as np

from frostsynth import process


def test_fillnan():
    data = np.array([float("nan"), 1, 1, 2, 2, float("nan"), float("nan"), 3, 3, float("nan")])
    process.fillnan(data)
    assert (data == np.array([1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0])).all()


def test_steps_since():
    data = np.arange(10) * 0.3
    delta = 1 / np.array(process.steps_since_one(data))
    assert np.allclose(delta[delta != 0], 0.3)
