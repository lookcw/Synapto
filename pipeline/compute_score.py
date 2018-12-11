from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GroupKFold
import numpy as np

#define function to compute cross validation score
def compute_group_score(clf, X, y, num_folds, groups, scoring='accuracy'):
	gkf = GroupKFold(n_splits=num_folds)
	score = 0
	print "groups: ",groups.shape
	for train, test in gkf.split(X, y, groups=groups):
		clf.fit(X[train],y[train])
		score += clf.score(X[test], y[test])
	return float(score) / num_folds