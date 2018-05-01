import numpy as np
import os
import csv
import sys

def zscore(arr_in):
	norm1 = arr_in/np.linalg.norm(arr_in)
	return norm1

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
	if is_header:
		writer.writerow(header)
	for row in ans:
		writer.writerow(row)
		
zscore_file(sys.argv[1],sys.argv[2],False)

#zscore_file("data/erpn_1.csv","data/erpn_1_zscore_chris.csv",True)