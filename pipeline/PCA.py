# Reduces features way too much
# Feature Extraction with PCA -> does not have feature importance
# import numpy
# from pandas import read_csv
# from sklearn.decomposition import PCA
# # feature extraction
# pca = PCA(n_components=3)
# fit = pca.fit(X)
# get_feature_importance(fit, X)
# X_reduced = fit.transform(X)
# print(X_reduced.shape)
# # summarize components
# print("Explained Variance: %s") % fit.explained_variance_ratio_
# feature_red_name = format(fit)
# print(fit.components_)