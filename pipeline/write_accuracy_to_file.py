from compute_score import compute_group_score
import csv
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier  
import numpy as np
import time

def write_accuracy_to_file(clf, model, groups, X_reduced, X, y, num_folds, num_seeds, o_filename, filename, featureName, data_type):
	X = np.array(X)
	y = np.array(y)
	print('Cross-validation of : {0}'.format(model.__class__))
	(accuracy,f1, tnP,fpP,fnP,tpP,roc_auc) = compute_group_score(model, X, y, num_folds,groups, scoring='accuracy')
	(red_accuracy, red_f1, red_tnP,red_fpP,red_fnP,red_tpP,red_roc_auc) =\
		compute_group_score(model, X_reduced, y, num_folds,groups, scoring='accuracy')
	print('All features CV score = {0}'.format(accuracy))
	print('Reduced features CV score = {0}'.format(red_accuracy))

	try:
		with open(o_filename, 'r+') as csvfile:
			pass
	except IOError as e:
		with open(o_filename, 'a') as csvfile:
			header = ['Date','filename', 'Feature', 'Data', 'Classifier', 'Feature Reduction Classifier', 'Number of Features Before Reduction', 
			'Number of Features After Reduction', 'Num Folds', 'Num Seeds', 'Accuracy','F-score','True Negative',
			'False Positive','False Negative','True Positive',"ROCAUC", 'red Accuracy','red F-score',
			'red True Negative','red False Positive','red False Negative','red True Positive',"red ROCAUC"]
			writer = csv.DictWriter(csvfile, fieldnames=header)
			writer.writeheader()
	# Record the number of features that were reduced
	with open(o_filename, 'a') as f:
		writer = csv.writer(f)
		metrics = [accuracy,f1, tnP,fpP,fnP,tpP,roc_auc]
		red_metrics = [red_accuracy, red_f1, red_tnP,red_fpP,red_fnP,red_tpP,red_roc_auc]
		writer.writerow([time.strftime("%m/%d/%Y"), filename, featureName, data_type, format(model.__class__), format(clf.__class__), 
			X.shape, X_reduced.shape, num_folds, num_seeds]+ metrics + red_metrics)