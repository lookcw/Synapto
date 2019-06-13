import tsfresh
from tsfresh import extract_features
import pandas as pd



def extractTsFreshFeatures(time_series_electrode):
    time_series_df = pd.DataFrame(data=time_series_electrode)
    time_series_df['id'] =  len(time_series_df.index)*[1]
    extracted_features = extract_features(time_series_df,column_id = 'id')
    print extract_features.head(10)
    return extract_features
