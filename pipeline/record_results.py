from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GroupKFold
from sklearn.base import clone
from metrics import metrics
import numpy as np
import sys
from nn_keras import nn_keras
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score
import csv
import time
import os


RESULTS_HEADER = ['Date', 'filename', 'Feature', 'Data Type', 'Classifier','Num Patients'
				  'Num Features', 'Num Folds', 'Accuracy', 'F-score', 'Sensitivity', 'Specificity', 'Epochs Per Instances', 'Instances Per Patient']


def _metrics(y_true, y_pred, y_scores):

	L = float(len(y_true))
	tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
	roc_auc = -1
	if y_scores is not None:
		# y_conf = list(map(lambda x: max(x), y_scores))
		y_conf = y_scores[:, 1]
		roc_auc = roc_auc_score(y_true, y_conf)
	accuracy = accuracy_score(y_true, y_pred)
	f1 = f1_score(y_true, y_pred)
	return {
		'accuracy': accuracy,
		'f1': f1,
		'sensitivity': tp / (fn + tp),
		'specificity': tn / (tn + fp),
		'roc_auc': roc_auc
	}

def _write_result_header(results_filename):
	with open(results_filename, 'a') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=RESULTS_HEADER)
		writer.writeheader()

def write_result_list_to_results_file(results_filename, results_list):
	if os.path.exists(results_filename):
		_write_result_header(results_filename)
	with open(results_filename, 'a') as f:
		writer = csv.writer(f)
		for result in results_list:
			result_array = [
				time.strftime("%m/%d/%Y"),
				result['feature_filename'],
				result['feature_name'],
				result['data_type'],
				result['model'],
				result['num_patients'],
				result['num_features'],
				result['num_folds'],
				result['accuracy'],
				result['f1'],
				result['senstivity'],
				result['specificity'],
				result['epochs_per_instance'],
				result['instances_per_patient']
			]
			writer.writerow(result_array)



def _split_dataframe(df):
	X = df.drop(['patient num', 'instance num',
				 'instance code', 'class'], axis=1)
	y = df['class']
	groups = df['patient num']
	instance_nums = df['instane num']
	return (X, y, groups, instance_nums)


def get_results(clf, df, num_folds, feature_name, data_type, epochs_per_instance, time_points_per_epoch, features_filename):
	metrics = _compute_group_score(clf, df, num_folds)
	(X, y, groups, instance_num) = _split_dataframe(df)
	num_patients = max(groups)
	results = dict(metrics)
	results.update({
		'num_folds': num_folds,
		'feature_name': feature_name,
		'data_type': data_type,
		'epochs_per_patient': epochs_per_instance,
		'time_points_per_epoch': time_points_per_epoch,
		'feature_filename': features_filename,
		'num_patients': num_patients,
		'model': format(clf.__class__)
	})
	return results


# define function to compute cross validation score
def _compute_group_score(clf, df, num_folds, scoring='accuracy', nn_model=[]):
	(X, y, groups, instance_num) = _split_dataframe(df)

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
		y_scores = np.array(np.zeros((len(y), 2)))
	count = 0
	print("groups: ", groups.shape)
	if nn_model == []:
		for train, test in gkf.split(X, y, groups=groups):
			# print(X[train])
			# print(y[train])
			try:
				clf.fit(X[train], y[train])
			except ValueError:
				clf = nn_keras(X, y, n_hlayers=3, neurons=[
					100, 100, 100], learning_rate=0.1, n_folds=3, n_classes=2, seed=5, grps=groups)
				clf.fit(X[train], y[train])

			y_pred[count:count+len(test)] = clf.predict(X[test])

			if "keras" in str(clf):
				y_true[count:count+len(test)] = np.argmax(y[test], axis=1)
			else:
				y_true[count:count+len(test)] = y[test]

			if isPredictProba:
				y_scores[count:count+len(test)] = clf.predict_proba(X[test])
			clf = clone(clf)
			count += len(test)
		return _metrics(y_true, y_pred, y_scores)

	else:
		fold_num = 1
		count = 0
		# serialize initial model weights
		nn_model.save_weights("initial_model.h5")
		for train, test in gkf.split(X, y, groups=groups):
			nn_model.fit(X[train], y[train], epochs=100, batch_size=10)
			trainscores = nn_model.evaluate(X[train], y[train])
			train_acc = trainscores[1]*100
			testscores = nn_model.evaluate(X[test], y[test])
			test_acc = testscores[1]*100

			y_pred[count:count+len(test)] = nn_model.predict(X[test])[:, 1]
			y_true[count:count+len(test)] = y[test][:, 1]

			nn_model.load_weights("initial_model.h5")

			fold_num += 1
			count += len(test)

		y_pred = np.where(y_pred > 0.5, 1, 0)
		y_true = np.where(y_true > 0.5, 1, 0)
		return _metrics(y_true, y_pred, y_scores)
