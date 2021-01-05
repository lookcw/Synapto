# Features from PyRQA and Nolds - Given a time-series (time-series is the specific band given for a specific electrode and patient)
# as an input, compute nine different features for each time-series. 

# from pyrqa.file_reader import FileReader
from mne import connectivity
import numpy as np
import csv
import sys
import pandas as pd
from headers import compareHeader


def getHeader(time_series,config_feature):
    return compareHeader(time_series)

#def features_func(filepath, o_filename):
def extractFeatures(time_series, config_feature):
	
	eegMat = pd.DataFrame(data=time_series)
	numElectrodes = len(eegMat.columns)
	# indices = (np.array([0, 0, 0]), np.array([2, 3, 4]))    # This is used if we are interested in comparing only a few electrodes
	# data: shape=(n_epochs, n_signals, n_times) | (data points per electrode still works right)
	time_series = time_series.transpose()
	print(time_series.shape)
	time_series = time_series[:,0:5000].reshape(500, 21, 10) #epochs, rows, cols
	# time_series = time_series.reshape(10, 21, 5000)
	# time_series = [time_series.transpose()]
	
	# Returns con: list of arrays - connectivity measures, freqs: array, times: array (number of time points for which connectivity computed)
	pli = connectivity.spectral_connectivity(time_series, method='pli', mode='multitaper')
	# prints out the whole square - we want the lower triangle
	# print(pli[0][:,:,0]) # Currently returning an array size of (21, 21, 26) which is 21 signals and 26 frequencies? (currently returning 21 2D arrays)
	
	ret_arr = pli[0][:,:,0][np.tril_indices(numElectrodes, -1)]
	# print(pli[0][:,:,0])
	# print(ret_arr)
	print(ret_arr.shape)
	return ret_arr

def config_to_filename(config_feature):
    return str(config_feature)[1:-1].replace(' ', '').replace('\'', '')
# if __name__ == '__main__':
# 	time_series_electrode = [1, 2, 3, 4]
# 	extractFeatures(time_series_electrode)