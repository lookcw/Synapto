from sklearn.model_selection import cross_val_score
import numpy as np

#define function to compute cross validation score
def compute_score(clf, X, y, num_folds, scoring='accuracy'):
    xval = cross_val_score(clf, X, y, cv = num_folds, scoring=scoring)
    return np.mean(xval)