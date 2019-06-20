from scipy.fftpack import fft, ifft, fftfreq, fftshift
import csv
import os
import matplotlib.pyplot as plt
import numpy as np

# What would the input to the function be?
# Requires that it finds the correct file corresponding to the feature, instance num, epoch num, and timepoint num

# datafile = 'FeatureSets/DomFreq_Brazil1instances_4_epochs160_timepoints.csv'

def getHeader(time_series):
	numElectrodes = time_series.shape[1]
	headers = []
	for i in range(1,numElectrodes+1):
		headers.append('e'+str(i))

	return headers

def extractFeatures(feature_path, num_instances, epochs_per_instance):
	print "function called"
	feature_path = '/Users/megha/Synapto/pipeline/FeatureSets/DomFreq_Brazil1instances_4_epochs160_timepoints.csv'
	# with open(os.path.join(path, filename)) as f:
	# 	reader = csv.reader(f)
	# 	data = np.array(list(reader))
	data = np.array(list(csv.reader(open(feature_path))))
	# Get the data from the file 
	data = data[1:, 2:-1]

	# (2D array part: Number of rows (patients), columns), and epochs per patient 
	# NOTE: this has to be done manually - requires that you know how many epochs there are per patient (will be instances * number of epochs)
	epochs_per_patient = num_instances * epochs_per_instance
	data3D = data.reshape(25, 21, epochs_per_patient)

	features = np.zeros(shape=(25,21))
	# For each 2D array (which has all the epochs), get the variance 
	for i in range(len(data3D)):
		for j in range(len(data3D[i])):
			# print np.var(data3D[i][j].astype(np.float))
			features[i][j] = np.var(data3D[i][j].astype(np.float))
		# print "\n"

	return features