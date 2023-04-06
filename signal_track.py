
from const import Const
from soundsignal import SoundSignal
from signal_timedFloat import TimedFloat, toTimedFloat


class TrackElement(SoundSignal):
    # TrackElement with a start and end
    def __init__(self, soundsignal: SoundSignal, start: float = 0, end: float = 1,  ampl: SoundSignal = TimedFloat(.1)):
        self.soundsignal = soundsignal
        self.start = start
        self.end = end
        self.ampl = toTimedFloat(ampl)

class Track:
    # Track is a collection of track elements
    def __init__(self, elements=[], start: float = 0, end: float = 1,  ampl=TimedFloat(.1), name=""):
        self.elements = elements
        self.start = start
        self.end = end
        self.ampl = ampl
        self.name = name
        if type(ampl) is float:
            self.ampl = TimedFloat(ampl)

    def set(self, elem, s):
        match elem:
            case Const.AMPL:
                self.ampl = toTimedFloat(s)
            case other:
                print(f"WARNING: Track.set:unkown element:{elem}\n")
        return self

    def appendSignal(self, soundsignal, start, end,  ampl=.1):
        self.elements.append(TrackElement(soundsignal, start, end, toTimedFloat(ampl)))
        self.start = min(self.start, start)
        self.end = max(self.end, end)
        return self

    def getval(self, t):
        r = .0
        for elem in self.elements:
            # if t >= elem.start and t < elem.end:
            subt = t - elem.start
            v = elem.soundsignal.getval(subt)
            a = elem.ampl.getval(subt)
            r += v * max(0, a)
        return r * self.ampl.getval(t)
