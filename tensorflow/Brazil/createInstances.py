import csv
import numpy as np
import os

#def createInstances():

num_bunches = 1000
num_timePoints = 60

basepath = 'RawData/HCF50'
combined_HC = np.empty((0,21*num_timePoints+1))
for filename in os.listdir(basepath):
	if filename.endswith('.csv'):
		with open(os.path.join(basepath, filename)) as f:
			reader = csv.reader(f)
			array = list(reader)
			array = np.array(array)
			print array.shape
			#print len(array) #160,000
			#print len(array[0]) #21
			data = array

			#create bunches per patient
			total = np.empty((num_bunches,len(array[0])*num_timePoints+1)) #1000x210
			for bunch in range(num_bunches):
				index = bunch*(len(array)/num_bunches)
				#print index
				row = data[index]
				for i in range(1,num_timePoints):
					row = np.append(row, data[index+i])
				#print row
				row = np.append(row,[0])
				total[bunch] = row
			#print total
			combined_HC = np.concatenate((combined_HC,total))

basepath = 'RawData/ADF50'
combined_AD = np.empty((0,21*num_timePoints+1))
for filename in os.listdir(basepath):
	if filename.endswith('.csv'):
		with open(os.path.join(basepath, filename)) as f:
			reader = csv.reader(f)
			array = list(reader)
			array = np.array(array)
			print array.shape
			#print len(array) #160,000
			#print len(array[0]) #21
			data = array

			#create bunches per patient
			total = np.empty((num_bunches,len(array[0])*num_timePoints+1)) #1000x210
			for bunch in range(num_bunches):
				index = bunch*(len(array)/num_bunches)
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


out_file = open("testCreateInstances.csv","w")
for i in range(len(combined)):
	writer = csv.writer(out_file)
	writer.writerow(combined[i])


#createInstances