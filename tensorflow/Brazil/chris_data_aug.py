import numpy as np
import csv
import re



#creates copy of data set with slight noise and concatenates to end
#pass in patient feature set and desired number of augumented copies
def augment(array, copies):
	# with open(in_file) as f:
	# 	reader = csv.reader(f)
	# 	array = list(reader)
	# 	if (re.match("^\d+?\.\d+?$", array[0][0]) is None) or not array[0][0].isdigit():
	# 		array = array[1:]
	# 	print len(array)
	# 	array = np.array(array)
	HC = []
	AD = []
	for row in array:
		if row[-1] == "0":
			HC.append(row[:-2])
		else:
			AD.append(row[:-2])
	AD = np.array(AD).astype(float)
	HC = np.array(HC).astype(float)
	num_patients = len(HC) + len(AD)
	if len(HC) > 0:
		num_features = len(HC[0])
	else:
		num_features = len(AD[0])
	synthetic_data_AD = np.zeros(( copies*len(AD),num_features))
	synthetic_data_HC = np.zeros(( copies*len(HC),num_features))
	HC_curr_copy = 0
	AD_curr_copy = 0
	for i in range(copies):
		for j in range(num_features):
			AD_std = np.std(AD[:,j])
			HC_std = np.std(HC[:,j])
			for k in range(len(AD)):
				# print "k= ",k," copy_num = ",copy_num
				synthetic_data_AD[AD_curr_copy + k][j] = AD[k][j] + np.random.normal(0, AD_std**2)
			for k in range(len(HC)):
				synthetic_data_HC[HC_curr_copy + k][j] = HC[k][j] + np.random.normal(0, HC_std**2)
		HC_curr_copy += len(HC)

		AD_curr_copy += len(AD)
	
	AD_arr = np.concatenate((AD,synthetic_data_AD),axis = 0).tolist()
	HC_arr = np.concatenate((HC,synthetic_data_HC),axis = 0).tolist()		
	for i in range(len(AD_arr)):
		AD_arr[i] = np.concatenate((AD_arr[i],[0,1]),axis = 0)


	print "asdf",HC_arr[i]
	for i in range(len(HC_arr)):
		HC_arr[i] = np.concatenate((HC_arr[i],[1,0]),axis = 0)


	return np.concatenate((AD_arr,HC_arr),axis = 0)