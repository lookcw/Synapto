import pandas 

def split_dataframe(df):
    X = df.drop(['patient num', 'instance num',
                 'instance code', 'class'], axis=1, errors='ignore')
    columns = X.columns
    y = df['class'].values
    groups = df['patient num'].values
    instance_nums =  df['instance num'].values if 'instance num' in df else []
    return (X.values, y, groups, instance_nums, columns)
