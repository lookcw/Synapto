import csv
import numpy as np
import os
import sys
from FSL_features import extractFSLFeatures

#def createFSLFeatureSet(num_bunches, num_timePoints, extractFeatureFunc):
def createFSLFeatureSet(num_bunches, num_timePoints):

	identifier = str(num_bunches*25) + '_' + str(num_timePoints)

	features_path = sys.path[0] + '/FeatureSets/'+'FSLfeatures'+identifier+'.csv'

	if not os.path.exists(features_path):
		open(features_path,"w")

		out_file = open(features_path,"a") #used to be "a" for append
		writer = csv.writer(out_file)

		basepath = 'BrazilRawData/HCF50'
		for filename in os.listdir(basepath):
			if filename.endswith('.csv'):
				with open(os.path.join(basepath, filename)) as f:
					reader = csv.reader(f)
					data = np.array(list(reader))
					print(data.shape)

					print os.path.join(basepath, filename)

					#create bunches per patient
					for bunch in range(num_bunches):
						index = int(bunch*(len(data)/num_bunches))
						matrix = []
						matrix.append(data[index])
						for i in range(1,num_timePoints):
							matrix.append(data[index+i])
						matrix = np.array(matrix)
						print(matrix.shape)
						featuresRow = extractFSLFeatures(matrix)
						# print(featuresRow.shape)
						featuresRow = np.append(featuresRow,[0])
						writer.writerow(featuresRow)

		basepath = 'BrazilRawData/ADF50'
		for filename in os.listdir(basepath):
			if filename.endswith('.csv'):
				with open(os.path.join(basepath, filename)) as f:
					reader = csv.reader(f)
					data = np.array(list(reader))
					print(data.shape)

					print os.path.join(basepath, filename)

					#create bunches per patient
					for bunch in range(num_bunches):
						index = int(bunch*(len(data)/num_bunches))
						matrix = []
						matrix.append(data[index])
						for i in range(1,num_timePoints):
							matrix.append(data[index+i])
						matrix = np.array(matrix)
						print(matrix.shape)
						featuresRow = extractFSLFeatures(matrix)
						# print(featuresRow.shape)
						featuresRow = np.append(featuresRow,[1])
						writer.writerow(featuresRow)


#createFSLFeatureSet(1,215)
#minimum is about 215 raw points for extractFSLFeatures function