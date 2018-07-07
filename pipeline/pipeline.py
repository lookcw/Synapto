from featureSelection import feature_selection
from svm import svm_func
import os
import sys
import pandas as pd


#feature extraction
print("Feature Extraction...")

num_bunches = 1 #per patient
num_timePoints = 60 #per bunch

if os.path.exists(sys.path[0] + '/FeatureSets/ASDfeatures.csv') == False:
	createFeatureSet(num_bunches, num_timePoints)


#obtain global X (input features) and y (output values)
X = pd.read_csv(sys.path[0] + '/FeatureSets/ASDfeatures.csv', header = None)
print(X.shape)
#X.to_csv(sys.path[0] + '/FeatureSets/ASDfeatures.csv', header = False, index = False)
y = X.iloc[:,-1]
X.drop(X.columns[-1], axis=1, inplace=True)
#print(X.shape)




# feature selection
print("Feature Selection...")

feature_directory = sys.path[0] + '/FeatureSets'
reduced_directory = sys.path[0] + '/ReducedFeatureSets'
for filename in os.listdir(feature_directory):
	if filename.endswith(".csv"):
		reduced_filename = filename.split('.')[0] + "_feature_reduced.csv"
		print(reduced_filename)
		check_path = os.path.join(reduced_directory, reduced_filename)
		if (os.path.exists(check_path) == False):
			print(filename)
			path = os.path.join(feature_directory, filename)
			feature_selection(path)
		else: 
			print("file already feature reduced")
for filename in os.listdir(feature_directory):
	if filename.endswith("_feature_reduced.csv"):
		print("putting new file in feature reduced folder")
		os.rename(os.path.join(feature_directory, filename), os.path.join(reduced_directory, filename))


# learning model
print("Learning model...")

num_folds = 3
num_seeds = 3

for filename in os.listdir(reduced_directory):
	svm_func(os.path.join(reduced_directory,filename),'output.csv', num_folds, num_seeds)