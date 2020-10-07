from scipy.fftpack import fft, ifft, fftfreq, fftshift
import csv
import os
import matplotlib.pyplot as plt
from headers import linearHeader
import numpy as np
import sys
# Takes in a time series in the form of raw electrode data (takes in a matrix)


def getHeader(time_series,config_feature):
    return linearHeader(time_series)


def extractFeatures(time_series, config_feature):

    numElectrodes = time_series.shape[1]
    features = [None] * (numElectrodes)
    featuresI = 0

    for electrode in range(time_series.shape[1]):

        Fs = 256  # sampling rate
        T = 1/Fs  # sampling interval

        time_series_electrode = time_series[:, electrode]
        time_series_electrode = time_series_electrode.astype(np.float)

        y = time_series_electrode
        # number of timepoints in electrode
        N = time_series_electrode.shape[-1]

        yf = fft(y)
        yf = yf[0:int((N+1)/2)]  # get useable half of the fft vector
        freq = np.arange(0, Fs/2, Fs/N)
        yf_between = yf[(freq >= 3) & (freq <= 14)]

        #max_index = np.argmax(yf_above1)

        max_yf = max(yf_between)
        max_index = np.where(yf == max_yf)[0][0]
        freqMax = freq[max_index]  # this is the dominant frequency

        features[featuresI] = freqMax
        featuresI += 1

    return features


def config_to_filename(config_feature):
    return str(config_feature)[1:-1].replace(' ', '').replace('\'', '')
