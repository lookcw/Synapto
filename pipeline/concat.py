import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("input", nargs='+')
args = parser.parse_args()

curr_df = pd.read_csv(args.input[0])
for i in range(len(args.input)-1):
    curr_df = concatSets(curr_df,pd.read_csv(args.input[i]))

curr_df.to_csv(index=False)


def concatSets(df1,df2):
    new_df = pd.merge(df1, df2,  how='outer', left_on=['instance code','patient num','instance num','class'], right_on = ['instance code','patient num','instance num','class'])
    if(new_df.isnull().values.any()):
        raise Exception("featureSet Shapes do not match, try correct files")
    else:
        return new_df

