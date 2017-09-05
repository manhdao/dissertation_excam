import numpy as np
from sklearn.metrics import confusion_matrix


def dynamic_time_warp(seq_a, seq_b, _dist='square', normalization='none', print_mat=False, print_path=False):
    """Implement the crude DTW algorithm
    ---
    _dist: Method of calculate distance between 2 number. Choose from 'square' or 'absolute'
    normalization: Normalize the DTW distance. Choose from 'none' or 'path' (divided by optimal warping path)
                                                or 'short' (shorter series) or 'long' (longer series)"""

    if _dist == 'absolute':
        distance = lambda x,y: abs(x-y)
    elif _dist == 'square':
        distance = lambda x,y: (x-y)**2
    else:
        raise ValueError(_dist+ ' is not a correct distance measure. Choose from absolute and square')

    # Special cases: either series have no data
    if len(seq_a) == 0 or len(seq_b) == 0:
        return 0.0, []
      
    # create the cost matrix with an extra row and column, to facilitate finding optimal path
    num_rows, num_cols = len(seq_a), len(seq_b)
    dtw_matrix = np.zeros((num_rows+1, num_cols+1))
    
    #set up the matrix. The 1st row and column are not used
    for i in range(0, num_rows+1):
        for j in range(0, num_cols+1):
            dtw_matrix[i,j] = float('inf')
    dtw_matrix[0,0] = 0 

    for i in range(1, num_rows+1):
        for j in range(1, num_cols+1):
            # classical DTW function
            choices = dtw_matrix[i-1,j], dtw_matrix[i,j-1], dtw_matrix[i-1,j-1]
            dtw_matrix[i,j] = distance(seq_a[i-1], seq_b[j-1]) + min(choices) # index i-1, j-1 because 1st row 
                                                                              # and column of matrix are not used   
            
    if print_mat == True:
        print(dtw_matrix[1:,1:])
        
    # find optimal path
    r, c = num_rows, num_cols
    path = []
    
    while (r,c) != (1,1):
        path.append((r-1,c-1))

        # go backward from the bottom right cell up to [0,0]
        prev = min(dtw_matrix[r-1,c], dtw_matrix[r,c-1], dtw_matrix[r-1,c-1])
        if dtw_matrix[r-1,c-1] == prev:
            r, c = r-1, c-1
        else:
            r, c = min((r-1, c), (r, c-1), key = lambda x: dtw_matrix[x[0], x[1]])
    path.append((0,0))
    
    if print_path == True:
        print(path)
    
    if normalization == 'none':
        return np.sqrt(dtw_matrix[-1,-1]), path
    elif normalization == 'path':
        return np.sqrt(dtw_matrix[-1,-1])/len(path), path
    elif normalization == 'short':
        return np.sqrt(dtw_matrix[-1,-1])/min(num_rows,num_cols), path
    elif normalization == 'long':
        return np.sqrt(dtw_matrix[-1,-1])/max(num_rows,num_cols), path
    else:
        raise ValueError(normalization+ ' is not a correct normalization choice . Choose from none, path, '+ \
                                        'short, or long')


def condensed_matrix(seq, dist, **kwargs):
    """Calculate condensed dtw distance matrix of sub_sequences in a sequence,
    similar to scipy.spatial.distance.pdist"""
    
    length = len(seq)
    arr = []
    for i in range(0,length-1):
        for j in range(i+1, length):
            if dist == 'dtw':
                arr.append(dynamic_time_warp(seq[i],seq[j], **kwargs)[0])
            elif dist == 'levenshtein':
                arr.append(levenshtein(seq[i],seq[j], **kwargs))
            else:
                raise ValueError(dist+ ' is not a correct distance measure. Choose from dtw and levenshtein.')
    return arr



def distance_matrix(seq, dist, **kwargs):
    """Calculate distance dtw matrix of sub_sequences in a sequence, similar to scipy.spatial.distance.squareform"""

    length = len(seq)
    dist_mat = np.zeros((length, length))

    for i in range(0, length):
        dist_mat[i,i] = 0.

    for i in range(0, length):
        for j in range(i+1, length):
            if dist == 'dtw':
                dist_mat[i,j] = dynamic_time_warp(seq[i],seq[j], **kwargs)[0]
            elif dist == 'levenshtein':
                dist_mat[i,j] = levenshtein(seq[i],seq[j], **kwargs)
            else:
                raise ValueError(dist+ ' is not a correct distance measure. Choose from dtw and levenshtein.')
            dist_mat[j,i] = dist_mat[i,j]
    
    return dist_mat



def cross_distance_matrix(seq_a, seq_b, dist, **kwargs):
    """Calculate cross dtw distance matrix of sub_sequences in 2 sequences.
    ---
    dist: dtw or levenshtein"""
    
    arr = []
    for i in range(0,len(seq_a)):
        for j in range(0, len(seq_b)):
            if dist == 'dtw':
                arr.append(dynamic_time_warp(seq_a[i],seq_b[j], **kwargs)[0])
            elif dist == 'levenshtein':
                arr.append(levenshtein(seq_a[i],seq_b[j], **kwargs))
            else:
                raise ValueError(dist+ ' is not a correct distance measure. Choose from dtw and levenshtein.')
    
    return arr



def levenshtein(seq_a, seq_b, sub_cost=2, normalization='none', print_mat=False, print_path=False):
    """Implement the crude Levenshtein distance algorithm.
    ---
    normalization: Normalize the DTW distance. Choose from 'none' or 'short' (divided by shorter series)
                                                        or 'long' (longer series)"""

    # Special cases: either series have no data
    if len(seq_a) == 0 or len(seq_b) == 0:
        return 0.0, []

    # create the cost matrix with an extra row and column, as it is the algorithm
    num_rows, num_cols = len(seq_a), len(seq_b)
    lv_matrix = np.zeros((num_rows+1, num_cols+1))
    
    # filling in the edit distances
    for i in range(0, num_rows+1):
        lv_matrix[i, 0] = i
    for j in range(0, num_cols+1):
        lv_matrix[0,j] = j
    
    for i in range(1, num_rows+1):
        for j in range(1, num_cols+1):
            # classical levenshtein algorithm
            if seq_a[i-1] == seq_b[j-1]:
                substitution_cost = 0
            else:
                substitution_cost = sub_cost
            choices = lv_matrix[i-1,j]+1, lv_matrix[i,j-1]+1, lv_matrix[i-1,j-1]+substitution_cost
            lv_matrix[i,j] = min(choices)
    
    if print_mat == True:
        print(lv_matrix)

    if normalization == 'none':
        return lv_matrix[-1,-1]
    elif normalization == 'short':
        return lv_matrix[-1,-1]/np.sqrt(min(num_rows,num_cols))
    elif normalization == 'long':
        return lv_matrix[-1,-1]/np.sqrt(max(num_rows,num_cols))
    else:
        raise ValueError(normalization+ ' is not a correct normalization choice. Choose from none\
                                        short, or long')



def purity_score(y_true, y_cluster):
    """Calculate the purity score for the given cluster assignments and ground truth"""
    
    con_mat = confusion_matrix(y_true, y_cluster)    
    max_in_cluster = np.amax(con_mat,axis=0)
    
    return np.sum(max_in_cluster) / np.sum(con_mat)




####### DEPRECATED #######



def dynamic_time_warp_local_constraint(seq_a, seq_b, window=0, _dist='square', normalization='none', 
                            print_mat=False, print_path=False): # deprecated
    """Implement the crude DTW algorithm, with window of local constraint.
    ---
    _dist: Method of calculate distance between 2 number. 'square' or 'absolute'
    normalization: Normalize the DTW distance. 'none' or 'path' (divided by optimal warping path)
                                                or 'short' (shorter series) or 'long' (longer series)

    """

    if _dist == 'absolute':
        distance = lambda x,y: abs(x-y)
    elif _dist == 'square':
        distance = lambda x,y: (x-y)**2

    if len(seq_a) == 0 or len(seq_b) == 0:
        return 0.0, []
    
    # create the cost matrix with an extra row and column, to facilitate finding optimal path
    num_rows, num_cols = len(seq_a), len(seq_b)
    dtw_matrix = np.zeros((num_rows+1, num_cols+1))

    if window == 0:
        window = int(2*num_cols//3)
    window = max(window, abs(num_rows-num_cols))

    #set up the matrix. The 1st row and column are not used
    for i in range(0, num_rows+1):
        for j in range(0, num_cols+1):
            dtw_matrix[i,j] = float('inf')
    dtw_matrix[1,1] = distance(seq_a[0], seq_b[0])        
    
    if len(seq_a) > 1:
        dtw_matrix[2,1] = distance(seq_a[1], seq_b[0]) + dtw_matrix[1,1]
        nr2 = int(num_rows//2)
        # add some distances in first column to ensure accuracy
        for i in range(3,nr2+1):
            try:
                dtw_matrix[i,1] = distance(seq_a[i-1], seq_b[0]) + dtw_matrix[i-1,1]
            except:
                break
    
    if len(seq_b) == 1:
        # fill in the distances
        for i in range(2, num_rows+1):
            dtw_matrix[i,1] = distance(seq_a[i-1], seq_b[0]) + dtw_matrix[i-1,1]

    if len(seq_b) > 1:
        # fill in the distances
        for i in range(1, num_rows+1):
            for j in range(max(2, i-window), min(num_cols+1, i+window+1)):
                # classical DTW function
                choices = dtw_matrix[i-1,j], dtw_matrix[i,j-1], dtw_matrix[i-1,j-1]
                dtw_matrix[i,j] = distance(seq_a[i-1], seq_b[j-1]) + min(choices) # index i-1, j-1 because 1st row 
                                                                                  # and column of matrix are not used
            
    if print_mat == True:
        print(dtw_matrix[1:,1:])
        
    # find optimal path
    r, c = num_rows, num_cols
    path = []
    
    while (r,c) != (1,1):
        path.append((r-1,c-1))

        # go backward from the bottom right cell up to [0,0]
        prev = min(dtw_matrix[r-1,c], dtw_matrix[r,c-1], dtw_matrix[r-1,c-1])
        if dtw_matrix[r-1,c-1] == prev:
            r, c = r-1, c-1
        else:
            r, c = min((r-1, c), (r, c-1), key = lambda x: dtw_matrix[x[0], x[1]])
    path.append((0,0))
    
    if print_path == True:
        print(path)
    
    if normalization == 'none':
        return np.sqrt(dtw_matrix[-1,-1]), path
    elif normalization == 'path':
        return np.sqrt(dtw_matrix[-1,-1])/len(path), path
    elif normalization == 'short':
        return np.sqrt(dtw_matrix[-1,-1])/min(num_rols,num_cols), path
    elif normalization == 'long':
        return np.sqrt(dtw_matrix[-1,-1])/max(num_rols,num_cols), path
    else:
        raise ValueError(normalization+ ' is not a correct normalization choice. Choose from none, path, '+ \
                                        'short, or long')