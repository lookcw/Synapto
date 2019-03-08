import csv
import numpy as np
import os
import sys
from FSL_features import extractFSLFeatures

#def createFSLFeatureSet(num_epochs, num_timePoints, extractFeatureFunc):
def createFSLFeatureSet(num_epochs, num_timePoints, path1, path2, data_type, recurr):

	identifier = str(num_epochs) + 'epochs_' + str(num_timePoints) + 'timepoints'

	features_path = sys.path[0] + '/FeatureSets/'+data_type+'FSLfeatures'+identifier+'.csv'
	needHeader = True


	if not os.path.exists(features_path):
		open(features_path,"w") 

		out_file = open(features_path,"a") #used to be "a" for append
		writer = csv.writer(out_file)
		patient_num = 1
		for filename in os.listdir(path1):
			print patient_num
			if filename.endswith('.csv'):
				with open(os.path.join(path1, filename)) as f:
					reader = csv.reader(f)
					data = np.array(list(reader))
					if needHeader:
						num_electrodes = data.shape[1]
						print num_electrodes
						header = ['patient num']
						for i in range(num_electrodes):
							for j in range(i+1,num_electrodes):
								header.append("e"+str(i+1) +"_e"+str(j+1))
						header.append('class')
						writer.writerow(header)
						needHeader = False


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
						featuresRow = np.insert(featuresRow,0,patient_num)
						writer.writerow(featuresRow)
					patient_num += 1

		for filename in os.listdir(path2):
			print patient_num
			if filename.endswith('.csv'):
				with open(os.path.join(path2, filename)) as f:
					reader = csv.reader(f)
					data = np.array(list(reader))

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
						featuresRow = np.insert(featuresRow,0,patient_num)
						writer.writerow(featuresRow)
					patient_num += 1


#createFSLFeatureSet(1,215)
#minimum is about 215 raw points for extractFSLFeatures function