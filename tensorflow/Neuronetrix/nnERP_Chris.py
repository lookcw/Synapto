import tensorflow as tf
import numpy as np
import csv
import os
import math
import six
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' #hide warnings

# Network Parameters
#tf.set_random_seed(5)
learning_rate = 0.4
n_hidden1 = 20 # 1st layer number of neurons
n_hidden2 = 20 # 2nd layer number of neurons
n_hidden3 = 20 # 3rd layer number of neurons
n_input = 190 # Data input (190 total erp values per patient)
n_classes = 2 # 0 or 1 for Healthy or Alzheimer's
num_folds = 3 #cross validation

#declare interactive session
sess = tf.InteractiveSession()

X = tf.placeholder(tf.float32, shape=[None, n_input], name="x-input")
Y = tf.placeholder(tf.float32, shape=[None, n_classes], name="y-input")

W1 = tf.Variable(tf.random_normal([n_input, n_hidden1],stddev=math.sqrt(n_input)), name="Weight1")
W2 = tf.Variable(tf.random_normal([n_hidden1, n_hidden2],stddev=math.sqrt(n_input)), name="Weight2")
W3 = tf.Variable(tf.random_normal([n_hidden2, n_hidden3],stddev=math.sqrt(n_input)), name="Weight3")
W4 = tf.Variable(tf.random_normal([n_hidden3, n_classes],stddev=math.sqrt(n_input)), name="Weight4")

b1 = tf.Variable(tf.random_normal([n_hidden1],stddev=math.sqrt(n_input)), name="Bias1")
b2 = tf.Variable(tf.random_normal([n_hidden2],stddev=math.sqrt(n_input)), name="Bias2")
b3 = tf.Variable(tf.random_normal([n_hidden3],stddev=math.sqrt(n_input)), name="Bias3")
b4 = tf.Variable(tf.random_normal([n_classes],stddev=math.sqrt(n_input)), name="Bias4")

#forward-pass
#hidden layer 
H1 = tf.nn.sigmoid(tf.matmul(X, W1) + b1)
H2 = tf.nn.sigmoid(tf.matmul(H1, W2) + b2)
H3 = tf.nn.sigmoid(tf.matmul(H2, W3) + b3)

#predicted values
output = tf.nn.sigmoid(tf.matmul(H3, W4) + b4)

#backward-pass
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=output))
optimizer = tf.train.GradientDescentOptimizer(learning_rate)
train = optimizer.minimize(loss)

#training set
array_Y = []

basepath = 'data/'
total = []
with open(os.path.join(basepath, "erpn1_shuf_biased1.csv")) as f:
	reader = csv.reader(f)
	array = list(reader)
	array = np.array(array)
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


X_data = np.array(total)
print(array_Y)
array_Y = np.array(array_Y)
#convert to one-hot arrays
array_Y = array_Y.astype(int)
Y_data = np.eye(n_classes)[array_Y]

#controlled shuffle function
# def shuffle(input):
# 	np.random.seed(1)
# 	return np.random.shuffle(input)

# shuffle(X_data)
# shuffle(Y_data)

#cross-validation 
elements = len(X_data)
train_X=[]
train_Y=[]
test_X=[]
test_Y=[]
total_accuracy = 0
total_fp = 0
total_fn = 0

for i in range(0,num_folds):
	Xdata = X_data
	Ydata = Y_data
	Xdata = np.array(Xdata)
	Ydata = np.array(Ydata)
	first_index=int((i*elements/float(num_folds)))
	second_index=int(((i+1)*elements/float(num_folds)))
	#print('first index',first_index)
	#print('second index',second_index)
	
	#split the sets into training and testing sets
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
	test_prediction = tf.equal(tf.argmax(output, axis=1), tf.argmax(test_Y, axis=1))
	
	test_accuracy = tf.reduce_mean(tf.cast(test_prediction, "float"))
	fold_accuracy = test_accuracy.eval({X: test_X, Y: test_Y})
	print("Test Accuracy:", fold_accuracy)
	
	#compute false positive and false negative rates
	YIndex = tf.argmax(test_Y, axis=1)
	outputIndex = tf.argmax(output, axis=1)
	diff = YIndex-outputIndex
	#false positive: negative diff
	fp = tf.less(diff,0)
	fpRate = tf.reduce_mean(tf.cast(fp, "float"))
	print("False Positive:", fpRate.eval({X: test_X, Y: test_Y}))
	#false negative: positive diff
	fn = tf.greater(diff,0)
	fnRate = tf.reduce_mean(tf.cast(fn, "float"))
	print("False Negative:", fnRate.eval({X: test_X, Y: test_Y}))
		
	#compute overall accuracy, false negative, and false positive
	total_accuracy += fold_accuracy*((len(test_X)+0.0)/len(X_data))
	total_fp += fnRate.eval({X: test_X, Y: test_Y})*(float(len(test_X))/len(X_data))
	total_fn += fpRate.eval({X: test_X, Y: test_Y})*(float(len(test_X))/len(X_data))
		
print("Overall Accuracy:", total_accuracy)
print("Overall False Positive:", total_fp)
print("Overall False Negative:", total_fn)