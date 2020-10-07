import os
import sys
import pandas as pd
import argparse
# import seaborn as sns
import matplotlib.pyplot as plt 
from identifier import filenameToParam

# Takes in a set which contains names of files (feature averages that already exist)
def average_features(features_file):
    
    # Feaature name = Get name before the ".csv"
    feature_name = features_file.split('.')[0] 
    feature_avg_filename = feature_name + "_averages.csv"
    print(feature_avg_filename)

    # if feature_avg_filename not in set_averages:
    if not os.path.exists(feature_avg_filename):
        # set_averages.append(feature_avg_filename)

        dataset = pd.read_csv(features_file).drop(columns=['instance code','patient num','instance num'], errors='ignore')
        meaned = dataset.groupby(['class']).mean()
        data = meaned
        data.insert(0, "name_of_feature", feature_name)
        print(data)

        data.to_csv(feature_avg_filename)
    else:
        print("File for those feature averages already exists!")

if __name__ == "__main__":
    # set_averages = []
    features_file = sys.argv[1]
    average_features(features_file)
