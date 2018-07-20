from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

def butter_bandpass(lowcut, highcut, fs, order=6):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=6):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Delta
def runD():

    fs = 250.0
    lowcut = 0.5 
    highcut = 3.0

    return butter_bandpass_filter(x, lowcut, highcut, fs, order=6)
 
 # Theta
 def runT():

    fs = 250.0
    lowcut = 3.0
    highcut = 8.0

    return butter_bandpass_filter(x, lowcut, highcut, fs, order=6)

# Alpha
def runA():

    fs = 250.0
    lowcut = 8.0 
    highcut = 12.0

    return butter_bandpass_filter(x, lowcut, highcut, fs, order=6)

# Beta
def runB():

    fs = 250.0
    lowcut = 12.0 
    highcut = 38.0

    return butter_bandpass_filter(x, lowcut, highcut, fs, order=6)

# Gamma
def runG():

    fs = 250.0
    lowcut = 38.0 
    highcut = 45.0

    return butter_bandpass_filter(x, lowcut, highcut, fs, order=6)

Delta = runD()
Theta = runT()
Alpha = runA()
Beta = runB()
Gamma = runG()