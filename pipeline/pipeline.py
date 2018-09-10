from recursiveFeatureElim import recursiveFeatureElim
from svm import svm_func
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import time
from ASD_features import extractASDFeatures
from WTcoef import extractWaveletFeatures
from createFeatureSet import createFeatureSet
from compute_score import compute_score


featureName = ''
num_bunches = 0 #per patient
num_timePoints = 0 #per instance
startAtFS = False

for i in range(1,len(sys.argv),2):		
	if str(sys.argv[i]) == "-h":
		helpString = ('Run pipeline starting from beginning:\nInput arguments:\n-f: feature name (choices: ASD, Wavelet)' + 
		'\n-i: instances per patient (ex: 1)\n-t: number of time points per instance (ex: 60)' +
		'\n\nRun pipeline starting from feature selection:\nInput arguments:\n-fs: feature selection (.../PathToFeatureSetFile)')
		print(helpString)
		sys.exit()
	elif str(sys.argv[i]) == "-f":
		featureName = sys.argv[i+1]
	elif str(sys.argv[i]) == "-i":
		num_bunches = int(sys.argv[i+1])
	elif str(sys.argv[i]) == "-t":
		num_timePoints = int(sys.argv[i+1])
	elif str(sys.argv[i]) == "-fs":
		features_path = sys.argv[i+1]
		startAtFS = True
	else:
		print("Wrong format. Remember header must precede argument provided.\nUse -h for help.")
		sys.exit()

# If starting at the beginning - at feature set creation
if not startAtFS:
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
	else:
		print("Invalid feature name. Choose from list in help documentation")
		sys.exit()

	#feature extraction
	print("Creating Feature Set...")

	#unique identifier for different input parameters
	identifier = str(num_bunches*25) + '_' + str(num_timePoints)

	#define features and reduced_features paths
	features_path = sys.path[0] + '/FeatureSets/'+featureName+'features'+identifier+'.csv'
	reduced_features_path = sys.path[0] + '/ReducedFeatureSets/'+featureName+'features'+identifier+'_reduced.csv'
	
	#create feature set if does not exist in Feature Sets folder
	if not os.path.exists(features_path):
		#3rd parameter is extractFeature function of choice
		#try:
		createFeatureSet(num_bunches, num_timePoints, featureName, extractFeatureFunc)
		#except:
		print("Did not input valid feature name")
			#sys.exit()
	else:
		print("Feature set already exists")


	#obtain global X (input features) and y (output values)
	data = pd.read_csv(features_path)
else: #starting pipeline with feature selection
	data = pd.read_csv(features_path)

#shuffle rows of dataframe
data.sample(frac=1).reset_index(drop=True)
#### obtain Y using last column
y = data.iloc[:,-1]
#### obtain X by dropping last column
X = data.drop(data.columns[-1], axis=1)

##################################################################################

#### feature selection
print("Feature Selection...")
print("Input Shape:", X.shape)


#### Substitute other feature selection methods here 

#####################################

# Reduces features way too much
# Select K Best - no feature importance 
# from sklearn.feature_selection import SelectKBest
# from sklearn.feature_selection import chi2
# # feature extraction
# clf = SelectKBest(score_func=chi2, k=4)
# clf = clf.fit(X, y)

# This clf does NOT have a feature importance feature 

# # summarize scores
# np.set_printoptions(precision=3)
# X_reduced = fit.transform(X)
# # summarize selected features
# print(X_reduced.shape)

# feature_red_name = format(fit)

#####################################

# Reduces features way too much
# Feature Extraction with PCA -> does not have feature importance
# import numpy
# from pandas import read_csv
# from sklearn.decomposition import PCA
# # feature extraction
# pca = PCA(n_components=3)
# fit = pca.fit(X)
# get_feature_importance(fit, X)
# X_reduced = fit.transform(X)
# print(X_reduced.shape)
# # summarize components
# print("Explained Variance: %s") % fit.explained_variance_ratio_
# feature_red_name = format(fit)
# print(fit.components_)

#####################################

#### recursive feature elimination from ASD paper -> this plots 
#### uses SVC
# X_reduced = recursiveFeatureElim(X,y)
# print(X_reduced.shape)

#####################################

# alternative feature selection from sklearn: all have feature importance
# import feature importances plot function
from feature_ranking import get_feature_importance
from pandas import read_csv
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier

clf = ExtraTreesClassifier()
# Get features with ranking of feature's importance (for our visualization purposes)
feat_importances_et = get_feature_importance(clf, X, y, 50) #top 50 features

clf = RandomForestClassifier(n_estimators=50, max_features='sqrt')
feat_importances_rf = get_feature_importance(clf, X, y, 50)

clf = GradientBoostingClassifier()
feat_importances_gb = get_feature_importance(clf, X, y, 50)

common_features = pd.Series(list(set(feat_importances_rf).intersection(set(feat_importances_gb)))).values
print(common_features)

#reduce features
from sklearn.feature_selection import SelectFromModel
model = SelectFromModel(clf, prefit=True)
X_reduced = model.transform(X)
print(X_reduced.shape)

##################################################################################

# learning model
print("Learning model...")
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
#from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier  

num_folds = 10
num_seeds = 10
o_filename = 'output_pipeline.csv'


# Megha's svm
#svm_func(X_reduced,y,num_seeds, num_folds, 'output_pipeline.csv')

#various sklearn models
logreg = LogisticRegression() 
logreg_cv = LogisticRegressionCV()
rf = RandomForestClassifier()
gboost = GradientBoostingClassifier()
#xgboost = XGBClassifier() -> not working
svc = SVC()
kneighbors = KNeighborsClassifier(n_neighbors=5)  

#loop through models and print accuracy for each
models = [logreg, logreg_cv, rf, gboost, svc, kneighbors]
for model in models:
	print('Cross-validation of : {0}'.format(model.__class__))
	all_score = compute_score(model, X, y, num_folds, scoring='accuracy')
	reduced_score = compute_score(model, X_reduced, y, num_folds, scoring='accuracy')
	print('All features CV score = {0}'.format(all_score))
	print('Reduced features CV score = {0}'.format(reduced_score))

	try:
		with open(o_filename, 'r+') as csvfile:
			pass
	except IOError as e:
		with open(o_filename, 'w') as csvfile:
			header = ['Date', 'Classifier', 'Feature Reduction Classifier', 'Number of Features Before Reduction', 
			'Number of Features After Reduction', 'Accuracy', 'Num Folds', 'Num Seeds']
			writer = csv.DictWriter(csvfile, fieldnames=header)
			writer.writeheader()
	# Record the number of features that were reduced
	with open(o_filename, 'a') as f:
		writer = csv.writer(f)
		writer.writerow([time.strftime("%m/%d/%Y"), format(model.__class__), clf, 
			X.shape, X_reduced.shape, format(reduced_score), num_folds, num_seeds])

# Insert new line into CSV file 
with open(o_filename, 'a') as f:
	writer = csv.writer(f)
	writer.writerow("\n")


