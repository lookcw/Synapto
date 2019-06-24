import numpy as np
from scipy.signal import hilbert
from pacpy.pac import plv
import csv
import os


data_path = 'BrazilRawData/ADF50'
# data_path = 'SampleDataTesting'
filename = 'AD_50lp01.csv'
time_series = np.array(list(csv.reader(open(os.path.join(data_path, filename)))))

for electrode in range(time_series.shape[1]):
	 
	time_series_electrode = time_series[:,electrode]
	time_series_electrode = np.delete(time_series_electrode, 0)
	time_series_electrode = time_series_electrode.astype(np.float)

	t = time_series_electrode

	lo = np.sin(t * 2 * np.pi * 6) # Create low frequency carrier
	hi = np.sin(t * 2 * np.pi * 100) # Create modulated oscillation
	hi[np.angle(hilbert(lo)) > -np.pi*.5] = 0 # Clip to 1/4 of cycle

	plv(lo, hi, (4,8), (80,150)) # Calculate PAC
	print "done"