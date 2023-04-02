from const import Const
from soundsignal import SoundSignal


class SignalSum(SoundSignal):
    #SignalSum is a collection of signals

    def __init__(self, elements=[], ampl=1, name=""):
        self.elements = elements
        self.ampl     = ampl
        self.name     = name

    def set(self, elem, s):
        match elem:
            case Const.AMPL:
                self.ampl = s
            case other:
                print(f"WARNING: SignalSum.set:unkown element:{elem}\n")
        return self

    def setampl(self, s):
        return self.set(Const.AMPL, s)

    def appendSignal(self, s):
        self.elements.append( s)
        return self

    def getval(self, t):
        r = .0
        for e in self.elements :
            r += e.getval(t)
        return r * self.ampl.getval(t)
