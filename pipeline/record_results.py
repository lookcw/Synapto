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
from sklearn.metrics import roc_curve
from sklearn.metrics import f1_score
import csv
import time
import os
import matplotlib.pyplot as plt
from dataset_functions import split_dataframe
import pandas as pd


RESULTS_HEADER = [
    'Date',
    'Feature',
    'Data Type',
    'Classifier',
    'Num Patients',
    'Num Features',
    'ROC AUC',
    'Accuracy',
    'F-score',
    'Sensitivity',
    'Specificity',
    'filename',
    'Num Folds',
    'Epochs Per Instances',
    'Instances Per Patient'
]
PRINT_RESULTS_HEADER = [
    'Feature',
    'Data Type',
    'Model',
    'Bands',
    'ROC AUC',
    'Accuracy',
    'F-score',
    'Sensitivity',
    'Specificity',
]


def _metrics(y_true, y_pred, y_scores):

    L = float(len(y_true))
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    roc_auc = -1
    fpr, tpr = [], []
    if y_scores is not None:
        # y_conf = list(map(lambda x: max(x), y_scores))
        y_conf = y_scores[:,1]
        roc_auc = roc_auc_score(y_true, y_conf)
        fpr, tpr, thresholds = roc_curve(y_true, y_conf)
        plt.plot(fpr, tpr)
        plt.show()
    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    return {
        'accuracy': accuracy,
        'f1': f1,
        'sensitivity': tp / (fn + tp),
        'specificity': tn / (tn + fp),
        'roc_auc': roc_auc,
        'roc_curve': [fpr, tpr]
    }


def _write_result_header(results_filename):
    with open(results_filename, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=RESULTS_HEADER)
        writer.writeheader()


def print_results(results_list):
    for result in results_list:
        print([
            result['feature_name'],
            result['data_type'],
            result['model'],
            result['bands_func'],
            round(result['roc_auc'], 2),
            round(result['accuracy'], 2),
            round(result['f1'], 2),
            round(result['sensitivity'], 2),
            round(result['specificity'], 2),
        ])


def write_result_list_to_results_file(results_filename, results_list):
    if not os.path.exists(results_filename):
        _write_result_header(results_filename)
    with open(results_filename, 'a') as f:
        writer = csv.writer(f)
        for result in results_list:
            result_array = [
                time.strftime("%m/%d/%Y"),
                result['feature_name'],
                result['data_type'],
                result['bands_func'],
                result['model'],
                result['num_patients'],
                result['num_features'],
                result['roc_auc'],
                result['accuracy'],
                result['f1'],
                result['sensitivity'],
                result['specificity'],
                result['feature_filename'],
                result['num_folds'],
                result['epochs_per_instance'],
                result['instances_per_patient'],
                result['roc_curve']
            ]
            writer.writerow(result_array)


def get_results(clf, df, config, config_features):
    metrics = _compute_group_score(
        clf, df, config['num_folds'], config['is_voted_instances'])
    (X, y, groups, instance_num) = split_dataframe(df)
    num_patients = max(groups)
    results = dict(metrics)
    results.update({
        'num_folds': config['num_folds'],
        'feature_name': config['feature_name'],
        'data_type': config['data_type'],
        'bands_func':  (config_features['bands_func'].__name__ if 'bands_func' in config_features else 'none'),
        'instances_per_patient': config['num_instances'],
        'epochs_per_instance': config['epochs_per_instance'],
        'time_points_per_epoch': config['time_points_per_epoch'],
        'feature_filename': config_features['filename'],
        'num_patients': num_patients,
        'model': format(clf.__class__).split('.')[-1].replace('\'>', ''),
        'num_features': len(df.columns) - 4
    })
    return results


"""
This function returns the metrics for predictions predicted by _compute_group_pred

Raises:
    Exception: [description]

Returns:
    [type] -- [description]
"""
def _compute_group_score(clf, df, num_folds, is_voted_instances, scoring='accuracy', nn_model=[]):

    if is_voted_instances:
        (y_true, y_pred, y_scores, groups) = _compute_group_pred(
            clf, df, num_folds, is_voted_instances)
        pred_dict = {'y_pred': y_pred, 'groups': groups, 'y_true': y_true}
        df = pd.DataFrame(pred_dict)
        df['vote'] = df.groupby(['groups']).transform(
            lambda x: x.value_counts().index[0])['y_pred']
        df['conf'] = y_scores[:, 0]
        print(df.sort_values(by=['groups']))
        voted = df.groupby(['groups']).mean()
        print(voted)
        inv_conf = 1 - df['conf']
        voted_scores = np.array(list(zip(df['conf'],inv_conf)))
        print(_metrics(df['y_true'],df['y_pred'], voted_scores))
        raise Exception('this is supposed to happen dw')

    else:
        return _metrics(y_true, y_pred, y_scores)


def _compute_group_pred(clf, df, num_folds, scoring='accuracy', nn_model=[]):
    (X, y, groups, instance_num) = split_dataframe(df)
    print(sorted(list(zip(groups, y)), key=lambda x: x[0]))
    if "keras" in str(clf):
        y = y.astype(int)
        y = np.eye(2)[y]

    isPredictProba = False
    invert_op = getattr(clf, "predict_proba", None)
    if callable(invert_op):
        isPredictProba = True
    gkf = GroupKFold(n_splits=num_folds)
    y_true = np.array(np.zeros(len(y)))
    y_pred = np.array(np.zeros(len(y)))
    y_groups = np.array(np.zeros(len(y)))
    y_scores = None
    if isPredictProba:
        y_scores = np.array(np.zeros((len(y), 2)))
    count = 0
    if nn_model == []:
        for train, test in gkf.split(X, y, groups=groups):
            clf.fit(X[train], y[train])
            y_pred[count:count+len(test)] = clf.predict(X[test])
            y_groups[count:count+len(test)] = groups[test]
            if "keras" in str(clf):
                y_true[count:count+len(test)] = np.argmax(y[test], axis=1)
            else:
                y_true[count:count+len(test)] = y[test]

            if isPredictProba:
                y_scores[count:count+len(test)] = clf.predict_proba(X[test])
            clf = clone(clf)
            count += len(test)
        print(sorted(list(zip(groups, y_true)), key=lambda x: x[0]))
        return (y_true, y_pred, y_scores, y_groups)

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
        return (y_true, y_pred, y_scores, groups)
