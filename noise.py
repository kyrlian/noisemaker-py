#!python3

from player import Player
from signal_track import Track, TrackElement
from signal_oscillator import Oscillator
from const import Const
import examples

print("MAKE SOME NOISE")
print("Preparing track")

#tr = examples.example_sin440()
#tr = examples.example_pulse440()
#tr = examples.example_majeurmineur()
#tr = examples.example_enveloppe()
#tr = examples.example_harmonicsTuning(440, 5) #TODO review plots
#tr = examples.example_drums()
#tr = examples.example_combined1()
#tr = examples.example_engine()
tr = examples.example_gotobass()

p = Player()
p.play(tr)
