import os
import sys
from subprocess import Popen, PIPE, call
import numpy as np
from headers import compareHeader, linearHeader
from average_heatmap import average_heatmap, regions_header


def getHeader(time_series_electrode, config_feature):
    if config_feature['compress']:
        return linearHeader(time_series_electrode)
    else:
        return compareHeader(time_series_electrode)


def extractFeatures(time_series_electrode, config_feature):
    time_series_electrode = time_series_electrode.astype(str)
    numElectrodes = len(time_series_electrode[0])
    options = list(map(str,[
        "-l", config_feature['l'],
        "-m", config_feature['m'],
        "-p", config_feature['p'],
        "-s", config_feature['s'],
        "-x", config_feature['x'],
        "-w", config_feature['w']
      ]))

    if "TERM_PROGRAM" in os.environ:
        p=Popen(["./FSL_mac"] + options, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        inMat="\n".join([' '.join(x)
                           for x in time_series_electrode]).encode('utf-8')
        output, err=p.communicate(input=inMat)
        mat=[s.strip().split(' ')
               for s in output.decode().strip().split('\n')]
    else:
        p=Popen(["./FSL_linux"] + options,
                stdin=PIPE, stdout=PIPE, stderr=PIPE)
        inMat="\n".join([','.join(x)
                           for x in time_series_electrode]).encode('utf-8')
        output, err=p.communicate(input=inMat)
        mat=np.array([s.strip().split(' ')
                        for s in output.decode().strip().split('\n')]).astype(float)
    if config_feature['compress']:
        # subtracting 2 because every electrode always has a 1 in its column
        return (np.sum(mat, axis=1) - 1)/numElectrodes
    else:
        return mat[np.triu_indices(numElectrodes, 1)]


def config_to_filename(config_feature):
    no_filename_config = {i:config_feature[i] for i in config_feature if 'file' not in i}
    return str(no_filename_config)[1:-1].replace(' ', '').replace('\'', '')
