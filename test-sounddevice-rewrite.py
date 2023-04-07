#!python3

# python3 -m pip install sounddevice
# python3 -m pip install numpy

"""Play a sine signal."""
import sys

import numpy
import sounddevice


class Track:

    def __init__(self, f=440, a=.2):
        self.frequency = f
        self.amplitude = a

    def getval(self, t):
        print(f"getval({t})")
        return self.amplitude * numpy.sin(2 * numpy.pi * self.frequency * t)


class Player():
    def __init__(self):
        self.device = None

    def play(self, track):
        self.start_idx = 0
        try:
            samplerate = sounddevice.query_devices(self.device, 'output')[
                'default_samplerate']

            def callback(outdata, frames, time, status):
                if status:
                    print(status, file=sys.stderr)
                #start_t = time.outputBufferDacTime
                #tarray = start_t + numpy.arange(frames) / samplerate
                tarray = (self.start_idx + numpy.arange(frames)) / samplerate
                tarray = tarray.reshape(-1, 1)
                outdata[:] = track.getval(tarray)
                self.start_idx += frames

            with sounddevice.OutputStream(device=self.device, channels=1, callback=callback, samplerate=samplerate):
                print('press Return to quit')
                input()

        except KeyboardInterrupt:
            quit

        except Exception as e:
            quit(type(e).__name__ + ': ' + str(e))


p = Player()
mytrack = Track(440, .2)
p.play(mytrack)
