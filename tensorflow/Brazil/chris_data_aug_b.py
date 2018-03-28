import numpy as np
import csv


#creates copy of data set with slight noise and concatenates to end
#pass in patient feature set and desired number of augumented copies
def augment(in_file, copies):

	array_Y = []
	total = []
	countHC = 0

	with open(in_file) as f:
		reader = csv.reader(f)
		array = list(reader)
		# if not ((isinstance(array[0][0],float)) || (isinstance(array[0][0],int))):
		# 	array = array[1:]
		print len(array)
		array = np.array(array)

		 
		for row in array[0:]:
			if (row[-1] == "-"):
				total.append(row[0:-1])
				#output = 0
				array_Y.extend("-")
				countHC = countHC + 1
			else:
				total.append(row[0:-1])
				#output = 1
				array_Y.extend("+")
	total = np.array(total)

	Xdata = np.array(total, dtype = float)
	Ydata = np.array(array_Y)

	num_patients = len(Xdata)
	num_features = len(Xdata[0])
	synthetic_data = np.zeros((num_features, copies*num_patients))
	appendY = Ydata

	count = 0
	for copy in range(copies):

		for i in range(num_features):

			feature = Xdata[0:num_patients, i]

			HCstdv = np.std(feature[:countHC])
			ADstdv = np.std(feature[countHC:])
			HCnoise = np.random.normal(0, HCstdv, len(feature[:countHC]))
			ADnoise = np.random.normal(0, ADstdv, len(feature[countHC:]))
			feature[:countHC] = feature[:countHC] + HCnoise
			feature[countHC:] = feature[countHC:] + ADnoise
			synthetic_feature = feature
			synthetic_data[i] = synthetic_feature


		synthetic_data = np.transpose(synthetic_data)

		Xdata = np.concatenate((Xdata, synthetic_data))
		#print synthetic_data
		#print Xdata
		synthetic_data = np.zeros((num_features, num_patients))

		Ydata = np.append(Ydata, appendY)


	data = np.zeros((len(Xdata), num_features + 1))

	# for i in range(len(Xdata)):
	#     data[i] = np.append(Xdata[i], Ydata[i])

	
	out_file = open("data_aug.csv","w")
	
	for count in range(len(Xdata)):
		writer = csv.writer(out_file)
		arr = np.ndarray.tolist(Xdata[count])

		arr.append(Ydata[count])
		writer.writerow(arr)

augment("test.csv", 20)

# augment("Feature_Sets/AllFFT_B_z.csv", 10)

