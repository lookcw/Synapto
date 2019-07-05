import numpy as np
import random
from sklearn.utils import shuffle


def shuffle_y(y):
	num_shuffles = random.randint(1,21)

	for i in range(num_shuffles):
		y = shuffle(y)

	return y