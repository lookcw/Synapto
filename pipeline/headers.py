from regions import regions


def compareHeader(time_series_electrode):
    num_cols = time_series_electrode.shape[1]
    header = []
    for i in range(1, num_cols+1):
        for j in range(i+1, num_cols+1):
            header.append('e'+str(i)+'_e'+str(j))
    return header


def linearHeader(time_series_electrode):
    num_cols = time_series_electrode.shape[1]
    header = []
    for i in range(1, num_cols+1):
        header.append('e'+str(i))
    return header


def ordered_linear_region_header(region):
    """Returns column headers of regionalized electrodes given region string

    Args:
        region_name (str): name of regionalization schema

    Returns:
        [str]: list of headers
    """

    if isinstance(region, str):
        return sorted(regions[region].keys())
    elif isinstance(region, dict):
        return sorted(region.keys())


def ordered_compare_region_header(region):
    if isinstance(region, str):
        region_names = regions[region].keys()
    elif isinstance(region, dict):
        region_names = region.keys()
    sorted_region_names = sorted(region_names)
    return [sorted_region_names[i]+'_'+sorted_region_names[j]
            for j in range(len(sorted_region_names))
            for i in range(len(sorted_region_names))
            if i > j]

def ordered_compare_region_pairs(region):
    if isinstance(region, str):
        region_names = regions[region].keys()
    elif isinstance(region, dict):
        region_names = region.keys()
    sorted_region_names = sorted(region_names)
    return [(sorted_region_names[i],sorted_region_names[j])
            for j in range(len(sorted_region_names))
            for i in range(len(sorted_region_names))
            if i > j]