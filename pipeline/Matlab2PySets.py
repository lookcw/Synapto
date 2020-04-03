import pandas as pd
import numpy as np
from identifier import paramToFilename
import os
from shutil import copyfile


bands_to_dataset = {
    'alpha': 'NC_alpha',
    'beta': 'NC_beta',
    'delta': 'NC_delta',
    'theta': 'NC_theta',
    'gamma': 'NC_gamma'
}


def transform_name(filename):
    config = {}
    config_feature = {}
    parts_arr = filename.split('_')
    if parts_arr[1] in bands_to_dataset:
        config['data_type'] = bands_to_dataset[parts_arr[1]]
        config['is_bands'] = True
        config_feature['bands_func'] = bands_to_dataset[parts_arr[1]]
    else:
        config['data_type'] = 'NCClean'
        config['is_bands'] = False
        config_feature['bands_func'] = None
    config['epochs_per_instance'] = 1
    if 'ep' in parts_arr[3]:
        config['epochs_per_instance'] = int(parts_arr[3].replace('ep', ''))
    config['num_instances'] = 1
    config['feature_name'] = parts_arr[0]
    config['time_points_per_epoch'] = int(
        23808 / config['epochs_per_instance'])
    return paramToFilename(config, config_feature)


dir_str = 'MatlabFeatureSets'
directory = os.fsencode(dir_str)
dest_dir_str = 'FeatureSets'

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"):
        dst = os.path.join(dest_dir_str, transform_name(filename)) + '.csv'
        if not os.path.exists(dst):        
            src = os.path.join(dir_str, filename)
            copyfile(src,dst)