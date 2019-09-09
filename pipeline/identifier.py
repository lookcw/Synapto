def paramToFilename(CONFIG):
    return CONFIG['feature_name'] + "_" + str(CONFIG['data_type']) + "_" + str(CONFIG['num_instances']) + '_instances_' + str(CONFIG['time_points_per_epoch']) + '_epochs_' + str(CONFIG['epochs_per_instance']) + '_timepoints.csv'
def recurrParamToFilename(CONFIG):
    return CONFIG['feature_name'] +"_" + str(CONFIG['data_type']) + "_" + str(CONFIG['num_instances'])+'_instances_'+ str(CONFIG['time_points_per_epoch']) + '_epochs_' + str(CONFIG['epochs_per_instance']) + '_timepoints_recurr.csv'

def filenameToParam(filename):
    line = filename.split('_')
    # feature_name, datatype, num_instances, epochs,timepoints
    return ('_'.join(line[:-7]),line[-7],line[-6],line[-4],line[-2])