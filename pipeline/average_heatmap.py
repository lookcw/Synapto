
from regions import regions
import numpy as np

def average_heatmap(correlation_matrix,regionalization):
    corre_regions = regions[regionalization]
    num_regions = len(corre_regions)
    regionalized_matrix = np.ones((num_regions,num_regions))
    
    sorted_region_names = sorted(corre_regions.keys())
    for i in range(len(sorted_region_names)):
        for j in range(len(sorted_region_names)):
            if i>=j:
                avg = _add_correlation(corre_regions[sorted_region_names[i]],corre_regions[sorted_region_names[j]],correlation_matrix)
                regionalized_matrix[i][j] = avg
                regionalized_matrix[j][i] = avg
    return regionalized_matrix[np.triu_indices(len(corre_regions), 0)]


def _add_correlation(region1,region2,correlation_matrix):
    region1, region2 = np.array(region1),np.array(region2)
    return correlation_matrix[region1[:, None],region2].mean()

def regions_header(regionalization):
    sorted_region_names = sorted(regions[regionalization].keys())
    return [sorted_region_names[i]+'_'+sorted_region_names[j] 
    for j in range(len(sorted_region_names)) 
    for i in range(len(sorted_region_names))
    if i>=j]
