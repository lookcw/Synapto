import numpy as np
import os
import csv
import sys

def zscore(arr_in):
	ans = np.empty_like(arr_in)
	std = np.std(arr_in)
	mean = np.mean(arr_in)

	for i in range(len(arr_in)):
		ans[i] =float(arr_in[i]-mean)/std
	return ans

def zscore_file(in_file,out_file,is_header):
	f_in = open(in_file,'rb')
	reader = csv.reader(f_in,delimiter=",")
	if (is_header):
		header = next(reader)
	mat = np.array(list(reader))
	print mat
	ans = np.empty_like(mat.transpose())
	labels = mat[:,-1]
	print labels
	mat = np.delete(mat,-1,1)
	mat = mat.astype(np.float)
	mat = mat.transpose()
	print len(mat)
	for i in range(len(mat)):
		ans[i] = zscore(mat[i])
	ans[len(mat)] = labels
	ans = ans.transpose()
	f_out = open(out_file,'wb')
	writer = csv.writer(f_out,delimiter=",")	
	writer.writerow(header)
	for row in ans:
		writer.writerow(row)
zscore_file(sys.argv[1],sys.argv[2],True)
#zscore_file("data/erpn_1.csv","data/erpn_1_zscore_chris.csv",True)