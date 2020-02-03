import pandas as pd
import argparse
import seaborn as sns
import matplotlib.pyplot as plt 


parser = argparse.ArgumentParser()
parser.add_argument("-i", help="input feature file to save model for")
args = parser.parse_args()
in_filename = args.i

dataset = pd.read_csv(in_filename).drop(columns=['instance code','patient num','instance num'])
meaned = dataset.groupby(['class']).mean()
print(meaned)
diff_percent = (meaned.loc[1]-meaned.loc[0])/meaned.loc[0]
print(diff_percent)
high_ax = diff_percent.nlargest(10).plot.bar(rot=90)
high_ax.set_title('higher')
plt.show()
low_ax = diff_percent.nsmallest(10).plot.bar(rot=90)
low_ax.set_title('lower')
plt.show()