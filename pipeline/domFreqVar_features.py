from scipy.fftpack import fft, ifft, fftfreq, fftshift
import csv
import os
import matplotlib.pyplot as plt
import numpy as np

def getHeader(num_electrodes):
	headers = ['patient num']
	for i in range(1,num_electrodes+1):
		headers.append('e'+str(i))

	return headers


def extractFeatures(featureRead_path, out_path, num_instances, epochs_per_instance, num_electrodes):
	print("function called")
	
	out_file = open(out_path,"a") #used to be "a" for append
	writer = csv.writer(out_file)	

	header = []
	header += getHeader(num_electrodes)
	header.append('class')
	writer.writerow(header)

	data = np.array(list(csv.reader(open(featureRead_path))))
	data = data[1:, 2:-1] # Get the data from the file (the dom freq feature matrix set)

	# (2D array part: Number of rows (patients), columns), and epochs per patient 
	# NOTE: this has to be done manually - requires that you know how many epochs there are per patient (will be instances * number of epochs)
	epochs_per_patient = num_instances * epochs_per_instance
	data3D = data.reshape(25, num_electrodes, epochs_per_patient)

	adhc = 0
	# For each 2D array (which has all the epochs), get the variance 
	# where i is a patient and j is an electrode
	for i in range(len(data3D)):
		featuresRow = [i+1]
		if(i >= 12):
			adhc = 1
		for j in range(len(data3D[i])):
			# print(np.var(data3D[i][j].astype(np.float)))	
			featuresRow = np.append(featuresRow, np.var(data3D[i][j].astype(np.float)))
		featuresRow = np.append(featuresRow,adhc)
		writer.writerow(featuresRow)
		# print("\n")
