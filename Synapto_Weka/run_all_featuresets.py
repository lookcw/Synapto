import os
import sys
from subprocess import call
import csv

data_dir = "../Feature_Sets/"
data_dirs = os.listdir(data_dir)
output_file = "output.csv"


results = list(csv.reader(open(output_file,'r'),delimiter = ','))

done_files = set([])

for result in results:
	done_files.add(result[1])




count = 0
for dir in data_dirs:
	for filename in os.listdir(os.path.join(data_dir,dir)):
		if filename.split("/")[-1].split(".")[0] not in done_files:
			infile= os.path.join(data_dir+dir,filename)
			print infile
			# print "java -jar OpenCSVWriter.jar -i ", infile," -o ", output_file
			call(["java", "-jar", "OpenCSVWriter.jar", "-i", infile,"-o", output_file]) 