#!python3

# https://stackoverflow.com/questions/974071/python-library-for-playing-fixed-frequency-sound
# https://pypi.org/project/PyAudio/
# https://realpython.com/playing-and-recording-sound-python/#comparison-of-audio-libraries

# python3 -m pip install sounddevice
# python3 -m pip install numpy

import sys
import numpy
import sounddevice

class Player():
    def __init__(self):
        self.device = None

    def play(self, track):
        try:
            samplerate = sounddevice.query_devices(self.device, 'output')[
                'default_samplerate']

            def callback(outdata, frames, time, status):
                if status:
                    print(status, file=sys.stderr)
                start_t = time.outputBufferDacTime
                tarray = start_t + numpy.arange(frames) / samplerate
                tarray = tarray.reshape(-1, 1)
                outdata[:] = track.getval(tarray)

            with sounddevice.OutputStream(device=self.device, channels=1, callback=callback, samplerate=samplerate):
                print('press Return to quit')
                input()

        except KeyboardInterrupt:
            quit

        except Exception as e:
            quit(type(e).__name__ + ': ' + str(e))
