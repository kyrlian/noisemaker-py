import math
from  matplotlib import pyplot
import numpy

def plotsignal(signal, filename, nbseconds, samplerate):
    axis = numpy.arange(0.0, nbseconds, samplerate/10)
    pyplot.plot(axis, signal.getval(axis))
    pyplot.show()