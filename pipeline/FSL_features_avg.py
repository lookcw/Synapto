import os
import sys
from subprocess import Popen, PIPE, call
import numpy as np
from headers import compareHeader

def getHeader(time_series_electrode):
    return compareHeader(time_series_electrode)

def extractFeatures(time_series_electrode, config_feature):
    time_series_electrode = time_series_electrode.astype(str)
    if "TERM_PROGRAM" in os.environ:
        p = Popen(["./FSL_mac", "-l", "1", "-m", "10", "-p", "0.049", "-s",
                   "1", "-x", "200", "-w", "2000"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        inMat = "\n".join([','.join(x) for x in time_series_electrode]).encode('utf-8')
        output, err = p.communicate(input=inMat)
        mat = [s.strip().split(' ') for s in output.decode().strip().split('\n')]
    else:
        p = Popen(["./FSL_linux", "-l", "1", "-m", "10", "-p", "0.049", "-s",
                   "1", "-x", "200", "-w", "2000"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        inMat = "\n".join([','.join(x) for x in time_series_electrode]).encode('utf-8')
        output, err = p.communicate(input=inMat)
        mat = [s.strip().split(' ') for s in output.decode().strip().split('\n')]
    
    return list(map(float, vec))


    # Instead of getting the upper triangular matrix, get average value for each electrode (avoid comparing same electrode but get value for everything else)
    # After getting the electrode values for each comparision, get the mean and append this value to vec which holds the feature values of interest
    vec = []
    for i in range(len(mat)):
        avg_elec = []
        for j in range(len(mat[0])):
            if i not j:
                avg_elec.append(mat[i][j])
        vec.append(np.mean(avg_elec))
    return list(map(float, vec))


def config_to_filename(config_feature):
    return str(config_feature['l']) + "_l_" + str(config_feature['m']) + "_m_" + str(config_feature['p']) + '_p_' + str(config_feature['s']) + '_s_' + str(config_feature['x']) + '_x_' + str(config_feature['w']) + '_w_.csv'
    
    