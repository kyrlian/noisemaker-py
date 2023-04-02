import math
from soundsignal import SoundSignal
from signal_timedFloat import TimedFloat
from const import Const

class xyPair:
    #xyPair is a simple x,y struct, for custom shapes
    def __init__(self,x,y):
        self.x = x
        self.y = y

class TimedPair:
    def __init__(self,tfx,tfy):
        self.x = tfx
        self.y = tfy

class CustomShape(SoundSignal):
    def __init__(self,phase=0.0,ampl=1.0,points=[], name=""):
        self.phase  = phase
        self.ampl   = ampl
        self.points = points
        self.name   = name
        #x is relative to previous, to enable to change part of the shape only - y is absolute
        
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
            period += points[i].x.getval(t)
        return period

    def getval(self, t):
        phase = self.phase.getval(t)
        points = self.points
        period = self.getperiod(t)
        tmod = math.fmod(t+(phase*period), period) #adjusted time: O-p
        previousx = points[0].x.getval(tmod)
        previousy = points[0].y.getval(tmod)
        y = .0
        for i in range(len(points)):
            point = points[i]
            deltax = point.x.getval(t) #x is relative
            nextx = previousx + deltax
            nexty = point.y.getval(t)
            if previousx <= tmod and tmod < nextx:
                y = previousy + (tmod-previousx)/(deltax)*(nexty-previousy)
                #print("    getcustomval;x;%v;y;%v;\n" % x, y)
            previousx = nextx
            previousy = nexty
        return y * self.ampl.getval(t)


#CONSTRUCTORS - helpers
def timedPairList_xy(xylist):
    res = [](TimedPair)()
    for xy in xylist :
        res.append( TimedPair(xy.x, xy.y))
    return res

def timedPairList_yd(ylist, duration):
    #build an array of xy from a list of y and a total duration
    nbpoints = len(ylist)
    tfx = TimedFloat(duration / (float(nbpoints - 1)))
    res = [](TimedPair)()
    res.append( TimedPair(TimedFloat(.0), TimedFloat(ylist[0])))
    for i in range(nbpoints):
        res.append( TimedPair(tfx, TimedFloat(ylist[i]))) #x is relative to previous

    return res

def customShape_tp(points):
    #lastx := points[len(points)-1].x
    return CustomShape(TimedFloat(.0), TimedFloat(1.0), points)
def customShape_xy(points):
    #var lastx = points[len(points)-1].x
    #var freq = 1 / lastx
    #return customShape(tf(freq), tf(.0), tf(1.0), timedPairList_xy(points))
    return customShape_tp(timedPairList_xy(points))
def customShape_yd(ylist, duration):
    return customShape_tp(timedPairList_yd(ylist, duration))


