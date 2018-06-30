# Features from PyRQA and Nolds - Given a time-series (time-series is the specific band given for a specific electrode and patient)
# as an input, compute nine different features for each time-series. 
from pyrqa.settings import Settings
from pyrqa.neighbourhood import FixedRadius
from pyrqa.metric import EuclideanMetric
from pyrqa.computation import RQAComputation
from pyrqa.file_reader import FileReader
import nolds
import numpy as np
import csv
import sys

#def features_func(filepath, o_filename):
def features_func(time_series_electrode):
	

	dfa = nolds.dfa(time_series_electrode)
	sampen = nolds.sampen(time_series_electrode)

	settings = Settings(time_series_electrode, embedding_dimension=3,
 	                        time_delay=1,
 	                        neighbourhood=FixedRadius(1.0),
 	                        similarity_measure=EuclideanMetric,
 	                        theiler_corrector=1,
 	                        min_diagonal_line_length=2,
 	                        min_vertical_line_length=2,
 	                        min_white_vertical_line_length=2)
	computation = RQAComputation.create(settings, verbose=False)
	result = computation.run()
	# 7 features: L_entr, L_max, L_mean, RR, DET, LAM, and TT

	return [result.entropy_diagonal_lines, result.longest_diagonal_line, 
	result.average_diagonal_line, result.recurrence_rate,
	result.determinism, result.laminarity, result.trapping_time, dfa, sampen]

if __name__ == '__main__':

	o_filename = "features.csv"
	filepath_inserted = False

	# Only write header once
	try:
		with open(o_filename, 'r+') as csvfile:
			pass
	except IOError as e:
		with open(o_filename, 'w') as csvfile:
			header = ["L_entr", "L_max", "L_mean", "RR", "DET", "LAM", "TT", "DFA", "SampE"]
			writer = csv.DictWriter(csvfile, fieldnames=header)
			writer.writeheader()

	if len(sys.argv) == 1 or len(sys.argv) % 2 == 0:
		print("Did not enter inputs in correct format. Probably missing a header.")
		sys.exit()

	for i in range(1,len(sys.argv),2):		
		if str(sys.argv[i]) == "-i":
			filepath = str(sys.argv[i+1])
			filepath_inserted = True
		else:
			print("Wrong format. Remember header must precede argument provided.")

	if(filepath_inserted is False):
		print("Input file path was not inserted. Please insert the filepath.")
		exit(0)

	#features_func(filepath, o_filename)


