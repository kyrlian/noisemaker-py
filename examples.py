from signal_oscillator import Oscillator
from signal_track import Track, TrackElement
from const import Const
from signal_timedFloat import TimedFloat
from signal_customshape import customShape_yd, timedPairList_yd, CustomShape
from signal_sum import SignalSum
from helpers import accordMajeur, accordMineur, getSemiToneFreq, harmonics
import math
from plot import plotsignal
from random import random


def example_sin440():
    o440 = Oscillator(Const.SIN, 440.0)
    return Track([TrackElement(o440, 0, 10)], 0, 10, .1, "sintrack")


def example_pulse440():
    o2 = Oscillator(Const.PULSE, 440.0, width=.5, name="pulse 440")
    return Track().appendSignal(o2, .0, 5.0, .8).set(Const.AMPL, .5)


def example_majeurmineur():
    lfoa = customShape_yd([.0, .8, .4, .4, .0], .5).set(Const.AMPL, 1 / 1.3)
    envshape = timedPairList_yd([.0, .8, .4, .4, .0], .5)
    lfoa2 = CustomShape(.5, 1/1.3, envshape)
    tmajeur = accordMajeur(440.0)
    tmineur = accordMineur(440.0)
    return Track().appendSignal(tmajeur, .0, 5, TimedFloat(.8, lfoa)).appendSignal(tmineur, .0, 5.0, TimedFloat(.8, lfoa2))


def example_enveloppe():
    lfoa = CustomShape(
        points=[(.0, .0), (.1, .8), (.1, .5), (.2, .0), (.1, .0)])
    o2 = Oscillator(Const.SIN, 440.0, 0, TimedFloat(.8, lfoa))
    return Track().appendSignal(o2, .0, 5.0, 1.0)


def example_harmonicsTuning(baseFreq, nharmonics):
    sum = SignalSum(name=f"harmonicsTuning {nharmonics}")
    outOfTuneMax = .5  # ratio of basefreq
    tuningDuration = 10.0  # seconds
    stableDuration = 10.0  # seconds
    for i in range(1, nharmonics):
        f2pi = math.pow(2, float(i))
        n1Freq = baseFreq * f2pi
        n2Freq = getSemiToneFreq(n1Freq, 4)
        n3Freq = getSemiToneFreq(n1Freq, 7)
        # print("    harmonicsTuning:n1Freq:%v    ,n2Freq:%v    ,n3Freq:%v\n" % n1Freq, n2Freq, n3Freq)
        outOfTuneStart = (2.0 * random() - 1.0) * \
            outOfTuneMax  # +-outOfTuneMax
        tuningLfof = CustomShape(points=[
                                 (.0, 1.0 + outOfTuneStart), (tuningDuration, 1.0), (stableDuration, 1.0)]).setName("tuningLfof")
        plotsignal(
            tuningLfof, f"tuningLfof_{i}", 2*int(tuningDuration+stableDuration), 4410)
        plotsignal(TimedFloat(n1Freq, tuningLfof),
                   f"timedFloat_n1Freq_{i}", 2*int(tuningDuration+stableDuration), 4410)
        # print("tuningLfof.getperiod(.0):%v\n" % tuningLfof.getperiod(.0))
        accAmp = TimedFloat(1.0 / f2pi / 3)
        sum = sum. \
            appendSignal(Oscillator(Const.SIN, TimedFloat(n1Freq, tuningLfof), .0, accAmp)).\
            appendSignal(Oscillator(Const.SIN, TimedFloat(n2Freq, tuningLfof), .0, accAmp)).\
            appendSignal(Oscillator(Const.SIN, TimedFloat(
                n3Freq, tuningLfof), .0, accAmp))
    return sum.set(Const.AMPL, .8)


def example_drums():
    # var oHighKicks = oscillator_noise(CustomShape(points=[]xyPair{{.0, .0}, {.1, .8}, {.1, .1}, {.8, .0}}))
    tOscs = Track(name="SINSINNOISE").\
        appendSignal(Oscillator(Const.SIN, 55, 0, .7), .0, 5.0, 1.0).\
        appendSignal(Oscillator(Const.SIN, 110, .5, .6), .0, 5.0, 1.).\
        appendSignal(Oscillator(Const.NOISE, 1, 0, .1), .0, 5.0, .08)
    print(tOscs)
    # length of the last part of the enveloppe
    fslope = customShape_yd([1.0, .1], 2.0)
    enveloppe = [[.0, .0], [.2, .8], [.1, .6], [.1, .1],
                 (TimedFloat(.6, fslope), .0)]  # Envelope of the hit
    ampl = TimedFloat(.8, CustomShape(0, 1, enveloppe))
    drums = Track(name="DRUM+ENV")
    print(drums)
    drums.appendSignal(tOscs, .0, 5.0, ampl)
    print(drums)
    return drums


def example_combined1():
    # intro
    baseFreq = 22.5
    finalTrack = Track(name="main").appendSignal(
        harmonics(baseFreq, 6), 0, 5, 1.0)
    # bip
    i = 7
    f2pi = math.pow(2, float(i))
    lfoaBip = Oscillator(Const.PULSE, 4, 0, .9, .2)
    oBip = Oscillator(Const.SIN, baseFreq*f2pi, 0, 1.0/f2pi)
    oHighKicks = Oscillator(
        Const.NOISE, 1.0, 0, TimedFloat(.8, Oscillator(Const.PULSE, 8, .1, .2, .1)))
    finalTrack.\
        appendSignal(oBip, float(i)/5, float(i), TimedFloat(.8, lfoaBip)).\
        appendSignal(oHighKicks, float(i)/5, 5.0, 1)
    print(finalTrack)
    return finalTrack


def example_engine():
    tduration = 30.0
    nbh = 3
    # variable factor of the length of the silence
    variableSilence = [TimedFloat(1.0, customShape_yd([1.0, .01], tduration)), TimedFloat(.0)]
    otherPistonHit = [.2, .0]

    # .appendSignal(oscillator_noise(TimedFloat(.6)))
    piston1 = harmonics(75, nbh)
    enveloppe1 = [[.0, .0], [.1, .8], [.1, .0], variableSilence, otherPistonHit, variableSilence, otherPistonHit, variableSilence, otherPistonHit, variableSilence]  # Envelope of the hit 1
    cs1 = CustomShape(0, 1, enveloppe1)
    # global enveloppe uses the hit enveloppe, but with a viariable repetition frequency
    ampl1 = TimedFloat(.8, cs1)
    piston1.set(Const.AMPL, ampl1)
    print(piston1)

    # .appendSignal(oscillator_noise(TimedFloat(.5)))
    piston2 = harmonics(70, nbh)
    enveloppe2 = [otherPistonHit, variableSilence, [.0, .0], [.1, .8], [.1, .0], variableSilence, otherPistonHit, variableSilence, otherPistonHit, variableSilence]  # Envelope of the hit 1
    ampl2 = TimedFloat(.8, CustomShape(0, 1, enveloppe2))
    piston2.set(Const.AMPL, ampl2)
    print(piston2)

    # .appendSignal(oscillator_noise(TimedFloat(.4)))
    piston3 = harmonics(65, nbh)
    enveloppe3 = [otherPistonHit, variableSilence, otherPistonHit, variableSilence, [.0, .0], [.1, .8], [.1, .0], variableSilence, otherPistonHit, variableSilence]  # Envelope of the hit 1
    ampl3 = TimedFloat(.8, CustomShape(0, 1, enveloppe3))
    piston3.set(Const.AMPL, ampl3)
    print(piston3)

    # .appendSignal(oscillator_noise(TimedFloat(.3)))
    piston4 = harmonics(60, nbh)
    enveloppe4 = [otherPistonHit, variableSilence, otherPistonHit, variableSilence, otherPistonHit, variableSilence, [.0, .0], [.1, .8], [.1, .0], variableSilence]  # Envelope of the hit 1
    ampl4 = TimedFloat(.8, CustomShape(0, 1, enveloppe4))
    piston4.set(Const.AMPL, ampl4)
    print(piston4)

    engine = SignalSum(name="engine").\
        appendSignal(piston1).\
        appendSignal(piston2).\
        appendSignal(piston3).\
        appendSignal(piston4)
    print(engine)

    return engine
