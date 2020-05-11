import os
import sys
import pandas as pd
import argparse
import matplotlib.pyplot as plt 
from identifier import filenameToParam

# Takes in a set which contains names of files (feature averages that already exist)
def regionalize_average_features(features_file):
    
    # Feaature name = Get name before the ".csv"
    feature_name = features_file.split('.')[0] 
    feature_avg_filename = feature_name + "_regionalized.csv"
    print(feature_avg_filename)

    # Electrodes corresponding to regions
    regions = {
        "Anterior": [0,1,2,4,6],
        "Temporal/Left": [3,8,13],
        "Central": [5,9,10,11,15],
        "Temporal/Right": [7,12,17],
        "Posterior": [14,16,18,19,20]
    }

    if not os.path.exists(feature_avg_filename):

        dataset = pd.read_csv(features_file).drop(columns=['instance code','patient num','instance num'])
        # dataset = pd.read_csv(features_file).drop(columns=['patient num'])
        data = dataset.loc[:,'class'].to_frame() 
        print(type(data))
        # data.insert(0, "name_of_feature", feature_name) #Can add in feature names as a column if necessary
        
        # Select the columns identified as the regions and average them horizontally 
        for region_name in regions:
            data[region_name] = dataset.iloc[:,regions[region_name]].mean(axis=1)
        
        data.to_csv(feature_avg_filename, index=False)
    else:
        print("File for the regionalized averages already exists!")

if __name__ == "__main__":
    features_file = sys.argv[1]
    regionalize_average_features(features_file)

    # Example of what features_file can equal
    # features_file = "FeatureSets/DomFreq-_Brazil_1_instances_1602_epochs_1_timepoints_{}.csv"