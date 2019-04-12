from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from sklearn.feature_selection import SelectFromModel

def get_XReduced(clf, X):

	model = SelectFromModel(clf, prefit=True)
	X_reduced = model.transform(X)
	return X_reduced