import pandas as pd
import matplotlib.pyplot as plt


def get_feature_importance(clf, X, y):
	clf = clf.fit(X,y)
	#print(clf)


	#plot feature importances (top 50)
	feat_importances = pd.Series(clf.feature_importances_, index=X.columns)
	feat_importances = feat_importances.nlargest(50)
	plt.figure(figsize=(16,8))
	feat_importances.plot(kind='barh')
	plt.gca().invert_yaxis()
	plt.show()

	#reduce features
	# X_reduced = clf.transform(X)
	# print(X_reduced.shape)

	# return X_reduced
