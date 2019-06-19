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