import os
import sys
from subprocess import call



data_dirs = ["../Data/AD/","../Data/HC/"]
output_dir = "Brazil_FSL/"
bands = ["Alpha","Theta","Gamma","Beta","Delta"]
count = 0
for data_dir in data_dirs:
	for band in bands:
		for filename in (os.listdir(os.path.join(data_dir,band))):
			if count == 1:
				sys.exit(0)
			if "AD" in data_dir:
				label = "AD"
			else:
				label = "HC"
			file = os.path.join(output_dir,band) + "/" + filename.replace(".csv","") + ".dat"
			#./FSL -l 1 -m 10 -p .049 -s 1 -x 100 -w 410 -i input file -o test.dat
			if not os.path.exists(file):
				call(["./FSL","-l", "1", "-m", "10", "-p", "0.049", "-s", "1", "-x", "100", "-w", "410", "-i", os.path.join(data_dir + "/" + band,filename),"-o",file]) 