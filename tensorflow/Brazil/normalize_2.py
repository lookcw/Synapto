import numpy as np
import os
import csv
import sys
from numpy import linalg as LA

def zscore_file(in_file,out_file,is_header):
	f_in = open(in_file,'rb')
	reader = csv.reader(f_in,delimiter=",")
	# if (is_header):
	# 	header = next(reader)
	mat = np.array(list(reader))
	mat = mat.astype(np.float)
	x_normed = (mat - mat.min(0)) / mat.ptp(0)
	f_out = open(out_file,'wb')
	writer = csv.writer(f_out,delimiter=",")	
	# if is_header:
	# 	writer.writerow(header)
	for row in x_normed:
		writer.writerow(row)
		
zscore_file(sys.argv[1],sys.argv[2],False)

#zscore_file("data/erpn_1.csv","data/erpn_1_zscore_chris.csv",True)