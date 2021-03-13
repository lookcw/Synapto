import numpy as np
import pandas as pd
import click
import ast
from ast import literal_eval
from statistics import stdev, mean
import matplotlib.pyplot as pl

import csv

ICA_SUMMARY_FOLDER = 'Unmixing_Mats/Summaries/'
ICA_FIGURE_FOLDER = 'Unmixing_Mats/Figures/'


@click.command()
@click.argument('filename')
def summarize_and_hist_ICA(filename):
    ica_coeff_df = pd.read_csv(filename)
    file_prefix = filename.split('/')[-1].split('.')[0]
    with open(ICA_SUMMARY_FOLDER + file_prefix+'_summary.csv', 'w') as summary_file:
        writer = csv.writer(summary_file)
        HEADER = ['region', 'mean', 'stdev']
        for col in ica_coeff_df.columns:
            pl.clf()
            all_vals = [literal_eval(x)[1]
                        for x in ica_coeff_df[col].dropna().tolist()]
            fig = pl.hist(all_vals)
            pl.title(col)
            pl.xlabel('Unmixing Matrix value')
            pl.ylabel("Frequency")
            pl.savefig(ICA_FIGURE_FOLDER+file_prefix + '_' + col + '.png')
            writer.writerow([col, mean(all_vals), stdev(all_vals)])


if __name__ == '__main__':
    summarize_and_hist_ICA()
