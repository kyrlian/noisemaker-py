import math
from soundsignal import SoundSignal

class Filter(SoundSignal):
    def __init__(self, low, high):
        self.input = input
        self.low = low
        self.high = high

    def getval(self, t):
        v = self.input.getval(t)
        if v < self.low:
            v = self.low
        elif v > self.high:
            v = self.high
        return v


class Inverter(SoundSignal):
    # takes an input signal and gives 1/signal(t)
    def __init__(self, input):
        self.input = input

    def getval(self, t):
        return 1 / self.input.getval(t)


class Power(SoundSignal):
    # takes an input signal and gives 2^signal(t)
    # With base = 2, the output signal of power is a v/oct - raising input by 1 doubles the output, raising 1 octave
    # with base = 2, the output signal of power is a v/oct - raising input by 1 doubles the output, raising 1 octave
    # with base = semiToneConst = root(2.0, 12) = 1,05946309435929, the output signal of power is a v/semitone
    # with base = semiToneConst = root(2.0, 12) = 1,05946309435929, the output signal of power is a v/semitone
    # with base = semiToneConst = root(2.0, 12) = 1,05946309435929, the output signal of power is a v/semitone
    # with base = semiToneConst = root(2.0, 12) = 1,05946309435929, the output signal of power is a v/semitone
    def __init__(self, input, base=2):
        self.input = input
        self.base = base

    def getval(self, t):
        return math.pow(self.base, self.input.getval(t))


class Amplify(SoundSignal):
    # - use native methods when possible to keep the type
    def __init__(self, input, factor=2):
        self.input = input
        self.factor = factor

    def getval(self, t):
        return self.input.getval(t) * self.factor.getval(t)


#    TODO
#   shift(delay) - return signal(t-delay)
#  echo(delay,factor) - return signal(t)+signal.shift(delay).amplify(factor)
