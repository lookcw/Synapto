import os
import pandas as pd
import sys

count = 1
for filename in os.listdir('/Users/Anoop/Downloads/AD_csv'):
    if filename.endswith('.xlsx'):
        dfList = []
        for f in os.listdir('/Users/Anoop/Downloads/AD_csv/' + filename):
            if f[len(f)-1] != '3':
                print(f)
                path = '/Users/Anoop/Downloads/AD_csv/' + filename + '/' + f
                df = pd.read_csv(path, header=None)
                df = df.drop(df.columns[0], axis=1)
                dfList.append(df)
        concatDf = pd.concat(dfList, axis=1)
        concatDf.to_csv('/Users/Anoop/Documents/Neuronetrix/AD/AD' + str(count) + '.csv', index=None, header=None)
        count += 1



count = 1
for filename in os.listdir('/Users/Anoop/Downloads/HC_csv'):
    if filename.endswith('.xlsx'):
        dfList = []
        for f in os.listdir('/Users/Anoop/Downloads/HC_csv/' + filename):
            if f[len(f)-1] != '3':
                print(f)
                path = '/Users/Anoop/Downloads/HC_csv/' + filename + '/' + f
                df = pd.read_csv(path, header=None)
                df = df.drop(df.columns[0], axis=1)
                dfList.append(df)
        concatDf = pd.concat(dfList, axis=1)
        concatDf.to_csv('/Users/Anoop/Documents/Neuronetrix/HC/HC' + str(count) + '.csv', index=None, header=None)
        count += 1
