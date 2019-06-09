import os
import sys
from subprocess import Popen, PIPE, call
import numpy as np
import pandas as pd
from pandas import DataFrame

# Takes in a time series in the form of raw electrode data (takes in a matrix)

elec = [0,1,2,3,4,5,6,7,8,9,15,16,17,18,19,20]

def extractPearsonFeatures(time_series_electrode):
    eegMat = pd.DataFrame(data = time_series_electrode)
#     pctChange = eegMat.pct_change()
    numElectrodes = len(eegMat.columns)
    features = [None] * (numElectrodes * (numElectrodes -1)/2)
    featuresI = 0
    for i in elec:
#     for i in range(numElectrodes):
        # for j in range(i+1,numElectrodes):
        for j in elec:
            features[featuresI] = eegMat.ix[:,i].corr(eegMat.ix[:,j])
            featuresI += 1
    return features