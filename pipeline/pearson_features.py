import os
import sys
import pandas as pd
import numpy as np
from pandas import DataFrame
from headers import compareHeader, linearHeader, regionHeader
from average_heatmap import average_heatmap

import numpy

elec = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 20]


def getHeader(time_series_electrode, config_feature):
    if config_feature['compress']:
        return linearHeader(time_series_electrode)
    if config_feature['regions']:
        return regionHeader(5)
    else:
        return compareHeader(time_series_electrode)


def extractFeatures(time_series_electrode, config_feature):
    eegMat = pd.DataFrame(data=time_series_electrode)
#     pctChange = eegMat.pct_change()
    numElectrodes = len(eegMat.columns)
    corr_mat = np.zeros((numElectrodes, numElectrodes))
    for i in range(numElectrodes):
        #     for i in range(numElectrodes):
        # for j in range(i+1,numElectrodes):
        corr_mat[i][i] = 1
        for j in range(i+1, numElectrodes):
            corr = eegMat.iloc[:, i].corr(eegMat.iloc[:, j])
            corr_mat[i][j] = corr
            corr_mat[j][i] = corr
    if config_feature['compress']:
        # subtracting 2 because every electrode always has a 1 in its column
        return (np.sum(corr_mat,axis=1) - 1)/numElectrodes
    elif config_feature['regions']:
        print(corr_mat)
        region_corr_mat = average_heatmap(corr_mat)
        region_corr_mat = np.array(region_corr_mat)
        return region_corr_mat[np.triu_indices(5, 1)]
    else:
        return corr_mat[np.triu_indices(numElectrodes, 1)]

# TEMPORARY: THESE ARE THE FEATURES FOR FSL


def config_to_filename(config_feature):
    return str(config_feature)[1:-1].replace(' ','').replace('\'','')
