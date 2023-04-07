import numpy

class SoundSignal:
    # anything that gives a val at a time - both oscillator and track are signals
    # Audio signal is expected -1 to 1
    # Control signal is V/Oct like (-1 = lower freq by 1 octave)
    # Trigger, Gate or Clock are pulses - unused yet

    def getval(self,t:numpy.ndarray):
        pass
