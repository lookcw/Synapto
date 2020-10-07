# Features from PyRQA and Nolds - Given a time-series (time-series is the specific band given for a specific electrode and patient)
# as an input, compute nine different features for each time-series. 

# from pyrqa.file_reader import FileReader
from mne import connectivity
import numpy as np
import csv
import sys

#def features_func(filepath, o_filename):
def extractFeatures(time_series_electrode):
	
	# indices = (np.array([0, 0, 0]), np.array([2, 3, 4]))    # col indices
	# # data: shape=(n_epochs, n_signals, n_times) | (data points per electrdoe still works right)
	# con_flat = connectivity.spectral_connectivity(time_series_electrode, method='pli', indices=None)
	print("hi")

# if __name__ == '__main__':
# 	time_series_electrode = [1, 2, 3, 4]
# 	extractFeatures(time_series_electrode)