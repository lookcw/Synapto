from scipy.fftpack import fft, ifft, fftfreq, fftshift
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
# Takes in a time series in the form of raw electrode data (takes in a matrix)

def extractDomFreqFeatures(time_series):

	numElectrodes = time_series.shape[1]
	features = [None] * (numElectrodes)
	featuresI = 0

	for electrode in range(time_series.shape[1]):

		Fs = 250.0;  # sampling rate
		T = 1/Fs; # sampling interval

		time_series_electrode = time_series[:,electrode]
		time_series_electrode = time_series_electrode.astype(np.float)

		y = time_series_electrode
		N = time_series_electrode.shape[-1] # number of timepoints in electrode

		yf = fft(y)
		yf = yf[0:(N/2)+1] # get useable half of the fft vector
		print(yf.shape)

		freq = np.arange(0,Fs/2,Fs/N)
		freq = freq[freq>=1]

		max_index = np.argmax(yf)

		print(freq.shape)
		print("the max index is", max_index)
		freqMax = freq[max_index]

		features[featuresI] = freqMax
		featuresI += 1
		
	return features
