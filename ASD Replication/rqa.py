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

time_series = [0.1, 0.5, 0.3, 1.7, 0.8, 2.4, 0.6, 1.2, 1.4, 2.1, 0.8]

settings = Settings(attributes[0], embedding_dimension=3,
                        time_delay=1,
                        neighbourhood=FixedRadius(1.0),
                        similarity_measure=EuclideanMetric,
                        theiler_corrector=1,
                        min_diagonal_line_length=2,
                        min_vertical_line_length=2,
                        min_white_vertical_line_length=2)

computation = RQAComputation.create(settings, verbose=False)
result = computation.run()
print(result)

