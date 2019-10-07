import numpy as np
from sklearn.model_selection import GridSearchCV

# svc_params = {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
#                      'C': [1, 10, 100, 1000]}

# random_forest_params = {'bootstrap': [True, False],
#                     'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
#                     'max_features': ['auto', 'sqrt'],
#                     'min_samples_leaf': [1, 2, 4],
#                     'min_samples_split': [2, 5, 10],
#                     'n_estimators': [100, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]}

# gradient_boosting_params = {
#     "loss":["deviance"],
#     "learning_rate": [0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2],
#     "min_samples_split": np.linspace(0.1, 0.5, 12),
#     "min_samples_leaf": np.linspace(0.1, 0.5, 12),
#     "max_depth":[3,5,8],
#     "max_features":["log2","sqrt"],
#     "criterion": ["friedman_mse",  "mae"],
#     "subsample":[0.5, 0.618, 0.8, 0.85, 0.9, 0.95, 1.0],
#     "n_estimators":[10] 
# }

# log_regression_params = {'max_iter': [1000],'penalty': ['l2'], 'C': [5,10], 'solver': 'liblinear'}

# kneighbors_params = {'n_neighbors': [3,10,20,50] }

# adaboost_params = {'n_estimators' : [10,30,50] }

svc_params = {'kernel': ['rbf'], 'gamma': [1e-3],
                     'C': [1]}

random_forest_params = {'bootstrap': [True, False],
                    'max_depth': [10,50,100],
                    'max_features': ['auto'],
                    'min_samples_leaf': [1],
                    'min_samples_split': [2],
                    'n_estimators': [100]}

gradient_boosting_params = {
    "loss":["deviance"],
    "learning_rate": [0.01],
    "min_samples_split": np.linspace(0.1, 0.5, 1),
    "min_samples_leaf": np.linspace(0.1, 0.5, 1),
    "max_depth":[3],
    "max_features":["log2"],
    "criterion": ["friedman_mse"],
    "subsample":[0.5],
    "n_estimators":[10] 
}

log_regression_params = {'max_iter': [1000],'penalty': ['l2'], 'C': [5], 'solver': 'liblinear'}

kneighbors_params = {'n_neighbors': [3] }

adaboost_params = {'n_estimators' : [10] }

keras_params = {}

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
    'KerasClassifier': keras_params,
}

