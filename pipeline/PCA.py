# Reduces features way too much
import numpy
import os
from pandas import read_csv
import pandas as pd
from sklearn.decomposition import PCA
import sys

def pca(folder_name, features_file, num_components, class_num):
  
    # Feaature name = Get name before the ".csv"
    # feature_name = features_file.split('.')[0]
    # print(feature_name)
    # feature = feature_name.split('/')[1]
    # root = feature_name.split('/')[0]
    # print(root)

    # feature_pca_folder = root + "_pca/"
    # feature_avg_filename = feature_pca_folder + feature + "_pca.csv"
    # print(feature_avg_filename)

    # if not os.path.exists(feature_pca_folder):
    #     os.makedirs(feature_pca_folder)

    # Feaature name = Get name before the ".csv"
    feature_name = features_file.split('.')[0]
    folder_pca = folder_name + "_pca/"
    original_file = folder_name + "/" + features_file
    feature_avg_filename = folder_pca + feature_name + "_pca.csv"

    print(feature_avg_filename)

    if not os.path.exists(folder_pca):
        os.makedirs(folder_pca)

    # Electrodes corresponding to regions
    regions = {
        "Anterior": [0,1,2,4,6],
        "Temporal/Left": [3,8,13],
        "Central": [5,9,10,11,15],
        "Temporal/Right": [7,12,17],
        "Posterior": [14,16,18,19,20]
    }

    if not os.path.exists(feature_avg_filename):

        dataset = pd.read_csv(original_file)
        # dataset = pd.read_csv(features_file).drop(columns=['patient num'])
        # data = dataset.iloc[:, 0].to_frame() 
        numCols = len(regions)
        numRows = len(dataset)
        data = pd.DataFrame(index=range(numRows))

        # Select the columns identified as the regions and average them horizontally 
        for region_name in regions:
            X = dataset.iloc[:,regions[region_name]]

            pca = PCA(n_components=num_components)
            fit = pca.fit(X)
            X_reduced = fit.transform(X)
            print(X_reduced.shape)
            # data['class'] = class_num
            data[region_name] = X_reduced

            # summarize components
            # print("Explained Variance: %s") % fit.explained_variance_ratio_
            # feature_red_name = format(fit)
            # print(fit.components_)
        
        data.to_csv(feature_avg_filename, index=False)
    else:
        print("File for the regionalized averages already exists!")


if __name__ == "__main__":
    
    # TO RUN: python PCA.py folder_name 
    # This will iterate through all the files in a given folder 

    # If you do NOT want to iterate through all the filenames in a folder, need to do 
    # a separate command that only takes in a filename 
    num_components = 1
    class_num = 0
    folder_name = sys.argv[1]
    
    for filename in os.listdir(folder_name):
        if filename.endswith(".csv"):
            pca(folder_name, filename, num_components, class_num)
    
