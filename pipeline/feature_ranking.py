
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from dataset_functions import split_dataframe
import csv
import click

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


if __name__ == "__main__":
	write_feature_importance()
	print()
