def paramToFilename(feature_name, datatype, num_instances ,num_timePoints, epochs_per_instance):
    return feature_name +"_" + str(datatype) + "_" + str(num_instances)+'_instances_'+ str(epochs_per_instance) + '_epochs_' + str(num_timePoints) + '_timepoints.csv'
def recurrParamToFilename(feature_name, datatype, num_instances ,num_timePoints, epochs_per_instance):
    return feature_name +"_" + str(datatype) + "_" + str(num_instances)+'_instances_'+ str(epochs_per_instance) + '_epochs_' + str(num_timePoints) + '_timepoints_recurr.csv'

def filenameToParam(filename):
    line = filename.split('_')
    #feature_name, datatype, num_instances, epochs,timepoints
    return ('_'.join(line[:-7]),line[-7],line[-6],line[-4],line[-2])