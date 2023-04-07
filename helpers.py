import math
from signal_sum import SignalSum
from signal_oscillator import Oscillator
from const import Const


def root(x, n):
    lower = .0
    upper = x
    r = .0
    while upper-lower >= 0.000000001:
        r = (upper + lower) / 2.0
        temp = math.pow(r, n)
        if temp > x:
            upper = r
        else:
            lower = r
    return r


semiToneConst = root(2.0, 12)  # 1,05946309435929
toneConst = root(2.0, 7)  # 1,104089513673812


def getSemiToneFreq(fstart, nsemitones):
    nfreq = fstart * math.pow(semiToneConst, float(nsemitones))
    return nfreq


def accord3(baseFreq, gap1, gap2):  # 3,4
    return SignalSum(). \
        appendSignal(Oscillator(Const.SIN, baseFreq, ampl=.7)). \
        appendSignal(Oscillator(Const.SIN, getSemiToneFreq(baseFreq, gap1),ampl=.6)). \
        appendSignal(Oscillator(Const.SIN, getSemiToneFreq(baseFreq, gap1+gap2),ampl=.5))


def accordMineur(fstart):
    return accord3(fstart, 3, 4)


def accordMajeur(fstart):
    return accord3(fstart, 4, 3)


def harmonics(baseFreq, nharmonics):
    sum = SignalSum(name=f"harmonics {nharmonics}")
    for i in range(1, nharmonics):
        f2pi = math.pow(2, float(i))
        sum = sum.appendSignal(Oscillator(
            Const.SIN, baseFreq*f2pi, .0, 1.0/f2pi))
    return sum
