import os
import pandas as pd
import argparse
import seaborn as sns
import matplotlib.pyplot as plt 
from identifier import filenameToParam

# AVERAGE_FEATURE_SET_FOLDER = '/Users/megha/Synapto/pipeline/AverageFeatures/'

def average_features(set_averages):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="input feature file to save model for")
    args = parser.parse_args()
    in_filename = args.i
    feature_name = filenameToParam(in_filename)[0].split('/')[1]
    print(feature_name)

    if feature_name not in set_averages:

        set_averages.append(feature_name)
       
        dataset = pd.read_csv(in_filename).drop(columns=['instance code','patient num','instance num'])
        meaned = dataset.groupby(['class']).mean()
        data = meaned
        data.insert(0, "name_of_feature", feature_name)
        print(data)
        name_csv = feature_name + "_averages.csv"
        
        # name_csv = AVERAGE_FEATURE_SET_FOLDER + feature_name + "_averages.csv"
        # setting the csv file 
        data.to_csv(name_csv)

    # os.path.join(AVERAGE_FEATURE_SET_FOLDER, name_csv)

set_features = []
average_features(set_features)