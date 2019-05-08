def paramToFilename(datatype, num_instances ,num_timePoints, epochs_per_instance):
    return str(datatype) + str(num_instances)+'instances_'+ str(epochs_per_instance) + '_epochs' + str(num_timePoints) + '_timepoints.csv'
def recurrParamToFilename(datatype, num_instances ,num_timePoints, epochs_per_instance):
    return str(datatype) + str(num_instances)+'instances_'+ str(epochs_per_instance) + '_epochs' + str(num_timePoints) + '_timepoints_recurr.csv'