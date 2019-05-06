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
# from WTcoef import extractWaveletFeatures
from createFeatureSet import createFeatureSet
from createMatrixFeatureSet import createMatrixFeatureSet
from pearson_features import extractPearsonFeatures
from FSL_features import extractFSLFeatures
from compute_score import compute_group_score
from nn_keras import nn_keras
import random
from sklearn.utils import shuffle
import functools
#from nn_Recurr import nn_Recurr


featureName = ''
data_type = ''
num_epochs = 0 #per patient
num_timePoints = 0 #per instance
startAtFS = False
FS = True #feature selection
RECURR = False

for i in range(1,len(sys.argv),2):
	if str(sys.argv[i]) == "-h":
		helpString = ('Run pipeline starting from beginning:\nInput arguments:\n-d: data type (choices: Brazil, Greece)' +
		'\n-f: feature name (choices: ASD, Wavelet, FSL)\n-i: instances per patient (ex: 1)\n-t: number of time points per instance (ex: 60)' +
		'\n-nfs: no feature selection\n-recurr: use LSTM' +
		'\n\nRun Pipeline With Existing Feature Set:\nInput arguments:\n-fs: feature set (.../PathToFeatureSetFile)')
		print(helpString)
		sys.exit()
	
	elif str(sys.argv[i]) == "-d":
		data_type = sys.argv[i+1]
		if data_type != 'Brazil' and data_type != 'Greece' and data_type != 'newBrazil':
			print("Invalid type of data. Choose from list in help documentation")
			sys.exit()
	elif str(sys.argv[i]) == "-e":
		epochs_per_instance = int(sys.argv[i+1])

	elif str(sys.argv[i]) == "-f":
		featureName = sys.argv[i+1]

	elif str(sys.argv[i]) == "-i":
		num_instances = int(sys.argv[i+1])
		if num_instances == 0:
			print("Did not input instances per patient argument (-p)")
			sys.exit()

	elif str(sys.argv[i]) == "-t":
		num_timePoints = int(sys.argv[i+1])
	elif str(sys.argv[i]) == "-nfs":
		FS = False
	elif str(sys.argv[i]) == "-recurr":
		RECURR = True
	elif str(sys.argv[i]) == "-fs":
		features_path = sys.argv[i+1]
		filename = features_path.split('/')[-1]
		startAtFS = True
	else:
		print("Wrong format. Remember header must precede argument provided.\nUse -h for help.")
		sys.exit()

num_epochs = num_instances * epochs_per_instance

# If starting at the beginning - at feature set creation
if not startAtFS:
	if data_type == '':
		print("Did not input data type. Choose from list in help documentation")
		sys.exit()
	if data_type != 'Brazil' and data_type != 'Greece' and data_type != 'newBrazil':
		print("Invalid type of data. Choose from list in help documentation")
		sys.exit()
	if not RECURR:
		if featureName == '':
			print("Did not input feature name argument (-f)")
			#sys.exit()
	if num_epochs == 0:
		print("Did not input instances per patient argument (-i)")
		#sys.exit()
	if num_timePoints == 0:
		print("Did not input time points argument (-t)\nUse -h for help.")
		sys.exit()
	if not RECURR:
		if featureName == 'ASD':
			extractFeatureFunc = extractASDFeatures
		# elif featureName == 'Wavelet':
			# extractFeatureFunc = extractWaveletFeatures
		elif featureName == 'FSL':
			extractFeatureFunc = functools.partial(createMatrixFeatureSet,extractFSLFeatures,featureName)
		elif featureName == 'Pearson':
			extractFeatureFunc = functools.partial(createMatrixFeatureSet,extractPearsonFeatures,featureName)
		else:
			print("Invalid feature name. Choose from list in help documentation")
			sys.exit()

	#feature extraction
	print("Creating Feature Set...")

	if (RECURR):
		identifier = str(num_epochs) + 'epochs_' + str(num_timePoints) + 'timepoints'
		features_path = sys.path[0] + '/FeatureSets/'+data_type+'Recurr'+identifier+'.csv'
	else:
		#unique identifier for different input parameters
		identifier = str(num_epochs) + 'epochs_' + str(num_timePoints) + 'timepoints'

	#define features and reduced_features paths
	filename = data_type+featureName+identifier+'.csv'
	features_path = sys.path[0] + '/FeatureSets/'+ filename
	reduced_features_path = sys.path[0] + '/ReducedFeatureSets/'+featureName+'features'+identifier+'_reduced.csv'
	
	#create feature set if does not exist in Feature Sets folder
	if not os.path.exists(features_path):
		print("feature file dne, making it now")
		#3rd parameter is extractFeature function of choice
		if (data_type == 'Brazil'):
			data_folder_path1 = 'BrazilRawData/HCF50'
			data_folder_path2 = 'BrazilRawData/ADF50'
			num_electrodes = 21

		if (data_type == 'Greece'):
			data_folder_path1 = '.../PathToGreeceHC_DataFolder'
			data_folder_path2 = '.../PathToGreeceMCI_DataFolder'
			num_electrodes = 8

		if (data_type == 'newBrazil'):
			data_folder_path1 = 'BrazilRawData/HCF50_new'
			data_folder_path2 = 'BrazilRawData/ADF50_new'
			num_electrodes = 21
			
		if (featureName == 'FSL' or featureName == 'Pearson'):
			extractFeatureFunc(num_instances ,num_timePoints, epochs_per_instance, data_folder_path1, data_folder_path2, data_type, RECURR)
		elif (RECURR):
			createFeatureSet(num_epochs, num_timePoints, '', '', num_electrodes, 
				data_folder_path1, data_folder_path2, data_type, RECURR)
		else:
			createFeatureSet(num_epochs, num_timePoints, featureName, extractFeatureFunc, num_electrodes, 
				data_folder_path1, data_folder_path2, data_type, RECURR)

	else:
		print("Feature set already exists")

	if (data_type == 'Brazil'):
		num_electrodes = 21
	if (data_type == 'Greece'):
		num_electrodes = 8


	#obtain global X (input features) and y (output values)

	#use existing headers made from createFeatureSet function if not FSL or Recurr
	#if (not featureName == 'FSL' and not RECURR):
	#	data = pd.read_csv(features_path)
	#otherwise assume no headers in featureset csv
	#else:
	#	data = pd.read_csv(features_path, header = None)
	
	data = pd.read_csv(features_path,header = 'infer',delimiter=',')
else: #starting pipeline with feature selection
	data = pd.read_csv(features_path, header = 'infer')

#shuffle rows of dataframe
data = shuffle(data)
data.sample(frac=1).reset_index(drop=True)
#### obtain Y using last column
y = data.iloc[:,-1].values
groups = data['patient num']
print "groups.shape :" + str(groups.shape) 
print groups
	

unique, counts = np.unique(groups, return_counts=True)
#### obtain X by dropping last and first columns (label and group number)
X = data.drop([data.columns[-1],data.columns[0]], axis=1)
# X.to_csv("fuckk.csv",index= False) 

##################################################################################

#### feature selection
print("Feature Selection...")
print("Input Shape:", X.shape)


# import feature importances plot function
from feature_ranking import get_feature_importance

#drop first patient id column made from createFSLFeatureSet function
#if (FSL):
#	X = data.drop(data.columns[0], axis=1)

##################################################################################
from pandas import read_csv
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from feature_ranking import get_feature_importance # import feature importances plot function

if (FS):
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

	# alternative feature selection from sklearn
	# Feature Importance with Extra Trees Classifier -> has feature importance 

	#  get x_reduced code from this file
	from get_XReduced import get_XReduced

	clf1 = ExtraTreesClassifier()
	clf2 = RandomForestClassifier(n_estimators=50, max_features='sqrt')
	clf3 = GradientBoostingClassifier()
	# add the classifiers to the array 
	clfs = [clf1, clf2, clf3]
	x_reduced = []

	for clf in clfs:	
		feat_importances_et = get_feature_importance(clf, X, y, 945) #top 50 features
		x_reduced.append(get_XReduced(clf, X))


##################################################################################

# learning model
print("Learning model...")
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier  
from write_accuracy_to_file import write_accuracy_to_file
#from xgboost import XGBClassifier

<<<<<<< HEAD
num_folds = 5
=======
num_folds = 10
>>>>>>> adding instance number functionality
num_seeds = 10
o_filename = 'output_pipeline.csv'

#various sklearn models
logreg = LogisticRegression() 
logreg_cv = LogisticRegressionCV()
rf = RandomForestClassifier()
gboost = GradientBoostingClassifier()
svc = SVC()
kneighbors = KNeighborsClassifier(n_neighbors=5)  
#xgboost = XGBClassifier() -> not working

#loop through models and print accuracy for each
models = [logreg, logreg_cv, rf, gboost, svc, kneighbors]
# models = [svc]
# Get and write accuracies to an output csv file
for i in range(0, len(clfs)):
	print(format(clfs[i].__class__))
	print("\n")
	for model in models:
		write_accuracy_to_file(clfs[i], model, groups, x_reduced[i], X, y, num_folds, num_seeds, o_filename, filename, featureName, data_type)

# Megha's svm
#svm_func(X_reduced,y,num_seeds, num_folds, 'output_pipeline.csv')

#nn_keras
#nn_keras(X, y, n_hlayers = 3, neurons = [100, 100, 100],learning_rate = 0.1,n_folds =2,n_classes = 2, seed = 5)

#nn_Recurr
# if (RECURR):
	# nn_Recurr(X, y, n_hlayers = 3, neurons = [100, 100, 100],learning_rate = 0.1,n_folds =2,n_classes = 2, seed = 5, 
	# 	n_electrodes = num_electrodes, n_timeSteps=num_timePoints)

