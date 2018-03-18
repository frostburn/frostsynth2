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
