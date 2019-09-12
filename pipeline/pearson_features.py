import os
import sys
from subprocess import Popen, PIPE, call
import numpy as np
import pandas as pd
from pandas import DataFrame
from headers import compareHeader

elec = [0,1,2,3,4,5,6,7,8,9,15,16,17,18,19,20]

def getHeader(time_series_electrode):
   return compareHeader(time_series_electrode)
   

def extractFeatures(time_series_electrode, config_feature):
    eegMat = pd.DataFrame(data = time_series_electrode)
#     pctChange = eegMat.pct_change()
    numElectrodes = len(eegMat.columns)
    features = [None] * int(numElectrodes * (numElectrodes -1)/2)
    featuresI = 0
    for i in range(numElectrodes):
#     for i in range(numElectrodes):
        # for j in range(i+1,numElectrodes):
        for j in range(i+1,numElectrodes):
            features[featuresI] = eegMat.ix[:,i].corr(eegMat.ix[:,j])
            featuresI += 1
    return features

# TEMPORARY: THESE ARE THE FEATURES FOR FSL
def config_to_filename(config_feature):
    if 'bands_func' in config_feature:
        return config_feature['bands_func'] + "_band_" + str(config_feature['l']) + "_l_" + str(config_feature['m']) + "_m_" + str(config_feature['p']) + '_p_' + str(config_feature['s']) + '_s_' + str(config_feature['x']) + '_x_' + str(config_feature['w']) + '_w_.csv'
    else:
        return str(config_feature['l']) + "_l_" + str(config_feature['m']) + "_m_" + str(config_feature['p']) + '_p_' + str(config_feature['s']) + '_s_' + str(config_feature['x']) + '_x_' + str(config_feature['w']) + '_w_.csv'