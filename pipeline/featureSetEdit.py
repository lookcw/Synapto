# Input: feature set where the LAST column is + and -
# Output: attributes and value as separate arrays. Value is outputted as 1 or 0 instead of + or - 

# Pass in array with all the featureset data 
def remove_plus_min(data):
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

	return value, attributes