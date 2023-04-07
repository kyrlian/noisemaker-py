from const import Const
from soundsignal import SoundSignal
from signal_timedFloat import toTimedFloat

class SignalSum(SoundSignal):
    # SignalSum is a collection of signals

    def __init__(self, elements=None, ampl=1, name=""):
        # using elements=[] in the declaration gave weird result when initializing with SignalSum(name="that") : I had the elements of the previous SignalSum declaration !
        if elements is None:
            elements=[]
        self.elements = elements
        self.ampl = toTimedFloat(ampl)
        self.name = name

    def __str__(self):
        elems = ", ".join(list(map(lambda e: e.__str__(),self.elements)))
        return f"SignalSum {self.name}, elements: [{elems}]"
    
    def set(self, elem, s):
        match elem:
            case Const.AMPL:
                self.ampl = toTimedFloat(s)
            case other:
                print(f"WARNING: SignalSum.set:unkown element:{elem}\n")
        return self

    def appendSignal(self, s):
        self.elements.append(s)
        return self

    def getval(self, t):
        r = .0
        for e in self.elements:
            r += e.getval(t)
        return r * self.ampl.getval(t)
