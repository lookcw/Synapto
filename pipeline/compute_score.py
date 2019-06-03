from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GroupKFold
from sklearn.base import clone
from metrics import metrics
import numpy as np
import sys
from nn_keras import nn_keras

#define function to compute cross validation score
def compute_group_score(clf, X, y, num_folds, groups, scoring='accuracy', nn_model = []):

	# print(X.shape)
	# print(y.shape)

	if "keras" in str(clf):
		# print("yes")
		y = y.astype(int)
		y = np.eye(2)[y]

	isPredictProba = False
	invert_op = getattr(clf, "predict_proba", None)
	if callable(invert_op):
		isPredictProba = True
	gkf = GroupKFold(n_splits=num_folds)
	y_true = np.array(np.zeros(len(y)))
	y_pred = np.array(np.zeros(len(y)))
	y_scores = None
	if isPredictProba:
		y_scores = np.array(np.zeros((len(y),2)))
	count = 0
	print "groups: ",groups.shape
	if nn_model == []:
		for train, test in gkf.split(X, y, groups=groups):
			# print(X[train])
			#print(y[train])
			try:
				clf.fit(X[train],y[train])
			except ValueError:
				clf = nn_keras(X, y, n_hlayers = 3, neurons = [100,100,100],learning_rate = 0.1,n_folds =3,n_classes = 2, seed = 5, grps = groups)
				clf.fit(X[train],y[train])

			y_pred[count:count+len(test)] = clf.predict(X[test])

			if "keras" in str(clf):
				y_true[count:count+len(test)] = np.argmax(y[test], axis=1)
			else:
				y_true[count:count+len(test)] = y[test]

			if isPredictProba:
				y_scores[count:count+len(test)] = clf.predict_proba(X[test])
			clf = clone(clf)
			count += len(test)
		(accuracy,f1, tnP,fpP,fnP,tpP,roc_auc) = metrics(y_true,y_pred,y_scores)
		# print("Test accuracy",accuracy)
		print("Test f1",f1)
		# print("Test tnP",tnP)
		# print("Test fnP",fnP)
		# print("Test fpP",fpP)
		# print("Test tpP",tpP)
		print("Test roc_auc",roc_auc)
		return (accuracy,f1, tnP,fpP,fnP,tpP,roc_auc)
	else:
		fold_num = 1
		count = 0
		#serialize initial model weights
		nn_model.save_weights("initial_model.h5")
		for train, test in gkf.split(X, y, groups=groups):
			# print "Fold Number: " + str(fold_num)
			nn_model.fit(X[train], y[train], epochs = 100, batch_size = 10)
			trainscores = nn_model.evaluate(X[train], y[train])
			train_acc = trainscores[1]*100
			# print "nn_model group k-fold train acc: " + str(train_acc)
			testscores = nn_model.evaluate(X[test], y[test])
			test_acc = testscores[1]*100
			#print "nn_model group k-fold test acc: " + str(test_acc)

			y_pred[count:count+len(test)] = nn_model.predict(X[test])[:,1]
			y_true[count:count+len(test)] = y[test][:,1]

			#reset model parameters
			nn_model.load_weights("initial_model.h5")

			fold_num += 1
			count += len(test)

		y_pred = np.where(y_pred > 0.5, 1, 0)
		y_true = np.where(y_true > 0.5, 1, 0)
		(accuracy,f1,tnP,fpP,fnP,tpP,roc_auc) = metrics(y_true,y_pred, None)
		print("Test accuracy",accuracy)
		# print("Test f1",f1)
		# print("Test tnP",tnP)
		# print("Test fnP",fnP)
		# print("Test fpP",fpP)
		# print("Test tpP",tpP)
		print("Test roc_auc",roc_auc)
