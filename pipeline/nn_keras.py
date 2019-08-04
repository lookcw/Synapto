import tensorflow as tf
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
import csv
import os
import math
import six
import sys
import datetime
import sys
#from compute_score import compute_group_score
from keras.wrappers.scikit_learn import KerasClassifier
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' #hide warnings
print("starting")
# Network Parameters

from numpy.random import seed
seed(1)
from tensorflow import set_random_seed
set_random_seed(2)



def nn_keras(X, y,n_hlayers = 0,neurons = [],n_folds = 0,learning_rate = 0,n_classes = 0, seed = 5, grps = []):
	
	if n_hlayers == 0:
		print("did not set n_hlayers to hiddle layers")
		sys.exit(1)
	if neurons == 0:
		print("did not set neurons array")
		sys.exit(1)
	if n_folds == 0:
		print("did not set number of folds")
		sys.exit(1)
	if learning_rate == 0:
		print("did not set learning rate")
		sys.exit(1)
	if seed == 0:
		print("did not set seed")
		sys.exit(1)

	X_data = np.array(X)
	array_Y = np.array(y)

	instances, n_input = X_data.shape
	print("Instances", instances)

	# #training set
	# array_Y = []
	# total = []
	# with open(in_file) as f:
	# 	reader = csv.reader(f)
	# 	#next(reader)
	# 	array = list(reader)
	# 	n_input =  len(array[0])-1 
	# 	array = np.array(array)
		
	# # Data input (190 total erp values per patient)
	# 	#add each patient's erp values (row) to HC or AD vector 
	# 	for row in array[0:]: #first row is column headers
	# 		if (row[-1] == '0.0'): #rows 1-96 are HC patients
	# 			total.append(row[0:-1])
	# 			#output = 0
	# 			array_Y.extend([0])
	# 		else: #rows 97-171 are AD patients
	# 			total.append(row[0:-1])
	# 			#output = 1
	# 			array_Y.extend([1])
	# total = np.array(total)
	
	# tf.set_random_seed(seed)

	# X_data = np.array(total)
	# array_Y = np.array(array_Y)


	#convert to one-hot arrays
	array_Y = array_Y.astype(int)
	Y_data = np.eye(n_classes)[array_Y]


	#controlled shuffle function
	def shuffle(input):
		np.random.seed(5)
		np.random.shuffle(input)

	#shuffle(X_data)
	#shuffle(Y_data)
	#shuffle(grps)

	X_data = np.array(X_data)
	Y_data = np.array(Y_data)

	# #create neural network
	# model = Sequential()
	# model.add(Dense(neurons[0], activation = 'relu', input_dim = n_input))

	# for i in range(1,n_hlayers):
	# 	model.add(Dense(neurons[i], activation = 'relu'))
	# 	model.add(Dropout(0.25))

	# model.add(Dense(n_classes, activation = 'softmax'))

	# #Compile model
	# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

	def create_network():
		model = Sequential()
		model.add(Dense(neurons[0], kernel_initializer='random_uniform',  activation = 'relu', input_dim = n_input))

		for i in range(1,n_hlayers):
			model.add(Dense(neurons[i], activation = 'relu'))

		model.add(Dense(n_classes, kernel_initializer='random_uniform', activation = 'softmax'))

		#Compile model
		model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

		return model

	network = KerasClassifier(build_fn=create_network, epochs=50, batch_size=10, verbose=0)
	#compute_group_score(clf = [], X = X_data, y = Y_data, num_folds = n_folds, groups = grps, scoring='accuracy', nn_model = model)

	return network

	#cross-validation 
	# elements = len(X_data)
	# train_X=[]
	# train_Y=[]
	# test_X=[]
	# test_Y=[]
	# total_testAccuracy = 0
	# total_trainAccuracy = 0
	# total_fp = 0
	# total_fn = 0
	# total_TP = 0
	# total_TN = 0
	# total_FP = 0
	# total_FN = 0
	# total_Prec = 0
	# total_Fmeasure = 0
	# total_AUC = 0



	# for fold in range(0,n_folds):
	# 	model = Sequential()
	# 	model.add(Dense(neurons[0], activation = 'relu', input_dim = n_input))

	# 	for i in range(1,n_hlayers):
	# 		model.add(Dense(neurons[i], activation = 'relu'))

	# 	model.add(Dense(n_classes, activation = 'softmax'))

	# 	#Compile model
	# 	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

	# 	Xdata = X_data
	# 	Ydata = Y_data
	# 	Xdata = np.array(Xdata)
	# 	Ydata = np.array(Ydata)
	# 	first_index=int((fold*elements/float(n_folds)))
	# 	second_index=int(((fold+1)*elements/float(n_folds)))
		
	# 	#split the sets into training and testing sets

	# 	test_X = Xdata[first_index:second_index]
	# 	test_Y = Ydata[first_index:second_index]

	# 	if(len(test_X) == 0):
	# 		print "fold number too high or not enough instances to test on."
	# 		sys.exit(1)
	# 	index = [];
	# 	for n in range(first_index,second_index):
	# 		index.extend([n])
		
	# 	Xdata = np.delete(Xdata,index,axis=0)
	# 	Ydata = np.delete(Ydata,index,axis=0)
	# 	print len(test_X)
	# 	train_X = Xdata
	# 	train_Y = Ydata
		
	# 	#Fit model
	# 	print "training..."
	# 	print(train_X.shape)
	# 	print(train_Y.shape)

	# 	model.fit(train_X, train_Y, epochs = 21, batch_size = 10)

	# 	# evaluate the model
	# 	print "testing..."
	# 	trainscores = model.evaluate(train_X, train_Y)
	# 	train_acc = trainscores[1]*100
	# 	total_trainAccuracy = total_trainAccuracy + train_acc
	# 	print("\n%s: %.2f%%" % ("train acc", train_acc))

	# 	testscores = model.evaluate(test_X, test_Y)
	# 	test_acc = testscores[1]*100
	# 	total_testAccuracy = total_testAccuracy + test_acc
	# 	print("\n%s: %.2f%%" % ("test acc", test_acc))


	# 	#compute overall accuracy, false negative, and false positive
	# 	#total_accuracy += fold_accuracy*(float(len(test_X))/len(X_data))
	# 	#total_TP += TPrate*(float(len(test_X))/len(X_data))
	# 	#total_TN += TNrate*(float(len(test_X))/len(X_data))
	# 	#total_FP += FPrate*(float(len(test_X))/len(X_data))
	# 	#total_FN += FNrate*(float(len(test_X))/len(X_data))
	# 	#total_Prec += Prec*(float(len(test_X))/len(X_data))
	# 	#total_Fmeasure += Fmeasure*(float(len(test_X))/len(X_data))
	# 	#total_AUC += AUC[1]*(float(len(test_X))/len(X_data))
		
			
	# #print("Overall Accuracy:", total_accuracy)
	# #print("Overall False Negative:", total_FN)
	# #print("Overall False Positive:", total_FP)
	# #print("Overall Precision:", total_Prec)
	# #print("Overall Recall:", total_TP)
	# #print("Overall F-measure:", total_Fmeasure)
	# #print("Overall ROC AUC:", total_AUC)

	# total_trainAccuracy = total_trainAccuracy/n_folds
	# print "Overall Train Accuracy", total_trainAccuracy
	# total_testAccuracy = total_testAccuracy/n_folds
	# print "Overall Test Accuracy", total_testAccuracy

	# # results = [datetime.datetime.now(),iden,filename,total_trainAccuracy,total_testAccuracy,total_FN,total_FP,total_TP,total_TN,total_Fmeasure,total_AUC,n_hlayers,neurons,learning_rate,n_folds,n_classes,seed]
	# # r_file = open(results_file,'a')
	# # writer = csv.writer(r_file,delimiter=',')
	# # writer.writerow(results)
