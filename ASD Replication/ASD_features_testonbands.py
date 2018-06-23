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


# This gets the first column of the csv file 

def features_func(filepath, o_filename):
	for i in range(0,21):
		time_series_electrode = FileReader.file_as_float_array(filepath,
			delimiter=',', column = i, offset = 0)
		print time_series_electrode
		
		# takes extremely long to run 
		dfa = nolds.dfa(time_series_electrode)
		sampen = nolds.sampen(time_series_electrode)
		print 'dfa', dfa
		print 'sampen', sampen

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
		print 'L_entr:', result.entropy_diagonal_lines
		print 'L_max:', result.longest_diagonal_line
		print 'L_mean:', result.average_diagonal_line
		print 'RR:', result.recurrence_rate
		print "DET:", result.determinism
		print "LAM:", result.laminarity
		print "TT:", result.trapping_time

	

		with open(o_filename, 'a') as f:
			writer = csv.writer(f)
			writer.writerow([result.entropy_diagonal_lines, result.longest_diagonal_line, 
				result.average_diagonal_line, result.recurrence_rate,
				result.determinism, result.laminarity, result.trapping_time, dfa, sampen])

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

	features_func(filepath, o_filename)


