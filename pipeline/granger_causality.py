import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import csv2rec
import nitime
import nitime.analysis as nta
import nitime.timeseries as ts
import nitime.utils as tsu
from nitime.viz import drawmatrix_channels

TR = 1.89
f_ub = 0.15
f_lb = 0.02

data_path = 'BrazilRawData/HCF50'
filename = 'HC_50lp01.csv'
data_rec = csv2rec(os.path.join(data_path, filename))

# names are ordered according to increasing byte offset (the .dtype.names)
roi_names = np.array(data_rec.dtype.names)
nseq = len(roi_names)
n_samples = data_rec.shape[0]
data = np.zeros((nseq, n_samples))

for n_idx, roi in enumerate(roi_names):
    data[n_idx] = data_rec[roi]


pdata = tsu.percent_change(data)
time_series = ts.TimeSeries(pdata, sampling_interval=TR)

# Creating a Granger Analyser object 
G = nta.GrangerAnalyzer(time_series, order=1)

C1 = nta.CoherenceAnalyzer(time_series)
C2 = nta.CorrelationAnalyzer(time_series)

freq_idx_G = np.where((G.frequencies > f_lb) * (G.frequencies < f_ub))[0]
freq_idx_C = np.where((C1.frequencies > f_lb) * (C1.frequencies < f_ub))[0]

coh = np.mean(C1.coherence[:, :, freq_idx_C], -1)  # Averaging on the last dimension
g1 = np.mean(G.causality_xy[:, :, freq_idx_G], -1)

fig01 = drawmatrix_channels(coh, roi_names, size=[10., 10.], color_anchor=0)
fig02 = drawmatrix_channels(C2.corrcoef, roi_names, size=[10., 10.], color_anchor=0)
plt.show()