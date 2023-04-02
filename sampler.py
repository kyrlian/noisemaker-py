


import math
import time
import sys
import pyaudio # pip install pyaudio

# https://stackoverflow.com/questions/974071/python-library-for-playing-fixed-frequency-sound
# https://pypi.org/project/PyAudio/
# https://realpython.com/playing-and-recording-sound-python/#comparison-of-audio-libraries

class TrackStreamer:
    #Beep Streamer struct
    def __init__(self,soundsignal):
        self.vamlax = 1.0
        samplerate = 44100
        channels=2
        self.bufferseconds = 1
        self.soundsignal  = soundsignal
        self.sampleposition = 0
        amplitude = .1 
        frequency = 440

        def callback(data, frame_count, time_info, status):
            # If len(data) is less than requested frame_count, PyAudio automatically
            # assumes the stream is finished, and the stream stops.
            if status:
                print(status, file=sys.stderr)
            global start_idx
            t = (start_idx + np.arange(frame_count)) / samplerate
            t = t.reshape(-1, 1)
            data[:] = amplitude * math.sin(2 * math.pi * frequency * t)
            start_idx += frame_count
            return (data, pyaudio.paContinue)

        # Instantiate PyAudio and initialize PortAudio system resources (2)
        p = pyaudio.PyAudio()

        # Open stream using callback (3)
        stream = p.open(format=p.get_format_from_width(1),
                        channels=self.channels,
                        rate=self.samplerate,
                        output=True,
                        stream_callback=callback)

        # Wait for stream to finish (4)
        while stream.is_active():
            time.sleep(0.1)

        # Close the stream (5)
        stream.close()

        # Release PortAudio system resources (6)
        p.terminate()