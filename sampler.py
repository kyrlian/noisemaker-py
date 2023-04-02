
VALMAX = 1.0
SAMPLERATE = 44100 #Only Capitalized variable are visible outside the package - I used SAMPLERATE for readability
BUFFERSECONDS = 1

class TrackStreamer:
    #Beep Streamer struct
    def __init__(self,tracksignal,):
        self.trackpointer   = Signal()
        self.samplePosition = int()
        #nbsamples      int //max number of sample based on track's end time and SAMPLERATE
    
    def Stream(str, samples):
        #beep.Streamer interface requires Stream and Err
        tstart = time.Now()
        for i in samples :
            time = float(str.samplePosition) / float(SAMPLERATE)
            val = str.trackpointer.getval(time)
            if val > valmax:
                valmax = val #store and display the max value seen
                print("WARNING - sampler:valmax=%v\n" % val)
            samples[i][0] = val
            samples[i][1] = val
            str.samplePosition += 1
        if False: #activate to show computing stats
            elapsed = time.Since(tstart)
            microseconds = 1000.0 * 1000.0 * len(samples) / SAMPLERATE
            duration = time.Duration(microseconds) * time.Microsecond
            print("    sampler.Stream:Computed %v samples for %v in %v\n" % len(samples), duration, elapsed)
        return len(samples), True

    def Err(str):
        return nil



def trackStreamer(signal):
    #Infinite streamer
    return TrackStreamer(signal, 0)

def timedStreamer(signal, nbseconds):
    #Finite streamer based on track duration
    trackstr = trackStreamer(signal)
    return beep.Take(SAMPLERATE*nbseconds, trackstr)

def saveToWav(signal, filename, nbseconds):
    print("Saving to %v\n" % filename+".wav")
    file, fileerr = os.CreateTemp("out", filename+"_*.wav")
    #trackstr := trackStreamer(signal)
    #timedStreamer := beep.Take(trackstr.nbsamples, &trackstr)
    timedStreamer = timedStreamer(signal, nbseconds)
    format = beep.Format(SampleRate= beep.SampleRate(SAMPLERATE), NumChannels= 2, Precision= 2)
    writeerr = wav.Encode(file, timedStreamer, format)

#Run
def runSampler(signal, nbseconds):
    print("Preparing speaker\n")
    sampleRate = beep.SampleRate(SAMPLERATE)
    buffSize = bufferseconds * sampleRate.N(time.Second)
    print("    sampler.initSpeaker:buffSize=%v\n" % buffSize)
    speaker.Init(sampleRate, buffSize)
    print("Preparing streamer\n")
    #var trackstr = trackStreamer(signal)
    timedStreamer = timedStreamer(signal, nbseconds)
    print("Playing speaker\n")
    speaker.Play(timedStreamer)
    select {}
