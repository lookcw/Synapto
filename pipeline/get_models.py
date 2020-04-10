from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from gridsearch import gridsearch


def get_models(config):

    MODELS = [
        RandomForestClassifier(),
        GradientBoostingClassifier(),
        KNeighborsClassifier(n_neighbors=5)
    ]


    if config['gridsearch']:
        GRIDSEARCH_MODELS = []

        for model in MODELS:
            GRIDSEARCH_MODELS.append(gridsearch(model))
        return GRIDSEARCH_MODELS

    else:
        return MODELS