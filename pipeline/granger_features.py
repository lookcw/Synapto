import os
import sys
from subprocess import Popen, PIPE, call
import numpy as np
import matplotlib.pyplot as plt
import nitime
import nitime.analysis as nta
import nitime.timeseries as ts
import nitime.utils as tsu
from nitime.viz import drawmatrix_channels
import csv
import pandas as pd
from pandas import DataFrame
from headers import compareHeader
# Takes in a time series in the form of raw electrode data (one column)

def getHeader(time_series_electrode):
	return compareHeader(time_series_electrode)

def extractFeatures(time_series, config_feature):

	print(time_series.shape)
	TR = 1/256.0
	f_ub = 30
	f_lb = 0.5

	# normalize data to be in terms of percent change
	pdata = tsu.percent_change(time_series.transpose())
	time_series_g = ts.TimeSeries(pdata, sampling_interval=T)

	# Creating a Granger Analyser object 
	G = nta.GrangerAnalyzer(time_series_g, order=1)
	C1 = nta.CoherenceAnalyzer(time_series_g)
	C2 = nta.CorrelationAnalyzer(time_series_g)

	freq_idx_G = np.where((G.frequencies > f_lb) * (G.frequencies < f_ub))[0]
	freq_idx_C = np.where((C1.frequencies > f_lb) * (C1.frequencies < f_ub))[0]

	coh = np.mean(C1.coherence[:, :, freq_idx_C], -1)  # Averaging on the last dimension
	g1 = np.mean(G.causality_xy[:, :, freq_idx_G], -1)

	# print(g1.shape)
	# print(len(g1))

	# place feature values in matrix and return the linearlized form of it
	numElectrodes = time_series.shape[1]
	features = [None] * 210
	# features = [None] * (numElectrodes * (numElectrodes -1)/2).astype(np.int)
	featuresI = 0

	# Prints out None if the you're comparing 1 and 1 
	# print(g1)
	for i in range(len(g1)):
		features[featuresI] = coh[i][i]
	# print(features)

	for i in range(len(g1)):
		for j in range(i+1, len(g1)):
			features[featuresI] = g1[i][j]
			featuresI += 1

	# roi_names = ['electrode1','electrode2','electrode3','electrode4','electrode5','electrode6','electrode7','electrode8','electrode9','electrode10','electrode11','electrode12','electrode13','electrode14','electrode15','electrode16','electrode17','electrode18','electrode19','electrode20','electrode21']
	# fig01 = drawmatrix_channels(g1, roi_names, size=[10., 10.], color_anchor=0)
	# plt.show()

	return features

# TEMPORARY: THESE ARE THE FEATURES FOR FSL
def config_to_filename(config_feature):
    return ''