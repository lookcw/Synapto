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
from keras.wrappers.scikit_learn import KerasClassifier
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' #hide warnings


def keras_to_sklearn(neurons = [],n_classes = 0):

	def create_network():
		model = Sequential()
		model.add(Dense(neurons[0], kernel_initializer='random_uniform',  activation = 'relu', input_dim = 21))

		for i in range(1,len(neurons)):
			model.add(Dense(neurons[i], activation = 'relu'))

		model.add(Dense(n_classes, kernel_initializer='random_uniform', activation = 'softmax'))

		#Compile model
		model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

		return model

	network = KerasClassifier(build_fn=create_network, epochs=50, batch_size=10, verbose=0)
	
	return network