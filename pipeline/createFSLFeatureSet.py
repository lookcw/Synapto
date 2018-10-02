import csv
import numpy as np
import os
from FSL_features import extractFSLFeatures

#def createFSLFeatureSet(num_bunches, num_timePoints, extractFeatureFunc):
def createFSLFeatureSet(num_bunches, num_timePoints):
	basepath = 'BrazilRawData/HCF50'
	combined_HC = np.empty((0,21*num_timePoints+1))
	for filename in os.listdir(basepath):
		if filename.endswith('.csv'):
			with open(os.path.join(basepath, filename)) as f:
				reader = csv.reader(f)
				data = np.array(list(reader))
				print(data.shape)

				##
				print os.path.join(basepath, filename)
 				extractFSLFeatures(data)

				#create bunches per patient
				total = np.empty((num_bunches,len(data[0])*num_timePoints+1)) #1000x630
				for bunch in range(num_bunches):
					index = int(bunch*(len(data)/num_bunches))
					matrix = []
					matrix.append(data[index])
					for i in range(1,num_timePoints):
						matrix.append(data[index+i])
					matrix = np.array(matrix)
					print(matrix.shape)
					featuresRow = extractFSLFeatures(matrix)
					print(features.shape)
					featuresRow = np.append(featuresRow,[0])


createFSLFeatureSet(1,30)