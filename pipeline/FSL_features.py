import os
import sys
from subprocess import Popen, PIPE, call
import numpy as np
from headers import compareHeader, linearHeader


def getHeader(time_series_electrode, config_feature):
    if config_feature['compress']:
        return linearHeader(time_series_electrode)
    else:
        return compareHeader(time_series_electrode)


def extractFeatures(time_series_electrode, config_feature):
    time_series_electrode = time_series_electrode.astype(str)
    numElectrodes = len(time_series_electrode[0])
    if "TERM_PROGRAM" in os.environ:
        p = Popen(["./FSL_mac", "-l", "1", "-m", "10", "-p", "0.049", "-s",
                   "1", "-x", "200", "-w", "2000"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        inMat = "\n".join([','.join(x)
                           for x in time_series_electrode]).encode('utf-8')
        output, err = p.communicate(input=inMat)
        mat = [s.strip().split(' ')
               for s in output.decode().strip().split('\n')]
    else:
        p = Popen(["./FSL_linux", "-l", "1", "-m", "10", "-p", "0.049", "-s",
                   "1", "-x", "200", "-w", "2000"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        inMat = "\n".join([','.join(x)
                           for x in time_series_electrode]).encode('utf-8')
        output, err = p.communicate(input=inMat)
        mat = np.array([s.strip().split(' ')
                        for s in output.decode().strip().split('\n')]).astype(float)
    if config_feature['compress']:
        # subtracting 2 because every electrode always has a 1 in its column
        return (np.sum(mat, axis=1) - 1)/numElectrodes
    elif config_feature['regions']:
        region_corr_mat = average_heatmap(corr_mat)
        return region_corr_mat[np.triu_indices(numElectrodes, 1)]
    else:
        return mat[np.triu_indices(numElectrodes, 1)]


def config_to_filename(config_feature):
    return str(config_feature)[1:-1].replace(' ','').replace('\'','')
