import csv
import numpy as np
import os
<<<<<<< HEAD
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
=======
import sys
from FSL_features import extractFSLFeatures

#def createFSLFeatureSet(num_epochs, num_timePoints, extractFeatureFunc):
def createFSLFeatureSet(num_epochs, num_timePoints, path1, path2):

	identifier = str(num_epochs) + 'epochs_' + str(num_timePoints) + 'timepoints'

	features_path = sys.path[0] + '/FeatureSets/'+'FSLfeatures'+identifier+'.csv'

	if not os.path.exists(features_path):
		open(features_path,"w")

		out_file = open(features_path,"a") #used to be "a" for append
		writer = csv.writer(out_file)

		for filename in os.listdir(path1):
			if filename.endswith('.csv'):
				with open(os.path.join(path1, filename)) as f:
					reader = csv.reader(f)
					data = np.array(list(reader))
					print(data.shape)

					print os.path.join(path1, filename)

					#create bunches per patient
					for bunch in range(num_epochs):
						index = int(bunch*(len(data)/num_epochs))
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

		for filename in os.listdir(path2):
			if filename.endswith('.csv'):
				with open(os.path.join(path2, filename)) as f:
					reader = csv.reader(f)
					data = np.array(list(reader))
					print(data.shape)

					print os.path.join(path2, filename)

					#create bunches per patient
					for bunch in range(num_epochs):
						index = int(bunch*(len(data)/num_epochs))
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
>>>>>>> fsl-pipeline
