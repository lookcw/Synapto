def compareHeader(time_series_electrode):
    num_cols = time_series_electrode.shape[1]
    header = []
    for i in range(1,num_cols+1):
        for j in range(i+1,num_cols+1):
            header.append('e'+str(i)+'_e'+str(j))
    return header

def linearHeader(time_series_electrode):
    num_cols = time_series_electrode.shape[1]
    header = []
    for i in range(1,num_cols+1):
        header.append('e'+str(i))    
    return header

def regionHeader(num_regions):
    header = []
    # Anterior, Temporal/Left, Central, Temporal/Right, Posterior
    regions = ['A','TL','C','TR','P']
    for i in range(num_regions):
        for j in range(i+1,num_regions):
            header.append(f'{regions[i]}_{regions[j]}')
    print(header)
    return header