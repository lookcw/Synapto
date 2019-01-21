from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score

def metrics(y_true,y_pred,y_scores):

	L = float(len(y_true))
	tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
	(tnP, fpP, fnP, tpP) = (tn/L, fp/L, fn/L, tp/L)
	roc_auc = -1
	if y_scores is not None:
		# y_conf = list(map(lambda x: max(x), y_scores))
		y_conf = y_scores[:,1]
		roc_auc = roc_auc_score(y_true, y_conf)
	accuracy = accuracy_score(y_true, y_pred)
	f1 = f1_score(y_true,y_pred)
	return (accuracy,f1, tnP,fpP,fnP,tpP,roc_auc)
