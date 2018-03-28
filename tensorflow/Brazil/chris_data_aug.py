import numpy as np
import csv
import re



#creates copy of data set with slight noise and concatenates to end
#pass in patient feature set and desired number of augumented copies
def augment(in_file,out_file, copies):
	with open(in_file) as f:
		reader = csv.reader(f)
		array = list(reader)
		if (re.match("^\d+?\.\d+?$", array[0][0]) is None) or not array[0][0].isdigit():
			array = array[1:]
		print len(array)
		array = np.array(array)
	HC = []
	AD = []
	for row in array:
		if row[-1] == "-":
			HC.append(row[:-1])
		else:
			AD.append(row[:-1])
	AD = np.array(AD).astype(float)
	HC = np.array(HC).astype(float)
	num_patients = len(HC) + len(AD)
	print num_patients
	num_features = len(HC[0])
	synthetic_data_AD = np.zeros(( copies*len(AD),num_features))
	synthetic_data_HC = np.zeros(( copies*len(HC),num_features))
	HC_curr_copy = 0
	AD_curr_copy = 0
	for i in range(copies):
		print "copy = ",i
		for j in range(num_features):
			AD_std = np.std(AD[:,j])
			HC_std = np.std(HC[:,j])
			for k in range(len(AD)):
				# print "k= ",k," copy_num = ",copy_num
				synthetic_data_AD[AD_curr_copy + k][j] = AD[k][j] + np.random.normal(0, AD_std)
			for k in range(len(HC)):
				synthetic_data_HC[HC_curr_copy + k][j] = HC[k][j] + np.random.normal(0, HC_std)
		HC_curr_copy += len(HC)
		AD_curr_copy += len(AD)
	AD_arr = np.concatenate((AD,synthetic_data_AD),axis = 0).tolist()
	HC_arr = np.concatenate((HC,synthetic_data_HC),axis = 0).tolist()

	for i in range(len(AD_arr)):
		AD_arr[i].append("+")
	for i in range(len(HC_arr)):
		HC_arr[i].append("-")

	writer = csv.writer(open(out_file,'w'),delimiter = ',')
	writer.writerows(AD_arr[0:len(AD)])
	writer.writerows(HC_arr[0:len(HC)])
	writer.writerows(AD_arr[len(AD):])
	writer.writerows(HC_arr[len(HC):])



augment("Feature_Sets/AllFFT_B_z.csv","Feature_Sets/AllFFT_B_z_aug1.csv",10)