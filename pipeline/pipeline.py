from featureSelection import reduce_features
from svm import svm_func
import os
import sys
import pandas as pd
import numpy as np
from ASD_features import ASDfeatures_func
from createFeatureSet import createFeatureSet


#feature extraction
print("Feature Extraction...")

num_bunches = 1 #per patient
num_timePoints = 60 #per bunch

identifier = str(num_bunches*25) + '_' + str(num_timePoints)
features_path = sys.path[0] + '/FeatureSets/ASDfeatures'+identifier+'.csv'
reduced_features_path = sys.path[0] + '/ReducedFeatureSets/ASDfeatures'+identifier+'_reduced.csv'

if os.path.exists(features_path) == False:
	createFeatureSet(num_bunches, num_timePoints, ASDfeatures_func)


#obtain global X (input features) and y (output values)
data = pd.read_csv(features_path, header = None)

#X.to_csv(sys.path[0] + '/FeatureSets/ASDfeatures.csv', header = False, index = False)
y = data.iloc[:,-1]
X = data.drop(data.columns[-1], axis=1)

#shuffle X and y

# feature selection
print("Feature Selection...")

if os.path.exists(reduced_features_path) == False:
	X_reduced = reduce_features(X,y)
	X_reduced = pd.DataFrame(X_reduced)

	#combine X_reduced and y and output reduced csv file if does not exist
	data_reduced = pd.concat([X_reduced, y], axis=1)
	print(data_reduced.shape)
	data_reduced.to_csv(reduced_features_path, header=None, index=None)
else:
	data_reduced = pd.read_csv(reduced_features_path, header=None)
	X_reduced = data_reduced.drop(data_reduced.columns[-1], axis=1)

print(X_reduced.shape)

# feature_directory = sys.path[0] + '/FeatureSets'
# reduced_directory = sys.path[0] + '/ReducedFeatureSets'
# for filename in os.listdir(feature_directory):
# 	if filename.endswith(".csv"):
# 		reduced_filename = filename.split('.')[0] + "_feature_reduced.csv"
# 		print(reduced_filename)
# 		check_path = os.path.join(reduced_directory, reduced_filename)
# 		if (os.path.exists(check_path) == False):
# 			print(filename)
# 			path = os.path.join(feature_directory, filename)
# 			feature_selection(path)
# 		else: 
# 			print("file already feature reduced")
# for filename in os.listdir(feature_directory):
# 	if filename.endswith("_feature_reduced.csv"):
# 		print("putting new file in feature reduced folder")
# 		os.rename(os.path.join(feature_directory, filename), os.path.join(reduced_directory, filename))


#alternative feature selection
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
clf = RandomForestClassifier(n_estimators=50, max_features='sqrt')
clf = clf.fit(X, y)


#feature ranking
features = pd.DataFrame()
features['feature'] = X.columns
features['importance'] = clf.feature_importances_
features.sort_values(by=['importance'], ascending=True, inplace=True)
features.set_index('feature', inplace=True)
features.plot(kind='barh', figsize=(25, 25))
#print(features)

#reduce features
model = SelectFromModel(clf, prefit=True)
X_reduced = model.transform(X)
print(X_reduced.shape)

# learning model
print("Learning model...")

num_folds = 10
num_seeds = 10

#megha's svm
svm_func(X_reduced,y,num_seeds,num_folds, 'output.csv')


from sklearn.model_selection import cross_val_score

def compute_score(clf, X, y, scoring='accuracy'):
    xval = cross_val_score(clf, X, y, cv = num_folds, scoring=scoring)
    return np.mean(xval)


from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier  

#models
logreg = LogisticRegression()
logreg_cv = LogisticRegressionCV()
rf = RandomForestClassifier()
gboost = GradientBoostingClassifier()
xgboost = XGBClassifier()
svc = SVC()
kneighbors = KNeighborsClassifier(n_neighbors=5)  

models = [logreg, logreg_cv, rf, gboost, xgboost, svc, kneighbors]
for model in models:
	print('Cross-validation of : {0}'.format(model.__class__))
	all_score = compute_score(model, X, y, scoring='accuracy')
	reduced_score = compute_score(model, X_reduced, y, scoring='accuracy')
	print('All features CV score = {0}'.format(all_score))
	print('Reduced features CV score = {0}'.format(reduced_score))

