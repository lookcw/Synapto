import numpy as np
import scipy as sp
import csv
import os
import matplotlib.pyplot as plt 
import utils
import pandas as pd
import peakutils
from scipy.signal import find_peaks


def getHeader(time_series):
    numElectrodes = time_series.shape[1]
    headers = []
    for i in range(1,numElectrodes+1):
        headers.append('e'+str(i))
    return headers

def extractSharpnessFeatures(time_series):
    
    # electrode = [1.113, 2.212, 1.231, 1.028, -3.289, -4.289, 0.123, 8.233, 9, 10, -2, 1, -3, 5, 6, 7, -10]
    # zero_crossings = np.where(np.diff(np.sign(electrode)))[0]

    numElectrodes = time_series.shape[1]
    features = [None] * (numElectrodes)
    featuresI = 0

    for col in range(time_series.shape[1]):   

        peak_first = 0
        trough_first = 0

        electrode = time_series[:,col]
        electrode = electrode.astype(np.float)

        peaks = peakutils.peak.indexes(np.array(electrode)) #get peaks
        troughs = peakutils.peak.indexes(np.array([-1*x for x in electrode])) #get troughs
        extremes = [x for x in peaks] + [x for x in troughs]
        extremes.sort() #combine peaks and troughs then sort. peaks and troughs will alternate (can't have two peaks in a row)

        if(extremes[0] == peaks[0]):
            peak_first = 1
        else:
            trough_first = 1

        peaks = []
        troughs = []

        for i in range(0, len(extremes)):
            if(peak_first):
                if(i%2 == 0):
                    peaks.append(np.abs(electrode[extremes[i]]))
                else:
                    troughs.append(np.abs(electrode[extremes[i]]))
            else:
                if(i%2 == 0):
                    troughs.append(np.abs(electrode[extremes[i]]))
                else:
                    peaks.append(np.abs(electrode[extremes[i]]))

        peak_mean = np.mean(peaks)
        peak_trough = np.mean(troughs)

        print peak_mean
        print peak_trough
        sharpness_ratio = max(np.log(peak_mean/peak_trough), np.log(peak_trough/peak_mean))

        features[featuresI] = sharpness_ratio
        featuresI += 1

    return features


# data_path = 'SampleDataTesting'
# filename = 'AD_50lp01_short.csv'
# time_series = np.array(list(csv.reader(open(os.path.join(data_path, filename)))))
# # time_series = np.random.randint(-2, 2, (10, 10))
# extractSharpnessFeatures(time_series)