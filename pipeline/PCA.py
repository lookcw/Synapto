# Reduces features way too much
import numpy
import os
from pandas import read_csv
import pandas as pd
from sklearn.decomposition import PCA
# feature extraction

def pca(X, num_components, class_num):

    # Feaature name = Get name before the ".csv"
    feature_name = features_file.split('.')[0] 
    feature_avg_filename = feature_name + "_pca.csv"
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

        dataset = pd.read_csv(features_file)
        # dataset = pd.read_csv(features_file).drop(columns=['patient num'])
        data = dataset.loc[:,'class'].to_frame() 
        
        # Select the columns identified as the regions and average them horizontally 
        for region_name in regions:
            X = dataset.iloc[:,regions[region_name]]
            print(X.shape)

            pca = PCA(n_components=num_components)
            fit = pca.fit(X)
            X_reduced = fit.transform(X)
            data[region_name] = X_reduced

            # summarize components
            # print("Explained Variance: %s") % fit.explained_variance_ratio_
            # feature_red_name = format(fit)
            # print(fit.components_)
        
        data.to_csv(feature_avg_filename, index=False)
    else:
        print("File for the regionalized averages already exists!")


if __name__ == "__main__":
    # features_file = sys.argv[1]
    num_components = 1
    features_file = "FeatureSets/DomFreq-_Brazil_1_instances_1602_epochs_1_timepoints_{}.csv"
    pca(features_file, num_components)
    
