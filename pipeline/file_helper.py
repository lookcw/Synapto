import os
import re
import pandas as pd
import numpy as np

EXTRA_COLUMNS = ['instance code', 'patient num', 'instance num', 'class']


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
    print(np_arr.shape)
    df = pd.concat([extra_cols, pd.DataFrame(data=np_arr, columns=header)], axis = 1)
    # Make a list of all of the columns in the df
    cols = list(df.columns.values)
    cols.pop(cols.index('class'))  # Remove b from list
    # Create new dataframe with columns in the order you want
    df = df[cols+['class']]
    return df
