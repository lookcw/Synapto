from headers import compareHeader
from headers import linearHeader
import numpy as np

def getHeader(time_series_electrode):
   return linearHeader(time_series_electrode)

def extractFeatures(time_series_electrode):
   print("SHAPE")

   print(time_series_electrode.shape)
   return list(time_series_electrode[0])
   #flat = time_series_electrode.flatten()
   #return flat
