
def average_heatmap(matrix):
    # Temporal/Left, Central, Temporal/Right, Posterior
    regions = [[0,1,2,4,6],[3,8,13],[5,9,10,11,15],[7,12,17],[14,16,18,19,20]]

    region_matrix = []
    for i in range(len(regions)):
        arr = []
        for j in range(len(regions)):
            arr.append(1)
        region_matrix.append(arr)
    

    for i in range(len(regions)):
        for j in range(i+1,len(regions)):
            _add_correlation(i, j, matrix, regions, region_matrix)

    #print(region_matrix)
    return region_matrix


def _add_correlation(i,j, matrix, regions, region_matrix):
    sum = 0
    count = 0

    for x in regions[i]:
        for y in regions[j]:
            sum += matrix[x][y]
            count += 1
    
    avg = sum/count

    region_matrix[i][j] = avg
    region_matrix[j][i] = avg
     


import numpy as np
matrix = np.random.rand(21,21)
average_heatmap(matrix)


#average_heatmap([[1,4,2,3],[4,1,2,2],[2,2,1,1],[3,2,1,1]], [[0,1,2],[3]])

# 1 4 2 3
# 4 1 2 2
# 2 2 1 1
# 3 2 1 1

# regions = [[1,7,12],[3,6,10],etc...]

# take 9 intersections of [1,7,12],[3,6,10] in matrix and average value
# this average value is correlation value between these 2 regions
# create new list/matrix of regional correlations
