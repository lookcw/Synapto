import os
import sys
from subprocess import call



data_dirs = ["../Data/AD_BD/","../Data/HC_BD"]
output_dir = "../Data/Brazil_FSL/" 
count = 0
for data_dir in data_dirs:
	for filename in (os.listdir(data_dir)):
		if count == 1:
			sys.exit(0)
		if "AD" in data_dir:
			label = "AD"
		else:
			label = "HC"
		file = output_dir + label + "_" + filename.split(" ")[0] + "_" + filename.split(" ")[1] + ".dat"
		#./FSL -l 1 -m 10 -p .049 -s 1 -x 100 -w 410 -i input file -o test.dat
		call(["./FSL","-l", "1", "-m", "10", "-p", "0.049", "-s", "1", "-x", "100", "-w", "410", "-i", os.path.join(data_dir,filename),"-o",file]) 