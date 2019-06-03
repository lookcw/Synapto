import numpy as np
import os
import csv
import sys
from numpy import linalg as LA

def norm(arr_in):
	x_normed = (x - x.min(0)) / x.ptp(0)
	print len(norm1)
	for i in norm1:
		if abs(i) > 1:
			print "theres an issue"
	return norm1

def zscore_file(in_file,out_file,is_header):
	f_in = open(in_file,'rb')
	reader = csv.reader(f_in,delimiter=",")
	# if (is_header):
	# 	header = next(reader)
	mat = np.array(list(reader))
	print mat
	ans = np.empty_like(mat.transpose())
	mat = mat.transpose()
	labels = mat[-1]
	mat = np.delete(mat,len(mat)-1,0)
	mat = mat.astype(np.float)
	print len(mat)
	count = 0
	for i in range(len(mat)):
		ans[i] = norm(mat[i])
		count += 1
		print count
	ans[len(mat)] = labels
	ans = ans.transpose()
	f_out = open(out_file,'wb')
	writer = csv.writer(f_out,delimiter=",")	
	# if is_header:
	# 	writer.writerow(header)
	for row in ans:
		writer.writerow(row)
		
zscore_file(sys.argv[1],sys.argv[2],False)

#zscore_file("data/erpn_1.csv","data/erpn_1_zscore_chris.csv",True)