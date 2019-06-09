import os
import sys
from subprocess import Popen, PIPE, call
import numpy as np


def extractFSLFeatures(time_series_electrode):
    time_series_electrode = time_series_electrode.astype(str)
    if "TERM_PROGRAM" in os.environ:
        p = Popen(["./FSL_mac", "-l", "1", "-m", "10", "-p", "0.049", "-s",
                   "1", "-x", "200", "-w", "2000"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        inMat = "\n".join([' '.join(x) for x in time_series_electrode])
        output, err = p.communicate(input=inMat)
        mat = [s.strip().split(' ') for s in output.strip().split('\n')]
    else:
        p = Popen(["./FSL_linux", "-l", "1", "-m", "10", "-p", "0.049", "-s",
                   "1", "-x", "200", "-w", "2000"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        inMat = "\n".join([','.join(x) for x in time_series_electrode])
        output, err = p.communicate(input=inMat)
        mat = [s.strip().split(' ') for s in output.strip().split('\n')]
    vec = []
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if j > i:  # gets upper triangular matrix
                vec.append(mat[i][j])
    return map(float, vec)
