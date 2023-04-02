from soundsignal import SoundSignal
from const import Const
import math
from random import random

class Oscillator(SoundSignal):
    def __init__(self,shape=Const.SIN,freq=440,phase=0,ampl=1,width=None,name=""):
        self.shape = shape
        self.freq  = freq
        self.phase = phase
        self.ampl  = ampl
        self.width = width # optional, to set the width of the top of the PULSE shape
        self.name  = name

    def setname(self, s):
        self.name = s
        return self

    def set(self, elem, s):
        match elem:
            case Const.FREQ:
                self.freq = s
            case Const.PHASE:
                self.phase = s
            case Const.AMPL:
                self.ampl = s
            case Const.WIDTH:
                self.width = s
            case other:
                print("WARNING: Oscillator.set:unkown element:%v\n" % elem)
        return self

    def getval(self, t):
        freq = self.freq.getval(t)
        phase = self.phase.getval(t)
        period = 1.0 / freq
        tmod = math.fmod(t, period)
        xmod = math.fmod(tmod*freq+phase, 1)
        #print("    Oscillator:getval:x:%v,xmod:%v\n" % x, xmod)
        y = 0.0
        match self.shape: #All shapes have a period of 1
            case Const.SIN:
                y = math.sin(2.0 * math.pi * xmod)
            case Const.FLAT:
                y = 1.0
            case Const.SQR:
                if xmod < .5:
                    y = 1.0
                else:
                    y = -1.0
            case Const.PULSE:
                if xmod < self.width.getval(t): #with width=.5 it's just a square
                    y = 1.0
                else:
                    y = -1.0
            case Const.SAW: #ramp up
                y = -1.0 + 2*xmod
            case Const.ISAW: #ramp down
                y = 1.0 - 2*xmod
            case Const.TRI: #ramp up and down
                if xmod < .5:
                    y = -1.0 + 4.0*xmod
                else:
                    y = 3.0 - 4.0*xmod
            case Const.NOISE:
                y = 2.0*random.random() - 1.0 #rand is [0.0,1.0)
                #if self.customshape is not None:
                #    y = getcustomshapeval(self.customshape, xmod, t)
            case other:
                print(f"WARNING: Oscillator.getval:unkown shape:{self.shape}\n" )
        return y * self.ampl.getval(t) #can be negative - ex for LFOs
