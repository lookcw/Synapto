from random import *
import csv
write_array=[None] * 3000

writer = open("random_test.csv", 'w')
csvwriter = csv.writer(writer,delimiter=',')
for i in range(len(write_array) - 1):
	write_array[i] = "col "+str(i)
write_array[-1] = "result"
csvwriter.writerow(write_array)
for i in range(25):
	for j in range(len(write_array) - 1):
		write_array[j] = uniform(1,30)
	if i < 13:
		write_array[-1] = "+"
	else:
		write_array[-1] = "-"
	csvwriter.writerow(write_array)
