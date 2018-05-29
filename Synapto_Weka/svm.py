import numpy as np
from sklearn import svm
from sklearn.model_selection import *
from sklearn.metrics import accuracy_score
import csv
import sys


def svm_func():
	
	# Get file and read with csv reader
	with open("../../../Synapto/tensorflow/Brazil/Feature_Sets/Fil_higARmin7.csv") as f:
		reader = csv.reader(f)
		next(reader) #skip header 
		data = [r for r in reader] #Place all data in data array 


	# attributes stores all the attributes and value stores the respective values (0 ir 1)
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
			

	X = np.array(attributes)
	y = np.array(value)

	# For leave one out, number of splits is 25 - can change this number if different number of folds is needed
	kf = KFold(n_splits=25)

	# Radial basis function
	clf = svm.SVC(kernel = 'rbf', C = 1.0)

	scores = []

	for train, test in kf.split(X):
		print("%s %s" % (train, test))
		X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]
		clf.fit(X[train], y[train])
		print('Prediction:', clf.predict(X_test))
		y_pred = clf.predict(X_test)
		print(accuracy_score(y_test, y_pred))
		scores.append(accuracy_score(y_test, y_pred))

	scores = np.array(scores)
	print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


if __name__ == '__main__':

	svm_func()

# 	if len(sys.argv) == 1 or len(sys.argv) % 2 == 0:
# 		print("Did not enter inputs in correct format. Probably missing a header.")
# 		sys.exit()

# 	if str(sys.argv[1]) == "-i":
# 		filepath = str(sys.argv[2])
# 		svm_func(filepath)
# 		print("Worked")
# 	else:
# 		print("Wrong format. Remember header must precede argument provided.")







