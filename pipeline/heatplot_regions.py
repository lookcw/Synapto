import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from regions import regions
import numpy as np
from statistics import stdev
import csv
import click
WITHIN_ENUM = 'within'
BETWEEN_ENUM = 'between'
WITHIN_REGION_CORRELATION_FOLDER='Cross_Corr/Within_Region/'
BETWEEN_REGION_CORRELATION_FOLDER = 'Cross_Corr/Between_Region/'
HEADER_STATS = ['MEAN', 'STDEV']
SUMMARY_FOLDER = 'Cross_Corr/Summaries/'

# Specify filename and type of regions that you want to extract (find names of regions in regions.py - spectral_126, spectral_128, etc.)

def write_within_heatmap(filename, schema_name):

    # Extract indices (a dictionary) that contains information about electrodes contained in each region 
    indices = regions[schema_name]

    # Extract data from csv
    data = pd.read_csv(filename)
    data = data.drop(columns=['instance num','instance code','class','patient num'], errors='ignore')

    for region_name, col_indices in indices.items():
        
        print(col_indices)
        # Extract columns from particular region 
        region_data = data.iloc[:, col_indices] 

        # Plot correlation heatmap for region 
        corr = region_data.corr()
        corr_filename = filename.split('/')[-1].split(".")[0]+'_'+region_name+'.csv'
        np.savetxt(WITHIN_REGION_CORRELATION_FOLDER+corr_filename, corr.values, delimiter=",")        
        ax = sns.heatmap(
            corr, 
            vmin=-1, vmax=1, center=0,
            cmap=sns.diverging_palette(20, 220, n=200),
            square=True,
            annot_kws={"fontsize":7}
        )
        ax.set_xticklabels(
            ax.get_xticklabels(),
            rotation=45,
            horizontalalignment='right'
        )
        ax.set_title(region_name)
        fig = ax.get_figure()
        plt.tight_layout()
        # fig.savefig(f'{filename.split("/")[-1].split(".")[0]}')
        plt.show()
    write_within_corr_stats(filename,schema_name)


def get_corr_stats(corr_mat):
    num_features = corr_mat.shape[0]
    tri_inds = np.triu_indices(num_features, 1)
    all_corr = corr_mat[tri_inds]
    return[np.mean(all_corr), stdev(all_corr)]


def write_within_corr_stats(filename, region_name):
    schema = regions[region_name]
    file_prefix = WITHIN_REGION_CORRELATION_FOLDER+filename.split('/')[-1].split('.')[0]
    summary_prefix = '_'.join(file_prefix.split('/')[-1].split('_')[:-1])
    with open(SUMMARY_FOLDER+summary_prefix+'_summary'+'.csv', 'w+') as summary_file:
        writer = csv.writer(summary_file)
        writer.writerow(['region'] + HEADER_STATS)
        for region in schema:
            filename = file_prefix+'_'+region+'.csv'
            corr_mat = np.genfromtxt(filename, delimiter=',')
            writer.writerow([region] + get_corr_stats(corr_mat))


def write_between_heatmap(filename):
    data = pd.read_csv(filename)
    data = data.drop(columns=['instance num','instance code','class','patient num'], errors='ignore')
    corr = data.corr().abs()
    corr_filename = filename.split('/')[-1]
    np.savetxt(BETWEEN_REGION_CORRELATION_FOLDER+corr_filename, corr.values, delimiter=",")        

    ax = sns.heatmap(
        corr, 
        vmin=-1, vmax=1, center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=True,
        annot=True,
        annot_kws={"fontsize":7}
    )
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        horizontalalignment='right'
    )
    fig = ax.get_figure()
    plt.tight_layout()
    # fig.savefig(f'{filename.split("/")[-1].split(".")[0]}')
    plt.show()
    write_between_corr_stats(filename,corr.values)

def write_between_corr_stats(filename,corr_mat):
    file_prefix = BETWEEN_REGION_CORRELATION_FOLDER+filename.split('/')[-1].split('.')[0]
    summary_prefix = '_'.join(file_prefix.split('/')[-1].split('_')[:-1])
    with open(SUMMARY_FOLDER+summary_prefix+'_summary'+'.csv', 'w+') as summary_file:
        writer = csv.writer(summary_file)
        writer.writerow(HEADER_STATS)
        writer.writerow(get_corr_stats(corr_mat))

@click.command()
@click.argument('filename')
@click.option('--schema_name')
@click.option('--corr_type', default=BETWEEN_ENUM)
def main(filename, schema_name, corr_type):
    if corr_type == BETWEEN_ENUM:
        write_between_heatmap(filename)
    else:
        write_within_heatmap(filename, schema_name)


if __name__ == '__main__':
    main()