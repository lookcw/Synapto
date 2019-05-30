import csv
import numpy as np
import os
import sys
from BandPass1 import getBands

global_patient_num = 0

def writeFeatureSet(function,adhc, start_num, features_path, needHeader, compareElectrodes, num_epochs,num_timePoints,path,isBands=False):
	bands =['d','t','a','b','g']
	global global_patient_num
	out_file = open(features_path,"a") #used to be "a" for append (where to write results to)
	writer = csv.writer(out_file)
	patient_num = start_num
	for filename in os.listdir(path):
		print "patient num: " + str(patient_num)
		if filename.endswith('.csv'):
			with open(os.path.join(path, filename)) as f:
				reader = csv.reader(f)
				data = np.array(list(reader))
				
				# if comparing electrodes: do this header
				if needHeader and compareElectrodes:
					num_electrodes = data.shape[1] # number of columns = number of electrodes
					header = ['patient num']
					if (isBands):
						for band in bands:
							for i in range(num_electrodes):
								for j in range(i+1,num_electrodes):
									header.append(band+"_"+"e"+str(i+1) +"_e"+str(j+1))
					else :
						for i in range(num_electrodes):
							for j in range(i+1,num_electrodes):
								header.append("e"+str(i+1) +"_e"+str(j+1))
					header.append('class')
					writer.writerow(header)
					needHeader = False
				# If getting a value per electrode: do this header 
				elif needHeader: 
					num_electrodes = data.shape[1] # number of columns = number of electrodes
					header = ['patient num']
					if (isBands):
						for band in bands:
							for i in range(num_electrodes):
								header.append(band+"_"+"e"+str(i+1))
					else :
						for i in range(num_electrodes):
							header.append("e"+str(i+1))
					header.append('class')
					writer.writerow(header)
					needHeader = False


				#create bunches per patient
				for bunch in range(num_epochs):
					index = int(bunch*(len(data)/num_epochs))
					matrix = []
					matrix.append(data[index])
					print matrix
					for i in range(1,num_timePoints):
						matrix.append(data[index+i])
					matrix = np.array(matrix,dtype=np.float) 
					featuresRow = []
					if(isBands):
						transposed = np.transpose(matrix)
						delta = np.empty(transposed.shape)
						theta = np.empty(transposed.shape)
						alpha = np.empty(transposed.shape)
						beta = np.empty(transposed.shape)
						gamma = np.empty(transposed.shape)
						for i in range(len(transposed)):
							bands = getBands(transposed[i])
							delta[i] = bands[0]
							theta[i] = bands[1]
							alpha[i] = bands[2]	
							beta[i] = bands[3]
							gamma[i] = bands[4]
						allBands = [delta,theta,alpha,beta,gamma]
						for i in range(len(allBands)):
							featuresRow.append(function(np.transpose(allBands[i]).astype('str')))	
						
					else:
						featuresRow = function(matrix)
					featuresRow = np.array(featuresRow)
					featuresRow = np.append(featuresRow,[adhc])
					featuresRow = np.insert(featuresRow,0,patient_num)
					writer.writerow(featuresRow)
				patient_num += 1
				global_patient_num = patient_num

#def createFSLFeatureSet(num_epochs, num_timePoints, extractFeatureFunc):
def createMatrixFeatureSet(function,feature_name,num_epochs, num_timePoints, path1, path2, data_type, recurr,):
	# print ("num epochs: ", num_epochs)
	identifier = str(num_epochs) + 'epochs_' + str(num_timePoints) + 'timepoints'
	features_path = sys.path[0] + '/FeatureSets/' + data_type + feature_name + identifier+'.csv'
	# print("feature set: " + features_path)

	if not os.path.exists(features_path):
		# if comparing electrodes
		if (feature_name == 'FSL' or feature_name == 'Pearson' or feature_name == 'Granger'):
			writeFeatureSet(function,0,1,features_path, True, True, num_epochs,num_timePoints,path1)
			writeFeatureSet(function,1,global_patient_num,features_path, False, False, num_epochs,num_timePoints,path2)
		else: # If getting a value per electrode
			writeFeatureSet(function,0,1,features_path, True, False, num_epochs,num_timePoints,path1)
			writeFeatureSet(function,1,global_patient_num,features_path, False, False, num_epochs,num_timePoints,path2)

#createFSLFeatureSet(1,215)
#minimum is about 215 raw points for extractFSLFeatures function