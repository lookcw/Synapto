from sklearn.metrics import confusion_matrix

def confMat(y_true,y_pred):

	L = len(y_true)
	tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
	(tnP, fpP, fnP, tpP) = (tn/L, fp/L, fn/L, tp/L)

	return (tnP,fpP,fnP,tnP)
