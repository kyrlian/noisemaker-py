import math
from soundsignal import SoundSignal
from const import Const
from signal_timedFloat import TimedFloat, toTimedFloat
import numpy


class CustomShape(SoundSignal):
    def __init__(self, phase=0.0, ampl=1.0, points=[], name=""):
        self.phase = toTimedFloat(phase)
        self.ampl = toTimedFloat(ampl)
        self.points = []
        for xy in points:
            self.points.append([toTimedFloat(xy[0]), toTimedFloat(xy[1])])
        self.name = name
        # x is relative to previous, to enable to change part of the shape only - y is absolute

    def set(self, elem, s):
        match elem:
            case Const.PHASE:
                self.phase = toTimedFloat(s)
            case Const.AMPL:
                self.ampl = toTimedFloat(s)
            case other:
                print(f"WARNING: CustomShape.set:unkown element:{elem}\n")
        return self

    def setName(self, n):
        self.name = n
        return self

    def getperiod(self, t):
        points = self.points
        period = .0
        # iterate on all points of the shape, get the x value at t, and add
        # t is a numpy array of times, so we'll get a numpy array of periods at each time
        for point in points:
            period += point[0].getval(t)
        return period

    def getval(self, t:numpy.ndarray):
        phase = self.phase.getval(t)
        points = self.points
        period = self.getperiod(t)
        tmod = numpy.fmod(t+(phase*period), period)  # adjusted time: O-p
        previousx = points[0][0].getval(tmod)
        previousy = points[0][1].getval(tmod)
        y = .0
        #t is an array of time, I need to find in wich segment of the shape each t is 
        for point in points[1:]: #TODO rewrite now t is an array of times
            deltax = point[0].getval(t)  # x is relative
            nextx = previousx + deltax
            nexty = point[1].getval(t)
            #if previousx <= tmod and tmod < nextx:
            #    y = previousy + (tmod-previousx)/(deltax)*(nexty-previousy)
            test = ( previousx <= tmod )*( tmod < nextx)
            y += test * ( previousy + (tmod-previousx)/(deltax)*(nexty-previousy) )
            previousx = nextx
            previousy = nexty
        return y * self.ampl.getval(t)

# CONSTRUCTORS - helpers

def timedPairList_yd(ylist, duration):
    # build an array of xy from a list of y and a total duration
    nbpoints = len(ylist)
    tfx = duration / (float(nbpoints - 1))
    res = [[.0, ylist[0]]]
    for i in range(nbpoints):
        res.append([tfx, ylist[i]])  # x is relative to previous
    return res

def customShape_yd(ylist, duration):
    return CustomShape(.0, 1.0, timedPairList_yd(ylist, duration))
