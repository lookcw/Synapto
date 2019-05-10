import pandas as pd
import numpy as np

#function to take in feature set and output 3d matrix of elements grouped by instance num
def file_2_recurr_X(features_path):
    df = pd.read_csv(features_path)
    instance_nums = df['instance num']
    max_instance = int(instance_nums.iloc[-1])
    epochs_per_instance = len(df.loc[df['instance num'] == 1])
    groups = np.zeros((75,epochs_per_instance,len(df.columns) - 3))
    y = df.groupby(['instance num']).first()['class']
    for i in range(1,max_instance+1):
        groups[i-1] = df.loc[df['instance num'] == i].drop(columns = ['patient num','class','instance num']).values
    print len(y),len(groups)
    return (groups,y)
## a test if you want to see how this function works
# file_2_recurr_X('FeatureSets/Brazil3instances_10_epochs4000_timepoints.csv')