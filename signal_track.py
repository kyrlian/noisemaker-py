
from const import Const
from soundsignal import SoundSignal
from signal_timedFloat import TimedFloat, toTimedFloat
from signal_modifiers import Amplifier
import numpy

class TrackElement(SoundSignal):
    # TrackElement with a start and end
    def __init__(self, soundsignal: SoundSignal, start: float = 0, end: float = 1,  ampl=.1):
        self.soundsignal = soundsignal
        self.start = start
        self.end = end
        self.ampl = toTimedFloat(ampl)

    def __str__(self):
        return self.soundsignal.__str__()

class Track:
    # Track is a collection of track elements
    def __init__(self, trackelements=None, start: float = 0, end: float = 1,  ampl=.1, name=""):
        # using trackelements=[] in the declaration gave weird result when initializing with Track(name="that") : I had the elements of the previous track declaration !
        if trackelements is None:
            trackelements=[]
        self.trackelements = trackelements
        self.start = start
        self.end = end
        self.ampl = toTimedFloat(ampl)
        self.name = name

    def __str__(self):
        elems = ", ".join(list(map(lambda e: e.__str__(),self.trackelements)))
        return f"Track {self.name}, elements: [{elems}]"

    def set(self, elem, s):
        match elem:
            case Const.AMPL:
                self.ampl = toTimedFloat(s)
            case other:
                print(f"WARNING: Track.set:unkown element:{elem}\n")
        return self

    def appendSignal(self, soundsignal, start, end,  ampl=.1):
        self.trackelements.append(TrackElement(soundsignal, start, end, ampl))
        self.start = min(self.start, start)
        self.end = max(self.end, end)
        return self

    def getval(self, t:numpy.ndarray):
        r = .0
        tmin = numpy.min(t)
        tmax = numpy.max(t)
        #print(f"name:{self.name}, tmin:{tmin}, tmax:{tmax}")
        for elem in self.trackelements:
            #print(elem.soundsignal.name)
            if tmax >= elem.start and tmin <= elem.end:
                subt = t - elem.start
                v = elem.soundsignal.getval(subt)
                a = elem.ampl.getval(subt)
                r += v * numpy.maximum(0, a)
        return r * self.ampl.getval(t)
