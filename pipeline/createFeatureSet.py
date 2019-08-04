import csv
import numpy as np
import os
import sys
import pandas as pd
from BandPass1 import splitbands


def createFeatureSet(num_epochs, num_timePoints, featureName, function, num_electrodes, path1, path2, data_type, f_path, recurr):

	#extract from path to first patient group folder
	# HC
	combined_group1 = np.empty((0,num_electrodes*num_timePoints+2))
	patient_num = 1

	# for each filename inside the folder (HC), if the file is a csv file, open it
	for filename in os.listdir(path1):
		if filename.endswith('.csv'):
			with open(os.path.join(path1, filename)) as f:
				# read the data (format is rows = electrode readings (time points), columns = electrodes (21 of them))
				reader = csv.reader(f)
				array = np.array(list(reader))
				print(array.shape)
				data = array

				#create bunches per patient
				total = np.empty((num_epochs,len(array[0])*num_timePoints+2)) #1000x210
				for bunch in range(num_epochs):
					index = int(bunch*(len(array)/num_epochs))
					#print index
					row = data[index]
					for i in range(1,num_timePoints):
						row = np.append(row, data[index+i])
					#print row
					row = np.append(row,[0])
					total[bunch][0] = patient_num
					total[bunch][1:] = row
					patient_num += 1
				#print total
				combined_group1 = np.concatenate((combined_group1,total))
				
	#extract from path to second patient group folder
	# AD
	combined_group2 = np.empty((0,num_electrodes*num_timePoints+2))
	for filename in os.listdir(path2):
		if filename.endswith('.csv'):
			with open(os.path.join(path2, filename)) as f:
				reader = csv.reader(f)
				array = list(reader)
				array = np.array(array)
				print(array.shape)
				#print len(array) #160,000
				#print len(array[0]) #21
				data = array

				#create bunches per patient
				total = np.empty((num_epochs,len(array[0])*num_timePoints+2)) #1000x210
				for bunch in range(num_epochs):
					index = int(bunch*(len(array)/num_epochs))
					#print index
					row = data[index]
					for i in range(1,num_timePoints):
						row = np.append(row, data[index+i])
					#print row
					row = np.append(row,[1])
					total[bunch][0] = patient_num
					total[bunch][1:] = row
					patient_num += 1
				#print total
				combined_group2 = np.concatenate((combined_group2,total))

				# reader = csv.reader(f)

				# time_point_count = 0
				# patient_num = 1
				# # Patient number is first number in the row
				# curr_array = [patient_num]
				# featureSet = []

				# # For each row in the file 
				# for row in reader:
				# 	if time_point_count != num_timePoints:
				# 		curr_array.extend(row)
				# 		time_point_count += 1
				# 	else:
				# 		curr_array.append(0)
				# 		featureSet.append(curr_array)
				# 		curr_array = []
				# 		time_point_count = 0
				# patient_num += 1
				# combined_group2 = np.concatenate((combined_group2,featureSet))

	combined = np.concatenate((combined_group1, combined_group2))
	#print(combined.shape) #25000x631

	if (recurr):
		#identifier = str(num_epochs) + 'epochs_' + str(num_timePoints) + 'timepoints'
		#features_path = sys.path[0] + '/FeatureSets/'+data_type+'Recurr'+identifier+'.csv'
		if not os.path.exists(f_path):
			out_file = open(f_path,"w")
			writer = csv.writer(out_file)
			for i in range(len(combined)):
				writer.writerow(combined[i])
	else:
		#store and delete last column
		targets = combined[:,-1]
		groups = combined[:,0]
		combined = np.delete(combined,-1,axis=1)
		combined = np.delete(combined,0,axis=1)
		#reshape into 25000 x timepoints x 21
		combined = np.reshape(combined,(len(combined), num_timePoints, num_electrodes))

		from BandPass1 import splitbands

		identifier = str(num_epochs) + 'epochs_' + str(num_timePoints) + 'timepoints'

		# features_path = sys.path[0] + '/FeatureSets/'+data_type+featureName+'features'+identifier+'.csv'
		features_path = sys.path[0] + '/FeatureSets/'+data_type+featureName+identifier+'.csv'

		if not os.path.exists(features_path):
			open(features_path,"w")

		#count number of lines already present in file - start at this number + 1 for iterations
		read_file = open(features_path,"r")
		reader = csv.reader(read_file)
		row_count = sum(1 for row in reader)
		print "printing row count"
		print row_count

		out_file = open(features_path,"a") #used to be "a" for append
		writer = csv.writer(out_file)

		print("Feature Extraction...")


		#initialize header list (add the first column which is patient num)
		headers = []
		headers.append("patient_num")

		#create header list
		# for all columns 
		for i in range(row_count,len(combined)):
			#transpose each n x 21 so each row is time series points (columns) of 1 electrode (row)
			transposed = np.transpose(combined[i]) 
			#print "Transposed shape"
			#print(transposed.shape) Shape is (21, 60) 
			#add another dimension in each row to make it 5 bands x n
			# for each electrode 
			for j in range(len(transposed)):
				if (i==0):
					bands = splitbands(transposed[j])
				#squish each band of raw points into n feature values
				for k in range(len(bands)): #bands[j] = band of raw data
					if (j==0):
						bandfeatures = function(bands[k])
					#adding headers
					if (i == 0):
						# Shouldn't be printing out patient num here
						featureHeaders = []
						# This gets repeated for each band
						for h in range(len(bandfeatures)):		
							featureHeaders.append("electrode"+str(j+1)+"band"+str(k+1)+"feature"+str(h+1))
						headers.extend(featureHeaders)

		headers.append('class')
		writer.writerow(headers)

		for i in range(row_count,len(combined)):
			print(i)
			print(str(i+1) + " out of " + str(25*num_epochs))
			#transpose each n x 21 so each row is time series points (columns) of 1 electrode (row)
			transposed = np.transpose(combined[i]) 
			features = [groups[i]]
			#add another dimension in each row to make it 5 bands x n
			for j in range(len(transposed)):
				bands = splitbands(transposed[j])
				#squish each band of raw points into n feature values
				for k in range(len(bands)): #bands[j] = band of raw data
					bandfeatures = function(bands[k])
					features.extend(bandfeatures)

			features.append(targets[i])
			#Add feature values of each band from each electrode (per instance) to new array
			writer.writerow(features)