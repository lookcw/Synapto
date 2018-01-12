import numpy as np
import os
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
import datetime
import csv
import sys	
from Tkinter import *




descriptor_dir = '../CorrelationAnalysis/newsdescriptors/'	
results_file=open('Results.csv','a')
result_writer=csv.writer(results_file,delimiter=',')
n = 1
data_file=""
for argument in sys.argv[1:]:
	if argument == "-data":
		data_file = sys.argv[n+1]
	n+=1

des_file=open("test4.csv",'r')
reader=csv.reader(des_file,delimiter=',')
array=np.array(list(reader))
print array.shape
#elements=len(featuresets)
normal_acc=[]

data=array[:][:,0:-2].astype(np.float) #extract the training data without target
target=array[:][:,-1].astype(np.float) #extract target
print target

print data.shape
print target.shape
print type(target)
print data
new_patient_file=open(data_file,"rb	")
new_reader=csv.reader(new_patient_file,delimiter=',')
test_set=np.array(list(new_reader))
test_set=test_set[0]
test_set=test_set[0:-2]
print type(test_set)
test_set=np.array(test_set)
test_set=test_set.reshape(1,-1)
print test_set
print type(test_set)


clf2 = RandomForestClassifier() #Initialize with whatever parameters you want to
clf1 = LogisticRegression(random_state=1)
clf2 = RandomForestClassifier(random_state=1)
clf3 = GaussianNB()
clf4 = KNeighborsClassifier(n_neighbors=2, algorithm='ball_tree')
clf5 = BernoulliNB()

eclf1 = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3),('knn',clf4),('mnb',clf5)], voting='soft')
eclf1 = eclf1.fit(data, target)


pred=eclf1.predict(data[4].reshape(1,-1))
conf=eclf1.predict_proba(data[4].reshape(1,-1))[0][0]
print conf
root = Tk()
T = Text(root, height=5, width=70)
T.pack()
if pred ==0:
	T.insert(END, "There is a "+str(round(conf, 2))+"% chance you do not have Alzheimer's")
else:
	T.insert(END, "There is a "+str(round(conf, 2))+" % chance you do have Alzheimer's")
mainloop()

# 10-Fold Cross validation


