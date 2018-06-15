# Features from PyRQA
from pyrqa.settings import Settings
from pyrqa.neighbourhood import FixedRadius
from pyrqa.metric import EuclideanMetric
from pyrqa.computation import RQAComputation
from pyrqa.file_reader import FileReader
import csv


with open("../../../Synapto/tensorflow/Brazil/Feature_Sets/Fil_higARmin7.csv") as f:
		reader = csv.reader(f)
		next(reader) #skip header 
		data = [r for r in reader] #Place all data in data array 

rows = len(data)
attributes = [0] * rows
for row in range(rows):
	cols = len(data[row]) - 1
	attributes[row] = [0] * cols

value_char = []
value = []

# Adding attributes to attribute 2D array and corresponding values to value 1D array 
for row in range(rows):
	cols = len(data[row])
	for col in range(cols):
		if col == cols - 1:
			value_char = data[row][col]
			if value_char == '+':
				value.append(1)
			else:
				value.append(0)
		else:
			attributes[row][col] = float(data[row][col])

# This gets the first column of the csv file (how do you get all the columns)
time_series = FileReader.file_as_float_array('../../../Synapto/tensorflow/Brazil/Feature_Sets/Fil_higARmin7.csv',
	delimiter=',', column = 0, offset = 1)

# Note: attributes has the rows (where as here time-series has the columns)
settings = Settings(attributes, embedding_dimension=3,
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

with open("features_rqa.csv", 'a') as f:
		writer = csv.writer(f)
		writer.writerow(["L_entr", "L_max", "L_mean", "RR", "DET", "LAM", "TT"])
		writer.writerow([result.entropy_diagonal_lines, result.longest_diagonal_line, 
			result.average_diagonal_line, result.recurrence_rate,
			result.determinism, result.laminarity, result.trapping_time])


