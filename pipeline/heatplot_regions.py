import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

filename = sys.argv[1]
indices = sys.argv[2]

data = pd.read_csv(filename)
data = data.drop(columns=['instance num','instance code','class','patient num'], errors='ignore')
# print(data)
for k, v in indices.items():
    for region_name, col_indices in v.items():

        print(data)
        # region_data = pd.DataFrame(data, index=col_indices, columns=col_indices)
        region_data = data.iloc[col_indices, col_indices]
        print(region_data)

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
        fig.savefig(f'{filename.split("/")[-1].split(".")[0]}')
        plt.show()