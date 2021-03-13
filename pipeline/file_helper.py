import os
import re
import pandas as pd
import numpy as np
import csv
import itertools

EXTRA_COLUMNS = ['instance code', 'patient num', 'instance num', 'class']
UNMIXING_MATRIX_FOLDER = 'Unmixing_Mats'



def get_files_matched_by_regex(folder_path, regex):
    return [f for f in os.listdir(folder_path) if re.match(regex, f)]


def split_df_from_file(file_path):
    df = pd.read_csv(file_path)
    extra_cols = df[EXTRA_COLUMNS]
    numpy_arr = df.drop(columns=EXTRA_COLUMNS).to_numpy()
    return (numpy_arr, extra_cols)


def write_feature_set(feature_path, feature_set_df):
    print('writing feature set to file')
    feature_set_df.to_csv(feature_path, index=False)


def rejoin_np_arr_with_df(extra_cols, np_arr, header):
    print(extra_cols)
    print(np_arr[0].shape)
    df = pd.concat([extra_cols, pd.DataFrame(
        data=np_arr[0], columns=header)], axis=1)
    # Make a list of all of the columns in the df
    cols = list(df.columns.values)
    cols.pop(cols.index('class'))  # Remove b from list
    # Create new dataframe with columns in the order you want
    df = df[cols + ['class']]
    return df

def transpose_no_loss(lst):
    return list(map(list, itertools.zip_longest(*lst, fillvalue=None)))

def write_unmixing_matrix(ordered_region_header, mixing_mat, feature_filepath):
    unmixing_filepath = UNMIXING_MATRIX_FOLDER + '/' + \
                        feature_filepath.split('/')[-1] \
                        .split('.')[0] + '_A_.csv'
    
    to_write = transpose_no_loss(mixing_mat)
    with open(unmixing_filepath,'w') as f:
        writer = csv.writer(f)
        writer.writerow(ordered_region_header)
        writer.writerows(to_write)
    
