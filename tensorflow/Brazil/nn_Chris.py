import tensorflow as tf
import numpy as np
import csv
import os
import math
import six
import sys
import datetime
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' #hide warnings
print "starting"
# Network Parameters
#tf.set_random_seed(5)



def x_validation(in_file = "" ,n_hlayers = 0,neurons = [],n_folds = 0,results_file  = "" 
	,identifier = "" ,learning_rate = 0,n_classes = 0):
	if in_file == "":
		print "did not include file name"
		sys.exit(1)
	if n_hlayers == 0:
		print "did not set n_hlayers to hiddle layers"
		sys.exit(1)
	if neurons == 0:
		print "did not set neurons array"
		sys.exit(1)
	if n_folds == 0:
		print "did not set number of folds"
		sys.exit(1)
	if results_file == "":
		print "did not set results file"
		sys.exit(1)
	if learning_rate == 0:
		print "did not set learning rate"
		sys.exit(1)
	#training set
	array_Y = []
	total = []
	with open(in_file) as f:
		reader = csv.reader(f)
		#next(reader)
		array = list(reader)
		n_input =  len(array[0])-1 
		array = np.array(array)
	# Data input (190 total erp values per patient)
		#add each patient's erp values (row) to HC or AD vector 
		for row in array: #first row is column headers
			if (row[-1] == "-"): #rows 1-96 are HC patients
				total.append(row[0:-1])
				#output = 0
				array_Y.extend([0])
			else: #rows 97-171 are AD patients
				total.append(row[0:-1])
				#output = 1
				array_Y.extend([1])
	total = np.array(total)
	print total
	print array_Y


	X_data = np.array(total)
	array_Y = np.array(array_Y)
	#convert to one-hot arrays
	array_Y = array_Y.astype(int)
	Y_data = np.eye(n_classes)[array_Y]

	#controlled shuffle function
	def shuffle(input):
		np.random.seed(3)
		return np.random.shuffle(input)

	shuffle(X_data)
	shuffle(Y_data)
	#cross-validation 
	elements = len(X_data)
	train_X=[]
	train_Y=[]
	test_X=[]
	test_Y=[]
	total_accuracy = 0
	total_fp = 0
	total_fn = 0
	total_TP = 0
	total_TN = 0
	total_FP = 0
	total_FN = 0
	total_Prec = 0
	total_Fmeasure = 0
	total_AUC = 0

			


	for i in range(0,n_folds):
		W = [0 for i in range(n_hlayers+1)]
		b = [0 for i in range(n_hlayers+1)]
		H = [0 for i in range(n_hlayers)]
		#declare interactive session
		sess = tf.InteractiveSession()
		X = tf.placeholder(tf.float32, shape=[None, n_input], name="x-input")
		Y = tf.placeholder(tf.float32, shape=[None, n_classes], name="y-input")
		W[0] = tf.Variable(tf.random_normal([n_input, neurons[0]]), name="Weight1")
		b[0] = tf.Variable(tf.random_normal([neurons[0]]), name="Bias1")
		H[0] = tf.nn.sigmoid(tf.matmul(X, W[0]) + b[0])

		for i in range(1,n_hlayers):
			W[i] = tf.Variable(tf.random_normal([neurons[i-1], neurons[i]]), name="Weight" + str(i+1))
			b[i] = tf.Variable(tf.random_normal([neurons[i]]), name="Bias"+str(i+1))

		W[-1] = tf.Variable(tf.random_normal([neurons[-1], n_classes]), name="Weight" + str(n_hlayers+1))
		b[-1] = tf.Variable(tf.random_normal([n_classes]), name="Bias"+str(n_hlayers+1))

		for i in range(1,n_hlayers):
			H[i] = tf.nn.sigmoid(tf.matmul(H[i-1], W[i]) + b[i])
		output = tf.nn.sigmoid(tf.matmul(H[-1], W[-1]) + b[-1])

		#predicted values


		#backward-pass
		loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=output))
		optimizer = tf.train.GradientDescentOptimizer(learning_rate)
		train = optimizer.minimize(loss)


		Xdata = X_data
		Ydata = Y_data
		Xdata = np.array(Xdata)
		Ydata = np.array(Ydata)
		first_index=int((i*elements/float(n_folds)))
		second_index=int(((i+1)*elements/float(n_folds)))
		#print('first index',first_index)
		#print('second index',second_index)
		
		#split the sets into training and testing sets
		print len(test_X)
		test_X = Xdata[first_index:second_index]
		test_Y = Ydata[first_index:second_index]

		index = [];
		for n in range(first_index,second_index):
			index.extend([n])
		
		Xdata = np.delete(Xdata,index,axis=0)
		Ydata = np.delete(Ydata,index,axis=0)
		print len(test_X)
		print len(Xdata)
		train_X = Xdata
		train_Y = Ydata
		
		#train/test model
		init = tf.global_variables_initializer()
		sess.run(init)

		#cycles of all training set
		for epoch in range(1000):
			#train with each example
			for j in range(len(train_X)):
				sess.run(train, feed_dict={X: train_X[j:j+1], Y: train_Y[j:j+1]})
				#print "x = " + str(train_X[j:j+1]) + "  y = "+str(train_Y[j:j+1])
			# if epoch == 0:
			# 	sys.exit(0)
				
			if epoch == 999:
				print('Epoch ', epoch)
				print('Train Prediction ', sess.run(output, feed_dict={X: train_X, Y: train_Y}))
				#print('Weight1 ', sess.run(w1))
				#print('Bias1 ', sess.run(b1))
				print('cost ', sess.run(loss, feed_dict={X: train_X, Y: train_Y}))
				
				train_prediction = tf.equal(tf.argmax(output, axis=1), tf.argmax(Y, axis=1))
				#calculate train accuracy
				train_accuracy = tf.reduce_mean(tf.cast(train_prediction, "float"))
				print("Train Accuracy:", train_accuracy.eval({X: train_X, Y: train_Y}))
					
					
		#test model
		print('Test Prediction ', sess.run(output, feed_dict={X: test_X, Y: test_Y}))
		#confusion matrix
		labels = tf.argmax(test_Y, axis=1)
		predictions = tf.argmax(output.eval({X: test_X}), axis=1)
		
		matrix = sess.run(tf.confusion_matrix(labels,predictions))
		print(matrix)
		
		if(len(matrix) == 2):
			TN = float(matrix[0][0])
			FP = float(matrix[0][1])
			FN = float(matrix[1][0])
			TP = float(matrix[1][1])
			
		total = TN + FP + FN + TP
		actualNO = TN + FP
		actualYES = FN + TP
		predYES = FP + TP
		
		fold_accuracy = (TP + TN)/total
		print("Test Accuracy:", fold_accuracy)
		if(actualYES == 0):
			TPrate = 1
		else:
			TPrate = TP/actualYES

		print("Recall:", TPrate)
		if actualNO == 0:
			TNrate = 1
		else:
			TNrate = TN/actualNO
		print("True Negative:", TNrate)
		if(actualNO == 0):
			FPrate = 0
		else:
			FPrate = FP/actualNO

		print("False Positive:", FPrate)
		if(actualYES == 0):
			FNrate = 0
		else:
			FNrate = FN/actualYES

		print("False Negative:", FNrate)
		if(predYES == 0):
			Prec = 0
		else:
			Prec = TP/predYES

		print("Precision:", Prec)
		if((Prec+TPrate) == 0):
			Fmeasure = 0
		else:
			Fmeasure = (2*Prec*TPrate)/(Prec+TPrate)
		
		print("F-measure:", Fmeasure)
		
		auc = tf.metrics.auc(labels,
		predictions,
		weights=None,
		num_thresholds=200,
		metrics_collections=None,
		updates_collections=None,
		curve='ROC',
		name=None)
		
		tf.local_variables_initializer().run()
		AUC = sess.run(auc)
		print("ROC AUC:", AUC[1])
		
		#compute overall accuracy, false negative, and false positive
		total_accuracy += fold_accuracy*(float(len(test_X))/len(X_data))
		total_TP += TPrate*(float(len(test_X))/len(X_data))
		total_TN += TNrate*(float(len(test_X))/len(X_data))
		total_FP += FPrate*(float(len(test_X))/len(X_data))
		total_FN += FNrate*(float(len(test_X))/len(X_data))
		total_Prec += Prec*(float(len(test_X))/len(X_data))
		total_Fmeasure += Fmeasure*(float(len(test_X))/len(X_data))
		total_AUC += AUC[1]*(float(len(test_X))/len(X_data))
		
			
	print("Overall Accuracy:", total_accuracy)
	print("Overall False Negative:", total_FN)
	print("Overall False Positive:", total_FP)
	print("Overall Precision:", total_Prec)
	print("Overall Recall:", total_TP)
	print("Overall F-measure:", total_Fmeasure)
	print("Overall ROC AUC:", total_AUC)
	results = [datetime.datetime.now(),iden,filename,total_accuracy,total_FN,total_FP,total_TP,total_TN,total_Fmeasure,total_AUC,n_hlayers,neurons,learning_rate,n_folds,n_classes]
	r_file = open(results_file,'a')
	writer = csv.writer(r_file,delimiter=',')
	writer.writerow(results)



n=1
for argument in sys.argv[1:]:
	if (argument == "-f"):
		filename = sys.argv[n+1]
	if argument == "-i":
		iden = sys.argv[n+1]
	n+=1

x_validation(in_file = filename,identifier = iden, n_hlayers = 3, neurons = [20,30,20],learning_rate = 0.2,results_file = "../Results.csv",n_folds = 3,n_classes = 2)