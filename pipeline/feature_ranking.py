
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from dataset_functions import split_dataframe
import csv
import click
import scipy.stats
import sys

MODEL = RandomForestClassifier()

FEATURE_IMPORTANCE_FOLDER = 'FeatureImportances'

@click.command()
@click.argument('feature_filename')
def write_feature_importance(feature_filename):
	output_filename = _get_output_filename(feature_filename)
	(importances,feature_names) = get_file_featureset_importance(feature_filename)
	with open(output_filename,'w') as f:
		writer = csv.writer(f)
		writer.writerow(feature_names)
		writer.writerow(importances)
	print(output_filename)


def get_file_featureset_importance(filename):
	df = pd.read_csv(filename)
	(X,y,groups,instance_nums, columns) = split_dataframe(df)
	return _get_feature_importance(MODEL,X,y, columns)


def _get_feature_importance(clf, X, y, columns):
	clf = clf.fit(X,y)
	return (clf.feature_importances_,columns)


def _get_output_filename(feature_filepath):
	return FEATURE_IMPORTANCE_FOLDER + '/' + \
           feature_filepath.split('/')[-1] \
           .split('.')[0] + '_Importance_.csv'

def correlate_feature_importance(filename_feat1, filename_feat2):
	df_1 = pd.read_csv(filename_feat1)
	# df_2 = pd.read_csv(filename_feat2)
	print(df_1)
	feature_1 = df_1[1,:].values()
	# feature_2 = df_2.loc[0,:]
	# r = np.corrcoef(feature_1, feature_2)
	print(feature_1)
	r = "hi"
	# r = scipy.stats.pearsonr(feature_1, feature_2)[0]
	return r

if __name__ == "__main__":
	# write_feature_importance()
	# print()
	f1 = open("FeatureImportances/Hig_1.csv")
	f2 = open("FeatureImportances/DF_1.csv")
	r = correlate_feature_importance(f1, f2)
	print(r)
