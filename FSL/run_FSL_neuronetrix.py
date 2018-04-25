import os
import sys
from subprocess import call



data_dirs = os.listdir("../Data/")
output_dir = "Brazil_FSL/"

# bands = [""]
count = 0
for data_dir in data_dirs:
	dirs = os.listdir(os.path.join("../Data",data_dir))
	for filename in dirs:
		if count == 1:
			sys.exit(0)
		if "AD" in data_dir:
			label = "AD"
		else:
			label = "HC"

		file = os.path.join(output_dir,data_dir) + "/" + filename.replace(".csv","") + ".dat"
		if not os.path.exists(os.path.dirname(file)):
			try:
				os.makedirs(os.path.dirname(file))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					print "exiting python program now"
					raise
		#./FSL -l 1 -m 10 -p .049 -s 1 -x 100 -w 410 -i input file -o test.dat
		if not os.path.exists(file):
			call(["./FSL","-l", "1", "-m", "10", "-p", "0.049", "-s", "1", "-x", "100", "-w", "410", "-i", os.path.join("../Data/"+ data_dir,filename),"-o",file]) 