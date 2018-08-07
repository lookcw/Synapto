import pandas as pd


def get_feature_importance(clf, X, y):
	clf = clf.fit(X,y)

	#feature ranking
	features = pd.DataFrame()
	features['feature'] = X.columns
	features['importance'] = clf.feature_importances_
	features.sort_values(by=['importance'], ascending=True, inplace=True)
	features.set_index('feature', inplace=True)
	features.plot(kind='barh', figsize=(25, 25))
	import matplotlib.pyplot as plt
	plt.show()

	#reduce features
	# X_reduced = clf.transform(X)
	# print(X_reduced.shape)

	# return X_reduced
