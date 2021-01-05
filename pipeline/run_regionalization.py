import numpy as np
from functools import reduce
from statistics import mean
from regions import regions
from headers import ordered_linear_region_header,\
    ordered_compare_region_header,\
    ordered_compare_region_pairs
from math import sqrt
from file_helper import split_df_from_file, rejoin_np_arr_with_df, write_unmixing_matrix
from sklearn.decomposition import FastICA


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
        num_electrodes = int((1 + sqrt(1+8*feature_set.shape[1])) / 2)
    sorted_electrodes = sorted(
        reduce((lambda x, key: x+(regions[key])), regions, []))
    if not sorted_electrodes == list(range(num_electrodes)):
        raise AssertionError(
            "regionalization type does not match electrode set")


def run_regionalization_from_path(feature_path, config, config_feature):
    (feature_set, extra_cols) = split_df_from_file(feature_path)
    (regionalized, headers) = run_regionalization(
        feature_set, config, config_feature)
    return rejoin_np_arr_with_df(extra_cols, regionalized, headers)


def run_regionalization(feature_set, config, config_feature):
    regionalization_type = config['regionalization_type']
    region_name = config['regionalization']
    feature_type = config['feature_type']
    feature_set = np.array(feature_set)
    _validate_regions(feature_set, feature_type, regions[region_name])
    schema = regions[region_name]
    if regionalization_type == 'average' and feature_type == 'linear':
        return (_linear_regionalize(feature_set, schema, _calc_avg),
                ordered_linear_region_header(region_name))
    elif regionalization_type == 'average' and feature_type == 'compare':
        return (_compare_regionalize(feature_set, schema, _calc_avg),
                ordered_compare_region_header(region_name))
    elif regionalization_type == 'ICA' and feature_type == 'linear':
        ((res, mixing_mat), header) = (_linear_regionalize(feature_set, schema, _calc_ica),
                                       ordered_linear_region_header(region_name))
        write_unmixing_matrix(ordered_linear_region_header(region_name),
                              mixing_mat,
                              config_feature['regionalized_filepath'])
        return (res, header)
    elif regionalization_type == 'ICA' and feature_type == 'compare':
        ((res, mixing_mat), header) = (_compare_regionalize(feature_set, schema, _calc_ica),
                                       ordered_compare_region_header(region_name))
        write_unmixing_matrix(ordered_compare_region_header(region_name),
                              mixing_mat,
                              config_feature['regionalized_filepath'])
        return (res, header)


def _calc_ica(region_features):
    ica = FastICA(n_components=1, whiten=True)
    transformed = ica.fit_transform(region_features)[:, 0]
    A_ = ica.mixing_.flatten()
    return (transformed, A_)


def _calc_avg(region_features):
    num_features = region_features.shape[0]
    mixing_mat = num_features * [1/num_features]
    return (np.mean(region_features, axis=1),  mixing_mat)


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
    mixing_mat = []
    for (i, region) in enumerate(ordered_region_names):
        region_columns = feature_set[:, regions[region]]
        regionalization_result = regionalization_func(region_columns)
        regionalized[:, i] = regionalization_result[0]
        mixing_mat.append((zip(regions[region], regionalization_result[1])))
    return (np.array(regionalized), mixing_mat)


def _compare_regionalize(feature_set, regions, regionalization_func):
    # used quadratic formula to get this number
    num_electrodes = int((1 + sqrt(1+8*feature_set.shape[1])) / 2)
    num_subjects = len(feature_set)
    correlation_matrices = np.zeros(
        (num_subjects, num_electrodes, num_electrodes))
    l_idx = np.tril_indices(num_electrodes, -1)
    u_idx = np.triu_indices(num_electrodes, 1)
    for i in range(num_subjects):
        correlation_matrices[i][l_idx] = feature_set[i]
        correlation_matrices[i][u_idx] = feature_set[i]

    num_regions = len(regions)
    regionalized_matrix = np.ones((num_subjects, num_regions, num_regions))
    ordered_region_names = ordered_linear_region_header(regions)
    mixing_mat = []
    i,j = 0,1 #first triangle index
    for (region_name1, region_name2) in ordered_compare_region_pairs(regions):
        region1 = np.array(regions[region_name1])
        region2 = np.array(regions[region_name2])
        region_features = correlation_matrices[:, region1[:, None], region2]
        region_flattened = region_features.reshape(num_subjects, -1)
        print(region_flattened.shape)
        regionalized = regionalization_func(region_flattened)
        regionalized_matrix[:, i, j] = regionalized[0]
        regionalized_matrix[:, j, i] = regionalized[0]
        i,j = increment_tri_inds(i,j,num_regions)
        mixing_mat.append(regionalized[1])
    return (regionalized_matrix[:, np.triu_indices(num_regions, 1)[0],
                                np.triu_indices(num_regions, 1)[1]],
            mixing_mat
            )


def increment_tri_inds(i, j, length):
    if j == length - 1:
        i += 1
        j = i+1
    else:
        j += 1
    return (i,j)
