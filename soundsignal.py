from signal_modifiers import Amplifier
from signal_timedFloat import toTimedFloat

class SoundSignal:
    # anything that gives a val for a time - both oscillator and track are signals
    # Audio signal is expected -1 to 1
    # Control signal is V/Oct like (-1 = lower freq by 1 octave)
    # Trigger, Gate or Clock are pulses - unused yet

    def getval(self,t):
        pass

    def amplify(self,f):
        if self.ampl is not None:
            self.ampl = Amplifier(self.ampl,f)