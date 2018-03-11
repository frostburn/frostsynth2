import numpy as np

EPSILON = 1e-12
tau = 2 * np.pi


def sine(phase):
    return np.sin(tau * phase)


def cosine(phase):
    return np.cos(tau * phase)


def softsaw(phase, sharpness):
    sharpness = np.clip(sharpness, EPSILON, 1.0 - EPSILON)
    return np.arctan(
        sharpness * sine(phase) / (1.0 + sharpness * cosine(phase))
    ) / np.arcsin(sharpness)


def softarc(phase, sharpness):
    too_small = (sharpness < EPSILON)
    return np.where(
        too_small,
        cosine(phase),
        np.where(
            sharpness < 1,
            (
                np.hypot(
                    (1 + sharpness) * cosine(0.5 * phase),
                    (1 - sharpness) * sine(0.5 * phase)
                ) - 1
            ) / (sharpness + too_small),
            abs(cosine(0.5 * phase)) * 2 - 1
        )
    )
