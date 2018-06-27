import csv
import numpy as np
import os
import sys

a = [[1,2,3],[4,5,6],[7,8,9]]
print(a)
for i in range(len(a)):
	a = np.transpose(a)
print(a)
sys.exit()

num_bunches = 1000
num_timePoints = 30

basepath = 'RawData/HCF50'
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

basepath = 'RawData/ADF50'
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
print(combined.shape) #25000x631

#store and delete last column
targets = combined[:,-1]
combined = np.delete(combined,-1,axis=1)
#reshape into 25000 x 21 x timepoints
combined = np.reshape(combined,(len(combined), 21, n_timeSteps))
#transpose each 21 x n so each row is time series points of 1 electrode
for i in range(len(combined)):
	combined[i] = np.transpose(combined[i])
#squish each row of raw points into feature vector
#flatten out array so as to concatenate feature values from each electrode
sys.exit()

out_file = open("/Users/Anoop/Documents/Synapto/IgnoreData/testCreateInstances.csv","w")
for i in range(len(combined)):
	writer = csv.writer(out_file)
	writer.writerow(combined[i])


#createInstances