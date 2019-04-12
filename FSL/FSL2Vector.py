import os
import csv

data_dir = "Brazil_FSL"
vec_dir = "Brazil_FSL_Features"
for dir_name in (os.listdir(data_dir)):
	for filename in (os.listdir(os.path.join(data_dir,dir_name))):
		vec = []
		file = os.path.join(vec_dir + "/" +  dir_name ,filename.split('.')[0]+".csv")
		if not os.path.exists(os.path.dirname(file)):
			try:
				os.makedirs(os.path.dirname(file))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
		reader = csv.reader(open(os.path.join( data_dir + "/" + dir_name  ,filename),'r'),delimiter = ' ')
		writer = csv.writer(open(file,'w'),delimiter = ',')
		mat = list(reader)
		print len(mat)
		for i in range(len(mat)):
			for j in range(len(mat[0])):
				if j > i+1: #gets upper triangular matrix 
					vec.append(mat[i][j])
		writer.writerow(vec)


