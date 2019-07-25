import csv
import numpy as np
import os
import sys
from BandPass1 import getBands
from identifier import paramToFilename
from numpy import genfromtxt

global_patient_num = 0
global_instance_num = 0

#TODO
# def writeFeatureSet(function,adhc, start_num, features_path, needHeader, compareElectrodes, num_epochs,num_timePoints,path,isBands=False):
def writeFeatureSet(functionClass, adhc, start_num, features_path, num_instances, epochs_per_patient,num_timePoints, path, isBands=False):
	# isBands = 1
	bands =['d','t','a','b','g']
	global global_patient_num
	global global_instance_num
	out_file = open(features_path,"a") #used to be "a" for append
	writer = csv.writer(out_file)
	patient_num = start_num
	for filename in os.listdir(path):
		print "patient num: " + str(patient_num)
		if filename.endswith('.csv'):
			with open(os.path.join(path, filename)) as f:
				reader = csv.reader(f)
				data = np.array(list(reader))
				
################################################ HEADERS #################################################		
				if global_patient_num == 0:
					num_electrodes = data.shape[1] # number of columns = number of electrodes
					header = ['instance code', 'patient num', 'instance num']

					if (isBands):
						for band in bands:
							header += map(lambda x: band + '_' + x, functionClass.getHeader(data)) #appending band number onto header names
					else :
						header += functionClass.getHeader(data)

					header.append('class')
					writer.writerow(header)
#################################################################################################
				
				#create bunches per patient
				for bunch in range(num_instances*epochs_per_patient):
					index = int(bunch*(len(data)/(num_instances*epochs_per_patient)))
					matrix = []
					matrix.append(data[index])
					for i in range(1,num_timePoints):
						matrix.append(data[index+i])
					matrix = np.array(matrix,dtype=np.float) 
					print global_instance_num, '  ', epochs_per_patient
					featuresRow = [patient_num, int(global_instance_num/epochs_per_patient) + 1]

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
							featuresRow.append(functionClass.extractFeatures(np.transpose(allBands[i]).astype('str')))	
					else:
						instanceCode = filename.replace('.csv','') + '_' + str(global_instance_num)
						featuresRow = [instanceCode, patient_num, int(global_instance_num/epochs_per_patient) + 1]
						featuresRow += (functionClass.extractFeatures(matrix))
						
						
					###### TO SAVE SUMMARY STATISTICS ABOUT PEARSON #######
					# toWrite = np.zeros((21,21))
					# # toWrite[np.triu_indices(21, 1)] = featuresRow
					# if(adhc == 0):
					# 	summary_filename = '0_file.csv'
					# else:
					# 	summary_filename = '1_file.csv'
					# exists = os.path.isfile(summary_filename)
					# if exists:
					# 	pearson_data = genfromtxt(summary_filename, delimiter=',')
					# 	pearson_data += toWrite
					# 	np.savetxt(summary_filename, pearson_data, delimiter=",")
					# else:
					# 	np.savetxt(summary_filename, toWrite, delimiter=",")
					
					featuresRow = np.array(featuresRow)
					featuresRow = np.append(featuresRow,adhc)
					writer.writerow(featuresRow)
					global_instance_num+=1

				patient_num += 1
				global_patient_num = patient_num

def createMatrixFeatureSet(function,feature_name, num_electrodes, num_instances, num_timePoints, epochs_per_patient, path1, path2, path3, features_path, data_type, recurr,):
	print("feature set: " + features_path)

	if(feature_name == "DomFreqVar"):
		featuresRead_path = sys.path[0] + '/FeatureSets/'+  paramToFilename("DomFreq", data_type, num_instances ,num_timePoints, epochs_per_patient)
		function.extractFeatures(featuresRead_path, features_path, num_instances, epochs_per_patient, num_electrodes)
	elif (path3 == None):
		if not os.path.exists(features_path):
			writeFeatureSet(function,0,1,features_path, num_instances, epochs_per_patient, num_timePoints,path1)
			writeFeatureSet(function,1,global_patient_num,features_path, num_instances, epochs_per_patient, num_timePoints,path2)
	elif (path2 == None):
		if not os.path.exists(features_path):
			writeFeatureSet(function,0,1,features_path, num_instances, epochs_per_patient, num_timePoints,path1)
			writeFeatureSet(function,2,global_patient_num,features_path, num_instances, epochs_per_patient, num_timePoints,path3)
	elif (path1 == None):
		if not os.path.exists(features_path):
			writeFeatureSet(function,1,1,features_path, num_instances, epochs_per_patient, num_timePoints,path2)
			writeFeatureSet(function,2,global_patient_num,features_path, num_instances, epochs_per_patient, num_timePoints,path3)
	else:
		if not os.path.exists(features_path):
			writeFeatureSet(function,0,1,features_path, num_instances, epochs_per_patient, num_timePoints,path1)
			writeFeatureSet(function,1,global_patient_num,features_path, num_instances, epochs_per_patient, num_timePoints,path2)
			writeFeatureSet(function,2,global_patient_num,features_path, num_instances, epochs_per_patient, num_timePoints,path3)

