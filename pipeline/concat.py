import pandas as pd
import argparse
from identifier import filenameToParam, paramToFilename

#run using `python concat.py <filename1> <filename2> <filenameN>` it will output to the current directory.

def concatSets(df1,df2):
    print(df1)
    print(df2)
    new_df = pd.merge(df1, df2,  how='outer', left_on=['instance code','patient num','class'], right_on = ['instance code','patient num','class'])
    if(new_df.isnull().values.any()):
        raise Exception("featureSet Shapes do not match, try correct files")
    else:
        return new_df


parser = argparse.ArgumentParser()
parser.add_argument("input", nargs='+')
args = parser.parse_args()

curr_df = pd.read_csv(args.input[0])
# first_params = filenameToParam(args.input[0].split('/')[-1])

# features = [first_params[0]]
for i in range(len(args.input)-1):
    # curr_params = filenameToParam(args.input[i+1].split('/')[-1])
    # for j in range(1,4):
        # if curr_params[i] != curr_params[i]:
        #     raise Exception("these two files were not created with the same parameters")
    # features.append(curr_params[0])
    curr_df = concatSets(curr_df,pd.read_csv(args.input[i+1]))

# file_features = '_'.join(features)
# config = {
#     'feature_name':first_params[0],
#     'data_type':first_params[1],
#     'num_instances':first_params[2],
#     'time_points_per_epochs':first_params[3],
#     'epochs_per_instance':first_params[1],
# }
# co
# filename =  paramToFilename(file_features,first_params[1],first_params[2],first_params[3],first_params[4])
curr_df.to_csv('concatted.csv', index=False)



