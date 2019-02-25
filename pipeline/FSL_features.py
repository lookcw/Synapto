import os
import sys
from subprocess import Popen, PIPE, call
import numpy as np


def extractFSLFeatures(time_series_electrode,l=1, m=10, p=0.049, s=1, x=100, w=410):
    if "TERM_PROGRAM" in os.environ:
        p = Popen(["./FSL_mac", "-l", str(l), "-m", str(m), "-p", str(p), "-s",
                   str(s), "-x", str(x), "-w", str(w)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        inMat = "\n".join([' '.join(x) for x in time_series_electrode])
        output, err = p.communicate(input=inMat)
        mat = [s.strip().split(' ') for s in output.strip().split('\n')]
    else:
        p = Popen(["./FSL_linux", "-l", str(l), "-m", str(m), "-p", str(p), "-s",
                   str(s), "-x", str(x), "-w", str(w)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        inMat = "\n".join([','.join(x) for x in time_series_electrode])
        output, err = p.communicate(input=inMat)
        mat = [s.strip().split(' ') for s in output.strip().split('\n')]
    vec = []
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if j > i:  # gets upper triangular matrix
                vec.append(mat[i][j])
    return map(float, vec)
