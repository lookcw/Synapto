import os
import sys
from subprocess import call



data_dirs = ["../Data/AD_BD_Fil/","../Data/HC_BD_Fil"]
output_dir = "Brazil_FSL/" 
count = 0
for data_dir in data_dirs:
	for filename in (os.listdir(data_dir)):
		if count == 1:
			sys.exit(0)
		if "AD" in data_dir:
			label = "AD"
		else:
			label = "HC"
		file = output_dir + label + "_" + filename.split("Fil")[0] + "_" + filename.split("Fil")[1].replace(".txt","") + ".dat"
		#./FSL -l 1 -m 10 -p .049 -s 1 -x 100 -w 410 -i input file -o test.dat
		if not os.path.exists(file):
			call(["./FSL","-l", "1", "-m", "10", "-p", "0.049", "-s", "1", "-x", "100", "-w", "410", "-i", os.path.join(data_dir,filename),"-o",file]) 