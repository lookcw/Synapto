import numpy as np
from scipy.signal import hilbert
import sys
sys.path.append('pacpy/pacpy')
from pacpy.pac import plv, mi_tort, mi_canolty, glm, ozkurt
from BandPass1 import band_pass, runB, runG
import csv
import os

def getHeader(time_series_electrode):
    header = []
    num_cols = time_series_electrode.shape[1]
    for i in range(1,num_cols + 1):
        header.append("plv_"+str(i))
        header.append("mi_tort_"+str(i))
        header.append("glm_"+str(i))
        header.append("ozkurt_"+str(i))
    return header

def extractFeatures(time_series_electrodes):
    feature = []
    for column in time_series_electrodes.T:
        feature += __extractFeatures(column)
    return feature

def __extractFeatures(time_series):
    lo = runB(time_series)
    hi = runG(time_series)
    return[
        plv(lo, hi, (4,8), (80,120), fs=250),
        mi_tort(lo, hi, (4,8), (80,150), fs=250),
        glm(lo, hi, (4,8), (80,150), fs=250),
        ozkurt(lo, hi, (4,8), (80,150), fs=250)]
