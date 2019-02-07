
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv


def get_feature_importance(clf, X, y, num_features):
	clf = clf.fit(X,y)
	#print(clf)


	#plot feature importances (top 50)
	feat_importances = pd.Series(clf.feature_importances_, index=X.columns)
	feat_importances = feat_importances.nlargest(num_features)

	# Sort the feature importances in decreasing order (with the highest importance values at the top)
	indices = np.argsort(feat_importances)[::-1]


	o_filename = 'feature_importance_values.csv'

	try:
		with open(o_filename, 'r+') as csvfile:
			pass
	except IOError as e:
		with open(o_filename, 'w') as csvfile:
			header = ['Number', 'Which Feature', 'Importance Value']
			writer = csv.DictWriter(csvfile, fieldnames=header)
			writer.writeheader()
	# Record the number of features that were reduced
	with open(o_filename, 'a') as f:
		writer = csv.writer(f)
		# Print the feature importances to a console
		# X.shape[1] goes to the total number of features 
<<<<<<< HEAD
		for feat in range(1, X.shape[1]):
=======
		for feat in range(1,X.shape[1]):
>>>>>>> 17cdab2fa1e30db05acabf29680e89ece2d0de2c
			print("%d. feature %d (%f)" % (feat + 1, indices[feat], feat_importances[indices[feat]]))
			writer.writerow([feat + 1, indices[feat], feat_importances[indices[feat]]])

	# for f in range(X.shape[1]):
	# 	print("%d. feature %d" % (f + 1, indices[f]))
	
	# Plot features
	plt.figure(figsize=(16,8))
	feat_importances.plot(kind='barh')
	plt.gca().invert_yaxis()
	#plt.show()
	#print(feat_importances)

	return feat_importances

	#reduce features
	# X_reduced = clf.transform(X)
	# print(X_reduced.shape)

	# return X_reduced
