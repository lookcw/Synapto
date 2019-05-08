def paramToFilename(feature_name, datatype, num_instances ,num_timePoints, epochs_per_instance):
    return feature_name +"_" + str(datatype) + str(num_instances)+'instances_'+ str(epochs_per_instance) + '_epochs' + str(num_timePoints) + '_timepoints.csv'
def recurrParamToFilename(feature_name, datatype, num_instances ,num_timePoints, epochs_per_instance):
    return feature_name +"_" +str(datatype) + str(num_instances)+'instances_'+ str(epochs_per_instance) + '_epochs' + str(num_timePoints) + '_timepoints_recurr.csv'