from soundsignal import SoundSignal


def toTimedFloat(v):
    if type(v) is float or type(v) is int:
        return TimedFloat(v, None)
    return v


class TimedFloat(SoundSignal):

    def __init__(self, base: float, ampl: SoundSignal = None):
        self.base = base
        self.ampl = toTimedFloat(ampl)

    def getval(self, t):
        r = self.base
        if self.ampl is not None:
            r *= self.ampl.getval(t)
        return r
