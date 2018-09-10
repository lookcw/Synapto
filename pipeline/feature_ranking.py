
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_feature_importance(clf, X, y, num_features):
	clf = clf.fit(X,y)
	#print(clf)


	#plot feature importances (top 50)
	feat_importances = pd.Series(clf.feature_importances_, index=X.columns)
	feat_importances = feat_importances.nlargest(num_features)

	indices = np.argsort(feat_importances)[::-1]

	for f in range(X.shape[1]):
		print("%d. feature %d (%f)" % (f + 1, indices[f], feat_importances[indices[f]]))
	
	# Plot features
	plt.figure(figsize=(16,8))
	feat_importances.plot(kind='barh')
	plt.gca().invert_yaxis()
	plt.show()

	return feat_importances

	#reduce features
	# X_reduced = clf.transform(X)
	# print(X_reduced.shape)

	# return X_reduced
