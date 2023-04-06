import math
from soundsignal import SoundSignal
from const import Const
from signal_timedFloat import TimedFloat, toTimedFloat


class CustomShape(SoundSignal):
    def __init__(self, phase=0.0, ampl=1.0, points=[], name=""):
        self.phase = toTimedFloat(phase)
        self.ampl = toTimedFloat(ampl)
        self.points = points
        self.name = name
        # x is relative to previous, to enable to change part of the shape only - y is absolute

    def set(self, elem, s):
        match elem:
            case Const.PHASE:
                self.phase = s
            case Const.AMPL:
                self.ampl = s
            case other:
                print(f"WARNING: CustomShape.set:unkown element:{elem}\n")
        return self

    def setName(self, n):
        self.name = n
        return self

    def getperiod(self, t):
        points = self.points
        period = .0
        for i in range(len(points)):
            period += points[i][0].getval(t)
        return period

    def getval(self, t):
        phase = self.phase.getval(t)
        points = self.points
        period = self.getperiod(t)
        tmod = math.fmod(t+(phase*period), period)  # adjusted time: O-p
        previousx = points[0][0].getval(tmod)
        previousy = points[0][1].getval(tmod)
        y = .0
        for i in range(len(points)):
            point = points[i]
            deltax = point[0].getval(t)  # x is relative
            nextx = previousx + deltax
            nexty = point[1].getval(t)
            if previousx <= tmod and tmod < nextx:
                y = previousy + (tmod-previousx)/(deltax)*(nexty-previousy)
                # print("    getcustomval;x;%v;y;%v;\n" % x, y)
            previousx = nextx
            previousy = nexty
        return y * self.ampl.getval(t)


# CONSTRUCTORS - helpers

def timedPairList_yd(ylist, duration):
    # build an array of xy from a list of y and a total duration
    nbpoints = len(ylist)
    tfx = TimedFloat(duration / (float(nbpoints - 1)))
    res = [(TimedFloat(.0), TimedFloat(ylist[0]))]
    for i in range(nbpoints):
        res.append([tfx, TimedFloat(ylist[i])])  # x is relative to previous
    return res

def customShape_xy(xylist):
    timedpairlist = []
    for xy in xylist:
        timedpairlist.append([toTimedFloat(xy[0]), toTimedFloat(xy[1])])
    return CustomShape(.0, 1.0, timedpairlist)

def customShape_yd(ylist, duration):
    return CustomShape(.0, 1.0, timedPairList_yd(ylist, duration))
