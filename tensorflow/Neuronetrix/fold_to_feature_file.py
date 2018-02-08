import numpy as np
import csv
import os

num_HC = 75
num_AD = 75

f_out = open("data/all_fft_des.csv",'wb')
writer = csv.writer(f_out,delimiter=',')
count = 0
HC_folders = ["HCD_fft","HCS_fft","HCT_fft"]
AD_folders = ["ADD_fft","ADS_fft","ADT_fft"]
HC_prefix = ["NHDfft","NHSfft","NHTfft"]
AD_prefix = ["NADfft","NASfft","NATfft"]
for i in range(num_HC):
	HC = []
	count_cols = 0 
	for j in range(len(HC_folders)):
		f = open(HC_folders[j] + "/" + HC_prefix[j] + str(i+1) +".csv",'r')
		reader = csv.reader(f,delimiter = "," )
		array = np.array(list(reader))
		#concatenate each electrode fft vector into one vector per instance

		for e in range(len(array.T)):
			if count == 0:
				count_cols += len(array[:,e])
			E = (array[:,e])
			HC.extend(E)
			
		#add fft values of each instance
		#output = 0
	HC.append('-')
	print HC[-1]
	if count == 0:
			header = []
			for i in range(1,count_cols+2):
				header.append("col " + str(i))
			writer.writerow(header)
			count += 1	
	writer.writerow(HC)

for i in range(num_AD):
	AD = []
	count_cols = 0 
	for j in range(len(AD_folders)):
		f = open(AD_folders[j] + "/" + AD_prefix[j] + str(i+1) +".csv",'r')
		reader = csv.reader(f,delimiter = "," )
		array = list(reader)
		array = np.array(array)
		#concatenate each electrode fft vector into one vector per instance

		for e in range(len(array.T)):
			if count == 0:
				count_cols += len(array[:,e])
			E = (array[:,e])
			AD.extend(E)
			
		#add fft values of each instance
		#output = 0
	AD.append('+')
	writer.writerow(AD)