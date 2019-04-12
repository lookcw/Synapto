# alternative feature selection from sklearn: all have feature importance
# import feature importances plot function
from feature_ranking import get_feature_importance
from pandas import read_csv
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier

clf = ExtraTreesClassifier()
# Get features with ranking of feature's importance (for our visualization purposes)
feat_importances_et = get_feature_importance(clf, X, y, 945) #top 50 features

clf = RandomForestClassifier(n_estimators=50, max_features='sqrt')
feat_importances_rf = get_feature_importance(clf, X, y, 945)

clf = GradientBoostingClassifier()
feat_importances_gb = get_feature_importance(clf, X, y, 945)

common_features = pd.Series(list(set(feat_importances_rf).intersection(set(feat_importances_gb)))).values
print(common_features)

#reduce features
from sklearn.feature_selection import SelectFromModel
model = SelectFromModel(clf, prefit=True)
X_reduced = model.transform(X)
print("reduced shape:" + str(X_reduced.shape))