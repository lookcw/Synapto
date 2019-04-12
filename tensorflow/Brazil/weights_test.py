import tensorflow as tf
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' #hide warnings
seed = 1
tf.set_random_seed(seed)


sess = tf.InteractiveSession()



W = tf.Variable(tf.random_normal([3, 3]), name="Weight1")

for i in range(4):
	init = tf.global_variables_initializer()
	sess.run(init)
	print sess.run(W)