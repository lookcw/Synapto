from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from svm import svm_func
import os
import sys
import pandas as pd
import numpy as np
import csv
from BandPass1 import delta_band_pass, theta_band_pass, alpha_band_pass, beta_band_pass, gamma_band_pass
import time
# from ASD_features import extractASDFeatures
# from WTcoef import extractWaveletFeatures
from createMatrixFeatureSet2 import create_feature_set, write_feature_set
import pearson_features
import granger_features
import domFreq_features
import domFreqVar_features
# import feature_steepness
import FSL_features
from Feature_settings import fsl_settings, pearson_settings
import pac_features
from record_results import get_results, write_result_list_to_results_file, print_results
from nn_keras import nn_keras
from nn_Recurr import nn_Recurr
import random
from sklearn.utils import shuffle
import functools
from identifier import paramToFilename, recurrParamToFilename
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, GradientBoostingClassifier
from group import file_2_recurr_X
from shuffle_data import shuffle_data
import copy
#from nn_Recurr import nn_Recurr

BANDS = [
    alpha_band_pass,
    beta_band_pass,
    delta_band_pass,
    theta_band_pass,
    gamma_band_pass,
]

FEATURE_NAMES_TO_CLASS = {
    'FSL': FSL_features,
    'PAC': pac_features,
    'DomFreq': domFreq_features,
    'Pearson': pearson_features,
    'Granger': granger_features,
    'DomFreqVar': domFreqVar_features
}

# FEATURE_CONFIGS = {
#     'FSL': FSL_config_array,
#     'PAC': PAC_config_array,
#     'DomFreq': DomFreq_config_array,
#     'Pearson': Pearson_config_array,
#     'Granger': Granger_config_array,
# }

DATA_TYPE_TO_FOLDERS = {
    'Brazil': ('BrazilRawData/HCF50', 'BrazilRawData/ADF50'),
    'newBrazil': ('BrazilRawData/HCF50_new', 'BrazilRawData/ADF50_new'),
    'AR': ('BrazilRawData/HC_AR', 'BrazilRawData/AD_AR'),
    'Test': ('BrazilRawData/TestHC', 'BrazilRawData/TestAD')
}

RESULTS_FILENAME = 'pipeline_results.csv'
FEATURE_SET_FOLDER = 'FeatureSets/'

MODELS = [
    LogisticRegression(),
    LogisticRegressionCV(),
    RandomForestClassifier(),
    GradientBoostingClassifier(),
    SVC(kernel="rbf",C=5.0),
    KNeighborsClassifier(n_neighbors=5)
]

################################################### DEFAULT SETTINGS ###################################################

CONFIG = {
    'data_type': '',
    'positive_folder_path': '',
    'negative_folder_path': '',
    'feature_name': '',
    'feature_class': '',
    'data_folder': '',
    'identifier_func': paramToFilename,
    'is_bands': False,
    'hc': False,
    'ad': False,
    'dlb': False,
    'is_force_overwrite': False,
    'startAtFS': False,
    'RECURR': False,
    'num_epochs': 1,  # per patient
    'time_points_per_epoch': 160000,  # per instance
    'num_instances': 1,
    'epochs_per_instance': 1,
    'num_folds': 4
}

CONFIG_FEATURES = {
    'FSL': fsl_settings(),
    'Pearson': pearson_settings()
}

# feature_name = ''
# data_type = ''
# hc = False
# ad = False
# dlb = False
# is_bands = False
# is_force_overwrite = False
# startAtFS = False
# RECURR = False

# num_epochs = 1  # per patient
# time_points_per_epoch = 160000  # per instance
# num_instances = 1
# epochs_per_instance = 1
# num_folds = 4
# identifier_func = paramToFilename

############################################## PARAMETER READING & SETTING ##############################################


for i in range(1, len(sys.argv), 2):
    if str(sys.argv[i]) == "-h":
        helpString = ('Run pipeline starting from beginning:\nInput arguments:\n-d: data type (choices: Brazil, Greece)' +
                      '\n-f: feature name (choices: ASD, Wavelet, FSL, Steepness)\n-i: instances per patient (ex: 1)\n-t: number of time points per instance (ex: 60)' +
                      '\n-nfs: no feature selection\n-recurr: use LSTM' + '\n-c1: class (HC, AD, DLB)' + '\n-c2: class (HC, AD, DLB)' +
                      '\n\nRun Pipeline With Existing Feature Set:\nInput arguments:\n-fs: feature set (.../PathToFeatureSetFile)')
        print(helpString)
        sys.exit()

    elif str(sys.argv[i]) == "-d":
        CONFIG['negative_folder_path'] = DATA_TYPE_TO_FOLDERS[sys.argv[i+1]][0]
        CONFIG['positive_folder_path'] = DATA_TYPE_TO_FOLDERS[sys.argv[i+1]][1]
        CONFIG['data_type'] = sys.argv[i+1]
    elif str(sys.argv[i]) == "-p":
        CONFIG['positive_folder_path'] = sys.argv[i+1]
    elif str(sys.argv[i]) == "-n":
        CONFIG['negative_folder_path'] = sys.argv[i+1]
    elif str(sys.argv[i]) == "-e":
        CONFIG['epochs_per_instance'] = int(sys.argv[i+1])
    elif str(sys.argv[i]) == "-f":
        CONFIG['feature_name'] = sys.argv[i+1]
        CONFIG['feature_class'] = FEATURE_NAMES_TO_CLASS[sys.argv[i+1]]
        config_features = CONFIG_FEATURES[sys.argv[i+1]]
    elif str(sys.argv[i]) == "-i":
        CONFIG['num_instances'] = int(sys.argv[i+1])
    elif str(sys.argv[i]) == "-t":
        CONFIG['time_points_per_epoch'] = int(sys.argv[i+1])
    elif str(sys.argv[i]) == "-fs":
        CONFIG['filename'] = sys.argv[i+1].split('/')[-1]
        CONFIG['startAtFS'] = True
    elif str(sys.argv[i]) == "-overwrite":
        CONFIG['is_force_overwrite'] = True
    elif str(sys.argv[i]) == "-recurr":
        CONFIG['RECURR'] = True
        CONFIG['identifier_func'] = recurrParamToFilename
    elif str(sys.argv[i]) == "-bands":
        CONFIG['is_bands'] = True
    else:
        print("Wrong format. Remember header must precede argument provided.\nUse -h for help.")
        sys.exit()
if CONFIG['data_type'] == '':
    CONFIG['data_type'] = CONFIG['negative_folder_path'].split('/')[-1] + '-' + CONFIG['positive_folder_path'].split('/')[-1]
    CONFIG['data_type'] = CONFIG['negative_folder_path'].split('/')[-1] + '-' + CONFIG['positive_folder_path'].split('/')[-1]

features_filename = CONFIG['identifier_func'](CONFIG) # Get filename
if CONFIG['is_bands'] == False:
    feature_filenames = [features_filename + CONFIG['feature_class'].config_to_filename(config_feature) for config_feature in config_features]
    print(feature_filenames)

    feature_paths = [os.path.join(FEATURE_SET_FOLDER, feature_filename) for feature_filename in feature_filenames]
    for feature_path in feature_paths:
        if os.path.exists(feature_path) and not is_force_overwrite:
            print("feature file already exists... skipping featureset creation")
            CONFIG['startAtFS'] = True

############################################## FEATURE SET CREATION/ READING ##############################################
if not CONFIG['startAtFS']:
    if not CONFIG['positive_folder_path'] or not CONFIG['negative_folder_path']:
        print("Did not input data type. Choose from list in help documentation")
        sys.exit()
    if CONFIG['data_type'] == '' and CONFIG['positive_folder_path'] and CONFIG['negative_folder_path']:
        data_folder_path3 = None
        CONFIG['data_type'] = CONFIG['negative_folder_path'].split(
            '/')[-1] + '-' + CONFIG['positive_folder_path'].split('/')[-1]
    if not CONFIG['RECURR']:
        extractFeatureFunc = functools.partial( 
            create_feature_set)
    if CONFIG['is_bands']:
        # [CONFIG_FEATURE['bands_func'] = bands_func for config_feature in CONFIG_FEATURES for bands_func in BANDS]
        config_feature_bands = []
        for config_feature in config_features:
            for bands_func in BANDS:
                copy_config_feature = copy.deepcopy(config_feature)
                copy_config_feature['bands_func'] = bands_func
                config_feature_bands.append(copy_config_feature)
        feature_sets = [extractFeatureFunc(CONFIG, config_feature) for config_feature in config_feature_bands]
        feature_filenames = [features_filename + CONFIG['feature_class'].config_to_filename(config_feature) for config_feature in config_feature_bands]
        feature_paths = [os.path.join(FEATURE_SET_FOLDER, feature_filename) for feature_filename in feature_filenames]
        
        print(feature_filenames)
        zip(feature_filenames, feature_sets)
        # CONFIG_FEATURES['bands_func'] = bands_func for bands_func in BANDS
        # feature_sets = [extractFeatureFunc(CONFIG, bands_func) for bands_func in BANDS]
    else:
        feature_sets = [extractFeatureFunc(CONFIG, config_feature) for config_feature in config_features]
        
        zip(feature_filenames, feature_sets)
        # feature_sets = [extractFeatureFunc(
        #     positive_folder_path, negative_folder_path, num_instances, epochs_per_instance, time_points_per_epoch)]
else:
    feature_sets = [pd.read_csv(features_path, header='infer')]

for feature_path in feature_paths:
    [write_feature_set(features_path, feature_set) for feature_set in feature_sets]


######################################################## PREDICTION ########################################################


# shuffle rows of dataframe
feature_sets = [shuffle(feature_set) for feature_set in feature_sets]
results = [get_results(model, feature_set, num_folds, feature_name, data_type, num_instances, epochs_per_instance,
                       time_points_per_epoch, features_path) for feature_set in feature_sets for model in MODELS]
print_results(results)
write_result_list_to_results_file(RESULTS_FILENAME, results)
