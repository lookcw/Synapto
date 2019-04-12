import numpy as np
import pywt
from pywt import wavedec

def extractWaveletFeatures(x):

	# Input variable: one patient one electrode vector
	[cA, cD] = wavedec(x, 'db4', level=1)


	mean = np.mean(abs(cA))

	std = np.std(cA)

	avgpwr = np.sum(cA**2)

	features1 = np.append(mean,std)
	features = np.append(features1,avgpwr)

	return features