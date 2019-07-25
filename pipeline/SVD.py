from sklearn.decomposition import TruncatedSVD
import numpy as np
import pandas as pd
import sys

def svd(features_path, n):
    df = pd.read_csv(features_path)
<<<<<<< HEAD
    df1 = df.drop(['instance code', 'patient num', 'instance num'], axis=1)
=======
    df1 = df.drop(['patient num', 'instance num'], axis=1)
>>>>>>> Fixing Anoop branch
    print(df1)
    X = df1.values
    svd = TruncatedSVD(n_components=n, n_iter=7, random_state=42)
    X_trans = svd.fit_transform(X)
    print(X_trans.shape)
    SVD_features_path = features_path.split('.')[0] + '_SVD.' + features_path.split('.')[1]
<<<<<<< HEAD
    df_SVD = pd.concat([df[['instance code', 'patient num', 'instance num']],pd.DataFrame(X_trans)], axis=1)
=======
    df_SVD = pd.concat([df[['patient num', 'instance num']],pd.DataFrame(X_trans)], axis=1)
>>>>>>> Fixing Anoop branch
    df_SVD = pd.concat([df_SVD, df[['class']]], axis=1)
    print(df_SVD)
    df_SVD.to_csv(SVD_features_path, index=False)

# X = np.array([[4,5,4,5,6],[1,2,5,2,1], [4,23,5,3,2]])
# print(X)
# svd = TruncatedSVD(n_components=2, n_iter=7, random_state=42)
# X = svd.fit_transform(X)  
# print(X)