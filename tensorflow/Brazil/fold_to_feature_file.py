import numpy as np
import csv
import os

#turns folders of fft data and puts them all into a feature set file
#change HC* & AD* arrays based on name of files

num_HC = 12
num_AD = 12

f_out = open("Feature_Sets/fft_B_des.csv",'wb')
writer = csv.writer(f_out,delimiter=',')
count = 0
# HC_folders = ["AD_fft","HC_fft_B","HC_fft_S"]
# AD_folders = ["AD_fft","AD_fft_B_Chris","AD_fft_S"]
HC_folders = ["../../Data/HC_fft_B"]
AD_folders = ["../../Data/AD_fft_B"]
# HC_prefix = ["BAfft","BAfftB1","NHTfft"]
# AD_prefix = ["NADfft","NASfft","NATfft"]
HC_prefix = ["BHfftB"]
AD_prefix = ["BAfftB"] 
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
	print "appending -"
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
		print HC[-1]
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
	print "appending +"
	AD.append('+')
	writer.writerow(AD)