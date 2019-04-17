from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from sklearn.feature_selection import SelectFromModel
import numpy as np

def get_XReduced(clf, X):

	model = SelectFromModel(clf, prefit=True)
	# np.nan_to_num(X)
	X_reduced = model.transform(X)
	return X_reduced