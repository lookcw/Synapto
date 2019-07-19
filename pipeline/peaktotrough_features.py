#python packages
import numpy as np
import scipy as sp
import csv
import os
import matplotlib.pyplot as plt
import peakutils
import pandas as pd
# import pac
# import seaborn as sns
# sns.set_style('white')
# import imp
# import shape
# import utils
# imp.reload(utils)

def extractSteepnessFeatures(time_series):
    
    widthS = 3
    Fs = 250.0
    S = 13
    Sc = 12
    flo = (13,30)
    fhi = (50, 150)

    ts = pd.DataFrame(time_series) #convert to pd dataframe to get each electrode (column)
    
    for col in ts:
        
        electrode = ts[col]
        print electrode

        peaks = peakutils.peak.indexes(np.array(electrode)) #get peaks
        troughs = peakutils.peak.indexes(np.array([-1*x for x in electrode])) #get troughs

        print peaks

data_path = 'BrazilRawData/ADF50'
filename = 'AD_50lp01.csv'
time_series = np.array(list(csv.reader(open(os.path.join(data_path, filename)))))
extractSteepnessFeatures(time_series)