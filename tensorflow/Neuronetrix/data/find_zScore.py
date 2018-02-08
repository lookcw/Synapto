import numpy as np
import os
import csv

def zscore(arr_in):
	ans = np.empty_like(arr_in)
	std = np.std(arr_in)
	mean = np.mean(arr_in)
	for i in arr_in:
		ans.append(float(i-mean)/std)
	return ans

def zscore_file(in_file,out_file,is_header):
	f_in = open(in_file,'rb')
	reader = csv_reader(f_in,delimiter=",")
	if (is_header):
		header = reader.readline()
	mat = np.array(reader.read_lines())
	mat = mat.transpose()
	ans = np.empty_like(mat)
	for line in mat:
		ans.append(zscore(line))
	ans = ans.transpose()
	f_out = open(out_file,'wb')
	writer = csv_writer(f_out,delimiter=",")	
	writer.writerow(header)
	for row in ans:
		writer.writerow(row)

zscore_file("../data/erpn_1.csv","../data/erpn_1_zscore_chris.csv",True)