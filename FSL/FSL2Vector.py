import os
import csv

data_dir = "Brazil_FSL"
vec_dir = "Brazil_FSL_Features"
for filename in (os.listdir(data_dir)):
	vec = []
	reader = csv.reader(open(os.path.join(data_dir,filename),'r'),delimiter = ' ')
	writer = csv.writer(open(os.path.join(vec_dir,filename.split('.')[0]+".csv"),'w'),delimiter = ',')
	mat = list(reader)
	print len(mat)
	for i in range(len(mat)):
		for j in range(len(mat[0])):
			if j > i+1: #gets upper triangular matrix 
				vec.append(mat[i][j])
	writer.writerow(vec)


