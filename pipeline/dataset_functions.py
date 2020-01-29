import pandas

def split_dataframe(df):
    X = df.drop(['patient num', 'instance num',
                 'instance code', 'class'], axis=1).values
    y = df['class'].values
    groups = df['patient num'].values
    instance_nums = df['instance num'].values
    return (X, y, groups, instance_nums)
