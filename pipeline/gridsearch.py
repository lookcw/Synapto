import numpy as np
from sklearn.model_selection import GridSearchCV
from statistics import mode

svc_params = {'kernel': ['rbf','linear'], 'gamma': [100,10,1,1e-1],
                     'C': [0.1,1,2,5, 10,100],
                     'probability':[True,False]
                     }

random_forest_params = {'bootstrap': [True],
                    'max_depth': [None],
                    'max_features': ['auto'],
                    'min_samples_leaf': [1, 4],
                    'min_samples_split': [2, 10],
                    'n_estimators': [100, 600]}
                    
# random_forest_params = {'bootstrap': [True],
#                     'max_depth': [50],
#                     'max_features': ['auto'],
#                     'min_samples_leaf': [1],
#                     'min_samples_split': [2],
#                     'n_estimators': [100]}

gradient_boosting_params = {
    "loss":["deviance"],
    "learning_rate": [0.01, 0.05, 0.2],
    "min_samples_split": np.linspace(0.1, 0.5, 2),
    "min_samples_leaf": np.linspace(0.1, 0.5, 2),
    "max_depth":[3,5,8],
    "max_features":["log2","sqrt"],
    "criterion": ["friedman_mse",  "mae"],
    "subsample":[0.5, 0.618, 0.8, 1.0],
    "n_estimators":[10] 
}

# gradient_boosting_params = {
#     "loss":["deviance"],
#     "learning_rate": [0.01],
#     "min_samples_split":np.linspace(0.1, 0.5, 2),
#     "min_samples_leaf": np.linspace(0.1, 0.5, 2),
#     "max_depth":[3],
#     "max_features":["log2"],
#     "criterion": ["friedman_mse"],
#     "subsample":[0.5],
#     "n_estimators":[10] 
# }

log_regression_params = {'max_iter': [1000],'penalty': ['l2'], 'C': [5,10], 'solver': 'liblinear'}

kneighbors_params = {'n_neighbors': [10] }

adaboost_params = {'n_estimators' : [10,30,50] }

def gridsearch(clf):
    tuned_parameters = class_config[clf.__class__.__name__]
    grid_clf = GridSearchCV(clf, tuned_parameters, cv=5)
    return grid_clf


class_config = {
    'SVC': svc_params,
    'RandomForestClassifier': random_forest_params,
    'GradientBoostingClassifier': gradient_boosting_params,
    'LogisticRegression':log_regression_params,
    'KNeighborsClassifier': kneighbors_params,
    'AdaBoostClassifier': adaboost_params,
}

def get_best_param(arr):
    if isinstance(arr[0],int) or isinstance(arr[0],float):
        return sum(arr)/len(arr)
    else:
        return mode(arr)

def get_best_params(params_list):
    best = {}
    for param in params_list[0]:
        best[param] = get_best_param([params[param] for params in params_list])
    return best

