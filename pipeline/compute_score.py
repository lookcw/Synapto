from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GroupKFold
from sklearn.base import clone
from metrics import metrics
import numpy as np

#define function to compute cross validation score
def compute_group_score(clf, X, y, num_folds, groups, scoring='accuracy'):
	isPredictProba = False
	invert_op = getattr(clf, "predict_proba", None)
	if callable(invert_op):
		isPredictProba = True
	gkf = GroupKFold(n_splits=num_folds)
	y_true = np.array(np.zeros(len(y)))
	y_pred = np.array(np.zeros(len(y)))
	y_scores = None
	if isPredictProba:
		y_scores = np.array(np.zeros((len(y),2)))
	count = 0
	print "groups: ",groups.shape
	for train, test in gkf.split(X, y, groups=groups):
		clf.fit(X[train],y[train])
		y_pred[count:count+len(test)] = clf.predict(X[test])
		y_true[count:count+len(test)] = y[test]
		if isPredictProba:
			y_scores[count:count+len(test)] = clf.predict_proba(X[test])
		clf = clone(clf)
		count += len(test)
	(accuracy,f1, tnP,fpP,fnP,tpP,roc_auc) = metrics(y_true,y_pred,y_scores)
	return (accuracy,f1, tnP,fpP,fnP,tpP,roc_auc)