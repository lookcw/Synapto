import numpy as np
import random
from sklearn.utils import shuffle


def shuffle_data(data):
	num_shuffles = random.randint(1,101)

	for i in range(num_shuffles):
		data = shuffle(data)

	return data