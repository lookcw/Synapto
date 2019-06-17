from scipy.fftpack import fft, ifft, fftfreq, fftshift
import csv
import os
import matplotlib.pyplot as plt
import numpy as np

# What would the input to the function be?
# Requires that it finds the correct file corresponding to the feature, instance num, epoch num, and timepoint num

datafile = 'FeatureSets/DomFreq_Brazil1instances_4_epochs160_timepoints.csv'
data = np.array(list(csv.reader(open(datafile))))
# Get the data from the file 
data = data[1:, 2:-1]

# (2D array part: Number of rows (patients), columns), and epochs per patient 
# NOTE: this has to be done manually - requires that you know how many epochs there are per patient (will be instances * number of epochs)
data3D = data.reshape(25, 21, 4)

# For each 2D array (which has all the epochs), get the variance 
for i in range(len(data3D)):
	for j in range(len(data3D[i])):
		print np.var(data3D[i][j].astype(np.float))
	print "\n"

#Hm I feel like we shouldn't write to file here but 


# b = np.reshape(a, (5, 21, 25)) 
# print(b.shape)
