# Reduces features way too much
# Select K Best - no feature importance 
# from sklearn.feature_selection import SelectKBest
# from sklearn.feature_selection import chi2
# # feature extraction
# clf = SelectKBest(score_func=chi2, k=4)
# clf = clf.fit(X, y)

# This clf does NOT have a feature importance feature 

# # summarize scores
# np.set_printoptions(precision=3)
# X_reduced = fit.transform(X)
# # summarize selected features
# print(X_reduced.shape)

# feature_red_name = format(fit)