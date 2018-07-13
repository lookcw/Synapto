import numpy as np
from sklearn import svm
from sklearn.model_selection import *
from sklearn.metrics import accuracy_score
import csv
import sys
from decimal import Decimal
import time
import random
from featureSetEdit import remove_plus_min


def svm_func(X, y, seeds, folds, o_filename):
	# print(filepath)
	# print("Number folds: ", folds)
	# # Get file and read with csv reader
	# with open(filepath) as f:
	# 	reader = csv.reader(f)
	# 	next(reader) #skip header 
	# 	data = [r for r in reader] #Place all data in data array 

	# # Using common function that will remove +/- 
	# value, attributes = remove_plus_min(data)

	# X = np.array(attributes)
	# y = np.array(value)

	accuracies = 0

	for seed in range(0, seeds, 1):
		print("Seed number: ", seed)
		r1 = random.Random(seed)

		# For leave one out, number of splits is 25 - can change this number if different number of folds is needed
		kf = KFold(n_splits=folds, shuffle = True, random_state = int(r1.random()*100))

		# Radial basis function
		clf = svm.SVC(kernel = 'rbf', C = 1.0)

		scores = []

		for train, test in kf.split(X):
			#print("%s %s" % (train, test))
			X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]
			clf.fit(X_train, y_train)
			y_pred = clf.predict(X_test) # Predict on test set - store in y_pred
			#print('Prediction:', y_pred) 
			#print("Actual: ", y_test)	
			#print(accuracy_score(y_test, y_pred)) # Get accuracy by comparing prediction to actual 
			scores.append(accuracy_score(y_test, y_pred))

		scores = np.array(scores)
		#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

		accuracy = round(scores.mean(),2)
		accuracies += accuracy

	final_accuracy = accuracies/seeds
	print(final_accuracy)
	# Write to output file
	with open(o_filename, 'a') as f:
		writer = csv.writer(f)
		writer.writerow([time.strftime("%m/%d/%Y"), final_accuracy, folds, seeds])

	
if __name__ == '__main__':

	o_filename = "output.csv"
	num_folds = 10
	num_seeds = 10
	filepath_inserted = False

	# Only write header once
	try:
		with open(o_filename, 'r+') as csvfile:
			pass
	except IOError as e:
		with open(o_filename, 'w') as csvfile:
			header = ['Date', 'Filepath', 'Accuracy', 'Num Folds', 'Num Seeds']
			writer = csv.DictWriter(csvfile, fieldnames=header)
			writer.writeheader()

	if len(sys.argv) == 1 or len(sys.argv) % 2 == 0:
		print("Did not enter inputs in correct format. Probably missing a header.")
		sys.exit()

	for i in range(1,len(sys.argv),2):		
		if str(sys.argv[i]) == "-i":
			filepath = str(sys.argv[i+1])
			filepath_inserted = True
		elif str(sys.argv[i]) == "-o":
			o_filename = sys.argv[i+1]
		elif str(sys.argv[i]) == "-f":
			num_folds = int(sys.argv[i+1])
		elif str(sys.argv[i]) == "-s":
			num_seeds = int(sys.argv[i+1])
		else:
			print("Wrong format. Remember header must precede argument provided.")

	if(filepath_inserted is False):
		print("Input file path was not inserted. Please insert the filepath.")
		exit(0)

	print(filepath)
	print("Number folds: ", folds)
	#Get file and read with csv reader
	with open(filepath) as f:
		reader = csv.reader(f)
		next(reader) #skip header 
		data = [r for r in reader] #Place all data in data array 

	# Using common function that will remove +/- 
	value, attributes = remove_plus_min(data)

	X = np.array(attributes)
	y = np.array(value)

	#svm_func(X, y)


