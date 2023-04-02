
import math
from const import Const
from soundsignal import SoundSignal

class TrackElement(SoundSignal):
    #TrackElement with a start and end
    def __init__(self,soundsignal,start=0,end=1,ampl=1.0):
        self.soundsignal = soundsignal
        self.start  = start
        self.end    =end
        self.ampl   = ampl #TODO maybe remove ampl from here, we can use .amplify on the signal if needed


class Track:
    #Track is a collection of track elements
    def __init__(self,elements=[],start=0,end=1,ampl=1.0,name=""):
        self.elements = elements
        self.start  = start
        self.end    =end
        self.ampl   = ampl
        self.name     = name

    def set(self, elem, s):
        match elem:
            case Const.AMPL:
                self.ampl = s
            case other:
                print(f"WARNING: Track.set:unkown element:{elem}\n")
        return self

    def appendSignal(self, signal, start, end, ampl):
        self.elements.append( TrackElement(signal, start, end, ampl))
        self.start = math.min(self.start, start)
        self.end = math.max(self.end, end)
        return self

    def getval(self, t):
        r = .0
        for elem in self.elements :
            if t >= elem.start and t < elem.end:
                subt = t - elem.start
                v = elem.signal.getval(subt)
                a = elem.ampl.getval(subt)
                r += v * math.Max(0, a)
        return r * self.ampl.getval(t)
