import os
import sys
from subprocess import call
import csv

data_dirs = os.listdir("../Feature_Sets/")
output_file = "output.csv"


results = list(csv.reader(open(output_file,'r'),delimiter = ','))

done_files = set([])

for result in results:
	done_files.add(result[1])




count = 0
for dir in data_dirs:
	for filename in os.listdir(os.path.join("../Feature_Sets",dir)):
		if filename.split("/")[-1].split(".")[0] not in done_files:
			print filename
			call(["java -jar OpenCSVWriter.jar -i ", filename," -o ", output_file]) 
