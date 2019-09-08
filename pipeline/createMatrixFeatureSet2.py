import numpy as np
import sys
import os
from numpy import genfromtxt
import pandas as pd


STARTER_COLUMNS = ['instance code','patient num', 'instance num',]
CLASS_COLUMN = ['class']

def write_feature_set(feature_path, feature_set_df):
    print('writing feature set to file')
    feature_set_df.to_csv(feature_path, index=False)


def create_feature_set(functionClass, positive_data_folder, negative_data_folder,
                       num_instances, epochs_per_instance, time_points_per_epoch, bands_func=   None):
    print('starting feature set creation')
    (positive_features, patient_count, instance_count) = _get_features_for_folder(positive_data_folder,
                                                                                  0, 0, functionClass, num_instances,
                                                                                  epochs_per_instance,
                                                                                  time_points_per_epoch, 1, bands_func)
    (negative_features, patient_count, instance_count) = _get_features_for_folder(negative_data_folder, patient_count, instance_count,
                                                 functionClass, num_instances, epochs_per_instance,
                                                 time_points_per_epoch, 0, bands_func)
    labels = STARTER_COLUMNS + \
        get_labels_from_folder(positive_data_folder, functionClass, time_points_per_epoch)\
         + CLASS_COLUMN
    data = np.array(positive_features + negative_features)
    return pd.DataFrame(data=data,  columns = labels)

def get_labels_from_folder(data_folder,functionClass, time_points_per_epoch):
    whole_data_set = genfromtxt(os.path.join(data_folder, os.listdir(data_folder)[0]), delimiter=',')
    epoch_data_set = whole_data_set[0:time_points_per_epoch]
    return functionClass.getHeader(epoch_data_set)

def _get_features_for_folder(CONFIG, data_folder, patient_count, functionClass, data_class, bands_func):
    filenames = [filename for filename in os.listdir(data_folder)]
    folder_features_with_filenames = [
        _extract_feature_for_one_patient(
            functionClass,
            filename,
            genfromtxt(os.path.join(data_folder,filename), delimiter=','),
            CONFIG['num_instances'],
            CONFIG['epochs_per_instance'],
            CONFIG['time_points_per_epoch'],
            bands_func
        )
        for filename in os.listdir(data_folder) if filename.endswith('.csv')
    ]
    folder_features = [folder_feature[0] for folder_feature in folder_features_with_filenames]
    filenames = [folder_feature[1] for folder_feature in folder_features_with_filenames]
    return _unpack_add_groups(folder_features, filenames, patient_count, instance_count, data_class)

# def _get_features_for_folder(data_folder, patient_count, instance_count, functionClass, num_instances, epochs_per_instance, time_points_per_epoch, data_class, bands_func):
#     filenames = [filename for filename in os.listdir(data_folder)]
#     folder_features_with_filenames = [
#         _extract_feature_for_one_patient(
#             functionClass,
#             filename,
#             genfromtxt(os.path.join(data_folder,filename), delimiter=','),
#             num_instances,
#             epochs_per_instance,
#             time_points_per_epoch,
#             bands_func
#         )
#         for filename in os.listdir(data_folder) if filename.endswith('.csv')
#     ]
#     folder_features = [folder_feature[0] for folder_feature in folder_features_with_filenames]
#     filenames = [folder_feature[1] for folder_feature in folder_features_with_filenames]
#     return _unpack_add_groups(folder_features, filenames, patient_count, instance_count, data_class)


def _unpack_add_groups(X, filenames, patient_count, instance_count, data_class):
    """Turns 4d array of patients to 2d    
    Arguments:
        X {4D numpy array} -- [description]
        patient_count {[type]} -- [description]
        instance_count {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    two_d_array = []
    for (patient_data, filename) in zip(X,filenames):
        for instance_data in patient_data:
            for epoch_data in instance_data:
                two_d_array.append([filename.replace('.csv',''), patient_count, instance_count] + epoch_data.tolist() + [data_class])
            instance_count += 1
        patient_count += 1
    return (two_d_array, patient_count, instance_count)


def _extract_feature_for_one_patient(functionClass, filename, patient_data_set, num_instances, epochs_per_instance, time_points_per_epoch, bandsFunc=None):
    """applys the extractFeatures function of function class onto one patient's dataset

    Arguments:
        functionClass {module} -- a module with at least 2 public methods, extractFeatures and getHeader
        data_set {np.array} -- 2d numpy array where number of columns is number of electrodes
        num_instances {int} -- number of instances per patient
        epochs_per_instance {int} -- epochs per instance
        time_points_per_epoch {int} -- time points per epoch

    Keyword Arguments:
        bandsFunc {function} -- A function to apply to each electrode, supposed to be a band pass function (default: {None})

    Returns:
        3d numpy array -- 3d array, where first dimension is across instances, 2nd is across epochs, 3rd is across time points
    """
    print(f'extracting features for {filename}')
    if(bandsFunc):
        transposed_data_set = np.transpose(patient_data_set)
        transposed_filtered = [bandsFunc(time_series)
                               for time_series in transposed_data_set]
        patient_data_set = np.transpose(transposed_filtered)
    features = []

    count = 0
    for _ in range(num_instances):
        instance_features = []
        for _ in range(epochs_per_instance):
            feature_row = functionClass.extractFeatures(
                patient_data_set[count*time_points_per_epoch:(count+1) * time_points_per_epoch])
            instance_features.append(feature_row)
            count += 1
        features.append(instance_features)
    if hasattr(functionClass, 'apply_after'):
        features = functionClass.apply_after(features)
    return (np.array(features), filename)
