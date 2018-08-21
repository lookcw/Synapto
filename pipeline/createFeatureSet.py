import csv
import numpy as np
import os
import sys
import pandas as pd

def createFeatureSet(num_bunches, num_timePoints, featureName, extractFeatures):

	basepath = 'BrazilRawData/HCF50'
	combined_HC = np.empty((0,21*num_timePoints+1))
	for filename in os.listdir(basepath):
		if filename.endswith('.csv'):
			with open(os.path.join(basepath, filename)) as f:
				reader = csv.reader(f)
				array = list(reader)
				array = np.array(array)
				print(array.shape)
				#print len(array) #160,000
				#print len(array[0]) #21
				data = array

				#create bunches per patient
				total = np.empty((num_bunches,len(array[0])*num_timePoints+1)) #1000x630
				for bunch in range(num_bunches):
					index = int(bunch*(len(array)/num_bunches))
					row = data[index]
					for i in range(1,num_timePoints):
						row = np.append(row, data[index+i])
					#print row
					row = np.append(row,[0])
					total[bunch] = row
				#print total
				combined_HC = np.concatenate((combined_HC,total)) #12000x630

	basepath = 'BrazilRawData/ADF50'
	combined_AD = np.empty((0,21*num_timePoints+1))
	for filename in os.listdir(basepath):
		if filename.endswith('.csv'):
			with open(os.path.join(basepath, filename)) as f:
				reader = csv.reader(f)
				array = list(reader)
				array = np.array(array)
				print(array.shape)
				#print len(array) #160,000
				#print len(array[0]) #21
				data = array

				#create bunches per patient
				total = np.empty((num_bunches,len(array[0])*num_timePoints+1)) #1000x210
				for bunch in range(num_bunches):
					index = int(bunch*(len(array)/num_bunches))
					#print index
					row = data[index]
					for i in range(1,num_timePoints):
						row = np.append(row, data[index+i])
					#print row
					row = np.append(row,[1])
					total[bunch] = row
				#print total
				combined_AD = np.concatenate((combined_AD,total))

	combined = np.concatenate((combined_HC, combined_AD))
	#print(combined.shape) #25000x631

	#store and delete last column
	targets = combined[:,-1]

	combined = np.delete(combined,-1,axis=1)
	#reshape into 25000 x timepoints x 21
	combined = np.reshape(combined,(len(combined), num_timePoints, 21))

	from BandPass1 import splitbands

	identifier = str(num_bunches*25) + '_' + str(num_timePoints)

	features_path = sys.path[0] + '/FeatureSets/'+featureName+'features'+identifier+'.csv'

	if not os.path.exists(features_path):
		open(features_path,"w")

	#count number of lines already present in file - start at this number + 1 for iterations
	read_file = open(features_path,"r")
	reader = csv.reader(read_file)
	row_count = sum(1 for row in reader)
	print(row_count)

	out_file = open(features_path,"a") #used to be "a" for append
	writer = csv.writer(out_file)

	print("Feature Extraction...")

	#initialize header list
	headers = []
	
	#create header list
	for i in range(row_count,len(combined)):
		#transpose each n x 21 so each row is time series points (columns) of 1 electrode (row)
		transposed = np.transpose(combined[i]) 
		#add another dimension in each row to make it 5 bands x n
		for j in range(len(transposed)):
			if (i==0):
				bands = splitbands(transposed[j])
			#squish each band of raw points into n feature values
			for k in range(len(bands)): #bands[j] = band of raw data
				if (j==0):
					bandfeatures = extractFeatures(bands[k])
				#adding headers
				if (i == 0):
					featureHeaders = []
					for h in range(len(bandfeatures)):
						featureHeaders.append(("electrode"+str(j+1)+"band"+str(k+1)+"feature"+str(h+1)))
					headers.extend(featureHeaders)

	headers.append('class')
	writer.writerow(headers)
