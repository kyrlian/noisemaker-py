#!python3

from player import Player
from signal_track import Track, TrackElement
from signal_oscillator import Oscillator
from const import Const
from signal_timedFloat import TimedFloat

print("MAKE SOME NOISE")
print("Preparing track")

o440 = Oscillator(Const.SIN, 440.0)
mytrack = Track([TrackElement(o440)], 0, 10, .1)
p = Player()
p.play(mytrack)
