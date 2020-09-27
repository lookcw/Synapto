import numpy as np
from functools import reduce
from statistics import mean
from regions import regions



def regionalize(feature_set,region_name):
    feature_set = np.array(feature_set)
    _validate_regions(feature_set,regions[region_name])
    return _regionalize(feature_set,regions[region_name])

def get_regionalized_header(region_name):
    """Returns column headers of regionalized electrodes

    Args:
        region_name (str): name of regionalization schema

    Returns:
        [str]: list of headers
    """
    return sorted(regions[region_name].keys())

def _validate_regions(feature_set,regions):
    """Checks if the regions match feature_set (number of electrodes
     and checks if all indicies are in the regions)

    Args:
        feature_set (flat numpy array) patient features
        regions (dict str -> [int]): dict describing region 
        to list of electrode indices
    """
    sorted_electrodes = sorted(reduce((lambda x,key: x+(regions[key])),regions,[]))
    if not sorted_electrodes == list(range(feature_set.shape[2])):
        raise AssertionError("regionalization type does not match electrode set")
        

def _regionalize(feature_set,regions):
    """Averages the feature data per region, collapses features for
    regions of electrodes into features for one 'regional electrode'
    Regions must be sorted because ordering of keys in dictionary is 
    not deterministic, and so must standardize region orderings of 
    final featureset

    Args:
        feature_set (flat numpy array) patient features
        regions (dict str -> [int]): dict describing region 
        to list of electrode indices
    """
    regionalized = []
    sorted_region_names = sorted(regions.keys())
    for region in sorted_region_names:
        regionalized.append(np.mean([feature_set[0][0][e] for e in regions[region]]))
    return [[regionalized]]
