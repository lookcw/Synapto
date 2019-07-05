import numpy as np
from scipy.signal import hilbert
from pacpy.pac import plv
from pacpy.pac import mi_tort
import csv
import os


# data_path = 'BrazilRawData/ADF50'
# # data_path = 'SampleDataTesting'
# filename = 'AD_50lp01.csv'
# time_series = np.array(list(csv.reader(open(os.path.join(data_path, filename)))))

# for electrode in range(time_series.shape[1]):
	 
# 	time_series_electrode = time_series[:,electrode]
# 	time_series_electrode = np.delete(time_series_electrode, 0)
# 	time_series_electrode = time_series_electrode.astype(np.float)

# 	t = time_series_electrode

# 	lo = np.sin(t * 2 * np.pi * 6) # Create low frequency carrier
# 	hi = np.sin(t * 2 * np.pi * 100) # Create modulated oscillation
# 	hi[np.angle(hilbert(lo)) > -np.pi*.5] = 0 # Clip to 1/4 of cycle

# 	plv(lo, hi, (4,8), (80,150)) # Calculate PAC
# 	print "done"

# import numpy as np
# from scipy.signal import hilbert
# from pacpy.pac import plv

t = np.arange(0, 10, .001) # Define time array
lo = np.sin(t * 2 * np.pi * 6) # Create low frequency carrier
hi = np.sin(t * 2 * np.pi * 100) # Create modulated oscillation
hi[np.angle(hilbert(lo)) > -np.pi*.5] = 0 # Clip to 1/4 of cycle

# plv(t, hi, (13,50), (30,150)) # Calculate PAC
Nbins=20
phadeg = np.degrees(lo)

binsize = 360 / Nbins
phase_lo = np.arange(-180, 180, binsize)
mean_amp = np.zeros(len(phase_lo))
for b in range(len(phase_lo)):
    phaserange = np.logical_and(phadeg >= phase_lo[b],
                                phadeg < (phase_lo[b] + binsize))
    mean_amp[b] = np.mean(hi[phaserange])

p_j = np.zeros(len(phase_lo))
for b in range(len(phase_lo)):
    p_j[b] = mean_amp[b] / sum(mean_amp)

h = -np.sum(p_j * np.log10(p_j))
h_max = np.log10(Nbins)
pac = (h_max - h) / h_max

