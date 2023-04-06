from random import random
from signal_oscillator import Oscillator
from signal_track import Track
from const import Const
from signal_timedFloat import TimedFloat
from signal_customshape import customShape_xy, customShape_yd, timedPairList_yd, CustomShape
from signal_sum import SignalSum
from helpers import accordMajeur, accordMineur, getSemiToneFreq, harmonics
import math
from plot import plotsignal

def example_simple():
    o2 = Oscillator(Const.PULSE, 440.0)
    o2.setname("pulse 440")
    return Track().appendSignal(o2, .0, 5.0, .8).amplify(.5)

def example_majeurmineur():
    lfoa = customShape_yd([.0, .8, .4, .4, .0], .5).amplify(1 / 1.3)
    envshape = timedPairList_yd([.0, .8, .4, .4, .0], .5)
    lfoa2 = CustomShape(.5, 1/1.3, envshape)
    tmajeur = accordMajeur(440.0)
    tmineur = accordMineur(440.0)
    return Track().appendSignal(tmajeur, .0, 5, TimedFloat(.8, lfoa)).appendSignal(tmineur, .0, 5.0, TimedFloat(.8, lfoa2))

def example_enveloppe():
    lfoa = customShape_xy([(.0, .0), (.1, .8), (.1, .5), (.2, .0), (.1, .0)]) #x is relative
    o2 = Oscillator(Const.SIN, 440.0, 0, TimedFloat(.8, lfoa))
    return Track().appendSignal(o2, .0, 5.0, 1.0)

def example_harmonicsTuning(baseFreq, nharmonics):
    sum = SignalSum(name=f"harmonicsTuning {nharmonics}")
    outOfTuneMax = .5     #ratio of basefreq
    tuningDuration = 10.0 #seconds
    stableDuration = 10.0 #seconds
    for i in range(1, nharmonics):
        f2pi = math.Pow(2, float(i))
        n1Freq = baseFreq * f2pi
        n2Freq = getSemiToneFreq(n1Freq, 4)
        n3Freq = getSemiToneFreq(n1Freq, 7)
        #print("    harmonicsTuning:n1Freq:%v    ,n2Freq:%v    ,n3Freq:%v\n" % n1Freq, n2Freq, n3Freq)
        outOfTuneStart = (2.0*random.random() - 1.0) * outOfTuneMax #+-outOfTuneMax
        tuningLfof = customShape_xy([(.0, 1.0 + outOfTuneStart), (tuningDuration, 1.0), (stableDuration, 1.0)]).setName("tuningLfof")
        plotsignal(tuningLfof, f"tuningLfof_{i}", 2*int(tuningDuration+stableDuration), 4410)
        plotsignal(TimedFloat(n1Freq, tuningLfof), f"timedFloat_n1Freq_{i}", 2*int(tuningDuration+stableDuration), 4410)

        #print("tuningLfof.getperiod(.0):%v\n" % tuningLfof.getperiod(.0))
        accAmp = TimedFloat(1.0 / f2pi / 3)
        sum = sum. \
            appendSignal(Oscillator(Const.SIN, TimedFloat(n1Freq, tuningLfof), .0, accAmp)).\
            appendSignal(Oscillator(Const.SIN, TimedFloat(n2Freq, tuningLfof), .0, accAmp)).\
            appendSignal(Oscillator(Const.SIN, TimedFloat(n3Freq, tuningLfof), .0, accAmp))
    return sum.amplify(TimedFloat(.8))


def example_drums():
    #var oHighKicks = oscillator_noise(customShape_xy([]xyPair{{.0, .0}, {.1, .8}, {.1, .1}, {.8, .0}}))
    tOscs = Track().\
        appendSignal(Oscillator(Const.SIN, 55, 0, .7), .0, 5.0, 1.0).\
        appendSignal(Oscillator(Const.SIN, 110, .5, .6), .0, 5.0, 1.).\
        appendSignal(Oscillator(Const.NOISE,0, 0,.1), .0, 5.0, .08)
    fslope = customShape_yd([1.0, .1], 2.0)                                                          #length of the last part of the enveloppe
    enveloppe = [[.0, .0], [.2, .8], [.1, .6], [.1, .1], (TimedFloat(.6, fslope), .0)] #Envelope of the hit
    ampl = TimedFloat(.8, CustomShape(0,1, enveloppe))
    return Track().appendSignal(tOscs, .0, 5.0, ampl)



def example_combined1():
    #intro
    baseFreq = 22.5
    finalTrack = Track().appendSignal(harmonics(baseFreq, 6), 0, 5, 1.0)
    #bip
    i = 7
    f2pi = math.Pow(2, float(i))
    lfoaBip = Oscillator(Const.PULSE,4,0, .9, .2)
    oBip = Oscillator(Const.SIN, baseFreq*f2pi, 0, 1.0/f2pi)
    oHighKicks = Oscillator(Const.NOISE, 0,0, TimedFloat(.8, Oscillator(Const.PULSE,8, .1, .2, .1)))
    return finalTrack.\
        appendSignal(oBip, float(i)/5, float(i), TimedFloat(.8, lfoaBip)).\
        appendSignal(oHighKicks, float(i)/5, 5.0, 1)


def example_engine():
    tduration = 30.0
    nbh = 3
    variableSilence = [TimedFloat(1.0, customShape_yd([1.0, .01], tduration)), TimedFloat(.0)] #variable factor of the length of the silence
    otherPistonHit = [.2, .0]

    piston1 = harmonics(75, nbh)                                                                                                                                                     #.appendSignal(oscillator_noise(TimedFloat(.6)))
    enveloppe1 = [[.0, .0], [.1, .8], [.1, .0], variableSilence, otherPistonHit, variableSilence, otherPistonHit, variableSilence, otherPistonHit, variableSilence] #Envelope of the hit 1
    cs1 = CustomShape(0,1, enveloppe1)
    ampl1 = TimedFloat(.8, cs1) #global enveloppe uses the hit enveloppe, but with a viariable repetition frequency
    #print("    example_engine:cs1.getperiod(.0):%v\n" % cs1.getperiod(.0))

    piston2 = harmonics(70, nbh)                                                                                                                                                     #.appendSignal(oscillator_noise(TimedFloat(.5)))
    enveloppe2 = [otherPistonHit, variableSilence, [.0, .0], [.1, .8], [.1, .0], variableSilence, otherPistonHit, variableSilence, otherPistonHit, variableSilence] #Envelope of the hit 1
    ampl2 = TimedFloat(.8, CustomShape(0,1, enveloppe2))

    piston3 = harmonics(65, nbh)                                                                                                                                                     #.appendSignal(oscillator_noise(TimedFloat(.4)))
    enveloppe3 = [otherPistonHit, variableSilence, otherPistonHit, variableSilence, [.0, .0], [.1, .8], [.1, .0], variableSilence, otherPistonHit, variableSilence] #Envelope of the hit 1
    ampl3 = TimedFloat(.8, CustomShape(0,1, enveloppe3))

    piston4 = harmonics(60, nbh)                                                                                                                                                     #.appendSignal(oscillator_noise(TimedFloat(.3)))
    enveloppe4 = [otherPistonHit, variableSilence, otherPistonHit, variableSilence, otherPistonHit, variableSilence, [.0, .0], [.1, .8], [.1, .0], variableSilence] #Envelope of the hit 1
    ampl4 = TimedFloat(.8, CustomShape(0,1, enveloppe4))

    return SignalSum(name="engine").\
        appendSignal(piston1.setampl(ampl1)).\
        appendSignal(piston2.setampl(ampl2)).\
        appendSignal(piston3.setampl(ampl3)).\
        appendSignal(piston4.setampl(ampl4))