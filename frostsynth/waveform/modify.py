def oddify(f):
    def oddified(phase, separation, *args, **kwargs):
        return 0.5 * (f(phase, *args, **kwargs) - f(phase + separation, *args, **kwargs))
    return oddified
