import os
import sys
import csv

data_dir = "Brazil_FSL/"
for filename in (os.listdir(data_dir)):
	f = open(os.path.join(data_dir,filename),'r')
	reader = csv.reader(f,delimiter = ' ')
	