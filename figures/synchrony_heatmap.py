import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import genfromtxt

filename = 'FSL_diff_Heatmap.csv'
data = pd.read_csv(filename,delimiter=',')
data = data.set_index('region')
print(data)
ax = sns.heatmap(
    data, 
    vmin=0, vmax=0.05, center=.025,
    cmap="Greens",
    square=True,
    annot=True,
    annot_kws={"fontsize":12}
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right',
    fontsize = 12

)
fig = ax.get_figure()
plt.tight_layout()
plt.show()
fig.savefig(f'{filename.split("/")[-1].split(".")[0]}')
