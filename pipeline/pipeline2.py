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
from createMatrixFeatureSet2 import create_feature_set, write_feature_set, get_labels_from_folder
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

# FEATURE_configS = {
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
    'Test': ('BrazilRawData/TestHC', 'BrazilRawData/TestAD'),
    'NCClean': ('New_Castle_Data/HC_clean', 'New_Castle_Data/AD_clean'),
    'NCF50': ('New_Castle_Data/HCF50', 'New_Castle_Data/ADF50'),
    'NCFN50': ('New_Castle_Data/HCFN50', 'New_Castle_Data/ADFN50'),
    'DLB-AD': ('New_Castle_Data/DLB_clean', 'New_Castle_Data/AD_clean'),
    'HC-DLB': ('New_Castle_Data/HC_clean', 'New_Castle_Data/DLB_clean'),
    'NC_alpha': ('New_Castle_Data/HCFN50_alpha', 'New_Castle_Data/ADFN50_alpha'),
    'NC_beta': ('New_Castle_Data/HCFN50_beta', 'New_Castle_Data/ADFN50_beta'),
    'NC_gamma': ('New_Castle_Data/HCFN50_gamma', 'New_Castle_Data/ADFN50_gamma'),
    'NC_delta': ('New_Castle_Data/HCFN50_delta', 'New_Castle_Data/ADFN50_delta'),
    'NC_theta': ('New_Castle_Data/HCFN50_theta', 'New_Castle_Data/ADFN50_theta')
}

RESULTS_FILENAME = 'pipeline_results.csv'
FEATURE_SET_FOLDER = 'FeatureSets/'

MODELS = [
    # LogisticRegression(),
    # LogisticRegressionCV(),
    RandomForestClassifier(),
    GradientBoostingClassifier(),
    SVC(kernel="rbf", C=5.0),
    KNeighborsClassifier(n_neighbors=5)
]

################################################### DEFAULT SETTINGS ###################################################

config = {
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
    'force_overwrite': False,
    'skip_fs_creation': False,
    'RECURR': False,
    'num_epochs': 1,  # per patient
    'time_points_per_epoch': 160000,  # per instance
    'num_instances': 1,
    'epochs_per_instance': 1,
    'num_folds': 10,
    'concat_type': 'vertical',
    'is_voted_instances': False
}

CONFIG_FEATURES = {
    'FSL': fsl_settings(),
    'Pearson': pearson_settings(),
    'DomFreq': [{}],
    'Granger': [{}],
}

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
        config['negative_folder_path'] = DATA_TYPE_TO_FOLDERS[sys.argv[i+1]][0]
        config['positive_folder_path'] = DATA_TYPE_TO_FOLDERS[sys.argv[i+1]][1]
        config['data_type'] = sys.argv[i+1]
    elif str(sys.argv[i]) == "-p":
        config['positive_folder_path'] = sys.argv[i+1]
    elif str(sys.argv[i]) == "-n":
        config['negative_folder_path'] = sys.argv[i+1]
    elif str(sys.argv[i]) == "-e":
        config['epochs_per_instance'] = int(sys.argv[i+1])
    elif str(sys.argv[i]) == "-f":
        config['feature_name'] = sys.argv[i+1]
        config['feature_class'] = FEATURE_NAMES_TO_CLASS[sys.argv[i+1]]
        config_features = CONFIG_FEATURES[sys.argv[i+1]]
    elif str(sys.argv[i]) == "-i":
        config['num_instances'] = int(sys.argv[i+1])
    elif str(sys.argv[i]) == "-t":
        config['time_points_per_epoch'] = int(sys.argv[i+1])
    elif str(sys.argv[i]) == "-v":
        config['is_voted_instances'] = True
    elif str(sys.argv[i]) == "-fs":
        config['filename'] = sys.argv[i+1].split('/')[-1]
        config['skip_fs_creation'] = True
    elif str(sys.argv[i]) == "-overwrite":
        config['force_overwrite'] = True
    elif str(sys.argv[i]) == "-recurr":
        config['RECURR'] = True
        config['identifier_func'] = recurrParamToFilename
    elif str(sys.argv[i]) == "-concat":
        config['concat_type'] = sys.argv[i+1]
    elif str(sys.argv[i]) == "-bands":
        config['is_bands'] = True
    else:
        print("Wrong format. Remember header must precede argument provided.\nUse -h for help.")
        sys.exit()
if config['data_type'] == '':
    config['data_type'] = config['negative_folder_path'].split(
        '/')[-1] + '-' + config['positive_folder_path'].split('/')[-1]
    config['data_type'] = config['negative_folder_path'].split(
        '/')[-1] + '-' + config['positive_folder_path'].split('/')[-1]

# features_filename = config['identifier_func'](config) # Get filename
if not config['skip_fs_creation']:
    if config['is_bands']:
        config_feature_bands = []
        for config_feature in config_features:
            for bands_func in BANDS:
                copy_config_feature = copy.deepcopy(config_feature)
                copy_config_feature['bands_func'] = bands_func
                config_feature_bands.append(copy_config_feature)
        config_features = config_feature_bands
    for config_feature in config_features:
        config_feature['filename'] = config['identifier_func'](config, config_feature) + config['feature_class'].config_to_filename(
            config_feature) + '.csv'
feature_paths = [os.path.join(FEATURE_SET_FOLDER, config_feature['filename'])
                 for config_feature in config_features]
for feature_path in feature_paths:
    if os.path.exists(feature_path) and not config['force_overwrite']:
        print("feature file already exists... skipping featureset creation")
        config['skip_fs_creation'] = True
print(get_labels_from_folder(config))
############################################## FEATURE SET CREATION/ READING ##############################################
if not config['skip_fs_creation']:
    if not config['positive_folder_path'] or not config['negative_folder_path']:
        print("Did not input data type. Choose from list in help documentation")
        sys.exit()
    if config['data_type'] == '' and config['positive_folder_path'] and config['negative_folder_path']:
        data_folder_path3 = None
        config['data_type'] = config['negative_folder_path'].split('/')[-1] + \
            '-' + config['positive_folder_path'].split('/')[-1]
    feature_sets = [create_feature_set(
        config, config_feature) for config_feature in config_features]
    [write_feature_set(feature_path, feature_set) for (
        feature_set, feature_path) in zip(feature_sets, feature_paths)]
else:
    feature_sets = [pd.read_csv(feature_path, header='infer')
                    for feature_path in feature_paths]


######################################################## PREDICTION ########################################################


# shuffle rows of dataframe
feature_sets = [shuffle(feature_set) for feature_set in feature_sets]
results = [get_results(model, feature_set, config, config_feature) for (
    feature_set, config_feature) in zip(feature_sets, config_features) for model in MODELS]
print_results(results)
write_result_list_to_results_file(RESULTS_FILENAME, results)
