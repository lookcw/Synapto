import numpy as np


#creates copy of data set with slight noise and concatenates to end
#pass in patient feature set and desired number of augumented copies
def augment(Xdata, Ydata, copies):
	num_patients = len(Xdata)
	num_features = len(Xdata[0])
	synthetic_data = np.zeros((num_features,num_patients))
	appendY = Ydata

	for copy in range(copies):

		for i in range(num_features):

			feature = Xdata[0:num_patients,i]
			stdv = np.std(feature)
			noise = np.random.normal(0,stdv,len(feature))
			#implement dynamic stddev in noise data based on feature stddev/zscore
			#print(noise)
			synthetic_feature = feature + noise
			#print(synthetic_feature)
			synthetic_data[i] = synthetic_feature
			#print(synthetic_data)

		synthetic_data = np.transpose(synthetic_data)
		Xdata = np.concatenate((Xdata,synthetic_data))

		synthetic_data = np.zeros((num_features,num_patients))

		Ydata = np.append(Ydata, appendY)

	print(Xdata)
	print(Ydata)


xdata = np.array([[1,1,30,35],
				 [2,2,31,37],
				 [2,3,31,34]], dtype = float)

array_Y = np.array([0,0,1])

augment(xdata, array_Y, 2)




