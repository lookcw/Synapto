import numpy as np
import csv
import os
import scipy
from scipy import stats

data_path = 'SampleDataTesting'
filename = 'Averages.csv'
time_series = np.array(list(csv.reader(open(os.path.join(data_path, filename)))))

y1 = scipy.stats.norm.pdf(time_series)
print y1

for col in range(time_series.shape[1]):
	a = time_series[0][col]
	b = time_series[1][col]



	
