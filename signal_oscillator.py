from soundsignal import SoundSignal
from const import Const
import numpy
from random import random
from signal_timedFloat import TimedFloat, toTimedFloat


class Oscillator(SoundSignal):

    def __init__(self, shape=Const.SIN, freq: SoundSignal = 440, phase: SoundSignal = 0, ampl: SoundSignal = .1, width=.5, name=""):
        self.shape = shape
        assert freq is not 0
        self.freq = toTimedFloat(freq)
        self.phase = toTimedFloat(phase)
        self.ampl = toTimedFloat(ampl)
        # optional, to set the width of the top of the PULSE shape
        self.width = toTimedFloat(width)
        if name == "":
            name = f"{shape}-{freq}"
        self.name = name

    def __str__(self):
        return f"Oscillator {self.name} {self.shape} {self.freq.base}"

    def setname(self, str):
        self.name = str
        return self

    def set(self, elem, s: SoundSignal):
        match elem:
            case Const.FREQ:
                self.freq = toTimedFloat(s)
            case Const.PHASE:
                self.phase = toTimedFloat(s)
            case Const.AMPL:
                self.ampl = toTimedFloat(s)
            case Const.WIDTH:
                self.width = toTimedFloat(s)
            case other:
                print("WARNING: Oscillator.set:unkown element:%v\n" % elem)
        return self

    def getval(self, t):
        freq = self.freq.getval(t)
        phase = 0
        if self.phase is not None:
            phase = self.phase.getval(t)
        period = 1.0 / freq
        tmod = numpy.fmod(t, period)
        xmod = numpy.fmod(tmod * freq + phase, 1)
        # print("    Oscillator:getval:x:%v,xmod:%v\n" % x, xmod)
        y = 0.0
        match self.shape:  # All shapes have a period of 1
            case Const.SIN:
                y = numpy.sin(2.0 * numpy.pi * xmod)
            case Const.FLAT:
                y = 1.0
            case Const.SQR:
                y = (xmod < .5) * 2 - 1
            case Const.PULSE:
                # with width=.5 it's just a square
                # gives 1 if test is True, -1 if False
                y = (xmod < self.width.getval(t)) * 2 - 1  
            case Const.SAW:  # ramp up
                y = -1.0 + 2*xmod
            case Const.ISAW:  # ramp down
                y = 1.0 - 2*xmod
            case Const.TRI:  # ramp up and down
                # m is -1/+1
                m = (xmod < .5) * 2 - 1 
                y = 1 - 2 * m + m * 4 * xmod
                #if xmod < .5:
                #    y = -1.0 + 4.0 * xmod
                #else:
                #    y = 3.0 - 4.0 * xmod
            case Const.NOISE:
                y = 2.0 * random() - 1.0  # rand is [0.0,1.0)
                # if self.customshape is not None:
                #    y = getcustomshapeval(self.customshape, xmod, t)
            case other:
                print(
                    f"WARNING: Oscillator.getval:unkown shape:{self.shape}\n")
        return y * self.ampl.getval(t)  # can be negative - ex: LFOs
