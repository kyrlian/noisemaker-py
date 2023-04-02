package main

import
#    "fmt"
"fmt"
"math"
"math/rand"

def example_simple():
    o2 = oscillator_sf(PULSE, 440.0)
    o2.setname("pulse 440")
    return NewTrack().appendSignal(o2, .0, 5.0, tf(.8)).amplify(tf(.5))

_ = example_simple()

    #Avoid not used error

def example_majeurmineur():
    lfoa = customShape_yd([](float64)(.0, .8, .4, .4, .0), .5).amplify(tf(1 / 1.3))
    envshape = timedPairList_yd([](float64)(.0, .8, .4, .4, .0), .5)
    lfoa2 = customShape(tf(.5), tf(1/1.3), envshape)
    tmajeur = accordMajeur(440.0)
    tmineur = accordMineur(440.0)
    return NewTrack().
        appendSignal(tmajeur, .0, 5, timedFloat(.8, lfoa)).
        appendSignal(tmineur, .0, 5.0, timedFloat(.8, lfoa2))

_ = example_majeurmineur()

    #Avoid not used error

def example_enveloppe():
    lfoa = customShape_xy([]xyPair((.0, .0), (.1, .8), (.1, .5), (.2, .0), (.1, .0))) #x is relative
    o2 = oscillator(SIN, tf(440.0), tf(0), timedFloat(.8, lfoa))
    return NewTrack().appendSignal(o2, .0, 5.0, tf(1.0))

_ = example_enveloppe()

    #Avoid not used error

def example_harmonicsTuning(baseFreq, nharmonics):
    sum = signalSum_n("harmonicsTuning" + fmt.Sprint(nharmonics))
    outOfTuneMax = .5     #ratio of basefreq
    tuningDuration = 10.0 #seconds
    stableDuration = 10.0 #seconds
    for i = 1; i <= nharmonics; i += 1:
        f2pi = math.Pow(2, float(i))
        n1Freq = baseFreq * f2pi
        n2Freq = getSemiToneFreq(n1Freq, 4)
        n3Freq = getSemiToneFreq(n1Freq, 7)
        #print("    harmonicsTuning:n1Freq:%v    ,n2Freq:%v    ,n3Freq:%v\n" % n1Freq, n2Freq, n3Freq)
        outOfTuneStart = (2.0*rand.Float64() - 1.0) * outOfTuneMax #+-outOfTuneMax
        tuningLfof = customShape_xy([]xyPair((.0, 1.0 + outOfTuneStart), (tuningDuration, 1.0), (stableDuration, 1.0))).setName("tuningLfof")
        plotsignal(tuningLfof, "tuningLfof_"+fmt.Sprint(i), 2*int(tuningDuration+stableDuration), 4410)
        plotsignal(timedFloat(n1Freq, tuningLfof), "timedFloat_n1Freq_"+fmt.Sprint(i), 2*int(tuningDuration+stableDuration), 4410)

        #print("tuningLfof.getperiod(.0):%v\n" % tuningLfof.getperiod(.0))
        accAmp = tf(1.0 / f2pi / 3)
        sum = sum.
            appendSignal(oscillator(SIN, timedFloat(n1Freq, tuningLfof), tf(.0), accAmp)).
            appendSignal(oscillator(SIN, timedFloat(n2Freq, tuningLfof), tf(.0), accAmp)).
            appendSignal(oscillator(SIN, timedFloat(n3Freq, tuningLfof), tf(.0), accAmp))
    return sum.amplify(tf(.8))

_ = example_harmonicsTuning(22.5, 10)

    #Avoid not used error

def example_drums():
    #var oHighKicks = oscillator_noise(customShape_xy([]xyPair{{.0, .0}, {.1, .8}, {.1, .1}, {.8, .0}}))
    tOscs = NewTrack().
        #appendSignal(oHighKicks, .0, 5.0, tf(1.0)).
        appendSignal(oscillator(SIN, tf(55.0), tf(0), tf(.7)), .0, 5.0, tf(1.0)).
        appendSignal(oscillator(SIN, tf(110.0), tf(.5), tf(.6)), .0, 5.0, tf(1.0)).
        appendSignal(oscillator_noise(tf(.1)), .0, 5.0, tf(.08))
    fslope = customShape_yd([]float(1.0, .1), 2.0)                                                          #length of the last part of the enveloppe
    enveloppe = []TimedPair(tp(.0, .0), tp(.2, .8), tp(.1, .6), tp(.1, .1), (timedFloat(.6, fslope), tf(.0))) #Envelope of the hit
    ampl = timedFloat(.8, customShape(tf(0), tf(1.0), enveloppe))
    return NewTrack().appendSignal(tOscs, .0, 5.0, ampl)

_ = example_drums()

    #Avoid not used error

def example_combined1():
    #intro
    baseFreq = 22.5
    finalTrack = NewTrack().appendSignal(harmonics(baseFreq, 6), 0, 5, tf(1.0))
    #bip
    i = 7
    f2pi = math.Pow(2, float(i))
    lfoaBip = oscillator_pulse(tf(4), tf(0), tf(.9), tf(.2))
    oBip = oscillator(SIN, tf(baseFreq*f2pi), tf(0), tf(1.0/f2pi))
    oHighKicks = oscillator(NOISE, tf(0), tf(0), timedFloat(.8, oscillator_pulse(tf(8), tf(.1), tf(.2), tf(.1))))
    finalTrack = finalTrack.
        appendSignal(oBip, float(i)/5, float(i), timedFloat(.8, lfoaBip)).
        appendSignal(oHighKicks, float(i)/5, 5.0, tf(1))
    #finalise
    return finalTrack

_ = example_combined1()

    #Avoid not used error

def example_engine():
    tduration = 30.0
    nbh = 3
    variableSilence = TimedPair(timedFloat(1.0, customShape_yd([](float64)(1.0, .01), tduration)), tf(.0)) #variable factor of the length of the silence
    otherPistonHit = TimedPair(tf(.2), tf(.0))

    piston1 = harmonics(75, nbh)                                                                                                                                                     #.appendSignal(oscillator_noise(tf(.6)))
    enveloppe1 = []TimedPair(tp(.0, .0), tp(.1, .8), tp(.1, .0), variableSilence, otherPistonHit, variableSilence, otherPistonHit, variableSilence, otherPistonHit, variableSilence) #Envelope of the hit 1
    cs1 = customShape(tf(0), tf(1.0), enveloppe1)
    ampl1 = timedFloat(.8, cs1) #global enveloppe uses the hit enveloppe, but with a viariable repetition frequency
    #print("    example_engine:cs1.getperiod(.0):%v\n" % cs1.getperiod(.0))

    piston2 = harmonics(70, nbh)                                                                                                                                                     #.appendSignal(oscillator_noise(tf(.5)))
    enveloppe2 = []TimedPair(otherPistonHit, variableSilence, tp(.0, .0), tp(.1, .8), tp(.1, .0), variableSilence, otherPistonHit, variableSilence, otherPistonHit, variableSilence) #Envelope of the hit 1
    ampl2 = timedFloat(.8, customShape(tf(0), tf(1.0), enveloppe2))

    piston3 = harmonics(65, nbh)                                                                                                                                                     #.appendSignal(oscillator_noise(tf(.4)))
    enveloppe3 = []TimedPair(otherPistonHit, variableSilence, otherPistonHit, variableSilence, tp(.0, .0), tp(.1, .8), tp(.1, .0), variableSilence, otherPistonHit, variableSilence) #Envelope of the hit 1
    ampl3 = timedFloat(.8, customShape(tf(0), tf(1.0), enveloppe3))

    piston4 = harmonics(60, nbh)                                                                                                                                                     #.appendSignal(oscillator_noise(tf(.3)))
    enveloppe4 = []TimedPair(otherPistonHit, variableSilence, otherPistonHit, variableSilence, otherPistonHit, variableSilence, tp(.0, .0), tp(.1, .8), tp(.1, .0), variableSilence) #Envelope of the hit 1
    ampl4 = timedFloat(.8, customShape(tf(0), tf(1.0), enveloppe4))

    return signalSum_n("engine").
        appendSignal(piston1.setampl(ampl1)).
        appendSignal(piston2.setampl(ampl2)).
        appendSignal(piston3.setampl(ampl3)).
        appendSignal(piston4.setampl(ampl4))

_ = example_engine() #Avoid not used error
