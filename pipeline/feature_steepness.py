###Steepness Ratio

import numpy as np
import scipy.signal
import peakutils
import matplotlib.pyplot as plt
import pandas as pd

def extractSteepnessFeatures(time_series_electrode):
    ts_electrode = pd.DataFrame(time_series_electrode) #convert to pd dataframe to get each electrode (column)
    steepness_array = [] #array with each electrodes' steepness ratio (total of 21 values)
    for col in ts_electrode:
        electrode_arr = ts_electrode[col] #array of one electrode

        peaks = peakutils.peak.indexes(np.array(electrode_arr)) #get peaks
        troughs = peakutils.peak.indexes(np.array([-1*x for x in electrode_arr])) #get troughs
        extremes = [x for x in peaks] + [x for x in troughs]
        extremes.sort() #combine peaks and troughs then sort. peaks and troughs will alternate (can't have two peaks in a row)
        
        slopes = []
        for i in range(len(extremes)-1):
            cut  = [electrode_arr[x] for x in range(extremes[i], extremes[i+1]+1)]  #get x values for a cut between a peak and trough or trough and peak
            max_slope = abs(max([x - z for x, z in zip(cut[:-1], cut[1:])])) #calculate slope between each combo values in cut
            slopes.append(max_slope) 

        if peaks[0] < troughs[0]: #if a peak comes first, the first slope is a decay
            #slopes will alternate between decay (trough to peak) and rise (peak to trough)
            decay = np.array([slopes[x] for x in range (0, len(slopes), 2)])
            rise = np.array([slopes[x] for x in range (1, len(slopes), 2)])
        elif peaks[0] > troughs[0]: #if a peak comes first, the first slope is a rise
            #slopes will alternate between rise and decay
            rise = np.array([slopes[x] for x in range (0, len(slopes), 2)])
            decay = np.array([slopes[x] for x in range (1, len(slopes), 2)])
        else:
            print("steepness_ratio error")

        steepness_ratio = decay.mean() / rise.mean()
        steepness_array.append(steepness_ratio)
    return steepness_array

