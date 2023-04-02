import math

def getMinMax(signal, nbseconds, samplerate):
    ymin = signal.getval(.0)
    ymax = ymin
    step = 1 / float(samplerate)
    xmax = float(nbseconds)
    for x in range(xmax):
        y = signal.getval(x)
        ymin = math.Min(ymin, y)
        ymax = math.Max(ymax, y)
    return ymin, ymax

def plotsignal(signal, filename, nbseconds, samplerate):
    print(f"Ploting signal to out/{filename}.png")
    #nbseconds := 30
    nbsamples = samplerate * nbseconds / 10
    signalfunc = plotter.NewFunction(funcx:
        return signal.getval(x))
    signalfunc.Color = color.RGBA(B= 255, A= 255)
    signalfunc.Samples = nbsamples
    p = plot.New()
    p.Add(signalfunc)
    p.Legend.Add("signal", signalfunc)
    p.X.Min = .0
    p.X.Max = float(nbseconds)
    #p.Y.Min = -2.0
    #p.Y.Max = 2.0
    p.Y.Min, p.Y.Max = getMinMax(signal, nbseconds, samplerate)
    err = p.Save(2048, 1024, "out/"+filename+".png")