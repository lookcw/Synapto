from scipy.fftpack import fft, ifft, fftfreq, fftshift
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
# Takes in a time series in the form of raw electrode data (takes in a matrix)

def getHeader(time_series):
	numElectrodes = time_series.shape[1]
	headers = []
	for i in range(1,numElectrodes+1):
		headers.append('e'+str(i))
	return headers

def extractFeatures(time_series):

	numElectrodes = time_series.shape[1]
	features = [None] * (numElectrodes)
	featuresI = 0
	Fs = 250.0;  # sampling rate
	T = 1/Fs; # sampling interval

	for electrode in range(numElectrodes):	

		time_series_electrode = time_series[:,electrode]
		time_series_electrode = time_series_electrode.astype(np.float)

		y = time_series_electrode
		N = time_series_electrode.shape[-1] # number of timepoints in electrode

		yf = fft(y)
		yf = yf[0:(N/2)] # get useable half of the fft vector
		print(yf.shape)

		freq = np.arange(0,Fs/2,Fs/N)
		yf = yf[freq>=1] # get fft value when freq is greater than 1

		max_index = np.argmax(yf)

		print(freq.shape)
		print("the max index is", max_index)
		freqMax = freq[max_index] # this is the dominant frequency 

		features[featuresI] = freqMax
		featuresI += 1
		
	return features

data_path = 'BrazilRawData/ADF50'
filename = 'AD_50lp01.csv'
time_series = np.array(list(csv.reader(open(os.path.join(data_path, filename)))))
# time_series = np.random.randint(-2, 2, (10, 10))
extractFeatures(time_series)
