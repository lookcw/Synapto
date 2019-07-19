import numpy as np
import csv
import os
import scipy
from scipy import stats

data_path = 'FeatureSets'
filename = 'DomFreq_Brazil_1_instances_1_epochs_160000_timepoints.csv'
time_series_brazil = np.array(list(csv.reader(open(os.path.join(data_path, filename)))))
filename = 'DomFreq_AR_1_instances_1_epochs_160000_timepoints.csv'
time_series_ar = np.array(list(csv.reader(open(os.path.join(data_path, filename)))))


num_cols = time_series_brazil.shape[1]

# print "PRINTING HC TTEST VALUES"
print "HC Non AR - STD"
for col in range(3, num_cols-1):
	hc_brazil = time_series_brazil[1:22,col].astype(float)
	# hc_ar = time_series_ar[1:22,col].astype(float)
	
	# twosample_results_hc = scipy.stats.ttest_ind(hc_brazil, hc_ar)
	# print np.mean(hc_brazil)
	print np.std(hc_brazil)
	# print np.mean(hc_ar)
	# print twosample_results_hc
print "\n"

print "HC AR - STD"
for col in range(3, num_cols-1):
	# hc_brazil = time_series_brazil[1:22,col].astype(float)
	hc_ar = time_series_ar[1:22,col].astype(float)
	
	# twosample_results_hc = scipy.stats.ttest_ind(hc_brazil, hc_ar)
	# print np.mean(hc_brazil)
	# print np.mean(hc_ar)
	print np.std(hc_ar)
	# print twosample_results_hc
print "\n"

# print "PRINTING AD TTEST VALUES"
print "AD Non AR - STD"
for col in range(3, num_cols-1):
	ad_brazil = time_series_brazil[22:,col].astype(float)
	# ad_ar = time_series_ar[22:,col].astype(float)

	# twosample_results_ad = scipy.stats.ttest_ind(ad_brazil, ad_ar)
	# print np.mean(ad_brazil)
	print np.std(ad_brazil)
	# print np.mean(ad_ar)
	# print twosample_results_ad
print "\n"

print "AD AR - STD"
for col in range(3, num_cols-1):
	# ad_brazil = time_series_brazil[22:,col].astype(float)
	ad_ar = time_series_ar[22:,col].astype(float)

	# twosample_results_ad = scipy.stats.ttest_ind(ad_brazil, ad_ar)
	# print np.mean(ad_brazil)
	# print np.mean(ad_ar)
	print np.std(ad_ar)
	# print twosample_results_ad
	


	
