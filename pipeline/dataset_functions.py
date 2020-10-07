import pandas 

def split_dataframe(df):
    X = df.drop(['patient num', 'instance num',
                 'instance code', 'class'], axis=1, errors='ignore').values
    y = df['class'].values
    groups = df['patient num'].values
    instance_nums =  df['instance num'].values if 'instance num' in df else []
    return (X, y, groups, instance_nums)
