import pandas as pd
import argparse
import seaborn as sns
import matplotlib.pyplot as plt 
from identifier import filenameToParam

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="input feature file to save model for")
args = parser.parse_args()
in_filename = args.i
feature_name = filenameToParam(in_filename)[0].split('/')[1]
print(feature_name)

dataset = pd.read_csv(in_filename).drop(columns=['instance code','patient num','instance num'])
meaned = dataset.groupby(['class']).mean()
data = meaned
data.insert(1, "name_of_feature", feature_name)
print(data)
data.to_csv('averages.csv')

