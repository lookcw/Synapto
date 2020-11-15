import numpy as np
from functools import reduce
from statistics import mean
from regions import regions
from headers import ordered_linear_region_header, ordered_compare_region_header
from math import sqrt
from file_helper import split_df_from_file, rejoin_np_arr_with_df


def _validate_regions(feature_set, feature_type, regions):
    """Checks if the regions match feature_set (number of electrodes
     and checks if all indicies are in the regions)

    Args:
        feature_set (flat numpy array) patient features
        regions (dict str -> [int]): dict describing region
        to list of electrode indices
    """
    if feature_type == 'linear':
        num_electrodes = feature_set.shape[1]
    elif feature_type == 'compare':
        num_electrodes = (1 + sqrt(1+8*feature_set.shape[1])) / 2
    sorted_electrodes = sorted(
        reduce((lambda x, key: x+(regions[key])), regions, []))
    if not sorted_electrodes == list(range(num_electrodes)):
        raise AssertionError(
            "regionalization type does not match electrode set")


def run_regionalization_from_path(feature_path, regionalization_type, feature_type, region_name):
    (feature_set, extra_cols) = split_df_from_file(feature_path)
    (regionalized, headers) = run_regionalization(
        feature_set, regionalization_type, feature_type, region_name)
    return rejoin_np_arr_with_df(extra_cols, regionalized, headers)


def run_regionalization(feature_set, regionalization_type, feature_type, region_name):
    feature_set = np.array(feature_set)
    _validate_regions(feature_set, feature_type, regions[region_name])
    schema = regions[region_name]
    if regionalization_type == 'average' and feature_type == 'linear':
        return (_linear_regionalize(feature_set, schema, _calc_avg),
                ordered_linear_region_header(region_name))
    elif regionalization_type == 'average' and feature_type == 'compare':
        return (_compare_regionalize(feature_set, schema, _calc_avg),
                ordered_linear_region_header(region_name))
    elif regionalization_type == 'ICA' and feature_type == 'linear':
        return (_linear_regionalize(feature_set, schema, _calc_ica),
                ordered_compare_region_header(region_name))
    elif regionalization_type == 'ICA' and feature_type == 'compare':
        return (_compare_regionalize(feature_set, schema, _calc_ica),
                ordered_compare_region_header(region_name))


def _calc_ica(region_features):
    ica = FastICA(n_components=1)
    return ica.fit_transform(region_features)[:, 0]


def _calc_avg(region_features):
    return np.mean(region_features, axis=1)


def _linear_regionalize(feature_set, regions, regionalization_func):
    """gets the ICA of the feature data per region, collapses features for
    regions of electrodes into features for one 'regional electrode'
    Regions must be sorted because ordering of keys in dictionary is
    not deterministic, and so must standardize region orderings of
    final featureset

    Args:
        feature_set (flat numpy array) patient features
        regions (dict str -> [int]): dict describing region
        to list of electrode indices
    """
    ordered_region_names = ordered_linear_region_header(regions)
    regionalized = np.zeros((feature_set.shape[0], len(regions)))
    for (i, region) in enumerate(ordered_region_names):
        region_columns = feature_set[:, regions[region]]
        regionalized[:, i] = regionalization_func(region_columns)
    return np.array(regionalized)


def _compare_regionalize(feature_set, regions, regionalization_func):
    # used quadratic formula to get this number
    num_electrodes = (1 + sqrt(1+8*len(feature_set))) / 2
    num_subjects = len(feature_set)
    correlation_matrices = np.zeros(
        (num_subjects, num_electrodes, num_electrodes))
    l_idx = np.tril_indices(num_electrodes, -1)
    u_idx = np.triu_indices(num_electrodes, 1)
    for i in num_subjects:
        correlation_matrix[i][l_idx] = feature_set.iloc[i]
        correlation_matrix[i][u_idx] = feature_set.iloc[i]

    num_regions = len(regions)
    regionalized_matrix = np.ones((num_regions, num_regions))
    ordered_region_names = ordered_region_header(regions)

    for i in range(len(ordered_region_names)):
        region1 = np.array(regions[sorted_region_names[i]])
        for j in range(len(ordered_region_names)):
            if i >= j:
                region2 = np.array(regions[sorted_region_names[j]])
                region_features = correlation_matrix[:,
                                                     region1[:, None], region2]
                region_flattened = region_features.reshape(num_subjects, -1)
                regionalized = regionalization_function(region_flattened)
                regionalized_matrix[:, i, j] = regionalized
                regionalized_matrix[:, j, i] = regionalized
    return regionalized_matrix[:, np.triu_indices(num_regions, 1)]
