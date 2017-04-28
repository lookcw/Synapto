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


descriptor_dir = '../CorrelationAnalysis/newsdescriptors/'	
results_file=open('Results.csv','a')
result_writer=csv.writer(results_file,delimiter=',')
n = 1
identifier="default identifier"
for argument in sys.argv[1:]:
	if argument == "-iden":
		identifier = sys.argv[n+1]
	n+=1
	
# if identifier == "default identifier":
# 	print "error: put in identifier with -iden arg"
# 	sys.exit(0)


# now = datetime.datetime.now()
# if identifier!="0":
# 	result_writer.writerow([now,identifier])

des_file=open("test.csv",'r')
reader=csv.reader(des_file,delimiter=',')
array=np.array(list(reader))
print array.shape
#elements=len(featuresets)
normal_acc=[]
#calculate indicies to split by for cross validaton
# for i in range(0,num_folds):
# 	first_index=int((i*elements/float(num_folds)))
# 	second_index=int(((i+1)*elements/float(num_folds)))
data=array[:][:,0:-2].astype(np.float) #extract the training data without target
target=array[:][:,-1].astype(np.float) #extract target
print target
#(X_train,X_test,y_train,y_test)=train_test_split(data,target,t.est_size=0.2,random_state=0)
print data.shape
print target.shape
print type(target)
clf=svm.SVC(kernel='linear'	,decision_function_shape=None) #create svm
scores = cross_val_score(clf,data,target,cv=15,scoring='accuracy')#cv its number of folds 
predicted=cross_val_predict(clf,data,target,cv=15)
if identifier!="0":
	result_writer.writerow([metrics.accuracy_score(target,predicted)])
print  "accuracy: "+str(metrics.accuracy_score(target,predicted))


clf2 = RandomForestClassifier() #Initialize with whatever parameters you want to
clf1 = LogisticRegression(random_state=1)
clf2 = RandomForestClassifier(random_state=1)
clf3 = GaussianNB()
clf4 = KNeighborsClassifier(n_neighbors=2, algorithm='ball_tree')
clf5 = BernoulliNB()

eclf1 = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3),('knn',clf4),('mnb',clf5)], voting='soft')
eclf1 = eclf1.fit(data, target)
print(eclf1.predict(data))
# 10-Fold Cross validation
print np.mean(cross_val_score(eclf1, data, target, cv=15))



