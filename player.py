#!python3

# https://python-sounddevice.readthedocs.io/en/latest/

# python3 -m pip install sounddevice
# python3 -m pip install numpy

import sys
from bs4 import CData
import numpy
import sounddevice
from soundsignal import SoundSignal

class Player():
    def __init__(self):
        self.device = None

    def play(self, track:SoundSignal):
        self.start_idx = 0
        try:
            samplerate = sounddevice.query_devices(self.device, 'output')[
                'default_samplerate']

            def callback(outdata: numpy.ndarray, frames: int, time: CData, status: sounddevice.CallbackFlags):
                if status:
                    print(status, file=sys.stderr)
                # start_t = time.outputBufferDacTime
                # tarray:numpy.ndarray = start_t + numpy.arange(frames) / samplerate
                tarray:numpy.ndarray = (self.start_idx + numpy.arange(frames)) / samplerate
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
