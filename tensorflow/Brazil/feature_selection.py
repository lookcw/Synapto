import numpy as np
from sklearn.svm import SVC
from sklearn.feature_selection import RFECV
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
import pandas as pd 
import csv
import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' #hide warnings
print("starting")
# Network Parameters

def feature_selection(in_file = "", n_classes = 0):
	if in_file == "":
		print("did not include file name")
		sys.exit(1)
	if n_classes == 0:
		print("did not include number of classes")
		sys.exit(1)

	#training set
	array_Y = []
	total = []
	with open(in_file) as f:
		reader = csv.reader(f)
		#next(reader)
		array = list(reader)
		n_input =  len(array[0])-1 
		array = np.array(array)
		
	# Data input
		#add each patient's feature values (row) to array
		for row in array[1:]: #first row is column headers
			if (row[-1] == '-'): #HC patients
				total.append(row[0:-1])
				#output = 0
				array_Y.extend([0])
			else: #AD patients
				total.append(row[0:-1])
				#output = 1
				array_Y.extend([1])
	total = np.array(total)


	X_data = np.array(total)
	array_Y = np.array(array_Y)


	#controlled shuffle function
	def shuffle(input):
		np.random.seed(5)
		np.random.shuffle(input)

	shuffle(X_data)
	shuffle(array_Y)

	def reduce_features(X, y):
		# Create the RFE object and compute a cross-validated score.
		svc = SVC(kernel="linear")
		# The "accuracy" scoring is proportional to the number of correct
		# classifications
		rfecv = RFECV(estimator=svc, step=1, cv=3, scoring='accuracy')

		print(X.shape)
		print(y.shape)
		rfecv.fit(X, y)

		# Plot number of features VS. cross-validation scores
		plt.figure()
		plt.xlabel("Number of features selected")
		plt.ylabel("Cross validation score (nb of correct classifications)")
		plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
		#plt.show()

		feature_ranking = rfecv.ranking_
		optimal_features = rfecv.n_features_

		print("Optimal number of features : %d" % optimal_features)
		print("Feature ranking : ", feature_ranking)
	
		reduced_features_indices = np.where(feature_ranking == 1)

		X = np.take(X, reduced_features_indices, axis=1)
		X = np.reshape(X,(len(X), optimal_features))
		print(X.shape)

		df = pd.DataFrame(X)
		df.to_csv(in_file[0:-4] + '_feature_reduced.csv', header = False, index = False)

	reduce_features(X_data, array_Y)


n=1
for argument in sys.argv[1:]:
	if (argument == "-f"):
		filename = sys.argv[n+1]

feature_selection(in_file = filename, n_classes = 2)

