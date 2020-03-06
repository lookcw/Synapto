import os
import sys
import pandas as pd
from pandas import DataFrame
from headers import compareHeader
import numpy

elec = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 20]


def getHeader(time_series_electrode):
    return compareHeader(time_series_electrode)


def extractFeatures(time_series_electrode, config_feature):
    eegMat = pd.DataFrame(data=time_series_electrode)
    numpy.savetxt("pearson_example.csv", eegMat, delimiter=",")
#     pctChange = eegMat.pct_change()
    numElectrodes = len(eegMat.columns)
    features = [None] * int(numElectrodes * (numElectrodes - 1)/2)
    featuresI = 0
    for i in range(numElectrodes):
        #     for i in range(numElectrodes):
        # for j in range(i+1,numElectrodes):
        for j in range(i+1, numElectrodes):
            features[featuresI] = eegMat.iloc[:, i].corr(eegMat.iloc[:, j])
            featuresI += 1
    return features

# TEMPORARY: THESE ARE THE FEATURES FOR FSL


def config_to_filename(config_feature):
    return ''
