import numpy as np

match = -3
blank = 5
sub = 1
gap = '-'
d=3

#class that is contains a 'value' or distance and a pointer ot the previous distance index
class dist_value:
    def __init__(self, value, prev_dist_index: tuple[int,int] = None):
        self.value = value
        self.prev_dist_index = prev_dist_index

    def set_pointer(self, dist):
        self.prev_dist_index = dist

    def __str__(self):
        return f"{self.value}"


def print_dict(band_dict):
    for key, value in band_dict.items():
        print(key, value.value)


#initalizes the 'basecase' of the matrix
def intit_basecase(matrix, d_row, d_col):
    for i in range(1,d_col):
        matrix[(0,i)] = dist_value(matrix.get((0, i-1)).value + blank )
        matrix.get(tuple([0,i])).prev_dist_index = [0,i-1]
    for i in range(1,d_row):
        #if(band):
        matrix[(i,0)] = dist_value(matrix.get((i-1,0)).value + blank)
        matrix.get(tuple([i,0])).prev_dist_index = [i-1,0] 
    
    return None

#this is used to calculate the distance to take in the matrix 
def calculate_dist(diag, up, side, seq1: str, seq2: str, 
                row_index, col_index) -> tuple[int, tuple[int, int]]:
    if(side!=None):
        side = side.value+blank
    if(up!= None):
        up = up.value+blank
    index = None
    if seq1[row_index] == seq2[col_index]:
        diag = diag.value+match
    else:
        diag = diag.value +sub
    dist = diag
    index = [row_index-1, col_index-1]
    if(up==None):
        if(side < diag):
            dist = side
            index = [row_index, col_index-1]
    elif(side==None):
        if(up < diag):
            dist = up
            index = [row_index-1, col_index]
    else:
        if (side < diag) and (side <= up):
            dist = side
            index = [row_index, col_index-1]
        elif (up < side) and (up < diag):
            dist = up
            index = [row_index-1, col_index]

    return dist, index


# this function gets the normal edit of a sequence
def normal_edit(seq1, seq2):
    dist = 0
    matrix = dict()
    matrix.update({tuple([0,0]): dist_value(0)})
    intit_basecase(matrix,len(seq1), len(seq2))
    fill_matrix(matrix, len(seq2), d, seq1, seq2, False)
    dist = matrix.get((len(seq1)-1, len(seq2)-1)).value

    return dist, matrix


#this function is used to get banded edit, calls same functions as normal edit but with diff values
def banded_edit(seq1: str, seq2: str, d, bandwidth):
    dist = 0
    band_dict = dict()
    band_dict.update({tuple([0,0]): dist_value(0)})
    intit_basecase(band_dict,d+1,d+1)
    if(d< (len(seq2)-1)):
        d=d+2
    fill_matrix(band_dict,d,bandwidth, seq1, seq2,True) 
    dist = band_dict.get((len(seq1)-1, len(seq2)-1)).value
    return dist, band_dict


#this function gets the alignment strings through the back pointers
def get_alignment(matrix, seq1, seq2):
    alg_mat = []
    align1 = ''
    align2 = ''
    alg_mat.append([len(seq1)-1,len(seq2)-1])
    i = len(seq1)-1
    j = len(seq2)-1
    while(1):
        prev = matrix.get((i,j)).prev_dist_index
        if(prev == [0,0]) or (prev == None):
            break
        alg_mat.append(prev)
        i = prev[0]
        j = prev[1]
    alg_mat.reverse()
    prev_i = -1
    prev_j = -1
    for val in alg_mat:
        if(val[0] == prev_i):
            align1 = align1 + gap
        else:
            align1 = align1 + seq1[val[0]]
        if(val[1] == prev_j):
            align2 = align2 + gap
        else:
            align2 = align2 + seq2[val[1]]
        prev_i = val[0]
        prev_j = val[1]
    return align1, align2 

# this funciton fills the 'matrix' for either banded or normal algorithm, sets bounds with different values
def fill_matrix(matrix, d, bandwidth, seq1, seq2, band: bool):
    b_col = 1
    at_bandwidth = False
    for i in range(1,len(seq1)):
        for j in range(b_col, d):
            dist, index = calculate_dist(matrix.get((i-1,j-1)), matrix.get((i-1,j)), 
                matrix.get((i,j-1)), seq1, seq2, i, j) # call function
            matrix[(i,j)] = dist_value(dist) #setting new dist_value
            matrix.get((i,j)).prev_dist_index = index 

        if(band):
            if(d != len(seq2)):
                d = d+1
            if(at_bandwidth):
                b_col = b_col+1 
            if(d > bandwidth):
                at_bandwidth = True

    return None 
            

# for right now it is str1 on row, str2 on col
'''here are some of my thoughts, so for normal obviously want to create a matrix with back pointers
if we are moving to the right, or down it will cost 5
a match will be moving diagonal with a cost of -3
a substitution will also be a diagonal move with cost of 1
whichever string is bigger goes on top, smaller one goes on bottom, we need the first 
value to be blank on both strings
the 'backpointers' of the data structure should be the indexes not the distance value
seq1_len = len(seq1)
    seq2_len = len(seq2)
    if(seq1_len > seq2_len):
        matrix = np.empty(seq2_len, seq1_len)
    else:
        matrix = np.empty(seq1_len, seq2_len)
'''

def align(
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1,
        gap='-'
) -> tuple[float, str | None, str | None]:
    match = match_award
    blank = indel_penalty
    sub = sub_penalty 
    gap = gap
    seq1 = gap + seq1
    seq2 = gap + seq2
    d = banded_width
    band = (2*d)+1
    if(banded_width == -1):
        dist, matrix = normal_edit(seq1, seq2)
    else:
        dist, matrix = banded_edit(seq1, seq2,d, band)


    alignment1, alignment2 = get_alignment(matrix,seq1,seq2)

    return int(dist), alignment1, alignment2
    """
        Align seq1 against seq2 using Needleman-Wunsch
        Put seq1 on left (j) and seq2 on top (i)
        => matrix[i][j]
        :param seq1: the first sequence to align; should be on the "left" of the matrix
        :param seq2: the second sequence to align; should be on the "top" of the matrix
        :param match_award: how many points to award a match
        :param indel_penalty: how many points to award a gap in either sequence
        :param sub_penalty: how many points to award a substitution
        :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
        :param gap: the character to use to represent gaps in the alignment strings
        :return: alignment cost, alignment 1, alignment 2
    """

'''def main():
    str1 = "hey"
    str2 = "he"
    dist2, a2, b2 = align("ATGCATGC", "ATGGTGC")
    #dist2, a2, b2 = align("ATGCATGC", "ATGGTGC")
    print(a2)
    print(b2)
    print(dist2)
    #dist, a, b = align("ACAATCC", "AGCATGC", banded_width=3)
    #dist, a, b = align("GGGGTTTTAAAACCCCTTTT", "TTTTAAAACCCCTTTTGGGG", banded_width=2)
    #dist, a, b = align("ATGCATGC", "ATGGTGC", banded_width=3)
    dist, a, b = align("ataagagtgattggcgatatcggctccgtacgtaccctttctactctcgggctcttccccgttagtttaaatctaatctctttataaacggcacttcc", 
        "ataagagtgattggcgtccgtacgtaccctttctactctcaaactcttgttagtttaaatctaatctaaactttataaacggcacttcctgtgtgtccat", banded_width=20)
    print(a)
    print(b)
    print(dist)
   
   
  
   # normal_edit(str1, str2)



if __name__ == "__main__":
    main()'''
