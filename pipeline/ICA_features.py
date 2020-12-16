import pandas as pd
from run_regionalization import get_regionalized_header
from regions import regions
import argparse
from scipy import signal
import numpy as np
from sklearn.decomposition import FastICA
import sys
np.random.seed(0)
np.set_printoptions(threshold=sys.maxsize)

parser = argparse.ArgumentParser(description='ICA on features within regions')
parser.add_argument(
    '-fs', '--feature_set', help='feature file to find ICA\'d regions of')
parser.add_argument(
    '-r', '--region', help='name of region schema in regions.py to use')
args = parser.parse_args()

filename = args.feature_set
schema = args.region
out_filename = filename.split('.')[0]+'_ica_'+schema+'.csv'

in_df = pd.read_csv(filename)
pre_ica = in_df.drop(
    columns=['instance code', 'patient num', 'instance num', 'class']).values

schema_header = get_regionalized_header(schema)
post_ica = np.zeros((pre_ica.shape[0], len(schema_header)))
for (i, region) in enumerate(schema_header):
    region_columns = pre_ica[:, regions[schema][region]]
    ica = FastICA(n_components=1)
    post_ica[:, i] = ica.fit_transform(region_columns)[:, 0]

ica_df = pd.DataFrame(data=post_ica, columns=schema_header).join(
    in_df[['instance code', 'patient num', 'instance num', 'class']])
ica_df.to_csv(out_filename, index=False)
print(out_filename)
