import numpy as np
from sklearn import svm
import csv


# Get file and read with csv reader
with open('../../Synapto/tensorflow/Brazil/Feature_Sets/Fil_higARmin7.csv') as f:
	reader = csv.reader(f)
	next(reader) #skip header 
	data = [r for r in reader]


# attributes stores all the attributes and value stores the respective values 
# Initializing attributes - 2D array that stores attributes belonging to each
# patient in each row 
rows = len(data)
attributes = [0] * rows
for row in range(rows):
	cols = len(data[row]) - 1
	attributes[row] = [0] * cols

# In order for the value to be read by clf.fit, change the + and - char values
# to 1 and 0, respectively
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
		

# Each entry in data has the features + value 
# for d in attributes:
# 	print(d)

attributes_1 = np.array(attributes)

clf = svm.SVC(kernel = 'rbf', C = 1.0)
clf.fit(attributes_1, value)

#ready to predict after this
