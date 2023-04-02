from soundsignal import SoundSignal

class TimedFloat(SoundSignal):

    def __init__(self,base,ampl=None):
        self.base = base
        self.ampl = ampl

    def getval(self, t):
        r = self.base
        if self.ampl is not None:
            r *= self.ampl.getval(t)
        return r
