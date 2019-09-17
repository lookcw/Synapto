<<<<<<< HEAD
def paramToFilename(feature_name, datatype, num_instances ,num_timePoints, epochs_per_instance):
    return feature_name +"_" + str(datatype) + "_" + str(num_instances)+'_instances_'+ str(epochs_per_instance) + '_epochs_' + str(num_timePoints) + '_timepoints.csv'
def curry_param_to_filename(datatype, num_instances ,num_timePoints, epochs_per_instance):
    def lam(feature_name):
        return paramToFilename(feature_name, datatype,num_instances,num_timePoints,epochs_per_instance)
    return lam
def recurrParamToFilename(feature_name, datatype, num_instances ,num_timePoints, epochs_per_instance):
    return feature_name +"_" + str(datatype) + "_" + str(num_instances)+'_instances_'+ str(epochs_per_instance) + '_epochs_' + str(num_timePoints) + '_timepoints_recurr.csv'
=======
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
>>>>>>> e8236e582c25523248f188a308092874b4f53f6e

def filenameToParam(filename):
    line = filename.split('_')
    # feature_name, datatype, num_instances, epochs,timepoints
    return ('_'.join(line[:-7]), line[-7], line[-6], line[-4], line[-2])
