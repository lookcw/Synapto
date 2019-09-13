def paramToFilename(config, config_feature):
    return config['feature_name'] + \
        "-" + (config_feature['bands_func'].__name__ if config['is_bands'] else '') + "_" + \
        str(config['data_type']) + "_" + \
        str(config['num_instances']) + '_instances_' + \
        str(config['time_points_per_epoch']) + '_epochs_' + \
        str(config['epochs_per_instance']) + '_timepoints_'

def recurrParamToFilename(config):
    return config['feature_name'] + \
        "-" + config['bands_func'].__name__ if config['is_bands'] else '' + "_" + \
        str(config['data_type']) + "_" + \
        str(config['num_instances']) + '_instances_' + \
        str(config['time_points_per_epoch']) + '_epochs_' + \
        str(config['epochs_per_instance']) + '_timepoints_recurr'

def filenameToParam(filename):
    line = filename.split('_')
    # feature_name, datatype, num_instances, epochs,timepoints
    return ('_'.join(line[:-7]), line[-7], line[-6], line[-4], line[-2])
