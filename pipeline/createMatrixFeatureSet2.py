import numpy as np
import sys
import os
from numpy import genfromtxt
from app_config import STARTER_COLUMNS


STARTER_COLUMNS = ['instance code','patient num', 'instance num',]
CLASS_COLUMN = ['class']

def write_feature_set(feature_path, feature_set):



def create_feature_set(functionClass, positive_data_folder, negative_data_folder,
                       num_instances, epochs_per_instance, time_points_per_epoch, bands_func):
    (positive_features, patient_count, instance_count) = _get_features_for_folder(positive_data_folder,
                                                                                  0, 0, functionClass, num_instances,
                                                                                  epochs_per_instance,
                                                                                  time_points_per_epoch, bands_func)
    (negative_features, patient_count, instance_count) = _get_features_for_folder(negative_data_folder, patient_count, instance_count,
                                                 functionClass, num_instances, epochs_per_instance,
                                                 time_points_per_epoch, bands_func)
    labels = STARTER_COLUMNS + functionClass.getHeader() + CLASS_COLUMN
    return positive_features + negative_features    

def get_labels_from_folder(folder,functionClass, time_points_per_epoch):
    whole_data_set =  genfromtxt(os.listdir(data_folder)[0], delimiter=',')
    epoch_data_set = whole_data_set[0:time_points_per_epoch]
    return functionClass.getHeader(epoch_data_set)

def _get_features_for_folder(data_folder, patient_count, instance_count, functionClass, num_instances, epochs_per_instance, time_points_per_epoch, bands_func):
    folder_features = [
        _extract_feature_for_one_patient(
            functionClass,
            genfromtxt(filename, delimiter=','),
            num_instances,
            epochs_per_instance,
            time_points_per_epoch,
            bands_func
        )
        for filename in os.listdir(data_folder)
    ]
    return _unpack_add_groups(folder_features, patient_count, instance_count)


def _unpack_add_groups(X, patient_count, instance_count):
    """Turns 4d array of patients to 2d    
    Arguments:
        X {4D numpy array} -- [description]
        patient_count {[type]} -- [description]
        instance_count {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    two_d_array = []
    for patient_data in X:
        for instance_data in patient_data:
            for epoch_data in instance_data:
                two_d_array.append(
                    [patient_count, instance_count] + epoch_data)
            instance_count += 1
        patient_count += 1
    return (two_d_array, patient_count, instance_count)


def _extract_feature_for_one_patient(functionClass, patient_data_set, num_instances, epochs_per_instance, time_points_per_epoch, bandsFunc=None):
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
    if(bandsFunc):
        transposed_data_set = np.transpose(patient_data_set)
        transposed_filtered = [bandsFunc(time_series)
                               for time_series in transposed_data_set]
        data_set = np.transpose(transposed_filtered)
    features = []

    count = 0
    for _ in range(num_instances):
        instance_features = []
        for _ in range(epochs_per_instance):
            feature_row = functionClass.extractFeatures(
                data_set[count*time_points_per_epoch:(count+1) * time_points_per_epoch])
            instance_features.append(feature_row)
            count += 1
        features.append(instance_features)
    if functionClass.hasattr('apply_after'):
        features = functionClass.apply_after(features)
    return np.array(features)
