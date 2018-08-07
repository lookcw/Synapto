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
# Network Parameters

def recursiveFeatureElim(X, y):
	# Create the RFE object and compute a cross-validated score.
	svc = SVC(kernel="linear")
	# The "accuracy" scoring is proportional to the number of correct
	# classifications
	rfecv = RFECV(estimator=svc, step=1, cv=3, scoring='accuracy')

	rfecv.fit(X, y)

	# Plot number of features VS. cross-validation scores
	plt.figure()
	plt.xlabel("Number of features selected")
	plt.ylabel("Cross validation score (nb of correct classifications)")
	plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
	plt.show()

	feature_ranking = rfecv.ranking_
	optimal_features = rfecv.n_features_

	print("Optimal number of features : %d" % optimal_features)
	#print("Feature ranking : ", feature_ranking)

	reduced_features_indices = np.where(feature_ranking == 1)
	print(reduced_features_indices)
	
	X_reduced = np.take(X.values, reduced_features_indices, axis=1)
	X_reduced = np.reshape(X_reduced,(len(X), optimal_features))
	return X_reduced

	# df = pd.DataFrame(X)
	# df['Y'] = Ycol
	# df.to_csv(in_file[0:-4] + '_feature_reduced.csv', header = False, index = False)

#reduce_features(X_data, array_Y)
