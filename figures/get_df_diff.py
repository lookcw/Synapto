import pandas as pd



hc_df = pd.read_csv('FSL_HC_Heatmap.csv').set_index('region').astype(float)
ad_df = pd.read_csv('FSL_AD_Heatmap.csv').set_index('region').astype(float)

new_df = ad_df - hc_df

new_df.to_csv('FSL_diff_Heatmap.csv')