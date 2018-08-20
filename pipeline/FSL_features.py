import os
import sys
from subprocess import Popen, PIPE
import numpy as np


def extractASDFeatures(time_series_electrode):
	p = Popen(["optirun","./FSL","-l", "1", "-m", "10", "-p", "0.049", "-s", "1", "-x", "100", "-w", "410"]
		, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate(input=time_series_electrodes)
	mat = [s.strip().split(' ') for s in output.strip().split('\n')]
	print mat
	vec = []
	for i in range(len(mat)):
		for j in range(len(mat[0])):
			if j > i+1: #gets upper triangular matrix 
				vec.append(mat[i][j])
		print  map(float,vec)
