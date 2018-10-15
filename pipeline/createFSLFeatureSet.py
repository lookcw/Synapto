import csv
import numpy as np
import os
from FSL_features import extractFSLFeatures

#def createFSLFeatureSet(num_bunches, num_timePoints, extractFeatureFunc):
def createFSLFeatureSet(num_bunches, num_timePoints):

	featureSet = []

	basepath = 'BrazilRawData/HCF50'
	#combined_HC = np.empty((0,21*num_timePoints+1))
	for filename in os.listdir(basepath):
		if filename.endswith('.csv'):
			with open(os.path.join(basepath, filename)) as f:
				reader = csv.reader(f)
				data = np.array(list(reader))
				print(data.shape)
				
				#s = extractFSLFeatures(data)
				#print(s)
				#create bunches per patient
				#total = np.empty((num_bunches,len(data[0])*num_timePoints+1)) #1000x630
				for bunch in range(num_bunches):
					index = int(bunch*(len(data)/num_bunches))
					matrix = []
					matrix.append(data[index])
					for i in range(1,num_timePoints):
						matrix.append(data[index+i])
					matrix = np.array(matrix)
					print(matrix.shape)
					featuresRow = extractFSLFeatures(matrix)
					featuresRow = np.append(featuresRow,[0])
					print(featuresRow.shape)
					featureSet.append(featuresRow)

	basepath = 'BrazilRawData/ADF50'
	#combined_HC = np.empty((0,21*num_timePoints+1))
	for filename in os.listdir(basepath):
		if filename.endswith('.csv'):
			with open(os.path.join(basepath, filename)) as f:
				reader = csv.reader(f)
				data = np.array(list(reader))
				print(data.shape)

				#create bunches per patient
				#total = np.empty((num_bunches,len(data[0])*num_timePoints+1)) #1000x630
				for bunch in range(num_bunches):
					index = int(bunch*(len(data)/num_bunches))
					matrix = []
					matrix.append(data[index])
					for i in range(1,num_timePoints):
						matrix.append(data[index+i])
					matrix = np.array(matrix)
					print(matrix.shape)
					featuresRow = extractFSLFeatures(matrix)
					featuresRow = np.append(featuresRow,[1])
					print(featuresRow.shape)
					featureSet.append(featuresRow)

	return featureSet
	#output csv file instead

createFSLFeatureSet(1,100)