import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from regions import regions

# Specify filename and type of regions that you want to extract (find names of regions in regions.py - spectral_126, spectral_128, etc.)
filename = sys.argv[1]
region_name = sys.argv[2]

# Extract indices (a dictionary) that contains information about electrodes contained in each region 
indices = regions[region_name]

# Extract data from csv
data = pd.read_csv(filename)
data = data.drop(columns=['instance num','instance code','class','patient num'], errors='ignore')

for region_name, col_indices in indices.items():

    print(col_indices)
    # Extract columns from particular region 
    region_data = data.iloc[:, col_indices] 

    # Plot correlation heatmap for region 
    corr = region_data.corr()
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
    ax.set_title(region_name)
    fig = ax.get_figure()
    plt.tight_layout()
    # fig.savefig(f'{filename.split("/")[-1].split(".")[0]}')
    plt.show()