from joblib import dump, load
import argparse
import pandas as pd
from dataset_functions import split_dataframe
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, GradientBoostingClassifier


clf = RandomForestClassifier()
parser = argparse.ArgumentParser()
parser.add_argument("-i", help="input feature file to save model for")
parser.add_argument("-o", help="output filename of model")
args = parser.parse_args()
in_filename = args.i
out_filename = args.o

(X, y, _, _) = split_dataframe(pd.read_csv(in_filename))

clf.fit(X,y)
dump(clf, out_filename)
