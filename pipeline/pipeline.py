from featureSelection import reduce_features
from svm import svm_func
import os
import sys
import pandas as pd
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

X_reduced = reduce_features(X,y)
X_reduced = pd.DataFrame(X_reduced)

#combine X_reduced and y and output reduced csv file if does not exist
#append them with axis=1
data_reduced = pd.concat([X_reduced, y], axis=1)
print(data_reduced.shape)
if os.path.exists(reduced_features_path) == False:
	data_reduced.to_csv(reduced_features_path)

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


# learning model
print("Learning model...")

num_folds = 3
num_seeds = 3

svm_func(os.path.join(reduced_directory,filename),'output.csv', num_folds, num_seeds)

