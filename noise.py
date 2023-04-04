def main():
    print("MAKE SOME NOISE")

    print("Preparing track")
    signal = example_harmonicsTuning(22.5, 10)

    nbsecs = 20
    plotsignal(signal, signal.name, nbsecs, 44100/10) #plot track for 30 seconds
    saveToWav(signal, signal.name, nbsecs)            #save to wave file
    runSampler(signal, nbsecs)                        #play on speakers
