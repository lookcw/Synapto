from featureSelection import reduce_features
from svm import svm_func
import os
import sys
import pandas as pd
import numpy as np
from ASD_features import extractASDFeatures
from WTcoef import extractWaveletFeatures
from createFeatureSet import createFeatureSet

featureName = ''

num_bunches = 0 #per patient
num_timePoints = 0 #per instance

for i in range(1,len(sys.argv),2):		
	if str(sys.argv[i]) == "-h":
		helpString = ('Input argument headers:\n-f: feature name (choices: ASD, Wavelet)' + 
		'\n-i: number of instances per patient (ex: 1)\n-t: number of time points per instance (ex: 60)')
		print(helpString)
		sys.exit()
	elif str(sys.argv[i]) == "-f":
		featureName = sys.argv[i+1]
	elif str(sys.argv[i]) == "-i":
		num_bunches = int(sys.argv[i+1])
	elif str(sys.argv[i]) == "-t":
		num_timePoints = int(sys.argv[i+1])
	else:
		print("Wrong format. Remember header must precede argument provided.\nUse -h for help.")
		sys.exit()

if featureName == '':
	print("Did not input feature name argument (-f)")
	#sys.exit()
if num_bunches == 0:
	print("Did not input instances per patient argument (-i)")
	#sys.exit()
if num_timePoints == 0:
	print("Did not input time points argument (-t)\nUse -h for help.")
	sys.exit()

if featureName == 'ASD':
	extractFeatureFunc = extractASDFeatures
elif featureName == 'Wavelet':
	extractFeatureFunc = extractWaveletFeatures


#feature extraction
print("Feature Extraction...")

#unique identifier for different input parameters
identifier = str(num_bunches*25) + '_' + str(num_timePoints)

#define features and reduced_features paths
features_path = sys.path[0] + '/FeatureSets/'+featureName+'features'+identifier+'.csv'
reduced_features_path = sys.path[0] + '/ReducedFeatureSets/'+featureName+'features'+identifier+'_reduced.csv'

#create feature set if does not exist in Feature Sets folder
if os.path.exists(features_path) == False:
	#3rd parameter is extractFeature function of choice
	try:
		createFeatureSet(num_bunches, num_timePoints, featureName, extractFeatureFunc)
	except:
		print("Did not input valid feature name")
		sys.exit()

#obtain global X (input features) and y (output values)
data = pd.read_csv(features_path, header = None)

#shuffle rows of dataframe
data.sample(frac=1).reset_index(drop=True)

#obtain Y using last column
y = data.iloc[:,-1]
#obtain X by dropping last column
X = data.drop(data.columns[-1], axis=1)


# feature selection
print("Feature Selection...")

#create reduced_features file if does not exist in Reduced Features Sets folder
# if os.path.exists(reduced_features_path) == False:
# 	X_reduced = reduce_features(X,y)
# 	X_reduced = pd.DataFrame(X_reduced)
# 	#combine X_reduced and y
# 	data_reduced = pd.concat([X_reduced, y], axis=1)
# 	print(data_reduced.shape)
# 	#output reduced csv file
# 	data_reduced.to_csv(reduced_features_path, header=None, index=None)
# else: #read in reduced csv file if already exists
# 	data_reduced = pd.read_csv(reduced_features_path, header=None)
# 	#remove output column to obtain X_reduced
# 	X_reduced = data_reduced.drop(data_reduced.columns[-1], axis=1)

# print(X_reduced.shape)

#feature selection from ASD paper
ASDX_reduced = reduce_features(X,y)
print(ASDX_reduced.shape)

#alternative feature selection from sklearn
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
#define function to compute cross validation score
def compute_score(clf, X, y, scoring='accuracy'):
    xval = cross_val_score(clf, X, y, cv = num_folds, scoring=scoring)
    return np.mean(xval)


from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier  

#various sklearn models
logreg = LogisticRegression()
logreg_cv = LogisticRegressionCV()
rf = RandomForestClassifier()
gboost = GradientBoostingClassifier()
xgboost = XGBClassifier()
svc = SVC()
kneighbors = KNeighborsClassifier(n_neighbors=5)  

#loop through models and print accuracy for each
models = [logreg, logreg_cv, rf, gboost, xgboost, svc, kneighbors]
for model in models:
	print('Cross-validation of : {0}'.format(model.__class__))
	all_score = compute_score(model, X, y, scoring='accuracy')
	reduced_score = compute_score(model, ASDX_reduced, y, scoring='accuracy')
	print('All features CV score = {0}'.format(all_score))
	print('Reduced features CV score = {0}'.format(reduced_score))

