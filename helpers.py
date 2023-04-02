package main

import
#    "fmt"
"fmt"
"math"

def root(x, n):
    lower = .0
    upper = x
    r = .0
    for upper-lower >= 0.000000001:
        r = (upper + lower) / 2.0
        temp = math.Pow(r, float(n))
        if temp > x:
            upper = r
        else:
            lower = r
    return r

semiToneConst = root(2.0, 12) #1,05946309435929
toneConst = root(2.0, 7)      #1,104089513673812
_ = toneConst + semiToneConst

    #Avoid not used error

def getSemiToneFreq(fstart, nsemitones):
    nfreq = fstart * math.Pow(semiToneConst, float(nsemitones))
    #print("    getFreq(%v,%v)=%v\n" % fstart, nsemitones, nfreq)
    return nfreq

def accord3(baseFreq, gap1, gap2):
: #3,4
    return signalSum().
        appendSignal(oscillator_sf(SIN, baseFreq).amplify(tf(.7))).
        appendSignal(oscillator_sf(SIN, getSemiToneFreq(baseFreq, gap1)).amplify(tf(.6))).
        appendSignal(oscillator_sf(SIN, getSemiToneFreq(baseFreq, gap1+gap2)).amplify(tf(.5)))

def accordMineur(fstart):
    return accord3(fstart, 3, 4)
def accordMajeur(fstart):
    return accord3(fstart, 4, 3)

def harmonics(baseFreq, nharmonics):
    sum = signalSum_n("harmonics" + fmt.Sprint(nharmonics))
    for i = 1; i <= nharmonics; i += 1:
        f2pi = math.Pow(2, float(i))
        sum = sum.appendSignal(oscillator_sfpa(SIN, baseFreq*f2pi, .0, 1.0/f2pi))
    return sum
