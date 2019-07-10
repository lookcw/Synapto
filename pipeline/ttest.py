import numpy as np
import csv
import os
import scipy
from scipy import stats

data_path = 'FeatureSets'
filename = 'DomFreq_Brazil_1_instances_1_epochs_16000_timepoints.csv'
time_series_brazil = np.array(list(csv.reader(open(os.path.join(data_path, filename)))))
filename = 'DomFreq_AR_1_instances_1_epochs_16000_timepoints.csv'
time_series_ar = np.array(list(csv.reader(open(os.path.join(data_path, filename)))))


num_cols = time_series_brazil.shape[1]

for col in range(2, num_cols-1):
	hc_brazil = time_series_brazil[1:13,col].astype(float)
	hc_ar = time_series_ar[1:13,col].astype(float)
	
	ad_brazil = time_series_brazil[13:,col].astype(float)
	ad_ar = time_series_ar[13:,col].astype(float)

	twosample_results_hc = scipy.stats.ttest_ind(hc_brazil, hc_ar)
	twosample_results_ad = scipy.stats.ttest_ind(ad_brazil, ad_ar)
	
	print twosample_results_hc
	print twosample_results_ad

	


	
